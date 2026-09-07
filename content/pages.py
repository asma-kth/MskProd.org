"""Standalone site pages: about, privacy, accessibility, how to revise, glossary."""
from mskbuild import markup
from mskbuild.render import (layout, crumbs, crumbs_ld, ico, esc, write,
                             SITE_URL, SITE_NAME, mascot_svg)


def _page(path, title, description, crumb, body_md, extra="", greeting="", ld=None):
    trail = [("Home", "/"), (crumb, None)]
    body = """<div class="wrap">
  %s
  <div class="wrap-narrow" style="width:100%%;margin-inline:auto">
    <article class="prose" style="padding-bottom:var(--sp-8)">
      <header class="topic-header"><h1>%s</h1><p class="lead">%s</p></header>
      %s
      %s
    </article>
  </div>
</div>""" % (crumbs(trail), esc(title), esc(description), markup.render(body_md), extra)
    return path, layout(title=title, description=description, path=path,
                        body=body, greeting=greeting,
                        jsonld=(ld or []) + [crumbs_ld(trail)])


# ============================================================ HOW TO REVISE

HOW_TO_REVISE = """
Most students revise by reading their notes again, highlighting things, and copying work out neatly. All three of those feel productive and almost none of the effect survives to the exam. This page describes what actually works, and it is based on decades of evidence from cognitive psychology rather than on what feels comfortable.

## The one idea that matters most

!key Retrieval beats review :: Trying to recall something from memory strengthens that memory far more than reading it again does. This single finding is the most robust result in the whole of learning research, and almost nobody acts on it.

Practically, that means: read a page once, **close it**, and write down everything you can remember. Then open it and see what you missed. The gap between what you read and what you can produce is the only thing that matters, and rereading never shows it to you.

This feels much worse than rereading, because you are confronted with what you do not know. That discomfort is the mechanism working.

## The five techniques that are worth your time

### 1. Retrieval practice

Test yourself, from memory, without your notes.

- Do the ten question check on every topic on this site
- Write exam answers before looking at the mark scheme
- Cover a definition, say it out loud, then check
- Use flashcards, but say the answer before flipping

### 2. Spaced practice

Revisit material after a delay rather than all at once.

A workable schedule for any topic:

- Learn it today
- Retrieve it after **one day**
- Retrieve it after **three days**
- Retrieve it after **one week**
- Retrieve it after **one month**

Each retrieval takes a few minutes. Four spaced sessions of ten minutes beat one session of forty by a very large margin, and the difference grows the longer the gap to the exam.

### 3. Interleaving

Mix topics rather than blocking them. Instead of two hours on networks, do forty minutes on networks, forty on algorithms and forty on data representation.

Blocking feels smoother because you stay in one mode. Interleaving is harder and produces better retention and better ability to tell similar problems apart, which is exactly what an exam demands.

### 4. Elaboration

Ask why and how, not just what.

- Why does virtual memory make a computer slow?
- How does a firewall differ from anti malware, and why do you need both?
- Why is RISC used in phones rather than CISC?

Answers to why questions stick because they connect to things you already know. Isolated facts do not.

### 5. Concrete examples and practice questions

Do questions. Then do more questions. Then mark them honestly against the mark scheme.

## What to stop doing

+ Rereading notes. It produces a strong feeling of familiarity and very little recall.
+ Highlighting. It feels like processing and is close to passive.
+ Copying work out neatly. This is handwriting practice.
+ Watching videos without pausing to answer anything.
+ Making beautiful revision materials you never use.
+ Revising the topics you like. Your comfort is not a good guide.

## Building a plan that survives contact with reality

1. **List every topic** on the specification. This site is organised by specification point precisely so you can use it as a checklist.
2. **Rate each one honestly**, red, amber or green, based on whether you could explain it to somebody now.
3. **Start with red.** Not with what you enjoy.
4. **Book specific sessions**, not vague intentions. "Tuesday 5 to 5:40, networks" happens. "Do some revision this week" does not.
5. **Every session ends with retrieval.** Close everything and write what you remember.
6. **Re-rate weekly**, and let the ratings decide next week's sessions.

## Exam technique, which is worth several grades

- **Underline the command word first.** Describe, explain, compare, evaluate and justify all want different things.
- **Count the marks.** Four marks means four separate creditworthy points. Write four.
- **Explain means because.** Every point needs a reason or a consequence attached.
- **Compare means both.** Say what each one is like, not just what one is like.
- **Discuss and evaluate mean both sides plus a conclusion.** A one sided answer is capped in the mark scheme however correct it is.
- **Show working in calculations**, with units on every line. Method marks are real marks.
- **Answer the question in front of you**, not the similar one you revised.
- **Leave nothing blank.** A blank is a guaranteed zero and a rough attempt frequently is not.

!grade The single biggest improvement available to most students :: Write answers out fully, from memory, and mark them against the real mark scheme. Recognising a correct answer is a completely different skill from producing one, and only the second is tested.

## A realistic weekly pattern

You do not need four hours a night. You need consistency.

| When | What | How long |
| Monday to Thursday | One topic: read, then ten question check, then five exam answers | 40 minutes |
| Friday | Retrieval only, on the topics from the past week and the past month | 20 minutes |
| Saturday | One full past paper, timed, or half a paper | 45 to 90 minutes |
| Sunday | Mark the paper, list every dropped mark and why | 30 minutes |

That is under five hours a week, and done from January it is worth more than any amount of panic in May.

## If you are behind

Do not try to cover everything. Cover the highest value things:

1. The topics that appear on **every** paper: data representation, algorithms, programming fundamentals, networks
2. The **command words**, so you stop losing marks you already know the content for
3. **Past paper questions** rather than notes, because they show you what is actually asked

Fixing the way you answer questions is faster than learning three more topics, and it applies to every question on the paper.
"""

# ================================================================= GLOSSARY

GLOSSARY = [
    ("Abstraction", "Removing detail that is not relevant to the problem being solved, so that only what matters remains.", "All"),
    ("ACID", "Atomicity, Consistency, Isolation and Durability, the guarantees a reliable database transaction provides.", "KS5"),
    ("Algorithm", "A finite sequence of unambiguous, correctly ordered steps that solves a problem.", "All"),
    ("ALU", "Arithmetic Logic Unit. Performs all arithmetic and logical operations inside the processor.", "KS4"),
    ("Amdahl's law", "The principle that the speedup from parallel processing is limited by the fraction of a task that must remain sequential.", "KS5"),
    ("ASCII", "A 7 bit character set representing 128 characters, sufficient for English text.", "KS3"),
    ("Bandwidth", "The amount of data that can be transmitted over a connection in a given time.", "KS4"),
    ("Big O notation", "A description of how an algorithm's time or memory use grows as its input grows, in the worst case.", "KS5"),
    ("Binary", "Base 2. A number system using only 0 and 1, matching the two states of electronic components.", "KS3"),
    ("Binary search", "Finding an item in sorted data by repeatedly halving the search range. O(log n).", "KS4"),
    ("Bit", "A binary digit, either 0 or 1. The smallest unit of data.", "KS3"),
    ("Boolean", "A data type with exactly two values, true and false.", "KS3"),
    ("Bubble sort", "Repeatedly comparing adjacent items and swapping them if out of order. Simple but O(n squared).", "KS4"),
    ("Byte", "Eight bits.", "KS3"),
    ("Cache", "Small, very fast memory close to the processor holding recently and frequently used data and instructions.", "KS4"),
    ("Casting", "Converting a value from one data type to another, such as int() or str() in Python.", "KS3"),
    ("CIR", "Current Instruction Register. Holds the instruction currently being decoded and executed.", "KS5"),
    ("Client server", "A network model where central servers provide resources to client computers.", "KS4"),
    ("Colour depth", "The number of bits used to store the colour of each pixel. n bits gives 2 to the power n colours.", "KS3"),
    ("Compiler", "A translator converting an entire program to machine code before execution, producing an executable.", "KS4"),
    ("Compression", "Reducing file size, either lossily by discarding data or losslessly by encoding it more efficiently.", "KS4"),
    ("Concurrency", "Carrying out parts of a task at the same time, or appearing to by switching rapidly between them.", "KS5"),
    ("Constant", "A named value fixed when set and not changeable afterwards.", "KS3"),
    ("Control Unit", "The processor component that decodes instructions and generates the control signals coordinating everything else.", "KS4"),
    ("Cookie", "A small file stored on a device by a website, used to remember settings or to track browsing.", "KS3"),
    ("Data Protection Act 2018", "UK legislation governing how organisations collect, store and use personal data.", "KS3"),
    ("Deadlock", "A state where two processes each hold a resource the other needs, so neither can proceed.", "KS5"),
    ("Decomposition", "Breaking a large problem into smaller sub problems that are easier to solve and test.", "All"),
    ("Defensive design", "Writing a program so it continues to work correctly despite unexpected input or misuse.", "KS4"),
    ("De Morgan's laws", "The rules that the negation of an AND is the OR of the negations, and vice versa.", "KS5"),
    ("Denary", "Base 10, the everyday number system. Also called decimal.", "KS3"),
    ("Digital divide", "The gap between those with reliable access to technology and the internet and those without.", "KS3"),
    ("Dijkstra's algorithm", "An algorithm finding the shortest path in a weighted graph with non negative weights.", "KS5"),
    ("DNS", "Domain Name System. Resolves human readable domain names into IP addresses.", "KS4"),
    ("Encapsulation", "Bundling data with the methods that act on it and controlling access, so an object protects its own state.", "KS5"),
    ("Encryption", "Scrambling data with a key so that intercepted data cannot be understood.", "KS4"),
    ("Firewall", "Hardware or software inspecting network traffic and blocking anything that does not meet its rules.", "KS4"),
    ("Fetch decode execute", "The cycle a processor repeats continuously to run instructions.", "KS4"),
    ("Hash function", "A function producing a fixed size output from any input, designed to be one way.", "KS5"),
    ("Hash table", "A structure using a hash function to map keys directly to array positions, giving average constant time lookup.", "KS5"),
    ("Heuristic", "A rule of thumb producing a good enough solution quickly, without guaranteeing the optimal one.", "KS5"),
    ("Hexadecimal", "Base 16, using 0 to 9 and A to F. One hex digit represents four bits.", "KS3"),
    ("HTTPS", "The encrypted version of HTTP, protecting web traffic from being read if intercepted.", "KS4"),
    ("Interpreter", "A translator converting and executing a program one statement at a time, each time it runs.", "KS4"),
    ("Interrupt", "A signal requesting the processor's attention, checked at the end of each fetch decode execute cycle.", "KS5"),
    ("IP address", "An address identifying a device on a network, assigned by the network and used for routing between networks.", "KS4"),
    ("Iteration", "Repeating a set of instructions, either a fixed number of times or until a condition is met.", "KS3"),
    ("Linked list", "A structure of nodes each holding data and a pointer to the next, allowing dynamic size and cheap insertion.", "KS5"),
    ("Lossless compression", "Compression that reduces size without losing any data, so the original is restored exactly.", "KS4"),
    ("Lossy compression", "Compression that permanently removes data, giving much smaller files at the cost of quality.", "KS4"),
    ("MAC address", "A unique address assigned to network hardware by its manufacturer, used within a local network.", "KS4"),
    ("Malware", "Any software written with the intention of causing harm.", "KS3"),
    ("Merge sort", "A divide and conquer sort with consistent O(n log n) time but O(n) additional space.", "KS4"),
    ("Metadata", "Data about data, such as the dimensions and colour depth stored with an image.", "KS4"),
    ("MOD", "The modulus operator, which returns the remainder after a division.", "KS3"),
    ("Normalisation", "Organising a database to remove redundancy and eliminate update, insertion and deletion anomalies.", "KS5"),
    ("Object", "A specific instance created from a class, holding its own data and sharing the class's methods.", "KS5"),
    ("Operating system", "System software managing hardware and software and providing an environment for applications.", "KS4"),
    ("Overflow", "An error where a result requires more bits than are available, so the stored value is wrong.", "KS4"),
    ("Packet", "A small unit of data sent across a network, carrying addresses and a sequence number.", "KS3"),
    ("PageRank", "An algorithm ranking pages by importance derived from the weighted link structure of the web.", "KS5"),
    ("Paging", "Dividing memory into fixed size pages mapped to equally sized physical frames.", "KS5"),
    ("Peer to peer", "A network model where every computer is equal, acting as both client and server.", "KS4"),
    ("Phishing", "A fraudulent message imitating a trusted organisation to obtain personal information.", "KS3"),
    ("Pipelining", "Overlapping the fetch, decode and execute stages of consecutive instructions to raise throughput.", "KS5"),
    ("Pixel", "Picture element. The smallest single point of colour in a bitmap image.", "KS3"),
    ("Polymorphism", "Objects of different classes responding to the same method call, each in their own way.", "KS5"),
    ("Precondition", "A condition that must be true before a subroutine is called for it to work correctly.", "KS5"),
    ("Protocol", "An agreed set of rules governing how data is transmitted between devices.", "KS4"),
    ("RAM", "Random access memory. Volatile main memory holding the operating system, running programs and data in use.", "KS3"),
    ("Recursion", "A subroutine calling itself, with a base case that stops the process.", "KS5"),
    ("RISC", "Reduced Instruction Set Computer. Few simple fixed length instructions, pipelining well and using less power.", "KS5"),
    ("ROM", "Read only memory. Non volatile memory holding the boot program available at switch on.", "KS3"),
    ("Sampling", "Measuring the amplitude of a sound wave at regular intervals and storing each value in binary.", "KS3"),
    ("Selection", "Choosing between different paths through a program based on a condition.", "KS3"),
    ("SQL", "Structured Query Language, used to search and manipulate data held in a database.", "KS4"),
    ("Stack", "A last in first out data structure supporting push and pop. Used for the call stack and backtracking.", "KS5"),
    ("Subroutine", "A named block of code performing one task, callable from elsewhere. A function returns a value, a procedure does not.", "KS4"),
    ("Two's complement", "A signed integer representation where the most significant bit carries a negative place value.", "KS5"),
    ("Unicode", "A character set using 16 or more bits per character, covering over a million characters from all major scripts.", "KS3"),
    ("Validation", "Checking that input data is sensible and in the expected format before the program uses it.", "KS3"),
    ("Variable", "A named memory location holding a value that can change while the program runs.", "KS3"),
    ("Virtual memory", "An area of secondary storage used as an extension of RAM when physical memory is full.", "KS4"),
    ("Von Neumann architecture", "A design where instructions and data share one memory, fetched one instruction at a time.", "KS4"),
]


def build(register, add_search, courses):
    # ------------------------------------------------------ how to revise
    path, html = _page(
        "/how-to-revise/", "How to Revise Properly",
        "What actually works in revision, based on evidence rather than on what feels productive, plus exam technique worth several grades.",
        "How to revise", HOW_TO_REVISE,
        greeting="This page is worth more than any single topic on the site. Most students never change how they revise, and that is exactly why changing it works so well.")
    write(path, html)
    register(path, 0.8, "monthly")
    add_search("How to revise properly", path, "Evidence based revision technique",
               "revision retrieval practice spaced interleaving exam technique command words how to revise")

    # ---------------------------------------------------------- glossary
    stages = sorted({s for _, _, s in GLOSSARY})
    rows = "".join(
        '<div class="keyterm" data-term><dt>%s <span class="badge" style="font-size:.65rem;vertical-align:middle">%s</span></dt><dd>%s</dd></div>'
        % (esc(t), esc(s), esc(d)) for t, d, s in sorted(GLOSSARY, key=lambda x: x[0].lower()))
    extra = ('<div class="card" style="margin-bottom:var(--sp-4);padding:var(--sp-3) var(--sp-4)">'
             '<label for="glossaryFilter" class="sr-only">Filter the glossary</label>'
             '<input id="glossaryFilter" type="search" placeholder="Type to filter, for example binary or recursion" '
             'style="width:100%%;border:0;font:inherit;font-size:1rem;background:transparent;color:var(--ink);outline:none">'
             '</div>'
             '<dl class="keyterms" id="glossaryList">%s</dl>'
             '<p class="muted" id="glossaryEmpty" hidden>No terms matched. Try a shorter word.</p>'
             '<script>(function(){var i=document.getElementById("glossaryFilter"),'
             'l=document.getElementById("glossaryList"),e=document.getElementById("glossaryEmpty");'
             'if(!i)return;i.addEventListener("input",function(){var q=i.value.toLowerCase(),n=0;'
             'l.querySelectorAll("[data-term]").forEach(function(r){var m=r.textContent.toLowerCase().indexOf(q)>-1;'
             'r.hidden=!m;if(m)n++;});e.hidden=n>0;});})();</script>' % rows)
    path, html = _page(
        "/glossary/", "Computing Glossary",
        "Every key term across Key Stage 3, GCSE and A Level computing, each defined in one sentence you could write in an exam.",
        "Glossary",
        "Definitions written the way a mark scheme wants them: one sentence, precise, and using the vocabulary the examiner is looking for. Type in the box to filter, and cover the definition and say it out loud before you read it.",
        extra=extra,
        greeting="Do not read this list. Cover a definition, say it out loud, then check. Retrieval is what makes it stick.")
    write(path, html)
    register(path, 0.7, "monthly")
    add_search("Computing glossary", path, "%d key terms defined" % len(GLOSSARY),
               "glossary definitions key terms vocabulary " + " ".join(t.lower() for t, _, _ in GLOSSARY))

    # ------------------------------------------------------------- about
    total_topics = sum(len(u.topics) for c in courses for u in c.units)
    total_quiz = sum(len(t.quiz) for c in courses for u in c.units for t in u.topics)
    about = """
MskProd Computing is a free revision site for UK students studying computing at Key Stage 3, GCSE and A Level. There are **%d topics**, **%d knowledge check questions** and several hundred auto marked exam-style questions, written board by board for OCR, AQA and Edexcel and sequenced in the order the subject is actually taught in school.

Everything on the site is free. There is no account to create and no subscription. The site is paid for by advertising, and how that works is set out in the [privacy policy](/privacy/).

## Why this site exists

Most computing revision material falls into one of two categories. Either it is a list of bullet points that tells you what the answer is without ever explaining why, or it is a wall of text written for a teacher rather than a student. Neither of those helps somebody sitting at a desk in April trying to work out what a page fault actually is.

This site is built on a different premise: that the reason behind a fact is the thing worth knowing, because the reason is where the marks are and, more importantly, because a reason is something you can reconstruct when you have forgotten the detail.

Every topic therefore has the same structure:

+ A full explanation written to be understood, with the mechanism explained rather than asserted
+ Key terms defined the way a mark scheme wants them, plus flashcards for retrieval practice
+ A ten question knowledge check with an explanation for every answer, right or wrong
+ Five exam-style written questions marked automatically against a real mark scheme, with a model answer
+ A section on what separates a top grade answer from an average one, and the mistakes that cost marks

## About the author

!info Please personalise this section :: This paragraph is a placeholder. Replace the text below with your own introduction, and this note along with it.

This site is written and maintained by a computing teacher working in a UK secondary school, covering Key Stage 3 through to A Level. It began as a set of resources for one department and grew into something worth making available to anyone.

## How the site is built

The site is a set of static HTML pages generated from structured content. That means it loads quickly, works without JavaScript for reading, is fully accessible to screen readers and search engines, and has no database to be breached because there is no database at all.

The quizzes and the exam marker run entirely in your browser. Your scores are stored on your own device using local storage and are never transmitted anywhere. There is no server that could see them.

## A note on exam papers

Real past papers are the copyright of the exam boards and cannot lawfully be republished here. Every paper in the [exam papers section](/exam-papers/) is therefore written from scratch to match the structure, question style, command words and mark allocation of the real assessments, with a full mark scheme for each. Links to the official past papers on each board's own website are provided alongside them.

This site is written independently and is not endorsed by, affiliated with or connected to OCR or any other awarding body. Always check the current specification on the exam board's own website, since specifications do change.

## Getting in touch

Corrections are genuinely welcome. If something on this site is wrong, unclear or out of date, please say so, and it will be fixed.
"""
    path, html = _page(
        "/about/", "About MskProd Computing",
        "A free revision site for UK computing students at Key Stage 3, GCSE and A Level, covering OCR, AQA and Edexcel, with no accounts, adverts or tracking.",
        "About", about % (total_topics, total_quiz),
        extra='<div class="center" style="max-width:220px;margin:var(--sp-6) auto 0">%s</div>' % mascot_svg(),
        greeting="I am Pixel. I live in the corner of every page, and I run entirely on your own device. Nothing you do here is sent anywhere.",
        ld=[{"@context": "https://schema.org", "@type": "AboutPage",
             "name": "About " + SITE_NAME, "url": SITE_URL + "/about/"}])
    write(path, html)
    register(path, 0.6, "yearly")
    add_search("About", path, "About this site", "about author contact")

    # ----------------------------------------------------------- privacy
    privacy = """
**Last updated: September 2026**

The short version: the site itself asks nothing of you and keeps your work on your own device. It is paid for by advertising, and those adverts are served by Google, which does set cookies and does collect data about the people who see them. That part is explained in full below.

## What this site does not do

+ There are no user accounts and no sign up. You cannot create one.
+ The site owner runs no analytics. There is no Google Analytics, no visitor counter and no fingerprinting by this site.
+ Your quiz scores, exam answers and progress are never uploaded. They stay in your browser.
+ Nothing you type into the exam answer boxes is transmitted anywhere or read by anybody.
+ Nothing about you is sold by the site owner.

## Advertising

This site carries adverts supplied by **Google AdSense**, and that is how it stays free to use.

To show adverts, Google receives your IP address, information about your browser and device, and the page you are reading. Google and its partners may store and read cookies or similar identifiers on your device to measure how adverts perform and, where you have agreed to it, to choose adverts based on your interests.

This means the honest position is: **the site owner collects nothing about you, but Google does.** What Google does with it is governed by [Google's own privacy policy](https://policies.google.com/privacy) and by [how Google uses data from sites that use its services](https://policies.google.com/technologies/partner-sites).

If you are in the UK or the EEA, you will be asked on your first visit whether you agree to advertising cookies. You can decline, and you can change your answer later. Declining does not restrict any part of the site: every topic, quiz, exam question and tool works exactly the same either way.

You can also opt out of personalised advertising across the whole web at [Google's Ads Settings](https://adssettings.google.com), and most browsers let you block or delete cookies for individual sites.

## Data stored on your own device

The quizzes, the exam answer marker and the theme switch need to remember a few things between visits. These are stored in your browser's **local storage**, which is a small area of your own device.

The following may be stored locally:

| What | Why |
| Your quiz scores | So you can see which topics you have completed and how you did |
| Your exam-style answer marks | So your progress on written questions is not lost when you close the tab |
| Which topics you have opened | So the course pages can show a small marker next to topics you have visited |
| Your light or dark theme choice | So the site looks the way you left it |
| Whether you asked Pixel to stay quiet | So the mascot respects that |

**This data never leaves your device.** It is not transmitted to any server, it is not accessible to the site owner, and there is no mechanism by which it could be. It is stored by your browser under this website's address and is readable only by this website on this device.

You can delete all of it at any time by clearing site data for this website in your browser settings, or by using the button below.

<p><button class="btn btn-secondary" type="button" data-reset-progress>Clear everything this site has stored on my device</button></p>

## The mascot

Pixel, the robot cat, runs entirely in your browser. The facts, tips and messages are all contained in a JavaScript file downloaded with the page. Nothing you do is analysed and no request is made to any server when Pixel speaks.

## Third party services

The site loads its typefaces from **Google Fonts**. When your browser requests those font files it makes a request to Google's servers, which as with any web request involves your IP address and browser information being visible to Google. If you would prefer to avoid it, most browsers and privacy extensions can block requests to fonts.googleapis.com, and the site remains fully readable and fully functional with a fallback typeface.

The runnable Python examples download the Python engine from a public code network (jsDelivr) the first time you press Run on a page. That request is only made if you press Run.

Besides these and the advertising described above, the site makes no other third party requests.

Links to external websites, such as the exam board pages in the exam papers section, are clearly marked and open in a new tab. Once you follow such a link, that website's own privacy policy applies and this one does not.

## Hosting

The site is a set of static files served by a hosting provider. Like almost all web servers, the host may keep standard server logs recording requests, which typically include IP addresses, for a limited period for security and operational purposes. This is normal infrastructure logging outside the site owner's control and is not used to identify or profile visitors.

## Your rights under UK GDPR

The UK General Data Protection Regulation and the Data Protection Act 2018 give individuals rights over personal data held about them, including the rights of access, rectification and erasure.

The site owner holds no personal data about you, so there is nothing held here to request access to, correct or erase. The data stored in your browser is under your own control and can be deleted at any time using the button above or your browser's settings.

For the data Google collects through the adverts, Google is the data controller. Requests about that data should go to Google, using the contacts in [its privacy policy](https://policies.google.com/privacy). You can withdraw your consent to advertising cookies at any time, and doing so does not affect anything else on the site.

## Children

This site is written for school age students, including Key Stage 3 pupils who may be as young as eleven, and it asks for no personal information from anybody of any age.

Because the site carries advertising, adverts here are served as non-personalised: they are chosen from the content of the page rather than from any profile of the reader, and they are not used to build one. If you are a parent or a teacher and have a question about this, please get in touch through the [about page](/about/).

## Changes to this policy

If this policy ever changes, the date at the top of this page will be updated, and any change that affects what is collected about you will be stated here plainly.

## Contact

If you have a question about privacy on this site, please get in touch through the [about page](/about/).
"""
    path, html = _page(
        "/privacy/", "Privacy Policy",
        "The site owner collects no personal data and your quiz scores never leave your device. The site is funded by Google adverts, which do set cookies. Explained in full here.",
        "Privacy", privacy,
        greeting="Short version: your scores never leave your device. The adverts are Google's, and they do use cookies. It is all explained here.",
        ld=[{"@context": "https://schema.org", "@type": "WebPage",
             "name": "Privacy Policy", "url": SITE_URL + "/privacy/"}])
    write(path, html)
    register(path, 0.5, "yearly")
    add_search("Privacy policy", path, "What is stored, what Google collects for adverts, and your rights",
               "privacy policy gdpr data cookies tracking advertising adsense consent")

    # ----------------------------------------------------- accessibility
    access = """
This site is built so that it can be used by everybody, including people using a screen reader, people navigating by keyboard, people with low vision and people with limited dexterity. Accessibility was designed in rather than added afterwards.

## What has been done

### Structure and semantics

+ Every page uses proper heading levels in order, so screen reader users can navigate by heading
+ Landmarks are used correctly: header, nav, main and footer
+ A skip to content link is the first focusable element on every page
+ Every page has a descriptive, unique title
+ Lists, tables and definition lists are marked up as such rather than styled to look like them

### Keyboard access

+ Every interactive element can be reached and operated with the keyboard alone
+ Quiz options respond to Enter and Space as well as to a click
+ Focus is always visible, with a clear high contrast outline
+ The search dialog can be opened with the forward slash key and closed with Escape
+ Nothing traps keyboard focus

### Visual design

+ Body text and interface text meet or exceed the WCAG AA contrast requirement in both light and dark themes
+ A dark theme is available and the site also respects your operating system preference automatically
+ Text uses relative units and reflows correctly when zoomed to 200 per cent
+ Colour is never the only way information is conveyed. Correct and incorrect quiz answers are marked with a symbol and text as well as a colour
+ Line length is limited to around 68 characters, and line height is generous, both of which materially help readers with dyslexia
+ The typeface is chosen for legibility rather than for style

### Motion

+ Animation is decorative only and never conveys information
+ All animation, including the mascot, is disabled automatically if your system is set to prefer reduced motion
+ Nothing flashes, blinks or moves unexpectedly

### Content

+ Language is kept as plain as the subject allows, and technical terms are defined when first used
+ Explanations are broken into short sections with clear headings
+ Code blocks scroll horizontally within their own container rather than forcing the whole page to scroll
+ Tables scroll within their own container on narrow screens

### Without JavaScript

Every explanation, key term, quiz question and exam question is present in the HTML and fully readable with JavaScript disabled. JavaScript adds interactivity such as instant marking, the theme switch and the search dialog, but nothing that is needed to read and learn from the content.

## Known limitations

Being honest about what is not perfect is more useful than claiming everything is.

+ Some tables of technical comparison are wide by nature. They scroll horizontally on a narrow screen, which is a compromise rather than an ideal solution.
+ Diagrams are currently described in text rather than presented visually. This is better for screen reader users but means some concepts that would benefit from an illustration do not yet have one.
+ The exam answer marker requires typing. There is currently no alternative input method for students who would find that difficult, and voice input from the operating system is the only workaround.

## Standards

The site aims to meet **WCAG 2.2 level AA**. If you find something that does not, that is a fault to be fixed rather than a limitation to be explained away.

## Reporting a problem

If any part of this site is difficult or impossible for you to use, please say so through the [about page](/about/). Accessibility problems are treated as bugs and are prioritised as such.
"""
    path, html = _page(
        "/accessibility/", "Accessibility",
        "How this site is built to be usable by everybody, what has been done, what standard it aims for, and what is not yet perfect.",
        "Accessibility", access,
        greeting="If any part of this site is hard for you to use, that is a bug. Please report it.")
    write(path, html)
    register(path, 0.5, "yearly")
    add_search("Accessibility", path, "Accessibility statement",
               "accessibility screen reader keyboard contrast wcag")
