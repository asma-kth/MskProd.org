"""OCR Level 1/Level 2 Cambridge National in Creative iMedia J834.

R093 is the written paper: 70 marks, 1 hour 15 minutes, and the only unit
here that is examined. It is covered topic area by topic area, in the depth
the paper actually asks for.

R094 and R097 are internally assessed set assignments. They have no exam, so
their pages do not pretend to have one: the written practice on those topics
is headed "Check you could explain this" and is aimed at understanding the
assessment criteria rather than at sitting a paper.

A note on the exam-style questions. They are written to match the real
paper's command words, mark tariffs and scenario style, and the extended
answers use the same levels-of-response shape. They are not copies of OCR
past papers, which are OCR's copyright; they are practice in the same form.
"""
from mskbuild.models import Topic, Section, Unit, Course, Q, EQ, MP

# =============================================================== R093 TA1

M_SECTORS = Topic(
    slug="the-media-industry",
    title="R093 TA1: Sectors, Products and Purpose",
    spec="R093 TA1",
    icon="i-video",
    minutes=24,
    blurb="The sectors of the media industry, the products each one makes, and the purpose behind every product. The paper opens here almost every year.",
    fact="The credits on a feature film can run past two thousand names. Almost none of them are people the audience could name, and most of their work happened before a single frame was shot or long after the last one was.",
    sections=[
        Section("The sectors", """
The media industry is split into sectors. A sector is a group of companies making the same broad kind of product. You need to be able to name them and give products for each, because the paper asks for exactly that.

| Sector | What it makes |
| **Television and film** | Programmes, feature films, adverts, trailers, streaming series |
| **Publishing** | Books, magazines, newspapers, e-books, digital editions |
| **Advertising and marketing** | Campaigns, banner adverts, social media content, branding |
| **Music** | Recordings, streaming releases, music videos, cover artwork |
| **Video games** | Console, PC and mobile games, and the assets inside them |
| **Web and app development** | Websites, mobile apps, web applications |
| **Photography** | Commercial, editorial, product and event photography |
| **Animation and visual effects** | 2D and 3D animation, motion graphics, VFX for film |

!key Sector is not the same as product :: A sector is the part of the industry. A product is the thing it makes. "Television and film" is a sector; "a trailer" is a product. Questions that ask for a sector and get a product back score nothing.

### Companies work across sectors

A single company often sits in several. A games studio makes the game (video games), the trailer for it (television and film) and the website that sells it (web development). If a question describes a company, read what it actually produces rather than what its name suggests.
"""),
        Section("Types of product", """
Products are grouped by the form they take, and this is the other half of the same question.

| Type | Examples |
| **Audio visual** | Film, television, animation, video, streaming content |
| **Print based** | Magazines, books, posters, packaging, leaflets, newspapers |
| **Digital and interactive** | Websites, apps, games, interactive multimedia, e-learning |
| **Audio** | Podcasts, radio programmes, music, sound effects |
| **Multimedia** | Products combining several of the above, such as a museum kiosk |

A product can belong to more than one type. A music video is audio visual and audio. A website carrying video is digital and interactive, and audio visual.
"""),
        Section("Purpose", """
Every media product exists to do something. The specification lists these, and a question asking for "the purpose" wants one of them, not a description of the product.

- **Entertain** — a drama series, a game, a comedy podcast
- **Inform** — a news bulletin, a documentary, an instruction leaflet
- **Educate** — a revision website, a training video, an e-learning module
- **Advertise or promote** — a poster, a trailer, a sponsored social post
- **Persuade or influence** — a charity appeal, a political broadcast
- **Provide a service** — online banking, a council website, a booking app

### Most products have more than one purpose

A charity television advert entertains enough to stop you skipping it, informs you about the problem, and persuades you to donate. Saying only "to advertise" leaves marks on the table when the question is worth more than one.

!grade How to turn a 1 mark answer into a 3 mark answer :: Name the purpose, say which part of the product achieves it, and say what effect that has on the audience. "To persuade. The closing shot of the child looking at the camera with the donation number over it is designed to make the viewer feel personally responsible, so they are more likely to give."
"""),
    ],
    keyterms=[
        ("Sector", "A part of the media industry grouping companies that make the same broad kind of product."),
        ("Audio visual", "A product combining moving image and sound, such as film, television or animation."),
        ("Purpose", "What a media product is made to do: entertain, inform, educate, advertise, persuade or provide a service."),
        ("Multimedia", "A product that combines several media types, such as text, image, audio and video together."),
    ],
    grade="""
The difference between a pass and a distinction on this topic area is almost always **specificity**. "A magazine" is a product. "A monthly print magazine for mountain bikers, sold in supermarkets and by subscription" shows you understand the sector, the product, the audience and the distribution all at once, and the longer questions are marked on exactly that.
""",
    mistakes=[
        "Giving a product when the question asked for a sector, or the other way round.",
        "Listing only one purpose when the question is worth three or more marks.",
        "Naming a company rather than a sector. Netflix is a company; television and film is the sector.",
        "Writing 'social media' as a sector. It is a distribution platform, and it belongs in TA4.",
    ],
    quiz=[
        Q("Which of these is a sector rather than a product?",
          ["Publishing", "A trailer", "A podcast", "A banner advert"], 0,
          "Publishing is a part of the industry. The other three are things that get made."),
        Q("A company produces podcasts. Which type of product is that?",
          ["Audio", "Print based", "Audio visual", "Interactive"], 0,
          "A podcast is sound only, so it is an audio product."),
        Q("What is the main purpose of a council website that lets you report a pothole?",
          ["Provide a service", "Entertain", "Advertise", "Educate"], 0,
          "It exists so the public can do something, which is the definition of providing a service."),
        Q("Which sector would produce the cover artwork for an album?",
          ["Music", "Publishing", "Photography", "Animation"], 0,
          "Album artwork is produced within the music sector, usually by a designer working for the label."),
        Q("A museum kiosk combines text, photographs, audio narration and video. What type of product is it?",
          ["Multimedia", "Print based", "Audio", "Audio visual"], 0,
          "It combines several media types in one product, which is what multimedia means."),
        Q("Which of these best describes the purpose of a film trailer?",
          ["Advertise and persuade", "Educate and inform", "Provide a service", "Entertain only"], 0,
          "A trailer exists to advertise the film and persuade you to watch it. It entertains only as a means to that end."),
        Q("Which product type is a monthly magazine?",
          ["Print based", "Digital and interactive", "Audio visual", "Audio"], 0,
          "A printed magazine is a print based product, even if a digital edition also exists."),
        Q("A studio makes a mobile game, its launch trailer and its website. How many sectors is it working across?",
          ["Three", "One", "Two", "Four"], 0,
          "Video games, television and film, and web development: three sectors from one project."),
        Q("Which purpose does a supermarket's recipe video on social media mainly serve?",
          ["Advertise or promote", "Provide a service", "Educate", "Inform"], 0,
          "It teaches you a recipe, but it exists to sell the ingredients, so promotion is the purpose."),
        Q("What is wrong with giving 'Netflix' as an answer to 'name a sector of the media industry'?",
          ["Netflix is a company, not a sector", "Netflix is not a media business",
           "Netflix is a product", "Nothing, it is correct"], 0,
          "The sector is television and film. Netflix is one company operating within it."),
    ],
    exam=[
        EQ("Identify **two** sectors of the media industry and give **one** product made by each.", 4,
           [MP("A valid sector is named", ["television", "film", "publishing", "advertising", "music", "games", "web", "photography", "animation"]),
            MP("A product that genuinely belongs to that sector", ["trailer", "magazine", "poster", "website", "game", "podcast", "advert", "book"]),
            MP("A second, different valid sector is named", ["second sector", "publishing", "music", "games", "photography", "animation", "web"]),
            MP("A product that genuinely belongs to the second sector", ["product", "book", "app", "music video", "photograph"])],
           "Television and film is a sector, and it produces products such as film trailers. Publishing is a second sector, and it produces products such as monthly magazines.",
           command="Identify"),
        EQ("State **three** different purposes a media product might have.", 3,
           [MP("One purpose from the specification list", ["entertain", "inform", "educate", "advertise", "promote", "persuade", "influence", "service"]),
            MP("A second, different purpose", ["inform", "educate", "advertise", "persuade", "entertain", "service"]),
            MP("A third, different purpose", ["educate", "persuade", "service", "promote", "inform", "entertain"])],
           "To entertain, to inform and to persuade.",
           command="State"),
        EQ("A charity is producing a 30 second television advert asking the public to donate.\n\nExplain **two** purposes this product has and how each one is achieved.", 4,
           [MP("Persuade is identified as a purpose", ["persuade", "influence", "convince", "donate"]),
            MP("How persuasion is achieved in the advert", ["emotive", "music", "close up", "real people", "call to action", "donation number", "story"]),
            MP("Inform is identified as a second purpose", ["inform", "educate", "aware", "facts", "statistics"]),
            MP("How informing is achieved", ["statistic", "voiceover", "caption", "explains", "shows the problem"])],
           "One purpose is to persuade, which is achieved through emotive content: close shots of an affected child with slow music underneath, ending on a direct call to action with the donation number on screen. A second purpose is to inform, which is achieved through a voiceover and on screen captions giving statistics about how many people the problem affects, so that the viewer understands why their donation is needed.",
           command="Explain"),
        EQ("A publisher is launching a monthly print magazine about climbing, aimed at experienced climbers.\n\nDiscuss how the sector it belongs to, the type of product it is, and its purpose affect the decisions the publisher must make.", 8,
           [MP("The sector is correctly identified as publishing", ["publishing", "print"]),
            MP("The product type is correctly identified as print based", ["print based", "print", "magazine"]),
            MP("At least one purpose is identified", ["inform", "entertain", "advertise", "educate"]),
            MP("A decision that follows from it being print", ["CMYK", "resolution", "300", "dpi", "bleed", "paper", "print deadline", "cannot be changed", "fixed"]),
            MP("A decision that follows from the audience being experienced", ["technical", "jargon", "assumed knowledge", "specialist", "advanced", "not beginner"]),
            MP("A decision that follows from the purpose", ["advertisers", "content mix", "reviews", "features", "informing"]),
            MP("A consequence of being monthly rather than daily or online", ["lead time", "deadline", "cannot update", "planned in advance", "schedule"]),
            MP("A judgement that weighs the points against each other", ["most important", "overall", "therefore", "the main constraint"])],
           "The magazine sits in the publishing sector and is a print based product, and both of those shape the work. Because it is printed, every image must be supplied at around 300 dpi in CMYK rather than RGB, pages need bleed, and once the issue goes to press nothing can be corrected, so proofreading and sign off matter far more than they would online. Because it is monthly, the content has a long lead time and must be planned issue by issue; it cannot react to news in the way a website could, so the publisher will favour features and reviews over reporting. The purposes are to inform and to entertain, with a commercial purpose underneath, since the magazine is funded by advertisers who want to reach climbers, and that affects the mix of content and where adverts sit. Because the audience is experienced rather than beginner, the writing can use technical terms without explaining them, and the photography has to be credible to people who climb, since a staged or technically wrong image would lose the readers' trust. The constraint that drives the most decisions is print itself: it fixes the deadline, the colour mode and the resolution, and it removes any chance of correcting a mistake afterwards.",
           command="Discuss"),
    ],
)

M_ROLES = Topic(
    slug="job-roles-in-media",
    title="R093 TA1: Job Roles and Working in the Industry",
    spec="R093 TA1",
    icon="i-user",
    minutes=26,
    blurb="Who does what, at which stage, and the difference between being employed and being freelance. Expect to name roles and say what they are responsible for.",
    fact="The job title 'best boy' on a film crew is the chief assistant to the gaffer, who runs the lighting department. Neither title tells you anything about the job, which is why the exam asks you to describe responsibilities rather than recognise names.",
    sections=[
        Section("Pre-production roles", """
Pre-production is everything before anything is made. These roles plan it.

| Role | Responsible for |
| **Client** | Commissioning the work and defining what is needed |
| **Producer** | The whole project: budget, schedule, hiring, and delivery |
| **Project manager** | Coordinating people, deadlines and resources day to day |
| **Scriptwriter** | Writing the script, dialogue or copy |
| **Storyboard artist** | Drawing the planned shots so everyone can see the intention |
| **Concept artist** | Producing early visual ideas for characters, locations and style |
| **Researcher** | Finding facts, locations, contributors and reference material |

!key Producer against director :: The producer is responsible for the project: money, people and deadlines. The director is responsible for the creative decisions: how it looks, sounds and performs. A question asking you to distinguish them is asking for exactly that split.
"""),
        Section("Production and post-production roles", """
### Production

| Role | Responsible for |
| **Director** | Creative decisions, directing performers and crew |
| **Camera operator** | Operating the camera to get the shots the director wants |
| **Sound engineer** | Capturing clean audio on location or in a studio |
| **Lighting technician** | Setting up lighting to achieve the intended look |
| **Graphic designer** | Creating visual assets, layouts and branding |
| **Web developer** | Building the website or web application |
| **Games developer** | Designing and programming the game |
| **Animator** | Creating moving images from drawings, models or rigs |
| **Photographer** | Taking the photographs the brief requires |

### Post-production

| Role | Responsible for |
| **Video editor** | Assembling the footage into the finished sequence |
| **Sound editor** | Editing and mixing audio, adding effects and music |
| **VFX artist** | Adding visual effects and compositing elements together |
| **Colourist** | Grading the footage so the colour is consistent and intentional |
| **Quality assurance tester** | Finding faults before the product reaches the audience |
"""),
        Section("Employment and working patterns", """
You need the difference between these, and the advantages and drawbacks of each, because it is a reliable source of four mark questions.

| | Employed | Freelance |
| **Paid** | A regular salary | Per job or per day |
| **Work** | Provided by the employer | Must be found by the individual |
| **Holiday and sick pay** | Yes | No |
| **Equipment** | Provided | Usually their own |
| **Tax** | Deducted automatically | Self assessed |
| **Variety** | One employer, steady work | Many clients, varied projects |
| **Security** | Higher | Lower, with gaps between jobs |

### Contract types

- **Permanent** — ongoing, no end date
- **Fixed term** — a contract ending on a set date, common for one production
- **Freelance** — self employed, working for a client on a contract basis
- **Part time and shift work** — common in broadcast, where output is continuous

!grade Say why it suits the industry :: Media work is project based: a drama needs forty people for ten weeks and none of them afterwards. That is the reason freelancing is so common, and saying it is what lifts an answer from listing differences to explaining them.
"""),
    ],
    keyterms=[
        ("Producer", "The person responsible for the project as a whole: budget, schedule, staffing and delivery."),
        ("Director", "The person responsible for the creative decisions and for directing cast and crew."),
        ("Freelance", "Self employed, working for clients job by job rather than for one employer."),
        ("Post-production", "Everything done after filming or capture: editing, sound, effects and grading."),
        ("Quality assurance", "Systematic testing to find faults before a product is released."),
    ],
    grade="""
Top answers attach the role to the **stage** and to a **consequence**. Not "the editor edits the video" but "the video editor works in post-production, assembling the footage into the final sequence, so if the camera operator failed to shoot enough coverage the editor has nothing to cut to and the problem surfaces weeks after the shoot has wrapped."
""",
    mistakes=[
        "Confusing the producer with the director. Producer is money, people and deadlines; director is creative.",
        "Describing a role by its name rather than its responsibility. 'A sound engineer does the sound' earns nothing.",
        "Putting a role in the wrong stage, such as calling the editor a production role.",
        "Listing freelance advantages without saying who they are an advantage for, the worker or the company.",
    ],
    quiz=[
        Q("Who is responsible for the budget and schedule of a production?",
          ["The producer", "The director", "The editor", "The client"], 0,
          "The producer runs the project: money, people and deadlines."),
        Q("At which stage does a storyboard artist work?",
          ["Pre-production", "Production", "Post-production", "Distribution"], 0,
          "The storyboard is drawn before anything is shot, so it is pre-production."),
        Q("A freelancer is ill for a week. What happens to their pay?",
          ["They are not paid", "They receive sick pay", "Their client pays half", "They are paid as normal"], 0,
          "Freelancers are self employed, so there is no sick pay. That is the main drawback."),
        Q("Who makes the creative decisions about how a scene should look and be performed?",
          ["The director", "The producer", "The camera operator", "The project manager"], 0,
          "That is the director's job. The camera operator executes it."),
        Q("Which role would add explosions and composite a background into live footage?",
          ["VFX artist", "Colourist", "Sound editor", "Animator"], 0,
          "Visual effects and compositing are the VFX artist's work, in post-production."),
        Q("Why is freelancing so common in the media industry?",
          ["Work is project based, so teams are needed only for a period",
           "Companies are not allowed to employ people permanently",
           "Freelancers are always cheaper",
           "There are no permanent roles in media"], 0,
          "A production needs a large crew for a short time and none of them afterwards."),
        Q("Which role finds faults in a game before release?",
          ["Quality assurance tester", "Games developer", "Producer", "Concept artist"], 0,
          "QA testing exists to catch faults before the audience does."),
        Q("A contract runs for the eight weeks of one production and then ends. What type is it?",
          ["Fixed term", "Permanent", "Freelance", "Part time"], 0,
          "A contract with a set end date is fixed term."),
        Q("Which of these is a pre-production role?",
          ["Concept artist", "Colourist", "Video editor", "Sound editor"], 0,
          "Concept art is produced during planning. The other three are post-production."),
        Q("What does a colourist do?",
          ["Grades footage so colour is consistent and intentional",
           "Chooses the colours for a logo",
           "Paints backgrounds for animation",
           "Decides the colour mode for printing"], 0,
          "Colour grading is a post-production job on moving image."),
    ],
    exam=[
        EQ("Identify **two** job roles involved in the pre-production stage and describe the responsibility of each.", 4,
           [MP("A genuine pre-production role is named", ["scriptwriter", "storyboard artist", "producer", "concept artist", "researcher", "project manager", "client"]),
            MP("Its responsibility is described, not just restated", ["writes", "plans", "draws", "coordinates", "defines", "finds"]),
            MP("A second, different pre-production role is named", ["storyboard", "concept", "researcher", "producer", "scriptwriter"]),
            MP("The second responsibility is described", ["responsible for", "draws", "produces", "manages", "researches"])],
           "A scriptwriter is responsible for writing the script, including the dialogue and the scene descriptions the crew will work from. A storyboard artist is responsible for drawing the planned shots in sequence, so that the director, camera operator and editor can all see the intended framing and order before anything is filmed.",
           command="Identify"),
        EQ("Explain the difference between the role of the producer and the role of the director.", 4,
           [MP("The producer's area is identified as the project rather than the content", ["budget", "schedule", "money", "deadlines", "hiring", "organises", "manages the project"]),
            MP("An example of a producer decision", ["budget", "hires", "signs off", "schedule", "deadline"]),
            MP("The director's area is identified as creative", ["creative", "how it looks", "performances", "directs", "vision", "shots"]),
            MP("An example of a director decision", ["camera", "performance", "framing", "tone", "look"])],
           "The producer is responsible for the project rather than its content: they secure and control the budget, build the schedule, hire the crew and are accountable for delivering on time. The director is responsible for the creative decisions: how the product looks and sounds, how performers play a scene and what each shot contains. In short, the producer decides what is possible and the director decides what it will be.",
           command="Explain"),
        EQ("Explain **two** disadvantages of working as a freelancer in the media industry.", 4,
           [MP("One genuine disadvantage is identified", ["no sick pay", "no holiday pay", "insecure", "gaps", "must find work", "irregular income"]),
            MP("It is explained rather than stated", ["because", "which means", "so they", "this leads to"]),
            MP("A second, different disadvantage", ["own equipment", "tax", "self assessment", "no pension", "no training"]),
            MP("The second is explained", ["because", "means", "has to pay", "responsible for"])],
           "One disadvantage is that there is no holiday or sick pay, so any time a freelancer is not working is time they earn nothing, and an illness during a contracted shoot can cost them the fee entirely. A second is that they must constantly find their own work, which means unpaid time spent pitching and networking between jobs, and income that varies sharply from month to month even when the annual total is good.",
           command="Explain"),
        EQ("A small studio has been commissioned to produce a two minute promotional video for a local theatre.\n\nIdentify **three** job roles the studio will need and justify why each is required.", 6,
           [MP("A role appropriate to the product is named", ["director", "camera operator", "editor", "scriptwriter", "sound", "producer"]),
            MP("A justification tied to this product rather than generic", ["because the video needs", "to plan", "to film", "the theatre"]),
            MP("A second appropriate role", ["camera", "editor", "sound", "director", "producer"]),
            MP("A justification for the second", ["because", "needed to", "without this"]),
            MP("A third appropriate role", ["editor", "sound", "camera", "director"]),
            MP("A justification for the third", ["because", "so that", "required to"])],
           "A scriptwriter is required to turn the theatre's brief into a two minute structure with a voiceover, because at that length every line has to earn its place and that cannot be improvised on the day. A camera operator is required to capture the footage of performances and the building to the framing the director wants, because the quality of the original capture limits everything that can be done later. A video editor is required to assemble the footage, cut it to two minutes and lay the voiceover and music against it, because the pace of a promotional video is created in the edit rather than on the shoot.",
           command="Justify"),
    ],
)

# =============================================================== R093 TA2

M_CLIENT = Topic(
    slug="client-requirements-and-the-brief",
    title="R093 TA2: Client Requirements and the Brief",
    spec="R093 TA2",
    icon="i-paper",
    minutes=24,
    blurb="How a client sets out what they want, the difference between what they say and what they also need, and the constraints every job arrives with.",
    fact="A brief that says only 'make us a logo' is the most expensive kind of brief, because every assumption the designer makes has to be unmade later. Experienced studios refuse to start without a written one.",
    sections=[
        Section("What a client brief contains", """
A **client brief** is the document that says what the client needs. Written properly, it answers six questions, and the exam expects you to know them because almost every longer question starts from a brief.

| In the brief | What it tells you |
| **Purpose** | What the product is for: to inform, promote, entertain, provide a service |
| **Target audience** | Who it is for, in detail, not "everyone" |
| **Message** | The single idea the audience should take away |
| **Content** | What must be included: text, images, logo, contact details, legal lines |
| **Deliverables** | Exactly what is handed over, in which formats and sizes |
| **Constraints** | Deadline, budget, house style, platform, legal limits |

### Types of brief

| Type | How it works |
| **Negotiated** | Client and agency discuss and agree it together, so both sides understand it |
| **Commission** | The client approaches a specific company and asks them to produce the work |
| **Formal** | A written, contractual document, used where the money or risk is significant |
| **Informal** | Discussed verbally, quick but easy to dispute later |
| **Contractual** | Legally binding, setting out deliverables, payment and ownership |
| **Tender** | The client invites several companies to bid, and picks one |
| **Cooperative** | Two or more companies work on the brief together |

!key Why the type matters :: The type decides what happens when there is a disagreement. An informal brief leaves no record of what was agreed, so the client can insist they asked for something they never mentioned. Questions about brief types are really questions about risk.
"""),
        Section("Explicit and implicit requirements", """
This distinction is worth marks almost every year, and students lose them by not knowing the words.

- **Explicit requirements** are stated in the brief. "The logo must work in one colour." "Deliver by 14 March." "Include the charity number."
- **Implicit requirements** are not stated, but the client would expect them anyway. Correct spelling. A logo that still reads at the size of a pen. Images the client actually has the right to use. Accessible contrast. Files that open on the client's software.

### Why implicit requirements get missed

Nobody writes down what they assume. A client asking for a website does not say "and it should work on a phone", because to them that is what a website is. Two thirds of their visitors will be on a phone, so if it does not work there, the job has failed even though the brief never mentioned it.

!warn Being technically right is not the same as being right :: Delivering exactly what the brief listed, with a typo in the client's own name, fails. The explicit requirements were met and an implicit one was not, and the client will only see the typo.
"""),
        Section("Constraints and limitations", """
Every job has limits. Naming them is a one mark answer; explaining what each one forces you to change is a three mark answer.

| Constraint | What it forces |
| **Time** | Fewer concepts, simpler production, earlier sign off |
| **Budget** | Stock images instead of a shoot, one voice actor instead of three |
| **Resources** | The software, cameras and people actually available |
| **Technical** | Resolution, file size limits, codecs, platform specifications |
| **Legal** | Clearances, certification, advertising rules, data protection |
| **House style** | The client's existing fonts, colours and logo rules must be obeyed |
| **Platform** | A square crop for one feed, 16:9 for another, 9:16 for a third |

### Working with a client

- **Negotiation** happens where the brief asks for something impossible in the time or money available. It is normal, and it is better done at the start.
- **Sign off** is the client formally approving a stage. Once a stage is signed off, changes to it cost money, which is why sign off points exist at all.
- **Scope creep** is requirements growing after the brief was agreed. The defence is a written brief and recorded sign off.

!grade Turn a limitation into a decision :: "The budget was limited" earns little. "The budget would not cover a photo shoot, so the campaign was built around bold typography and one licensed stock image, which also meant the design worked at any size without recropping" earns the mark, because it names the constraint and the decision that followed from it.
"""),
    ],
    keyterms=[
        ("Client brief", "The document setting out the purpose, audience, message, content, deliverables and constraints of a job."),
        ("Explicit requirement", "Something the brief states directly."),
        ("Implicit requirement", "Something the client expects without stating it, such as correct spelling or mobile support."),
        ("Tender", "A brief offered to several companies, who each bid for the work."),
        ("Sign off", "Formal client approval of a stage, after which changes cost time and money."),
        ("Scope creep", "Requirements expanding after the brief has been agreed."),
        ("House style", "A client's existing rules for fonts, colours and logo use."),
    ],
    grade="""
The top band answers tie every requirement to a **consequence for the work**. A brief is not a list to be repeated back; it is a set of instructions that each rule out some options and force others. Show that chain — requirement, decision, effect on the audience — and the marks follow.
""",
    mistakes=[
        "Confusing explicit and implicit. Explicit is written down; implicit is assumed.",
        "Listing constraints without saying what each one changes about the work.",
        "Describing the audience as 'everyone', which tells a designer nothing.",
        "Forgetting that a deliverable includes the format and size, not just the thing itself.",
        "Treating negotiation as failure. Agreeing a realistic brief at the start is professional.",
    ],
    quiz=[
        Q("Which of these is an implicit requirement?",
          ["The text being free of spelling errors", "A 14 March deadline",
           "Including the charity number", "Supplying the logo as an SVG"], 0,
          "Nobody writes 'spell it correctly' in a brief, but every client expects it."),
        Q("A client invites four agencies to bid for a job. What type of brief is that?",
          ["Tender", "Commission", "Negotiated", "Cooperative"], 0,
          "A tender is put out to several companies who compete for the work."),
        Q("What is the main risk of an informal brief?",
          ["There is no record of what was agreed",
           "It takes too long to write", "It is legally binding",
           "It cannot include a deadline"], 0,
          "Verbal agreements are quick, but a dispute later has nothing to appeal to."),
        Q("What does sign off mean?",
          ["The client formally approving a stage of the work",
           "Finishing the project", "Signing the contract",
           "Sending the invoice"], 0,
          "After sign off, changes to that stage cost extra, which is the point of having it."),
        Q("A brief says the product must be under 2 MB. What kind of constraint is that?",
          ["Technical", "Legal", "Budget", "House style"], 0,
          "File size is a technical limit, and it affects compression and asset choices."),
        Q("What is scope creep?",
          ["Requirements growing after the brief was agreed",
           "Running out of budget", "Missing the deadline",
           "A brief with too much detail"], 0,
          "It is the main reason projects overrun, and a written brief is the defence against it."),
        Q("Why is 'aimed at everyone' a weak audience definition?",
          ["It gives no basis for any design decision",
           "It is too expensive to reach everyone",
           "Products can only have one audience",
           "It breaks advertising rules"], 0,
          "If the audience could be anyone, no font, tone or platform choice can be justified."),
        Q("Which is a deliverable rather than a requirement?",
          ["A logo supplied as SVG, PNG and single colour versions",
           "The product must look premium", "The audience is aged 25 to 40",
           "The deadline is 14 March"], 0,
          "A deliverable is the actual file handed over, in a stated format."),
        Q("A client's existing brand has set fonts and colours that must be used. What is this called?",
          ["House style", "A tender", "Scope creep", "An implicit requirement"], 0,
          "House style is the client's own rulebook, and it is a real constraint on design."),
        Q("When is the best time to negotiate an impossible deadline?",
          ["Before work starts", "After the first draft",
           "On the delivery date", "It should never be negotiated"], 0,
          "Raising it at the start is professional; raising it on the deadline is a failure."),
    ],
    exam=[
        EQ("State **two** pieces of information that should be included in a client brief.", 2,
           [MP("One valid element of a brief", ["purpose", "audience", "message", "content", "deliverables", "deadline", "budget", "constraints"]),
            MP("A second, different valid element", ["audience", "deadline", "budget", "content", "message", "format"])],
           "The target audience, and the deadline for delivery.",
           command="State"),
        EQ("Explain the difference between an explicit requirement and an implicit requirement.", 4,
           [MP("Explicit is defined as stated in the brief", ["stated", "written", "set out", "specified", "listed"]),
            MP("An example of an explicit requirement", ["deadline", "include the logo", "size", "format", "colour"]),
            MP("Implicit is defined as expected but not stated", ["not stated", "assumed", "expected", "unwritten", "taken for granted"]),
            MP("An example of an implicit requirement", ["spelling", "works on a phone", "legible", "accessible", "quality", "right to use"])],
           "An explicit requirement is one the client has stated in the brief, such as a deadline of 14 March or an instruction that the logo must work in a single colour. An implicit requirement is one the client has not written down but would still expect to be met, such as the text being correctly spelled or the website working properly on a phone. Both have to be satisfied, because a product that meets every explicit requirement but misspells the client's own name has still failed.",
           command="Explain"),
        EQ("A local bakery has asked a designer for a set of new packaging labels. The bakery has a small budget and needs the labels in three weeks.\n\nExplain **two** ways these constraints will affect the designer's decisions.", 4,
           [MP("The budget constraint is identified", ["budget", "cost", "money", "cheap"]),
            MP("A decision that follows from the budget", ["stock", "no photo shoot", "fewer colours", "one colour", "illustration", "typography", "existing assets"]),
            MP("The time constraint is identified", ["three weeks", "deadline", "time", "short"]),
            MP("A decision that follows from the time", ["fewer concepts", "earlier sign off", "simpler", "no revisions", "existing templates", "quick printing"])],
           "The small budget means a photo shoot is not realistic, so the designer will build the labels around typography and illustration, or a single licensed stock image, which keeps the cost to one licence rather than a day's shooting. The three week deadline means fewer concepts can be explored and sign off has to come early, because printing and die cutting need time at the end; the designer will therefore present two or three developed ideas rather than six rough ones, and will confirm the print specification with the printer before any artwork is finished.",
           command="Explain"),
        EQ("A charity is commissioning a short video to be shown on its website and on social media.\n\nDiscuss why a written client brief is important for this project, and what problems could arise without one.", 8,
           [MP("The brief records the purpose and message", ["purpose", "message", "what it is for", "aim"]),
            MP("The brief defines the audience", ["audience", "donors", "who it is for", "demographic"]),
            MP("The brief fixes deliverables including formats and sizes", ["format", "16:9", "9:16", "square", "aspect ratio", "resolution", "deliverables", "length"]),
            MP("Without it, assumptions are made and the wrong product is produced", ["assume", "guess", "misunderstanding", "wrong", "different idea"]),
            MP("Without it, there is no defence against scope creep", ["scope creep", "keeps adding", "more changes", "extra requests", "grows"]),
            MP("Without it, disputes about payment or ownership cannot be settled", ["dispute", "payment", "contract", "ownership", "no record", "evidence"]),
            MP("Legal requirements specific to a charity may be missed", ["charity number", "consent", "permission", "safeguarding", "advertising rules", "data protection"]),
            MP("A judgement about which risk matters most and why", ["most important", "greatest risk", "overall", "therefore"])],
           "A written brief matters here because the video has to do a specific job for a specific audience, and both of those have to be agreed before anything is filmed. It records the purpose and the single message the charity wants viewers to take away, which is what every editing decision will be judged against. It defines the audience, since a video aimed at existing donors is a different film from one aimed at recruiting new ones. It fixes the deliverables precisely: the website needs a 16:9 version, social media needs a square or vertical crop, and the two have to be framed differently at the shoot rather than cropped badly afterwards, so this cannot be decided at the end. It also captures the constraints that a charity in particular carries: consent from anyone appearing on camera, safeguarding if children are involved, and the charity number or regulated wording on any appeal for donations. Without a brief, the most likely outcome is simply the wrong product: the producer builds what they imagined and the charity sees something that does not match what they pictured, with no record to show who was right. Beyond that, there is no defence against scope creep, because each new request looks reasonable in isolation, and no evidence to resolve a dispute over payment or over who owns the footage afterwards. The greatest risk is the legal one, because a missing consent form can mean the finished video cannot be published at all, and unlike a disagreement about style, that cannot be fixed in the edit.",
           command="Discuss"),
    ],
)

M_AUDIENCE = Topic(
    slug="target-audience-and-segmentation",
    title="R093 TA2: Target Audience and Segmentation",
    spec="R093 TA2",
    icon="i-user",
    minutes=24,
    blurb="How audiences are described and divided up, and how each description changes the product. Expect to justify design choices against a named audience.",
    fact="Audience segmentation is why the same supermarket sells an identical bag of pasta under three different labels at three different prices. The pasta is the segment-blind part; the packaging is doing all the work.",
    sections=[
        Section("Describing an audience", """
Audiences are described in three ways, and strong answers use all three.

### Demographics: who they are

| Factor | Example |
| **Age** | 11 to 14, or 25 to 40, or over 65 |
| **Gender** | Where the product is genuinely gendered, such as a specialist magazine |
| **Income and occupation** | What they can afford and what they understand |
| **Education** | How technical the language can be |
| **Location** | Local, national, international; urban or rural |
| **Ethnicity, religion and culture** | Imagery, language and dates that will or will not land |
| **Family status** | Single, couple, parents of young children |

### Psychographics: how they think

Values, attitudes, interests, lifestyle and aspirations. Two 30 year olds on the same salary can want opposite things, and psychographics is what separates them. A brand that sells on sustainability is targeting an attitude, not an age.

### Behaviour: what they do

How often they buy, which platform they use, whether they watch with sound on, how long they stay. This is measurable, which is why it drives most real decisions online.

!key Segmentation :: Dividing a broad market into groups that behave similarly, so each group can be addressed properly. A product aimed at a segment beats a product aimed at everyone, because it can make choices.
"""),
        Section("How the audience changes the product", """
This is the part that carries the marks. For each audience factor, there is a decision.

| If the audience is | Then |
| **Younger** | Shorter, faster edits; vertical video; informal tone; platform native |
| **Older** | Larger type, higher contrast, no assumed app knowledge, clearer navigation |
| **Expert in the field** | Technical vocabulary without explanation; respect for accuracy |
| **New to the field** | Define terms, build up, avoid jargon, use analogy |
| **On mobile** | Thumb reach, one column, big tap targets, works on a slow connection |
| **In a noisy place** | Captions and on screen text, because the sound will be off |
| **International** | Avoid idiom, culture specific humour and date formats; allow for translation |

### Accessibility is part of the audience

Around one in five people in the UK has a disability. Designing for the audience includes contrast that can be read with low vision, captions for deaf viewers, alternative text for screen readers, and controls that work without a mouse. It is also a legal duty for service providers under the Equality Act 2010.

!grade Never justify with taste :: "I used a bold sans serif because it looks nice" scores nothing. "I used a bold sans serif at 18 point because the audience is over 65 and the leaflet will be read in a waiting room, often without reading glasses" scores every time, because the choice is traced to the audience.
"""),
        Section("Finding out who the audience is", """
You are not supposed to guess. The specification expects you to know where audience information comes from.

- **Client knowledge** — they usually know their customers better than anyone
- **Analytics** — real data on who visits, on what device, for how long
- **Surveys and questionnaires** — quick, cheap, large samples, but shallow
- **Interviews and focus groups** — slow, small, but reveal reasons
- **Observation and user testing** — what people do, rather than what they say they do
- **Competitor analysis** — who the similar products are clearly aimed at
- **Published market research** — industry reports, census data, Ofcom and ASA research

### Why what people say and what they do differ

Ask people how long they spend on social media and the average answer is well under the measured figure. That is not lying; it is memory. It is also why observation and analytics are trusted over self report when the two disagree.

!warn One is not a sample :: Asking your family is not research. Five people from the actual audience is worth more than fifty from outside it, and the exam will credit you for saying who you asked, not just that you asked.
"""),
    ],
    keyterms=[
        ("Target audience", "The specific group a media product is made for."),
        ("Demographics", "Measurable characteristics of an audience such as age, income, location and occupation."),
        ("Psychographics", "An audience's values, attitudes, interests and lifestyle."),
        ("Segmentation", "Dividing a market into groups that behave similarly so each can be addressed properly."),
        ("Analytics", "Measured data about how real users behave with a product."),
        ("Focus group", "A guided discussion with a small group from the audience, used to find out why they think something."),
        ("Accessibility", "Designing so that people with disabilities can use the product."),
    ],
    grade="""
Top answers name the audience **precisely** and then trace at least three decisions back to it. Vague audience, vague justification, low mark. "Men aged 18 to 24 who follow football on their phones during matches" lets you justify vertical video, captions, a fast cut and a 15 second length in one sentence each.
""",
    mistakes=[
        "Describing the audience only by age, when psychographics and behaviour carry just as many marks.",
        "Saying 'aimed at everyone', which makes every design decision unjustifiable.",
        "Justifying choices by personal taste rather than by the audience.",
        "Forgetting accessibility, which is part of designing for a real audience and a legal duty.",
        "Treating a survey of friends as audience research.",
    ],
    quiz=[
        Q("Which of these is a psychographic factor?",
          ["Caring strongly about sustainability", "Being aged 25 to 34",
           "Living in Manchester", "Earning £30,000 a year"], 0,
          "Psychographics are values, attitudes and lifestyle. The other three are demographics."),
        Q("A product is aimed at people over 70. Which design change follows?",
          ["Larger type and higher contrast", "Faster editing and trending audio",
           "Vertical video only", "More technical jargon"], 0,
          "Eyesight changes with age, so legibility becomes the dominant design factor."),
        Q("Why do social media videos need on screen captions?",
          ["Most are watched with the sound off", "Captions improve the colour",
           "It is required by the platform", "They make the file smaller"], 0,
          "A large majority of feed video is watched muted, so uncaptioned speech is lost."),
        Q("What does segmentation mean?",
          ["Dividing a market into groups that behave similarly",
           "Splitting a video into scenes", "Separating layers in a graphic",
           "Dividing a budget between tasks"], 0,
          "Each segment can then be addressed with choices that suit it."),
        Q("Which research method shows what users actually do rather than what they say?",
          ["Observation and analytics", "A questionnaire", "A focus group", "An interview"], 0,
          "Self report is unreliable about frequency and duration; measurement is not."),
        Q("An audience is described as 'experienced developers'. What follows for the language used?",
          ["Technical terms can be used without explanation",
           "Every term must be defined", "Avoid all technical words",
           "Use simple analogies throughout"], 0,
          "Over explaining to an expert audience reads as patronising and wastes their time."),
        Q("Which of these is a demographic factor?",
          ["Occupation", "Attitude to risk", "Brand loyalty", "Interest in cycling"], 0,
          "Occupation is measurable and factual. The others are psychographic or behavioural."),
        Q("Why is accessibility part of designing for an audience?",
          ["Around one in five people has a disability, and it is a legal duty",
           "It improves search rankings only", "It reduces file size",
           "It is optional good practice with no legal basis"], 0,
          "The Equality Act 2010 requires service providers to make reasonable adjustments."),
        Q("A client says their audience is 'everyone'. What should the designer do?",
          ["Work with the client to define a primary segment",
           "Design for the widest possible age range",
           "Accept it and design generically",
           "Pick an audience without telling the client"], 0,
          "Nothing can be justified against 'everyone', so the first job is narrowing it."),
        Q("Which method is best for finding out why an audience dislikes a design?",
          ["A focus group or interview", "Website analytics",
           "A multiple choice survey", "Competitor analysis"], 0,
          "Numbers tell you that something is wrong; talking to people tells you why."),
    ],
    exam=[
        EQ("Give **two** demographic factors used to describe a target audience.", 2,
           [MP("One valid demographic factor", ["age", "gender", "income", "occupation", "location", "education", "family", "ethnicity"]),
            MP("A second, different demographic factor", ["income", "location", "occupation", "age", "education", "gender"])],
           "Age, and household income.",
           command="Give"),
        EQ("Explain the difference between demographics and psychographics when describing an audience.", 4,
           [MP("Demographics defined as measurable factual characteristics", ["measurable", "factual", "who they are", "statistics", "age", "income"]),
            MP("An example of a demographic", ["age", "income", "location", "occupation"]),
            MP("Psychographics defined as values, attitudes and lifestyle", ["values", "attitudes", "lifestyle", "interests", "beliefs", "how they think"]),
            MP("An example of a psychographic, or why the distinction matters", ["sustainability", "status", "adventurous", "health conscious", "two people the same age", "different wants"])],
           "Demographics are the measurable facts about an audience: their age, income, occupation, education and where they live. Psychographics describe how that audience thinks: their values, attitudes, interests and lifestyle. The distinction matters because two people with identical demographics can want opposite things. Two 30 year olds on the same salary in the same city might be targeted completely differently if one buys on price and the other buys on sustainability, and only psychographics tells you which is which.",
           command="Explain"),
        EQ("A museum is producing an interactive touchscreen exhibit for visitors aged 60 and over.\n\nExplain **three** design decisions the audience should lead to, and why.", 6,
           [MP("A decision about text size or legibility", ["larger text", "font size", "legible", "bigger type", "18pt"]),
            MP("The reason linked to the audience", ["eyesight", "vision", "without glasses", "age related"]),
            MP("A decision about contrast or colour", ["contrast", "dark on light", "avoid low contrast", "colour"]),
            MP("The reason linked to the audience", ["harder to read", "vision", "glare", "lighting"]),
            MP("A decision about controls or navigation", ["large buttons", "simple navigation", "clear labels", "no gestures", "no swipe", "fewer steps"]),
            MP("The reason linked to the audience", ["dexterity", "not familiar with", "assumed knowledge", "confidence", "touchscreen experience"])],
           "The text should be set noticeably larger than usual, around 18 to 20 point for body copy, because age related changes to eyesight are near universal over 60 and many visitors will read the screen without their glasses. Colour contrast should be high, with dark text on a light background and no pale grey on white, because reduced contrast sensitivity makes low contrast text effectively invisible and museum lighting adds glare. The controls should be large, clearly labelled buttons with no swipe or pinch gestures, because gesture conventions are learned from phone use rather than being obvious, and a visitor who cannot work out how to move on simply walks away from the exhibit.",
           command="Explain"),
        EQ("A sportswear company is launching a campaign aimed at women aged 18 to 25 who run recreationally and post about it on social media.\n\nDiscuss how this audience should influence the style, platform and content of the campaign.", 8,
           [MP("The platform choice is linked to the audience's behaviour", ["social", "vertical", "9:16", "reels", "short form", "phone"]),
            MP("A decision about video or image length or pace", ["short", "seconds", "fast", "first three seconds", "hook"]),
            MP("Captions or sound off viewing is addressed", ["captions", "sound off", "muted", "on screen text"]),
            MP("A decision about tone of voice", ["informal", "conversational", "peer", "not corporate", "authentic"]),
            MP("A decision about imagery or casting", ["real runners", "relatable", "not models", "diverse", "body types", "user generated"]),
            MP("A psychographic or behavioural insight is used, not just age", ["values", "community", "achievement", "progress", "shares", "identity", "authenticity"]),
            MP("Accessibility or inclusivity is considered", ["captions", "contrast", "alt text", "inclusive", "representation"]),
            MP("A judgement weighing the factors", ["most important", "overall", "the key factor", "therefore"])],
           "The audience's behaviour decides the platform first: this group watches short form video on a phone, so the campaign should be built vertically at 9:16 for feeds and stories rather than cropped down from a 16:9 master, and each piece needs to work in under fifteen seconds with the point made in the first three, because that is when the thumb decides. Almost all of that viewing happens with the sound off, so every spoken line needs burned in captions and the key message has to be carried by on screen text and image rather than by voiceover. The tone should be conversational and peer to peer rather than corporate, because this audience is unusually alert to advertising that pretends to be authentic, and a brand voice that sounds like a press release is dismissed instantly. Casting and imagery follow the same logic: real recreational runners of varying body types and paces, shot on routes that look like ordinary streets and parks, are more persuasive than studio shots of athletes, because the audience is buying an identity it can see itself in. The psychographic insight underneath all of this is that running is being used to mark progress and to belong to a community, which is why the campaign should centre on shared achievement and give people something they would willingly post themselves, rather than centring on the product's features. Captions and strong contrast also make the campaign usable by deaf and partially sighted members of the same audience, which costs nothing and widens the reach. Of all these factors the behavioural one is the most decisive, because getting the format and the first three seconds wrong means the rest of the work is never seen at all.",
           command="Discuss"),
    ],
)

M_RESEARCH = Topic(
    slug="research-methods-and-sources",
    title="R093 TA2: Research Methods and Sources",
    spec="R093 TA2",
    icon="i-search",
    minutes=22,
    blurb="Primary and secondary research, quantitative and qualitative data, and how to tell whether a source can be trusted.",
    fact="A survey question can decide its own answer. 'Should the council waste money on a new website?' and 'Should the council invest in a new website?' describe the same thing and produce opposite results, which is why examiners ask about bias.",
    sections=[
        Section("Primary and secondary research", """
Two words, and the paper expects you to use them correctly.

| | Primary research | Secondary research |
| **Meaning** | You collect it yourself, for this project | Somebody else collected it, for their own reasons |
| **Examples** | Surveys, interviews, focus groups, observation, user testing, your own test shoots | Books, industry reports, census data, articles, competitor products, analytics you did not set up |
| **Advantages** | Exactly the question you need; current; you control the quality | Fast, cheap or free, often large scale and professionally conducted |
| **Drawbacks** | Slow, costs money, small samples, easy to do badly | May be out of date, about a different audience, or biased towards whoever paid for it |

### Use both

Real projects start with secondary research, because it is free and it shows what is already known, then use primary research to answer the questions the secondary research left open. An answer that recommends only one is weaker than one that explains the order.

!key Primary is about who collected it, not what it is :: A questionnaire is primary if you wrote and ran it. The same questionnaire's published results, read by somebody else a year later, are secondary research to them.
"""),
        Section("Quantitative and qualitative data", """
| | Quantitative | Qualitative |
| **What it is** | Numbers and counts | Words, opinions and reasons |
| **Collected by** | Closed questions, analytics, counts, ratings | Open questions, interviews, focus groups, observation |
| **Answers** | How many, how often, how long | Why, how it felt, what they expected |
| **Strength** | Comparable, measurable, can show a trend | Explains the numbers; finds problems nobody thought to ask about |
| **Weakness** | Says nothing about why | Hard to compare; small samples; interpretation can be subjective |

### They are a pair, not a choice

Analytics show that 70% of users leave the booking page. That is quantitative, and it is useless on its own. Watching six people try to book reveals that the date picker does not work with a thumb. That is qualitative, and it is the reason. You need the number to know where to look and the words to know what to fix.

### Sampling

- **Sample size** — small samples swing wildly; a survey of ten people proves almost nothing
- **Representative** — the sample has to resemble the audience; the wrong fifty people are worse than the right five
- **Random** — choosing who to ask by convenience builds in bias before the first question
"""),
        Section("Judging a source", """
Secondary research is only as good as its source, and the specification expects you to be able to assess one.

| Test | Question to ask |
| **Authority** | Who wrote it, and what do they know? |
| **Currency** | How old is it? Platform statistics age in months |
| **Purpose** | Why was it published? Who paid for it? |
| **Evidence** | Does it say where its numbers came from? |
| **Corroboration** | Does an independent source agree? |
| **Bias** | Does the publisher gain if you believe it? |

### Where bias comes from

- **Funded research** — a study paid for by an industry rarely harms that industry
- **Leading questions** — the wording suggests the answer
- **Self selection** — only people who already care fill in the survey
- **Cherry picking** — quoting the one favourable figure from a mixed report

!warn Reliable is not the same as relevant :: Ofcom data is extremely reliable, and still tells you nothing if it is about a different age group in a different year. Say why a source fits your audience, not just that it is trustworthy.
"""),
    ],
    keyterms=[
        ("Primary research", "Data you collect yourself for this project."),
        ("Secondary research", "Data collected by somebody else for their own purposes."),
        ("Quantitative data", "Numerical data: counts, measurements and ratings."),
        ("Qualitative data", "Non numerical data: opinions, reasons and descriptions."),
        ("Representative sample", "A group whose makeup resembles the audience being studied."),
        ("Bias", "A systematic distortion that pushes results in one direction."),
        ("Leading question", "A question worded so that it suggests its own answer."),
    ],
    grade="""
The mark is in the **justification of the method**. Not "I did a survey" but "I surveyed 40 Year 10 students because the product is for that age group, used closed questions so the results could be compared, and then interviewed four of them to find out why the least popular design was disliked."
""",
    mistakes=[
        "Mixing up primary and secondary. It depends on who collected it, not on the type of data.",
        "Treating quantitative and qualitative as a choice when strong projects use both.",
        "Quoting a source without checking its date, especially for platform and audience statistics.",
        "Using a sample that is convenient rather than representative.",
        "Writing survey questions that lead the respondent to an answer.",
    ],
    quiz=[
        Q("You interview six people from the target audience yourself. What kind of research is that?",
          ["Primary", "Secondary", "Quantitative", "Tertiary"], 0,
          "You collected it yourself for this project, so it is primary. It is also qualitative."),
        Q("Reading a published Ofcom report on media use is which kind of research?",
          ["Secondary", "Primary", "Qualitative only", "Observation"], 0,
          "Somebody else collected it for their own purposes, so to you it is secondary."),
        Q("Which data type answers 'why did users abandon the page?'",
          ["Qualitative", "Quantitative", "Demographic", "Numerical"], 0,
          "Reasons are qualitative. The number who abandoned is quantitative."),
        Q("What is the main drawback of primary research?",
          ["It takes time and money and samples are often small",
           "It is always biased", "It cannot produce numbers",
           "It is out of date"], 0,
          "Collecting it yourself is slow and expensive, which is why samples stay small."),
        Q("Which of these is a leading question?",
          ["Don't you agree the old logo looks dated?",
           "How would you describe the old logo?",
           "Which logo do you prefer, A or B?",
           "How often do you see the logo?"], 0,
          "It tells the respondent the expected answer before they reply."),
        Q("A survey is answered only by people who follow the brand already. What problem is that?",
          ["Self selection bias", "A leading question",
           "Too small a sample", "Out of date data"], 0,
          "The people who care most answer, so the results look far more positive than reality."),
        Q("Why should you check the date of a secondary source about social media use?",
          ["Platform usage changes within months",
           "Old sources are always wrong", "Dates affect copyright",
           "Older research uses smaller samples"], 0,
          "A three year old figure about which platform teenagers use is likely to be wrong now."),
        Q("Which is the strongest sample for testing a product aimed at Year 8 students?",
          ["Twenty Year 8 students from two different schools",
           "Fifty adults", "Your five closest friends",
           "Two hundred people of any age online"], 0,
          "It must resemble the audience. Size matters less than being the right people."),
        Q("Analytics show a 70% drop off on one page. What should you do next?",
          ["Watch real users attempt that page to find out why",
           "Redesign the page immediately", "Survey the whole audience",
           "Ignore it as a single figure"], 0,
          "The number locates the problem; qualitative research explains it."),
        Q("A study showing a product is safe was funded by the company selling it. What should you note?",
          ["The funder has an interest in the result, so corroborate it",
           "The study must be false", "Funded studies cannot be cited",
           "It is primary research"], 0,
          "Funding does not make research wrong, but it does mean you look for independent agreement."),
    ],
    exam=[
        EQ("Identify **one** primary and **one** secondary research method.", 2,
           [MP("A genuine primary method", ["survey", "questionnaire", "interview", "focus group", "observation", "user testing"]),
            MP("A genuine secondary method", ["report", "article", "census", "book", "competitor", "published", "existing data", "website"])],
           "A primary method is running a questionnaire with the target audience. A secondary method is reading a published industry report.",
           command="Identify"),
        EQ("Describe **two** advantages of using primary research when designing a product for a specific audience.", 4,
           [MP("It answers exactly the question needed", ["specific", "exactly", "tailored", "the question you need", "relevant"]),
            MP("Development of that point", ["because", "whereas secondary", "designed for this project"]),
            MP("It is current, or its quality is controlled", ["up to date", "current", "recent", "control", "know how it was collected", "reliable"]),
            MP("Development of that point", ["because", "means", "so you can trust"])],
           "The first advantage is relevance: the questions are written for this project, so the answers address exactly the decision being made, whereas a published report will have been written to answer somebody else's question about a slightly different audience. The second is currency and control: the data is collected now, and because you designed the method you know the sample size, who was asked and how, so you can judge how much weight the results deserve rather than having to trust a source you cannot check.",
           command="Describe"),
        EQ("A design agency has found an online article claiming that 90% of teenagers prefer a particular social media platform.\n\nExplain **two** checks the agency should make before relying on this figure.", 4,
           [MP("Check the date or currency", ["date", "how old", "current", "out of date", "when"]),
            MP("Why that matters", ["changes quickly", "platforms change", "no longer true", "months"]),
            MP("Check the source, author or funding", ["who wrote", "author", "who paid", "funded", "authority", "publisher"]),
            MP("Why that matters, or that it should be corroborated", ["bias", "interest", "benefit", "corroborate", "second source", "independent"])],
           "The agency should first check when the figure was published, because platform preference among teenagers changes within months and a figure from three years ago may now be the wrong platform entirely. It should also check who produced the research and who paid for it, because a study published by a platform about its own popularity has an obvious interest in the result; the figure should be corroborated against an independent source such as Ofcom before any decision is based on it.",
           command="Explain"),
        EQ("A company's booking website is losing customers partway through the booking process.\n\nDiscuss how the company could use both quantitative and qualitative research to find and fix the problem.", 8,
           [MP("Quantitative data is used to locate the problem", ["analytics", "drop off", "percentage", "how many", "measure", "funnel"]),
            MP("A specific quantitative measure is named", ["bounce", "completion rate", "time on page", "clicks", "device", "abandonment"]),
            MP("The limitation of quantitative data is recognised", ["does not say why", "no reason", "only shows", "cannot explain"]),
            MP("Qualitative research is used to find the reason", ["interview", "observation", "user testing", "focus group", "watch", "open questions"]),
            MP("A specific qualitative method is described in context", ["watch five users", "ask them to book", "record where they hesitate", "think aloud"]),
            MP("The findings are turned into a change", ["redesign", "fix", "change the", "simplify", "larger", "fewer steps"]),
            MP("Re-testing or measuring after the change", ["test again", "re-measure", "compare", "A/B", "monitor"]),
            MP("A judgement about how the two methods relate", ["both needed", "together", "neither alone", "most useful"])],
           "The company should start with the quantitative data it already has, because analytics will show exactly where customers are being lost: the completion rate for each step of the booking funnel, the percentage abandoning on each page, the time spent before leaving and the device being used. That identifies the problem precisely, for instance that 70% of abandonment happens on the date selection step and that nearly all of it is on mobile. What the numbers cannot do is explain the cause, since a drop off figure is identical whether the page is confusing, slow or broken. The qualitative stage answers that: recruit five or six people from the real audience, ask them to make a booking on their own phones while talking through what they are doing, and record every point at which they hesitate, backtrack or guess. That typically produces a single concrete finding, such as the date picker requiring a tap on a target too small for a thumb, which no amount of analytics would have revealed. The change is then made on the basis of that finding, and the quantitative measurement is repeated afterwards to confirm the completion rate actually improved rather than assuming it did. Neither method is sufficient alone: the numbers say where to look and how much the problem is worth, and the observation says what to change, so the sensible order is quantitative first to locate, qualitative second to diagnose, quantitative again to verify.",
           command="Discuss"),
    ],
)

M_STYLE = Topic(
    slug="style-content-and-layout",
    title="R093 TA2: Style, Content, Layout and Media Codes",
    spec="R093 TA2",
    icon="i-palette",
    minutes=26,
    blurb="How the look of a product communicates before a word is read: colour, typography, layout conventions and the codes an audience already understands.",
    fact="Readers decide whether a page is for them in well under a second, before any text has been processed. That judgement is made entirely on colour, type and layout, which is why those three are treated as content rather than decoration.",
    sections=[
        Section("Style: colour and typography", """
### Colour

| Colour | Commonly associated with |
| **Red** | Urgency, passion, danger, appetite, sale |
| **Blue** | Trust, calm, stability, technology, finance |
| **Green** | Nature, health, sustainability, growth, permission |
| **Yellow** | Optimism, warning, attention, value |
| **Purple** | Luxury, creativity, imagination |
| **Black** | Premium, authority, formality |
| **White** | Simplicity, cleanliness, space, clinical |

These associations are **cultural, not universal**. White signifies mourning in parts of East Asia; red is lucky in China and a warning in the UK. An international product cannot assume a UK reading.

- **Colour palette** — a primary colour, one or two secondaries, and a neutral range
- **Contrast** — essential for legibility, not a style choice; the WCAG minimum is 4.5:1 for body text
- **Colour blindness** — around 8% of men; never use colour alone to carry meaning

### Typography

| Term | Meaning |
| **Serif** | Small strokes on the letter ends. Traditional, authoritative, used for long print text |
| **Sans serif** | No strokes. Clean, modern, the default on screen |
| **Slab serif** | Heavy rectangular serifs. Bold, confident, used for impact |
| **Script** | Handwriting style. Personal or luxury, poor legibility in quantity |
| **Display** | Designed for headlines only, never for body text |
| **Monospace** | Every character the same width. Code, data, technical |
| **Point size** | The size of the type |
| **Leading** | The space between lines. Too tight is the most common legibility error |
| **Kerning** | The space between two specific letters |
| **Tracking** | Letter spacing applied across a whole run of text |

!key Two typefaces is a system; five is a mess :: One for headings, one for body, used consistently at a few defined sizes. That is what makes a product look designed rather than assembled.
"""),
        Section("Layout and composition", """
Layout is how the eye is directed. These conventions are what the exam means by layout.

- **Grid** — columns and gutters that every element aligns to. The single biggest difference between amateur and professional layout
- **Rule of thirds** — a 3 by 3 grid; placing the subject on an intersection is more dynamic than centring it
- **Lead room and headroom** — space in front of a moving or looking subject, and above their head
- **Visual hierarchy** — size, weight, colour and position establishing what is read first, second and third
- **White space** — deliberate emptiness; it creates focus and makes a product read as premium
- **Alignment** — things that relate line up; things that line up look related
- **Proximity** — elements near each other are read as belonging together
- **Repetition** — repeated styling ties a multi-page product into one thing
- **Z pattern and F pattern** — how eyes scan a poster and a web page respectively
- **Focal point** — the one element the composition is built around

### Layout conventions by product

| Product | Convention the audience expects |
| **Magazine cover** | Masthead at the top, cover star, cover lines down one side, barcode and price |
| **Newspaper front** | Masthead, headline, lead image, columns, standfirst |
| **Web page** | Logo top left, navigation across the top, footer with legal links |
| **Poster** | One dominant image, a short headline, the essential information at the bottom |
| **App screen** | Navigation at the bottom within thumb reach, one task per screen |

Conventions can be broken, but only deliberately and for an effect. Broken by accident, they read as a mistake.
"""),
        Section("Media codes and conventions", """
**Media codes** are the signs a product uses to communicate meaning, and the audience reads them without being taught.

| Code type | What it covers |
| **Technical codes** | Camera angle, shot size, movement, lighting, editing pace, sound |
| **Symbolic codes** | Colour, objects, setting, costume, body language, typography |
| **Written codes** | Language, tone, headlines, captions, slogans, font choice |

### Technical codes, specifically

| Choice | What it conveys |
| **Low angle** | Power, dominance, threat |
| **High angle** | Vulnerability, smallness |
| **Eye level** | Neutrality, equality |
| **Close up** | Emotion, detail, intimacy |
| **Wide shot** | Context, isolation, scale |
| **Fast cutting** | Energy, urgency, excitement |
| **Slow dissolve** | Time passing, memory, calm |
| **Low key lighting** | Mystery, threat, drama |
| **High key lighting** | Openness, safety, cheerfulness |

### Genre conventions

Audiences bring expectations. A horror poster in bright yellow with a rounded playful font fails, not because the design is poor, but because it contradicts the codes the audience uses to work out what the product is. Questions about genre are asking whether you know that the audience, not the designer, decides what a convention means.

!grade Name the code and the effect :: "A low angle shot was used" is description. "A low angle shot was used so the figure fills the frame and looks down at the viewer, which makes them appear threatening before any dialogue" is analysis, and analysis is what the extended questions reward.
"""),
    ],
    keyterms=[
        ("House style", "A consistent set of fonts, colours and layout rules used across a product or brand."),
        ("Visual hierarchy", "The arrangement of elements so the eye reads them in the intended order."),
        ("White space", "Deliberate empty space used to create focus and separation."),
        ("Rule of thirds", "Placing key elements on the lines of a 3 by 3 grid rather than centring them."),
        ("Media code", "A sign a media product uses to communicate meaning to its audience."),
        ("Technical code", "Meaning created by camera, lighting, editing and sound choices."),
        ("Symbolic code", "Meaning created by colour, objects, setting, costume and typography."),
        ("Convention", "An established way of doing something that the audience expects."),
        ("Leading", "The vertical space between lines of text."),
    ],
    grade="""
Every design observation needs an **effect on the audience** attached. The structure that scores is: this choice, so this effect, which suits this audience and purpose. Three of those sentences will outscore a page of description every time.
""",
    mistakes=[
        "Describing a design without saying what effect it has on the audience.",
        "Treating colour associations as universal when they are cultural.",
        "Using colour alone to carry meaning, which fails for colour blind users.",
        "Confusing technical codes (camera, lighting, editing) with symbolic codes (colour, costume, setting).",
        "Setting body text in a display or script typeface.",
        "Calling a convention a rule. Conventions can be broken for effect; the exam wants you to know why.",
    ],
    quiz=[
        Q("A low angle shot of a character usually makes them appear:",
          ["Powerful or threatening", "Vulnerable", "Neutral", "Distant"], 0,
          "The viewer looks up at them, which reads as dominance."),
        Q("Which is a symbolic code rather than a technical code?",
          ["The colour of a character's costume", "The camera angle",
           "The editing pace", "The lighting setup"], 0,
          "Costume, colour, setting and objects are symbolic. Camera, lighting and editing are technical."),
        Q("What is leading?",
          ["The vertical space between lines of text", "The space between two letters",
           "The size of the type", "The width of a column"], 0,
          "Too little leading is the most common cause of hard to read body text."),
        Q("Why should colour never be the only thing carrying a meaning?",
          ["Around 8% of men are colour blind",
           "Colours print differently", "Screens vary in brightness",
           "It increases file size"], 0,
          "Red and green used alone to mean wrong and right are indistinguishable to many users."),
        Q("Which typeface class is designed for headlines only?",
          ["Display", "Sans serif", "Serif", "Monospace"], 0,
          "Display faces are drawn for impact at large sizes and become unreadable as body text."),
        Q("What does the rule of thirds suggest?",
          ["Place key elements on the lines of a 3 by 3 grid",
           "Use three colours maximum", "Divide a page into three columns",
           "Use three typefaces"], 0,
          "Off centre placement on a third is more dynamic than centring the subject."),
        Q("A horror film poster uses bright yellow and a rounded playful font. What is the problem?",
          ["It contradicts the genre conventions the audience reads",
           "Yellow is hard to print", "Rounded fonts are illegible",
           "Horror posters must be black"], 0,
          "The audience uses conventions to identify the genre, so breaking them accidentally misleads."),
        Q("What is visual hierarchy?",
          ["Arranging elements so the eye reads them in the intended order",
           "The order of layers in a file", "A ranking of design software",
           "The chain of command on a shoot"], 0,
          "Size, weight, colour and position decide what is noticed first."),
        Q("Why does white space make a design look more premium?",
          ["It creates focus and signals that space is not being sold",
           "It reduces printing costs", "It loads faster",
           "It is required by brand guidelines"], 0,
          "Crowded layouts read as cheap because value brands fill every gap with offers."),
        Q("Fast cutting in an edit most commonly conveys:",
          ["Energy and urgency", "Calm reflection", "Time passing", "Isolation"], 0,
          "Short shot lengths raise the pace, which the audience reads as excitement or tension."),
    ],
    exam=[
        EQ("Give **two** technical codes used in moving image products.", 2,
           [MP("One genuine technical code", ["camera angle", "shot size", "lighting", "editing", "sound", "camera movement", "close up"]),
            MP("A second, different technical code", ["lighting", "editing", "sound", "angle", "movement"])],
           "Camera angle, and lighting.",
           command="Give"),
        EQ("Explain how **two** symbolic codes could be used to show that a character is wealthy.", 4,
           [MP("One symbolic code is identified", ["costume", "clothing", "setting", "props", "objects", "colour", "location"]),
            MP("How it conveys wealth", ["tailored", "expensive", "designer", "quality", "gold", "marble", "large house"]),
            MP("A second, different symbolic code", ["setting", "props", "colour", "body language", "costume"]),
            MP("How the second conveys wealth", ["relaxed", "confident", "deep colours", "clean", "uncluttered", "staff", "car"])],
           "Costume is one: a precisely tailored suit in a dark, heavy fabric with no visible branding reads as wealth, because expensive clothing signals it through fit and quality rather than through logos. Setting is another: an uncluttered room with high ceilings, hard materials and very little furniture signals that space itself is being used as a luxury, which is a stronger indicator of wealth than filling the frame with possessions.",
           command="Explain"),
        EQ("A publisher is designing the cover of a new magazine for teenage gamers.\n\nExplain **three** style or layout decisions the publisher should make, and the effect each would have on the audience.", 6,
           [MP("A colour decision", ["colour", "palette", "bright", "neon", "dark", "contrast"]),
            MP("Its effect on the audience", ["stands out", "energy", "associates", "recognise", "appeals"]),
            MP("A typography decision", ["font", "typeface", "bold", "sans serif", "display", "masthead"]),
            MP("Its effect on the audience", ["impact", "legible", "modern", "matches", "reads as"]),
            MP("A layout decision", ["masthead", "cover lines", "rule of thirds", "hierarchy", "dominant image", "grid"]),
            MP("Its effect on the audience", ["read first", "draws the eye", "finds", "shelf", "recognisable", "order"])],
           "The palette should be high contrast with one strong accent colour, such as a saturated cyan or magenta against near black, because the cover has to compete on a shelf or in a thumbnail and because that combination is strongly associated with gaming interfaces, so the audience recognises the magazine's subject before reading a word. The masthead should be a heavy sans serif or slab serif set large across the top, because weight gives impact at thumbnail size and the simple letterforms stay legible where a script face would break up, which also makes the title recognisable issue after issue. The layout should give a single dominant character or game image placed on a rule of thirds intersection, with cover lines stacked down one side in a clear size hierarchy, because that directs the eye to the image first, then the biggest cover line, then the rest, so the reader learns what the issue is about in the order the publisher intends rather than scanning randomly.",
           command="Explain"),
        EQ("A charity is producing a poster to raise awareness of loneliness among older people.\n\nDiscuss how media codes, colour and layout could be used to communicate the message effectively to the public.", 8,
           [MP("A technical or photographic code is identified", ["wide shot", "close up", "angle", "lighting", "framing", "focus"]),
            MP("Its effect on the audience is explained", ["isolated", "small", "empathy", "vulnerable", "draws", "feel"]),
            MP("A colour decision with its effect", ["muted", "cold", "desaturated", "blue", "grey", "single warm", "contrast"]),
            MP("A typography decision with its effect", ["serif", "sans serif", "large", "simple", "legible", "quiet", "weight"]),
            MP("A layout decision with its effect", ["white space", "rule of thirds", "off centre", "hierarchy", "dominant image", "space around"]),
            MP("The audience's accessibility needs are addressed", ["contrast", "large text", "legible", "read at distance", "older readers"]),
            MP("A call to action or essential information is placed", ["call to action", "website", "phone number", "charity number", "bottom"]),
            MP("A judgement about which choice carries the message", ["most important", "the key", "overall", "above all"])],
           "The strongest code available here is framing. A wide shot of one person in a large, empty room, placed small and off centre on a rule of thirds intersection, makes the emptiness around them do the work: the viewer reads the space as isolation without the poster having to state it. Keeping the figure in soft focus or turned slightly away avoids making the image feel staged while still inviting empathy. The palette should be largely desaturated and cool, greys and blues, with one small area of warmth such as a lamp or a mug, because the contrast between the cold field and the single warm point suggests that something small could change the situation, which is exactly the charity's message. Typography should be quiet and confident rather than loud: a clean sans serif, set large, with plenty of leading, because shouting at the viewer about loneliness undercuts the tone, while poor legibility loses the message entirely. Layout should use generous white space, with the headline given a clear first place in the hierarchy and the call to action, the website and the registered charity number, grouped at the bottom where convention tells the viewer to look for it. Because the poster will often be seen by older readers in public spaces, text contrast must be well above the minimum and the smallest text still readable at two metres, which rules out thin weights and pale grey on white. Above all it is the use of space that carries the message, because a crowded poster about loneliness contradicts itself, and the viewer will feel that contradiction long before they analyse it.",
           command="Discuss"),
    ],
)

# =============================================================== R093 TA3

M_DOCS = Topic(
    slug="pre-production-documents",
    title="R093 TA3: Pre-production Documents",
    spec="R093 TA3",
    icon="i-pen",
    minutes=28,
    blurb="Which document goes with which product, what has to be on it, and why planning on paper is cheaper than planning in the software. The most heavily examined topic in R093.",
    fact="Pixar storyboards an entire film and cuts it together as a rough reel with temporary voices before a single frame is animated. Fixing a story problem on a drawing costs an afternoon; fixing it in finished animation costs months.",
    sections=[
        Section("Documents for generating ideas", """
These come first, while the idea is still forming.

| Document | What it is | What it is for |
| **Mood board** | A collage of colours, images, fonts and textures, annotated | Agreeing a look and feel with the client before design starts |
| **Mind map** | A branching diagram from a central idea | Exploring possibilities widely without committing |
| **Spider diagram** | A simpler mind map with one level of branches | Quick listing of related ideas |
| **Client brief interpretation** | Your written reading of what the brief actually requires | Making assumptions visible so they can be corrected early |

### Why a mood board earns its place

"Modern" means something different to every person who says it. A client who pictures Scandinavian minimalism and a designer who pictures neon cyberpunk can both say "modern" and agree enthusiastically. The mood board exposes that disagreement in an afternoon, instead of after two weeks of finished artwork.

!key Annotate everything :: An unannotated mood board is a scrapbook. Writing why each element is there is what makes it a planning document, and it is where the marks are.
"""),
        Section("Documents for designing and planning", """
This table is the single most useful thing in R093. Learn which document belongs to which product type.

| Document | Used for | Must show |
| **Visualisation diagram** | Static graphics: posters, covers, packaging, logos | Dimensions, layout, exact colours, named fonts, image positions, annotations |
| **Storyboard** | Moving image: film, video, animation, adverts | One frame per shot, shot type, camera movement, duration, dialogue, sound, transitions |
| **Script** | Anything with speech | Scene headings, action, character names, dialogue, and for AV a two column audio and visual layout |
| **Wireframe** | One screen of an interactive product | Placement of every element, with no styling or colour |
| **Navigation diagram** | The structure of an interactive product | Every screen as a box, every link as an arrow |
| **Asset list or table** | Every product | Every asset, its source, format, dimensions and licence |
| **Work plan** | Every product | Tasks, durations, order, dependencies, milestones, contingency |

### Visualisation diagrams in detail

A visualisation diagram is not a sketch. Another designer should be able to produce the graphic from it without asking a question. That means:

- **Canvas size and orientation**, in millimetres or pixels
- **Colours as values**, `#02848B` or `C100 M30 Y25 K10`, never "teal"
- **Fonts by name and size**, "Poppins SemiBold 42pt", never "a bold font"
- **Every element positioned**, with annotations explaining the intention
- **Bleed and safe margins** if it is going to print

### Storyboards in detail

One frame per shot, in order, each annotated with:

- **Shot type** — wide, mid, close up, extreme close up, over the shoulder
- **Camera angle** — high, low, eye level, Dutch
- **Camera movement** — pan, tilt, track, dolly, zoom, static
- **Duration** in seconds
- **Dialogue or voiceover** for that shot
- **Sound** — music, effects, ambience
- **Transition** into the next shot — cut, fade, dissolve, wipe

!warn The error that costs the most marks :: A storyboard for a poster, or a visualisation diagram for a video. Static product means visualisation diagram. Moving image means storyboard. Interactive means wireframe plus navigation diagram. Get this wrong and a whole question goes.
"""),
        Section("Wireframes, navigation diagrams and asset tables", """
### Wireframes

A wireframe shows **where things go**, deliberately without colour, fonts or images. Boxes with crosses stand in for images, grey bars for text. The point of leaving the styling out is that it keeps the conversation about structure. Wireframe **every distinct screen**, not just the home page.

### Navigation diagrams

Every screen is a box; every link is an arrow. Then check the four things that matter:

1. Can every screen be **reached** from the home screen?
2. Does every screen have a route **back**?
3. Are there any **dead ends**?
4. Is anything buried too **deep**, needing five or six clicks?

Three structures are worth knowing:

| Structure | Shape | Suits |
| **Linear** | One screen after another | A tutorial, a quiz, a story |
| **Hierarchical** | A home screen with sections and sub-sections | Most websites |
| **Hub and spoke** | A central screen with branches that return to it | Apps, kiosks, menus |

### Asset tables

One row per asset, and these columns:

| Asset | Type | Source | Format | Dimensions | Licence |
| hero-image | Image | Own photograph | JPG | 3000 x 2000 | Own work |
| logo-main | Vector | Client supplied | SVG | scalable | Client owned |
| backing-track | Audio | Free Music Archive | MP3 | 2:14 | CC BY 4.0, credit required |

The **licence column** is the one that matters. It is the evidence that nothing in the product infringes copyright, and an incomplete one can invalidate the whole piece of work.
"""),
    ],
    keyterms=[
        ("Mood board", "An annotated collage of colours, images and type that establishes the intended look and feel."),
        ("Visualisation diagram", "An annotated plan of a static graphic, detailed enough to work from."),
        ("Storyboard", "A frame by frame plan of a moving image product with shot, movement, duration and sound."),
        ("Wireframe", "A layout plan of one screen showing placement without any styling."),
        ("Navigation diagram", "A diagram of every screen in an interactive product and the links between them."),
        ("Asset table", "A record of every asset with its source, format, dimensions and licence."),
        ("Dead end", "A screen from which the user cannot continue or return."),
        ("Hierarchical structure", "A navigation structure with a home screen, sections and sub-sections."),
    ],
    grade="""
Two things separate the top band. First, **matching the document to the product** without hesitation. Second, explaining a document's purpose in terms of **what it prevents**: a storyboard prevents arriving on a shoot without knowing the shot list; an asset table prevents discovering at the end that an image cannot be used. Purpose expressed as risk avoided always outscores purpose expressed as "to plan it".
""",
    mistakes=[
        "Using a storyboard for a static product or a visualisation diagram for a video.",
        "Writing 'blue' and 'a bold font' on a visualisation diagram instead of exact values and font names.",
        "Wireframing only the home screen.",
        "Drawing a navigation diagram with dead ends or unreachable screens.",
        "Leaving the licence column of the asset table blank.",
        "Producing a mood board with no annotations, which makes it decoration rather than planning.",
    ],
    quiz=[
        Q("Which document would you produce to plan a magazine cover?",
          ["A visualisation diagram", "A storyboard", "A navigation diagram", "A wireframe"], 0,
          "A magazine cover is a static graphic, so it needs a visualisation diagram."),
        Q("Which document plans the shots of a 30 second advert?",
          ["A storyboard", "A visualisation diagram", "A mood board", "An asset table"], 0,
          "Moving image is planned shot by shot on a storyboard."),
        Q("What should a wireframe deliberately leave out?",
          ["Colour, fonts and final images", "The position of elements",
           "The navigation buttons", "The page headings"], 0,
          "Leaving styling out keeps the discussion about structure."),
        Q("What is a dead end in a navigation diagram?",
          ["A screen with no way to continue or return",
           "A screen with no content", "A broken link",
           "The last screen of a linear sequence"], 0,
          "Every screen needs a route onward or back, or the user gets stuck."),
        Q("Which column of an asset table is the evidence that the work is legal?",
          ["Licence", "Format", "Dimensions", "Source file name"], 0,
          "It records the right to use each asset, which is what copyright compliance rests on."),
        Q("How should a colour be recorded on a visualisation diagram?",
          ["As an exact value such as #02848B", "As 'teal'",
           "As 'the client's blue'", "Colour is not recorded"], 0,
          "Another designer must be able to reproduce it exactly, which a colour name cannot guarantee."),
        Q("Which navigation structure suits an online tutorial that must be done in order?",
          ["Linear", "Hierarchical", "Hub and spoke", "Mesh"], 0,
          "One screen follows another, which is what linear means."),
        Q("Why is a mood board produced before any design work?",
          ["To agree the look and feel with the client while changes are still cheap",
           "To list the assets needed", "To decide the deadline",
           "To show the final design"], 0,
          "Disagreements about style are much cheaper to resolve on a mood board."),
        Q("What must a storyboard frame include besides the drawing?",
          ["Shot type, camera movement, duration and sound",
           "Only the dialogue", "The file format",
           "The colour palette"], 0,
          "The annotations are what make it usable by a crew."),
        Q("Which documents together plan an interactive product's structure and screens?",
          ["Navigation diagram and wireframes", "Storyboard and script",
           "Visualisation diagram and mood board", "Asset table and work plan"], 0,
          "The navigation diagram gives the structure; wireframes give each screen."),
    ],
    exam=[
        EQ("State the pre-production document used to plan each of the following:\n\n(a) a cinema poster\n(b) a two minute animation\n(c) the structure of a website", 3,
           [MP("(a) visualisation diagram", ["visualisation", "visualization", "visual diagram"]),
            MP("(b) storyboard", ["storyboard"]),
            MP("(c) navigation diagram, or site map", ["navigation diagram", "site map", "sitemap", "structure diagram"])],
           "(a) A visualisation diagram. (b) A storyboard. (c) A navigation diagram.",
           command="State"),
        EQ("Identify **four** pieces of information that must appear on a visualisation diagram.", 4,
           [MP("Dimensions or canvas size", ["dimensions", "size", "canvas", "orientation", "mm", "pixels"]),
            MP("Exact colours", ["colour value", "hex", "CMYK", "#", "exact colours"]),
            MP("Named fonts, with sizes", ["font", "typeface", "named", "point size"]),
            MP("Position of each element, or annotations explaining choices", ["position", "placement", "layout", "where", "annotation", "labels"])],
           "The dimensions and orientation of the canvas; the exact colour values in hex or CMYK; the names and sizes of the fonts used; and the position of every image and text element, with annotations explaining the intention.",
           command="Identify"),
        EQ("A production company is planning a one minute promotional video.\n\nExplain **two** reasons why a storyboard is produced before filming begins.", 4,
           [MP("It communicates the intended shots to the whole crew", ["crew", "camera operator", "director", "everyone", "shared", "communicate"]),
            MP("Development of that reason", ["knows what to shoot", "shot list", "no misunderstanding", "same understanding"]),
            MP("It identifies problems while they are still cheap to fix", ["cheaper", "easier", "before filming", "on paper", "saves time", "avoid reshoot"]),
            MP("Development of that reason", ["reshoot costs", "wasted day", "missing shot", "editor has nothing"])],
           "One reason is communication: the storyboard shows the camera operator, director, sound recordist and editor exactly which shots are needed, in what order and for how long, so everyone arrives with the same understanding and the shoot works to a list rather than improvising. The second is cost: a problem spotted on a storyboard, such as a sequence that will not cut together because there is no establishing shot, takes minutes to fix with a pencil, whereas the same problem discovered in the edit means hiring the crew and location again for a reshoot.",
           command="Explain"),
        EQ("A college has commissioned an interactive website where students can browse courses, watch a short video about each one and apply online.\n\nDiscuss the pre-production documents the developers should produce, and justify why each is needed for this product.", 8,
           [MP("A navigation diagram is identified", ["navigation diagram", "site map", "structure"]),
            MP("Justified for this product", ["every screen", "reachable", "dead end", "route back", "courses", "depth"]),
            MP("Wireframes are identified", ["wireframe"]),
            MP("Justified for this product", ["each screen", "layout", "placement", "without styling", "course page", "application form"]),
            MP("A storyboard is identified for the videos", ["storyboard"]),
            MP("Justified for this product", ["videos", "shots", "short video", "filming", "each course"]),
            MP("An asset table is identified", ["asset table", "asset list", "licence"]),
            MP("A work plan, or a judgement about which document matters most", ["work plan", "schedule", "Gantt", "most important", "overall", "the key document"])],
           "The structural document comes first: a navigation diagram showing the home screen, the course listing, each individual course page, the video on it and the application form, with arrows for every link. For this product that is essential because there are many near identical course pages and an application flow, so the risks are a course that cannot be reached from the listing, an application form with no route back if the student changes their mind, and courses buried three or four levels deep. All three are visible on a diagram and invisible in a half built site. Wireframes come next, one for every distinct screen rather than only the home page, because the course page, the listing and the application form are completely different layouts; wireframing them without colour or type keeps the discussion on what goes where and lets the college approve the structure before any styling exists to argue about. A storyboard is needed for the course videos, since each one is a moving image product in its own right: shot type, duration, voiceover and the order of shots have to be planned so that one crew visit can capture every course rather than returning for missing footage. An asset table records every photograph, logo, video clip and piece of music with its source and licence, which matters particularly here because a college site will use student photographs, and that means consent as well as copyright. A work plan ties the lot together, ordering tasks so that filming, which depends on people and locations, is scheduled before the editing that depends on it. Of these, the navigation diagram is the one that cannot be skipped: a styling mistake is a day's work to correct, whereas a structural mistake discovered after the content is in means rebuilding the site.",
           command="Discuss"),
    ],
)

M_PLAN = Topic(
    slug="work-planning-and-workflow",
    title="R093 TA3: Work Planning and Workflow",
    spec="R093 TA3",
    icon="i-clock",
    minutes=22,
    blurb="Breaking a project into tasks, putting them in an order that works, and planning for the thing that will go wrong.",
    fact="The critical path method was developed in the 1950s for building chemical plants and launching missiles. The same maths now decides whether a two minute YouTube video gets finished on time.",
    sections=[
        Section("What a work plan contains", """
A work plan turns a project into something that can be tracked.

| Element | Meaning |
| **Task** | One unit of work with a clear finish |
| **Duration** | How long the task takes |
| **Sequence** | The order tasks happen in |
| **Dependency** | A task that cannot start until another finishes |
| **Milestone** | A fixed checkpoint, often a client sign off |
| **Resources** | The people, equipment, software and locations needed |
| **Contingency** | Spare time deliberately built in for problems |
| **Critical path** | The chain of dependent tasks that sets the shortest possible project length |

### Gantt charts

Tasks down the left, time across the top, one bar per task. Overlapping bars are tasks running in parallel; bars that start where another ends are dependencies. A Gantt chart answers the two questions a client asks: what are you doing now, and will it be ready on time.

!key Dependency is the word that earns marks :: You cannot edit footage that has not been shot, and you cannot shoot without a location booked. Saying "editing depends on filming, so filming has to finish first" shows you understand sequencing, which is what the question is testing.
"""),
        Section("Workflow and the production phases", """
Every media product moves through the same three phases, and knowing what belongs in each is examinable.

| Phase | Contains |
| **Pre-production** | Brief, research, ideas, planning documents, asset sourcing, scheduling, booking, risk assessment |
| **Production** | Filming, recording, photographing, designing, building, writing code |
| **Post-production** | Editing, grading, mixing, effects, testing, review, export, distribution |

### Why the order cannot be rushed

Teams that skip pre-production to "get started" spend the saved time three times over in post-production, because every missing decision has to be made late, with less information and more already built on top of it.

### Version control

- Save a new version at each significant stage rather than overwriting
- Use a naming convention that sorts correctly: `poster-v03-client-review.svg`
- Never use "final" in a file name. There is always a `final-final-2`
- Keep the layered working file as well as every export
- Back up in a second location, because one copy is not a backup
"""),
        Section("Risk, contingency and resources", """
### Risks worth planning for

| Risk | Typical contingency |
| Equipment failure | Spare battery, spare card, a second camera |
| A contributor pulling out | A reserve interviewee; shoot the flexible material first |
| Weather | An indoor alternative and a reserve date |
| Software or file corruption | Versioned saves and an off site backup |
| An asset turning out to be unlicensed | Clear licences before production, not after |
| Underestimated edit time | Contingency days before the deadline, not after |

### Resources

- **People** and their availability, which is usually the real constraint
- **Equipment**, booked rather than assumed
- **Locations**, with permission in writing
- **Software and hardware**, with the version checked
- **Time**, which is the only one that cannot be bought more of

!grade Contingency is not optimism :: "I would work faster" is not contingency. Contingency is naming a specific risk, saying what you would do instead, and putting the spare time in the plan where it is needed. A plan that finishes exactly on the deadline has no contingency at all.
"""),
    ],
    keyterms=[
        ("Work plan", "A schedule of tasks, durations, dependencies, milestones and resources for a project."),
        ("Gantt chart", "A bar chart of tasks against time, showing sequence, overlap and dependencies."),
        ("Dependency", "A task that cannot begin until another has finished."),
        ("Milestone", "A fixed checkpoint in a project, often a client sign off."),
        ("Contingency", "Spare time or an alternative plan deliberately built in for problems."),
        ("Critical path", "The sequence of dependent tasks that determines the shortest possible project duration."),
        ("Version control", "Keeping numbered versions of files so earlier states can be recovered."),
    ],
    grade="""
Answers reach the top band by being **specific to the product described**. Not "you need a work plan to stay organised" but "filming is on day four, so the location permission and the contributor confirmation have to be milestones on day two, and the two contingency days belong before the client review rather than after it."
""",
    mistakes=[
        "Listing tasks with no durations, order or dependencies, which is a to do list rather than a work plan.",
        "Planning to finish exactly on the deadline, which leaves no contingency at all.",
        "Calling 'working harder' a contingency plan.",
        "Putting post-production tasks in the production phase.",
        "Overwriting one file throughout instead of keeping versions.",
        "Using 'final' in a filename.",
    ],
    quiz=[
        Q("What is a dependency in a work plan?",
          ["A task that cannot start until another finishes",
           "A task that takes the longest", "A task done by someone else",
           "A milestone"], 0,
          "Editing depends on filming, so filming must finish first."),
        Q("What does a Gantt chart show?",
          ["Tasks plotted against time, with their order and overlap",
           "The budget for each task", "The structure of a website",
           "The shots in a video"], 0,
          "Bars against a timeline show sequence, parallel work and dependencies at a glance."),
        Q("Which of these is genuine contingency planning?",
          ["Booking a reserve date in case of bad weather",
           "Planning to work faster if you fall behind",
           "Hoping nothing goes wrong", "Starting the project earlier"], 0,
          "Contingency names a risk and provides a specific alternative."),
        Q("In which phase does colour grading happen?",
          ["Post-production", "Pre-production", "Production", "Distribution"], 0,
          "Grading is done to footage that already exists, so it is post-production."),
        Q("Why should 'final' never appear in a file name?",
          ["There is always another version after it",
           "It is too long", "Software cannot read it",
           "It breaks version control software"], 0,
          "Names like final-final-2 are the result, and nobody can tell which is current."),
        Q("What is a milestone?",
          ["A fixed checkpoint such as a client sign off",
           "The longest task in a project", "The project deadline only",
           "A task with no dependencies"], 0,
          "Milestones are points progress is measured against."),
        Q("Which is the real constraint on most small productions?",
          ["People's availability", "Hard disk space",
           "Software licences", "Internet speed"], 0,
          "Getting the right people in the same place on the same day is usually the hardest part."),
        Q("What is the critical path?",
          ["The chain of dependent tasks that sets the shortest possible duration",
           "The most expensive task", "The route to the location",
           "The order of shots in an edit"], 0,
          "Any delay to a task on the critical path delays the whole project."),
        Q("Risk assessment belongs in which phase?",
          ["Pre-production", "Production", "Post-production", "Distribution"], 0,
          "It is a planning activity, done before anyone is on location."),
        Q("Why keep the layered working file as well as the export?",
          ["Changes can be made without starting again",
           "It is smaller", "Exports cannot be opened",
           "It is required by copyright law"], 0,
          "A flattened export cannot be meaningfully edited, so the working file is the real asset."),
    ],
    exam=[
        EQ("Identify **three** things that should be included in a work plan.", 3,
           [MP("Tasks", ["task", "activities", "jobs", "stages"]),
            MP("Durations or deadlines", ["duration", "time", "how long", "deadline", "dates"]),
            MP("Dependencies, milestones, resources or contingency", ["dependency", "order", "sequence", "milestone", "resources", "contingency"])],
           "The tasks to be completed, the duration of each, and the dependencies showing which tasks must finish before others can begin.",
           command="Identify"),
        EQ("Explain why dependencies must be identified when planning a video production.", 3,
           [MP("A dependency means one task cannot start until another finishes", ["cannot start", "must finish first", "depends on", "after"]),
            MP("A relevant example from video production", ["edit", "film", "footage", "location", "script", "shoot"]),
            MP("The consequence of getting it wrong", ["delay", "wasted", "idle", "miss the deadline", "cannot work", "reshoot"])],
           "A dependency is a task that cannot begin until another has finished, and in a video production the chain is strict: the script has to exist before the storyboard, the storyboard before the shoot, and the footage before any editing. Identifying these means the schedule puts them in a workable order and the resources are booked for the right days. If they are missed, an editor is booked for a week in which no footage exists, which wastes the booking and pushes the whole project past its deadline, because every later task sits behind the delay.",
           command="Explain"),
        EQ("A student has four weeks to produce a two minute promotional video for a local business. Filming must take place on location at the business.\n\nDescribe **two** risks to this project and give a suitable contingency for each.", 4,
           [MP("A genuine risk is identified", ["weather", "equipment", "contributor", "access", "illness", "corruption", "business closed", "noise"]),
            MP("A specific, workable contingency for it", ["reserve date", "spare", "backup", "indoor", "second camera", "alternative"]),
            MP("A second, different risk", ["footage", "file", "edit time", "permission", "staff", "battery"]),
            MP("A specific contingency for the second", ["two copies", "cloud", "contingency days", "earlier", "written permission", "spare card"])],
           "One risk is that the business turns out to be too busy or too noisy on the filming day, so usable audio cannot be recorded. The contingency is to agree a reserve date before the first one and to record a clean voiceover separately, so the project does not depend on usable location sound. A second risk is losing the footage to a corrupted memory card, which would be unrecoverable within four weeks. The contingency is to copy the card to two separate drives on the day of the shoot before the card is reused, so no single failure can destroy the only copy.",
           command="Describe"),
        EQ("A small agency has six weeks to deliver a campaign consisting of a printed poster, a 30 second social media video and a landing page.\n\nDiscuss how the agency should plan and sequence this work, and explain the consequences of planning it badly.", 8,
           [MP("Tasks are broken down across the three deliverables", ["poster", "video", "landing page", "tasks", "break down"]),
            MP("Dependencies between tasks are identified", ["depends", "cannot start", "before", "after", "once"]),
            MP("Parallel work is identified where possible", ["at the same time", "parallel", "while", "simultaneously", "overlap"]),
            MP("A shared asset or brand decision is recognised as coming first", ["same images", "brand", "palette", "shared assets", "visual identity", "one shoot"]),
            MP("Milestones or client sign off points are placed", ["milestone", "sign off", "approval", "review", "checkpoint"]),
            MP("The print deadline is treated as fixed", ["print", "printer", "lead time", "cannot be changed", "fixed deadline"]),
            MP("Contingency is included and justified", ["contingency", "spare", "buffer", "reserve", "slack"]),
            MP("Consequences of poor planning are explained with a judgement", ["miss the deadline", "cost", "reshoot", "rush", "quality", "most serious"])],
           "The first move is to separate the work into tasks per deliverable and then look for what they share, because the three products are not independent: all of them need the same palette, typography and photography, so the brand decisions and a single photo shoot should sit at the front of the plan and feed all three. That turns one shoot into assets for the poster, the video and the page instead of three separate pieces of production. After that, dependencies set the order. The poster cannot be artworked until the images and the headline are approved, the video cannot be edited until the footage exists, and the landing page cannot be built until the copy and assets are ready, although the page's structure can be wireframed in parallel with filming because it does not depend on the footage. Printing is the hardest constraint in the whole plan: a printer needs files several days before delivery and will not accept late changes, so the print sign off milestone has to be set roughly a week before the campaign date and everything upstream of it scheduled backwards from there. The video and the page are more forgiving, since both can be updated after publication. Milestones belong at the points where a mistake would be expensive: brand sign off before any artwork, image approval before artworking, and a final client review before the print file is sent. Contingency of three or four days should sit immediately before the print deadline rather than at the end of the project, because that is where a delay cannot be absorbed. Planned badly, the likely failures are predictable: a shoot run after artwork has started, so the images do not fit the layout; the page and the poster using different colours because the brand decisions were made twice; and most seriously the print file arriving late, which cannot be solved with extra effort because the printer's schedule is outside the agency's control. That is the consequence worth emphasising, since the video and the page can be fixed after release and the poster cannot be fixed at all once it is printed.",
           command="Discuss"),
    ],
)

M_LEGAL = Topic(
    slug="legislation-and-permissions",
    title="R093 TA3: Legislation, Copyright and Permissions",
    spec="R093 TA3",
    icon="i-shield",
    minutes=26,
    blurb="Copyright, licences, intellectual property, data protection, consent and certification. Named laws and what each one actually stops you doing.",
    fact="Copyright is automatic. The moment a photograph is taken, the person who pressed the shutter owns it, with no registration and no copyright symbol needed. That is exactly why an image found through a search engine is almost never free to use.",
    sections=[
        Section("Copyright and intellectual property", """
### Copyright

**Copyright** protects original work automatically from the moment it is created. It covers photographs, video, music, text, artwork, software and designs. It does not have to be registered or marked.

- In the UK it lasts for the **life of the author plus 70 years** for most creative work
- The **creator** owns it, unless it was made as part of their employment, in which case the employer does
- **Infringement** is using it without permission: copying, publishing, adapting or performing it

### The other intellectual property rights

| Right | Protects | Example |
| **Copyright** | Original creative work | A photograph, a song, a video |
| **Trade mark** | Brand identifiers | A logo, a name, a slogan, a jingle |
| **Registered design** | The appearance of a product | The shape of a bottle |
| **Patent** | An invention or technical process | A new compression algorithm |

### Licences

| Licence | What it allows |
| **All rights reserved** | Nothing without explicit permission |
| **Royalty free** | Pay once, use many times within the licence terms. Not the same as free |
| **Rights managed** | Licensed for a specific use, place and period |
| **Creative Commons BY** | Use freely, credit the creator |
| **Creative Commons BY-SA** | Credit, and share any derivative under the same licence |
| **Creative Commons BY-NC** | Credit, non commercial use only |
| **Creative Commons CC0 / public domain** | No restrictions |
| **Editorial use only** | News and comment only. Never advertising |

!warn Two traps that catch real projects :: "Royalty free" does not mean free of charge; it means no repeat fee. And a site carrying advertising is commercial use, so a `BY-NC` asset cannot be used on it.
"""),
        Section("People, data and privacy", """
### Permissions and releases

- A **model release** is written consent from an identifiable person to use their image
- A **property release** is permission from an owner to film their building or land
- **Children** require consent from a parent or guardian, and the bar is higher
- **Location permission** is needed for most filming other than casual use of a public street
- **Music** needs a licence from the rights holder, which for commercial music usually means two: the recording and the composition

### Data protection

The **Data Protection Act 2018**, which implements the UK GDPR, governs personal data. For a media product collecting names, emails or analytics, the examinable principles are:

- Collect only what you need, for a stated purpose
- Keep it accurate, secure and no longer than necessary
- Be transparent: say what you collect and why, in a privacy notice
- People can ask what you hold, correct it, and ask for it to be deleted
- A breach of significance must be reported to the ICO within 72 hours

### The other named laws

| Law | What it covers |
| **Computer Misuse Act 1990** | Unauthorised access to systems, and malware |
| **Equality Act 2010** | Discrimination, and the duty to make reasonable adjustments, which is why accessibility is a legal issue |
| **Defamation Act 2013** | Publishing an untrue statement that damages someone's reputation |
| **Consumer Protection from Unfair Trading Regulations** | Misleading advertising claims |
"""),
        Section("Regulation and certification", """
Different media are regulated by different bodies, and the paper expects the names.

| Body | Regulates |
| **BBFC** | Film and video age ratings in the UK |
| **PEGI** | Age ratings for video games in Europe |
| **Ofcom** | Television, radio and video on demand standards |
| **ASA** | Advertising, across all media |
| **IPSO** | Most of the UK press |
| **ICO** | Data protection and privacy |

### Why certification affects production decisions

A rating is not applied at the end; it is designed for from the start. A film aiming for a 12A cannot shoot content that would push it to a 15 and expect to cut it out later, because the content usually turns out to be structural. The same applies to a game aiming for PEGI 7 and to an advert aiming to be shown before 9pm.

!grade Name the law and the specific action :: "You must follow copyright law" is a weak answer. "The photograph is licensed CC BY-NC, and because the website carries advertising it is a commercial use, so a different image or a paid licence is needed" names the right, applies it to the situation and reaches a conclusion. That is a full mark answer.
"""),
    ],
    keyterms=[
        ("Copyright", "An automatic right protecting original work, lasting in the UK for the author's life plus 70 years."),
        ("Intellectual property", "Creations of the mind protected by copyright, trade marks, designs or patents."),
        ("Trade mark", "Protection for a brand identifier such as a logo, name or slogan."),
        ("Royalty free", "A licence paid for once, allowing repeated use within its terms. Not free of charge."),
        ("Creative Commons", "A set of standard licences allowing reuse on stated conditions such as credit."),
        ("Model release", "Written consent from an identifiable person to use their image."),
        ("Data Protection Act 2018", "The UK law governing how personal data is collected, stored and used."),
        ("BBFC", "The body that classifies film and video for age suitability in the UK."),
        ("PEGI", "The European age rating system for video games."),
        ("ASA", "The body that regulates advertising in the UK."),
    ],
    grade="""
Full marks come from **applying** a named right to the scenario rather than reciting it. Identify the right, identify the use, say whether that use is permitted, and say what to do about it. Finishing with the action, obtain a licence, get a release, replace the asset, is what separates a 3 from a 1.
""",
    mistakes=[
        "Thinking work has to be registered or marked to be protected. Copyright is automatic.",
        "Treating 'royalty free' as meaning free of charge.",
        "Using a non commercial licence on a site that carries advertising or sells anything.",
        "Forgetting that identifiable people need a release, and children need parental consent.",
        "Confusing the regulators: BBFC for film, PEGI for games, ASA for adverts, Ofcom for broadcast.",
        "Assuming anything found through an image search may be used.",
    ],
    quiz=[
        Q("When does copyright begin on a photograph?",
          ["The moment it is taken", "When it is published",
           "When it is registered", "When the © symbol is added"], 0,
          "Protection is automatic and needs no registration or marking."),
        Q("How long does copyright usually last in the UK for creative work?",
          ["The author's life plus 70 years", "25 years",
           "50 years from publication", "Forever"], 0,
          "Life plus 70 years is the standard term for most creative works."),
        Q("What does 'royalty free' mean?",
          ["Pay once, then use repeatedly within the licence terms",
           "Free of charge", "Free for non commercial use",
           "No credit required"], 0,
          "It refers to not paying a fee per use, not to the asset being free."),
        Q("A site carrying adverts wants to use a CC BY-NC image. Is that allowed?",
          ["No, advertising makes it commercial use", "Yes, with credit",
           "Yes, if the advert is small", "Yes, images are exempt"], 0,
          "NC means non commercial, and a site funded by advertising is a commercial use."),
        Q("Which right protects a company logo?",
          ["Trade mark", "Copyright only", "Patent", "Registered design"], 0,
          "Brand identifiers are protected as trade marks."),
        Q("What is a model release?",
          ["Written consent from an identifiable person to use their image",
           "A licence for a piece of music", "Permission to film a building",
           "An age rating certificate"], 0,
          "Without one, an identifiable person can object to the use of their image."),
        Q("Which body classifies video games for age suitability?",
          ["PEGI", "BBFC", "Ofcom", "ASA"], 0,
          "PEGI rates games; the BBFC rates film and video."),
        Q("Within how long must a significant personal data breach be reported to the ICO?",
          ["72 hours", "7 days", "24 hours", "30 days"], 0,
          "The UK GDPR requires notification without undue delay and within 72 hours."),
        Q("Which law makes accessibility a legal duty for service providers?",
          ["Equality Act 2010", "Computer Misuse Act 1990",
           "Data Protection Act 2018", "Defamation Act 2013"], 0,
          "It requires reasonable adjustments so disabled people are not disadvantaged."),
        Q("Why does an intended age rating affect production rather than just distribution?",
          ["Content that changes the rating is usually structural and cannot simply be cut",
           "Ratings are decided before filming", "Certificates cost more later",
           "Ratings only apply to cinema releases"], 0,
          "A sequence that pushes a film from 12A to 15 is normally part of the story, not an add on."),
    ],
    exam=[
        EQ("State **two** types of intellectual property protection, other than copyright.", 2,
           [MP("One valid type", ["trade mark", "trademark", "patent", "registered design", "design right"]),
            MP("A second, different valid type", ["patent", "registered design", "trade mark", "design right"])],
           "A trade mark, and a patent.",
           command="State"),
        EQ("Explain why an image found using an internet search engine should not be used in a commercial media product.", 3,
           [MP("The image is protected by copyright automatically", ["copyright", "protected", "owned", "creator owns"]),
            MP("Permission or a licence is required", ["permission", "licence", "license", "pay", "rights"]),
            MP("The consequence of using it without permission", ["infringement", "sued", "legal action", "takedown", "fine", "damages", "withdrawn"])],
           "Any photograph is protected by copyright from the moment it is taken, and the copyright belongs to the photographer whether or not the image carries a symbol, a watermark or a credit. Appearing in search results is not permission; it only means the image is published somewhere. Using it commercially without a licence is infringement, and the rights holder can demand payment, force the product to be withdrawn or pursue damages, which for a printed product means the whole run is wasted.",
           command="Explain"),
        EQ("A college is producing a promotional video that will feature students, including some under 16, and background music from a chart recording.\n\nIdentify the permissions the college needs and explain why each is required.", 6,
           [MP("Consent from identifiable students is required", ["consent", "release", "permission", "model release"]),
            MP("Why it is required", ["identifiable", "image", "right to", "privacy", "object"]),
            MP("Parental or guardian consent is required for under 16s", ["parent", "guardian", "under 16", "child"]),
            MP("Why the bar is higher for children", ["cannot consent", "safeguarding", "legally", "protection"]),
            MP("A music licence from the rights holder is required", ["licence", "rights holder", "permission", "PRS", "label", "copyright"]),
            MP("Why, or what the alternative is", ["copyright", "two rights", "recording and composition", "expensive", "royalty free alternative", "production music"])],
           "The college needs written consent from every student who is identifiable in the video, because an individual's image is personal data and they have a right to object to its use; consent also has to cover where the video will be shown, since agreeing to appear in an open day screening is not the same as agreeing to appear in a social media advert. For students under 16 that consent must come from a parent or guardian, because a child cannot give informed consent to publication and the college has a safeguarding duty as well as a legal one. The chart recording needs a licence from the rights holders, and in practice that means two permissions, one for the sound recording owned by the label and one for the underlying composition owned by the writer and publisher. Those licences are expensive and often refused for promotional use, so the realistic solution is production music or a Creative Commons track whose licence permits commercial use.",
           command="Explain"),
        EQ("A small business is building a website that will sell products, collect customer email addresses for a newsletter, and use photographs of customers using the products.\n\nDiscuss the legal responsibilities the business has, and the consequences of failing to meet them.", 8,
           [MP("Copyright and licensing of assets is addressed", ["copyright", "licence", "images", "fonts", "music", "permission"]),
            MP("Consent for customer photographs is addressed", ["consent", "release", "permission", "identifiable"]),
            MP("Data protection law is named and applied", ["Data Protection Act", "GDPR", "personal data", "ICO"]),
            MP("Specific data obligations are described", ["privacy notice", "only what is needed", "secure", "delete", "unsubscribe", "purpose", "access"]),
            MP("Accessibility duty under the Equality Act is addressed", ["Equality Act", "accessib", "reasonable adjustment", "disabled"]),
            MP("Advertising or consumer law is addressed", ["ASA", "misleading", "consumer protection", "claims", "accurate"]),
            MP("Consequences are specific", ["fine", "ICO", "enforcement", "sued", "damages", "takedown", "reputation", "withdraw"]),
            MP("A judgement about which duty carries the greatest risk and why", ["most serious", "greatest risk", "biggest", "overall", "therefore"])],
           "The business has duties in four separate areas, and all of them apply to this one website. Every asset on the site, the photographs, the fonts, any music and any icons, must either be the business's own work or be covered by a licence that permits commercial use, since the site sells products and is therefore unambiguously commercial; a non commercial Creative Commons licence is not usable here. The customer photographs need written consent from each identifiable person, specifying that the images will be used for marketing on a commercial website, because consent for one use does not transfer to another. Collecting email addresses brings the Data Protection Act 2018 and the UK GDPR into play: the business must say in a privacy notice what it collects and why, collect only what the newsletter actually needs, store it securely, provide a working unsubscribe link, honour requests to see or delete the data, and report a serious breach to the ICO within 72 hours. Because it provides a service to the public, the Equality Act 2010 requires reasonable adjustments, which in practice means the site must be usable with a screen reader and a keyboard and must meet contrast requirements. Finally the product claims and prices must not mislead, which is enforced by the ASA and by consumer protection law. The consequences differ sharply in scale. An unlicensed image typically produces a demand for a licence fee and a takedown, which is embarrassing but survivable. An inaccessible site risks a complaint and the loss of customers who cannot use it. A data protection failure is the most serious of the four, because the ICO can impose penalties calculated against turnover, the obligation to notify makes concealment itself an offence, and the business would be publishing its own breach to the customers it depends on. The practical conclusion is that the data the site collects, rather than the content it displays, is where the greatest risk sits, so the privacy notice and the security of the mailing list deserve attention before launch rather than after.",
           command="Discuss"),
    ],
)

# =============================================================== R093 TA4

M_FORMATS = Topic(
    slug="file-formats-and-properties",
    title="R093 TA4: File Formats and Properties",
    spec="R093 TA4",
    icon="i-disk",
    minutes=26,
    blurb="Which format for which job, how compression works, and the properties that decide whether a file is fit for purpose. Reliable marks if you know the table.",
    fact="A JPG loses a little quality every time it is saved. Open and re-save the same photograph two hundred times and it degrades into coloured blocks, which is why the working file is never a JPG.",
    sections=[
        Section("Image formats", """
### Raster and vector

| | Raster (bitmap) | Vector |
| **Made of** | A grid of pixels | Mathematical paths and shapes |
| **Scaling** | Blurs or pixelates when enlarged | Scales to any size with no loss |
| **Suits** | Photographs, detailed textures | Logos, icons, diagrams, type |
| **File size** | Grows with dimensions and colour depth | Grows with the number of shapes |
| **Formats** | JPG, PNG, GIF, TIFF, BMP, WEBP | SVG, AI, EPS, PDF |

### The formats themselves

| Format | Compression | Transparency | Use it for |
| **JPG** | Lossy | No | Photographs, where small size matters more than perfect fidelity |
| **PNG** | Lossless | Yes, full alpha | Graphics with flat colour, screenshots, anything needing transparency |
| **GIF** | Lossless, 256 colours | Yes, 1 bit only | Simple animation; obsolete for still images |
| **TIFF** | Lossless or none | Yes | Print production and archive masters |
| **SVG** | None, it is text | Yes | Logos, icons and diagrams on the web |
| **WEBP** | Lossy or lossless | Yes | Modern web images, smaller than JPG at the same quality |
| **PDF** | Mixed | Yes | Sending a finished layout to print or to a client |

!key Choose by the job, not by habit :: Photograph on a web page: JPG or WEBP. Logo: SVG. Screenshot or a graphic with transparency: PNG. Press ready artwork: PDF or TIFF. Those four sentences answer most format questions in the paper.
"""),
        Section("Audio, video and document formats", """
### Audio

| Format | Compression | Use |
| **MP3** | Lossy | Distribution, podcasts, music where size matters |
| **AAC / M4A** | Lossy | Better quality than MP3 at the same size; streaming and Apple devices |
| **WAV** | Uncompressed | Recording and editing masters |
| **AIFF** | Uncompressed | As WAV, on Apple systems |
| **FLAC** | Lossless | Archiving without quality loss |

### Video

| Format | Notes |
| **MP4 (H.264)** | The universal delivery format. Plays everywhere |
| **MOV** | Apple's container, common in production |
| **AVI** | Older Windows container, large files |
| **WMV** | Older Windows format, heavily compressed |
| **MKV** | Flexible container, less widely supported by browsers |

A **container** such as MP4 or MOV holds streams encoded with a **codec** such as H.264 or AAC. Two MP4 files can be completely different inside, which is why a file sometimes will not play even though the extension is right.

### Document and project formats

- **PDF** — fixed layout, looks identical everywhere, for final delivery
- **DOCX, ODT, RTF, TXT** — editable text, in descending order of features
- **PSD, XCF, AI, SVG, PRPROJ, AEP** — working project files, keeping layers and edits
- **ZIP** — a lossless archive, used to deliver a set of files together
"""),
        Section("Properties, compression and fitness for purpose", """
### Properties that get examined

| Property | What it means | Why it matters |
| **Resolution** | Pixels per inch, or total pixel dimensions | 72 ppi is fine on screen; print needs about 300 |
| **Dimensions** | Width and height in pixels or millimetres | Decides whether an image can fill its space |
| **Colour depth** | Bits per pixel | 24 bit gives 16.7 million colours; 8 bit gives 256 |
| **Colour mode** | RGB or CMYK | Screens are RGB; printing presses are CMYK |
| **Aspect ratio** | Width to height | 16:9 landscape, 1:1 square, 9:16 vertical |
| **Frame rate** | Frames per second | 25 fps UK broadcast, 24 cinema, 50 or 60 for sport |
| **Bit rate** | Data per second | The main control over video and audio quality and size |
| **Sample rate** | Audio samples per second | 44.1 kHz is CD quality |
| **Bit depth (audio)** | Bits per sample | 16 bit for delivery, 24 bit for recording |

### Compression

- **Lossless** — nothing is discarded, the original can be restored exactly. PNG, FLAC, ZIP, TIFF
- **Lossy** — detail the eye or ear is least likely to notice is thrown away permanently. JPG, MP3, MP4, AAC

Lossy compression is **generational**: each re-save of a JPG discards more. Always edit the master and export a new copy, rather than editing the export.

### Fitness for purpose

A file is fit for purpose when its format and properties match where it is going.

| Destination | Needs |
| Print poster | CMYK, 300 ppi, PDF or TIFF, with bleed |
| Website hero image | RGB, around 72 to 144 ppi, JPG or WEBP, compressed to a few hundred kilobytes |
| Logo for any use | SVG master, with PNG exports at the sizes needed |
| Social video | MP4 H.264, correct aspect ratio for the platform, captions burned in or supplied |
| Podcast | MP3 at 128 kbps mono or stereo, from a WAV master |

!warn RGB sent to a printing press :: The colours shift, and bright greens and oranges in particular come back dull. Converting to CMYK at the start means the designer sees the real colour; converting at the end means a surprise.
"""),
    ],
    keyterms=[
        ("Raster", "An image stored as a grid of pixels."),
        ("Vector", "An image stored as mathematical paths, scalable without loss."),
        ("Lossy compression", "Compression that permanently discards data to reduce file size."),
        ("Lossless compression", "Compression that reduces size with no data lost."),
        ("Resolution", "The pixel density of an image, measured in pixels per inch."),
        ("Colour depth", "The number of bits used per pixel, which sets how many colours are possible."),
        ("Codec", "The method used to encode and decode a video or audio stream."),
        ("Container", "A file format such as MP4 that holds encoded audio and video streams."),
        ("Bit rate", "The amount of data used per second of audio or video."),
        ("Aspect ratio", "The ratio of a product's width to its height."),
    ],
    grade="""
Format questions are marked on **justification**. Never give the format alone. "PNG, because the logo must sit over a coloured background and PNG supports transparency where JPG does not, and because lossless compression keeps the flat colours and sharp edges clean" is the shape of a full mark answer.
""",
    mistakes=[
        "Saying a format is 'better' without naming the use. Fitness for purpose is the whole question.",
        "Using JPG where transparency is needed. JPG cannot store it.",
        "Sending RGB files to a commercial printer instead of CMYK.",
        "Supplying a logo as a JPG with no vector master.",
        "Repeatedly editing and re-saving a JPG, which compounds the quality loss.",
        "Confusing resolution with dimensions. 300 ppi tells you nothing on its own about how big the image is.",
    ],
    quiz=[
        Q("Which format should be used for a logo that must scale to any size?",
          ["SVG", "JPG", "PNG", "GIF"], 0,
          "A vector format stores shapes rather than pixels, so it never pixelates."),
        Q("Which of these uses lossy compression?",
          ["JPG", "PNG", "TIFF", "FLAC"], 0,
          "JPG discards detail permanently to reduce size. The other three are lossless."),
        Q("What resolution is normally required for commercial print?",
          ["About 300 ppi", "72 ppi", "150 ppi", "600 ppi"], 0,
          "Around 300 ppi at final size is the standard expectation for print."),
        Q("A graphic needs a transparent background on a web page. Which format?",
          ["PNG", "JPG", "BMP", "TIFF"], 0,
          "PNG supports full alpha transparency and is well supported in browsers."),
        Q("Which colour mode is used for printing?",
          ["CMYK", "RGB", "HSL", "Greyscale"], 0,
          "Presses print cyan, magenta, yellow and black inks."),
        Q("What is the difference between a container and a codec?",
          ["The container holds streams; the codec encodes them",
           "They are the same thing", "The codec holds the container",
           "A container is only for audio"], 0,
          "MP4 is a container; H.264 is a codec that might be inside it."),
        Q("Why should you not edit and re-save a JPG repeatedly?",
          ["Each save discards more detail permanently",
           "The file gets larger each time", "It changes the dimensions",
           "It converts to CMYK"], 0,
          "Lossy compression is generational, so quality degrades with every save."),
        Q("Which audio format would you record and edit in?",
          ["WAV", "MP3", "AAC", "M4A"], 0,
          "Uncompressed WAV keeps full quality for editing; MP3 is for delivery."),
        Q("A video is for a vertical social media feed. Which aspect ratio?",
          ["9:16", "16:9", "4:3", "1:1"], 0,
          "Vertical video is 9:16, and cropping a 16:9 master to it loses the sides."),
        Q("What does bit rate control in a video file?",
          ["The data used per second, and so the quality and size",
           "The number of colours", "The frame size",
           "The length of the video"], 0,
          "Higher bit rate means more data per second, so better quality and a bigger file."),
    ],
    exam=[
        EQ("State **one** suitable file format for each of the following, and give a reason for each choice:\n\n(a) a photograph on a web page\n(b) a company logo", 4,
           [MP("(a) JPG, WEBP or similar lossy raster format", ["jpg", "jpeg", "webp"]),
            MP("A reason referring to size, compression or photographic content", ["small", "compress", "photograph", "loads", "quality to size"]),
            MP("(b) SVG, or another vector format", ["svg", "ai", "eps", "vector"]),
            MP("A reason referring to scalability or transparency", ["scale", "any size", "no loss", "pixelate", "transparen", "sharp"])],
           "(a) JPG, because lossy compression gives a small file at a quality that is acceptable for a photograph on screen, so the page loads quickly. (b) SVG, because it stores the logo as mathematical paths, so it stays perfectly sharp at any size from a favicon to a banner and supports a transparent background.",
           command="State"),
        EQ("Explain the difference between lossy and lossless compression, using an example of each.", 4,
           [MP("Lossy defined as permanently discarding data", ["discard", "removes", "permanently", "thrown away", "cannot be restored"]),
            MP("A correct lossy example", ["jpg", "jpeg", "mp3", "mp4", "aac"]),
            MP("Lossless defined as reducing size with nothing lost", ["nothing lost", "restored exactly", "identical", "no loss", "original can be"]),
            MP("A correct lossless example", ["png", "flac", "zip", "tiff", "gif"])],
           "Lossy compression reduces file size by permanently throwing away data that the eye or ear is least likely to notice, so the original can never be recovered and quality drops further with each re-save. JPG is a lossy format, and so is MP3. Lossless compression reduces size by storing the same information more efficiently, so the file can be decompressed back to an exact copy of the original. PNG and FLAC are lossless, as is ZIP. The choice is a trade: lossy gives much smaller files for delivery, lossless keeps the master intact for editing and archiving.",
           command="Explain"),
        EQ("A designer has produced a poster that will be printed professionally and also published on the client's website.\n\nExplain the properties the two versions must have, and why they differ.", 6,
           [MP("The print version needs CMYK", ["CMYK"]),
            MP("The web version needs RGB", ["RGB"]),
            MP("Print resolution of around 300 ppi is stated", ["300", "high resolution", "ppi", "dpi"]),
            MP("Web resolution or file size is addressed", ["72", "144", "lower", "screen", "small file", "kilobytes", "loads"]),
            MP("Appropriate print format is named", ["PDF", "TIFF", "press ready", "bleed"]),
            MP("Appropriate web format is named, with a reason for the difference", ["JPG", "WEBP", "PNG", "because", "loads quickly", "bandwidth"])],
           "The print version must be CMYK, because a printing press lays down cyan, magenta, yellow and black ink and an RGB file has to be converted at some point; converting it at the start means the designer sees the colours that will actually be printed rather than being surprised by dull greens. It needs to be around 300 ppi at final size so that detail and type edges are sharp on paper, and it should be supplied as a press ready PDF with bleed and crop marks so that trimming does not leave white edges. The web version must be RGB, because screens emit red, green and blue light, and a CMYK file either will not display correctly or will be converted by the browser with unpredictable results. It only needs enough pixels for the size it is displayed at, so a far lower resolution is appropriate, and it should be exported as a compressed JPG or WEBP of a few hundred kilobytes. The properties differ because the two destinations have opposite priorities: print is a fixed, one chance process where quality cannot be recovered, while the web is a bandwidth limited medium where a slow page loses the audience before the poster is seen.",
           command="Explain"),
        EQ("A media company is delivering a campaign as a printed leaflet, a social media video and a podcast episode.\n\nDiscuss the file formats and properties each deliverable requires, and justify your choices.", 8,
           [MP("A suitable print format is named with properties", ["PDF", "TIFF", "CMYK", "300"]),
            MP("Print properties justified", ["press", "ink", "sharp", "bleed", "cannot be changed", "one chance"]),
            MP("A suitable video format is named", ["MP4", "H.264", "H264"]),
            MP("Video properties addressed", ["aspect ratio", "9:16", "1:1", "16:9", "bit rate", "resolution", "frame rate", "captions"]),
            MP("Video choice justified by platform or audience", ["plays everywhere", "platform", "compatib", "vertical", "mobile", "sound off"]),
            MP("A suitable audio format is named with properties", ["MP3", "AAC", "kbps", "44.1", "mono", "stereo"]),
            MP("The master versus delivery distinction is made", ["WAV", "master", "export", "working file", "layered", "archive"]),
            MP("An overall judgement about fitness for purpose", ["fit for purpose", "destination", "overall", "therefore", "each"])],
           "Each deliverable goes to a different destination, and the destination decides the format rather than any general idea of quality. The leaflet is going to a commercial printer, so the artwork should be built in CMYK at around 300 ppi at final trimmed size and delivered as a press ready PDF with bleed, crop marks and fonts embedded or converted to outlines. That specification exists because print is a single irreversible process: a low resolution image or an unexpected colour conversion cannot be corrected after the run, and a missing font substituted by the printer's system would change the design. The social video should be exported as MP4 using the H.264 codec, because that combination plays on effectively every phone, browser and platform, and it should be mastered in the aspect ratio of the feed it is made for rather than cropped later, so a vertical 9:16 or square 1:1 version is framed as such at the shoot. Bit rate should be high enough that motion stays clean after the platform re-encodes it, which it always does, and captions should be supplied or burned in because most feed video is watched with the sound off. The podcast should be recorded and edited as uncompressed WAV at 44.1 kHz and 24 bit, then exported to MP3 at around 128 kbps for distribution, because podcast listeners are usually on mobile data and speech survives that compression well, while editing a lossy file would compound its artefacts. Running through all three is the same principle: the master is kept lossless and layered, and each delivery file is a separate export matched to its destination. Judging fitness for purpose means asking what the file has to survive, a printing press, a platform's own re-encoding, or a listener's data allowance, and choosing the format that survives it.",
           command="Discuss"),
    ],
)

M_DIST = Topic(
    slug="distribution-platforms",
    title="R093 TA4: Distribution Platforms and Media",
    spec="R093 TA4",
    icon="i-web",
    minutes=22,
    blurb="How a finished product reaches its audience, what each platform demands in return, and why the platform is a design decision rather than an afterthought.",
    fact="A film released in cinemas, on disc, on a subscription service and on broadcast television is the same film four times over, and each release has different artwork, a different length of advertising campaign and sometimes a different edit.",
    sections=[
        Section("Physical and online distribution", """
| | Physical | Online |
| **Examples** | Print, DVD and Blu-ray, USB, cinema, billboards, packaging | Websites, streaming, downloads, social media, apps, email |
| **Reach** | Limited by logistics and geography | Global and immediate |
| **Cost** | Manufacturing, storage, shipping, retail margin | Hosting and bandwidth, usually far lower |
| **Updating** | Impossible once produced | Can be corrected or replaced at any time |
| **Audience data** | Almost none | Detailed analytics |
| **Permanence** | The object persists and needs no power | Depends on a service continuing to exist |
| **Accessibility** | Fixed; large print must be a separate version | Resizable text, captions, screen readers |

### Why physical has not disappeared

A billboard reaches people who have blocked every advert online. Packaging is the only medium that reaches a customer at the moment of choosing. Print still carries authority that a web page does not. Questions offering a choice between physical and online usually want you to recognise that the answer depends on where the audience actually is.

!key The deadline is the real difference :: Online can be fixed after publication, print cannot. That single fact changes how much checking, proofing and sign off a print project needs, and it is worth saying in any comparison.
"""),
        Section("Platforms and what they demand", """
Each platform imposes its own requirements, and a product that ignores them underperforms however good it is.

| Platform | Demands |
| **Website** | Responsive layout, fast loading, SEO, accessibility, HTTPS |
| **Social feeds** | Correct aspect ratio per platform, captions, the point made in the first seconds, native upload rather than a link |
| **Video on demand** | High bit rate master, thumbnail artwork, subtitle files, metadata |
| **Streaming music and podcasts** | Correct loudness, episode artwork, RSS metadata, chapters |
| **App stores** | Store artwork, screenshots, age rating, privacy declaration, review process |
| **Email** | Small images, alt text, a plain text fallback, an unsubscribe link |
| **Print** | CMYK, 300 ppi, bleed, trim and safe margins, press deadline |
| **Broadcast** | Technical delivery specification, loudness standards, compliance review |

### Streaming compared with downloading

| | Streaming | Downloading |
| Playback | Starts almost at once | Must finish first |
| Storage used | Very little | The whole file |
| Needs a connection | Continuously | Only while downloading |
| Control | The platform keeps the file | The user holds a copy |
| Suits | Watch once content, live, discovery | Offline use, repeat listening, archiving |
"""),
        Section("Choosing and comparing platforms", """
A platform decision answers four questions:

1. **Where is the audience already?** Reaching them is cheaper than moving them.
2. **What does the product need to do there?** Be watched muted, be read slowly, be acted on immediately.
3. **What does the platform cost?** In money, in production work, and in the cut it takes.
4. **How will success be measured?** Views, completion rate, click through, sales, enquiries.

### Multi-platform campaigns

Most real campaigns run on several platforms at once, with a different cut or crop for each. That is not laziness; it is matching the asset to the context. The things to keep constant are the message, the palette and the logo. The things to change are the aspect ratio, the length and the call to action.

### Advantages and drawbacks worth having ready

| Online | |
| Advantages | Global reach, low cost, measurable, updateable, interactive, shareable |
| Drawbacks | Easy to pirate, depends on connection, enormous competition for attention, platform rules can change without notice |

| Physical | |
| Advantages | Tangible, no device needed, reaches ad blocked audiences, authority, collectable |
| Drawbacks | Manufacturing and distribution costs, slow, cannot be corrected, limited reach, environmental impact |

!grade Decide, then defend :: Questions asking which platform is "most appropriate" are marked on the justification, not the choice. Name the platform, tie it to where the audience is, say what the product must do there, and acknowledge one drawback and how you would handle it.
"""),
    ],
    keyterms=[
        ("Distribution", "The process of getting a finished media product to its audience."),
        ("Physical distribution", "Delivery through tangible media such as print, disc or packaging."),
        ("Streaming", "Playing media as it arrives over a network, without storing the whole file."),
        ("Downloading", "Transferring a complete file to a device before it is used."),
        ("Responsive design", "A layout that adapts to the screen size it is viewed on."),
        ("Native upload", "Posting a video directly to a platform rather than linking to it elsewhere."),
        ("Multi-platform", "Releasing a product across several platforms, adapted for each."),
    ],
    grade="""
Comparison questions need a **judgement**, not a list. Two balanced paragraphs ending with "therefore" and a reason will outscore six bullet points. Name the audience, name the platform, name one drawback, and say how you would manage it.
""",
    mistakes=[
        "Listing advantages of online distribution without saying who the audience is.",
        "Treating physical distribution as obsolete when it still reaches audiences online cannot.",
        "Posting the same crop of a video to every platform.",
        "Forgetting that print cannot be corrected after it is printed.",
        "Describing streaming as the same thing as downloading.",
        "Ending a 'which is most appropriate' question without actually choosing.",
    ],
    quiz=[
        Q("What is the main difference between streaming and downloading?",
          ["Streaming plays as it arrives and does not store the whole file",
           "Streaming is always higher quality", "Downloading needs no storage",
           "Streaming works without a connection"], 0,
          "Streaming trades storage and offline access for an immediate start."),
        Q("Which is a drawback of physical distribution?",
          ["It cannot be corrected once produced", "It cannot reach a local audience",
           "It requires a fast connection", "It provides too much audience data"], 0,
          "Once a leaflet is printed, an error is permanent across the whole run."),
        Q("Why should a video be uploaded natively to a social platform rather than linked?",
          ["Native uploads play automatically and are promoted by the platform",
           "Links are not allowed", "Native uploads are higher quality",
           "Linking breaks copyright"], 0,
          "Platforms favour content that keeps users on the platform, and autoplay matters."),
        Q("Which platform requirement is specific to print?",
          ["Bleed and trim margins", "Alt text", "Captions", "HTTPS"], 0,
          "Bleed allows for the inaccuracy of trimming, which only applies to printed material."),
        Q("A campaign runs on three social platforms. What should change between them?",
          ["Aspect ratio, length and call to action",
           "The logo", "The message", "The colour palette"], 0,
          "Format adapts to the platform; identity and message stay constant."),
        Q("Which is an advantage of online distribution for a small business?",
          ["It is measurable, so spending can be judged",
           "It guarantees attention", "It cannot be ignored",
           "It needs no updating"], 0,
          "Analytics show what worked, which physical distribution rarely can."),
        Q("Why does a billboard still have value in a digital campaign?",
          ["It reaches people who block online advertising",
           "It is cheaper than social media", "It can be updated daily",
           "It provides detailed analytics"], 0,
          "It is one of the few media an audience cannot opt out of."),
        Q("What does responsive design mean?",
          ["The layout adapts to the screen it is viewed on",
           "The site responds quickly", "Users can comment",
           "The design responds to feedback"], 0,
          "One layout, adapting across phone, tablet and desktop."),
        Q("Which platform requirement protects users with hearing impairments?",
          ["Captions and subtitle files", "Higher bit rate",
           "Thumbnail artwork", "Faster loading"], 0,
          "Captions also serve the majority who watch feed video muted."),
        Q("An app is being released. Which requirement is imposed by the platform?",
          ["Store artwork, screenshots, an age rating and a privacy declaration",
           "A printed manual", "Bleed margins", "An RSS feed"], 0,
          "App stores operate a review process with mandatory metadata."),
    ],
    exam=[
        EQ("Give **two** advantages of distributing a media product online rather than in print.", 2,
           [MP("One valid advantage", ["reach", "global", "cheaper", "cost", "quick", "measurable", "update", "analytics", "share"]),
            MP("A second, different valid advantage", ["update", "measurable", "cost", "reach", "interactive", "instant"])],
           "It reaches a global audience immediately rather than being limited by distribution, and it can be corrected or updated after publication.",
           command="Give"),
        EQ("Describe **two** differences between streaming and downloading a video.", 4,
           [MP("Streaming begins playing before the whole file arrives", ["straight away", "as it arrives", "immediately", "no wait", "buffer"]),
            MP("Downloading requires the file to transfer first", ["must finish", "wait", "whole file", "complete"]),
            MP("Streaming uses little storage and needs a continuous connection", ["no storage", "little storage", "continuous", "connection", "internet throughout"]),
            MP("Downloading stores the file and allows offline use", ["offline", "stored", "keeps a copy", "no connection needed", "storage space"])],
           "Streaming begins playing almost as soon as it starts arriving, because only a small buffer is needed before playback, whereas a download has to transfer completely before it can be watched. Streaming also uses almost no storage on the device but needs a continuous connection throughout, so it fails on a weak signal, while a download occupies the full file size on the device and can then be watched offline as many times as the user likes.",
           command="Describe"),
        EQ("A theatre wants to promote a new production to local audiences, including people over 70 who are among its most frequent attenders.\n\nJustify the distribution platforms the theatre should use.", 6,
           [MP("A platform suited to the older local audience is named", ["print", "leaflet", "poster", "local paper", "direct mail", "email"]),
            MP("Justified by where that audience actually is", ["over 70", "not on social", "reads", "local", "familiar", "trust"]),
            MP("A second platform is named", ["social media", "website", "email", "facebook", "local radio"]),
            MP("Justified for a different part of the audience or purpose", ["younger", "new audience", "booking", "shareable", "information"]),
            MP("The theatre's own website or booking route is addressed", ["website", "booking", "tickets", "box office", "information"]),
            MP("A drawback is acknowledged and managed", ["cost", "print cannot be changed", "reach", "however", "but", "to address this"])],
           "The theatre should lead with print and local press, because its most frequent attenders are over 70 and that audience is reliably reached by a posted season brochure, a local newspaper listing and posters in the town, whereas a social media campaign would largely miss them. Print also carries an authority this audience responds to, and a brochure sits on a kitchen table for weeks, which a post does not. Alongside that it should run email to its existing mailing list, which is the cheapest route to people who have already bought tickets and the easiest to measure, and social media to reach a younger local audience it does not currently have, using short vertical video of rehearsals rather than a photograph of a poster. All of these should point to one place: the theatre's own website, where the booking happens, because every platform's job is to move someone to the box office rather than to be admired. The obvious drawback of the print led approach is cost and inflexibility, since a brochure cannot be changed once printed and a date change would make it wrong; the theatre should therefore keep performance dates on the website as the authoritative source and print only what is genuinely fixed.",
           command="Justify"),
        EQ("A games studio is releasing a new title. It is considering distributing physically on disc as well as digitally through an online store.\n\nDiscuss the advantages and drawbacks of each option and recommend an approach.", 8,
           [MP("An advantage of digital distribution", ["instant", "global", "no manufacturing", "cheaper", "patch", "update", "no stock"]),
            MP("A drawback of digital distribution", ["platform cut", "piracy", "download size", "connection", "no resale", "competition", "store fees"]),
            MP("An advantage of physical distribution", ["collectable", "gift", "resale", "retail shelf", "no download", "tangible", "special edition"]),
            MP("A drawback of physical distribution", ["manufacturing", "stock", "shipping", "unsold", "slow", "cannot patch", "environmental"]),
            MP("Updating or patching is addressed", ["patch", "update", "day one", "fix after release", "cannot change the disc"]),
            MP("The audience or market is considered", ["audience", "players", "console", "PC", "collectors", "parents", "gift"]),
            MP("A clear recommendation is made", ["recommend", "should", "I would", "best option"]),
            MP("The recommendation is justified against the drawbacks raised", ["because", "therefore", "this addresses", "outweigh"])],
           "Digital distribution is the stronger default for a games studio. There is no manufacturing, no stock and no shipping, so the cost of reaching one more customer is effectively zero, the title is available globally the moment it launches, and the studio gets sales and play data it could never obtain from retail. Crucially, a digital title can be patched, which matters enormously for games because balance problems and bugs surface only when thousands of people play at once. The drawbacks are real: the store takes a substantial percentage of every sale, the game competes for visibility against thousands of others on the same storefront, a large download excludes players on slow or capped connections, and players own a licence rather than a copy they can lend or resell. Physical release answers some of those. A box on a shelf is itself advertising, it can be bought as a gift, which matters for a title aimed at younger players whose purchases are made by someone else, and it supports collector's editions that earn far more per unit than a digital copy. It also works for players with poor connections. Against that, discs cost money to press, distribute and warehouse, unsold stock is a loss, lead times mean the content is locked weeks before launch, and the disc almost always needs a day one patch anyway, which undercuts its main practical advantage. The recommendation is to launch digitally everywhere as the primary route, and to produce a limited physical edition aimed at collectors and the gift market rather than a mass retail print run. That keeps the economics and the patching flexibility of digital while capturing the shelf presence and the higher margin of physical, and it keeps the risk of unsold stock small, which is the drawback of physical distribution that would actually hurt a small studio.",
           command="Discuss"),
    ],
)

# ============================================================== R094 (NEA)

M_R094_IDENTITY = Topic(
    slug="visual-identity-and-digital-graphics",
    title="R094 TA1: Visual Identity and Planning",
    spec="R094 TA1 and TA2",
    icon="i-palette",
    minutes=26,
    exam_title="Check you could explain this",
    blurb="Interpreting the brief, researching, developing a visual identity and planning the graphic properly. Internally assessed, so this is about what the criteria reward.",
    fact="A brand identity is far more than a logo. It is the whole system of colour, type, imagery, tone and spacing that makes an organisation recognisable even when the logo is nowhere on the page.",
    sections=[
        Section("What visual identity is", """
**Visual identity** is the set of visual elements that make an organisation recognisable and that communicate what it stands for.

| Element | What it covers |
| **Logo** | The primary mark, plus any variations: stacked, horizontal, icon only, single colour |
| **Colour palette** | A primary colour, one or two secondaries, and a neutral range, defined as values |
| **Typography** | A heading face and a body face, with the sizes and weights used |
| **Imagery style** | The kind of photography or illustration, and how it is treated |
| **Tone of voice** | Formal, playful, premium, plain spoken |
| **Spacing and layout** | The grid, the margins, and the clear space kept around the logo |

### Logo types worth naming

- **Wordmark** — the name itself, styled. Google, Coca-Cola
- **Lettermark** — initials. BBC, IBM
- **Pictorial mark** — a recognisable object. Apple, Shell
- **Abstract mark** — a shape with no literal meaning. Nike, Pepsi
- **Mascot** — a character
- **Combination mark** — a symbol beside or above the name, which is the safest choice for a new brand because the symbol can later stand alone

!key A logo has to work at both extremes :: Legible as a favicon at 16 pixels, and sharp on the side of a van. If it only works at one size it is not finished, which is why detail is removed rather than added as a logo develops.
"""),
        Section("Interpreting the brief and researching", """
### Interpreting the brief

Write down, in your own words, what the brief actually requires:

- The **purpose** of the graphic
- The **audience**, in detail
- The **message** it has to carry
- The **content** that must appear: name, strapline, contact details, legal lines
- The **deliverables** and their formats and sizes
- The **constraints**: deadline, house style, print or screen, budget
- The **implicit** requirements the brief does not state

### Research that counts

| Type | What to do with it |
| **Competitor analysis** | Three or four direct competitors, analysed for colour, type and tone, with a note on what each is doing and what gap that leaves |
| **Sector conventions** | What the audience already expects from this kind of organisation |
| **Audience research** | Who they are, demographically and psychographically, and what they respond to |
| **Visual research** | Colour, type, texture, photographic style, from anywhere relevant |

The assessment rewards **analysis**, not collection. A screenshot with no comment is worth nothing; a screenshot with "this uses a cold blue and a geometric sans to look clinical, which suits a lab but would feel unwelcoming for a children's nursery" is worth a great deal.

### Ideas generation

1. **Mind map** to open the possibilities up
2. **Mood board**, annotated, to fix the look and feel with the client
3. **Thumbnail sketches**, at least six, quickly, before judging any of them
4. **Develop three distinct concepts**, genuinely different rather than three versions of one
5. **Choose one, and justify the choice** against the brief, the audience and the research

!warn One idea is the most expensive mistake in this unit :: Marks are explicitly available for exploring alternatives. A single polished concept with no alternatives caps the grade however good it is, and it also produces worse work, because the first idea is rarely the best one.
"""),
        Section("Planning the graphic", """
### The visualisation diagram

One per concept, annotated well enough that somebody else could produce the graphic without asking a question:

- **Canvas size and orientation**, in millimetres for print or pixels for screen
- **Every colour as a value**, `#02848B` or `C92 M26 Y25 K9`
- **Every font by name, weight and size**, "Poppins SemiBold 42pt"
- **Position of every element**, with measurements where they matter
- **Bleed and safe margins** for anything printed
- **Annotations explaining the intention**, not just labelling the parts

### The asset table

| Asset | Type | Source | Format | Dimensions | Licence |
| logo-mark | Vector | Own work | SVG | scalable | Own work |
| hero-photo | Raster | Unsplash | JPG | 4000 x 2667 | Unsplash licence, commercial use permitted |
| heading-font | Font | Google Fonts | WOFF2 | — | SIL Open Font Licence |

Every row completed, including fonts, because fonts are licensed software and a commercial project needs a licence that covers commercial use.

### Technical planning

- Decide **RGB or CMYK** now, from the destination, not at export
- Decide **vector or raster** per element: the logo and type vector, photographs raster
- Work out the **resolution** needed from the final physical size
- Plan the **file naming and versioning** before the first save

!grade What the top band looks like :: Every decision traced to the brief. "The palette is a deep teal with a warm cream, because the client is a family run bakery wanting to read as established rather than trendy, and the warm neutral keeps it from looking corporate the way a cool grey would." Taste is never a justification; the brief always is.
"""),
    ],
    keyterms=[
        ("Visual identity", "The system of colour, typography, imagery and tone that makes an organisation recognisable."),
        ("Wordmark", "A logo made from the organisation's name, styled distinctively."),
        ("Combination mark", "A logo pairing a symbol with the name, so the symbol can later stand alone."),
        ("Mood board", "An annotated collage establishing the intended look and feel."),
        ("Visualisation diagram", "An annotated plan of a static graphic, detailed enough to work from."),
        ("Asset table", "A record of every asset with its source, format, dimensions and licence."),
        ("Clear space", "The minimum empty margin kept around a logo in any layout."),
        ("House style", "The rules governing how a brand's fonts, colours and logo are used."),
    ],
    grade="""
+ Analyse research rather than collecting it; every example needs a comment on what it does and why
+ Produce at least three genuinely different concepts before choosing
+ Justify every choice against the brief, the audience or the research, never against taste
+ Put exact colour values and named fonts on the visualisation diagram
+ Complete the licence column for every asset, fonts included
+ Design the logo so it works at favicon size and in a single colour
""",
    mistakes=[
        "Justifying a design by personal preference instead of the brief.",
        "Presenting one concept, or three near identical versions of one concept.",
        "Collecting research with no analysis attached.",
        "Writing 'blue' and 'a bold font' on a visualisation diagram.",
        "Leaving the licence column incomplete, particularly for fonts.",
        "Designing a logo that only works large, with detail that disappears at small sizes.",
    ],
    quiz=[
        Q("What does visual identity include beyond the logo?",
          ["Colour palette, typography, imagery style and tone",
           "Only the logo at different sizes", "The client's contact details",
           "The file formats used"], 0,
          "It is the whole system that makes an organisation recognisable without the logo present."),
        Q("Which logo type is safest for a brand nobody has heard of yet?",
          ["Combination mark", "Abstract mark", "Lettermark", "Mascot"], 0,
          "The name teaches the audience who you are, and the symbol can stand alone once they know."),
        Q("What makes competitor research worth marks?",
          ["Analysis of what each competitor does and what gap it leaves",
           "The number of screenshots collected", "Listing competitors' names",
           "Copying the most successful design"], 0,
          "Collection is not research. The comment on each example is the assessed part."),
        Q("How should a colour be recorded on a visualisation diagram?",
          ["As an exact value such as #02848B", "As 'teal'",
           "As 'the same blue as the logo'", "Colour is decided later"], 0,
          "Someone else must be able to reproduce it exactly."),
        Q("Why must the licence of a font be recorded?",
          ["Fonts are licensed software and commercial use needs permission",
           "To record the file size", "Fonts have no licence",
           "To choose the point size"], 0,
          "Using a font without a commercial licence is the same kind of infringement as using an image."),
        Q("How many initial concepts should be developed?",
          ["At least three genuinely different ones", "One, developed fully",
           "Two very similar ones", "None, work straight in the software"], 0,
          "Exploring alternatives is explicitly rewarded and produces better final work."),
        Q("Why is detail removed as a logo develops?",
          ["So it stays legible at very small sizes",
           "To reduce the file size", "To make it cheaper to print",
           "Because simple logos are fashionable"], 0,
          "A logo has to survive being a favicon as well as being on a van."),
        Q("Which colour mode should be chosen at the start of a print project?",
          ["CMYK", "RGB", "It does not matter", "HSL"], 0,
          "Choosing it at the start means the designer sees the colours that will actually print."),
        Q("What is clear space in brand guidelines?",
          ["The minimum empty margin kept around the logo",
           "The white background of the logo", "Space left for a strapline",
           "The gap between letters"], 0,
          "It stops the logo being crowded by other elements and losing impact."),
        Q("What makes a justification score in the top band?",
          ["It links the decision to the brief, audience or research",
           "It describes the software used", "It says the design looks modern",
           "It explains how long the work took"], 0,
          "The mark is for the reasoning, and the reasoning has to come from the brief."),
    ],
    exam=[
        EQ("Explain why a mood board is produced before any design work begins.", 3,
           [MP("It gathers colours, images, type and textures capturing the intended feel", ["colours", "images", "fonts", "textures", "feel", "collect"]),
            MP("It establishes a shared understanding with the client", ["agree", "client", "direction", "shared", "same idea"]),
            MP("It is far cheaper to change than finished artwork", ["cheaper", "quicker", "easier to change", "early", "less work"])],
           "A mood board gathers colours, photographs, typefaces and textures that capture the feel the identity is aiming for, which gives something concrete to discuss about a quality that is very hard to describe in words. Its real purpose is to establish a shared understanding with the client before design begins, because a client who says modern and a designer who hears modern may have completely different pictures in mind. Resolving that disagreement over a mood board takes an afternoon; discovering it after two weeks of finished artwork means starting again.",
           command="Explain"),
        EQ("Describe **three** things that must appear on a visualisation diagram, and explain why each is needed.", 6,
           [MP("Dimensions and orientation", ["dimensions", "size", "canvas", "orientation", "mm", "pixels"]),
            MP("Why they are needed", ["final size", "resolution", "fit", "print", "produce it"]),
            MP("Exact colour values", ["hex", "CMYK", "#", "exact", "value"]),
            MP("Why they are needed", ["reproduce", "consistent", "same colour", "not guess", "print accurately"]),
            MP("Named fonts with sizes", ["font", "typeface", "name", "point", "size"]),
            MP("Why they are needed, or a fourth valid element", ["substitut", "not installed", "consistent", "position", "annotation"])],
           "The canvas dimensions and orientation must be stated, because every other decision depends on the final size: the resolution an image needs, whether a layout works in portrait, and how much space the text can occupy. Exact colour values must be given in hex or CMYK rather than colour names, so that anyone producing the graphic reproduces the same colour, and so a print version matches the screen version instead of shifting. Fonts must be named with their weights and sizes, because a diagram that says 'a bold font' leaves the choice to whoever builds it, and a font that is not installed will be silently substituted, which changes the design.",
           command="Describe"),
        EQ("A designer has been asked to create a visual identity for a new independent bookshop.\n\nJustify **three** decisions you would make about the identity, referring to the audience and purpose.", 6,
           [MP("A colour decision", ["colour", "palette", "warm", "green", "deep", "muted", "cream"]),
            MP("Justified by audience or purpose", ["readers", "independent", "not a chain", "welcoming", "established", "trust"]),
            MP("A typography decision", ["serif", "sans serif", "typeface", "font"]),
            MP("Justified by audience or purpose", ["books", "reading", "traditional", "authority", "legible", "character"]),
            MP("A logo or imagery decision", ["logo", "wordmark", "combination", "symbol", "illustration"]),
            MP("Justified, including practical use", ["signage", "bag", "stamp", "small", "one colour", "recognisable"])],
           "The palette would be a deep green with a warm cream and a single muted accent, because an independent bookshop is competing against chains on character rather than price, and warm, slightly muted colours read as established and welcoming where a bright primary palette would read as a discount retailer. The body typeface would be a serif, because the entire product the shop sells is set in serif type, so it carries an immediate association with reading and with authority, and it distinguishes the shop from the geometric sans serifs the chains use. The logo would be a combination mark, a simple pictorial symbol beside the shop's name, because nobody knows this shop yet and the name has to do the teaching; once it is recognised, the symbol alone can go on a stamp, a tote bag and a small shelf label, all of which need something that works in one colour at a few centimetres across.",
           command="Justify"),
    ],
)

M_R094_GRAPHICS = Topic(
    slug="creating-digital-graphics",
    title="R094 TA3: Creating and Reviewing Digital Graphics",
    spec="R094 TA3",
    icon="i-image",
    minutes=26,
    exam_title="Check you could explain this",
    blurb="The techniques the assessment expects to see evidenced, how to save and export properly, and how to write a review that actually scores.",
    fact="Boolean operations are how most logos are really built. A crescent moon is a circle with a second circle subtracted from it, and once you see that, half the logos on the high street come apart in front of you.",
    sections=[
        Section("Vector techniques", """
Vector software: Inkscape, Illustrator or Affinity Designer. This is where the logo and any scalable element is built.

| Technique | What it is for |
| **Shapes and paths** | The basic building blocks |
| **Node editing** | Moving, adding and removing points to shape a curve precisely |
| **Bezier curves** | Controlling a curve with handles rather than by eye |
| **Boolean operations** | Union, difference, intersection and exclusion, which is how most marks are constructed |
| **Align and distribute** | Making spacing exact rather than approximate |
| **Grouping and layers** | Keeping a complex drawing editable |
| **Strokes and fills** | Outline and interior, including gradients |
| **Convert text to paths** | So the file no longer depends on the font being installed |

### The four Boolean operations

- **Union** joins shapes into one
- **Difference** cuts the top shape out of the one beneath
- **Intersection** keeps only the overlap
- **Exclusion** keeps everything except the overlap

!key Convert text to paths before delivery, not before you are finished :: Once text is paths it cannot be edited as text, so keep an editable version as well. A printer without your font would otherwise substitute one and change the logo.
"""),
        Section("Raster techniques and exporting", """
Raster software: Photoshop, GIMP or Affinity Photo. This is where photographs are handled.

| Technique | Why it is the right way |
| **Layers** | Elements stay separate and editable |
| **Adjustment layers** | Colour and tone changes that can be altered or removed later |
| **Layer masks** | Hiding part of a layer without deleting it |
| **Selections** | Marquee, lasso, colour range, and refining an edge |
| **Crop and resize** | Resampling knowingly rather than by accident |
| **Levels and curves** | Correcting exposure and contrast properly |
| **Retouching** | Clone and healing tools, used sparingly |
| **Filters and effects** | Applied on their own layer, at a judged opacity |

**Non destructive editing** means the original pixels are never overwritten: adjustments live on their own layers and masks hide rather than delete. It is the difference between a file you can revise and a file you have to redo.

### Saving and exporting

| Keep | Why |
| The **layered working file** (.svg, .psd, .xcf, .afdesign) | It is the only version that can be meaningfully changed |
| **Every version**, numbered | So a rejected direction can be recovered |
| **Exports** per destination | Print, web and social each need their own |

A naming convention that sorts correctly, `bookshop-logo-v04-horizontal.svg`, and no file called "final".

### Testing the graphic

- View it at **100%** and at the **final physical size**, not just zoomed in
- Print a **proof** if it is going to print; screen colour lies
- Check the logo at **16 pixels** and in **one colour**
- Check **contrast** for any text on an image
- Open the exports on a **different machine**, which is how missing font problems are found
"""),
        Section("Reviewing the finished graphic", """
The review carries real marks, and it is where most work loses them by being too positive.

### What a review has to do

1. Compare the graphic against the **brief, point by point**. Quote the requirement, say whether it was met, and show where.
2. Report **feedback from others**: the client, a stakeholder, or people from the audience. Record what they said, including the criticism.
3. State honestly **what works and what does not**, with reasons.
4. Describe **specific improvements** and how each would be implemented.
5. Reflect on the **process**: what you would plan differently next time.

### The difference between the bands

| Weak review | Strong review |
| "I think it went well and the client liked it." | "The brief required the mark to work in one colour. It does, but at 16 pixels the gap between the two shapes closes up, so the favicon reads as a single blob. I would redraw the icon only version with the gap widened to twice the stroke weight." |
| "Everything worked as planned." | "The photo shoot overran because I had not booked the location for long enough, which cost a day of editing time. Next time I would schedule the shoot two days earlier than the plan requires." |

!warn A review with no criticism reads as a review that never happened :: Identifying a real weakness and explaining how you would fix it is evidence of understanding. Claiming everything was perfect is evidence of the opposite, and it is marked that way.
"""),
    ],
    keyterms=[
        ("Boolean operation", "Combining shapes using union, difference, intersection or exclusion."),
        ("Node editing", "Adjusting the individual points of a vector path to shape a curve."),
        ("Non destructive editing", "Editing with layers, masks and adjustment layers so original pixels are never overwritten."),
        ("Layer mask", "A greyscale layer that hides part of another layer without deleting it."),
        ("Adjustment layer", "A colour or tone change stored as its own editable layer."),
        ("Convert to paths", "Turning editable text into vector outlines so it no longer needs the font."),
        ("Proof", "A test print used to check colour and detail before a full run."),
        ("Working file", "The layered master file from which every export is produced."),
    ],
    grade="""
+ Work non destructively, so every change can be revised rather than redone
+ Evidence a genuine range of techniques, not one tool used repeatedly
+ Keep the layered master and export separately for each destination
+ Test the graphic at its real size, in one colour, and on another machine
+ Review against the brief point by point, with honest criticism
+ Give specific improvements and say how each would be made
""",
    mistakes=[
        "Editing pixels directly instead of using adjustment layers and masks.",
        "Delivering a logo as a JPG, with no vector master and no transparency.",
        "Judging a design only while zoomed in.",
        "Converting text to paths with no editable copy kept.",
        "Writing a review that claims everything succeeded.",
        "Giving improvements with no explanation of how they would be implemented.",
    ],
    quiz=[
        Q("Which Boolean operation cuts one shape out of another?",
          ["Difference", "Union", "Intersection", "Exclusion"], 0,
          "A crescent, a hole or a counter is usually made with difference."),
        Q("What is non destructive editing?",
          ["Using layers and masks so the original pixels are not overwritten",
           "Saving frequently", "Working only in vector software",
           "Backing up before editing"], 0,
          "It means any change can be adjusted or removed later."),
        Q("Why convert text to paths before sending a logo to a printer?",
          ["So the file does not depend on the font being installed",
           "To reduce the file size", "To keep the text editable",
           "To change the colour mode"], 0,
          "A missing font would otherwise be substituted and the logo would change."),
        Q("Which file should be kept as the master version of a logo?",
          ["The layered vector file", "A flattened JPG",
           "A PNG export", "A screenshot"], 0,
          "Every export comes from the master, which retains everything needed to make changes."),
        Q("What does a layer mask do?",
          ["Hides part of a layer without deleting it",
           "Locks a layer", "Merges two layers",
           "Changes a layer's colour"], 0,
          "Masking is reversible; deleting is not."),
        Q("At what size should a logo be checked?",
          ["At its smallest intended size as well as large",
           "Only at 100%", "Only zoomed in", "Only at print size"], 0,
          "Detail that works large often closes up at favicon size."),
        Q("Why open your exports on a different machine?",
          ["It reveals missing fonts and broken links",
           "It compresses the file", "It converts the colour mode",
           "It is required by the assessment"], 0,
          "Problems caused by assets only present on your own computer appear immediately."),
        Q("Which review comment would score most highly?",
          ["Naming a specific weakness and how it would be fixed",
           "Saying the client was happy", "Listing the software used",
           "Describing each step taken"], 0,
          "Honest, specific criticism with a solution is the evidence of understanding."),
        Q("Where should a filter effect be applied?",
          ["On its own layer, at a judged opacity",
           "Directly to the image layer", "To the whole file at export",
           "Before any other editing"], 0,
          "On its own layer it can be reduced or removed; applied directly it cannot."),
        Q("What is a proof?",
          ["A test print used to check colour and detail before a full run",
           "The final file", "A signed client approval",
           "The layered working file"], 0,
          "Screen colour is unreliable, so a proof is checked before committing to a print run."),
    ],
    exam=[
        EQ("Explain why a designer works non destructively when editing a photograph.", 3,
           [MP("Original pixels are not altered", ["original", "pixels", "not changed", "preserved", "intact"]),
            MP("Changes can be adjusted or removed later", ["adjust", "undo", "remove", "change later", "revise"]),
            MP("The consequence of destructive editing", ["start again", "cannot undo", "redo", "from the original", "lost"])],
           "Working non destructively means the edits live on their own layers, as adjustment layers and masks, rather than being baked into the image, so the original pixels are never overwritten. That matters because design is iterative: a client asking for the crop to be less tight or the colour to be warmer is a two minute change on a masked, layered file. If the same edits had been applied directly to the pixels and the file flattened, the only way to make that change is to go back to the original photograph and redo every step.",
           command="Explain"),
        EQ("Describe what should be included in a review of a finished digital graphic.", 4,
           [MP("Comparison against the brief or requirements", ["brief", "requirements", "against", "point by point", "met"]),
            MP("Feedback from the client, a stakeholder or the audience", ["feedback", "client", "stakeholder", "audience", "asked"]),
            MP("Honest identification of strengths and weaknesses", ["what works", "weakness", "strength", "honest", "did not work"]),
            MP("Specific improvements, with how they would be made", ["improve", "would change", "next time", "how", "redraw", "instead"])],
           "A review should compare the finished graphic against the brief requirement by requirement, saying for each one whether it was met and pointing to where in the work it was met. It should report feedback gathered from the client and from people in the target audience, including the criticism rather than only the praise. It should then state honestly what works and what does not, with reasons rather than opinions. Finally it should give specific improvements and say how each would be implemented, for instance redrawing the icon with a wider gap so it holds together at favicon size, rather than a general statement that the logo could be clearer.",
           command="Describe"),
        EQ("A student has produced a logo and delivered it only as a 600 pixel wide JPG.\n\nExplain **two** problems this will cause for the client.", 4,
           [MP("It cannot be enlarged without quality loss", ["pixelate", "blur", "quality", "enlarge", "scale", "raster"]),
            MP("Why that matters for a client", ["signage", "banner", "van", "print", "poster", "large"]),
            MP("JPG cannot store transparency", ["transparen", "white box", "background"]),
            MP("Why that matters for a client", ["coloured background", "photograph", "white square", "cannot place"])],
           "The first problem is scale. A JPG is a fixed grid of pixels, so at 600 pixels wide it can only be made smaller, not larger; the moment the client wants the logo on a banner, a van or a printed poster it will blur and show compression artefacts, and the only fix is to redraw it. A vector master such as an SVG would have scaled to any size without loss. The second problem is transparency, which JPG cannot store at all. The logo will therefore arrive with a solid white rectangle behind it, so it cannot be placed over a coloured background or a photograph without that box showing, which rules out most of the uses a logo exists for.",
           command="Explain"),
    ],
)

# ============================================================== R097 (NEA)

M_R097_PLAN = Topic(
    slug="interactive-digital-media",
    title="R097 TA1: Planning Interactive Digital Media",
    spec="R097 TA1 and TA2",
    icon="i-web",
    minutes=26,
    exam_title="Check you could explain this",
    blurb="Interactive means the user decides what happens, so you are not planning one experience but every route through it. Internally assessed.",
    fact="Interactive means the user controls what happens, and that single property changes everything about planning. You are not designing one path, you are designing every path somebody could take, including the ones you would never choose yourself.",
    sections=[
        Section("Types of interactive product and their structures", """
### What counts as interactive

Websites, apps, kiosks and exhibits, e-learning, interactive video, games, quizzes, virtual tours. The common property is that the user's choices change what happens next.

### Navigation structures

| Structure | Shape | Suits | Risk |
| **Linear** | One screen after another | A tutorial, a story, a quiz | Frustrating if the user wants to skip ahead |
| **Hierarchical** | Home, sections, sub-sections | Most websites | Content buried too deep |
| **Hub and spoke** | A centre with branches that return | Apps, kiosks, menus | The hub becomes crowded |
| **Networked** | Many screens linked many ways | Reference material, wikis | Users lose track of where they are |

Most real products mix them: a hierarchical site with a linear checkout inside it.

### The planning documents

| Document | Purpose |
| **Client brief interpretation** | Purpose, audience, message, content, constraints |
| **Mind map** | Exploring content and features before committing |
| **Mood board** | Agreeing look and feel |
| **Navigation diagram** | Every screen, every link. The most important document here |
| **Wireframes** | The layout of each distinct screen, without styling |
| **Storyboard** | Any video or animated sequence inside the product |
| **Script** | Narration, dialogue and on screen text |
| **Asset table** | Every asset, with source, format and licence |
| **Work plan** | Tasks, order, dependencies, milestones, contingency |
"""),
        Section("Navigation diagrams and wireframes", """
### Checking a navigation diagram

Every screen is a box, every link an arrow. Then test it:

1. Can every screen be **reached** from the entry point?
2. Does every screen have a route **back or onward**?
3. Are there **dead ends**, where the user is stuck?
4. Is anything too **deep**? More than three or four steps and people give up.
5. Is the structure **consistent**, so the user always knows where they are?

An **orphan screen** is one nothing links to. A **dead end** is one nothing links out of. Both are obvious on a diagram and invisible in a half built product.

### Wireframes

A wireframe shows placement and nothing else: boxes with a cross for images, grey bars for text, named rectangles for buttons. Leaving out colour and type is deliberate, because it keeps the review focused on structure rather than taste.

Wireframe **every distinct screen**: the home screen, a content screen, a form, a confirmation, and the error state. The error state is the one everybody forgets and users see most.

!key Annotate interactions, not just layout :: Write what each button does and which screen it leads to. A wireframe without that is a picture; with it, it is a specification.
"""),
        Section("Interface design and accessibility", """
### Principles that get credited

- **Consistency** — the same element looks and behaves the same everywhere
- **Feedback** — every action produces a visible response, so nobody taps twice
- **Clarity** — buttons say what they do; "Submit" is worse than "Send message"
- **Affordance** — things that can be tapped look tappable
- **Forgiveness** — mistakes can be undone and destructive actions confirm first
- **Efficiency** — the common task takes the fewest steps
- **Recognition over recall** — show the options rather than making people remember them

### Accessibility, which is both assessed and a legal duty

| Requirement | What it means in practice |
| **Contrast** | At least 4.5:1 for body text, 3:1 for large text |
| **Text size** | Resizable, and never below about 16 pixels for body text on screen |
| **Alternative text** | Every meaningful image described; decorative images marked as such |
| **Captions and transcripts** | For all video and audio |
| **Keyboard access** | Every control reachable and operable without a mouse |
| **Focus visible** | It is always clear which control is selected |
| **Not colour alone** | Meaning carried by text or shape as well as colour |
| **Tap targets** | Around 44 pixels minimum, within thumb reach on mobile |

### Planning the testing before building

Write the test plan as part of the planning, not afterwards. For each test: what is being tested, the data or action used, the expected result, and space for the actual result. Tests written after the build only ever test what already works.
"""),
    ],
    keyterms=[
        ("Interactive product", "A product in which the user's choices determine what happens next."),
        ("Navigation diagram", "A diagram of every screen in a product and the links between them."),
        ("Wireframe", "A layout plan of one screen showing placement without styling."),
        ("Dead end", "A screen the user cannot continue or return from."),
        ("Orphan screen", "A screen that nothing links to, so it can never be reached."),
        ("Hub and spoke", "A structure with a central screen and branches that return to it."),
        ("Affordance", "A visual cue showing that an element can be interacted with."),
        ("Feedback", "A visible response confirming to the user that an action registered."),
        ("Test plan", "A document written before building, listing each test, its data and its expected result."),
    ],
    grade="""
+ Produce a navigation diagram covering every screen, with no dead ends or orphans
+ Wireframe every distinct screen, including the error and confirmation states
+ Annotate each wireframe with what every control does and where it leads
+ Plan accessibility in, rather than retrofitting it
+ Write the test plan before building, including tests you expect to fail
+ Justify structural choices against the audience and the purpose
""",
    mistakes=[
        "Producing a navigation diagram with dead ends or unreachable screens.",
        "Wireframing only the home screen.",
        "Forgetting the error and confirmation screens, which users see most.",
        "Leaving accessibility until after the build, when it means rework.",
        "Writing the test plan after building, so it only tests what already works.",
        "Choosing a structure by habit rather than by what the content needs.",
    ],
    quiz=[
        Q("Which document is most important when planning an interactive product?",
          ["The navigation diagram", "The storyboard", "The mood board", "The script"], 0,
          "It shows every screen and link, which is the structure everything else rests on."),
        Q("What is an orphan screen?",
          ["A screen nothing links to, so it can never be reached",
           "A screen with no content", "A screen with no way back",
           "The final screen in a sequence"], 0,
          "A dead end has no way out; an orphan has no way in."),
        Q("Which structure suits a step by step tutorial?",
          ["Linear", "Networked", "Hub and spoke", "Hierarchical"], 0,
          "Each screen follows the previous one in a fixed order."),
        Q("What should a wireframe deliberately exclude?",
          ["Colour, fonts and final images", "Button positions",
           "Navigation elements", "Headings"], 0,
          "Leaving styling out keeps the review focused on structure."),
        Q("What is the minimum contrast ratio for body text?",
          ["4.5:1", "2:1", "3:1", "7:1"], 0,
          "4.5:1 for normal text, 3:1 for large text, under the WCAG AA standard."),
        Q("Why must every control be reachable by keyboard?",
          ["Many users cannot use a mouse or touchscreen",
           "Keyboards are faster", "It is a design convention",
           "It reduces loading time"], 0,
          "Keyboard access is a core accessibility requirement and a legal expectation."),
        Q("What does affordance mean in interface design?",
          ["Things that can be interacted with look like they can",
           "The product is affordable", "The layout adapts to the screen",
           "Users can undo mistakes"], 0,
          "A button that looks like plain text will not be pressed."),
        Q("Which screen do designers most often forget to wireframe?",
          ["The error state", "The home screen", "The menu", "The about page"], 0,
          "Users see error screens constantly, and an unplanned one is where they give up."),
        Q("Why write the test plan before building?",
          ["Otherwise it only tests what already works",
           "It is quicker", "It is required by law",
           "Testing cannot be done afterwards"], 0,
          "A test plan written afterwards is shaped by the build rather than by the requirements."),
        Q("A product needs three or four taps to reach its main content. What is the problem?",
          ["It is buried too deep and users will give up",
           "There are too many screens", "The structure is linear",
           "There is no feedback"], 0,
          "Depth is a measurable usability problem and it is visible on a navigation diagram."),
    ],
    exam=[
        EQ("Explain why a navigation diagram is produced before building an interactive product.", 3,
           [MP("It shows every screen and how they connect", ["every screen", "connected", "links", "structure"]),
            MP("It allows checking that every screen is reachable with a route back", ["reachable", "route back", "dead end", "stuck", "orphan"]),
            MP("Structural problems are far cheaper to fix on a diagram", ["cheaper", "easier", "before building", "rebuild", "quicker"])],
           "A navigation diagram maps every screen as a box and shows with arrows which screen each link leads to, so the whole structure can be seen at once. That makes it possible to verify that every screen can be reached, that there is always a route back or onward so nobody becomes stuck at a dead end, and that nothing important is buried so deep that users abandon it. Fixing those problems on a diagram takes minutes; discovering after the product is built that a whole section is unreachable means rebuilding the navigation and often restructuring several screens with content already in them.",
           command="Explain"),
        EQ("Describe **four** accessibility requirements an interactive product should meet.", 4,
           [MP("Sufficient colour contrast", ["contrast", "4.5", "legible"]),
            MP("Alternative text for images", ["alt text", "alternative text", "screen reader", "described"]),
            MP("Captions or transcripts for audio and video", ["caption", "subtitle", "transcript"]),
            MP("Keyboard operability, or not relying on colour alone", ["keyboard", "without a mouse", "focus", "colour alone", "tab"])],
           "Text must meet a contrast ratio of at least 4.5:1 against its background, so it stays readable for users with low vision. Every meaningful image needs alternative text, so a screen reader can describe it rather than announcing an unlabelled graphic. All video and audio needs captions or a transcript, which serves deaf users and also the many people using the product with the sound off. Every control must be operable by keyboard alone, with a visible focus indicator, because a large number of users cannot use a mouse or a touchscreen accurately.",
           command="Describe"),
        EQ("A museum wants an interactive touchscreen exhibit with a menu of six topics, each leading to text, images and a short video.\n\nJustify the navigation structure you would choose and explain how you would plan the screens.", 6,
           [MP("A suitable structure is named", ["hub and spoke", "hub", "hierarchical"]),
            MP("Justified for a public kiosk", ["returns to the menu", "next visitor", "short visit", "no training", "always get back", "queue"]),
            MP("The navigation diagram is described", ["navigation diagram", "every screen", "arrows", "links"]),
            MP("Dead ends and depth are addressed", ["dead end", "route back", "shallow", "two taps", "depth"]),
            MP("Wireframes for each distinct screen", ["wireframe", "each screen", "topic screen", "menu screen"]),
            MP("A kiosk specific consideration", ["timeout", "reset", "idle", "no keyboard", "tap targets", "standing", "children", "height"])],
           "A hub and spoke structure is the right choice. The menu is the hub, each of the six topics is a spoke, and every topic screen returns directly to the menu, which means the deepest the visitor ever goes is two taps and they can always get back in one. That suits a public kiosk specifically: visitors arrive with no instructions, stay for a minute or two, and the next person needs to find the exhibit in its starting state. A hierarchical structure with sub-sections would bury content and leave people stranded; a linear structure would force them through topics they do not care about. I would plan it with a navigation diagram showing the attract screen, the menu, the six topic screens and the video on each, with arrows in both directions, which makes it easy to confirm there are no dead ends and no screen more than two steps from the menu. Then I would wireframe each distinct screen rather than just the menu: the attract loop, the menu, a topic screen with text, image and video, and the video playing state with its own controls. Being a kiosk adds requirements that belong in the plan rather than being discovered later: an idle timeout that returns to the attract screen after a minute of no input, tap targets large enough for a visitor who is standing and not looking closely, no reliance on a keyboard, and a layout that works for both a child and an adult at a fixed screen height.",
           command="Justify"),
    ],
)

M_R097_MAKE = Topic(
    slug="creating-and-testing-interactive-media",
    title="R097 TA3: Creating, Testing and Reviewing",
    spec="R097 TA3 and TA4",
    icon="i-check",
    minutes=24,
    exam_title="Check you could explain this",
    blurb="Building in the right order, evidencing a real range of skills, testing against the plan and writing an honest review.",
    fact="A usability study only needs about five participants to find most of the problems in a product. The sixth person mostly rediscovers what the first five already showed you, which is why professional testing rounds are small and repeated.",
    sections=[
        Section("Building in the right order", """
1. **Structure first.** Create every screen and wire up the navigation with placeholder content. The product should be clickable end to end before anything looks finished.
2. **Content next.** Drop in the real text, images, audio and video.
3. **Styling last.** Apply the look once the structure has stopped moving.
4. **Test throughout.** Not as a final stage.

Styling before the structure is settled means restyling everything when it changes, which is where most of the wasted time in this unit goes.

### File and asset discipline

- A consistent naming convention, lower case, no spaces
- Folders by asset type: `images/`, `audio/`, `video/`, `css/`
- **Relative paths**, never absolute ones, or nothing works on another machine
- Keep every **source file** as well as the exports
- Back up in a second location

### Skills the assessment wants evidenced

| Area | What to show |
| **Combining media** | Text, image, audio, video and animation working together |
| **Navigation** | Working links across the whole product, no dead ends |
| **Interactivity** | Buttons, menus, rollovers, forms, quizzes, show and hide |
| **Video editing** | Trimming, cuts, transitions, titles, colour correction |
| **Audio editing** | Trimming, level balancing, fades, music mixed under narration |
| **Optimisation** | Assets compressed so the product loads quickly without visible loss |
| **Accessibility** | Alt text, captions, contrast, keyboard access, actually implemented |

!key Breadth is the point :: Six different techniques used competently evidence more than one technique used brilliantly, because the criteria ask for a range.
"""),
        Section("Testing", """
Test against the **plan**, not against what you happened to build.

| Test type | What it checks |
| **Functionality** | Every button, link and interactive element does what it should |
| **Navigation** | Every screen reachable, every route back working |
| **Content** | Spelling, accuracy, and everything the brief specified being present |
| **Media** | Video and audio play, at a sensible level, on every screen |
| **Compatibility** | Different browsers, devices and screen sizes |
| **Accessibility** | Keyboard only, screen reader, contrast, text resized to 200% |
| **Performance** | Load time on a slow connection |
| **Usability** | A real user completing a task without help |

### Recording a test properly

| # | Test | Data or action | Expected | Actual | Action taken |
| 1 | Home to Topic 3 | Tap Topic 3 | Topic 3 screen opens | As expected | None |
| 2 | Back from video | Tap Back during playback | Returns to topic, audio stops | Audio kept playing | Added a stop on unload; retested, passes |

The **expected result has to be written before the test is run**, or there is nothing to compare against. Record failures and the fix, because a test log with no failures is not believable.

### Usability testing

Give a real user a **task**, not a tour: "find out what time the museum opens on a Sunday and book two tickets." Then stay quiet and write down every hesitation, wrong tap and backtrack. The hesitations are the findings. Five users will surface most of the problems.

!warn You cannot usability test your own product :: You know where everything is, so you cannot experience being lost in it. Every evaluation that consists of the maker using their own product scores badly, and deserves to.
"""),
        Section("Reviewing and improving", """
### What the review must contain

1. **Against the brief**, requirement by requirement, with evidence of where each is met.
2. **Stakeholder and user feedback**, quoted, including the criticism.
3. **Honest strengths and weaknesses**, with reasons.
4. **Specific improvements**, each with how it would be implemented and what effect it would have.
5. **Reflection on the process**: what you would plan differently, and why.

### Turning a weak review into a strong one

| Weak | Strong |
| "The navigation worked well." | "Four of five testers reached the booking screen in under three taps. The fifth looked for a 'Book' button in the top right, where the convention puts it, and did not find it in the menu; I would add a persistent booking button to the header." |
| "I would add more content." | "Each topic has text and one image. Two testers asked for sources, so I would add a short references panel under each topic, collapsed by default so it does not compete with the main text." |
| "It all went to plan." | "I styled the topic screens before the navigation was finished, so adding the video screen meant restyling three screens. Next time I would leave all styling until the structure is signed off." |

!grade Evidence every claim :: "It is easy to use" is an opinion. "Five of six testers completed the task without help, and the one who failed was looking for a search function that does not exist" is evidence. The review is marked on evidence.
"""),
    ],
    keyterms=[
        ("Functionality testing", "Checking that every interactive element behaves as intended."),
        ("Usability testing", "Observing a real user attempting a task and recording where they struggle."),
        ("Compatibility testing", "Checking the product on different browsers, devices and screen sizes."),
        ("Test plan", "A document listing each test, the data used and the expected result, written before testing."),
        ("Optimisation", "Reducing asset file sizes so a product loads quickly without visible quality loss."),
        ("Relative path", "A file path given relative to the current file, so the product works on any machine."),
        ("Iteration", "Improving a product through repeated cycles of building, testing and refining."),
    ],
    grade="""
+ Build the structure first, style last, and test throughout
+ Evidence a genuine range of techniques across text, image, audio, video and interaction
+ Record the expected result before each test, and log the failures with their fixes
+ Watch real users attempt a task rather than demonstrating the product yourself
+ Quote user feedback, criticism included, in the review
+ Give specific improvements with the method and the expected effect
""",
    mistakes=[
        "Styling before the structure is complete, which means restyling it all later.",
        "Using absolute file paths, so nothing works on another machine.",
        "Testing only what already works.",
        "Writing the expected result after seeing the actual result.",
        "Evaluating by using the product yourself instead of watching someone else.",
        "A test log with no failures in it, which no assessor believes.",
        "Reviews that praise everything and improve nothing.",
    ],
    quiz=[
        Q("What should be built first in an interactive product?",
          ["The structure and navigation, with placeholder content",
           "The visual styling", "The video content", "The home screen design"], 0,
          "Styling an unfinished structure means restyling it when the structure changes."),
        Q("Why use relative file paths rather than absolute ones?",
          ["The product then works on any machine",
           "They load faster", "They are shorter",
           "Absolute paths are not allowed"], 0,
          "An absolute path points at your own computer and breaks everywhere else."),
        Q("What must be recorded before a test is run?",
          ["The expected result", "The actual result",
           "The time taken", "The tester's name"], 0,
          "Without an expected result there is nothing to compare the outcome against."),
        Q("What does usability testing involve?",
          ["Watching a real user attempt a task and recording the difficulties",
           "Checking every link works", "Testing in several browsers",
           "Proofreading the content"], 0,
          "It finds problems the maker cannot see, because the maker already knows the product."),
        Q("Roughly how many users are needed to find most usability problems?",
          ["About five", "One", "Twenty", "Fifty"], 0,
          "Five users surface the majority of issues; after that findings start repeating."),
        Q("Why is a test log with no failures a problem?",
          ["It suggests only the working parts were tested",
           "Failures are not allowed", "It is too short",
           "Tests must always fail once"], 0,
          "Genuine testing finds faults, and recording the fix is evidence of the process."),
        Q("What does optimising assets achieve?",
          ["Faster loading with no visible quality loss",
           "Better colour accuracy", "Easier editing",
           "Smaller screen sizes"], 0,
          "Oversized assets make an interactive product slow, which loses users fastest."),
        Q("Which test checks the product on different devices and screen sizes?",
          ["Compatibility testing", "Functionality testing",
           "Usability testing", "Content testing"], 0,
          "It is the test that catches a layout that only works on the machine it was built on."),
        Q("What makes an improvement suggestion score well?",
          ["It says how it would be implemented and what effect it would have",
           "It lists more content", "It is ambitious",
           "It blames the time available"], 0,
          "Specificity is the assessed quality: the method and the expected effect."),
        Q("Which review statement is evidence rather than opinion?",
          ["Five of six testers completed the task unaided",
           "The product is easy to use", "The design looks professional",
           "Everything worked as planned"], 0,
          "A measured outcome can be checked; an opinion cannot."),
    ],
    exam=[
        EQ("Explain why an interactive product should be tested by someone other than its creator.", 3,
           [MP("The creator already knows how it works", ["already knows", "built it", "familiar", "knows where"]),
            MP("So they cannot experience being confused by it", ["cannot", "biased", "assumes", "blind to", "obvious to them"]),
            MP("A new user reveals real problems", ["hesitate", "struggle", "real user", "finds", "unexpected", "where they go wrong"])],
           "The creator has an unavoidable advantage: they built the navigation, so they know where everything is and cannot experience the moment of not knowing. That means they are blind to exactly the problems testing is meant to find, and will unconsciously take the route they designed rather than the route a stranger would try. Someone from the audience, given a task and left alone, hesitates in places the creator never considered, taps things that are not buttons and looks for features that are not there, and every one of those moments is a finding that can be fixed.",
           command="Explain"),
        EQ("Describe **four** types of testing that should be carried out on an interactive product.", 4,
           [MP("Functionality testing", ["functionality", "every button", "links work"]),
            MP("Navigation testing, or content testing", ["navigation", "reachable", "dead end", "content", "spelling"]),
            MP("Compatibility testing", ["compatibility", "browsers", "devices", "screen sizes"]),
            MP("Usability or accessibility testing", ["usability", "real user", "accessibility", "keyboard", "screen reader", "contrast"])],
           "Functionality testing checks that every button, link and interactive element does what it is supposed to do. Navigation testing confirms that every screen can be reached and that there is always a route back, so no user becomes stuck. Compatibility testing runs the product on different browsers, devices and screen sizes, which catches layouts that only work on the machine it was built on. Usability and accessibility testing put it in front of real users, including keyboard only and screen reader use, to find where people struggle rather than where the code fails.",
           command="Describe"),
        EQ("A student's review of their interactive product says: \"Everything worked well and my friends liked it. If I had more time I would add more content.\"\n\nExplain **three** ways this review could be improved.", 6,
           [MP("Compare against the brief point by point", ["brief", "requirements", "each requirement", "against"]),
            MP("Why that matters", ["evidence", "met", "assessed", "shows"]),
            MP("Gather feedback from the target audience, not friends, and quote it", ["target audience", "not friends", "stakeholder", "quote", "specific feedback"]),
            MP("Why that matters", ["representative", "biased", "honest", "real users"]),
            MP("Identify specific weaknesses honestly", ["specific", "weakness", "what did not work", "honest"]),
            MP("Give improvements with the method and effect", ["how", "would implement", "effect", "instead of", "specific improvement"])],
           "First, it should work through the brief requirement by requirement, quoting each one, saying whether it was met and pointing to the screen where it was met, because the review is assessed on evidence and a general statement that everything worked proves nothing. Second, the feedback should come from people in the target audience rather than from friends, who are both unrepresentative and reluctant to criticise, and it should be quoted: what the tester was asked to do, what they actually did, and what they said. Third, the improvements have to be specific and come with a method and an expected effect. 'More content' is not a plan; 'two of five testers looked for a search function, so I would add a search field to the header, which would let users reach a topic directly instead of scanning the menu' identifies the evidence, the change and the benefit. Underneath all three is the same point: a review that finds nothing wrong reads as a review that was never carried out, and honest criticism of your own work is the thing being credited.",
           command="Explain"),
    ],
)

# ================================================================== COURSE

COURSE = Course(
    slug="ks4/imedia",
    seo="OCR J834 Creative iMedia",
    title="Creative iMedia",
    short="Creative iMedia",
    stage="KS4",
    board="OCR",
    code="J834",
    goal="Distinction star",
    icon="i-palette",
    accent="var(--purple)",
    blurb="OCR Cambridge National in Creative iMedia J834. R093, the written paper, covered topic area by topic area with quizzes and exam-style questions, plus what the R094 and R097 assessment criteria actually reward.",
    intro="",
    journey=[
        ("Learn R093 properly, because it is the only exam",
         "The coursework is marked on what you produce. R093 is a 70 mark written paper and it is the part most students under prepare for. Know the job roles, the documents, the formats and the legislation cold.", ""),
        ("Know exactly which document goes with which product",
         "Visualisation diagram for a static product, storyboard for moving image, wireframe and navigation diagram for interactive. Confusing these is the single most common error in this unit.", ""),
        ("Answer the command word you were given",
         "Identify and state want a name. Describe wants detail. Explain wants a reason. Discuss and evaluate want a judgement. Writing a description where the paper asked for an explanation loses half the marks.", ""),
        ("Justify everything against the brief",
         "The difference between a pass and a distinction is almost never technical skill. It is whether every decision is explained in terms of the client, the audience and the purpose.", ""),
        ("Get the licences right from the start",
         "Every asset needs a recorded source and licence. Fixing this at the end means rebuilding, and using an unlicensed image can invalidate the work entirely.", ""),
        ("Test with a real person and write down what they struggle with",
         "You cannot evaluate your own product fairly, because you already know how it works. Watching someone else use it produces the evidence the review needs.", ""),
    ],
    units=[
        Unit("r093", "R093: Creative iMedia in the Media Industry",
             "The written paper: 70 marks, 1 hour 15 minutes. The media industry, the factors that shape product design, pre-production planning, and distribution.",
             [M_SECTORS, M_ROLES, M_CLIENT, M_AUDIENCE, M_RESEARCH, M_STYLE,
              M_DOCS, M_PLAN, M_LEGAL, M_FORMATS, M_DIST],
             icon="i-video", term="Exam unit"),
        Unit("r094", "R094: Visual Identity and Digital Graphics",
             "Internally assessed. Developing a visual identity from a client brief, planning it, creating the graphics and reviewing them.",
             [M_R094_IDENTITY, M_R094_GRAPHICS], icon="i-palette", term="Coursework"),
        Unit("r097", "R097: Interactive Digital Media",
             "Internally assessed. Planning, creating, testing and reviewing an interactive digital media product.",
             [M_R097_PLAN, M_R097_MAKE], icon="i-web", term="Coursework"),
    ],
)
