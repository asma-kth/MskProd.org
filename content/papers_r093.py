"""OCR Cambridge National Creative iMedia R093: two more full length papers, B and C.

Modelled on the R093 examined unit: 70 marks in 1 hour 30 minutes. Section A
is ten one mark questions across the specification. Section B, 60 marks, is
built around one client brief, with short and medium answers and two 9 mark
extended responses, one a discussion and one about planning.
"""
from mskbuild.examkit import tick, rows, ans, write
from mskbuild.models import Paper

ACC = "var(--lilac-deep)"
ADVICE = ("Section A is quick: about ten minutes for ten marks. In Section B, read the brief twice and refer to it in every answer, "
          "because marks are given for applying what you know to this client, not for general statements.")
NOTE_A = "Answer all the questions in this section."
NOTE_B = "Answer all the questions in this section. They are about the client brief below."


# ===================================================================== Paper B

BRIEF_B = """**Client brief: Bright Path Adventure Centre**

Bright Path is an outdoor adventure centre in the Lake District. It offers climbing, kayaking and zip lines for families and for school groups. The centre has asked a media company to produce:

- a 60 second promotional video for its website and its social media accounts
- a poster to be displayed in tourist information centres and local hotels.

The products must show that the activities are exciting but safe, and appeal to families with children aged 8 to 14. They must use the centre's existing logo and its green and orange colours. Both products must be finished in six weeks, and the budget is £4,000."""

R093_B = Paper(
    slug="r093-paper-b",
    title="Creative iMedia R093 Paper B: Creative iMedia in the Media Industry",
    course="Creative iMedia", board="OCR", code="R093",
    minutes=90, marks=70, accent=ACC, spec="R093", full=True,
    blurb="A full length R093 paper. Section A: ten one mark questions. Section B: a brief for an adventure centre's promotional video and poster, covering requirements, audience, research, work planning, pre-production documents, copyright and permissions, file formats, and two 9 mark extended responses.",
    advice=ADVICE, calculator="You do not need a calculator.",
    instructions=["The two 9 mark questions are extended responses. In the real exam they are marked in levels; here every relevant point you make earns a mark, up to 9."],
    questions=[
        # ---------------------------------------------------- Section A
        tick("Which **one** of these is a print based product?", ["*A magazine", "A podcast", "A video game", "A website"],
             "A magazine is printed. A podcast is audio, and games and websites are digital and interactive.",
             label="1", section="Section A", section_note=NOTE_A),
        tick("Which **one** job role works in post-production?", ["*Video editor", "Scriptwriter", "Camera operator", "Storyboard artist"],
             "The video editor assembles the footage after filming. Scriptwriters and storyboard artists work in pre-production, and camera operators in production.",
             label="2"),
        tick("Which **one** of these is primary research?",
             ["*A focus group run by the design team", "A government census report", "A competitor's website", "A published book about families"],
             "Primary research is collected by you, for this project. The others were collected by someone else.", label="3"),
        tick("Which **one** of these is a demographic characteristic of an audience?", ["*Age", "Interests", "Values", "Attitudes"],
             "Demographics are measurable facts such as age. Interests, values and attitudes are psychographics.", label="4"),
        ans("Name the pre-production document that shows each shot of a video, in order, as a series of drawn frames.",
            ["storyboard", "storyboards", "story board"], model="A storyboard.", width=16, label="5"),
        tick("Which **one** image file format supports transparency and uses lossless compression?", ["*PNG", "JPG", "BMP", "MP3"],
             "PNG is lossless and supports transparency. JPG is lossy, BMP is usually uncompressed, and MP3 is audio.", label="6"),
        tick("Which **one** organisation gives age ratings to video games in the UK?", ["*PEGI", "BBFC", "Ofcom", "ASA"],
             "PEGI rates games. The BBFC rates films, Ofcom regulates broadcasting and the ASA regulates advertising.", label="7"),
        tick("Which **one** property of a video file decides how smooth movement looks?", ["*Frame rate", "Aspect ratio", "Colour depth", "File name"],
             "The frame rate is the number of frames shown each second; more frames give smoother movement.", label="8"),
        tick("Which **one** type of media code is the use of a low camera angle?", ["*Technical", "Symbolic", "Written"],
             "Camera angles, shot sizes, movement, lighting and editing are technical codes.", label="9"),
        ans("Give the name of the type of licence that lets a creator choose how others may use their work, often for free, with conditions such as giving credit.",
            ["creative commons", "creative commons licence", "creative commons license", "cc", "a creative commons licence"],
            model="Creative Commons.", width=18, label="10"),

        # ---------------------------------------------------- Section B
        write("Identify **two** client requirements for the products, from the brief.", 2, [
            ("Show that the activities are exciting but safe", ["exciting", "safe"]),
            ("Appeal to families with children aged 8 to 14", ["famil", "8 to 14", "children", "8-14"]),
            ("Use the centre's logo and its green and orange colours", ["logo", "green", "orange", "colour"]),
            ("Be finished in six weeks, within a budget of £4,000", ["six weeks", "6 weeks", "4,000", "4000", "budget", "deadline"]),
            ("A 60 second video for the website and social media, and a poster", ["60", "sixty", "poster", "website", "social media"]),
        ], "The products must show that the activities are exciting but safe, and they must use the centre's existing logo and its green and orange colours.",
              command="Identify", label="11(a)", section="Section B", section_note=NOTE_B, lead=BRIEF_B),
        write("Explain **one** way the age of the children in the target audience should affect the design of the promotional video.", 2, [
            ("A design choice, such as fast paced editing, close ups of the action, bright colours or upbeat music", ["fast", "pace", "action", "bright", "upbeat", "music", "close up", "children", "young", "excit"]),
            ("Explained: children of 8 to 14 lose interest quickly, so this keeps them engaged and makes them want to go", ["attention", "engag", "interest", "bored", "want to", "appeal", "keep them watching"]),
        ], "The video should use fast paced editing with close ups of children on the zip line and kayaks, set to upbeat music. Children of 8 to 14 lose interest quickly, so short, energetic shots keep them watching and make them ask their parents to go.",
              command="Explain", label="11(b)"),
        write("The company plans to carry out primary research with families who have visited the centre. Describe **two** methods of primary research it could use.", 4, [
            ("A questionnaire or online survey", ["questionnaire", "survey"]),
            ("Described: for example sent to past visitors by email, with closed questions that give data that can be counted", ["email", "online", "closed", "multiple choice", "rating", "quantitative", "many people", "sent"]),
            ("An interview or focus group", ["interview", "focus group"]),
            ("Described: a small group discuss their opinions in depth, giving reasons", ["discuss", "in depth", "opinions", "small group", "qualitative", "reasons", "why"]),
        ], "A questionnaire could be emailed to families who have visited, using closed questions, such as rating each activity, so the answers can be counted and compared. A focus group could bring together a few parents and children to discuss in depth what made the visit exciting and what made them feel safe, which explains the reasons behind the numbers.",
              command="Describe", label="11(c)"),
        write("Explain **one** advantage to the media company of using secondary research.", 2, [
            ("It is quick and cheap or free to obtain, because someone else has already collected it", ["quick", "fast", "cheap", "free", "already", "less time", "low cost"]),
            ("So it saves time and money on a project with a six week deadline and a fixed budget, and it may cover a large sample", ["six week", "deadline", "budget", "save", "large", "time", "money"]),
        ], "Secondary research, such as published tourism statistics, has already been collected by someone else, so it is quick and cheap to find. That matters on a project with a six week deadline and a £4,000 budget.",
              command="Explain", label="11(d)"),
        rows("Tick (✓) one box in each row to show whether each describes a demographic or a psychographic characteristic of the audience.",
             ["Demographic", "Psychographic"],
             [("Families living within 50 miles of the centre", "Demographic"), ("Enjoys outdoor adventure", "Psychographic"),
              ("Children aged 8 to 14", "Demographic"), ("Values safety", "Psychographic")],
             marks=2, model="Where people live and how old they are are demographic facts. What they enjoy and value are psychographic.",
             label="12(a)"),
        write("Identify **three** components that the work plan for this project should contain.", 3, [
            ("The tasks or activities to be done", ["task", "activit"]),
            ("How long each task will take, its timescale or duration", ["duration", "timescale", "how long", "time"]),
            ("Milestones or deadlines, such as the client signing off the storyboard", ["milestone", "deadline", "sign off", "sign-off", "review"]),
            ("Contingency time", ["contingency"]),
            ("The resources needed, such as people and equipment", ["resource", "equipment", "people", "crew", "staff"]),
            ("The order of the tasks and which depend on others", ["order", "depend", "sequence", "before"]),
        ], "The tasks to be completed, the time each will take, and milestones such as the client approving the storyboard.",
              command="Identify", label="12(b)"),
        write("Explain why the work plan should include contingency time.", 2, [
            ("Contingency is extra time set aside in case problems happen, such as bad weather stopping the outdoor filming", ["extra time", "spare time", "problem", "weather", "delay", "illness", "goes wrong", "unexpected"]),
            ("So the products can still be finished by the six week deadline", ["deadline", "six weeks", "on time", "still finished", "meet"]),
        ], "Contingency is spare time built into the plan for things that go wrong. Filming outdoors in the Lake District could easily be stopped by rain, so without contingency a delay could make the company miss the six week deadline.",
              command="Explain", label="12(c)"),
        write("Describe **two** items that should be included on the visualisation diagram for the poster.", 4, [
            ("The colours to be used", ["colour", "green", "orange"]),
            ("Given precisely, such as the green and orange of the house style as colour codes", ["code", "hex", "cmyk", "rgb", "exact", "value", "house style"]),
            ("The fonts, by name and size", ["font", "typeface", "typography"]),
            ("The position of each element, such as the logo, images and text, with annotations explaining the choices", ["position", "layout", "logo", "image", "text", "annotat", "where"]),
        ], "The colours, given as exact values matching the centre's green and orange, so the printer reproduces them correctly. The layout, showing where the logo, the photograph of the zip line and the text will go, with annotations explaining each choice.",
              command="Describe", label="13(a)"),
        tick("Which **three** pieces of information should be shown for each frame of the storyboard for the video?",
             ["*The shot type", "*The camera movement", "*How long the shot lasts", "The font size of the poster", "The budget", "The names of the hotels"],
             "Each storyboard frame shows the shot type, the camera angle and movement, its duration, the sound or dialogue and the transition to the next shot.",
             label="13(b)"),
        write("Explain why the company should produce a mood board before designing the products.", 2, [
            ("A mood board brings together images, colours, fonts and textures to show the intended look and feel", ["look and feel", "style", "images", "colours", "fonts", "textures", "ideas"]),
            ("So the client can agree the style before time and money are spent on the design", ["agree", "client", "approve", "before", "feedback", "time", "money", "wasted"]),
        ], "A mood board collects images, colours, fonts and textures to show the intended look and feel. The client can agree the style, or ask for changes, before any time or money is spent designing the real products.",
              command="Explain", label="13(c)"),
        write("The video editor wants to use a popular chart song as the soundtrack. Explain what the company must do to use the song legally.", 3, [
            ("The song is protected by copyright, owned by the artist, songwriter or record label", ["copyright", "owned", "artist", "record label", "songwriter", "owner"]),
            ("The company must get permission, a licence, from the rights holders", ["permission", "licence", "license", "rights holder"]),
            ("And usually pay a fee or royalties, or else use royalty free or Creative Commons music instead", ["fee", "pay", "royalt", "royalty free", "creative commons", "instead"]),
        ], "The song is protected by copyright, owned by the songwriter and the record label. The company must contact the rights holders for permission and a licence to use it in an advert, which usually means paying a fee. If that costs too much for a £4,000 budget, it should use royalty free music instead.",
              command="Explain", label="14(a)"),
        write("Families visiting the centre will be filmed during the shoot. Explain how the company should deal with this legally.", 3, [
            ("Get written permission, a signed release form, from everyone who can be identified", ["permission", "release", "consent", "signed", "agree"]),
            ("Children under 18 need consent from a parent or guardian", ["parent", "guardian", "under 18", "child"]),
            ("Footage of identifiable people is personal data, so it must be stored securely and used only as agreed, under the Data Protection Act", ["data protection", "personal data", "secure", "privacy", "gdpr", "stored"]),
        ], "Everyone who can be identified must sign a release form giving permission for the footage to be used. The children are under 18, so their parents or guardians must sign for them. The footage is personal data, so under the Data Protection Act it must be stored securely and only used for the purpose agreed.",
              command="Explain", label="14(b)"),
        write("Explain why the company should carry out a location recce at the centre before the shoot.", 3, [
            ("A recce is a visit to the location before filming", ["visit", "before", "in advance", "check"]),
            ("To check practical things such as lighting, power, access, noise and where cameras can go", ["light", "power", "access", "noise", "sound", "camera", "parking", "space"]),
            ("And to identify hazards, such as the water and heights, for the risk assessment, so the shoot is safe and goes to plan", ["hazard", "risk", "safe", "water", "height", "danger", "plan"]),
        ], "A recce is a visit to the centre before the shoot. The crew can check the light at the zip line and lake, where cameras can safely be placed, whether there is power and how noisy it is. It also identifies hazards, such as the water and the heights, for the risk assessment, so the shoot is safe and runs to plan.",
              command="Explain", label="14(c)"),
        tick("Which **one** video file format is most suitable for uploading to the website and to social media?", ["*MP4", "WAV", "PSD", "TIFF"],
             "MP4 plays on almost every device and platform. WAV is audio, and PSD and TIFF are image files.", label="15(a)"),
        write("Explain why the video should be compressed before it is uploaded to the website.", 2, [
            ("Compression makes the file smaller", ["smaller", "reduce", "file size", "less data"]),
            ("So it loads or streams faster with less buffering, and uses less bandwidth and storage", ["faster", "quicker", "buffer", "bandwidth", "storage", "upload", "stream", "load"]),
        ], "Compression reduces the file size, so the video starts quickly and streams without buffering, even on a phone with a slow connection, and it uses less storage on the web server.",
              command="Explain", label="15(b)"),
        rows("Tick (✓) one box in each row to show the most suitable file format for each file.", ["JPG", "SVG", "TIFF", "WAV"],
             [("A high quality, lossless image of the poster to send to the printer", "TIFF"),
              ("A photograph of a family kayaking for the website gallery", "JPG"),
              ("The centre's logo for the website, which must stay sharp at any size", "SVG"),
              ("The voiceover recording, before it is edited", "WAV")],
             marks=2, model="TIFF keeps full quality for print, JPG keeps photographs small for the web, SVG is a vector that scales, and WAV is an uncompressed recording to edit.",
             label="15(c)"),
        write("Explain **two** properties of the poster file that must be set correctly for professional printing.", 2, [
            ("A high resolution, about 300 dpi, so it is sharp when printed", ["resolution", "dpi", "ppi", "300", "sharp", "pixelat"]),
            ("The right dimensions and colour mode for print, such as A3 in CMYK, with bleed", ["dimension", "size", "a3", "a4", "cmyk", "colour mode", "bleed"]),
        ], "Its resolution must be about 300 dpi so it does not look pixelated, and its dimensions must match the printed size, such as A3, in CMYK colour with a bleed so nothing is cut off.",
              command="Explain", label="15(d)"),
        write("Discuss the suitability of social media, the centre's own website and local television as ways of distributing the promotional video to the target audience.", 9, [
            ("Social media reaches parents where they already spend time, and videos can be shared by families", ["share", "parents", "facebook", "instagram", "spend time", "already", "viral"]),
            ("Social media adverts can be targeted at families with children near the Lake District, and are cheap", ["target", "cheap", "low cost", "free", "location", "near", "analytics"]),
            ("But on social media the video competes with other content, so it must grab attention in the first seconds and work without sound", ["compete", "scroll", "first few seconds", "attention", "without sound", "captions", "subtitles"]),
            ("Each platform needs a different aspect ratio and length, so several versions may be needed", ["aspect ratio", "square", "vertical", "versions", "9:16", "different sizes", "length"]),
            ("The centre's website reaches people who are already interested and ready to book, with a link to booking", ["website", "already interested", "book", "booking", "searching"]),
            ("But the website only reaches people who already know about the centre", ["only reach", "already know", "find it", "search", "fewer people"]),
            ("Local television reaches a large local audience, including families who do not use social media", ["television", "tv", "large audience", "local", "broadcast", "older"]),
            ("But television advertising is expensive, beyond a £4,000 budget, and cannot be targeted as closely", ["expensive", "cost", "budget", "4,000", "4000", "cannot target", "not targeted"]),
            ("A justified conclusion, such as social media and the website together", ["conclusion", "overall", "most suitable", "best", "therefore", "recommend"]),
        ], "Social media is where many parents of 8 to 14 year olds already spend time, and a short, exciting video of children on the zip line is the kind of content families share, which spreads it for free. Paid posts can be targeted at families living within reach of the Lake District, and the analytics show how many people watched. However, the video has to compete with everything else in the feed, so it must grab attention in the first few seconds and make sense with the sound off, using captions. Each platform also needs its own aspect ratio, so square and vertical versions would be needed as well as the 16:9 original.\n\nThe centre's own website is free to use and reaches people who are already interested, such as parents comparing activity centres, and it can sit next to the booking button, which makes it very effective at turning interest into bookings. Its weakness is that it only reaches people who already know about the centre.\n\nLocal television would reach a large audience across the region, including grandparents and families who do not use social media, and it carries credibility. But airtime is expensive, far beyond a £4,000 budget, and it cannot be targeted at families as closely.\n\nOverall social media is the most suitable, because it reaches and targets the audience cheaply, with the website as the place where interested families watch the full video and book. Television is not realistic for this budget.",
              command="Discuss", label="16"),
        write("The company must plan the filming of the promotional video at the centre. Explain how it should plan the shoot, including the pre-production documents, the legal issues and health and safety.", 9, [
            ("A script for any voiceover or dialogue, and a storyboard showing every shot", ["script", "storyboard"]),
            ("A shot list or schedule saying what is filmed where and when", ["shot list", "schedule", "call sheet", "order of filming"]),
            ("A work plan with tasks, timings and milestones that fits the six week deadline", ["work plan", "gantt", "milestone", "deadline", "six weeks", "timing"]),
            ("A location recce to check light, access, power and camera positions", ["recce", "visit", "check the location"]),
            ("A risk assessment identifying hazards such as water and heights, and how to reduce them", ["risk assessment", "hazard", "water", "height", "safety"]),
            ("Permission from the centre to film on site", ["permission to film", "location permission", "centre's permission", "permission from the centre", "agree"]),
            ("Release forms from people filmed, with parental consent for children", ["release", "consent", "parent", "guardian"]),
            ("Booking the crew and equipment, including waterproof kit, within the budget", ["equipment", "crew", "book", "camera", "drone", "waterproof", "budget", "resource"]),
            ("Contingency, such as a spare day in case of bad weather", ["contingency", "spare day", "weather", "rain", "backup", "back-up"]),
        ], "The company should start with a script for the voiceover and a storyboard showing every shot, from the wide opening of the lake to close ups of children on the zip line, and get the client to approve both. From these it can write a shot list and a filming schedule, fitted into a work plan whose milestones meet the six week deadline.\n\nA location recce should be carried out first, to check the light at each activity, where cameras can be safely placed, access for equipment and whether there is power. The recce feeds a risk assessment covering the hazards of filming near deep water and at height, such as crew wearing buoyancy aids and harnesses and staying behind the centre's safety barriers.\n\nLegally, the centre must give written permission for filming on its site, and everyone who can be identified must sign a release form, with parents signing for children under 18. Any music must be licensed or royalty free.\n\nFinally the crew and equipment, such as a stabiliser, waterproof housing and microphones, must be booked within the £4,000 budget, and the schedule should include a contingency day in case rain stops the outdoor filming.",
              command="Explain", label="17"),
    ],
)


# ===================================================================== Paper C

BRIEF_C = """**Client brief: Harbour Lights music festival**

Harbour Lights is a three day music festival on the seafront in a coastal town, aimed at 16 to 25 year olds. The organisers have asked a media company to produce:

- a 30 second audio advert for local radio and online streaming services
- a set of graphics for social media, and a banner for the festival's website.

The products must use the festival's logo, a night-time seaside theme and the colours navy and gold, and must name the headline acts and the ticket website. Some of the music in the advert must be by bands who are playing at the festival. Everything must be ready eight weeks before the festival."""

R093_C = Paper(
    slug="r093-paper-c",
    title="Creative iMedia R093 Paper C: Creative iMedia in the Media Industry",
    course="Creative iMedia", board="OCR", code="R093",
    minutes=90, marks=70, accent=ACC, spec="R093", full=True,
    blurb="A full length R093 paper. Section A: ten one mark questions. Section B: a brief for a music festival's audio advert and social media graphics, covering constraints, audience, scripts, asset logs, copyright and trade marks, audio properties and file formats, and two 9 mark extended responses.",
    advice=ADVICE, calculator="You do not need a calculator.",
    instructions=["The two 9 mark questions are extended responses. In the real exam they are marked in levels; here every relevant point you make earns a mark, up to 9."],
    questions=[
        # ---------------------------------------------------- Section A
        tick("Which **one** of these is an audio product?", ["*A podcast", "A poster", "A web page", "A magazine"],
             "A podcast is audio only.", label="1", section="Section A", section_note=NOTE_A),
        tick("Which **one** job role is responsible for the budget and schedule of the whole project?",
             ["*Producer", "Video editor", "Camera operator", "Sound engineer"],
             "The producer runs the whole project: budget, schedule, hiring and delivery.", label="2"),
        tick("Which **one** of these is a source of secondary research?",
             ["*An industry report on festival audiences", "A survey of last year's visitors", "A focus group", "An interview with the client"],
             "Secondary research was collected by someone else for their own purposes, like a published report.", label="3"),
        tick("Which **one** of these is a psychographic characteristic of an audience?",
             ["*An interest in live music", "Age", "Income", "Where they live"],
             "Psychographics are interests, values and lifestyle. Age, income and location are demographics.", label="4"),
        ans("Name the pre-production document, made from a collage of images, colours, fonts and textures, that is used to agree the look and feel of a product.",
            ["mood board", "moodboard", "mood boards", "moodboards"], model="A mood board.", width=16, label="5"),
        tick("Which **one** audio file format is uncompressed?", ["*WAV", "MP3", "AAC", "MP4"],
             "WAV stores audio uncompressed. MP3 and AAC are lossy, and MP4 is a video container.", label="6"),
        tick("Which **one** organisation regulates advertising in all media in the UK?", ["*ASA", "BBFC", "PEGI", "IPSO"],
             "The Advertising Standards Authority regulates adverts in every medium.", label="7"),
        tick("Which **one** type of graphic can be enlarged to any size without losing quality?", ["*Vector", "Raster", "Bitmap", "JPG"],
             "A vector graphic is made of paths and shapes, so it is redrawn sharply at any size.", label="8"),
        tick("Which **one** law protects people's personal data?",
             ["*Data Protection Act 2018", "Computer Misuse Act 1990", "Defamation Act 2013", "Copyright, Designs and Patents Act 1988"],
             "The Data Protection Act 2018 controls how personal data is collected, stored and used.", label="9"),
        ans("Name the type of intellectual property that protects a brand's name or logo.",
            ["trade mark", "trademark", "trade marks", "trademarks", "registered trade mark", "registered trademark"],
            model="A trade mark.", width=16, label="10"),

        # ---------------------------------------------------- Section B
        write("Identify **two** constraints on the project, from the brief.", 2, [
            ("Time: everything must be ready eight weeks before the festival", ["eight weeks", "8 weeks", "deadline", "time"]),
            ("House style: the logo, the night-time seaside theme and the navy and gold colours must be used", ["logo", "navy", "gold", "theme", "colour", "house style"]),
            ("Content: the headline acts and the ticket website must be named", ["headline", "acts", "ticket website", "website"]),
            ("The advert must use music by bands playing at the festival, and be 30 seconds long", ["music", "bands", "30 seconds", "thirty"]),
        ], "Everything must be ready eight weeks before the festival, and the products must use the festival's logo and its navy and gold colours.",
              command="Identify", label="11(a)", section="Section B", section_note=NOTE_B, lead=BRIEF_C),
        write("Explain **two** ways the audio advert could be designed to appeal to 16 to 25 year olds.", 4, [
            ("Use upbeat tracks by the bands who are playing", ["upbeat", "bands", "their music", "tracks", "songs", "music"]),
            ("Because the audience will recognise the music and be excited to see the bands live", ["recognise", "excite", "fans", "live", "want to see", "know"]),
            ("Use a young, energetic, informal voiceover, with sound effects such as a cheering crowd or waves", ["voiceover", "presenter", "informal", "energetic", "young", "crowd", "waves", "sound effect"]),
            ("Because it creates the festival atmosphere and speaks to them in their own style", ["atmosphere", "feel", "their own", "relate", "style", "immerse", "picture"]),
        ], "The advert should be built around short clips of upbeat tracks by the headline bands, because the audience will recognise them and want to see those bands live. The voiceover should be young, fast and informal, over the sound of a cheering crowd and the sea, so listeners picture themselves at a night-time seaside festival.",
              command="Explain", label="11(b)"),
        write("The company wants to find out which acts the target audience would most like to see. Describe how it could collect this information.", 2, [
            ("An online survey or poll, for example on the festival's social media", ["survey", "poll", "questionnaire", "social media", "online", "vote"]),
            ("Asking them to rank or vote for acts, giving quantitative data that can be counted quickly", ["rank", "vote", "choose", "count", "quantitative", "numbers", "closed"]),
        ], "Run a poll on the festival's social media accounts, which the 16 to 25 year olds already follow, asking them to vote for the acts they most want to see. The votes can be counted quickly to show the most popular acts.",
              command="Describe", label="11(c)"),
        write("The client has given the company a formal, written brief. Explain **one** advantage of a formal brief for the media company.", 2, [
            ("Everything required is written down and agreed, so there is a clear record", ["written", "record", "agreed", "clear", "documented"]),
            ("So misunderstandings and disputes are avoided, and the company can check its work against the brief", ["misunderstand", "dispute", "disagree", "refer back", "check", "evidence", "protect"]),
        ], "A formal brief records exactly what the client asked for. If the client later disagrees with the finished products, the company can show that it met the agreed requirements, so disputes are avoided.",
              command="Explain", label="11(d)"),
        write("Describe the purpose of a script for the audio advert.", 2, [
            ("It sets out exactly what the voiceover will say", ["voiceover", "words", "what is said", "dialogue", "speech"]),
            ("And when music and sound effects come in, with timings, so the advert fits 30 seconds", ["music", "sound effect", "cue", "timing", "30 seconds", "length", "when"]),
        ], "The script sets out every word of the voiceover and marks when each music clip and sound effect comes in, with timings, so the voice artist and the editor produce an advert that fits exactly 30 seconds.",
              command="Describe", label="12(a)"),
        tick("Which **three** pieces of information should the script for the audio advert include?",
             ["*The words of the voiceover", "*Cues for the music and sound effects", "*Timings, so the advert lasts 30 seconds",
              "Camera angles", "Font sizes", "The colour palette"],
             "An audio script needs the words, the sound cues and the timings. Camera angles, fonts and colours do not apply to audio.",
             label="12(b)"),
        write("Explain why a visualisation diagram should be produced for the website banner before it is created.", 2, [
            ("It shows the planned layout, colours, fonts and images of the banner", ["layout", "colour", "font", "image", "position", "look"]),
            ("So the client can approve it, or ask for changes, before time is spent creating it", ["approve", "agree", "client", "change", "before", "feedback", "time"]),
        ], "A visualisation diagram shows where the logo, text and images will go and the exact navy and gold to be used, so the client can approve the design, or ask for changes, before the designer spends time creating it.",
              command="Explain", label="12(c)"),
        write("The company keeps an asset log for the project. Identify **three** items of information that should be recorded for each asset.", 3, [
            ("A description or name of the asset", ["name", "description", "what it is", "title"]),
            ("Its source, where it came from", ["source", "where it came", "url", "website", "creator", "from"]),
            ("Its file format and properties, such as dimensions", ["format", "file type", "dimension", "resolution", "size", "properties"]),
            ("Its licence or permission, and whether it is cleared for use", ["licence", "license", "permission", "copyright", "cleared", "rights"]),
        ], "For each asset: what it is, where it came from, and the licence or permission that allows it to be used.",
              command="Identify", label="12(d)"),
        rows("Tick (✓) one box in each row to show the phase of production each task belongs to.",
             ["Pre-production", "Production", "Post-production"],
             [("Writing the script", "Pre-production"), ("Recording the voiceover in a studio", "Production"),
              ("Mixing the voiceover with the music", "Post-production"), ("Booking the voiceover artist", "Pre-production")],
             marks=2, model="Planning and booking happen in pre-production, recording in production, and mixing in post-production.",
             label="12(e)"),
        write("Explain how the company can legally use music by the festival's bands in the advert.", 3, [
            ("The music is protected by copyright, owned by the band, songwriter or record label", ["copyright", "owned", "band", "record label", "songwriter", "owner"]),
            ("The company must get permission, a licence, from the rights holders", ["permission", "licence", "license", "rights holder"]),
            ("Paying any fee or royalties, and using the music only as the licence allows", ["fee", "pay", "royalt", "terms", "only as", "conditions"]),
        ], "The songs are protected by copyright, usually owned by the songwriters and the record label. The company must get a licence from the rights holders to use them in an advert, pay any fee or royalties, and use the clips only in the ways the licence allows. The bands may agree readily, because the advert promotes them.",
              command="Explain", label="13(a)"),
        write("The company wants to use photographs of last year's festival that it found on a photographer's website. Explain **two** legal issues with doing this.", 4, [
            ("The photographer owns the copyright in the photographs", ["copyright", "photographer owns", "owned by", "owner"]),
            ("So the company needs the photographer's permission, a licence, possibly for a fee; using them without it is infringement", ["permission", "licence", "license", "fee", "pay", "infring", "sued"]),
            ("People in the photographs can be identified, so their privacy is affected", ["identif", "privacy", "people in", "faces", "recognis"]),
            ("So permission or model releases are needed before using them in an advert", ["release", "consent", "permission from the people", "agree", "model release"]),
        ], "First, the photographer owns the copyright in the photographs, so the company must get permission and a licence, probably for a fee; using them without one is copyright infringement and could lead to legal action. Second, festival-goers can be recognised in the photographs. Using their images to advertise without their consent affects their privacy, so the company would need model releases or should choose photographs in which no one can be identified.",
              command="Explain", label="13(b)"),
        rows("Tick (✓) one box in each row to show the legal issue each situation raises.",
             ["Defamation", "Copyright", "Data protection", "Trade mark"],
             [("The advert falsely says a rival festival is unsafe", "Defamation"),
              ("Email addresses are collected through a ticket competition", "Data protection"),
              ("Another company's logo is used without permission", "Trade mark"),
              ("A song is used without a licence", "Copyright")],
             marks=2, model="A false, damaging claim is defamation, personal data is data protection, a logo is a trade mark, and a song is copyright.",
             label="13(c)"),
        tick("Which **one** audio file format is most suitable for streaming the advert online?", ["*MP3", "WAV", "AIFF", "FLAC"],
             "MP3 is compressed and plays everywhere. WAV and AIFF are uncompressed and FLAC is a large lossless format.", label="14(a)"),
        write("Explain why the social media graphics must be produced in several different sizes.", 2, [
            ("Each platform, and each type of post, uses different dimensions and aspect ratios, such as square posts and vertical stories", ["different", "aspect ratio", "dimension", "square", "vertical", "stories", "each platform"]),
            ("So each graphic displays correctly, without being cropped, stretched or squashed", ["cropped", "stretched", "distort", "squash", "displays correctly", "cut off", "fits"]),
        ], "Each platform uses its own dimensions, such as square feed posts and vertical 9:16 stories. A graphic made for one would be cropped or distorted on another, cutting off the acts' names or the ticket website.",
              command="Explain", label="14(b)"),
        write("Explain **two** properties of the audio advert file that affect both its quality and its file size.", 4, [
            ("Sample rate: the number of samples taken each second", ["sample rate", "samples per second", "khz", "hz"]),
            ("A higher sample rate gives better quality but a larger file", ["higher", "better quality", "larger", "bigger", "more accurate"]),
            ("Bit depth: the number of bits used for each sample; or the bit rate, the bits used per second", ["bit depth", "bits per sample", "bit rate", "kbps", "resolution"]),
            ("More bits give more accurate, higher quality sound but a larger file", ["more bits", "larger", "bigger", "quality", "detail", "dynamic range"]),
        ], "The sample rate is the number of times the sound is measured each second, such as 44.1 kHz: a higher rate records the sound more accurately but makes the file larger. The bit depth is the number of bits used to store each sample: more bits capture the volume more precisely, giving better quality, but again increase the file size.",
              command="Explain", label="14(c)"),
        rows("Tick (✓) one box in each row to show the most suitable file format for each file.", ["SVG", "JPG", "PNG", "WAV"],
             [("The festival logo, which must be resized for the banner", "SVG"), ("A photograph of the stage for a social media post", "JPG"),
              ("A gold title graphic with a transparent background", "PNG"), ("The edited master copy of the audio advert", "WAV")],
             marks=2, model="SVG scales without loss, JPG keeps photographs small, PNG keeps transparency, and WAV keeps the master at full quality.",
             label="14(d)"),
        write("Explain **one** advantage and **one** disadvantage of streaming the advert online, compared with the listener downloading it.", 2, [
            ("Advantage: it plays almost immediately, without waiting for the whole file, and takes no storage on the device", ["immediately", "straight away", "no waiting", "storage", "starts quickly", "no space"]),
            ("Disadvantage: it needs a constant internet connection, and may buffer on a slow connection", ["connection", "internet", "buffer", "signal", "offline", "slow"]),
        ], "Streaming starts playing almost at once and uses no storage on the listener's phone. But it needs a constant connection, so on a weak signal it may buffer or stop.",
              command="Explain", label="14(e)"),
        write("Discuss whether the festival should advertise mainly on local radio or mainly on social media to reach its target audience.", 9, [
            ("Social media is where most 16 to 25 year olds spend their time", ["social media", "spend time", "young people", "16 to 25", "most use", "tiktok", "instagram"]),
            ("Social media adverts can be targeted by age, interests and location, so money is not wasted", ["target", "interest", "location", "age", "not wasted"]),
            ("Posts can be shared and commented on by friends, spreading the advert for free", ["share", "comment", "friends", "viral", "free", "engage"]),
            ("Social media gives analytics showing who saw the advert and how many bought tickets", ["analytics", "data", "track", "measure", "clicks", "who saw"]),
            ("A link can take people straight to the ticket website", ["link", "click", "straight to", "ticket website", "buy"]),
            ("Local radio reaches people in the area around the festival, and an audio advert suits it", ["local", "area", "nearby", "radio", "audio"]),
            ("But fewer 16 to 25 year olds listen to local radio, and listeners cannot click through to buy", ["fewer", "older", "don't listen", "do not listen", "cannot click", "can't click", "no link"]),
            ("Radio airtime costs more and the effect is harder to measure", ["cost", "expensive", "harder to measure", "cannot measure", "no data"]),
            ("A justified conclusion: social media should be the main platform, perhaps supported by radio", ["conclusion", "overall", "main", "best", "therefore", "recommend", "both"]),
        ], "Social media is where most 16 to 25 year olds spend their time, so it is the most direct way to reach them. Adverts can be targeted at people of the right age who like the headline bands and live within travelling distance, so little money is wasted on the wrong audience. Posts can be shared and tagged among friends, which spreads the advert for free and suits a festival that people go to in groups. Every post can carry a link straight to the ticket website, and the analytics show how many people saw the advert and how many went on to buy.\n\nLocal radio reaches everyone in the area around the festival, including people driving or working, and it is the natural home for the audio advert the client has asked for. However, far fewer 16 to 25 year olds listen to local radio than use social media, listeners cannot click through to buy a ticket, and airtime is more expensive while its effect is harder to measure.\n\nOverall social media should be the main platform, because it reaches, targets and converts this audience best. The audio advert can still be used there and on streaming services, with a smaller amount of local radio to reach people in the town itself.",
              command="Discuss", label="15"),
        write("Explain how the company should plan the production of the audio advert, so that it is finished on time and meets the brief.", 9, [
            ("A work plan or Gantt chart with every task and its duration", ["work plan", "gantt", "task", "duration", "schedule"]),
            ("Milestones, such as the client approving the script, working back from the eight week deadline", ["milestone", "approve", "sign off", "sign-off", "eight weeks", "8 weeks", "deadline"]),
            ("Contingency time in case of delays", ["contingency", "spare time", "delay", "extra time"]),
            ("Writing the script, with the voiceover and the music and sound effect cues, and getting it approved", ["script"]),
            ("Licensing the bands' music early, because permission can take time", ["licen", "permission", "rights", "copyright", "early"]),
            ("Booking the voiceover artist and the recording studio, the resources needed", ["book", "voiceover artist", "studio", "resource", "equipment"]),
            ("An asset log of every sound and music clip, its source and its licence", ["asset log", "asset list", "assets"]),
            ("Post-production: editing and mixing to exactly 30 seconds, then a client review", ["edit", "mix", "30 seconds", "review", "post-production", "feedback"]),
            ("Exporting in the formats the radio station and streaming services require, and testing it", ["export", "format", "mp3", "wav", "test", "radio station", "specification"]),
        ], "The company should start by working back from the deadline, eight weeks before the festival, to build a work plan or Gantt chart listing every task, how long it takes and which tasks depend on others, with contingency time in case something is delayed. Milestones should include the client approving the script and approving the final mix.\n\nIn pre-production the scriptwriter writes the 30 second script, setting out the voiceover and the cues for the music and sound effects. Because some of the music must be by the festival's bands, licences should be requested at the very start, as permission can take weeks, and every clip should be recorded in an asset log with its source and licence. The voiceover artist and the studio must be booked for the recording day.\n\nAfter recording, the editor mixes the voiceover with the music and effects, cutting it to exactly 30 seconds, and the client reviews it. Finally it is exported in the formats the radio station and streaming services require, and tested on phone speakers and car radios, before the deadline.",
              command="Explain", label="16"),
    ],
)

PAPERS = [R093_B, R093_C]
