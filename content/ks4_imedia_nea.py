"""Creative iMedia J834: the two coursework units, R094 and R097.

Both units are internally assessed through an OCR-set assignment: a brief from
a fictional client, with tasks, marked by the centre and moderated by OCR.

  R094  Visual identity and digital graphics   25%  two tasks, 50 marks
        TA1  Develop visual identity                       Task 1
        TA2  Plan digital graphics for products            Task 1, applied in Task 2
        TA3  Create visual identity and digital graphics   Task 2
  R097  Interactive digital media              35%  three tasks
        TA1  Plan interactive digital media                Task 1
        TA2  Create interactive digital media              Task 2
        TA3  Review interactive digital media              Task 3

Each topic area has a page of its own, and each task has a guide: what it
asks for, how to do it step by step, a worked example and a checklist. The
worked examples use two invented clients, Spokes (a community bike repair
workshop) for R094 and Castle Hill Community Garden's visitor kiosk for R097,
deliberately unlike any OCR set assignment, so they show the quality of the
evidence without answering anybody's real brief.

There is no exam in either unit, so the written practice is headed "Check you
could explain this". Assignments are replaced over time, so every guide tells
students to work from their current assignment and its marking grid.
"""
from mskbuild.models import Topic, Section, Q, EQ, MP

NEA = "Check you could explain this"

J834_PAGE = ("https://www.ocr.org.uk/qualifications/cambridge-nationals/"
             "creative-imedia-level-1-2-j834/")
J834_SPEC = ("https://www.ocr.org.uk/Images/610942-specification-cambridge-"
             "nationals-creative-imedia-j834.pdf")
MOD_2024 = "https://www.ocr.org.uk/Images/727137-moderators-report-creative-imedia.pdf"
MOD_2023 = "https://www.ocr.org.uk/Images/704362-moderators-report-creative-imedia.pdf"
URS_R094 = "https://www.ocr.org.uk/Images/664336-visual-identity-and-digital-graphics.pdf"
URS_R097 = "https://www.ocr.org.uk/Images/664341-interactive-digital-media.pdf"

OCR_LINKS = """
- [OCR Cambridge Nationals in Creative iMedia (J834)](%s): the qualification page, with the specification and the assessment materials your teacher works from.
- [The J834 specification (PDF)](%s): the content of every topic area. Check that your version matches.
- [Moderators' report, summer 2024 (PDF)](%s) and [summer 2023 (PDF)](%s): what moderators saw in real R094 and R097 work, including where marks were most often lost.
""" % (J834_PAGE, J834_SPEC, MOD_2024, MOD_2023)

# ================================================================ R094 TA1

M_R094_IDENTITY = Topic(
    slug="visual-identity-and-digital-graphics",
    title="R094 TA1: Developing a Visual Identity",
    spec="R094 TA1",
    icon="i-palette",
    minutes=28,
    exam_title=NEA,
    blurb="What a visual identity is for, the elements and design style that make it up, interpreting the client's requirements, and developing an identity you can justify against the brief.",
    fact="A brand identity is far more than a logo. It is the whole system of colour, type, imagery, tone and spacing that makes an organisation recognisable even when the logo is nowhere on the page.",
    sections=[
        Section("What visual identity is", """
**Visual identity** is the set of visual elements that make an organisation recognisable and that communicate what it stands for.

### What it is for

| Purpose | What it means | Example |
| **Brand recognition** | People know who it is at a glance, even before they read the name | A logo recognised on a van from across the road |
| **Brand values** | It communicates what the organisation stands for | Earthy colours and plain type for a sustainable, practical business |
| **Brand loyalty** | Consistency builds familiarity, and familiarity builds trust | Customers who come back because they recognise and trust it |

### The elements

| Element | What it covers |
| **Name** | What the organisation is called, and how it is written |
| **Logo** | The primary mark, plus its variations: stacked, horizontal, icon only, single colour |
| **Slogan or strapline** | A short line that expresses the brand's promise or personality |
| **Colour palette** | A primary colour, an accent and neutrals, each defined as exact values |
| **Typography** | A heading typeface and a body typeface, with the sizes and weights used |
| **Graphics and imagery** | The style of photography or illustration, and how it is treated |
| **Layout** | The grid, the margins, and the clear space kept around the logo |

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
### The client's requirements

Before designing anything, write down in your own words what the client needs:

- the **business type**: what the organisation does, and its sector
- the **brand values**: the three or four words it wants to be known for, such as friendly, sustainable, practical
- the **target audience**: who they are, in as much detail as the brief allows
- the **purpose** of the identity and the **message** it has to carry
- the **content** that must appear: the name, a slogan, any required wording
- the **constraints**: the deadline, print or screen, any existing colours or styles to keep
- the **implicit** requirements, which the brief does not state but clearly expects

### Research that counts

| Type | What to do with it |
| **Competitor analysis** | Three or four direct competitors, analysed for colour, type and tone, with a note on what each is doing and what gap that leaves |
| **Sector conventions** | What the audience already expects from this kind of organisation |
| **Audience research** | Who they are, demographically and psychographically, and what they respond to |
| **Visual research** | Colour, type, texture and photographic style, from anywhere relevant |

The assessment rewards **analysis**, not collection. A screenshot with no comment is worth nothing; a screenshot with "this uses a cold blue and a geometric sans to look clinical, which suits a lab but would feel unwelcoming for a children's nursery" is worth a great deal.
"""),
        Section("Developing the identity", """
### Generating ideas

1. **Mind map** to open the possibilities up: the business, its values, its audience, and the images and words they suggest
2. **Mood board**, annotated, to fix the look and feel
3. **Thumbnail sketches**, at least six, quickly, before judging any of them
4. **Three distinct concepts**, genuinely different rather than three versions of one
5. **Choose one, and justify the choice** against the brief, the audience and the research

!warn One idea is the most expensive mistake in this unit :: Exploring alternatives is part of what is assessed. A single polished concept with no alternatives limits the marks however good it is, and it also produces worse work, because the first idea is rarely the best one.

### Refining the chosen concept

- Simplify until it works at its **smallest** size and in **one colour**.
- Test it on the **backgrounds** it will really appear on: white, the brand colour, a photograph.
- Check the **typeface** is legible at small sizes and suits the brand values.
- Keep the **development** in your evidence: each version, and why it changed.

### Defining the identity

Once the logo is settled, define the identity precisely enough that anyone could apply it consistently: the **logo and its versions**, with clear space and a minimum size; the **colour palette** as exact values; the **typefaces** by name, with their uses and licences; the **slogan**; and **rules** for how the logo must never be used. The [Task 1 guide](/ks4/imedia/r094-task-1-visual-identity/) shows a complete example as a one-page style guide.

!grade What the top band looks like :: Every decision traced to the brief. "The palette is a deep green with a warm orange accent, because the client is a community bike workshop that wants to feel sustainable and friendly rather than technical. Green carries the environmental message, and orange gives the energy of a volunteer-run project, where the black and grey of most cycle shops would read as expensive and specialist." Taste is never a justification; the brief always is.
"""),
        Section("Sources and further reading", OCR_LINKS + """
- [Adobe Color](https://color.adobe.com/create/color-wheel): build a palette from colour harmony rules and read off the exact values.
- [Google Fonts](https://fonts.google.com/): typefaces you may use commercially, each with its licence.
- [WebAIM contrast checker](https://webaim.org/resources/contrastchecker/): check that text in your colours is readable.
"""),
    ],
    keyterms=[
        ("Visual identity", "The system of colour, typography, imagery and tone that makes an organisation recognisable."),
        ("Brand recognition", "People identifying an organisation at a glance from its visual identity."),
        ("Brand values", "The qualities an organisation wants to be known for, such as friendly or sustainable."),
        ("Brand loyalty", "Customers returning because they recognise and trust the brand."),
        ("Slogan", "A short, memorable line expressing the brand's promise or personality."),
        ("Wordmark", "A logo made from the organisation's name, styled distinctively."),
        ("Combination mark", "A logo pairing a symbol with the name, so the symbol can later stand alone."),
        ("Mood board", "An annotated collage establishing the intended look and feel."),
        ("Style guide", "A document defining the logo, colours, typefaces and rules of a visual identity."),
        ("Clear space", "The minimum empty margin kept around a logo in any layout."),
    ],
    grade="""
+ Write the client's requirements in your own words, including what the brief only implies
+ Analyse research rather than collecting it; every example needs a comment on what it does and why
+ Produce at least three genuinely different concepts before choosing
+ Refine the chosen logo until it works small and in one colour, and keep the development
+ Define the identity with exact colour values, named typefaces and their licences
+ Justify every choice against the brief, the audience or the research, never against taste
""",
    mistakes=[
        "Justifying a design by personal preference instead of the brief.",
        "Presenting one concept, or three near identical versions of one concept.",
        "Collecting research with no analysis attached.",
        "Throwing away the rejected concepts, which are evidence of exploring alternatives.",
        "Defining colours as 'green' and 'orange' instead of exact values.",
        "Designing a logo that only works large, with detail that disappears at small sizes.",
    ],
    quiz=[
        Q("What does visual identity include beyond the logo?",
          ["Colour palette, typography, imagery style and tone",
           "Only the logo at different sizes", "The client's contact details",
           "The file formats used"], 0,
          "It is the whole system that makes an organisation recognisable without the logo present."),
        Q("Customers keep returning to a business because they recognise and trust it. Which purpose of visual identity is this?",
          ["Brand loyalty", "Brand recognition", "Brand values", "Brand positioning"], 0,
          "Consistency builds familiarity, and familiarity builds the trust that brings people back."),
        Q("Which logo type is safest for a brand nobody has heard of yet?",
          ["Combination mark", "Abstract mark", "Lettermark", "Mascot"], 0,
          "The name teaches the audience who you are, and the symbol can stand alone once they know."),
        Q("What makes competitor research worth marks?",
          ["Analysis of what each competitor does and what gap it leaves",
           "The number of screenshots collected", "Listing competitors' names",
           "Copying the most successful design"], 0,
          "Collection is not research. The comment on each example is the assessed part."),
        Q("Which of these is an element of a visual identity?",
          ["A slogan", "A navigation diagram", "A test plan", "A file size"], 0,
          "Name, logo and slogan are elements; colour, type, graphics and layout make up its style."),
        Q("How many initial concepts should be developed?",
          ["At least three genuinely different ones", "One, developed fully",
           "Two very similar ones", "None: work straight in the software"], 0,
          "Exploring alternatives is assessed, and it produces better final work."),
        Q("Why is detail removed as a logo develops?",
          ["So it stays legible at very small sizes",
           "To reduce the file size", "To make it cheaper to print",
           "Because simple logos are fashionable"], 0,
          "A logo has to survive being a favicon as well as being on a van."),
        Q("What is a style guide for?",
          ["Defining the identity so anyone can apply it consistently",
           "Listing the software used", "Recording the client's budget",
           "Planning the work schedule"], 0,
          "Exact colours, named fonts and logo rules are what make an identity consistent."),
        Q("What is clear space in brand guidelines?",
          ["The minimum empty margin kept around the logo",
           "The white background of the logo", "Space left for a slogan",
           "The gap between letters"], 0,
          "It stops the logo being crowded by other elements and losing impact."),
        Q("What makes a justification score in the top band?",
          ["It links the decision to the brief, audience or research",
           "It describes the software used", "It says the design looks modern",
           "It explains how long the work took"], 0,
          "The marks are for the reasoning, and the reasoning has to come from the brief."),
    ],
    exam=[
        EQ("Explain why a mood board is produced before any design work begins.", 3,
           [MP("It gathers colours, images, type and textures capturing the intended feel", ["colours", "images", "fonts", "textures", "feel", "collect"]),
            MP("It establishes a shared understanding with the client", ["agree", "client", "direction", "shared", "same idea"]),
            MP("It is far cheaper to change than finished artwork", ["cheaper", "quicker", "easier to change", "early", "less work"])],
           "A mood board gathers colours, photographs, typefaces and textures that capture the feel the identity is aiming for, which gives something concrete to discuss about a quality that is very hard to describe in words. Its real purpose is to establish a shared understanding with the client before design begins, because a client who says modern and a designer who hears modern may have completely different pictures in mind. Resolving that disagreement over a mood board takes an afternoon; discovering it after two weeks of finished artwork means starting again.",
           command="Explain"),
        EQ("Explain **two** purposes of a visual identity for a new business.", 4,
           [MP("Brand recognition: people identify the business quickly", ["recognis", "identify", "stand out", "at a glance", "remember"]),
            MP("Why that matters for a new business", ["new", "unknown", "compete", "noticed", "memorable"]),
            MP("Brand values or loyalty: it communicates what the business stands for, or builds trust", ["values", "stands for", "loyal", "trust", "return"]),
            MP("Why that matters for a new business", ["first impression", "customers", "come back", "consistent", "reputation"])],
           "The first purpose is brand recognition. A new business is unknown, so a distinctive, consistent identity helps people notice it and remember it, and recognise it again on a sign, a bag or a social media post without reading the name. The second purpose is to communicate the brand's values, which builds loyalty over time: colours, type and imagery tell customers what kind of business it is before they have used it, such as friendly and affordable or premium and expert, and applying them consistently makes the business feel established and trustworthy, which is what brings customers back.",
           command="Explain"),
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

# ================================================================ R094 TA2

M_R094_PLAN = Topic(
    slug="planning-digital-graphics",
    title="R094 TA2: Planning Digital Graphics for Products",
    spec="R094 TA2",
    icon="i-pen",
    minutes=30,
    exam_title=NEA,
    blurb="What digital graphics are for and the conventions they follow, the technical properties that decide resolution, colour and format, and the visualisation diagrams and asset tables that plan a graphic before it is made.",
    fact="An A4 page printed at 300 dots per inch needs nearly nine million pixels, 2480 by 3508. A typical phone screen shows under a third of that, which is why an image that looks sharp on a phone can print badly.",
    sections=[
        Section("Purpose and conventions of digital graphics", """
### What the graphic is for

| Purpose | What it has to do | Example product |
| **Advertise or promote** | Make the audience want something, and tell them how to get it | A poster for an event, a social media advert |
| **Inform** | Get facts across clearly and quickly | A notice, a map, an infographic |
| **Educate** | Help somebody learn or understand | A diagram on a revision sheet |
| **Entertain** | Engage, amuse or excite | Game artwork, a magazine cover |

Most graphics do more than one of these, but one purpose leads, and it decides the layout: an advert leads with the offer and the call to action, an information graphic with clarity.

### Layout conventions

- **Hierarchy**: the most important element is the largest or strongest, so it is read first.
- **Focal point**: one element draws the eye, often an image placed on a third.
- **Alignment and grid**: elements line up on a grid, so the page looks ordered.
- **White space**: empty space around elements, so the important ones stand out.
- **Proximity**: related information is grouped together.
- **Consistency**: the identity's fonts, colours and logo are used the same way everywhere.
- **Call to action**: what the audience should do next, and how.

!diagram imedia-layout-conventions
"""),
        Section("Technical properties of digital graphics", """
### Pixels, resolution and size

!diagram r094-graphic-properties

### Colour mode

Decide it from the destination at the start, not at export: **CMYK** for anything printed, **RGB** for anything on a screen.

!diagram imedia-colour-modes

### Raster or vector

The logo and any type should be **vector**, so they scale to any size. Photographs are **raster**, and need enough pixels for their largest use.

!diagram imedia-raster-vector

### File formats

| Format | Type | Use it for | Notes |
| **SVG** | Vector | Logos and icons on screen | Scales to any size; small files |
| **AI**, **EPS**, **AFDESIGN** | Vector | Working files and print logos | Need design software to open |
| **PSD**, **XCF**, **AFPHOTO** | Raster, layered | Working files | Keep layers, masks and live text |
| **PNG** | Raster | Screen graphics that need transparency | Lossless, so larger than JPG |
| **JPG** | Raster | Photographs on screen | Lossy compression; no transparency |
| **PDF** | Either | Print-ready files | Embeds fonts and keeps vectors |
| **TIFF** | Raster | High-quality print images | Large, lossless |
| **GIF** | Raster | Simple animation | Only 256 colours |

!diagram imedia-compression-types
"""),
        Section("Visualisation diagrams and asset tables", """
The planning documents are part of **Task 1** of the set assignment, and you build from them in Task 2. The [Task 1 guide](/ks4/imedia/r094-task-1-visual-identity/) has a complete visualisation diagram for a worked example.

### The visualisation diagram

One for each product, annotated well enough that somebody else could produce the graphic without asking a question:

- **Canvas size and orientation**, in millimetres for print or pixels for screen
- **Every colour as a value**, `#1F6F50` or the equivalent CMYK
- **Every font by name, weight and size**, "Poppins Bold 42pt"
- **Position of every element**, with measurements where they matter
- **Bleed and safe margins** for anything printed
- **Annotations explaining the intention**, not just labelling the parts

### The asset table

| Asset | Type | Source | Format | Dimensions | Licence |
| logo-mark | Vector | Own work | SVG | scalable | Own work |
| hero-photo | Raster | Unsplash | JPG | 4000 x 2667 | Unsplash licence, commercial use permitted |
| heading-font | Font | Google Fonts | WOFF2 | — | SIL Open Font Licence |

Every row completed, fonts included, because fonts are licensed software and a commercial project needs a licence that covers commercial use.

### Legal considerations

- **Copyright** protects images, fonts, music and video automatically, from the moment they are created. Using an asset without permission is infringement, even in a school project.
- A **licence** says what you may do with an asset. Creative Commons, stock library and font licences all set conditions, such as crediting the creator or non-commercial use only.
- A recognisable **person** in a photograph needs their permission, and another organisation's **trademark** cannot be used as if it were your client's.
- Record the source and licence of every asset in the asset table **as you find it**, not at the end.

!diagram imedia-licence-check

### Technical planning

- Decide **RGB or CMYK** now, from the destination, not at export
- Decide **vector or raster** for each element: the logo and type vector, photographs raster
- Work out the **resolution** needed from the final physical size
- Plan the **file naming and versioning** before the first save
"""),
        Section("Sources and further reading", OCR_LINKS + """
- [GOV.UK: how copyright protects your work](https://www.gov.uk/copyright): what copyright covers and how long it lasts.
- [Creative Commons licences](https://creativecommons.org/licenses/): what each licence lets you do, and what it requires.
- [Unsplash licence](https://unsplash.com/license) and [Pexels licence](https://www.pexels.com/license/): what you may and may not do with free stock photographs.
- [Wikimedia Commons](https://commons.wikimedia.org/): freely licensed images, each with its own licence stated.
- [diagrams.net](https://app.diagrams.net/): free for drawing visualisation diagrams.
"""),
    ],
    keyterms=[
        ("Hierarchy", "Ordering elements by size and strength so the most important is read first."),
        ("Focal point", "The element that draws the eye first."),
        ("White space", "Empty space around elements, used to make the important ones stand out."),
        ("Call to action", "The part of a graphic telling the audience what to do next."),
        ("Resolution", "The detail in an image: for print, dots per inch; for screen, the pixel dimensions."),
        ("DPI", "Dots per inch: how many printed dots make up each inch of a printed image."),
        ("CMYK", "The colour mode for print: cyan, magenta, yellow and black ink."),
        ("RGB", "The colour mode for screens: red, green and blue light."),
        ("Vector graphic", "An image stored as shapes and paths, which scales to any size without losing quality."),
        ("Raster graphic", "An image stored as a grid of pixels, which loses quality when enlarged."),
        ("Visualisation diagram", "An annotated plan of a static graphic, detailed enough to work from."),
        ("Asset table", "A record of every asset with its source, format, dimensions and licence."),
        ("Bleed", "Extra artwork beyond the trim edge, so printed colour runs right to the edge."),
    ],
    grade="""
+ Name the graphic's purpose and audience, and let them decide the layout
+ Use and explain layout conventions: hierarchy, focal point, alignment, white space
+ Work out the resolution and colour mode from the destination, with the numbers shown
+ Put exact sizes, colour values and named fonts on the visualisation diagram
+ Complete the asset table as you go, with a source and licence for every asset, fonts included
""",
    mistakes=[
        "Writing 'blue' and 'a bold font' on a visualisation diagram.",
        "Choosing RGB for a printed product, or deciding the colour mode at export.",
        "Sourcing a photograph too small for the size it will be printed.",
        "Leaving the licence column incomplete, particularly for fonts.",
        "Using images found on a search engine without checking who owns them.",
        "Labelling the parts of a visualisation diagram without explaining any of them.",
    ],
    quiz=[
        Q("A poster for a school fair mainly needs to:",
          ["Advertise or promote", "Educate", "Entertain", "Store data"], 0,
          "It has to make people want to come and tell them how, so the call to action leads."),
        Q("How should a colour be recorded on a visualisation diagram?",
          ["As an exact value such as #1F6F50", "As 'green'",
           "As 'the same as the logo'", "It is decided later"], 0,
          "Somebody else must be able to reproduce it exactly."),
        Q("How many pixels does an A4 page need at 300 dpi?",
          ["2480 × 3508", "1080 × 1080", "1920 × 1080", "300 × 300"], 0,
          "210 mm is 8.27 inches, times 300 is 2480; 297 mm gives 3508."),
        Q("Which colour mode should a printed leaflet be designed in?",
          ["CMYK", "RGB", "It does not matter", "HSL"], 0,
          "Printers use cyan, magenta, yellow and black ink, so design in what will print."),
        Q("Why should a logo be created as a vector?",
          ["It scales to any size without losing quality",
           "It is always smaller than a photograph",
           "Printers cannot print raster images",
           "Vectors are always in colour"], 0,
          "A logo appears at every size from a favicon to a banner."),
        Q("Which format suits a logo on a website that needs a transparent background?",
          ["SVG or PNG", "JPG", "GIF only", "TIFF"], 0,
          "JPG cannot store transparency; SVG scales and PNG keeps transparency."),
        Q("What does the asset table record for every asset?",
          ["Its source, format, dimensions and licence",
           "Only its file name", "The time it took to create",
           "The client's opinion of it"], 0,
          "It is the evidence that every asset can legally be used."),
        Q("Why must the licence of a font be recorded?",
          ["Fonts are licensed software and commercial use needs permission",
           "To record the file size", "Fonts have no licence",
           "To choose the point size"], 0,
          "Using a font without a commercial licence is the same kind of infringement as using an image."),
        Q("What is bleed?",
          ["Artwork extended beyond the trim edge so colour reaches the edge after cutting",
           "Colour running into the next page", "A printing fault",
           "The white border around a poster"], 0,
          "Usually 3 mm, so a slightly inaccurate cut never leaves a white sliver."),
        Q("What is white space for?",
          ["Making the important elements stand out", "Saving ink",
           "Filling the page", "Hiding mistakes"], 0,
          "Space around an element gives it emphasis; crowding takes it away."),
    ],
    exam=[
        EQ("Describe **three** things that must appear on a visualisation diagram, and explain why each is needed.", 6,
           [MP("Dimensions and orientation", ["dimensions", "size", "canvas", "orientation", "mm", "pixels"]),
            MP("Why they are needed", ["final size", "resolution", "fit", "print", "produce it"]),
            MP("Exact colour values", ["hex", "CMYK", "#", "exact", "value"]),
            MP("Why they are needed", ["reproduce", "consistent", "same colour", "not guess", "print accurately"]),
            MP("Named fonts with sizes", ["font", "typeface", "name", "point", "size"]),
            MP("Why they are needed, or a fourth valid element", ["substitut", "not installed", "consistent", "position", "annotation"])],
           "The canvas dimensions and orientation must be stated, because every other decision depends on the final size: the resolution an image needs, whether a layout works in portrait, and how much space the text can occupy. Exact colour values must be given in hex or CMYK rather than colour names, so that anyone producing the graphic reproduces the same colour, and so a print version matches the screen version instead of shifting. Fonts must be named with their weights and sizes, because a diagram that says 'a bold font' leaves the choice to whoever builds it, and a font that is not installed will be silently substituted, which changes the design.",
           command="Describe"),
        EQ("Explain why a logo should be created as a vector graphic rather than a raster graphic.", 3,
           [MP("A vector is stored as shapes and paths, not pixels", ["shapes", "paths", "maths", "points", "not pixels"]),
            MP("So it scales to any size without losing quality", ["scale", "any size", "no loss", "sharp", "enlarge"]),
            MP("A logo is used at many sizes, from favicon to signage", ["many sizes", "favicon", "sign", "van", "banner", "small and large"])],
           "A vector graphic is stored as shapes and paths described mathematically, rather than as a fixed grid of pixels. That means it can be scaled to any size and redrawn perfectly sharp every time, whereas a raster logo blurs and shows jagged edges when enlarged. A logo is used at almost every size there is, from a 16 pixel browser icon to a shop sign or the side of a van, so only a vector master can serve all of those uses from one file.",
           command="Explain"),
        EQ("A client wants an A4 poster. The photograph they supplied is 1200 by 800 pixels.\n\nExplain the problem this causes, and what the designer should do.", 4,
           [MP("A4 at 300 dpi needs about 2480 pixels across", ["2480", "300 dpi", "A4 needs", "pixels across", "resolution"]),
            MP("The photo would print too small, or too low a resolution if stretched", ["too small", "102", "145", "low resolution", "stretch"]),
            MP("It would look blurred or pixelated", ["blur", "pixel", "soft", "jagged", "poor quality"]),
            MP("A solution: a larger original, a smaller placement, or a different image", ["larger", "higher resolution", "original", "smaller", "reshoot", "different image", "ask the client"])],
           "Printed at the 300 dpi expected for print, A4 needs about 2480 pixels across its width, so a photograph 1200 pixels wide would only print about 10 centimetres wide. Stretched to fill the width it would drop to around 145 dpi, and because enlarging cannot add detail, it would look soft and blurred, with visible pixels in the detail. The designer should ask the client for the original, higher resolution file, or source or shoot a different image that is large enough, or redesign the layout so the photograph is used at a smaller size where its resolution is sufficient.",
           command="Explain"),
    ],
)

# ================================================================ R094 TA3

M_R094_GRAPHICS = Topic(
    slug="creating-digital-graphics",
    title="R094 TA3: Creating the Visual Identity and Digital Graphics",
    spec="R094 TA3",
    icon="i-image",
    minutes=28,
    exam_title=NEA,
    blurb="The vector and raster techniques to create the logo and the graphic, evidenced properly, then saving and exporting each file for its destination and checking it before it is finished.",
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
        Section("Raster techniques", """
Raster software: Photoshop, GIMP, Affinity Photo or Photopea. This is where photographs are handled.

| Technique | Why it is the right way |
| **Layers** | Elements stay separate and editable |
| **Adjustment layers** | Colour and tone changes that can be altered or removed later |
| **Layer masks** | Hiding part of a layer without deleting it |
| **Selections** | Marquee, lasso, colour range, and refining an edge |
| **Crop and resize** | Resampling knowingly rather than by accident |
| **Levels and curves** | Correcting exposure and contrast properly |
| **Retouching** | Clone and healing tools, used sparingly |
| **Text and typography** | Live text in the identity's fonts, kept editable |
| **Filters and effects** | Applied on their own layer, at a judged opacity |

**Non-destructive editing** means the original pixels are never overwritten: adjustments live on their own layers, and masks hide rather than delete. It is the difference between a file you can revise and a file you have to redo.

### Evidencing what you did

Screenshots of the process, with the tool, the settings and the reason, are the evidence that you used a technique and understood it.

!diagram r094-technique-evidence
"""),
        Section("Saving and exporting", """
| Keep | Why |
| The **layered working file** (.svg, .psd, .xcf, .afdesign) | It is the only version that can be meaningfully changed |
| **Every version**, numbered | So a rejected direction can be recovered |
| **Exports** for each destination | Print, web and social media each need their own |

!diagram r094-export-settings

### Export settings come from the destination

| Destination | Format | Settings |
| Commercial print | PDF | CMYK, 300 dpi, bleed included, fonts embedded |
| Website or app | PNG or SVG for graphics, JPG for photographs | RGB, exact pixel dimensions, compressed |
| Social media | JPG or PNG | RGB, the platform's pixel dimensions |
| Logo for the client | SVG, plus PNG with transparency | A full-colour and a one-colour version |

A naming convention that sorts correctly, such as `spokes-logo-v04-horizontal.svg`, and no file called "final".
"""),
        Section("Checking the graphic before it is finished", """
- View it at **100%** and at the **final physical size**, not just zoomed in.
- Print a **proof** if it is going to print; screen colour can mislead.
- Check the logo at **16 pixels** and in **one colour**.
- Check the **contrast** of any text placed on an image.
- Compare it with the **visualisation diagram** and the **brief**, point by point, and explain any change you made from the plan.
- Open the exports on a **different machine**, which is how missing font problems are found.

!warn Keep the reasons for changes :: A graphic that differs from its visualisation diagram is fine, and often better. A change that is not explained looks like the plan was ignored; a change with a reason ("the address competed with the logo, so I moved it into the call to action") shows the design is being judged.
"""),
        Section("Sources and further reading", OCR_LINKS + """
- [Inkscape](https://inkscape.org/): free vector software for logos and scalable graphics.
- [GIMP](https://www.gimp.org/): free raster image editing, with layers and masks.
- [Photopea](https://www.photopea.com/): a free image editor that runs in the browser and opens PSD files.
- [Google Fonts](https://fonts.google.com/): typefaces with licences that allow commercial use.
"""),
    ],
    keyterms=[
        ("Boolean operation", "Combining shapes using union, difference, intersection or exclusion."),
        ("Node editing", "Adjusting the individual points of a vector path to shape a curve."),
        ("Non-destructive editing", "Editing with layers, masks and adjustment layers so original pixels are never overwritten."),
        ("Layer mask", "A greyscale layer that hides part of another layer without deleting it."),
        ("Adjustment layer", "A colour or tone change stored as its own editable layer."),
        ("Convert to paths", "Turning editable text into vector outlines so it no longer needs the font."),
        ("Working file", "The layered master file from which every export is produced."),
        ("Export", "Saving a copy of the work in a format and with settings suited to one destination."),
        ("Proof", "A test print used to check colour and detail before a full run."),
        ("Naming convention", "A consistent pattern for file names, including a version number."),
    ],
    grade="""
+ Work non-destructively, so every change can be revised rather than redone
+ Evidence a genuine range of techniques, not one tool used repeatedly
+ Show the tool, the settings, the result and the reason for each technique
+ Keep the layered master and export separately for each destination, with the right settings
+ Check the graphic at its real size, in one colour and against the brief, and explain any change from the plan
""",
    mistakes=[
        "Editing pixels directly instead of using adjustment layers and masks.",
        "Delivering a logo only as a JPG, with no vector master and no transparency.",
        "Judging a design only while zoomed in.",
        "Converting text to paths with no editable copy kept.",
        "Overwriting the layered master with a flattened export.",
        "Screenshots of finished work with no evidence of how it was made.",
    ],
    quiz=[
        Q("Which Boolean operation cuts one shape out of another?",
          ["Difference", "Union", "Intersection", "Exclusion"], 0,
          "A crescent, a hole or a counter is usually made with difference."),
        Q("What is non-destructive editing?",
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
          ["The layered vector file", "A flattened JPG", "A PNG export",
           "A screenshot"], 0,
          "Every export comes from the master, which keeps everything needed to make changes."),
        Q("What does a layer mask do?",
          ["Hides part of a layer without deleting it", "Locks a layer",
           "Merges two layers", "Changes a layer's colour"], 0,
          "Masking is reversible; deleting is not."),
        Q("Which export suits a poster going to a commercial printer?",
          ["A PDF in CMYK at 300 dpi with bleed", "A JPG at 72 dpi in RGB",
           "A GIF", "A screenshot of the design"], 0,
          "Print needs CMYK, high resolution, bleed and embedded fonts."),
        Q("Why open your exports on a different machine?",
          ["It reveals missing fonts and broken links", "It compresses the file",
           "It converts the colour mode", "It is required by law"], 0,
          "Problems caused by assets that exist only on your own computer appear immediately."),
        Q("Which file name follows a good naming convention?",
          ["spokes-poster-v07.psd", "poster FINAL new (2).psd",
           "Untitled-1.psd", "my work.psd"], 0,
          "Lower case, no spaces, says what it is, and has a version number."),
        Q("Where should a filter effect be applied?",
          ["On its own layer, at a judged opacity", "Directly to the image layer",
           "To the whole file at export", "Before any other editing"], 0,
          "On its own layer it can be reduced or removed; applied directly it cannot."),
        Q("What is the best evidence that you used a technique and understood it?",
          ["Screenshots of the tool, settings and result, with your reason",
           "A screenshot of the finished graphic", "A list of the software used",
           "The file size of the export"], 0,
          "The process and the reasoning are what show understanding."),
    ],
    exam=[
        EQ("Explain why a designer works non-destructively when editing a photograph.", 3,
           [MP("Original pixels are not altered", ["original", "pixels", "not changed", "preserved", "intact"]),
            MP("Changes can be adjusted or removed later", ["adjust", "undo", "remove", "change later", "revise"]),
            MP("The consequence of destructive editing", ["start again", "cannot undo", "redo", "from the original", "lost"])],
           "Working non-destructively means the edits live on their own layers, as adjustment layers and masks, rather than being baked into the image, so the original pixels are never overwritten. That matters because design is iterative: a client asking for the crop to be less tight or the colour to be warmer is a two minute change on a masked, layered file. If the same edits had been applied directly to the pixels and the file flattened, the only way to make that change is to go back to the original photograph and redo every step.",
           command="Explain"),
        EQ("Describe how a poster should be saved and exported for printing and for social media.", 4,
           [MP("The layered master is kept and never overwritten", ["master", "layered", "working file", "keep", "not overwrite"]),
            MP("Print: PDF, CMYK, 300 dpi, bleed or fonts embedded", ["PDF", "CMYK", "300", "bleed", "embed"]),
            MP("Social media: JPG or PNG, RGB, the platform's pixel size", ["JPG", "PNG", "RGB", "1080", "pixels", "compressed"]),
            MP("A naming convention with version numbers", ["naming", "version", "v0", "convention", "file name"])],
           "The layered master file is saved first and kept, so every export comes from it and it is never overwritten by a flattened copy. For printing, the poster is exported as a PDF in CMYK at 300 dpi, with the bleed included and the fonts embedded, so the printer reproduces it exactly. For social media, a separate copy is exported as a JPG or PNG in RGB at the platform's pixel dimensions, such as 1080 by 1080, and compressed so it loads quickly. Every file follows a naming convention with a version number, so it is clear which is which and nothing is ever called final.",
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

# =========================================================== R094 TASK 1

M_R094_TASK1 = Topic(
    slug="r094-task-1-visual-identity",
    title="R094 Task 1 Guide: Designing the Identity and Planning the Graphic",
    spec="R094 Task 1",
    icon="i-flag",
    minutes=22,
    exam_title=NEA,
    blurb="What Task 1 of the R094 set assignment asks for: design concepts for the visual identity, their justification, and the planning documents for the digital graphic. Step by step, with a worked example on an invented brief.",
    fact="The Nike swoosh was designed in 1971 by Carolyn Davidson, a graphic design student at the time, for a fee of 35 dollars.",
    sections=[
        Section("What Task 1 asks you to do", """
R094 is assessed by an **OCR-set assignment**: a brief from a fictional client, with tasks to complete. Your teacher marks it, OCR moderates the marking, and it is worth a quarter of the qualification. Your teacher gives you the current assignment. Its wording, its tasks and its marking grid are what you are assessed against, so read them first and keep them open while you work.

!diagram r094-tasks-map

Task 1 assesses Topic Area 1 and the planning in Topic Area 2. On OCR's current recording sheet it is worth 20 of the unit's 50 marks, across three criteria: how **suitable your design concepts** are, how well you **justify** that they are fit for purpose, and your **planning documentation**. In outline:

| Part | What you produce |
| Interpret the client's requirements | The business type, brand values, target audience, purpose and constraints, in your own words |
| Research and generate ideas | Analysed research, a mind map and an annotated mood board |
| Design concepts | Different concepts for the visual identity, the chosen one developed and refined |
| Justify the designs | How each decision meets the client's requirements and suits the audience |
| Plan the digital graphic | A visualisation diagram, an asset table with sources and licences, and any other planning document the assignment asks for |
"""),
        Section("Step by step", """
1. **Read the brief twice.** Highlight everything the client says they want, and everything they imply. List the constraints.
2. **Write the client's requirements in your own words**: business type, brand values, target audience, purpose, and what must appear.
3. **Research, and analyse it.** Three or four competitors, each with a comment on what its identity communicates and what gap that leaves for your client.
4. **Mind map and mood board.** Annotate the mood board: why each colour, image and typeface is there.
5. **Sketch widely.** At least six quick thumbnails, then three genuinely different concepts.
6. **Judge the concepts against the brief**, choose one, and refine it until it works small and in one colour.
7. **Define the identity**: the logo and its versions, the palette as exact values, the typefaces with their licences, the slogan.
8. **Justify every decision** from the brief: the business, the values, the audience.
9. **Plan the digital graphic**: a visualisation diagram with exact sizes, colour values, fonts and positions, and the reason for each.
10. **Complete the asset table**: every image, font and other asset, with its source and licence, as you find it.

!key Your own words, all the way through :: Copying the brief back out shows nothing. Explaining what the client needs, including what the brief only implies, is the first evidence that you understand the task.
"""),
        Section("A worked example on a different brief", """
These extracts use an invented client, **Spokes**: a community bike repair workshop run by volunteers, whose brand values are friendly, sustainable and practical, and whose audience is local commuters, students and families. Do not copy them. Your client is different, and it is your decisions that are assessed.

!info Interpreting the requirements :: Spokes is a not-for-profit workshop, so the identity must feel welcoming rather than expert: most bike shops look technical and expensive, which would put off the families and students Spokes most wants to reach. The brief asks for something that works on a shop sign, on stickers and on social media, so the logo has to read at a few centimetres across and in one colour.

!diagram r094-logo-development

!diagram r094-style-guide

!info Justifying the palette :: Spokes Green carries the environmental message and is calm enough for long passages of text. Chain Orange is used only for calls to action, so on every poster it means 'do this'. I rejected black and grey, the colours most cycle shops use, because they read as specialist and expensive, the opposite of the welcome the brief asks for.

!info Justifying the typefaces :: Poppins Bold for headings, because its round letters feel friendly and stay legible on a sign at a distance. Source Sans 3 for body text, because it is clear at small sizes on stickers and phones. Both are free for commercial use under the SIL Open Font Licence, which is recorded in my asset table.

The client also needs an A4 poster for free repair Saturdays. This is the plan for it, which Task 2 then builds:

!diagram r094-poster-visualisation
"""),
        Section("What makes it strong", """
| Weaker evidence | Stronger evidence |
| The brief copied out | The brief interpreted: the implied needs and the constraints, in your own words |
| A page of screenshots | Each example analysed: what it communicates, and what that means for this client |
| One logo idea, polished | Three different concepts judged against the brief, and one refined |
| "I chose green because it looks nice" | "Green, because the brand values are sustainable and friendly, and the audience..." |
| Colours named and fonts described | Exact values, named typefaces, and their licences recorded |
| The final logo only | The development: each version, and why it changed |
| "A poster, blue, big title" | A visualisation diagram with exact sizes, values, fonts and positions, each explained |
| Assets listed by file name | Every asset with its source and licence, fonts included |
"""),
        Section("Before you hand in", """
+ The client's requirements are in your own words, including what the brief implies
+ The research is analysed, not just collected
+ The mood board is annotated
+ There are at least three genuinely different concepts, with the development of the chosen one shown
+ The identity has exact colour values, named typefaces with their licences, and the logo's versions
+ Every decision is justified from the brief: business, values, audience
+ The visualisation diagram gives exact sizes, colour values, fonts and positions, with reasons
+ The asset table records the source and licence of every asset that is not your own
+ The work is your own, and anything you used from elsewhere is acknowledged
"""),
        Section("Sources and further reading", OCR_LINKS + """
- [R094 unit recording sheet (PDF)](%s): the form on which your teacher records the marks for each part of R094.
- [JCQ: artificial intelligence](https://www.jcq.org.uk/exams-office/malpractice/artificial-intelligence/): the rules on AI tools in coursework.
- [Adobe Color](https://color.adobe.com/create/color-wheel) and [Google Fonts](https://fonts.google.com/): for building and recording a palette and choosing licensed typefaces.
""" % URS_R094),
    ],
    keyterms=[
        ("OCR-set assignment", "A brief with a fictional client and tasks, written by OCR, completed and marked in your school."),
        ("Moderation", "OCR checking a sample of a school's marking against the national standard."),
        ("Brand values", "The qualities an organisation wants to be known for."),
        ("Concept", "A distinct design idea, developed far enough to be judged against the brief."),
        ("Justification", "A reason for a design decision, taken from the brief, the audience or the research."),
        ("Visualisation diagram", "An annotated plan of a static graphic, detailed enough to work from."),
        ("Asset table", "A record of every asset with its source, format, dimensions and licence."),
    ],
    grade="""
+ Work from your current assignment and its marking grid, not from memory
+ Interpret the brief in your own words, including what it implies
+ Show alternatives and development, not just the final logo
+ Define the identity exactly, and justify every decision from the brief
+ Plan the graphic with exact, annotated decisions, and complete the asset table as you go
""",
    mistakes=[
        "Starting to design before the brief has been interpreted.",
        "Copying wording or designs from examples, including the ones on this site.",
        "Showing only the final logo, with no alternatives or development.",
        "Justifying choices by taste: 'I like it' or 'it looks modern'.",
        "Forgetting to record the source and licence of images and fonts.",
    ],
    quiz=[
        Q("Which topic areas does R094 Task 1 assess?",
          ["TA1, and the planning in TA2", "TA3 only",
           "TA2 and TA3", "None: it is a practice task"], 0,
          "Task 1 designs the identity and plans the graphic; Task 2 creates them."),
        Q("What should you read first, and keep open while you work?",
          ["Your current set assignment and its marking grid",
           "A previous student's work", "This website's examples",
           "The R093 exam paper"], 0,
          "The assignment's own wording and grid are what you are assessed against."),
        Q("How should the client's requirements be presented?",
          ["In your own words, including what the brief implies",
           "Copied exactly from the brief", "As a list of your favourite designs",
           "They do not need to be presented"], 0,
          "Interpreting the brief is the first evidence that you understand the task."),
        Q("Why keep the logo concepts you rejected?",
          ["They are evidence that you explored alternatives",
           "They make the file bigger", "The client might use all three",
           "They are needed for Task 2"], 0,
          "Exploring alternatives and developing one is part of what is assessed."),
        Q("Which justification is strongest?",
          ["Green, because the brand values are sustainable and friendly",
           "Green, because it is my favourite colour",
           "Green, because it looks modern", "Green, because it was quick"], 0,
          "A reason taken from the brief beats a reason taken from taste."),
        Q("Which planning document belongs in Task 1?",
          ["A visualisation diagram of the digital graphic",
           "The exported print PDF", "A screenshot of the finished poster",
           "A test log"], 0,
          "Planning documentation is one of Task 1's three criteria; Task 2 builds from it."),
        Q("What should an annotated mood board explain?",
          ["Why each colour, image and typeface is there",
           "Where each image was found, only", "How long it took",
           "Nothing: it should speak for itself"], 0,
          "Annotation turns a collage into evidence of thinking."),
        Q("Why do the examples on this site use an invented client?",
          ["To show the quality of evidence without answering anybody's real assignment",
           "Because OCR assignments are about bikes", "So they can be copied",
           "Because real clients are not allowed"], 0,
          "They show what good evidence looks like. Your decisions must be your own."),
    ],
    exam=[
        EQ("Explain why you should develop three different logo concepts before choosing one.", 3,
           [MP("Exploring alternatives is assessed or shows your design process", ["alternatives", "assessed", "marks", "process", "explore"]),
            MP("The first idea is rarely the best one", ["first idea", "not the best", "better", "compare"]),
            MP("Comparing them against the brief justifies the final choice", ["compare", "against the brief", "justify", "choose", "strongest"])],
           "Developing three genuinely different concepts shows that you explored alternatives, which is part of the design process the task assesses. It also produces better work, because the first idea is rarely the best, and seeing three side by side makes their strengths and weaknesses obvious. Judging each against the brief, its values, its audience and where the logo must work, then gives you a clear reason for the final choice, which is the justification the work needs.",
           command="Explain"),
        EQ("Describe the research you would carry out before designing a visual identity for a client.", 4,
           [MP("Competitor research, analysed", ["competitor", "rival", "similar businesses", "analys"]),
            MP("Sector conventions", ["convention", "sector", "expect", "industry", "similar"]),
            MP("Audience research", ["audience", "age", "interests", "survey", "who they are"]),
            MP("Visual research, such as colour, type and imagery, with notes", ["colour", "type", "font", "imagery", "mood board", "visual"])],
           "I would analyse three or four of the client's direct competitors, noting the colours, type and tone each uses, what that communicates, and what gap it leaves for my client. I would look at the conventions of the sector, because the audience already expects certain things of this kind of organisation, and the identity has to meet or deliberately break those expectations. I would research the target audience: who they are, what they respond to, and what would put them off. Finally I would gather visual research, colour, typefaces, textures and photographic styles, into an annotated mood board explaining why each piece is relevant.",
           command="Describe"),
        EQ("Explain why a designer completes an asset table while planning a digital graphic, rather than at the end.", 3,
           [MP("It records the source and licence of each asset", ["source", "licence", "where from", "permission"]),
            MP("Problems with an asset's licence are found early", ["early", "before", "replace", "cannot use", "unknown licence"]),
            MP("It avoids rebuilding or legal problems at the end", ["rebuild", "redo", "infringe", "legal", "deadline"])],
           "An asset table records where every image, font and other asset came from and the licence it is used under. Completing it while planning means any asset that cannot legally be used, such as a photograph with an unknown owner, is found before it has been built into the design. Discovering it at the end would mean replacing the asset and reworking the layout close to the deadline, or submitting work that infringes someone's copyright.",
           command="Explain"),
    ],
)

# =========================================================== R094 TASK 2

M_R094_TASK2 = Topic(
    slug="r094-task-2-digital-graphics",
    title="R094 Task 2 Guide: Creating the Identity and the Digital Graphic",
    spec="R094 Task 2",
    icon="i-flag",
    minutes=24,
    exam_title=NEA,
    blurb="What Task 2 of the R094 set assignment asks for: creating the visual identity and the digital graphic from your Task 1 plan, evidencing the techniques, and saving and exporting it properly. Step by step, with a worked example.",
    fact="Professional printers ask for 3 millimetres of bleed because guillotines cut stacks of hundreds of sheets at once, and a stack can shift by a millimetre or two. Bleed means a slightly wrong cut still looks right.",
    sections=[
        Section("What Task 2 asks you to do", """
Task 2 assesses Topic Area 3, applying what Topic Area 2 teaches about the properties of digital graphics. You **create** the visual identity and the digital graphic in software, from the plan you made in Task 1, and save and export them properly. On OCR's current recording sheet it carries 30 of the unit's 50 marks. Work from your current assignment and its marking grid: the product, its size and its audience come from the brief you were given.

| Part | What you produce |
| Set up from your plan | Documents with the size, resolution and colour mode the product needs |
| Create the identity | The logo and other identity elements, built in suitable software |
| Create the graphic | The product, built with a range of tools and techniques, following your plan |
| Evidence the process | The tools, settings and reasons for each technique, and any change from the plan explained |
| Save and export | The working files kept, and exports in formats and settings that suit the client's use |

!diagram r094-graphic-workflow
"""),
        Section("Starting from your plan", """
1. **Reread your Task 1 plan**: the visualisation diagram, the asset table, and the identity you designed.
2. **Confirm the technical properties** the product needs: the size in millimetres or pixels, the resolution, the colour mode, and the formats you will export.
3. **Gather the assets** from your asset table, and replace anything whose licence you could not clear.
4. **Keep the plan beside you** while you build, and note every change you make from it, with the reason.
"""),
        Section("Creating, step by step", """
1. **Set up the document from the plan**: size, resolution, colour mode and bleed.
2. **Build the logo in vector software**: shapes, paths, node editing and Boolean operations. Keep an editable version.
3. **Prepare the images in raster software**: crop, adjust and remove backgrounds with masks, non-destructively.
4. **Assemble the graphic** on a grid, following the visualisation diagram and applying the identity consistently.
5. **Check it**: at 100%, at its final size, printed as a proof, and against the brief. Explain any change from the plan.
6. **Save the layered master, then export** a version for each destination, named with a convention.

### Evidence of your process

- Screenshots of each technique: the **tool**, the **settings**, the **result**, and **why** you used it.
- **Before and after** images of edited photographs.
- Your **versions**, so the development is visible.
- The **reason for every change** from the visualisation diagram.

!key A range of techniques, each used for a reason :: Evidence of several different tools, each chosen for the job, shows more skill than one tool used over and over. Say why each was the right one.
"""),
        Section("A worked example on a different brief", """
The Spokes example continues: the client needs an A4 poster advertising free repair Saturdays, for print and for social media. Do not copy it; your product and your client are different.

!diagram r094-poster-anatomy

!info Explaining a change from the plan :: The visualisation diagram put the address in the top right corner. Built, it competed with the logo for attention, so I moved it into an orange pill under the details, where it completes the call to action and the eye finishes on it.

!info Explaining a technique :: I removed the background from my photograph of the bike with a layer mask rather than the eraser, so the background can be restored if the crop needs to change. The edge was refined at a 2 pixel radius so the wheels do not look cut out.
"""),
        Section("Before you hand in", """
+ The graphic follows your Task 1 plan, and every asset in it is in your asset table
+ The logo exists as an editable vector master
+ Your evidence shows a range of techniques, each with the tool, the settings and the reason
+ Every change from the plan is explained
+ The layered masters are saved, and each export suits its destination
+ Files follow a naming convention with version numbers
"""),
        Section("Sources and further reading", OCR_LINKS + """
- [R094 unit recording sheet (PDF)](%s): the form on which your teacher records the marks for each part of R094.
- [Inkscape](https://inkscape.org/), [GIMP](https://www.gimp.org/) and [Photopea](https://www.photopea.com/): free software for the vector and raster work.
- [GOV.UK: how copyright protects your work](https://www.gov.uk/copyright) and [Creative Commons licences](https://creativecommons.org/licenses/): for clearing the assets you use.
""" % URS_R094),
    ],
    keyterms=[
        ("Technique", "A particular use of a software tool to achieve an effect, such as masking or Boolean shaping."),
        ("Non-destructive editing", "Editing with layers, masks and adjustment layers so original pixels are never overwritten."),
        ("Layered master", "The working file, with its layers and live text, from which every export is made."),
        ("Export", "Saving a copy of the work in a format and with settings suited to one destination."),
    ],
    grade="""
+ Build from your Task 1 plan, and explain every change you make from it
+ Build the logo as a vector and edit images non-destructively
+ Evidence a range of techniques, each with the tool, the settings and the reason
+ Explain every change from the plan, and export properly for each destination
""",
    mistakes=[
        "Building the graphic before the visualisation diagram exists.",
        "Screenshots of the finished product only, with no evidence of how it was made.",
        "Leaving changes from the plan unexplained.",
        "Exporting one JPG for every use.",
        "Using an image found online with no source or licence recorded.",
    ],
    quiz=[
        Q("Which topic areas does R094 Task 2 assess?",
          ["TA3, applying the properties from TA2", "TA1 only",
           "TA1 and the planning in TA2", "None: it is a practice task"], 0,
          "Task 2 creates the identity and the graphic from the Task 1 plan."),
        Q("What do you build the graphic from in Task 2?",
          ["Your Task 1 plan: the visualisation diagram and the asset table",
           "A previous student's poster", "Whatever looks good on the day",
           "The R093 exam paper"], 0,
          "The plan is assessed in Task 1, and building from it saves time in Task 2."),
        Q("Which software should the logo be built in?",
          ["Vector software", "Raster software", "A word processor",
           "Spreadsheet software"], 0,
          "Vector shapes scale to any size; the logo has to work everywhere."),
        Q("What makes evidence of a technique strong?",
          ["The tool, the settings, the result and the reason",
           "The finished graphic alone", "The software's name",
           "The time it took"], 0,
          "It shows the skill and the understanding behind it."),
        Q("Your graphic differs from its visualisation diagram. What should you do?",
          ["Explain the change and the reason for it",
           "Change the diagram so they match", "Hide the difference",
           "Start again from the plan"], 0,
          "A change with a reason shows you are judging the design."),
        Q("Why save the layered master as well as the exports?",
          ["It is the only file that can be changed properly later",
           "Exports cannot be opened", "It is smaller", "It is required by law"], 0,
          "Exports are flattened; the master keeps layers, masks and live text."),
        Q("Which is the best way to remove a photograph's background?",
          ["A layer mask, so the background can be restored",
           "The eraser tool", "Painting over it in white",
           "Cropping it out"], 0,
          "Masking is non-destructive; erasing is not."),
        Q("What should every row of the asset table include?",
          ["The source and the licence", "Only the file name",
           "The colour of the asset", "The date you finished"], 0,
          "Those columns prove the asset can legally be used."),
    ],
    exam=[
        EQ("Describe the evidence you would include to show how you created a digital graphic.", 4,
           [MP("Screenshots of the tools and techniques used, with settings", ["screenshot", "tool", "setting", "technique"]),
            MP("Before and after images, or stages of the work", ["before", "after", "stages", "progress", "versions"]),
            MP("The reason each technique was used", ["why", "reason", "explain", "justify"]),
            MP("Changes from the plan explained, or file versions and exports shown", ["change", "plan", "version", "export", "naming"])],
           "I would include screenshots of each technique as I used it, showing the tool and its settings, such as the layer mask used to remove a background or the Boolean operation used to cut the logo shape. I would show the stages of the work with before and after images, and numbered versions, so the development is visible. Each screenshot would be annotated with why I chose that technique for that job. I would also explain every change I made from my visualisation diagram, and show the master file and the exports I produced for each destination.",
           command="Describe"),
        EQ("Explain why a logo is built in vector software, while photographs are edited in raster software.", 4,
           [MP("Vector graphics are shapes and paths, so they scale without losing quality", ["shapes", "paths", "scale", "any size", "no loss"]),
            MP("A logo is used at many sizes, so it must scale", ["many sizes", "small", "large", "sign", "favicon", "van"]),
            MP("Photographs are made of pixels, captured by a camera", ["pixels", "camera", "photograph", "continuous tone", "detail"]),
            MP("Raster software has the tools to edit pixels: masks, adjustments, retouching", ["mask", "adjust", "levels", "retouch", "selection", "layers"])],
           "A logo is built in vector software because a vector graphic is stored as shapes and paths rather than pixels, so it can be scaled to any size without losing quality, and a logo has to work at every size from a 16 pixel icon to a shop sign. A photograph is different: it is captured by a camera as millions of pixels of continuous tone and detail, which cannot be described as simple shapes, so it is edited in raster software, which has the tools for working on pixels, such as selections, layer masks, adjustment layers and retouching.",
           command="Explain"),
    ],
)

# ================================================================ R097 TA1

M_R097_PLAN = Topic(
    slug="interactive-digital-media",
    title="R097 TA1: Planning Interactive Digital Media",
    spec="R097 TA1",
    icon="i-web",
    minutes=28,
    exam_title=NEA,
    blurb="Interactive means the user decides what happens, so you are not planning one experience but every route through it: the product, its structure, its screens, its interface and its assets.",
    fact="Interactive means the user controls what happens, and that single property changes everything about planning. You are not designing one path, you are designing every path somebody could take, including the ones you would never choose yourself.",
    sections=[
        Section("Types of interactive product and their structures", """
### What counts as interactive

Websites, apps, kiosks and exhibits, e-learning, interactive video, games, quizzes, virtual tours. The common property is that the user's choices change what happens next.

!diagram r097-product-types

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
| **Script** | Narration, dialogue and on-screen text |
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

!diagram r097-ui-conventions

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
        Section("Planning the assets and the build", """
### Choosing the software

| Product | Typical software |
| Website | A web editor or a site builder, or HTML and CSS written by hand |
| Kiosk or interactive presentation | Presentation software with hyperlinks, run in kiosk or show mode |
| App or prototype | A prototyping tool such as Figma, or an app builder |
| Game or quiz | A game engine or a quiz authoring tool |

Choose from what the client needs and the device it will run on, and say why. A kiosk running a presentation in show mode is a perfectly good product if it meets the brief.

### The asset table and the folder plan

Every image, sound, video and font is listed with its **source**, **format**, **dimensions or duration**, and **licence**, before it is used. Plan the **folder structure** too, `images/`, `audio/`, `video/`, so the product works when it is moved to another machine.

### The work plan

Tasks in order, with their **dependencies** (navigation before content, content before styling), **milestones**, and **contingency** time for the things that always take longer, such as recording audio.
"""),
        Section("Sources and further reading", OCR_LINKS + """
- [W3C: Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/) and the [WCAG quick reference](https://www.w3.org/WAI/WCAG22/quickref/): the accessibility standard, and how to meet each part.
- [WebAIM contrast checker](https://webaim.org/resources/contrastchecker/): test any pair of colours against the contrast requirements.
- [GOV.UK Design System](https://design-system.service.gov.uk/): tested, accessible patterns for buttons, forms and navigation.
- [Nielsen Norman Group: 10 usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/): the principles behind interfaces people find easy.
- [diagrams.net](https://app.diagrams.net/): free for navigation diagrams and wireframes.
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
+ Choose the product and its structure from the client's purpose and audience, and justify both
+ Produce a navigation diagram covering every screen, with no dead ends or orphans
+ Wireframe every distinct screen, including the error and confirmation states
+ Annotate each wireframe with what every control does and where it leads
+ Plan accessibility in, rather than retrofitting it
+ Complete the asset table, folder plan and test plan before building
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
          "4.5:1 for normal text and 3:1 for large text, under the WCAG AA standard."),
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
        Q("Why plan a folder structure such as images/ and audio/ before building?",
          ["So the product still works when it is moved to another machine",
           "Folders make files smaller", "It hides the assets",
           "Software requires exactly those names"], 0,
          "Organised folders and relative paths keep every link working wherever the product runs."),
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

# ================================================================ R097 TA2

M_R097_MAKE = Topic(
    slug="creating-and-testing-interactive-media",
    title="R097 TA2: Creating Interactive Digital Media",
    spec="R097 TA2",
    icon="i-tools",
    minutes=26,
    exam_title=NEA,
    blurb="Building the product in the right order, preparing and optimising every asset, making the interactivity work, and saving and exporting the product so it runs where the client needs it.",
    fact="The first web page, published by Tim Berners-Lee in 1991, had no images at all: only text and hyperlinks. The link, not the picture, is what made it interactive.",
    sections=[
        Section("Building in the right order", """
1. **Structure first.** Create every screen and wire up the navigation with placeholder content. The product should be clickable end to end before anything looks finished.
2. **Content next.** Drop in the real text, images, audio and video.
3. **Styling last.** Apply the look once the structure has stopped moving.
4. **Test throughout.** Not as a final stage.

Styling before the structure is settled means restyling everything when it changes, which is where most of the wasted time in this unit goes.

!diagram r097-build-stages

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
        Section("Preparing and optimising assets", """
Assets almost never arrive the right size or format. **Repurposing** them, cropping, resizing, converting, trimming and compressing, is part of the skill being assessed.

!diagram r097-asset-pipeline

| Asset | Format for the product | Why |
| Photograph | JPG, about as wide as it will be shown | Lossy compression keeps photographs small |
| Logo, icon, line art | SVG, or PNG with transparency | Sharp edges, transparent backgrounds |
| Narration and sound effects | MP3 or AAC | Small files that every device plays |
| Video | MP4 (H.264) at the size it is shown | Plays almost everywhere, efficiently compressed |
| Captions | A text track, or captions burned in | Accessibility, and viewers with the sound off |

!warn A product is only as fast as its biggest file :: A 10 MB photograph shown 800 pixels wide makes every visit slow and every screen sluggish. Resize to the display size first, then compress, and check the quality by eye.
"""),
        Section("Making it interactive", """
| Element | What it does | Get it right by |
| **Buttons and links** | Move between screens or trigger an action | Clear labels that say what happens |
| **Navigation bar or menu** | Reaches the main sections from anywhere | The same place on every screen |
| **Rollovers and pressed states** | Show that something can be, or was, pressed | A visible change on hover, press and focus |
| **Hotspots** | Make part of an image respond | Big enough to hit, and signposted |
| **Forms and text input** | Collect answers or details | Labels, validation, and a confirmation |
| **Quizzes** | Test the user and respond | Feedback on every answer, and a score |
| **Media controls** | Play, pause and replay sound and video | Visible controls, captions, no autoplay with sound |
| **Show and hide** | Reveal extra content on demand | A clear control, and the content moves nothing else unexpectedly |

Every interaction should give **feedback**: a pressed state, a sound, a message or a new screen. A tap that appears to do nothing gets tapped again, which is how users break things.
"""),
        Section("Saving, exporting and publishing", """
The product has to run where the client needs it, on the device and in the software they have.

| Product | How it is delivered |
| Website | A folder of HTML, CSS, images and media, opened from `index.html`, with relative paths throughout |
| Kiosk or presentation | A show-mode file, or a PDF with working links, that opens straight into the first screen |
| Prototype | An exported or shared version that opens without editing tools |
| Game | An exported build that runs without the editor |

- Keep the **source** project as well as the exported product.
- Use a **naming convention** and **version numbers**: `garden-kiosk-v05`.
- **Test the exported version**, not just the one in the editor, on the device it is meant for, because that is the version the client will use.
"""),
        Section("Sources and further reading", OCR_LINKS + """
- [MDN Web Docs](https://developer.mozilla.org/): reference and tutorials for HTML, CSS and JavaScript.
- [Audacity](https://www.audacityteam.org/): free audio recording and editing.
- [Shotcut](https://shotcut.org/): free video editing, including captions.
- [GIMP](https://www.gimp.org/) and [Photopea](https://www.photopea.com/): free image editing for preparing assets.
- [Freesound](https://freesound.org/): sound effects under Creative Commons licences; check the licence of each one.
"""),
    ],
    keyterms=[
        ("Repurposing", "Changing an asset's size, format or content so it suits the product."),
        ("Optimisation", "Reducing asset file sizes so a product loads quickly without visible quality loss."),
        ("Relative path", "A file path given relative to the current file, so the product works on any machine."),
        ("Hotspot", "An area of an image or screen that responds when it is selected."),
        ("Rollover", "A change in appearance when the pointer moves over an element."),
        ("Feedback", "A visible or audible response confirming that an action registered."),
        ("Export", "Producing a version of the product that runs without the editing software."),
    ],
    grade="""
+ Build the structure first, style last, and test throughout
+ Repurpose and optimise every asset, and record what you changed
+ Evidence a genuine range of techniques across text, image, audio, video and interaction
+ Make every interaction give feedback, and implement accessibility for real
+ Export the product so it runs where the client needs it, and test that version
""",
    mistakes=[
        "Styling before the structure is complete, which means restyling it all later.",
        "Using absolute file paths, so nothing works on another machine.",
        "Dropping full-size photographs and videos straight into the product.",
        "Buttons that give no feedback when pressed.",
        "Testing only inside the editing software, never the exported product.",
        "Keeping only the exported product and losing the source files.",
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
        Q("What does optimising assets achieve?",
          ["Faster loading with no visible quality loss",
           "Better colour accuracy", "Easier editing", "Smaller screen sizes"], 0,
          "Oversized assets make an interactive product slow, which loses users fastest."),
        Q("Which format suits a logo with a transparent background on a screen?",
          ["SVG or PNG", "JPG", "MP3", "MP4"], 0,
          "JPG cannot store transparency."),
        Q("What is a hotspot?",
          ["An area of an image that responds when selected",
           "A wireless network", "A very bright colour",
           "A broken link"], 0,
          "Hotspots make parts of a picture interactive, such as each animal on a map."),
        Q("Why should every button give feedback when pressed?",
          ["Otherwise users tap again and think it is broken",
           "It makes the file smaller", "It is needed for printing",
           "It hides the navigation"], 0,
          "Feedback confirms the action registered."),
        Q("Which version of the product should be tested before delivery?",
          ["The exported version, on the device it is meant for",
           "Only the version in the editor", "Neither", "A screenshot of it"], 0,
          "The exported version is what the client will actually run."),
        Q("A 6000 pixel photo will be shown 800 pixels wide. What should be done first?",
          ["Resize it close to 800 pixels wide, then compress it",
           "Use it as it is", "Convert it to a GIF", "Print it"], 0,
          "Resizing first removes millions of pixels nobody will ever see."),
        Q("Which audio format is best for narration in a product?",
          ["MP3 or AAC", "Uncompressed WAV", "MIDI", "PDF"], 0,
          "Compressed audio is small and plays on almost every device."),
        Q("Why is breadth of techniques important in this unit?",
          ["The criteria ask for a range of skills",
           "One technique is never enough to build anything",
           "It makes the product longer", "It is required by law"], 0,
          "Several techniques used competently evidence more than one used brilliantly."),
    ],
    exam=[
        EQ("Explain why assets should be optimised before they are added to an interactive product.", 3,
           [MP("Large files make the product slow to load or respond", ["slow", "load", "lag", "large", "wait"]),
            MP("Users abandon slow products", ["give up", "leave", "abandon", "frustrat", "lose users"]),
            MP("Optimising reduces file size with no visible loss of quality", ["resize", "compress", "smaller", "no visible", "quality"])],
           "Assets straight from a camera or recorder are far larger than the product needs: a photograph may be twenty times wider than the space it fills. Every one of those files has to load, so an unoptimised product is slow to open and slow to move between screens, and users, especially on phones or slow connections, give up on products that keep them waiting. Resizing each asset to the size it is shown at and compressing it reduces the file size dramatically with no loss of quality anyone can see.",
           command="Explain"),
        EQ("Describe how you would make an interactive product easy to navigate.", 4,
           [MP("A consistent navigation bar or Home button on every screen", ["consistent", "same place", "every screen", "home", "menu", "navigation bar"]),
            MP("Clear labels on buttons and links", ["label", "clear", "says what", "wording"]),
            MP("Feedback or visible states when controls are used", ["feedback", "pressed", "hover", "state", "response"]),
            MP("A shallow structure with routes back and no dead ends", ["shallow", "two taps", "back", "dead end", "breadcrumb"])],
           "I would put a navigation bar with a Home button in the same place on every screen, so the user always knows how to get back to the start. Every button and link would have a clear label saying exactly what it does or where it goes. Every control would show a visible pressed or hover state, so the user knows their action registered. And I would keep the structure shallow, with every screen no more than two or three taps from home and a route back from each, so nobody reaches a dead end.",
           command="Describe"),
    ],
)

# ================================================================ R097 TA3

M_R097_REVIEW = Topic(
    slug="reviewing-interactive-media",
    title="R097 TA3: Testing and Reviewing Interactive Digital Media",
    spec="R097 TA3",
    icon="i-check",
    minutes=26,
    exam_title=NEA,
    blurb="Testing the product against a plan, with real users and honest results, then reviewing it against the brief with evidence, and proposing improvements and further development.",
    fact="A usability study only needs about five participants to find most of the problems in a product. The sixth person mostly rediscovers what the first five already showed you, which is why professional testing rounds are small and repeated.",
    sections=[
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
5. **Further development**: how the product could grow beyond the brief, such as new features, content or platforms.
6. **Reflection on the process**: what you would plan differently, and why.

### Turning a weak review into a strong one

| Weak | Strong |
| "The navigation worked well." | "Four of five testers reached the booking screen in under three taps. The fifth looked for a 'Book' button in the top right, where the convention puts it, and did not find it in the menu; I would add a persistent booking button to the header." |
| "I would add more content." | "Each topic has text and one image. Two testers asked for sources, so I would add a short references panel under each topic, collapsed by default so it does not compete with the main text." |
| "It all went to plan." | "I styled the topic screens before the navigation was finished, so adding the video screen meant restyling three screens. Next time I would leave all styling until the structure is signed off." |

!grade Evidence every claim :: "It is easy to use" is an opinion. "Five of six testers completed the task without help, and the one who failed was looking for a search function that does not exist" is evidence. The review is marked on evidence.
"""),
        Section("Sources and further reading", OCR_LINKS + """
- [Nielsen Norman Group: why you only need to test with 5 users](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/): the research behind small, repeated usability tests.
- [W3C: easy checks for accessibility](https://www.w3.org/WAI/test-evaluate/preliminary/): simple accessibility tests anyone can carry out.
- [WebAIM contrast checker](https://webaim.org/resources/contrastchecker/): test text colours against the standard.
- [Nielsen Norman Group: 10 usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/): principles to review an interface against.
"""),
    ],
    keyterms=[
        ("Functionality testing", "Checking that every interactive element behaves as intended."),
        ("Usability testing", "Observing a real user attempting a task and recording where they struggle."),
        ("Compatibility testing", "Checking the product on different browsers, devices and screen sizes."),
        ("Test plan", "A document listing each test, the data used and the expected result, written before testing."),
        ("Review", "A judgement of the product against the brief, backed by evidence."),
        ("Further development", "How a product could be extended beyond the brief, such as new features or platforms."),
        ("Iteration", "Improving a product through repeated cycles of building, testing and refining."),
    ],
    grade="""
+ Record the expected result before each test, and log the failures with their fixes
+ Watch real users attempt a task rather than demonstrating the product yourself
+ Review against the brief requirement by requirement, with evidence
+ Quote user feedback, criticism included
+ Give specific improvements with the method and the expected effect, and suggest further development
""",
    mistakes=[
        "Testing only what already works.",
        "Writing the expected result after seeing the actual result.",
        "Evaluating by using the product yourself instead of watching someone else.",
        "A test log with no failures in it, which no assessor believes.",
        "Reviews that praise everything and improve nothing.",
        "Improvements with no explanation of how they would be made or what they would achieve.",
    ],
    quiz=[
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
        Q("Which test checks the product on different devices and screen sizes?",
          ["Compatibility testing", "Functionality testing",
           "Usability testing", "Content testing"], 0,
          "It catches a layout that only works on the machine it was built on."),
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
        Q("What is further development?",
          ["How the product could grow beyond the brief",
           "Fixing the bugs found in testing", "Writing the test plan",
           "Making the product shorter"], 0,
          "Improvements fix what is there; further development adds what could come next."),
        Q("Which is the best accessibility test for keyboard users?",
          ["Use the whole product with the keyboard only",
           "Check the colours look nice", "Ask a friend if it is accessible",
           "Count the screens"], 0,
          "Tab through every control and check each can be reached, used and seen."),
        Q("Why test with members of the target audience rather than friends?",
          ["They are representative and less likely to hold back criticism",
           "Friends are not allowed", "It is quicker",
           "Friends cannot use computers"], 0,
          "The review needs honest evidence from the people the product is for."),
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

# =========================================================== R097 TASK 1

M_R097_TASK1 = Topic(
    slug="r097-task-1-planning-interactive-media",
    title="R097 Task 1 Guide: Planning the Interactive Product",
    spec="R097 Task 1",
    icon="i-flag",
    minutes=22,
    exam_title=NEA,
    blurb="What Task 1 of the R097 set assignment asks for, how to plan the product step by step, a worked navigation diagram and wireframes on an invented brief, and the checks to make before you hand it in.",
    fact="The idea of a page of linked 'trails' through information was described by Vannevar Bush in 1945, in an essay called As We May Think, decades before the first website.",
    sections=[
        Section("What Task 1 asks you to do", """
R097 is assessed by an **OCR-set assignment** in three tasks, marked by your teacher and moderated by OCR, and it is worth 35% of the qualification. Your teacher gives you the current assignment; its wording and marking grid are what you are assessed against. In OCR's sample assignment, Task 1 carries 20 of the unit's 70 marks.

!diagram r097-tasks-map

Task 1 assesses Topic Area 1: planning the interactive product. In outline:

| Part | What you produce |
| Interpret the brief | The client's requirements, the purpose and the target audience, in your own words |
| Choose the product and structure | The kind of product and its navigation structure, justified |
| Plan the structure | A navigation diagram of every screen and link |
| Plan each screen | Wireframes or visualisation diagrams for every distinct screen, annotated with interactions |
| Plan the assets | An asset table: every asset, its source, format and licence |
"""),
        Section("Step by step", """
1. **Interpret the brief**: the client, the purpose, the audience, the content that must be included, and the constraints, including the device it will run on.
2. **Choose the product type and structure**, and justify both from the purpose and the audience.
3. **Draw the navigation diagram**: every screen a box, every link an arrow. Check it for dead ends, orphans and depth.
4. **Wireframe every distinct screen**, annotated with what each control does and where it leads, and the error and confirmation states.
5. **Plan the interface**: consistent navigation, clear labels, feedback, and accessibility from the start.
6. **Complete the asset table**: every image, sound, video and font, with source, format, size and licence.
7. **Plan the testing and the work**, if your assignment asks for them here: a test plan with expected results, and a work plan with dependencies.
"""),
        Section("A worked example on a different brief", """
The example is an invented client: **Castle Hill Community Garden** wants a touchscreen guide in its visitor hut, for families and older visitors, showing what is growing, the wildlife, events and a short quiz. Do not copy it; your brief is different.

!info Choosing the structure :: A hub and spoke structure, because visitors stand at the kiosk for a minute or two with no instructions: every section is one tap from Home, every screen carries a Home button, and the kiosk resets itself after a minute so the next visitor starts at the beginning. A hierarchical site with sub-menus would bury the content these visitors want most.

!diagram r097-garden-navigation

!diagram r097-garden-wireframes

!info An asset table row :: hedgehog-photo · image · own photograph, taken in the garden · JPG, 1600 × 1067 after resizing · own work, no licence needed · alt text: "A hedgehog under the hedge by the compost bins".
"""),
        Section("What makes it strong", """
| Weaker evidence | Stronger evidence |
| The brief copied out | The brief interpreted, including the device, the setting and the audience's needs |
| "I chose hub and spoke" | The structure justified from how and where the product is used |
| A diagram with screens missing | Every screen and link, including the error states and the timeout |
| One wireframe of the home screen | Every distinct screen, annotated with what each control does |
| An asset list of file names | Sources, formats, sizes and licences, with permissions where people appear |
"""),
        Section("Before you hand in", """
+ The brief is interpreted in your own words: client, purpose, audience, content, constraints
+ The product type and structure are justified
+ The navigation diagram shows every screen and link, with no dead ends or orphans
+ Every distinct screen has an annotated wireframe, including error and confirmation states
+ Accessibility is planned in: contrast, text size, alt text, captions, keyboard access
+ The asset table is complete, with a source and licence for every asset
+ The work is your own, and anything you used from elsewhere is acknowledged
"""),
        Section("Sources and further reading", OCR_LINKS + """
- [R097 unit recording sheet (PDF)](%s): the form on which your teacher records the marks for each R097 task.
- [diagrams.net](https://app.diagrams.net/): free for navigation diagrams and wireframes.
- [W3C: WCAG 2.2 quick reference](https://www.w3.org/WAI/WCAG22/quickref/): what accessibility requires, to plan in from the start.
- [JCQ: artificial intelligence](https://www.jcq.org.uk/exams-office/malpractice/artificial-intelligence/): the rules on AI tools in coursework.
""" % URS_R097),
    ],
    keyterms=[
        ("Navigation diagram", "A diagram of every screen in a product and the links between them."),
        ("Wireframe", "A layout plan of one screen showing placement without styling."),
        ("Attract loop", "A screen or sequence a kiosk shows while idle, inviting the next visitor to start."),
        ("Asset table", "A record of every asset with its source, format, size and licence."),
    ],
    grade="""
+ Interpret the brief, including the device and setting the product is used in
+ Justify the product and its structure from the purpose and the audience
+ Plan every screen and every link, and annotate the interactions
+ Plan accessibility and the assets before anything is built
""",
    mistakes=[
        "A navigation diagram that misses screens, such as errors and confirmations.",
        "Wireframes with no annotation of what the controls do.",
        "Choosing a structure without saying why.",
        "An asset table with no licences.",
        "Planning for a laptop when the brief says the product runs on a phone or a kiosk.",
    ],
    quiz=[
        Q("Which topic area does R097 Task 1 assess?",
          ["TA1: planning interactive digital media", "TA2: creating it",
           "TA3: reviewing it", "R093 content"], 0,
          "Task 1 plans, Task 2 creates, Task 3 tests and reviews."),
        Q("In OCR's sample assignment, how many of R097's 70 marks does Task 1 carry?",
          ["20", "70", "5", "50"], 0,
          "Check your own assignment's grid, because assignments are updated."),
        Q("What should a navigation diagram show?",
          ["Every screen and every link between them",
           "Only the home screen", "The colour scheme", "The file sizes"], 0,
          "It is the map of the whole product."),
        Q("Why annotate wireframes with what each control does?",
          ["It turns a picture into a specification someone could build from",
           "It makes the wireframe colourful", "It replaces the navigation diagram",
           "It is only needed for games"], 0,
          "Interactions are the point of an interactive product."),
        Q("Why does the kiosk in the worked example reset after a minute?",
          ["So the next visitor starts at the beginning",
           "To save electricity", "To delete the content",
           "Because kiosks cannot stay on"], 0,
          "A public product has to recover from being left mid-way."),
        Q("Which belongs in the asset table?",
          ["A photograph's source, format, size and licence",
           "The client's phone number", "The test results",
           "The navigation structure"], 0,
          "It is the record that every asset can be used."),
        Q("When should accessibility be planned?",
          ["From the start, in the planning documents",
           "After the build", "Only if the client asks", "Never"], 0,
          "Retrofitting accessibility means rework."),
        Q("What is the strongest justification for a hub and spoke structure on a kiosk?",
          ["Visitors stay briefly with no instructions, so every section is one tap from Home",
           "It is the easiest to draw", "All products should use it",
           "It needs fewer screens"], 0,
          "The reason comes from how and where the product is used."),
    ],
    exam=[
        EQ("Explain why every distinct screen of an interactive product should be wireframed, not just the home screen.", 3,
           [MP("Each screen has a different layout or purpose", ["different", "layout", "each screen", "purpose", "content"]),
            MP("Error and confirmation screens are often forgotten but seen by users", ["error", "confirmation", "forgotten", "users see"]),
            MP("Problems are found before building, saving rework", ["before building", "rework", "cheaper", "plan", "early"])],
           "Each distinct screen has its own layout and job, a content page, a form, a quiz question, a confirmation, so a wireframe of the home screen tells you nothing about how the others will work. The screens most often left unplanned, such as error and confirmation states, are ones users see constantly, and an unplanned one is where they give up. Wireframing every screen finds layout and interaction problems while they are still a sketch, rather than after content has been built into them.",
           command="Explain"),
        EQ("Describe what should be included in the plan for an interactive product.", 4,
           [MP("Interpretation of the brief: purpose, audience, requirements", ["brief", "purpose", "audience", "requirement", "client"]),
            MP("A navigation diagram", ["navigation", "structure", "every screen", "links"]),
            MP("Wireframes or visualisations of each screen", ["wireframe", "visualisation", "layout", "each screen"]),
            MP("An asset table, or a test plan or work plan", ["asset", "licence", "source", "test plan", "work plan"])],
           "The plan should start with an interpretation of the brief: the client's requirements, the purpose of the product and its target audience, in the student's own words. It needs a navigation diagram showing every screen and the links between them, checked for dead ends. Each distinct screen should be wireframed and annotated with what every control does. Finally there should be an asset table recording every image, sound and video with its source and licence, and a test plan with expected results written before building.",
           command="Describe"),
    ],
)

# =========================================================== R097 TASK 2

M_R097_TASK2 = Topic(
    slug="r097-task-2-creating-interactive-media",
    title="R097 Task 2 Guide: Creating the Interactive Product",
    spec="R097 Task 2",
    icon="i-flag",
    minutes=22,
    exam_title=NEA,
    blurb="What Task 2 of the R097 set assignment asks for, how to build the product step by step from your plan, how to evidence the process, and a worked example on an invented brief.",
    fact="Most usability problems in interactive products are found by watching people use them, not by reading the code. That is why professional teams test half-built versions with real users rather than waiting until the end.",
    sections=[
        Section("What Task 2 asks you to do", """
Task 2 assesses Topic Area 2: creating the interactive product from your plan, using a range of skills, and saving and exporting it so it runs. Work from your current assignment and its marking grid.

| Part | What you produce |
| Prepare the assets | Images, audio and video repurposed and optimised for the product |
| Build the structure | Every screen, with working navigation |
| Add the content and interactivity | Text, media and interactive features working together |
| Apply the design | The look from your plan, consistent across every screen |
| Save and export | The source project kept, and a version that runs where the client needs it |
"""),
        Section("Step by step", """
1. **Prepare the assets**: crop, resize, convert and compress images; trim and normalise audio; edit and compress video; write alt text and captions.
2. **Build the structure**: every screen from the navigation diagram, linked, with placeholders. Click through it end to end.
3. **Add the content**: the real text, images, audio and video, checked against the plan.
4. **Make it interactive**: buttons, menus, hotspots, forms, quizzes, media controls, each giving feedback.
5. **Style it last**: the colours, fonts and layout from your plan, applied consistently.
6. **Test as you go**: every link and feature as it is built, not only at the end.
7. **Save and export**: keep the source project, export a version that runs on the client's device, and test that version.

!diagram r097-build-stages
"""),
        Section("Evidence of your process", """
- **Screenshots of each pass**: the structure, the content, the finished design.
- **Screenshots of the tools and settings** you used for each technique: compressing an image, trimming audio, adding a hotspot, linking a button.
- **Before and after** for every asset you repurposed, with the file sizes.
- **The reasons** for any change from your plan.
- Your **versions**, saved with a naming convention.

!key Show the range :: Evidence of different skills, combining media, navigation, interactivity, audio and video editing, optimisation and accessibility, each used for a reason, shows more than one feature built many times.

!info An example of explaining a change from the plan :: The wireframe put the Listen button under the text. On the kiosk, shorter visitors could not see it without stepping back, so I moved it beside the photograph, where the first tester found it straight away.
"""),
        Section("Before you hand in", """
+ Every screen from the navigation diagram exists, and every link works
+ Assets are repurposed and optimised, with before and after evidence
+ A range of interactive features works, and each gives feedback
+ Accessibility is implemented: alt text, captions, contrast, keyboard access
+ The design is consistent across every screen
+ Changes from the plan are explained
+ The source project is saved, and the exported version runs on the target device
"""),
        Section("Sources and further reading", OCR_LINKS + """
- [R097 unit recording sheet (PDF)](%s): the form on which your teacher records the marks for each R097 task.
- [MDN Web Docs](https://developer.mozilla.org/): reference and tutorials for building web pages.
- [Audacity](https://www.audacityteam.org/) and [Shotcut](https://shotcut.org/): free audio and video editing.
- [WebAIM contrast checker](https://webaim.org/resources/contrastchecker/): check the colours you apply.
""" % URS_R097),
    ],
    keyterms=[
        ("Repurposing", "Changing an asset's size, format or content so it suits the product."),
        ("Optimisation", "Reducing file sizes so the product loads quickly without visible quality loss."),
        ("Interactivity", "Features that respond to the user, such as buttons, hotspots and quizzes."),
        ("Export", "Producing a version of the product that runs without the editing software."),
    ],
    grade="""
+ Build from the plan, structure first and styling last, testing as you go
+ Repurpose and optimise every asset, with evidence
+ Show a range of skills, each used for a reason, with screenshots of how
+ Explain changes from the plan, and export a version that runs where it should
""",
    mistakes=[
        "Building screens that are not in the plan, or leaving planned screens out without explanation.",
        "Full-size assets dropped straight into the product.",
        "Evidence of the finished product only, with nothing on how it was built.",
        "Interactive features that give no feedback.",
        "Never testing the exported version.",
    ],
    quiz=[
        Q("Which topic area does R097 Task 2 assess?",
          ["TA2: creating interactive digital media", "TA1: planning it",
           "TA3: reviewing it", "R094 content"], 0,
          "Task 2 is where the product is built."),
        Q("What should be built first?",
          ["Every screen, linked, with placeholder content", "The colour scheme",
           "The quiz questions", "The final video"], 0,
          "A product clickable end to end can be tested before anything is styled."),
        Q("What is good evidence of repurposing an asset?",
          ["Before and after, with the tool, settings and file sizes",
           "The finished asset only", "The asset's file name",
           "A description of the software"], 0,
          "It shows what was changed, how, and what it achieved."),
        Q("Why test as you build rather than only at the end?",
          ["Faults are found while they are cheap to fix", "It is required by law",
           "It makes the product longer", "Testing at the end is not allowed"], 0,
          "A broken link found as it is made takes seconds to fix."),
        Q("Which version must be tested before you hand in?",
          ["The exported version, on the target device", "Only the editor version",
           "None", "A printed copy"], 0,
          "The exported version is what the client would actually use."),
        Q("Your product differs from the wireframe. What should you do?",
          ["Explain the change and why it was made", "Redraw the wireframe to match",
           "Ignore it", "Delete the change"], 0,
          "A reasoned change shows judgement; an unexplained one looks like the plan was ignored."),
        Q("Which shows the widest range of skills?",
          ["Combining media, interactivity, audio and video editing, and optimisation",
           "Fifty buttons that all do the same thing", "One very long page of text",
           "A single video"], 0,
          "The criteria reward a range of skills, each used for a reason."),
        Q("What should every interactive feature do when used?",
          ["Give feedback, so the user knows it worked", "Play a loud sound",
           "Open a new window", "Nothing visible"], 0,
          "Feedback stops users tapping again and breaking things."),
    ],
    exam=[
        EQ("Explain why an interactive product should be built with its structure first and its styling last.", 3,
           [MP("Structure first makes the product testable end to end early", ["clickable", "end to end", "test", "early", "navigation works"]),
            MP("The structure often changes during building", ["changes", "add a screen", "move", "restructure"]),
            MP("Styling first means restyling when it changes, wasting time", ["restyle", "redo", "waste", "time", "again"])],
           "Building the screens and the navigation first, with placeholder content, gives a product that can be clicked through end to end almost immediately, so structural problems such as a dead end or a missing route back are found early. The structure nearly always changes while a product is being built, a screen is added or a section is moved, and if every screen had already been styled, each change would mean restyling several screens. Leaving styling until the structure is settled means it is done once.",
           command="Explain"),
        EQ("Describe the evidence you would include to show how you created an interactive product.", 4,
           [MP("Screenshots of the product at each stage", ["screenshot", "stage", "pass", "structure", "content"]),
            MP("Screenshots of tools and settings for each technique", ["tool", "setting", "technique", "software"]),
            MP("Before and after evidence of repurposed assets, with sizes", ["before", "after", "file size", "repurpos", "optimis"]),
            MP("Reasons for changes from the plan, or saved versions", ["change", "plan", "reason", "version"])],
           "I would include screenshots of the product at each stage of the build, the linked structure, the content added and the finished design, so the process is visible. For each technique I would show the tool and settings I used, such as the compression settings for a photograph or the link set on a button. For every asset I repurposed I would show it before and after, with its file size, to evidence the optimisation. I would also explain every change I made from my plan, with the reason, and keep numbered versions of the project.",
           command="Describe"),
    ],
)

# =========================================================== R097 TASK 3

M_R097_TASK3 = Topic(
    slug="r097-task-3-reviewing-interactive-media",
    title="R097 Task 3 Guide: Testing and Reviewing the Product",
    spec="R097 Task 3",
    icon="i-flag",
    minutes=22,
    exam_title=NEA,
    blurb="What Task 3 of the R097 set assignment asks for, how to test the product and review it step by step, a worked example of a usability test and a review point, and the checks before you hand it in.",
    fact="Testers often say a product is easy to use and then fail the task in front of you. That is why good usability testing records what people do, not just what they say.",
    sections=[
        Section("What Task 3 asks you to do", """
Task 3 assesses Topic Area 3: testing the product you built and reviewing it against the brief. Work from your current assignment and its marking grid.

| Part | What you produce |
| Test the product | A test plan carried out, with expected and actual results, failures, fixes and retests |
| Test with users | Real users from the audience attempting tasks, with what they did and said recorded |
| Review against the brief | Each requirement judged, with evidence from the tests and the feedback |
| Strengths and weaknesses | An honest account, with reasons |
| Improvements and further development | Specific changes, how they would be made and their effect, and how the product could grow |
"""),
        Section("Testing, step by step", """
1. **Use your test plan**, with the expected result written before each test is run.
2. **Test every function and route**: each button, link, hotspot, form and media control, and every screen reachable with a route back.
3. **Test the content**: spelling, accuracy, and everything the brief asked for being present.
4. **Test compatibility and accessibility**: the target device, other screen sizes, keyboard only, contrast, captions.
5. **Run usability tests**: give users from the audience a task, watch without helping, and record what they do and say.
6. **Record failures honestly**, fix them, and retest.

!diagram r097-user-testing
"""),
        Section("Reviewing, step by step", """
1. **Quote each requirement** from the brief.
2. **Give the evidence**: the test result, the user's time, the quote.
3. **Judge it**: met, partly met or not met, and why.
4. **Propose an improvement**: what you would change, how, and what effect it would have.
5. **Suggest further development**: where the product could go beyond the brief.
6. **Reflect on your process**: what you would plan differently next time.

!diagram r097-review-structure

!warn Praise without evidence scores nothing :: "It worked well" is an opinion. Evidence is a test result, a time, a number of users, a quotation. Every judgement in the review needs one.
"""),
        Section("Before you hand in", """
+ Every planned test is carried out, with expected results written first
+ Failures are recorded with their fixes and retests
+ Real users from the audience tested real tasks, and you recorded what they did and said
+ Every requirement in the brief is judged, with evidence
+ Strengths and weaknesses are honest and explained
+ Improvements say what, how and with what effect, and further development is suggested
+ The review is your own analysis, in your own words
"""),
        Section("Sources and further reading", OCR_LINKS + """
- [R097 unit recording sheet (PDF)](%s): the form on which your teacher records the marks for each R097 task.
- [Nielsen Norman Group: why you only need to test with 5 users](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/): how many testers you need, and why.
- [W3C: easy checks for accessibility](https://www.w3.org/WAI/test-evaluate/preliminary/): quick accessibility tests to include in your plan.
""" % URS_R097),
    ],
    keyterms=[
        ("Usability test", "Watching a user from the audience attempt a task, and recording what they do and say."),
        ("Retest", "Running a failed test again after a fix, to confirm the fix worked."),
        ("Review", "A judgement of the product against the brief, backed by evidence."),
        ("Further development", "How a product could be extended beyond the brief."),
    ],
    grade="""
+ Test against your plan, with expected results first and failures recorded
+ Test with real users from the audience, and record actions as well as opinions
+ Judge every requirement with evidence
+ Make improvements specific, and suggest further development
""",
    mistakes=[
        "Testing your own product and calling it user testing.",
        "Recording only the tests that passed.",
        "Feedback from friends, with no tasks set.",
        "A review that praises everything.",
        "Improvements with no method or effect.",
    ],
    quiz=[
        Q("Which topic area does R097 Task 3 assess?",
          ["TA3: reviewing interactive digital media", "TA1: planning it",
           "TA2: creating it", "R093 content"], 0,
          "Task 3 tests the product and reviews it against the brief."),
        Q("What makes a usability test useful?",
          ["A real user from the audience given a task, watched without help",
           "Showing a friend around the product", "Testing it yourself",
           "Asking 'do you like it?'"], 0,
          "Tasks and observation produce evidence; tours and opinions do not."),
        Q("Which is evidence for a review?",
          ["Four of five testers found the events in two taps",
           "It is easy to use", "It looks great", "I worked hard on it"], 0,
          "Evidence can be checked."),
        Q("A test fails. What should the record show?",
          ["The failure, the fix and the retest", "Nothing: delete the test",
           "Only that it passed in the end", "The tester's name only"], 0,
          "The whole sequence is evidence of a real testing process."),
        Q("What should a review do with each requirement in the brief?",
          ["Quote it, give evidence, and judge whether it was met",
           "Copy it out", "Ignore the ones not met", "List them at the end"], 0,
          "Requirement by requirement, with evidence, is the structure that scores."),
        Q("Which is a further development rather than an improvement?",
          ["A QR code so visitors can take event details home on a phone",
           "Renaming a confusing button", "Fixing a broken link",
           "Increasing text contrast"], 0,
          "Improvements fix what is there; further development extends the product."),
        Q("Why record what testers do as well as what they say?",
          ["People often say it is easy, then struggle with the task",
           "It is quicker", "Testers never speak", "It is required by law"], 0,
          "Behaviour is stronger evidence than opinion."),
        Q("Why test the product with the keyboard only?",
          ["To check it is accessible to users who cannot use a mouse or touchscreen",
           "Keyboards are faster", "To save battery", "Touchscreens are banned"], 0,
          "Keyboard access is a core accessibility requirement."),
    ],
    exam=[
        EQ("Explain how usability testing provides evidence for the review of an interactive product.", 4,
           [MP("Real users from the audience attempt set tasks", ["real user", "audience", "task", "attempt"]),
            MP("Their actions, times and difficulties are recorded", ["record", "time", "hesitat", "wrong tap", "observe"]),
            MP("This gives measurable evidence for judging requirements", ["measur", "evidence", "requirement", "judge", "four of five"]),
            MP("Problems found lead to specific improvements", ["improve", "problem", "fix", "change", "specific"])],
           "Usability testing puts the product in front of real users from the target audience and gives them tasks, such as finding this month's events, so their behaviour rather than their opinion is observed. Recording what each one does, how long it takes, where they hesitate and what they say produces measurable evidence, such as four of five users completing the task in under twelve seconds. That evidence is what the review uses to judge whether each requirement was met, and every difficulty observed points to a specific improvement, such as renaming a section to the word users were actually looking for.",
           command="Explain"),
        EQ("Describe what a review of an interactive product should contain.", 4,
           [MP("Each requirement of the brief, judged with evidence", ["requirement", "brief", "evidence", "met"]),
            MP("User and stakeholder feedback, quoted", ["feedback", "quote", "users", "testers"]),
            MP("Honest strengths and weaknesses", ["strength", "weakness", "honest"]),
            MP("Specific improvements and further development", ["improve", "further development", "how", "effect"])],
           "A review should take each requirement of the brief in turn, say whether it was met, and give the evidence from testing that shows it. It should include feedback from users and the client, quoted, including the criticism. It should state the product's strengths and weaknesses honestly, with reasons. And it should propose specific improvements, saying what would change, how and with what effect, as well as suggesting further development beyond the original brief.",
           command="Describe"),
    ],
)

R094_TOPICS = [M_R094_IDENTITY, M_R094_PLAN, M_R094_GRAPHICS, M_R094_TASK1, M_R094_TASK2]
R097_TOPICS = [M_R097_PLAN, M_R097_MAKE, M_R097_REVIEW, M_R097_TASK1, M_R097_TASK2,
               M_R097_TASK3]
