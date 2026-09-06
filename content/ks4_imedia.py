"""OCR Level 1/Level 2 Cambridge National in Creative iMedia J834.

R093 is the examined unit and is covered in full with quizzes and exam-style
questions. R094 and R097 are internally assessed, so those topics focus on
what the assessment criteria actually reward.
"""
from mskbuild.models import Topic, Section, Unit, Course, Q, EQ, MP

M_TA1 = Topic(
    slug="the-media-industry",
    title="R093 TA1: The Media Industry",
    spec="R093 TA1",
    icon="i-video",
    minutes=26,
    blurb="The sectors of the media industry, the products each creates, and the job roles you must be able to name and describe.",
    fact="A single feature film credits roll can list over 2000 people. Almost none of them are the ones the audience could name, and most of the work happens long before or long after anything is filmed.",
    sections=[
        Section("Sectors and products", """
### The sectors

| Sector | Products |
| **Television and film** | Programmes, films, adverts, trailers, streaming content |
| **Publishing** | Books, magazines, newspapers, e-books, digital editions |
| **Advertising and marketing** | Campaigns, banner adverts, social media content, branding |
| **Music** | Recordings, streaming, music videos, promotional artwork |
| **Video games** | Console, PC and mobile games, in game assets |
| **Web and app development** | Websites, mobile apps, web applications |
| **Photography** | Commercial, editorial, product and event photography |
| **Animation and visual effects** | 2D and 3D animation, motion graphics, VFX |

### Types of product

- **Audio visual**: film, television, animation, video, streaming
- **Print based**: magazines, books, posters, packaging, leaflets
- **Digital and interactive**: websites, apps, games, interactive multimedia
- **Audio**: podcasts, radio, music, sound effects

### Purpose

Every product exists to do at least one of these, and questions frequently ask you to identify which.

- **Entertain**
- **Inform**
- **Educate**
- **Advertise or promote**
- **Persuade or influence**
- **Provide a service**

A single product often has several purposes at once. A charity advert entertains enough to hold attention, informs about the cause and persuades the viewer to donate.
"""),
        Section("Job roles", """
### Pre-production roles

| Role | Responsibility |
| **Client** | Commissions the work and defines what is needed |
| **Producer** | Manages the whole project, the budget and the schedule |
| **Project manager** | Coordinates people, deadlines and resources |
| **Scriptwriter** | Writes the script or copy |
| **Storyboard artist** | Draws the planned shots to show how the product will look |
| **Concept artist** | Produces early visual ideas for characters, locations and style |

### Production roles

| Role | Responsibility |
| **Director** | Makes the creative decisions and directs performers and crew |
| **Camera operator** | Operates the camera to capture the shots required |
| **Sound engineer** | Records and balances audio |
| **Lighting technician** | Sets up lighting to achieve the intended look |
| **Graphic designer** | Creates visual assets, layouts and branding |
| **Web developer** | Builds websites and web applications |
| **Games developer** | Designs and programmes games |
| **Animator** | Creates moving images from drawings or models |
| **Photographer** | Takes the photographs required |

### Post-production roles

| Role | Responsibility |
| **Video editor** | Assembles footage into the finished sequence |
| **Sound editor** | Edits and mixes the audio, adds effects and music |
| **VFX artist** | Adds visual effects and compositing |
| **Quality assurance tester** | Tests the product and reports faults |

### Working practices

- **Full time employee**: a permanent contract, regular salary, holiday and sick pay, and job security, in exchange for less flexibility
- **Freelance**: works project by project, choosing what to take on and setting their own rates, with no guaranteed income, no paid holiday and responsibility for their own tax and equipment
- **Contract**: employed for a fixed period, often for one production

!key Why freelancing dominates media :: Productions need a large team for a short time and then do not need them at all. Hiring everyone permanently would be impossible, which is why so much of the industry works freelance.
"""),
    ],
    keyterms=[
        ("Media sector", "A division of the media industry, such as television and film or publishing."),
        ("Audio visual product", "A product combining moving images and sound, such as a film or advert."),
        ("Interactive product", "A product the user controls, such as a website, app or game."),
        ("Client", "The person or organisation commissioning the work and defining what is required."),
        ("Producer", "The person managing the whole project including budget and schedule."),
        ("Freelance", "Working project by project rather than as a permanent employee."),
        ("Post-production", "The stage after filming or creation, covering editing, effects and finishing."),
    ],
    grade="""
+ Match a job role to the correct stage: pre-production, production or post-production
+ Describe what a role actually does, not just its title
+ Identify all the purposes of a product, since most have more than one
+ Give both an advantage and a disadvantage when comparing freelance and employed work
+ Use the correct sector name rather than a general description
""",
    mistakes=[
        "Confusing the producer with the director. The producer manages the project, the director makes the creative decisions.",
        "Placing editing in production. It is post-production.",
        "Giving only one purpose when a product clearly has several.",
        "Describing freelancing as simply better or worse, rather than a trade off between flexibility and security.",
    ],
    quiz=[
        Q("Who manages the overall budget and schedule of a production?",
          ["The producer", "The director", "The editor", "The camera operator"], 0,
          "The producer manages the project. The director makes the creative decisions."),
        Q("Which stage does video editing belong to?",
          ["Post-production", "Pre-production", "Production", "Distribution"], 0,
          "Post-production covers everything after the material has been captured."),
        Q("What is the main advantage of freelance work?",
          ["Flexibility to choose projects and set your own rates",
           "Guaranteed regular income", "Paid holiday and sick leave", "A permanent contract"], 0,
          "The other three are advantages of permanent employment, which freelancers give up."),
        Q("Which role draws the planned shots to show how a product will look?",
          ["Storyboard artist", "Concept artist", "Graphic designer", "Director"], 0,
          "The storyboard shows the sequence of shots. A concept artist produces early visual ideas for style."),
        Q("A charity advert asking viewers to donate has which primary purpose?",
          ["To persuade", "To educate only", "To entertain only", "To provide a service"], 0,
          "It also informs and holds attention, but persuasion to donate is the reason it exists."),
        Q("Which is an interactive media product?",
          ["A mobile app", "A printed magazine", "A radio broadcast", "A film poster"], 0,
          "Interactive products respond to what the user does rather than being consumed passively."),
        Q("Who is responsible for testing a product and reporting faults?",
          ["Quality assurance tester", "Producer", "Sound engineer", "Concept artist"], 0,
          "QA is a post-production role, and in games development it is a substantial part of the team."),
        Q("Why does the media industry rely heavily on freelancers?",
          ["Productions need large teams for short periods and then do not need them",
           "Freelancers are more skilled", "It is required by law",
           "Permanent staff cannot work on films"], 0,
          "The workload is project shaped, so a permanent workforce of that size would be unaffordable."),
        Q("Which sector produces branding and campaign material?",
          ["Advertising and marketing", "Publishing", "Music", "Photography"], 0,
          "Branding, campaigns and promotional content sit in advertising and marketing."),
        Q("Who defines what is required at the start of a project?",
          ["The client", "The editor", "The animator", "The QA tester"], 0,
          "The client commissions the work and sets out their requirements in the brief."),
    ],
    exam=[
        EQ("Identify two job roles involved in the pre-production stage and describe what each does.", 4, [
            MP("First valid pre-production role named", ["producer", "scriptwriter", "storyboard", "concept artist", "project manager", "client"]),
            MP("Description of what the first role does", ["manages", "writes", "draws", "plans", "coordinates", "responsible for"]),
            MP("Second valid pre-production role named", ["producer", "scriptwriter", "storyboard", "concept artist", "project manager", "client"]),
            MP("Description of what the second role does", ["manages", "writes", "draws", "plans", "coordinates", "responsible for"]),
        ], "A scriptwriter works in pre-production, writing the script or copy that sets out the dialogue, narration and action for the product, which everything else is then planned around. A storyboard artist also works in pre-production, drawing the planned shots in sequence so that the client and the crew can see how the finished product will look and how it will move from one shot to the next before any filming takes place.",
           command="Identify"),
        EQ("Explain two differences between working as a freelancer and being a full time employee in the media industry.", 4, [
            MP("A freelancer works project by project with no guaranteed income", ["project by project", "no guaranteed", "irregular", "between jobs"]),
            MP("An employee has a permanent contract and a regular salary", ["permanent", "regular salary", "contract", "steady"]),
            MP("A freelancer chooses which projects to take and when to work", ["chooses", "flexibility", "own hours", "select"]),
            MP("An employee receives benefits such as paid holiday and sick pay, which a freelancer does not", ["holiday", "sick pay", "pension", "benefits", "no paid"]),
        ], "The first difference is security of income. A full time employee has a permanent contract and receives a regular salary whether or not there is work to do at that moment, whereas a freelancer is paid per project and may have periods with no work and therefore no income at all, and must find their own next contract. The second difference is flexibility and benefits. A freelancer chooses which projects to accept, negotiates their own rate and organises their own working hours, but receives no paid holiday, no sick pay and no pension contributions, and is responsible for their own tax, insurance and equipment. An employee gives up much of that flexibility in exchange for those benefits and for greater stability.",
           command="Explain"),
        EQ("State three different purposes that a media product might have.", 3, [
            MP("To entertain", ["entertain", "enjoyment", "amuse"]),
            MP("To inform or educate", ["inform", "educate", "teach", "explain"]),
            MP("To advertise, promote or persuade", ["advertise", "promote", "persuade", "sell", "influence"]),
        ], "A media product may exist to entertain its audience, for example a comedy series or a game. It may exist to inform or educate, for example a documentary or an instructional video. It may exist to advertise or persuade, for example a commercial or a charity campaign encouraging viewers to donate. Many products serve more than one of these at once, since an advert must entertain sufficiently to hold attention while persuading.",
           command="State"),
        EQ("Describe the role of the producer and explain how it differs from the role of the director.", 4, [
            MP("The producer manages the overall project", ["manages", "overall", "in charge of the project", "oversees"]),
            MP("Including the budget, schedule and hiring of the team", ["budget", "schedule", "hiring", "resources", "money"]),
            MP("The director makes the creative decisions", ["creative", "artistic", "vision", "how it looks"]),
            MP("The director works with performers and crew during production", ["performers", "actors", "crew", "directs", "on set"]),
        ], "The producer is responsible for managing the project as a whole. They secure and control the budget, set and maintain the schedule, hire the key personnel and take responsibility for the production being delivered on time and within its financial limits. Their focus is organisational and commercial. The director is responsible for the creative side, deciding how the product should look and feel, interpreting the script, choosing how each scene is staged and shot, and directing the performers and the crew during production. In short, the producer decides what can be afforded and when it must be finished, while the director decides what it should actually be.",
           command="Describe"),
        EQ("A company is producing a mobile game. Identify three job roles that would be needed and explain why each is required.", 6, [
            MP("Names a role such as games developer or programmer", ["games developer", "programmer", "developer", "coder"]),
            MP("Explains that they build and programme the game itself", ["build", "programme", "code", "creates the game", "implements"]),
            MP("Names a role such as graphic designer or concept artist", ["graphic designer", "concept artist", "artist", "animator"]),
            MP("Explains that they create the visual assets and style", ["visual", "assets", "graphics", "characters", "look", "style"]),
            MP("Names a role such as quality assurance tester or sound engineer", ["quality assurance", "tester", "qa", "sound engineer", "audio", "project manager"]),
            MP("Explains why that role matters, such as finding faults before release", ["faults", "bugs", "testing", "sound", "audio", "coordinates", "before release"]),
        ], "A games developer or programmer is essential because they write the code that makes the game function, implementing the rules, the controls, the scoring and everything the player interacts with. A graphic designer or concept artist is needed to create the visual assets, including the characters, backgrounds, interface elements and overall visual style, since a mobile game competes for attention largely on how it looks in a store listing. A quality assurance tester is needed to play the game systematically on a range of devices and screen sizes, finding faults, crashes and balance problems and reporting them so they can be fixed before release, because a mobile game that crashes on launch receives poor reviews immediately and rarely recovers. A sound engineer and a project manager would also be required on any significant production, the first to create and balance the music and effects, and the second to coordinate the team against the deadline.",
           command="Identify"),
    ],
)

M_TA2 = Topic(
    slug="factors-influencing-product-design",
    title="R093 TA2: Factors Influencing Product Design",
    spec="R093 TA2",
    icon="i-palette",
    minutes=28,
    blurb="Target audience, client requirements, style, content and layout, and the media codes that make a product communicate what it intends.",
    fact="The colour blue is used by the overwhelming majority of banks and technology companies because it is associated with trust and stability. Choosing it is not creative timidity, it is a deliberate use of colour theory.",
    sections=[
        Section("Audience and client", """
### Segmenting an audience

| Category | Examples |
| **Age** | Under 12, teenagers, 18 to 25, over 60 |
| **Gender** | Where genuinely relevant to the product |
| **Location** | Local, national, international, urban, rural |
| **Income** | Which affects price point and where the product is placed |
| **Interests** | Sport, gaming, music, fashion, technology |
| **Ethnicity and culture** | Which affects language, imagery and what is appropriate |
| **Occupation and education** | Which affects the vocabulary and level of detail used |
| **Accessibility needs** | Visual, hearing, motor or cognitive requirements |

### How the audience changes the design

- A product for young children needs large simple visuals, few words, bright colour and instant clarity
- A product for professionals can assume expertise and prioritise density of information and speed of use
- An international audience requires care with language, symbols, colour meaning and cultural references

### Client requirements

The **client brief** sets out what the client needs. It typically covers the purpose, the target audience, the deadline, the budget, the required formats, the brand guidelines to follow and any content that must be included.

Requirements divide into:

- **Explicit**: stated directly in the brief, such as a 30 second duration
- **Implicit**: not stated but expected, such as complying with copyright law and matching the client's existing brand

!warn Implicit requirements are examined :: A brief may not say the work must be original and legally usable, but delivering something containing unlicensed images is a failure. Being able to identify implicit requirements is worth marks.
"""),
        Section("Style, content, layout and media codes", """
### Style

The overall look and feel: colour palette, typography, imagery, tone of voice and use of space. Style must suit both the purpose and the audience. A funeral director and a children's party company should not look similar.

### Content

What is actually included: text, images, video, audio, interactive elements. Content must be appropriate, accurate, legal and sufficient for the purpose, and no more than the audience will actually read or watch.

### Layout

How elements are arranged. Key principles:

- **Alignment**: elements line up, which is the fastest way to make a design look professional
- **White space**: empty space that gives the eye rest and makes the important thing stand out
- **Visual hierarchy**: size, weight, colour and position guide the eye to what matters first
- **Balance**: symmetrical for formality and stability, asymmetrical for energy and movement
- **Proximity**: related items grouped together, unrelated items separated
- **Consistency**: the same treatment for the same kind of element throughout

The **rule of thirds** divides a frame into a three by three grid and places key elements on the lines or intersections, which usually produces a more engaging composition than centring everything.

### Media codes

**Media codes** are the techniques used to create meaning.

**Technical codes**: camera angles, shot types, lighting, editing and sound.

- A **low angle** makes a subject look powerful, a **high angle** makes it look small or vulnerable
- A **close up** creates intimacy and shows emotion, a **wide shot** establishes place and context
- **High key lighting** is bright and even, suiting comedy and advertising. **Low key lighting** is dark with strong shadow, suiting drama, horror and mystery
- Fast cutting creates energy and tension. Long takes create calm or unease

**Symbolic codes**: colour, objects, setting, clothing and body language.

| Colour | Common association |
| Red | Danger, passion, urgency, excitement |
| Blue | Trust, calm, stability, professionalism |
| Green | Nature, health, growth, safety |
| Yellow | Optimism, warning, energy |
| Black | Luxury, sophistication, formality, threat |
| White | Purity, simplicity, space, cleanliness |
| Purple | Luxury, creativity, royalty |

!warn Colour meaning is cultural :: White signifies purity in Britain and mourning in parts of East Asia. For an international product this matters, and saying so earns a higher mark.

**Written codes**: the words themselves, the font and how text is presented. A serif font reads as traditional and authoritative, a sans serif as modern and clean, and a display font as informal or playful.
"""),
    ],
    keyterms=[
        ("Target audience", "The specific group of people a product is designed for."),
        ("Demographics", "Measurable characteristics of an audience such as age, location and income."),
        ("Client brief", "The document setting out what the client requires from the product."),
        ("Explicit requirement", "A requirement stated directly in the brief."),
        ("Implicit requirement", "A requirement not stated but expected, such as legal compliance."),
        ("Visual hierarchy", "Using size, colour and position to guide the eye to the most important element first."),
        ("White space", "Deliberately empty space in a design, giving clarity and emphasis."),
        ("Rule of thirds", "Dividing a frame into thirds and placing key elements on the lines or intersections."),
        ("Media codes", "Techniques used to create meaning, including technical, symbolic and written codes."),
        ("Low key lighting", "Dark lighting with strong shadow, used to create drama or tension."),
    ],
    grade="""
+ Describe the audience specifically, naming the demographic characteristics that matter here
+ Link every design decision to the audience or the purpose, never to personal preference
+ Identify implicit requirements as well as the explicit ones in a brief
+ Name the media code and say what meaning it creates in this particular product
+ Note that colour associations are cultural whenever the audience is international
""",
    mistakes=[
        "Describing the target audience as everyone. A product designed for everyone appeals strongly to nobody.",
        "Justifying a design choice by saying it looks nice rather than by reference to the audience.",
        "Listing colour meanings without applying them to the product in the question.",
        "Confusing high key and low key lighting.",
        "Missing the implicit requirements in a brief.",
    ],
    quiz=[
        Q("What is a target audience?",
          ["The specific group of people a product is designed for",
           "Everyone who might see the product", "The client who commissioned it",
           "The team producing it"], 0,
          "Being specific is the point. A product aimed at everyone appeals strongly to nobody."),
        Q("Which lighting style suits a horror trailer?",
          ["Low key, dark with strong shadows", "High key, bright and even",
           "Natural daylight only", "Backlighting only"], 0,
          "Deep shadow conceals information, which creates tension and unease."),
        Q("What does a low camera angle usually suggest about a subject?",
          ["Power and dominance", "Weakness and vulnerability", "Confusion", "Neutrality"], 0,
          "Looking up at something makes it appear larger and more imposing."),
        Q("Which colour is most commonly associated with trust and stability?",
          ["Blue", "Red", "Yellow", "Orange"], 0,
          "This is why banks, insurers and technology companies use it so heavily."),
        Q("What is white space in a design?",
          ["Deliberately empty space that gives clarity and emphasis",
           "Space that must be filled with content", "The background colour",
           "The margin required for printing"], 0,
          "It is a design element in its own right, not wasted space."),
        Q("What is an implicit requirement?",
          ["One that is expected but not stated in the brief",
           "One stated directly in the brief", "One added after the deadline",
           "One the client cannot afford"], 0,
          "Complying with copyright and matching existing brand guidelines are typical examples."),
        Q("What does the rule of thirds suggest?",
          ["Placing key elements on the lines or intersections of a three by three grid",
           "Using exactly three colours", "Dividing content into three sections",
           "Showing three items in every shot"], 0,
          "Off centre composition usually reads as more dynamic and engaging than centring everything."),
        Q("Why should colour meaning be considered carefully for an international product?",
          ["Colour associations differ between cultures", "Some colours cannot be printed",
           "International audiences prefer bright colours", "Colour costs more to reproduce"], 0,
          "White signifies purity in Britain and mourning in parts of East Asia, for example."),
        Q("What does visual hierarchy achieve?",
          ["It guides the eye to the most important element first",
           "It makes every element the same size", "It removes all colour",
           "It aligns the text to the left"], 0,
          "Size, weight, colour and position are the tools used to establish it."),
        Q("A product aimed at children under seven should use:",
          ["Large simple visuals, bright colour and very little text",
           "Dense text with detailed explanation", "A muted professional palette",
           "Small controls to fit more on screen"], 0,
          "Young children read slowly or not at all and have limited fine motor control."),
    ],
    exam=[
        EQ("Explain why identifying the target audience is important when designing a media product.", 4, [
            MP("The audience determines the style and tone that will appeal", ["style", "tone", "appeal", "look", "suit"]),
            MP("It determines the language and level of detail used", ["language", "vocabulary", "detail", "reading", "wording"]),
            MP("It determines the content and imagery that is appropriate", ["content", "imagery", "appropriate", "suitable", "images"]),
            MP("Without it the product may fail to engage anyone", ["fail", "not engage", "no one", "ineffective", "miss"]),
        ], "Identifying the target audience is important because almost every design decision depends on who the product is for. The style and tone must appeal to that group, so a product for teenagers uses very different colour, typography and pacing from one aimed at retired professionals. The language and level of detail must match their vocabulary and expertise, since text that is too complex loses them and text that is too simple feels patronising. The content and imagery must be appropriate and relevant to their interests and culture, and must avoid anything that would offend or exclude them. Without a clearly identified audience the designer is guessing, and a product designed to appeal to everyone typically appeals strongly to nobody because every choice has been compromised.",
           command="Explain"),
        EQ("Describe two media codes that could be used in a trailer for a horror film and explain the effect of each.", 4, [
            MP("Names a technical code such as low key lighting", ["low key", "lighting", "dark", "shadow"]),
            MP("Explains that it conceals information and creates tension", ["conceals", "hides", "tension", "unease", "cannot see", "fear"]),
            MP("Names a second code such as fast editing, close ups or sound", ["fast cutting", "editing", "close up", "sound", "music", "silence"]),
            MP("Explains the effect of the second code", ["tension", "panic", "startle", "emotion", "unsettling", "atmosphere"]),
        ], "Low key lighting would be used, meaning a dark image with strong shadows and high contrast. Its effect is to conceal much of what is in the frame, so the audience cannot see what is there, and the imagination fills the gap far more effectively than anything shown could, which creates sustained unease. Fast paced editing towards the end of the trailer would also be used, with shots cut increasingly short. Its effect is to give the audience less and less time to process each image, which raises the sense of panic and urgency and prevents them settling, and cutting abruptly to silence or black after that acceleration produces a very strong final impact.",
           command="Describe"),
        EQ("A client brief asks for a poster advertising a music festival for 16 to 25 year olds. Explain three design decisions you would make and justify each.", 6, [
            MP("A decision about colour and its justification", ["colour", "bright", "bold", "vibrant", "palette"]),
            MP("Justifies the colour choice against the audience or purpose", ["energy", "audience", "young", "stand out", "excitement", "eye catching"]),
            MP("A decision about typography and its justification", ["font", "typography", "typeface", "bold", "display"]),
            MP("Justifies the typography choice", ["modern", "readable", "at a distance", "young", "energetic", "informal"]),
            MP("A decision about layout or imagery and its justification", ["layout", "image", "photograph", "hierarchy", "space"]),
            MP("Justifies that decision, for example ensuring key information is seen first", ["hierarchy", "seen first", "essential information", "date", "line up", "glance"]),
        ], "First, I would use a bright, high contrast colour palette, for example a strong gradient in warm colours against a dark background. This suits the audience because a festival is associated with energy and excitement rather than calm, and it also serves a practical purpose: the poster will be seen on a crowded noticeboard or in a shop window and has to compete for attention from several metres away. Second, I would use a bold sans serif or display typeface for the festival name and headline acts, with a clean sans serif for the details. A heavy display face reads as contemporary and energetic rather than formal, which matches the audience, and it remains legible at a distance where a light serif face would disappear. Third, I would establish a clear visual hierarchy, making the festival name largest, the headline acts second, and the date, location and ticket information smaller but unmissable and grouped together at the bottom. This matters because a poster is glanced at for a second or two, and if the viewer does not absorb the name and the date in that time the poster has failed regardless of how attractive it is. Alignment and generous white space around the key information keep it readable rather than cluttered.",
           command="Explain"),
        EQ("Explain the difference between an explicit and an implicit client requirement, giving an example of each.", 4, [
            MP("An explicit requirement is stated directly in the brief", ["stated", "directly", "written", "specified"]),
            MP("Gives an example such as a duration, format or deadline", ["30 seconds", "duration", "format", "deadline", "size", "colour"]),
            MP("An implicit requirement is expected but not stated", ["not stated", "assumed", "expected", "unwritten", "understood"]),
            MP("Gives an example such as legal compliance or matching existing branding", ["copyright", "legal", "brand", "guidelines", "original", "accessible"]),
        ], "An explicit requirement is one the client has written into the brief, so there is no doubt about it. An example would be a specification that the advert must be exactly thirty seconds long and delivered as an MP4 file by a stated date. An implicit requirement is one the client has not written down but would certainly expect, and failing to meet it would mean the work is unacceptable even though nothing in the brief was breached. Examples include that all images and music used must be legally licensed or original, that the product must follow the client's existing brand colours and logo usage, and that it must be accessible to users with visual impairments. Identifying implicit requirements is an important professional skill, because a client rarely thinks to state things they assume everybody knows.",
           command="Explain"),
        EQ("Explain how layout affects how successfully a media product communicates its message.", 4, [
            MP("Visual hierarchy determines what the viewer notices first", ["hierarchy", "first", "notice", "draws the eye", "order"]),
            MP("Alignment and consistency make a design look professional and easy to follow", ["alignment", "aligned", "consistent", "professional", "tidy"]),
            MP("White space gives emphasis and prevents the design feeling cluttered", ["white space", "space", "cluttered", "emphasis", "breathing"]),
            MP("Proximity groups related information so it is understood together", ["proximity", "grouped", "together", "related", "near"]),
        ], "Layout determines the order in which a viewer takes information in, which decides whether the message is received at all. Visual hierarchy, created through size, weight, colour and position, controls what is noticed first, so the most important element must be the most prominent or the viewer may absorb something secondary and move on. Alignment and consistency matter because elements that line up and are treated the same way throughout read as deliberate and professional, while inconsistent placement makes a product look careless and undermines trust in its content. White space prevents the design feeling crowded and gives emphasis to what surrounds it, since an element with space around it stands out far more than one packed against others. Proximity groups related information together and separates unrelated information, so a date, time and venue placed as a block are understood as belonging together, whereas scattering them forces the viewer to reassemble them mentally and many simply will not.",
           command="Explain"),
    ],
)

M_TA3 = Topic(
    slug="pre-production-planning",
    title="R093 TA3: Pre-Production Planning",
    spec="R093 TA3",
    icon="i-pen",
    minutes=30,
    blurb="Every pre-production document you must be able to name, describe and produce, plus work planning, legislation and file management.",
    fact="A visualisation diagram and a storyboard are not the same thing, and confusing them is one of the most common errors in this unit. A visualisation shows one static design. A storyboard shows a sequence of moving shots.",
    sections=[
        Section("Pre-production documents", """
| Document | What it is | Used for |
| **Mood board** | A collage of images, colours, fonts and textures capturing the intended feel | Establishing style with the client before work begins |
| **Mind map** | A diagram branching outwards from a central idea | Generating and organising ideas quickly |
| **Visualisation diagram** | A hand drawn sketch of a **static** product such as a poster or a magazine page, annotated with colours, fonts and dimensions | Showing the client what a still image product will look like |
| **Storyboard** | A sequence of frames showing shots in order, annotated with shot type, camera movement, duration, dialogue and sound | Planning **moving image** products |
| **Script** | The written dialogue, narration and action | Film, video, animation, radio |
| **Wireframe** | A basic outline of a screen layout showing where each element goes, without styling | Planning websites, apps and interactive products |
| **Navigation diagram** | A diagram showing how screens or pages connect | Planning the structure and user journey of an interactive product |
| **Assets table** | A list of every asset needed, with its source, format, size, licence and status | Tracking what must be created or obtained |
| **Work plan** | Tasks, durations, dependencies, milestones and deadlines | Managing time and resources |

!key The three most confused documents :: A **visualisation diagram** is one static design. A **storyboard** is a sequence of moving shots. A **wireframe** is a screen layout for an interactive product. Learn which product type each belongs to.

### What a storyboard must include

- Shot number and a sketch of the frame
- **Shot type**: extreme long shot, long shot, mid shot, close up, extreme close up
- **Camera angle**: high, low, eye level, birds eye
- **Camera movement**: pan, tilt, zoom, tracking, static
- **Duration** of the shot
- **Dialogue, sound effects and music**
- **Transition** to the next shot: cut, fade, dissolve, wipe
- Lighting and any additional notes
"""),
        Section("Work planning, legislation and file management", """
### Work plans

A work plan lists every task with its start date, duration, who is responsible, what it depends on and the milestone it contributes to. A **Gantt chart** shows this visually, with time along the horizontal axis and a bar for each task, so overlapping work and the critical path are immediately visible.

**Contingency** is time deliberately built in for things going wrong, and a plan without it fails the first time anything is late.

### Legislation

- **Copyright, Designs and Patents Act 1988.** Protects the work of creators. You may not use someone else's image, music or footage without permission. **Royalty free** means you pay once and may use it under stated conditions. **Creative Commons** licences grant use in advance under conditions, usually including attribution. **Public domain** means the copyright has expired.
- **Data Protection Act 2018.** Governs how personal data is collected, stored and used.
- **Model release form.** Written permission from a recognisable person appearing in a product, required before their image can be used commercially.
- **Property release form.** Permission from the owner of a recognisable private property or artwork appearing in the product.
- **Certification and classification.** The BBFC classifies films and PEGI classifies games, so content must be appropriate to the intended rating.
- **Health and safety.** Risk assessments must be produced before a shoot, identifying hazards, who is at risk and the control measures in place.

!warn Using an image from a search engine is copyright infringement :: This appears in exam questions and in coursework. The answer is always to use your own material, properly licensed stock, or Creative Commons content with correct attribution.

### File formats

| Format | Type | Characteristics |
| JPG | Image, lossy | Small files, good for photographs, no transparency |
| PNG | Image, lossless | Supports transparency, larger files, good for graphics and logos |
| GIF | Image, lossless | 256 colours, supports simple animation |
| SVG | Image, vector | Scales to any size with no quality loss |
| TIFF | Image, lossless | Very high quality, very large, used in print |
| MP3 | Audio, lossy | Small files, standard for distribution |
| WAV | Audio, lossless | Uncompressed, very high quality, large |
| MP4 | Video, lossy | Widely compatible, good compression |
| MOV | Video | High quality, larger files |
| PDF | Document | Preserves layout across devices |

### File management

- **Naming conventions**: descriptive, consistent and versioned, such as `festival-poster-v3-final.psd`
- **Folder structures**: organised by project, then by asset type
- **Version control**: keeping earlier versions so you can go back
- **Backup**: at least two copies, one of them in a different physical location or in the cloud
"""),
    ],
    keyterms=[
        ("Mood board", "A collage of images, colours and fonts capturing the intended feel of a product."),
        ("Visualisation diagram", "An annotated sketch showing how a static product such as a poster will look."),
        ("Storyboard", "A sequence of annotated frames planning the shots of a moving image product."),
        ("Wireframe", "A basic outline of a screen layout, showing placement without styling."),
        ("Navigation diagram", "A diagram showing how the screens or pages of an interactive product connect."),
        ("Assets table", "A list of every asset required, with its source, format, licence and status."),
        ("Gantt chart", "A chart showing tasks as bars against time, making overlaps and deadlines visible."),
        ("Contingency", "Extra time built into a plan to absorb delays."),
        ("Model release form", "Written permission from a recognisable person for their image to be used."),
        ("Royalty free", "A licence allowing repeated use after a single payment, under stated conditions."),
        ("Creative Commons", "A licence granting use in advance under stated conditions, usually including attribution."),
    ],
    grade="""
+ Match each document to the correct product type, especially visualisation against storyboard against wireframe
+ Include every required element when describing a storyboard: shot type, angle, movement, duration, sound and transition
+ Justify a file format by the property that matters, such as PNG for transparency
+ Name the specific legislation or release form rather than saying it is against the rules
+ Explain contingency as planned time for things going wrong, not as spare time
""",
    mistakes=[
        "Confusing a visualisation diagram with a storyboard. Visualisation is static, storyboard is a moving sequence.",
        "Producing a storyboard with only sketches and no annotation of shot type, duration or sound.",
        "Saying an image from a search engine can be used if it is credited. Attribution does not create permission.",
        "Choosing JPG for a logo needing a transparent background. JPG does not support transparency.",
        "Producing a work plan with no contingency time.",
    ],
    quiz=[
        Q("Which document plans the shots of a moving image product?",
          ["Storyboard", "Visualisation diagram", "Wireframe", "Mood board"], 0,
          "A storyboard shows the sequence of shots. A visualisation shows one static design."),
        Q("Which document shows the layout of a screen in an interactive product?",
          ["Wireframe", "Storyboard", "Mind map", "Assets table"], 0,
          "Wireframes show placement without styling, so discussion stays on structure and flow."),
        Q("Which file format supports transparency?",
          ["PNG", "JPG", "MP3", "WAV"], 0,
          "PNG is lossless and supports an alpha channel, which is why logos are supplied as PNG or SVG."),
        Q("What is a model release form used for?",
          ["Obtaining written permission from a recognisable person to use their image",
           "Booking equipment", "Confirming a deadline", "Licensing music"], 0,
          "Without it a recognisable person's image cannot lawfully be used commercially."),
        Q("What does royalty free mean?",
          ["You pay once and may use the asset repeatedly under stated conditions",
           "The asset is completely free with no conditions",
           "The asset has no copyright", "You must pay each time it is used"], 0,
          "Free refers to the absence of ongoing royalties, not to the absence of a price or conditions."),
        Q("What does a Gantt chart show?",
          ["Tasks as bars against time, showing overlaps and deadlines",
           "The structure of a website", "The colours used in a design",
           "Every asset in a project"], 0,
          "It makes dependencies and the critical path visible at a glance."),
        Q("Why should contingency time be included in a work plan?",
          ["To absorb delays when something takes longer than expected",
           "To make the project appear longer", "Because clients require it",
           "To allow for extra features"], 0,
          "A plan with no slack fails the first time anything at all goes wrong."),
        Q("Which format is most suitable for a logo that must scale to any size?",
          ["SVG", "JPG", "GIF", "MP3"], 0,
          "SVG stores shapes mathematically, so it is redrawn at any size with no loss of quality."),
        Q("What must be produced before a shoot to identify hazards?",
          ["A risk assessment", "A mood board", "An assets table", "A navigation diagram"], 0,
          "It identifies hazards, who is at risk and the control measures put in place."),
        Q("What should an assets table record for each asset?",
          ["Its source, format, licence and current status",
           "Only its file name", "The client's contact details", "The shot type"], 0,
          "The licence column is what evidences that everything used is legally cleared."),
    ],
    exam=[
        EQ("State the difference between a visualisation diagram and a storyboard.", 2, [
            MP("A visualisation diagram shows the design of a single static product", ["static", "single", "still", "one image", "poster"]),
            MP("A storyboard shows a sequence of shots for a moving image product", ["sequence", "shots", "moving image", "video", "order"]),
        ], "A visualisation diagram is an annotated sketch showing how a single static product will look, such as a poster, a magazine cover or a book jacket, including its colours, fonts, images and dimensions. A storyboard is a sequence of frames showing the shots of a moving image product in order, with each frame annotated with details such as the shot type, camera movement, duration and accompanying sound.",
           command="State"),
        EQ("Describe four pieces of information that should be included on a storyboard.", 4, [
            MP("Shot type such as close up or long shot", ["shot type", "close up", "long shot", "mid shot", "wide"]),
            MP("Camera angle and movement", ["angle", "movement", "pan", "tilt", "zoom", "tracking", "high", "low"]),
            MP("Duration of the shot", ["duration", "length", "timing", "seconds", "how long"]),
            MP("Sound, dialogue or music, and the transition to the next shot", ["sound", "dialogue", "music", "transition", "cut", "fade"]),
        ], "Each frame of a storyboard should state the shot type, such as a close up or a long shot, so the crew knows how much of the scene is in frame. It should give the camera angle and any camera movement, for example a low angle with a slow pan to the right, since these carry meaning as well as showing what to film. It should give the duration of the shot in seconds, so that the total running time can be planned and the pacing controlled. It should also record the dialogue, sound effects or music accompanying the shot, and the transition into the next frame, such as a straight cut or a fade, since transitions strongly affect how a sequence feels.",
           command="Describe"),
        EQ("A student wants to use a photograph found through a search engine in a poster for a client. Explain why this is a problem and describe two acceptable alternatives.", 5, [
            MP("The photograph is protected by copyright", ["copyright", "protected", "owned"]),
            MP("Using it without permission breaches the Copyright, Designs and Patents Act 1988", ["permission", "copyright designs and patents", "1988", "illegal", "infringement"]),
            MP("The client could face legal action or be required to withdraw the work", ["legal action", "sued", "withdraw", "fine", "damages"]),
            MP("First alternative such as taking their own photograph", ["own photograph", "take it themselves", "create", "original"]),
            MP("Second alternative such as licensed stock or Creative Commons with attribution", ["stock", "royalty free", "creative commons", "licensed", "attribution"]),
        ], "A photograph found through a search engine belongs to whoever created it and is protected by copyright automatically from the moment it was taken. Using it in a client's poster without permission infringes the Copyright, Designs and Patents Act 1988, and because the poster is a commercial product the consequences are real: the copyright holder can demand payment, require the poster to be withdrawn and destroyed, or take legal action for damages, and the client would suffer both the cost and the reputational damage. Crediting the photographer does not fix this, because attribution is not the same as permission. The first acceptable alternative is for the student to take the photograph themselves, which gives the client clear ownership, and to obtain a model release form if any recognisable person appears in it. The second is to use a properly licensed image, either purchased from a stock library under a licence that permits commercial use, or sourced from a Creative Commons repository under a licence that allows commercial use, with the attribution the licence requires provided exactly as specified.",
           command="Explain"),
        EQ("Explain why a work plan should include contingency time.", 3, [
            MP("Tasks frequently take longer than estimated", ["longer", "overrun", "delayed", "underestimated"]),
            MP("Unexpected problems occur such as illness, equipment failure or client changes", ["illness", "equipment", "failure", "client changes", "unexpected", "problems"]),
            MP("Without contingency any delay pushes back the final deadline", ["deadline", "pushed back", "missed", "late", "knock on"]),
        ], "A work plan should include contingency time because estimates are rarely exact and tasks routinely take longer than expected, particularly creative tasks where the amount of revision needed cannot be known in advance. Unexpected problems also occur on almost every project: equipment fails, a location becomes unavailable, someone is ill, or the client asks for a change part way through. If every task in the plan is scheduled back to back with no slack, then any one of these delays pushes back every subsequent task and the final deadline is missed. Building contingency in at sensible points, particularly before major milestones, allows the plan to absorb ordinary problems without the delivery date being affected.",
           command="Explain"),
        EQ("A client needs a logo that will be used on a website with a coloured background and also printed on a large banner. Recommend suitable file formats and justify your choice.", 5, [
            MP("Recommends SVG for the master or scalable version", ["svg", "vector", "scalable"]),
            MP("Because a vector can be enlarged to banner size with no loss of quality", ["no loss", "any size", "banner", "sharp", "enlarged"]),
            MP("Recommends PNG for use on the website", ["png"]),
            MP("Because PNG supports transparency so the logo sits on any background colour", ["transparency", "transparent", "background", "alpha"]),
            MP("Explains why JPG would be unsuitable", ["jpg", "no transparency", "white box", "lossy", "artefacts"]),
        ], "The master version of the logo should be an SVG, which is a vector format storing the design as mathematical shapes rather than pixels. This means it can be scaled to any size, from a favicon to a banner several metres wide, and redrawn perfectly sharp at every size, which a fixed resolution image could not do. For use on the website a PNG export would also be supplied, because PNG is a lossless format that supports transparency, so the logo can be placed on the coloured background and the area around the letterforms will show that background through rather than sitting in a rectangle. A JPG would be unsuitable for either use. It does not support transparency, so the logo would appear inside a white box against the coloured background, and it is a lossy format, so the sharp edges of a logo would show visible compression artefacts, which is particularly noticeable at large print sizes.",
           command="Recommend"),
    ],
)

M_TA4 = Topic(
    slug="distribution-considerations",
    title="R093 TA4: Distribution Considerations",
    spec="R093 TA4",
    icon="i-layers",
    minutes=24,
    blurb="Properties of media file formats, compression, and the distribution platforms with the considerations each brings.",
    fact="A film released to cinemas, streaming, television and physical disc needs a different master for each, because the resolution, colour space, audio configuration and file format required by each platform are all different.",
    sections=[
        Section("File properties and compression", """
### Image properties

- **Resolution**, the pixel dimensions. Higher means more detail and a larger file. Print typically needs 300 dots per inch, screen typically 72 to 150.
- **Colour depth**, the bits per pixel. 24 bit gives over 16 million colours.
- **Colour mode**: **RGB** for anything displayed on a screen, **CMYK** for anything printed, since printing uses inks rather than light. A design created in RGB will shift in colour when printed unless converted.
- **Transparency**, supported by PNG, GIF and SVG but not by JPG.

### Audio and video properties

- **Sample rate**, samples per second. CD quality is 44,100 Hz.
- **Bit depth**, bits per sample. Higher gives greater dynamic range.
- **Bit rate**, data per second. Higher gives better quality and a larger file.
- **Frame rate**, frames per second. 24 for film, 25 or 30 for television, 60 for smooth motion and games.
- **Aspect ratio**, the ratio of width to height. 16:9 for widescreen, 9:16 for vertical mobile video, 1:1 for square social posts.

### Compression

**Lossy** permanently discards data, giving much smaller files with some quality loss that cannot be reversed. Used by JPG, MP3 and MP4.

**Lossless** reduces size without discarding anything, so the original is recovered exactly. Used by PNG, GIF and WAV.

The decision is always the same: how much does quality matter here, and how much does file size matter? Streaming to millions of users makes size decisive, so lossy is correct. Archiving a master copy makes quality decisive, so lossless is correct.

!key Keep the master lossless :: Work in a lossless format throughout production and export to lossy only at the final stage. Editing a lossy file repeatedly compounds the quality loss with every save.
"""),
        Section("Platforms and considerations", """
### Distribution platforms

| Platform | Considerations |
| **Streaming** | Adaptive bit rate for varying connections, platform specific encoding, requires a connection |
| **Social media** | Each platform has its own aspect ratio, duration limit and file size cap. Vertical video for mobile first platforms |
| **Website download** | File size affects load time and bandwidth cost. Consider users on mobile data |
| **Physical media** | Disc capacity, replication cost, no updates possible after pressing |
| **Broadcast television** | Strict technical standards for resolution, frame rate, audio levels and captions |
| **Cinema** | Very high resolution, specific colour space, DCP format |
| **Print** | CMYK, 300 dpi, bleed area, and a PDF that embeds fonts |

### Cross platform considerations

- **Accessibility**: subtitles and captions for those with hearing impairments, audio description for those with visual impairments, and sufficient colour contrast
- **Device and screen size**: a design that works on a desktop monitor may be unusable on a phone
- **Bandwidth**: users on limited mobile data will abandon a large file
- **Regional requirements**: language, classification and legal differences between territories
- **Version control**: exporting the correct version for each platform and tracking which is which

### Choosing formats for distribution

| Purpose | Format | Reason |
| Photograph on a web page | JPG | Small file, no transparency needed |
| Logo on a coloured background | PNG or SVG | Transparency, and SVG scales without loss |
| Print poster | PDF in CMYK at 300 dpi | Preserves layout, embeds fonts, correct colour for print |
| Video for social media | MP4 (H.264) | Universally supported with good compression |
| Master audio recording | WAV | Lossless, so no quality is lost before final export |
| Podcast for download | MP3 | Small enough for mobile data, quality is sufficient for speech |
"""),
    ],
    keyterms=[
        ("Resolution", "The pixel dimensions of an image, determining detail and file size."),
        ("DPI", "Dots per inch, the print resolution. 300 dpi is the usual standard for print."),
        ("RGB", "The colour mode used for screens, mixing red, green and blue light."),
        ("CMYK", "The colour mode used for print, mixing cyan, magenta, yellow and black ink."),
        ("Bit rate", "The amount of data per second in an audio or video file, affecting quality and size."),
        ("Frame rate", "The number of frames displayed per second in a video."),
        ("Aspect ratio", "The ratio of width to height of an image or video."),
        ("Adaptive bit rate", "Streaming that adjusts quality automatically to suit the viewer's connection speed."),
        ("Bleed", "Extra image area beyond the trim line of a print design, allowing for cutting inaccuracy."),
    ],
    grade="""
+ Justify a format by the property that matters for that platform, not by habit
+ Know that RGB is for screen and CMYK is for print, and what happens if they are confused
+ Match aspect ratio to platform, including vertical video for mobile first platforms
+ Always mention accessibility, since captions and contrast are frequently examinable
+ Explain why the master should stay lossless until final export
""",
    mistakes=[
        "Supplying a print design in RGB, which shifts colour when printed.",
        "Using JPG where transparency is needed.",
        "Exporting a print file at 72 dpi, which looks acceptable on screen and pixelated on paper.",
        "Using a single 16:9 export for every social platform regardless of their requirements.",
        "Repeatedly editing and resaving a lossy file, which compounds the quality loss each time.",
    ],
    quiz=[
        Q("Which colour mode should be used for a design that will be printed?",
          ["CMYK", "RGB", "HSL", "Greyscale"], 0,
          "Printing mixes inks rather than light, so an RGB file will shift in colour unless converted."),
        Q("What resolution is usually required for print?",
          ["300 dpi", "72 dpi", "150 dpi", "24 dpi"], 0,
          "72 dpi looks fine on a screen and visibly pixelated on paper."),
        Q("Which format should be used for a logo needing a transparent background?",
          ["PNG", "JPG", "MP3", "WAV"], 0,
          "PNG is lossless and supports an alpha channel. SVG is also suitable and additionally scales."),
        Q("What does adaptive bit rate streaming do?",
          ["Adjusts the quality automatically to suit the viewer's connection speed",
           "Compresses the file before upload", "Converts between formats",
           "Adds subtitles automatically"], 0,
          "It keeps playback smooth on a poor connection by reducing quality rather than buffering."),
        Q("Which aspect ratio suits a mobile first social platform?",
          ["9:16 vertical", "16:9 widescreen", "4:3", "21:9"], 0,
          "Users hold phones vertically, so vertical video fills the screen without rotating."),
        Q("Why should a master file be kept in a lossless format?",
          ["Repeatedly editing and resaving a lossy file compounds the quality loss",
           "Lossless files are smaller", "Lossy formats cannot be edited",
           "Clients only accept lossless"], 0,
          "Each lossy save discards more data permanently, so degradation accumulates."),
        Q("What is bleed in a print design?",
          ["Extra image area beyond the trim line allowing for cutting inaccuracy",
           "The gap between columns", "The margin around text",
           "The area reserved for the printer's marks"], 0,
          "Without it, a slight misalignment when trimming leaves a thin white edge."),
        Q("Which is the most important accessibility consideration for a video?",
          ["Subtitles or captions for viewers with hearing impairments",
           "A higher frame rate", "A larger file size", "A square aspect ratio"], 0,
          "Captions also help viewers watching without sound, which is most viewers on social media."),
        Q("What is a disadvantage of distributing on physical media?",
          ["The content cannot be updated once it has been pressed",
           "It cannot be sold in shops", "It requires an internet connection",
           "It has no capacity limit"], 0,
          "Replication cost and the impossibility of correcting an error afterwards are the key drawbacks."),
        Q("Which format is most suitable for a podcast intended for download on mobile data?",
          ["MP3", "WAV", "TIFF", "SVG"], 0,
          "MP3 is lossy but the quality is more than adequate for speech, and the small file size matters."),
    ],
    exam=[
        EQ("State the difference between RGB and CMYK colour modes and explain when each is used.", 3, [
            MP("RGB mixes red, green and blue light and is used for screens", ["rgb", "light", "screen", "display", "red green blue"]),
            MP("CMYK mixes cyan, magenta, yellow and black ink and is used for print", ["cmyk", "ink", "print", "cyan magenta yellow"]),
            MP("A file created in RGB will shift in colour when printed unless converted", ["shift", "different", "colour change", "convert", "not match"]),
        ], "RGB creates colour by mixing red, green and blue light and is the colour mode used by anything that emits light, so it is correct for screens, websites, video and digital displays. CMYK creates colour by mixing cyan, magenta, yellow and black inks on paper and is the colour mode used for print. The distinction matters because the two produce different ranges of colour: some vivid colours achievable in RGB simply cannot be reproduced with ink, so a design created in RGB and sent to a printer without conversion will come back looking noticeably duller or shifted, particularly in bright blues and greens. Converting to CMYK during design allows the designer to see and correct that shift before the job is printed.",
           command="State"),
    ],
)

M_R094 = Topic(
    slug="visual-identity-and-digital-graphics",
    title="R094: Visual Identity and Digital Graphics",
    spec="R094",
    icon="i-palette",
    minutes=26,
    blurb="What the assessment criteria actually reward across the three tasks: developing visual identity, planning graphics, and creating them.",
    fact="A brand identity is far more than a logo. It is the complete system of colour, typography, imagery, tone and spacing that makes an organisation recognisable even when the logo is not visible.",
    sections=[
        Section("Developing visual identity", """
### What visual identity means

**Visual identity** is the set of visual elements that make an organisation recognisable and communicate its values:

- **Logo**, in its primary form and any variations
- **Colour palette**, primary and secondary
- **Typography**, a heading face and a body face
- **Imagery style**, the kind of photography or illustration used
- **Tone**, the overall feel: formal, playful, premium, approachable
- **Spacing and layout** conventions

### The process, and what earns marks

1. **Interpret the client brief.** Identify the purpose, the audience, the message and any constraints. Note the implicit requirements too.
2. **Research.** Look at what competitors do, what conventions exist in the sector and what the audience expects. Evidence this with examples and analysis, not just screenshots.
3. **Mood board.** Collect colours, fonts, images and textures that capture the intended feel, and annotate why each is there.
4. **Mind map.** Explore ideas broadly before narrowing down.
5. **Sketch several concepts.** Quantity first. Three or four rough ideas explored properly beats one polished idea with no alternatives.
6. **Justify the chosen concept** against the brief and the audience.

!key What separates a high band :: Justification against the brief. Not "I chose blue because I like it", but "I chose blue because the client is a financial adviser targeting people over 45, and blue is strongly associated with trust and stability in that sector".
"""),
        Section("Planning and creating digital graphics", """
### Planning

A **visualisation diagram** for each concept, annotated with:

- Dimensions and orientation
- Colours, with actual hex or CMYK values, not just colour names
- Fonts, named, with sizes
- Where each image and text element goes
- Any effects or treatments

An **assets table** listing every asset, its source, its format, its dimensions and, critically, its **licence status**. This is where you evidence that everything used is legally cleared.

### Creating the graphic

**Vector work**, in Inkscape or Illustrator, for logos and anything that must scale:

- Shapes, paths and node editing
- Boolean operations: union, difference, intersection and exclusion, which is how most logos are actually constructed
- Grouping, alignment and distribution
- Converting text to paths so the file does not depend on the font being installed

**Raster work**, in Photoshop or GIMP, for photographic material:

- Layers, and non destructive editing using adjustment layers and masks rather than editing pixels directly
- Selections, cropping and resizing
- Colour correction, levels and curves
- Filters and effects used sparingly and purposefully

### Saving and exporting

- Keep the **working file** with layers intact, such as .svg, .psd or .xcf
- Export the correct format for each intended use
- Use a clear naming convention and keep every version

### Review

Compare the finished graphic against the brief point by point, gather feedback from the client or a stakeholder, state honestly what works and what does not, and describe what you would change and why. An honest review with specific criticism scores far more highly than one claiming everything succeeded.
"""),
    ],
    keyterms=[
        ("Visual identity", "The system of colour, typography, imagery and tone that makes an organisation recognisable."),
        ("Client brief", "The document setting out what the client requires."),
        ("Mood board", "An annotated collage capturing the intended look and feel."),
        ("Visualisation diagram", "An annotated sketch showing exactly how the finished graphic will look."),
        ("Assets table", "A record of every asset used, including its source and licence status."),
        ("Vector graphic", "An image stored as mathematical shapes, scalable without loss of quality."),
        ("Raster graphic", "An image stored as a grid of pixels, suited to photographic content."),
        ("Non destructive editing", "Editing using layers and masks so the original pixels remain unaltered."),
        ("Boolean operation", "Combining shapes using union, difference, intersection or exclusion."),
    ],
    grade="""
+ Justify every design decision against the brief and the audience, never against personal taste
+ Produce several distinct concepts, not one idea with minor variations
+ Give exact colour values and named fonts in visualisation diagrams, not vague descriptions
+ Complete the licence column of the assets table for every single asset
+ Work non destructively so changes can be made without starting again
+ Review honestly, identifying specific weaknesses and what you would change
""",
    mistakes=[
        "Justifying choices by personal preference rather than by the brief.",
        "Producing only one concept, which loses the marks for exploring alternatives.",
        "Leaving the licence column of the assets table incomplete.",
        "Editing pixels directly rather than using adjustment layers and masks.",
        "Writing a review claiming everything went perfectly.",
        "Delivering a logo only as a JPG, with no vector master and no transparency.",
    ],
    quiz=[
        Q("What does visual identity include beyond a logo?",
          ["Colour palette, typography, imagery style and tone",
           "Only the logo in different sizes", "The client's address",
           "The file formats used"], 0,
          "It is the whole system that makes an organisation recognisable even without the logo present."),
        Q("What should a visualisation diagram include?",
          ["Dimensions, exact colours, named fonts and the position of every element",
           "Only a rough sketch", "The finished artwork",
           "A list of competitors"], 0,
          "It must contain enough detail for someone else to produce the graphic from it."),
        Q("Why is the licence column of an assets table important?",
          ["It evidences that every asset used is legally cleared",
           "It records the file size", "It lists the software used",
           "It shows the deadline"], 0,
          "Without it there is no proof that the work does not infringe copyright."),
        Q("Which Boolean operation would cut one shape out of another?",
          ["Difference", "Union", "Intersection", "Exclusion"], 0,
          "Difference is how a crescent, a hole or a cut out counter is usually constructed."),
        Q("What is non destructive editing?",
          ["Using layers and masks so the original pixels are not permanently altered",
           "Saving frequently", "Working only in vector software",
           "Making a backup before editing"], 0,
          "It means any change can be adjusted or removed later without starting from the original again."),
        Q("Why should text in a logo be converted to paths?",
          ["So the file does not depend on the font being installed on another machine",
           "To reduce the file size", "To make the text editable",
           "To change the colour"], 0,
          "A printer without your font would otherwise substitute a different one and change the logo."),
        Q("What makes a strong justification of a colour choice?",
          ["Linking the colour's associations to the client's sector and audience",
           "Saying it is your favourite colour", "Saying it looks modern",
           "Saying it was easy to use"], 0,
          "The mark is for the reasoning, and the reasoning must come from the brief."),
        Q("How many initial concepts should be produced?",
          ["Several distinct ideas, so alternatives are genuinely explored",
           "Exactly one, developed fully", "Two, that are very similar",
           "None, work straight in the software"], 0,
          "Exploring alternatives is explicitly rewarded, and it produces better final work."),
        Q("Which file should be kept as the working version of a logo?",
          ["The layered vector file such as SVG or AI", "A flattened JPG",
           "A PNG export", "A PDF"], 0,
          "Exports are produced from the working file, which retains everything needed to make changes."),
        Q("What makes a review score highly?",
          ["Honest identification of specific weaknesses and what would be changed",
           "Stating that everything worked perfectly", "Describing the software used",
           "Listing the fonts chosen"], 0,
          "A review with no criticism reads as one that was never genuinely carried out."),
    ],
    exam=[
        EQ("Explain why a mood board is produced before designing a visual identity.", 3, [
            MP("It gathers colours, images, fonts and textures capturing the intended feel", ["colours", "images", "fonts", "textures", "feel", "collect"]),
            MP("It allows the designer and client to agree a direction before work begins", ["agree", "client", "direction", "before", "shared understanding"]),
            MP("It is far quicker and cheaper to change than finished artwork", ["quicker", "cheaper", "easier to change", "less work", "early"]),
        ], "A mood board gathers together colours, photographs, typefaces, textures and existing designs that capture the feel the identity is aiming for, giving a visual reference for something that is very difficult to describe in words. Its main purpose is to establish a shared understanding with the client before design work begins, since a client who says they want something modern and a designer who hears something modern may have entirely different pictures in mind. Resolving that disagreement over a mood board takes an afternoon, whereas discovering it after two weeks of finished artwork means starting again, so the mood board substantially reduces the risk and cost of the project.",
           command="Explain"),
    ],
)

M_R097 = Topic(
    slug="interactive-digital-media",
    title="R097: Interactive Digital Media",
    spec="R097",
    icon="i-web",
    minutes=26,
    blurb="Planning, creating and reviewing an interactive product, and what the assessment criteria actually reward at each stage.",
    fact="Interactive means the user controls what happens. That single property changes everything about the planning, because you are not designing one experience, you are designing every route a user could take.",
    sections=[
        Section("Planning an interactive product", """
### What makes it interactive

The user makes choices that change what happens. That means you are not planning a linear sequence but a **structure** of possible routes, and every route has to work.

### The planning documents

| Document | Purpose |
| **Mind map** | Explore content and features broadly |
| **Client brief interpretation** | Identify purpose, audience, message and constraints |
| **Mood board** | Establish the intended look and feel |
| **Navigation diagram** | Show every screen and how they connect. This is the most important document for an interactive product |
| **Wireframes** | Show the layout of each screen without styling |
| **Storyboard** | Plan any video or animated sequences within the product |
| **Script** | Write any narration, dialogue or on screen text |
| **Assets table** | Record every asset with source, format and licence |
| **Work plan** | Schedule tasks, dependencies and contingency |

### Navigation diagrams

Every screen appears as a box, with arrows showing which screen each link or button leads to. Check:

- Every screen can be **reached**
- Every screen has a way **back**
- There are no dead ends
- The **depth** is reasonable, so nothing takes six clicks to reach
- The structure is consistent, so the user always knows where they are

### Interface design principles

- **Consistency**: the same element looks and behaves the same everywhere
- **Feedback**: every action produces a visible response
- **Clarity**: buttons say what they do
- **Forgiveness**: mistakes can be undone, and destructive actions confirm first
- **Accessibility**: sufficient contrast, readable text sizes, keyboard access, alternative text, captions on video
"""),
        Section("Creating and reviewing", """
### Creating

- Build the **structure first**, then add content, then style it. Styling an incomplete structure means restyling it later.
- Use **consistent naming** for files and assets, and organise them in folders by type.
- Keep every **source file** as well as the exports.
- Test **as you build**, not only at the end.

### Skills that evidence technical competence

- Combining several media types: text, images, audio, video and animation
- Working navigation across the whole product, with no dead ends
- Interactive elements such as buttons, menus, rollovers, forms and quizzes
- Video editing including cuts, transitions, titles and colour correction
- Audio editing including trimming, level balancing, fades and background music mixed below narration
- Optimising assets so the product loads quickly without visible quality loss

### Testing

Test against the plan, not against what you happened to build.

| Test type | What it checks |
| Functionality | Every button, link and interactive element works |
| Navigation | Every screen is reachable and every route returns |
| Content | Spelling, accuracy, and that everything specified is present |
| Media | Video and audio play correctly at the right level |
| Compatibility | It works on different devices and screen sizes |
| Usability | A real user can complete a task without help |

Record for each test the test data used, the expected result and the actual result, and evidence any correction made.

### Reviewing

- Compare the product against the **original brief**, point by point
- Report **stakeholder feedback**, including the criticism
- State honestly what works, what does not and why
- Describe specific **further improvements** and how each would be implemented

!warn Do not evaluate your own product by using it :: You built it, so you know where everything is. Watch a real user attempt a task and record every point at which they hesitate. Those hesitations are the evaluation.
"""),
    ],
    keyterms=[
        ("Interactive product", "A product in which the user's choices determine what happens next."),
        ("Navigation diagram", "A diagram showing every screen of a product and how they connect."),
        ("Wireframe", "A layout sketch of a single screen, showing placement without styling."),
        ("Dead end", "A screen from which the user has no way to continue or return."),
        ("Usability testing", "Observing a real user attempting a task and recording where they struggle."),
        ("Functionality testing", "Checking that every interactive element behaves as intended."),
        ("Optimisation", "Reducing asset file sizes so a product loads quickly without visible quality loss."),
        ("Feedback", "A visible response confirming to the user that their action registered."),
    ],
    grade="""
+ Produce a navigation diagram covering every screen, with a route back from each
+ Wireframe every distinct screen, not only the home screen
+ Combine several media types to evidence a genuine range of technical skills
+ Test against the plan written beforehand, including cases that should fail
+ Watch a real user and record their difficulties rather than judging your own product
+ Review honestly, with specific improvements and how each would be implemented
""",
    mistakes=[
        "Producing a navigation diagram with dead ends, where the user cannot get back.",
        "Wireframing only the home screen.",
        "Styling before the structure is complete, which means restyling everything later.",
        "Testing only what already works.",
        "Evaluating by using the product yourself rather than watching someone else.",
        "Leaving asset licences unrecorded.",
    ],
    quiz=[
        Q("Which document is most important when planning an interactive product?",
          ["The navigation diagram", "The storyboard", "The mood board", "The script"], 0,
          "It shows every screen and how they connect, which is the structure the whole product depends on."),
        Q("What is a dead end in a navigation structure?",
          ["A screen the user cannot continue from or return from",
           "A broken image", "A screen with no text", "The final screen of a sequence"], 0,
          "Every screen needs a route onward or back, or the user becomes stuck."),
        Q("What should be built first when creating an interactive product?",
          ["The structure and navigation", "The visual styling",
           "The video content", "The final animations"], 0,
          "Styling an incomplete structure means having to restyle everything once it changes."),
        Q("What does usability testing involve?",
          ["Watching a real user attempt a task and recording where they struggle",
           "Checking that every link works", "Testing on different browsers",
           "Reading the content for spelling errors"], 0,
          "It reveals problems the creator cannot see, because they already know the product."),
        Q("Why should every asset's licence be recorded?",
          ["To evidence that everything used is legally cleared",
           "To calculate the file size", "To choose the format",
           "To decide the layout"], 0,
          "It is the proof that no copyright has been infringed, and it is assessed."),
        Q("What is meant by feedback in interface design?",
          ["Every action produces a visible response confirming it registered",
           "Comments from the client", "The review section of the project",
           "Testing by a stakeholder"], 0,
          "Without it, users repeatedly click because they cannot tell whether anything happened."),
        Q("Which accessibility feature helps users with hearing impairments?",
          ["Captions on video content", "Higher colour contrast",
           "Larger buttons", "A faster loading page"], 0,
          "Captions also help the large number of users who watch video with the sound off."),
        Q("What should a test record include for each test?",
          ["The test data, the expected result and the actual result",
           "Only the actual result", "A screenshot only", "The time taken"], 0,
          "Without an expected result recorded in advance there is nothing to compare against."),
        Q("Why should assets be optimised before being included?",
          ["So the product loads quickly without visible quality loss",
           "To improve the colour accuracy", "Because software requires it",
           "To make editing easier"], 0,
          "Oversized assets make an interactive product slow, which is the fastest way to lose a user."),
        Q("What makes a review of an interactive product score highly?",
          ["Honest criticism supported by stakeholder feedback, with specific improvements",
           "Stating that every part worked perfectly", "A long description of the software",
           "Screenshots of every screen"], 0,
          "Identifying real weaknesses and explaining how you would fix them shows genuine understanding."),
    ],
    exam=[
        EQ("Explain why a navigation diagram is produced when planning an interactive product.", 3, [
            MP("It shows every screen and how they are connected", ["every screen", "connected", "links", "structure"]),
            MP("It allows the designer to check every screen is reachable with a route back", ["reachable", "route back", "dead end", "get back", "no dead ends"]),
            MP("Structural problems are far easier to fix on a diagram than in a built product", ["easier to fix", "before building", "cheaper", "quicker", "on paper"]),
        ], "A navigation diagram maps every screen of the product as a box and shows with arrows which screen each link or button leads to, so the entire structure can be seen at once. This allows the designer to verify that every screen can actually be reached, that there is always a route back or onward so the user cannot become stuck at a dead end, and that nothing important is buried so deep that it takes too many clicks to find. Identifying and correcting these problems on a diagram takes minutes, whereas discovering after the product has been built that a whole section is unreachable means rebuilding the navigation and possibly restructuring several screens.",
           command="Explain"),
    ],
)

# ================================================================== COURSE

COURSE = Course(
    slug="ks4/imedia",
    title="Creative iMedia",
    short="Creative iMedia",
    stage="KS4",
    board="OCR",
    code="J834",
    goal="Distinction star",
    icon="i-palette",
    accent="var(--purple)",
    blurb="OCR Cambridge National in Creative iMedia J834. The R093 examined unit covered in full with quizzes and exam-style questions, plus guidance on what the R094 and R097 coursework assessment criteria actually reward.",
    intro="",
    journey=[
        ("Learn R093 properly, because it is the examined unit",
         "The coursework is marked on what you produce, but R093 is a written exam and it is the part most students under prepare for. Know the job roles, the documents and the legislation cold.", ""),
        ("Know exactly which document goes with which product",
         "Visualisation diagram for a static product, storyboard for moving image, wireframe and navigation diagram for interactive. Confusing these is the single most common error in this unit.", ""),
        ("Justify everything against the brief",
         "The difference between a pass and a distinction is almost never technical skill. It is whether every decision is explained in terms of the client, the audience and the purpose.", ""),
        ("Get the licences right from the start",
         "Every asset needs a recorded source and licence. Fixing this at the end means rebuilding, and using an unlicensed image can invalidate the work entirely.", ""),
        ("Test with a real person and write down what they struggle with",
         "You cannot evaluate your own product fairly, because you already know how it works. Watching someone else use it produces the evidence the review needs.", ""),
        ("Be honest in every review",
         "A review saying everything worked perfectly scores badly. Identifying a real weakness and explaining how you would fix it scores well.", ""),
    ],
    units=[
        Unit("r093", "R093: Creative iMedia in the Media Industry",
             "The examined unit. The media industry, factors influencing design, pre-production planning and distribution considerations.",
             [M_TA1, M_TA2, M_TA3, M_TA4], icon="i-video", term="Exam unit"),
        Unit("r094", "R094: Visual Identity and Digital Graphics",
             "Developing a visual identity from a client brief, planning it, and creating the digital graphics.",
             [M_R094], icon="i-palette", term="Coursework"),
        Unit("r097", "R097: Interactive Digital Media",
             "Planning, creating and reviewing an interactive digital media product.",
             [M_R097], icon="i-web", term="Coursework"),
    ],
)
