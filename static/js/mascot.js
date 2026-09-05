/* Pixel, the MskProd robot cat. Encouragement, study tips and fun facts.
   Pixel is fully local: no network calls, no tracking, nothing leaves the device. */
(function () {
  "use strict";
  var store = window.MskStore || { get: function (k, f) { return f; }, set: function () {} };

  var FACTS = [
    "The word bug for a computer fault predates computers. Thomas Edison used it in 1878. The famous moth taped into a Harvard logbook in 1947 was funny precisely because engineers already said it.",
    "Ada Lovelace wrote what is generally accepted as the first published algorithm in 1843, for a machine that was never built. She also predicted computers would one day compose music.",
    "There are only two hard things in computer science, according to a well known joke: cache invalidation, naming things, and off by one errors.",
    "A modern phone processor performs more calculations in one second than every computer on Earth managed in the whole of 1970.",
    "The first computer virus for personal computers, Brain, was written in 1986 by two brothers in Lahore who included their real phone number in the code. People rang them to complain.",
    "Binary is not a computer invention. Gottfried Leibniz described the binary number system in 1703, over 240 years before ENIAC.",
    "The QWERTY keyboard layout was designed in the 1870s. Nobody has managed to replace it since, which is a perfect example of a legacy system.",
    "One petabyte is about 500 billion pages of typed text. Streaming services shift several petabytes every single day.",
    "The Apollo 11 guidance computer had around 4 KB of RAM. A single modern emoji, stored as an image, is bigger than that.",
    "Grace Hopper popularised the idea that programmers should write in English-like words rather than machine code. Her work led directly to COBOL, which still runs a large share of the world's banking.",
    "The internet and the World Wide Web are not the same thing. The internet is the network of networks. The web is one service that runs on top of it, invented by Tim Berners-Lee in 1989.",
    "Python is not named after the snake. Guido van Rossum named it after Monty Python's Flying Circus.",
    "A GIF image can only use 256 colours at once. That restriction is exactly why old GIFs look grainy, and it is a lossless compression trade-off in action.",
    "The first webcam was pointed at a coffee pot in Cambridge so researchers could see if it was empty before walking to it. Laziness has driven a surprising amount of computing.",
    "Sorting algorithms matter more than you think. Bubble sort on a million items would take hours. Merge sort would take about a second.",
    "Every time you load a web page over HTTPS your device and the server agree a shared secret in the open, without ever sending it. That is public key cryptography, and it is genuinely beautiful maths.",
    "The QR code was invented in 1994 for tracking car parts in a Japanese factory. It survived because it can still be read when up to 30 per cent of it is damaged.",
    "Moore's Law was never a law of physics. It was an observation Gordon Moore made in 1965 about transistor counts, and the industry then treated it as a target to hit.",
    "The average smartphone contains more lines of code than the Space Shuttle did. Most of that code is not the fun part.",
    "RAM is volatile, which means it forgets everything the instant the power goes. This is why the exam answer is always about power, never about speed.",
    "The reason 8 bits became a byte is largely historical accident. IBM's System/360 in 1964 settled it, and everyone copied.",
    "Denary, decimal and base 10 all mean the same thing. Exam boards mostly say denary, so use that word and you can never lose a mark for it.",
    "A hash function turns any amount of data into a fixed size fingerprint. Change one character of a 900 page book and the hash changes completely.",
    "Pygame was first released in 2000 and is still one of the fastest ways to see your code do something visual, which is why it is brilliant for learning.",
    "The most expensive software bug in history may be the Ariane 5 rocket in 1996. A 64 bit number was converted to 16 bits, overflowed, and destroyed a rocket worth hundreds of millions.",
    "Compression works by removing redundancy. English text compresses well because letters are predictable. Truly random data cannot be compressed at all.",
    "There is no such thing as deleting a file in most file systems. The pointer to it is removed and the space is marked reusable. This is why forensic recovery works.",
    "The term algorithm comes from the name of the Persian mathematician al-Khwarizmi, who died around 850. His book also gave us the word algebra.",
    "Vector graphics store instructions, not pixels. That is why a logo saved as SVG stays sharp on a billboard while a JPEG turns into mush.",
    "Machine learning models do not understand anything. They find statistical patterns. Knowing that difference is worth marks at both GCSE and A Level."
  ];

  var TIPS = [
    "Reading a page twice feels productive but does almost nothing. Close the tab and write down what you remember. That single change is the biggest evidence-backed improvement in revision.",
    "Spacing beats cramming. Twenty minutes today, twenty in three days and twenty next week will beat an hour tonight, every time.",
    "In the exam, underline the command word first. Describe, explain, compare and justify all want different things, and mixing them up loses marks even when the knowledge is right.",
    "Marks are a shopping list. Four marks means the examiner wants four separate creditworthy things. Count your points before you move on.",
    "When a question says explain, every point needs a because or a so that. State plus reason is what turns a 1 into a 2.",
    "Do not revise the topics you enjoy. Revise the ones you avoid. The avoidance is the signal.",
    "Write code by hand sometimes. Both OCR papers include written programming, and the keyboard hides your syntax gaps.",
    "If a definition takes more than one sentence, you probably do not understand it yet. Compress it until it fits.",
    "Do a whole past paper in one sitting, timed, at least three times before the real thing. Stamina is a skill.",
    "Mark your own work against the mark scheme. Understanding why a point earns a mark teaches you more than getting it right did.",
    "Draw the diagram. Fetch decode execute, network topologies, binary trees and logic circuits are all much faster to recall as a picture than as a paragraph.",
    "Teach it to somebody, or to an empty room. If you stumble halfway through explaining paging, that is exactly the gap to go and close.",
    "Keep a mistakes book. One line per error you made, and the correction. Read it the morning of the exam instead of your notes."
  ];

  var PRAISE = [
    "You turned up and did the work. That is genuinely most of it.",
    "Every topic you finish is one fewer thing to panic about in May.",
    "Nobody starts good at this. They start confused and keep going.",
    "That is another one banked. Small sessions add up faster than you expect.",
    "You are building the habit, and the habit is what produces the grade."
  ];

  var facts = FACTS.slice(), tips = TIPS.slice();
  function pull(pool, source) {
    if (!pool.length) { Array.prototype.push.apply(pool, source); }
    var i = Math.floor(Math.random() * pool.length);
    return pool.splice(i, 1)[0];
  }

  var btn = document.getElementById("mascotBtn");
  var bubble = document.getElementById("mascotBubble");
  if (!btn || !bubble) return;
  var titleEl = bubble.querySelector("[data-bubble-title]");
  var textEl = bubble.querySelector("[data-bubble-text]");
  var hideTimer = null;

  function say(text, title, sticky) {
    if (hideTimer) { clearTimeout(hideTimer); hideTimer = null; }
    titleEl.textContent = title || "Pixel says";
    textEl.textContent = text;
    bubble.hidden = false;
    btn.classList.add("is-talking");
    btn.setAttribute("aria-expanded", "true");
    var ping = btn.querySelector(".mascot-ping");
    if (ping) ping.remove();
    setTimeout(function () { btn.classList.remove("is-talking"); }, 2400);
    if (!sticky) hideTimer = setTimeout(hide, 16000);
  }
  function hide() {
    bubble.hidden = true;
    btn.setAttribute("aria-expanded", "false");
    if (hideTimer) { clearTimeout(hideTimer); hideTimer = null; }
  }
  window.MskCat = { say: say, hide: hide };

  var modes = [
    function () { say(pull(facts, FACTS), "Fun fact"); },
    function () { say(pull(tips, TIPS), "Revision tip"); },
    function () { say(PRAISE[Math.floor(Math.random() * PRAISE.length)], "Pixel says"); }
  ];
  var modeIx = 0;
  function next() { modes[modeIx % modes.length](); modeIx++; }

  btn.addEventListener("click", function () {
    if (!bubble.hidden) { hide(); return; }
    next();
  });
  bubble.addEventListener("click", function (e) {
    if (e.target.closest(".bubble-close")) { hide(); return; }
    var act = e.target.closest("[data-cat]");
    if (!act) return;
    var kind = act.getAttribute("data-cat");
    if (kind === "fact") say(pull(facts, FACTS), "Fun fact");
    else if (kind === "tip") say(pull(tips, TIPS), "Revision tip");
    else if (kind === "quiet") { store.set("mascot", { quiet: Date.now() }); say("Understood. I will stay out of the way. Tap me any time you want a fact or a nudge.", "Pixel says"); }
  });

  /* First greeting: contextual, once per page load, and never if the student
     asked for quiet in the last day. */
  var pref = store.get("mascot", {});
  var quiet = pref.quiet && (Date.now() - pref.quiet) < 86400000;
  var greeting = document.body.getAttribute("data-cat-greeting");
  if (!quiet && greeting) {
    setTimeout(function () { say(greeting, "Pixel says"); }, 1600);
  } else if (!quiet) {
    var ping = document.createElement("span");
    ping.className = "mascot-ping";
    btn.appendChild(ping);
  }
})();
