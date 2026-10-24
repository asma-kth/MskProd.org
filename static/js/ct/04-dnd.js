/* Drag and drop for every card game, with two ways round it.
 *
 *   drag      press, move and release, with a mouse, a finger or a pen
 *   pick      tap or click a card, then tap or click where it goes
 *   keyboard  Tab to a card, Enter to pick it up, Tab to a box, Enter to drop;
 *             in a list, the arrow keys move a picked card up and down
 *
 * The engine owns the model. This module only reports "card X to zone Y at
 * position i" through onMove and the engine redraws, so all three ways run the
 * same code. Events are delegated from the board, so a redraw never loses them.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  CT.dnd = function (board, opts) {
    opts = opts || {};
    var picked = null, drag = null, lastFocus = null;
    var axis = opts.axis || "y";

    function itemOf(t) { var n = t && t.closest ? t.closest("[data-item]") : null; return n && board.contains(n) ? n : null; }
    function zoneOf(t) { var n = t && t.closest ? t.closest("[data-zone]") : null; return n && board.contains(n) ? n : null; }
    function zoneItems(z) { return Array.prototype.filter.call(z.querySelectorAll("[data-item]"), function (n) { return zoneOf(n.parentNode) === z; }); }
    function label(n) { return n.getAttribute("aria-label") || n.textContent.trim(); }

    function setPicked(n) {
      Array.prototype.forEach.call(board.querySelectorAll("[data-item].is-picked"), function (x) {
        x.classList.remove("is-picked"); x.setAttribute("aria-pressed", "false");
      });
      picked = n ? n.getAttribute("data-item") : null;
      board.classList.toggle("ct-picking", !!picked);
      if (n) {
        n.classList.add("is-picked"); n.setAttribute("aria-pressed", "true");
        CT.sound.play("pick");
        CT.announce("Picked up " + label(n) + ". Now choose where it goes, or press Escape.");
      }
    }

    function move(itemId, zone, index) {
      var zid = zone.getAttribute("data-zone");
      if (opts.canDrop && !opts.canDrop(itemId, zid)) { CT.sound.play("bad"); return; }
      lastFocus = itemId;
      setPicked(null);
      opts.onMove(itemId, zid, index);
      CT.sound.play("drop");
      var z = board.querySelector('[data-zone="' + zid + '"]');
      CT.announce("Placed in " + (z ? (z.getAttribute("data-zone-label") || label(z)) : zid) + ".");
      setTimeout(function () {
        var n = board.querySelector('[data-item="' + lastFocus + '"]');
        if (n && opts.keepFocus !== false) n.focus({ preventScroll: true });
      }, 0);
    }

    // Where in a zone's list a point falls: before the first card whose middle is past it.
    function indexAt(zone, x, y, exceptId) {
      var items = zoneItems(zone).filter(function (n) { return n.getAttribute("data-item") !== exceptId; });
      for (var i = 0; i < items.length; i++) {
        var r = items[i].getBoundingClientRect();
        if (axis === "x" ? x < r.left + r.width / 2 : (axis === "grid" ? (y < r.top + r.height / 2 && x < r.right) || y < r.top : y < r.top + r.height / 2)) return i;
      }
      return items.length;
    }

    // ------------------------------------------------------- pointer drag
    function onDown(e) {
      if (e.button !== undefined && e.button !== 0) return;
      var it = itemOf(e.target);
      if (!it || it.getAttribute("aria-disabled") === "true") return;
      drag = { id: it.getAttribute("data-item"), node: it, x0: e.clientX, y0: e.clientY, on: false, pid: e.pointerId };
    }
    function startDrag(e) {
      var r = drag.node.getBoundingClientRect();
      var g = drag.node.cloneNode(true);
      g.removeAttribute("id");
      g.className += " ct-ghost";
      g.style.width = r.width + "px";
      g.style.left = "0px"; g.style.top = "0px";
      g.setAttribute("aria-hidden", "true");
      document.body.appendChild(g);
      drag.ghost = g; drag.dx = e.clientX - r.left; drag.dy = e.clientY - r.top; drag.on = true;
      drag.node.classList.add("is-dragging");
      board.classList.add("ct-dragging");
      try { drag.node.setPointerCapture(drag.pid); } catch (err) { /* older browsers */ }
      CT.sound.play("pick");
    }
    function onMoveEvt(e) {
      if (!drag) return;
      if (!drag.on) {
        if (Math.abs(e.clientX - drag.x0) + Math.abs(e.clientY - drag.y0) < 7) return;
        startDrag(e);
      }
      e.preventDefault();
      drag.ghost.style.transform = "translate(" + (e.clientX - drag.dx) + "px," + (e.clientY - drag.dy) + "px) rotate(-2deg)";
      var under = document.elementFromPoint(e.clientX, e.clientY);
      var z = zoneOf(under);
      Array.prototype.forEach.call(board.querySelectorAll("[data-zone].is-over"), function (n) { if (n !== z) n.classList.remove("is-over"); });
      if (z) z.classList.add("is-over");
      drag.zone = z;
      if (e.clientY < 70) root.scrollBy(0, -14);
      else if (e.clientY > root.innerHeight - 70) root.scrollBy(0, 14);
    }
    function onUp(e) {
      if (!drag) return;
      var d = drag;
      drag = null;
      if (!d.on) return;           // a click: handled by onClick
      d.node.classList.remove("is-dragging");
      board.classList.remove("ct-dragging");
      if (d.ghost) d.ghost.remove();
      Array.prototype.forEach.call(board.querySelectorAll("[data-zone].is-over"), function (n) { n.classList.remove("is-over"); });
      d.node.setAttribute("data-just-dragged", "1");
      setTimeout(function () { d.node.removeAttribute("data-just-dragged"); }, 0);
      if (d.zone) move(d.id, d.zone, indexAt(d.zone, e.clientX, e.clientY, d.id));
    }
    function onCancel() {
      if (!drag) return;
      if (drag.ghost) drag.ghost.remove();
      if (drag.node) drag.node.classList.remove("is-dragging");
      board.classList.remove("ct-dragging");
      drag = null;
    }

    // ---------------------------------------------------- click and keys
    function onClick(e) {
      var it = itemOf(e.target);
      if (it && it.getAttribute("data-just-dragged")) return;
      var z = zoneOf(e.target);
      if (it) {
        var id = it.getAttribute("data-item");
        if (picked && picked !== id && z && opts.dropOnItem !== false) {
          // dropping onto a card in a list puts the picked card before it
          var idx = zoneItems(z).indexOf(it);
          move(picked, z, idx < 0 ? zoneItems(z).length : idx);
          return;
        }
        setPicked(picked === id ? null : it);
        if (picked === null) CT.announce("Put down.");
        return;
      }
      if (z && picked) {
        e.preventDefault();
        move(picked, z, zoneItems(z).length);
      }
    }
    function onKey(e) {
      if (e.key === "Escape" && picked) { setPicked(null); CT.announce("Put down."); return; }
      var it = itemOf(e.target), z = zoneOf(e.target);
      if ((e.key === "Enter" || e.key === " ") && z && !it && picked) {
        e.preventDefault();
        move(picked, z, zoneItems(z).length);
        return;
      }
      if (opts.sortable && it && picked === it.getAttribute("data-item") && (e.key === "ArrowUp" || e.key === "ArrowDown" || e.key === "ArrowLeft" || e.key === "ArrowRight")) {
        e.preventDefault();
        var zone = zoneOf(it.parentNode), list = zoneItems(zone), i = list.indexOf(it);
        var j = (e.key === "ArrowUp" || e.key === "ArrowLeft") ? i - 1 : i + 2;
        if (j < 0 || j > list.length) return;
        move(picked, zone, j);
        setTimeout(function () { var n = board.querySelector('[data-item="' + lastFocus + '"]'); if (n) setPicked(n); }, 0);
      }
    }

    board.addEventListener("pointerdown", onDown);
    root.addEventListener("pointermove", onMoveEvt, { passive: false });
    root.addEventListener("pointerup", onUp);
    root.addEventListener("pointercancel", onCancel);
    board.addEventListener("click", onClick);
    board.addEventListener("keydown", onKey);

    return {
      picked: function () { return picked; },
      cancel: function () { setPicked(null); },
      destroy: function () {
        board.removeEventListener("pointerdown", onDown);
        root.removeEventListener("pointermove", onMoveEvt);
        root.removeEventListener("pointerup", onUp);
        root.removeEventListener("pointercancel", onCancel);
        board.removeEventListener("click", onClick);
        board.removeEventListener("keydown", onKey);
        onCancel();
      }
    };
  };

  // The Watch step: a hand carries a copy of a card to where it belongs.
  CT.ghost = function (fromEl, toEl, done) {
    if (!fromEl || !toEl || CT.calm()) { done(); return; }
    var a = fromEl.getBoundingClientRect(), b = toEl.getBoundingClientRect();
    var g = fromEl.cloneNode(true);
    g.className += " ct-ghost ct-ghost-demo";
    g.style.width = a.width + "px";
    g.setAttribute("aria-hidden", "true");
    var hand = CT.el("div", { class: "ct-hand", "aria-hidden": "true" });
    hand.innerHTML = '<svg viewBox="0 0 32 32"><path d="M11 3c1.7 0 3 1.3 3 3v8.2l1.2-.6c1.4-.6 3 .1 3.5 1.5l.2.4 1.3-.5c1.4-.5 2.9.2 3.4 1.6l.1.3c1.5-.4 3 .5 3.4 2l1.1 4.3c.6 2.4-.3 4.9-2.3 6.3L24 32H12l-6.3-8.6c-.9-1.2-.7-2.9.5-3.8 1.1-.9 2.7-.8 3.7.2L8 17V6c0-1.7 1.3-3 3-3z" fill="#fff" stroke="#0F2026" stroke-width="1.6"/></svg>';
    document.body.appendChild(g);
    document.body.appendChild(hand);
    var x0 = a.left, y0 = a.top, x1 = b.left + b.width / 2 - a.width / 2, y1 = b.top + Math.min(b.height / 2, 60) - a.height / 2;
    var t0 = null, dur = 1100;
    function frame(t) {
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / dur), e = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
      var x = x0 + (x1 - x0) * e, y = y0 + (y1 - y0) * e - Math.sin(Math.PI * e) * 40;
      g.style.transform = "translate(" + x + "px," + y + "px)";
      hand.style.transform = "translate(" + (x + a.width / 2) + "px," + (y + a.height / 2) + "px)";
      if (p < 1) requestAnimationFrame(frame);
      else setTimeout(function () { g.remove(); hand.remove(); done(); }, 160);
    }
    g.style.left = "0px"; g.style.top = "0px";
    requestAnimationFrame(frame);
  };
})(typeof window !== "undefined" ? window : globalThis);
