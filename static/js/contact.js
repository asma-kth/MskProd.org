/* The contact form. It sends nothing itself: it writes the message and opens
   the reader's own email program, so they can check it and send it from their
   own address. The page address and question come from the report link that
   led here. */
(function () {
  "use strict";
  var form = document.querySelector("[data-contact-form]");
  if (!form) return;
  var to = form.getAttribute("data-to");
  var params = new URLSearchParams(location.search);
  var field = function (name) { return form.querySelector('[name="' + name + '"]'); };

  Array.prototype.forEach.call(field("type").options, function (o) {
    if (o.value === params.get("type")) field("type").value = o.value;
  });
  if (params.get("page")) field("page").value = "https://mskprod.org" + params.get("page");
  if (params.get("q")) field("question").value = params.get("q");

  function message() {
    var type = field("type");
    var label = type.options[type.selectedIndex].text;
    var page = field("page").value.trim();
    var question = field("question").value.trim();
    var subject = label + (page ? ": " + page.replace(/^https?:\/\/[^/]+/, "") : "") + (question ? ", question " + question : "");
    var body = [
      "What it is about: " + label,
      "Page: " + (page || "not given"),
      "Question: " + (question || "not given"),
      "I am a: " + field("role").value,
      "",
      field("details").value.trim(),
      ""
    ].join("\n");
    return { subject: subject, body: body };
  }

  var status = form.querySelector("[data-contact-status]");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!field("details").value.trim()) {
      status.textContent = "Please say what is wrong, or what you need, before sending.";
      field("details").focus();
      return;
    }
    var m = message();
    status.textContent = "Your email program should open with the message written. If nothing happens, use Copy the message and paste it into an email to " + to + ".";
    location.href = "mailto:" + to + "?subject=" + encodeURIComponent(m.subject) + "&body=" + encodeURIComponent(m.body);
  });

  var copy = form.querySelector("[data-contact-copy]");
  copy.addEventListener("click", function () {
    var m = message();
    var text = "To: " + to + "\nSubject: " + m.subject + "\n\n" + m.body;
    var done = function () { status.textContent = "Copied. Paste it into a new email to " + to + "."; };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { status.textContent = text; });
    } else {
      status.textContent = text;
    }
  });
})();
