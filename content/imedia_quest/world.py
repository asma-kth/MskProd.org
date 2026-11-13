"""The Media Realms: the story, the places, the guides, the monsters and the pets.

Every monster is a muddle, a common mistake on its topic. Its taunt states the
mistake, so students hear it said, and the line it says when cleared states the
fix. Guardians, once cleared, join the player as pets under a new name that says
what they learned.

Elements: ink, light, sound and spark. Each monster is weak to one of them.
"""

TITLE = "The Media Realms"
TAGLINE = "An R093 adventure"

ELEMENTS = {
    "ink": {"name": "Ink", "spell": "Ink Lash", "colour": "#C026D3", "deep": "#701A75"},
    "light": {"name": "Light", "spell": "Flash Beam", "colour": "#F59E0B", "deep": "#92400E"},
    "sound": {"name": "Sound", "spell": "Echo Blast", "colour": "#0D9488", "deep": "#134E4A"},
    "spark": {"name": "Spark", "spell": "Spark Bolt", "colour": "#2563EB", "deep": "#1E3A8A"},
}

STORY = [
    "The Media Realms run on stories, pictures and sound. Every film, poster, podcast and app here began as a brief and a plan.",
    "Then the Great Static rolled in. It turned good ideas into muddles: sectors swapped with products, audiences of everyone, plans with no spare time.",
    "You are an apprentice media mage. With Pixel and a pet at your side, travel the four realms topic by topic, clear every muddle and reach the Studio Spire.",
]

REALMS = [
    {"id": "isles", "ta": "TA1", "name": "The Industry Isles",
     "about": "Sectors, products, purposes and the people who make media.",
     "colour": "#0EA5E9", "deep": "#075985", "ground": "#FDE68A"},
    {"id": "vale", "ta": "TA2", "name": "The Vale of Design",
     "about": "Clients, audiences, research and style: what shapes a product before it is made.",
     "colour": "#22C55E", "deep": "#14532D", "ground": "#86EFAC"},
    {"id": "peaks", "ta": "TA3", "name": "The Planning Peaks",
     "about": "Planning documents, work plans and the law.",
     "colour": "#8B5CF6", "deep": "#4C1D95", "ground": "#C4B5FD"},
    {"id": "coast", "ta": "TA4", "name": "The Signal Coast",
     "about": "File formats and the platforms that carry a product to its audience.",
     "colour": "#F97316", "deep": "#7C2D12", "ground": "#FDBA74"},
]


def _m(mid, name, el, muddle, taunts, cleared, art, tamed=""):
    return {"id": mid, "name": name, "el": el, "muddle": muddle, "taunts": taunts,
            "cleared": cleared, "art": art, "tamed": tamed}


def _art(shape, c, c2, eyes=2, mouth="grin", top="none", mark="", extra=""):
    return {"shape": shape, "c": c, "c2": c2, "eyes": eyes, "mouth": mouth, "top": top, "mark": mark, "extra": extra}


def _guide(name, role, robe, hat, skin, hair):
    return {"name": name, "role": role, "look": {"robe": robe, "hat": hat, "skin": skin, "hair": hair}}


PLACES = [
    {"lesson": "the-media-industry", "realm": "isles", "name": "Sector Harbour", "x": 14, "y": 22,
     "guide": _guide("Captain Marisol", "Harbour master of the sectors", "teal", "wide", 3, "black"),
     "intro": [
         "Welcome to Sector Harbour, apprentice. Every ship here belongs to a sector: television and film, publishing, music, games and more.",
         "A sector is a part of the industry. A product is the thing it makes. The Static has muddled the two, and now ships dock at the wrong piers.",
         "Clear the muddles, and remember: most products have more than one purpose.",
     ],
     "monsters": [
         _m("mixmite", "Mixmite", "ink", "Swaps sectors and products, so a trailer gets called a sector.",
            ["Mixmite shouts: A trailer is a sector!", "Mixmite swaps the pier signs around!"],
            "A sector is a part of the industry, such as television and film. A trailer is a product it makes.",
            _art("round", "#64748B", "#CBD5E1", 2, "zig", "antenna", "swap")),
         _m("feedling", "Feedling", "light", "Insists that social media is a sector.",
            ["Feedling posts: Social media is a sector!", "Feedling scrolls straight past your spell!"],
            "Social media is a distribution platform, not a sector of the industry.",
            _art("drop", "#6366F1", "#C7D2FE", 1, "o", "none", "feed")),
         _m("onetrick", "Onetrick", "spark", "Believes every product has exactly one purpose.",
            ["Onetrick roars: One product, one purpose!", "Onetrick stamps on your spellbook!"],
            "Most products have several purposes. A charity advert can entertain, inform and persuade at once.",
            _art("wide", "#B45309", "#FCD34D", 1, "fang", "horns", "one"), tamed="Manyfold"),
     ]},
    {"lesson": "job-roles-in-media", "realm": "isles", "name": "The Crew Guildhall", "x": 31, "y": 13,
     "guide": _guide("Guildmaster Idris", "Keeper of the crew rolls", "crimson", "pointed", 5, "grey"),
     "intro": [
         "This is the Crew Guildhall, where every media role hangs its banner.",
         "The producer looks after money, people and deadlines. The director makes the creative decisions. Mix them up and a production stalls.",
         "Freelancers work here too: self employed, paid per job, and bringing their own kit.",
     ],
     "monsters": [
         _m("roleblur", "Roleblur", "sound", "Thinks the director keeps the project on budget.",
            ["Roleblur blurs the producer and the director!", "Roleblur hands the budget to the director!"],
            "The producer runs the budget, schedule, hiring and delivery. The director makes the creative decisions.",
            _art("round", "#0F766E", "#99F6E4", 3, "o", "ears", "blur")),
         _m("stagehop", "Stagehop", "ink", "Puts roles in the wrong stage, like the video editor on the film set.",
            ["Stagehop drags the editor onto the film set!", "Stagehop jumbles the call sheet!"],
            "A video editor works in post production, assembling the footage after it has been shot.",
            _art("tall", "#9333EA", "#E9D5FF", 2, "grin", "spikes", "clap")),
         _m("paydaze", "Paydaze", "light", "Believes freelancers get holiday and sick pay.",
            ["Paydaze promises paid holidays to every freelancer!", "Paydaze waves a fake payslip!"],
            "Freelancers are self employed: paid per job, with no holiday or sick pay, and they sort out their own tax.",
            _art("blob", "#BE185D", "#FBCFE8", 2, "fang", "horns", "coin"), tamed="Gigwing"),
     ]},
    {"lesson": "client-requirements-and-the-brief", "realm": "vale", "name": "The Brief Tower", "x": 61, "y": 12,
     "guide": _guide("Envoy Odette", "Keeper of client briefs", "gold", "pointed", 2, "red"),
     "intro": [
         "Every job begins here, at the Brief Tower. A good brief sets out the purpose, audience, message, content, deliverables and constraints.",
         "Some requirements are written down. Others are simply expected, like spelling the client's name correctly.",
         "Agree the brief, record every sign off, and the Static has nowhere to creep in.",
     ],
     "monsters": [
         _m("typotoad", "Typo Toad", "ink", "Ignores implicit requirements, like spelling the client's name right.",
            ["Typo Toad misspells the client's name!", "Typo Toad croaks: If it is not written down, it does not count!"],
            "Implicit requirements are expected even when unwritten, such as correct spelling and a website that works on phones.",
            _art("wide", "#15803D", "#BBF7D0", 2, "grin", "none", "typo")),
         _m("handshake", "Handshake Hob", "sound", "Trusts an informal brief to settle a dispute.",
            ["Handshake Hob says a chat is as good as a contract!", "Handshake Hob forgets what was agreed!"],
            "An informal brief leaves no record of what was agreed. A written, contractual brief protects both sides.",
            _art("round", "#A16207", "#FEF08A", 2, "grin", "ears", "hand")),
         _m("scopecreep", "Scope Creep", "spark", "Keeps adding requirements after the brief has been agreed.",
            ["Scope Creep adds three more pages to the brief!", "Scope Creep sneaks in another deliverable!"],
            "A written brief and recorded sign off stop scope creep. Changes after sign off cost time and money.",
            _art("tall", "#166534", "#4ADE80", 3, "fang", "leaf", "vine"), tamed="Signoff"),
     ]},
    {"lesson": "target-audience-and-segmentation", "realm": "vale", "name": "Audience Meadow", "x": 78, "y": 20,
     "guide": _guide("Seer Tomas", "Reader of audiences", "forest", "hood", 4, "brown"),
     "intro": [
         "Welcome to Audience Meadow. Nobody designs for everyone, apprentice.",
         "Describe an audience three ways: demographics for who they are, psychographics for how they think, and behaviour for what they do.",
         "Then let the audience, not your own taste, decide every design choice.",
     ],
     "monsters": [
         _m("everyoneeel", "Everyone Eel", "light", "Aims every product at everyone.",
            ["Everyone Eel wriggles: My audience is everyone!", "Everyone Eel blurs your target!"],
            "An audience of everyone tells a designer nothing. Aim at a segment and every choice can be justified.",
            _art("drop", "#0369A1", "#BAE6FD", 2, "o", "none", "crowd")),
         _m("tastebud", "Tastebud", "ink", "Justifies design choices by personal taste.",
            ["Tastebud picks blue, because blue looks nice!", "Tastebud ignores the audience completely!"],
            "Tie every choice to the audience, such as large, clear type for readers over 65.",
            _art("blob", "#DB2777", "#FBCFE8", 2, "grin", "antenna", "heart")),
         _m("mirrormuddle", "Mirror Muddle", "sound", "Mixes up demographics and psychographics.",
            ["Mirror Muddle calls income a psychographic!", "Mirror Muddle swaps values with ages!"],
            "Demographics are measurable facts such as age and income. Psychographics are values, attitudes and lifestyle.",
            _art("round", "#475569", "#E2E8F0", 2, "zig", "spikes", "mirror"), tamed="Segmenta"),
     ]},
    {"lesson": "research-methods-and-sources", "realm": "vale", "name": "The Great Archive", "x": 87, "y": 43,
     "guide": _guide("Archivist Priya", "Keeper of sources", "midnight", "beret", 4, "black"),
     "intro": [
         "The Great Archive holds every source in the Realms. Primary research you collect yourself. Secondary research somebody else collected.",
         "Numbers tell you how many. Words tell you why. A good researcher needs both.",
         "Beware the biased: leading questions, cherry picked figures and samples that look nothing like the audience.",
     ],
     "monsters": [
         _m("leadinglynx", "Leading Lynx", "sound", "Asks questions that suggest their own answer.",
            ["Leading Lynx asks: You love this poster, don't you?", "Leading Lynx steers your survey!"],
            "A leading question pushes people towards an answer. Neutral wording gets honest results.",
            _art("tall", "#C2410C", "#FED7AA", 2, "grin", "ears", "ask")),
         _m("cherrypicker", "Cherrypicker", "spark", "Quotes only the one favourable figure.",
            ["Cherrypicker plucks out the one good number!", "Cherrypicker hides the rest of the report!"],
            "Cherry picking is quoting only the favourable figure from a mixed report. Report the full picture.",
            _art("round", "#B91C1C", "#FECACA", 2, "grin", "leaf", "cherry")),
         _m("yesbird", "Yesbird", "light", "Asks only friends and family, who always agree.",
            ["Yesbird chirps: My mum says it is brilliant!", "Yesbird surveys its own nest!"],
            "A sample must resemble the real audience. The right five people beat the wrong fifty.",
            _art("drop", "#CA8A04", "#FEF9C3", 2, "o", "spikes", "nod"), tamed="Fairsample"),
     ]},
    {"lesson": "style-content-and-layout", "realm": "vale", "name": "The Style Gallery", "x": 69, "y": 41,
     "guide": _guide("Curator Felix", "Keeper of style", "purple", "beret", 1, "blond"),
     "intro": [
         "The Style Gallery shows how colour, type and layout guide the eye.",
         "Two typefaces make a system. White space gives focus. Every code, from a low angle shot to a red rose, carries meaning.",
         "And remember: colours do not mean the same thing in every culture.",
     ],
     "monsters": [
         _m("fontfright", "Fontfright", "ink", "Uses five different typefaces on one poster.",
            ["Fontfright adds a fifth typeface!", "Fontfright scrawls script lettering all over the page!"],
            "One typeface for headings and one for body text looks designed. Five look assembled.",
            _art("wide", "#7C3AED", "#DDD6FE", 2, "zig", "antenna", "font")),
         _m("clutterclaw", "Clutterclaw", "spark", "Fills every gap and leaves no white space.",
            ["Clutterclaw fills every empty space!", "Clutterclaw crams in another logo!"],
            "White space is deliberate emptiness. It creates focus and helps a product feel premium.",
            _art("blob", "#334155", "#94A3B8", 3, "fang", "spikes", "clutter")),
         _m("rainbowriddler", "Rainbow Riddler", "light", "Thinks colours mean the same in every culture.",
            ["Rainbow Riddler says white means the same everywhere!", "Rainbow Riddler paints the whole world one meaning!"],
            "Colour meanings are cultural: white signifies mourning in parts of East Asia, and red is lucky in China.",
            _art("tall", "#E11D48", "#FDE68A", 2, "grin", "horns", "rainbow"), tamed="Worldhue"),
     ]},
    {"lesson": "pre-production-documents", "realm": "peaks", "name": "Storyboard Cliffs", "x": 76, "y": 63,
     "guide": _guide("Sketcher Juno", "Keeper of plans", "crimson", "hood", 3, "brown"),
     "intro": [
         "At Storyboard Cliffs, every product is planned before it is made.",
         "A static product gets a visualisation diagram. Moving image gets a storyboard. An interactive product gets wireframes and a navigation diagram.",
         "And annotate everything. A plan nobody else can follow is just a drawing.",
     ],
     "monsters": [
         _m("scribblesprite", "Scribble Sprite", "light", "Makes mood boards with no annotations.",
            ["Scribble Sprite pastes pictures with no notes!", "Scribble Sprite turns your mood board into a scrapbook!"],
            "Annotations say why each item is there. That turns a scrapbook into a planning document.",
            _art("drop", "#0891B2", "#A5F3FC", 1, "grin", "antenna", "scribble")),
         _m("tealtongue", "Tealtongue", "sound", "Writes vague colours like teal instead of exact values.",
            ["Tealtongue writes: make it sort of teal!", "Tealtongue says any bold font will do!"],
            "A visualisation diagram gives colours as exact values, such as #02848B, and fonts by name and size.",
            _art("round", "#0D9488", "#CCFBF1", 2, "o", "ears", "drop")),
         _m("mismatchmantis", "Mismatch Mantis", "ink", "Uses the wrong planning document, like a storyboard for a poster.",
            ["Mismatch Mantis storyboards a poster!", "Mismatch Mantis wireframes a TV advert!"],
            "A static product needs a visualisation diagram, moving image a storyboard, and an interactive product wireframes and a navigation diagram.",
            _art("tall", "#4D7C0F", "#D9F99D", 2, "fang", "antenna", "mismatch"), tamed="Rightplan"),
     ]},
    {"lesson": "work-planning-and-workflow", "realm": "peaks", "name": "Clockwork Camp", "x": 58, "y": 77,
     "guide": _guide("Quartermaster Bo", "Keeper of schedules", "gold", "wide", 6, "black"),
     "intro": [
         "Clockwork Camp runs on work plans: tasks, durations, dependencies, milestones and contingency.",
         "You cannot edit footage that has not been shot. That is a dependency.",
         "Build spare time into the plan before something goes wrong, not after.",
     ],
     "monsters": [
         _m("lastminute", "Lastminute Lizard", "spark", "Plans to finish exactly on the deadline, with no contingency.",
            ["Lastminute Lizard plans every task to the final minute!", "Lastminute Lizard says: We will just work faster!"],
            "Contingency is spare time and a plan B for named risks. A plan that ends exactly on the deadline has none.",
            _art("wide", "#65A30D", "#ECFCCB", 2, "grin", "spikes", "clock")),
         _m("finalfinal", "Finalfinal", "ink", "Saves over the same file and keeps calling it final.",
            ["Finalfinal saves over yesterday's work!", "Finalfinal names a file final, then final again!"],
            "Save numbered versions, keep the layered master and back up in a second place.",
            _art("round", "#57534E", "#D6D3D1", 2, "zig", "antenna", "file")),
         _m("deadlinedrake", "Deadline Drake", "light", "Skips pre production to get started sooner.",
            ["Deadline Drake roars: No planning, just start filming!", "Deadline Drake burns the work plan!"],
            "Skipping pre production costs more time later, because every missing decision has to be made late.",
            _art("tall", "#B91C1C", "#FCA5A5", 2, "fang", "horns", "flame"), tamed="Milestone"),
     ]},
    {"lesson": "legislation-and-permissions", "realm": "peaks", "name": "The Court of Rights", "x": 42, "y": 64,
     "guide": _guide("Judge Amara", "Keeper of the law", "midnight", "crown", 5, "grey"),
     "intro": [
         "This is the Court of Rights. Copyright protects original work automatically, from the moment it is made.",
         "Get a release for people and places, a licence for music, and check every asset's licence before you use it.",
         "Know who regulates what: the BBFC for film, PEGI for games, the ASA for adverts, Ofcom for broadcast and the ICO for data.",
     ],
     "monsters": [
         _m("copycat", "Copycat", "ink", "Uses any image found through a search engine.",
            ["Copycat grabs a photo straight from an image search!", "Copycat says: If it is online, it is free!"],
            "Copyright still applies to images found online. Use your own work or an asset licensed for your use.",
            _art("round", "#525252", "#E5E5E5", 2, "grin", "ears", "copy")),
         _m("freebie", "Freebie", "spark", "Thinks royalty free means free of charge.",
            ["Freebie shouts: Royalty free means free!", "Freebie skips the licence fee!"],
            "Royalty free means paying once with no repeat fee. It is not the same as free.",
            _art("blob", "#0E7490", "#CFFAFE", 2, "grin", "antenna", "tag")),
         _m("rulejumble", "Rulejumble", "sound", "Mixes up which body regulates what.",
            ["Rulejumble sends a video game to the BBFC for its rating!", "Rulejumble reports a misleading advert to PEGI!"],
            "The BBFC rates film, PEGI rates games, the ASA regulates adverts, Ofcom regulates broadcast and the ICO handles data protection.",
            _art("wide", "#6D28D9", "#DDD6FE", 3, "zig", "horns", "gavel"), tamed="Warden"),
     ]},
    {"lesson": "file-formats-and-properties", "realm": "coast", "name": "The Format Forge", "x": 24, "y": 70,
     "guide": _guide("Smith Rowan", "Forger of files", "forest", "wide", 2, "red"),
     "intro": [
         "The Format Forge shapes every file for the place it is going.",
         "Photographs suit JPG, logos suit SVG, and anything that needs transparency suits PNG.",
         "Screens use RGB. Printing presses use CMYK. Choose the job first, then the format.",
     ],
     "monsters": [
         _m("jaggy", "Jaggy", "light", "Enlarges small raster images until they blur.",
            ["Jaggy stretches a tiny photo across a billboard!", "Jaggy turns your smooth edges into steps!"],
            "A raster image is a grid of pixels, so it blurs or pixelates when enlarged. Vectors scale with no loss.",
            _art("blob", "#1D4ED8", "#BFDBFE", 2, "zig", "spikes", "pixel")),
         _m("resavewraith", "Resave Wraith", "ink", "Edits and saves the same JPG over and over.",
            ["Resave Wraith saves the JPG again, and again, and again!", "Resave Wraith smudges every save!"],
            "Lossy compression is generational: each save discards more. Edit the master and export a fresh copy.",
            _art("drop", "#64748B", "#E2E8F0", 2, "o", "none", "save")),
         _m("rgbghoul", "RGB Ghoul", "spark", "Sends RGB artwork to a printing press.",
            ["RGB Ghoul sends glowing RGB artwork to the printer!", "RGB Ghoul turns your bright greens dull!"],
            "Printing presses use CMYK. Convert at the start, so you see the real printed colours while you design.",
            _art("tall", "#0F172A", "#22C55E", 3, "fang", "horns", "rgb"), tamed="Cymka"),
     ]},
    {"lesson": "distribution-platforms", "realm": "coast", "name": "The Beacon Lighthouse", "x": 9, "y": 52,
     "guide": _guide("Keeper Nia", "Keeper of the signal", "teal", "hood", 6, "black"),
     "intro": [
         "From the Beacon Lighthouse, products travel to their audiences, on screens and on paper.",
         "Online is global and measurable, and it can be fixed after release. Print cannot be corrected once it is printed.",
         "Each platform wants its own crop, captions and format. Choose the platform where the audience already is.",
     ],
     "monsters": [
         _m("samecrop", "Samecrop", "ink", "Posts the same crop of a video on every platform.",
            ["Samecrop squashes a wide video into a tall feed!", "Samecrop posts one crop everywhere!"],
            "Each platform needs its own aspect ratio, so a campaign makes a different crop for each one.",
            _art("wide", "#9A3412", "#FED7AA", 2, "grin", "ears", "crop")),
         _m("bufferbog", "Buffer Bog", "sound", "Thinks streaming needs the whole file before it plays.",
            ["Buffer Bog waits for the whole film to download!", "Buffer Bog freezes your stream!"],
            "Streaming plays as the data arrives. Downloading has to finish first, but then works offline.",
            _art("blob", "#3F6212", "#D9F99D", 2, "o", "none", "spin")),
         _m("misprintwyrm", "Misprint Wyrm", "light", "Believes printed material can be fixed after it is printed.",
            ["Misprint Wyrm prints ten thousand posters with a typo!", "Misprint Wyrm skips the proof!"],
            "Print cannot be corrected once it is produced, so it needs proofing and sign off before the run.",
            _art("tall", "#7F1D1D", "#FCA5A5", 2, "fang", "horns", "print"), tamed="Proofwyrm"),
     ]},
]

FINAL = {
    "id": "spire", "name": "The Studio Spire", "x": 50, "y": 45,
    "intro": [
        "Every muddle you cleared came from one place: the Great Static, coiled around the Studio Spire.",
        "It throws questions from every topic in R093. Use everything you have learned.",
    ],
    "monster": _m("greatstatic", "The Great Static", "spark", "Every muddle in the Realms, rolled into one storm.",
                  ["The Great Static hisses every muddle at once!", "The Great Static scrambles the signal!",
                   "The Great Static howls: Audiences of everyone! Plans with no spare time!"],
                  "The Static clears. Every sector, brief, plan and platform in the Realms makes sense again.",
                  _art("blob", "#1E1B4B", "#A78BFA", 3, "fang", "spikes", "static")),
}

# Starter pets: one of each element. They grow at pet level 4 and pet level 8.
STARTERS = [
    {"id": "inkling", "el": "ink", "stages": ["Inkling", "Quillfox", "Scriptor"],
     "about": "A little fox made of ink, who writes notes in the air.",
     "art": _art("round", "#A21CAF", "#F5D0FE", 2, "grin", "ears", "nib")},
    {"id": "lumi", "el": "light", "stages": ["Lumi", "Lumora", "Lumenwing"],
     "about": "A glowing moth who lights up every scene.",
     "art": _art("drop", "#D97706", "#FEF3C7", 2, "grin", "antenna", "star")},
    {"id": "echo", "el": "sound", "stages": ["Echo", "Reverb", "Resona"],
     "about": "A bat who hears a story before anyone tells it.",
     "art": _art("round", "#0F766E", "#CCFBF1", 2, "grin", "ears", "note")},
    {"id": "nibble", "el": "spark", "stages": ["Nibble", "Sparkbyte", "Voltdrake"],
     "about": "A tiny dragon who crackles with signal.",
     "art": _art("tall", "#1D4ED8", "#DBEAFE", 2, "grin", "horns", "bolt")},
]

# The shop. Prices are in coins; "free" items are owned from the start.
SHOP = {
    "potion": [
        {"id": "draught", "name": "Healing draught", "about": "Restores 40 energy in battle.", "price": 30, "heal": 40},
        {"id": "elixir", "name": "Full elixir", "about": "Restores all your energy in battle.", "price": 80, "heal": 999},
        {"id": "biscuit", "name": "Pixel biscuit", "about": "A treat that gives your active pet 40 pet XP.", "price": 50, "petxp": 40},
    ],
    "hat": [
        {"id": "pointed", "name": "Pointed hat", "price": 0},
        {"id": "wide", "name": "Wide brim hat", "price": 0},
        {"id": "hood", "name": "Wizard hood", "price": 60},
        {"id": "beret", "name": "Director's beret", "price": 80},
        {"id": "phones", "name": "Studio headphones", "price": 120},
        {"id": "starry", "name": "Starry hat", "price": 160},
        {"id": "crown", "name": "Golden crown", "price": 300},
    ],
    "robe": [
        {"id": "purple", "name": "Purple robe", "price": 0, "c": "#7C3AED", "c2": "#4C1D95"},
        {"id": "teal", "name": "Teal robe", "price": 0, "c": "#0D9488", "c2": "#134E4A"},
        {"id": "crimson", "name": "Crimson robe", "price": 40, "c": "#DC2626", "c2": "#7F1D1D"},
        {"id": "forest", "name": "Forest robe", "price": 60, "c": "#16A34A", "c2": "#14532D"},
        {"id": "midnight", "name": "Midnight robe", "price": 80, "c": "#1E3A8A", "c2": "#0F172A"},
        {"id": "gold", "name": "Gold robe", "price": 140, "c": "#D97706", "c2": "#78350F"},
        {"id": "rainbow", "name": "Rainbow robe", "price": 320, "c": "#EC4899", "c2": "#6D28D9"},
    ],
    "wand": [
        {"id": "oak", "name": "Oak wand", "price": 0},
        {"id": "crystal", "name": "Crystal wand", "price": 90},
        {"id": "quill", "name": "Quill wand", "price": 120},
        {"id": "mic", "name": "Microphone wand", "price": 160},
        {"id": "star", "name": "Star wand", "price": 220},
    ],
}

SKINS = ["#FDE7D6", "#F5CBA7", "#E0A47A", "#B97A4F", "#8D5A3B", "#5C3A24"]
HAIRS = {"black": "#1F1A17", "brown": "#6B3F1F", "blond": "#E8C064", "red": "#B4441F", "grey": "#9CA3AF", "blue": "#3B82F6"}
