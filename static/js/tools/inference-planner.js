/* Inference planner: how many GPUs does it take to serve a language model?
 *
 * Memory is the weights plus the KV cache (Level 10), which grows with the
 * context length and the number of conversations served at once. Speed uses
 * the memory-bandwidth model from the lesson: every generated token needs the
 * weights, and each conversation's cache, read from memory once. Both are
 * deliberately simple first estimates, and the page says so.
 */
(function () {
  "use strict";

  var MODELS = {
    m7: { label: "7B, full attention (32 layers)", params: 7e9, layers: 32, kv: 4096 },
    m8: { label: "8B, grouped-query attention (32 layers)", params: 8e9, layers: 32, kv: 1024 },
    m70: { label: "70B, grouped-query attention (80 layers)", params: 70e9, layers: 80, kv: 1024 }
  };
  var GPUS = {
    g24: { label: "24 GB gaming GPU, about 1 TB/s", mem: 24, bw: 1.0e12 },
    g80: { label: "80 GB data-centre GPU, about 3.3 TB/s", mem: 80, bw: 3.35e12 }
  };

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }
  function gb(bytes) { return bytes / 1e9; }
  function fmtGB(v) { return v >= 100 ? v.toFixed(0) + " GB" : v >= 10 ? v.toFixed(1) + " GB" : v.toFixed(2) + " GB"; }

  function build(body) {
    body.textContent = "";
    var row = el("div", "tool-row");
    function field(label, ctrl, out) {
      var f = el("div", "tool-field"), id = "ip-" + Math.random().toString(36).slice(2, 8);
      var l = el("label", null, label); l.setAttribute("for", id); ctrl.id = id;
      f.appendChild(l); f.appendChild(ctrl); if (out) f.appendChild(out); row.appendChild(f); return f;
    }
    function select(options, val) {
      var s = el("select");
      options.forEach(function (o) { var n = el("option", null, o[1]); n.value = o[0]; s.appendChild(n); });
      s.value = val; return s;
    }
    var sModel = select(Object.keys(MODELS).map(function (k) { return [k, MODELS[k].label]; }), "m8");
    field("Model", sModel);
    var sBits = select([["16", "16-bit"], ["8", "8-bit"], ["4", "4-bit"]], "16");
    field("Weights stored as", sBits);
    var sCtx = select([["2048", "2,000 tokens"], ["8192", "8,000 tokens"], ["32768", "32,000 tokens"], ["131072", "128,000 tokens"]], "8192");
    field("Context per conversation", sCtx);
    var sUsers = el("input"); sUsers.type = "range"; sUsers.min = "1"; sUsers.max = "64"; sUsers.step = "1"; sUsers.value = "8";
    var oUsers = el("span", "ip-num", "8");
    field("Conversations at once", sUsers, oUsers);
    var sGpu = select(Object.keys(GPUS).map(function (k) { return [k, GPUS[k].label]; }), "g80");
    field("GPU", sGpu);

    var gpusBox = el("div", "ip-gpus");
    var legend = el("p", "ip-legend");
    [["ip-w", "weights"], ["ip-k", "KV cache"], ["ip-o", "working space"], ["ip-f", "free"]].forEach(function (p) {
      var s = el("span", "ip-key " + p[0]); legend.appendChild(s); legend.appendChild(document.createTextNode(" " + p[1] + "   "));
    });
    var table = el("dl", "ip-facts");
    var status = el("p", "tool-status"); status.setAttribute("role", "status"); status.setAttribute("aria-live", "polite");
    var note = el("p", "tool-note", "First estimates only. Memory is weights + KV cache + 10% working space; the speed is the memory-bandwidth limit, assuming each conversation is half way through its context. Real systems also lose time to scheduling and arithmetic.");

    function fact(term, value, sub) {
      var d = el("div", "ip-fact");
      d.appendChild(el("dt", null, term));
      var dd = el("dd", null, value);
      if (sub) { dd.appendChild(el("span", "ip-sub", sub)); }
      d.appendChild(dd); table.appendChild(d);
    }

    function update() {
      var m = MODELS[sModel.value], g = GPUS[sGpu.value], bits = +sBits.value, ctx = +sCtx.value, users = +sUsers.value;
      oUsers.textContent = String(users);
      var weights = m.params * bits / 8;
      var kvPerToken = 2 * m.layers * m.kv * 2;                // keys and values, 16-bit, every layer
      var kv = kvPerToken * ctx * users;
      var work = 0.1 * (weights + kv);
      var total = weights + kv + work;
      var n = Math.max(1, Math.ceil(gb(total) / g.mem));
      // memory-bound decoding: each step reads the weights once and each cache (half full on average)
      var stepTime = (weights + kvPerToken * ctx * 0.5 * users) / (g.bw * n);
      var perUser = 1 / stepTime, totalRate = users / stepTime;

      gpusBox.textContent = "";
      var per = gb(total) / n;
      for (var i = 0; i < Math.min(n, 16); i++) {
        var card = el("div", "ip-gpu"), bar = el("div", "ip-bar");
        [["ip-w", gb(weights) / n], ["ip-k", gb(kv) / n], ["ip-o", gb(work) / n]].forEach(function (p) {
          var seg = el("span", "ip-seg " + p[0]); seg.style.height = Math.min(100, 100 * p[1] / g.mem).toFixed(2) + "%"; bar.appendChild(seg);
        });
        card.appendChild(bar);
        card.appendChild(el("span", "ip-cap", "GPU " + (i + 1) + ": " + fmtGB(per) + " of " + g.mem));
        gpusBox.appendChild(card);
      }
      if (n > 16) gpusBox.appendChild(el("p", "ip-more", "… and " + (n - 16) + " more GPUs"));

      table.textContent = "";
      fact("Weights", fmtGB(gb(weights)), m.params / 1e9 + " billion × " + bits + " bits");
      fact("KV cache per token", (kvPerToken / 1024).toFixed(0) + " KB", "2 × " + m.layers + " layers × " + m.kv + " numbers × 2 bytes");
      fact("KV cache in total", fmtGB(gb(kv)), ctx.toLocaleString("en-GB") + " tokens × " + users + (users === 1 ? " conversation" : " conversations"));
      fact("GPUs needed", String(n), fmtGB(gb(total)) + " in all");
      fact("Speed per conversation", perUser.toFixed(0) + " tokens/s", "at most");
      fact("Speed in total", totalRate.toFixed(0) + " tokens/s", users === 1 ? "for one conversation" : "across all " + users);
      status.textContent = "This set-up needs " + n + " GPU" + (n > 1 ? "s" : "") + ". Each conversation could get up to about " +
        perUser.toFixed(0) + " tokens per second" + (gb(kv) > gb(weights) ? "; the KV cache now needs more memory than the weights." : ".");
    }

    [sModel, sBits, sCtx, sGpu].forEach(function (c) { c.addEventListener("change", update); });
    sUsers.addEventListener("input", update);

    body.appendChild(row); body.appendChild(gpusBox); body.appendChild(legend); body.appendChild(table);
    body.appendChild(status); body.appendChild(note);
    update();
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="inference-planner"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
