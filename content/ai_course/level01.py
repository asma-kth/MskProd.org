"""Level 1: The Story of AI. History and key dates, 1843 to today."""
from mskbuild.models import Topic, Section, Q, EQ, MP

NEA = "Check you could explain this"

L1_1 = Topic(
    slug="history-of-ai-thinking-machines",
    title="Thinking Machines: AI from 1843 to 2011",
    spec="1.1",
    icon="i-book",
    minutes=32,
    exam_title=NEA,
    blurb="Where the idea of a thinking machine came from, the 1956 workshop that named the field, the booms and the two AI winters, and the slow rise of learning machines up to IBM Watson in 2011.",
    fact="The 1955 proposal for the Dartmouth workshop asked for two months and ten researchers, and claimed that a significant advance could be made in one summer. It took about sixty years.",
    sections=[
        Section("Before computers: the dream of a thinking machine", """
People imagined thinking machines long before anyone could build one: the bronze giant Talos in Greek myth, clockwork automata that wrote letters and played music in the 1700s. The modern story starts when the idea met mathematics.

| Year | Who | What they contributed |
| **1843** | Ada Lovelace | In her notes on Charles Babbage's Analytical Engine, she suggested it might compose music if the rules of harmony could be expressed in its language, and also warned that it "has no pretensions whatever to originate anything" |
| **1936** | Alan Turing | Described a universal machine that can carry out any step-by-step procedure, the idea behind every computer since |
| **1943** | Warren McCulloch and Walter Pitts | The first mathematical model of a brain cell: a unit that fires when enough of its inputs are on. Every artificial neuron descends from it |
| **1949** | Donald Hebb | Proposed that connections between brain cells strengthen when the cells fire together, the first idea of how learning might happen in a network |

!key Two questions that never went away :: Lovelace asked whether a machine could ever create rather than follow instructions. McCulloch and Pitts asked whether a network of simple switches could think. Modern AI is still arguing about the first and building on the second.
"""),
        Section("1950 to 1956: a field gets its name", """
In **1950** Alan Turing published *Computing Machinery and Intelligence*. Instead of arguing about what "thinking" means, he proposed a test he called the **imitation game**: a judge holds a typed conversation with a hidden human and a hidden machine, and if the judge cannot reliably tell which is which, the machine has done something we would call intelligent. It became known as the **Turing test**. Turing predicted that by about the year 2000 machines would fool an average judge in five minutes about 30% of the time.

Programs that played games and proved theorems followed quickly. **Christopher Strachey** wrote a draughts program for the Ferranti Mark 1 in Manchester in 1951. In 1956 the **Logic Theorist**, by Allen Newell, Herbert Simon and Cliff Shaw, proved 38 of the first 52 theorems in Whitehead and Russell's *Principia Mathematica*.

### The Dartmouth workshop, 1956

In 1955 four researchers, **John McCarthy**, **Marvin Minsky**, **Nathaniel Rochester** and **Claude Shannon**, proposed a summer workshop at Dartmouth College. Their proposal used the phrase **artificial intelligence** for the first time and set out the field's founding bet:

!info The Dartmouth conjecture :: "Every aspect of learning or any other feature of intelligence can in principle be so precisely described that a machine can be made to simulate it."

The workshop ran in the summer of 1956. It did not solve intelligence, but it gave the field a name, a community and an agenda, which is why 1956 is usually given as the year AI was born.

!diagram ai-timeline-early
"""),
        Section("The golden years and the first AI winter", """
The next fifteen years were full of confidence.

- **1958**: Frank Rosenblatt demonstrated the **perceptron**, a machine that learned to recognise simple patterns from examples using 400 light sensors as its eye. A newspaper reported it as the embryo of a computer that would walk, talk and be conscious.
- **1959**: Arthur Samuel coined the term **machine learning** for his draughts program, which improved by playing against itself until it could beat him.
- **1964 to 1966**: Joseph Weizenbaum's **ELIZA** held conversations by matching patterns in what people typed and turning them into questions. Many users felt it understood them, even though it understood nothing. That reaction is still called the **ELIZA effect**.
- **1966 to 1972**: **Shakey**, at the Stanford Research Institute, became the first mobile robot that could reason about its own actions.

In 1965 Herbert Simon predicted that "machines will be capable, within twenty years, of doing any work a man can do". Progress was real, but it was nowhere near that fast.

### Why the winter came

- In **1969** Minsky and Papert's book *Perceptrons* proved that a single-layer perceptron cannot learn simple functions such as XOR. Interest in neural networks collapsed for over a decade.
- Programs that worked on toy problems failed on real ones: the number of possibilities exploded, and computers were far too slow and small.
- In **1973** the **Lighthill Report** told the UK government that AI had failed to deliver on its promises, and funding was cut. American funding was redirected too.

The years from about **1974 to 1980** are called the **first AI winter**: less money, fewer students, and a reputation for overpromising.

!diagram ai-seasons
"""),
        Section("Expert systems, a second winter, and learning machines", """
### The expert systems boom

In the 1980s AI found money again with **expert systems**: programs that stored a specialist's knowledge as hundreds or thousands of IF-THEN rules.

| System | What it did |
| **MYCIN** (Stanford, 1970s) | Diagnosed blood infections and recommended antibiotics using about 600 rules. It matched specialists in tests but was never used on patients |
| **XCON** (Digital Equipment Corporation, 1980) | Configured customers' computer orders, and was reported to save the company tens of millions of dollars a year |

Japan launched its **Fifth Generation** computer project in 1982, and other governments responded with programmes of their own.

But rules were expensive to write, brittle when the world changed, and impossible to keep consistent at large scale. When the market for specialised AI computers collapsed in **1987**, the **second AI winter** followed, lasting into the early 1990s.

### Meanwhile, learning was quietly coming back

- **1986**: David Rumelhart, Geoffrey Hinton and Ronald Williams showed how **backpropagation** can train networks with hidden layers, the answer to the problem *Perceptrons* had exposed.
- **1989**: Yann LeCun trained a **convolutional neural network** to read handwritten postcodes. Its descendants were reading a large share of cheques in American banks by the late 1990s.
- **1997**: IBM's **Deep Blue** beat world chess champion Garry Kasparov. It searched about 200 million positions a second with rules written by experts: impressive, but not learning.
- **1997**: Sepp Hochreiter and Jürgen Schmidhuber invented the **LSTM**, a network with memory for sequences.
- **1990s and 2000s**: statistical machine learning powered spam filters, search engines and recommendations without anyone calling it AI.
- **2006**: Hinton and colleagues showed how to train deep networks layer by layer, and the term **deep learning** caught on.
- **2009**: **ImageNet**, led by Fei-Fei Li, labelled over 14 million images, giving vision researchers the data deep learning would need.
- **2011**: IBM's **Watson** won the quiz show *Jeopardy!*, and Apple's **Siri** put a voice assistant in millions of pockets.
"""),
        Section("Hands-on: rules versus learning", """
### Build ELIZA in ten lines

ELIZA had no understanding at all: it matched patterns and reflected your words back as questions. This version follows the same idea. Run it, then add your own rules.

```python
import re

RULES = [
    (r"I need (.*)", "Why do you need {0}?"),
    (r"I am (.*)", "How long have you been {0}?"),
    (r"I feel (.*)", "What makes you feel {0}?"),
    (r"(.*) mother(.*)", "Tell me more about your family."),
    (r"(.*)\\?", "Why do you ask that?"),
]

REFLECT = {"i": "you", "me": "you", "my": "your", "am": "are",
           "you": "I", "your": "my"}

def reflect(words):
    # Turn "my exams" into "your exams", as ELIZA did
    return " ".join(REFLECT.get(w.lower(), w) for w in words.split())

def eliza(sentence):
    for pattern, reply in RULES:
        match = re.match(pattern, sentence, re.IGNORECASE)
        if match:
            return reply.format(*[reflect(g) for g in match.groups()])
    return "Please, go on."

for line in ["I need a holiday", "I am worried about my exams",
             "I feel tired", "My mother says I work too hard", "Is this real?",
             "The weather is nice"]:
    print("You:  ", line)
    print("ELIZA:", eliza(line))
```

Every reply was written by a person in advance. Nothing was learned, and nothing new could ever be said. That is **symbolic AI**: intelligence written down as rules. The rest of this course is about the other approach, where the rules are learned from data.

### Activity: the imitation game

Work in threes: a judge, a human and a "machine". The human answers the judge's written questions honestly. The machine may only answer using a list of ten stock phrases agreed in advance. The judge has five questions to decide which is which. Then discuss: what questions gave the machine away, and what would a machine need to pass?

### Activity: timeline challenge

Write each event from this lesson on a card, shuffle them, and put them in order without looking. Then sort them into three piles: **ideas**, **rules and symbols**, and **learning**. Which pile grows fastest after 1986?
"""),
        Section("Level check", """
Before moving on, make sure you can:

+ Explain what Turing's imitation game tests, and why he proposed it
+ Say why 1956 is called the birth of AI, and name two people involved
+ Describe what a perceptron was, and what Minsky and Papert proved about it
+ Explain what an AI winter is, and give two causes of the first one
+ Compare an expert system with a learning system
+ Name three milestones between 1986 and 2011 that made deep learning possible
"""),
    ],
    keyterms=[
        ("Artificial intelligence", "The field of making machines do things that would need intelligence if a person did them, a name first used in the 1955 Dartmouth proposal."),
        ("Turing test", "Turing's imitation game: a machine passes if a judge cannot reliably tell it from a human in typed conversation."),
        ("Perceptron", "Rosenblatt's 1958 learning machine: a single artificial neuron that adjusts its weights from examples."),
        ("Machine learning", "Programs that improve at a task from data or experience rather than from rules written by a person. Coined by Arthur Samuel in 1959."),
        ("Symbolic AI", "AI built from explicit rules and symbols written by people, such as ELIZA and expert systems."),
        ("Expert system", "A program storing a specialist's knowledge as many IF-THEN rules."),
        ("AI winter", "A period of reduced funding and interest after AI failed to meet its promises: roughly 1974 to 1980, and 1987 to the early 1990s."),
        ("ELIZA effect", "The tendency to believe a program understands us when it is only matching patterns."),
        ("Backpropagation", "The method for training networks with hidden layers by passing the error backwards, popularised in 1986."),
        ("ImageNet", "A dataset of over 14 million labelled images, released in 2009, that fuelled the deep learning breakthrough."),
    ],
    mistakes=[
        "Thinking AI began with ChatGPT. The field is older than the personal computer.",
        "Believing Deep Blue learned to play chess. It searched positions using rules written by experts.",
        "Saying the Turing test proves a machine thinks. It tests whether a machine can imitate a human in conversation.",
        "Assuming progress was steady. AI has gone through booms and two deep winters.",
        "Thinking neural networks are new. The perceptron is from 1958 and backpropagation from 1986.",
    ],
    grade="""
### Read the originals

Turing's 1950 paper *Computing Machinery and Intelligence* is short and readable. Its sixth section answers nine objections to thinking machines, including one he called "Lady Lovelace's Objection". The 1955 Dartmouth proposal is only a few pages long. Reading the founders' own words shows how much they got right, such as learning, language and abstraction, and how badly they underestimated the time it would take.

### Symbolic versus connectionist AI

The history of AI is a long argument between two camps. **Symbolic AI**, nicknamed "good old-fashioned AI", holds that intelligence is the manipulation of symbols by rules. **Connectionism** holds that it emerges from many simple units learning the strengths of their connections. Symbolic AI dominated until the late 1980s; connectionism, as deep learning, dominates now. Many researchers expect the future to combine both, with neural networks that can also search, use tools and reason explicitly, a direction called **neuro-symbolic AI**.
""",
    quiz=[
        Q("Who wrote in 1843 that the Analytical Engine 'has no pretensions whatever to originate anything'?",
          ["Ada Lovelace", "Alan Turing", "Charles Babbage", "Claude Shannon"], 0,
          "Lovelace's notes also suggested the machine might compose music. Turing replied to her objection in 1950."),
        Q("What did Turing's 1950 imitation game test?",
          ["Whether a judge could tell a machine from a human in typed conversation",
           "Whether a machine could beat a human at chess",
           "Whether a machine could learn from examples",
           "Whether a machine could see"], 0,
          "Turing replaced the vague question 'can machines think?' with a practical test."),
        Q("Why is 1956 called the birth of AI?",
          ["The Dartmouth workshop gave the field its name and its agenda",
           "The first electronic computer was switched on that year",
           "Rosenblatt's perceptron first learned to recognise shapes",
           "A computer beat the world chess champion for the first time"], 0,
          "The 1955 proposal for the 1956 workshop first used the phrase artificial intelligence."),
        Q("What did Minsky and Papert show in 1969?",
          ["A single-layer perceptron cannot learn functions such as XOR",
           "Computers can never think", "Backpropagation works",
           "Expert systems are better than people"], 0,
          "Their result helped push neural network research into the shadows for over a decade."),
        Q("What was ELIZA?",
          ["A 1960s program that held conversations by matching patterns",
           "The first neural network able to learn from examples",
           "A chess computer that searched millions of positions",
           "A factory robot arm that could sort objects by colour"], 0,
          "It understood nothing, yet many users felt understood: the ELIZA effect."),
        Q("What is an AI winter?",
          ["A period when funding and interest collapse after overpromising",
           "A period when governments banned all research into AI",
           "A slowdown caused by a worldwide shortage of computer chips",
           "A yearly contest where AI programs compete on hard problems"], 0,
          "The first ran roughly from 1974 to 1980, the second from 1987 into the early 1990s."),
        Q("How did an expert system such as MYCIN work?",
          ["It applied hundreds of IF-THEN rules written by experts",
           "It learned from millions of examples", "It searched every possibility",
           "It copied a human brain"], 0,
          "Rules were powerful but expensive to write and brittle when things changed."),
        Q("Why was 1986 important for neural networks?",
          ["Backpropagation was shown to train networks with hidden layers",
           "McCulloch and Pitts published the first model of a neuron",
           "A computer beat the world chess champion for the first time",
           "The phrase artificial intelligence was used for the first time"], 0,
          "Hidden layers solve problems like XOR that a single perceptron cannot."),
        Q("How did Deep Blue beat Garry Kasparov in 1997?",
          ["By searching about 200 million positions a second using expert rules",
           "By learning from millions of its own games", "By using a neural network",
           "By guessing"], 0,
          "It was a triumph of search and engineering rather than learning."),
        Q("Why did ImageNet (2009) matter?",
          ["It gave researchers over 14 million labelled images to learn from",
           "It was the first search engine that could find photos",
           "It introduced the first camera able to recognise faces",
           "It proved neural networks could never classify images"], 0,
          "Deep learning needs enormous amounts of labelled data, and ImageNet supplied it."),
    ],
    exam=[
        EQ("Explain why the period from about 1974 to 1980 is called an AI winter.", 3,
           [MP("Funding and interest in AI fell sharply", ["funding", "money", "cut", "interest fell", "less"]),
            MP("Because AI had failed to meet its promises", ["promise", "overpromis", "hype", "failed", "expectations"]),
            MP("A specific cause, such as the Lighthill Report, Perceptrons, or computing limits", ["Lighthill", "Perceptrons", "XOR", "slow", "toy problems", "computing power"])],
           "It is called an AI winter because funding and interest in the field fell sharply after the confident predictions of the 1950s and 1960s were not met. Programs that worked on small toy problems failed on real ones, because the number of possibilities exploded and computers were far too slow. In the UK the 1973 Lighthill Report told the government AI had not delivered, and funding was cut, while Minsky and Papert's 1969 book Perceptrons had already shown the limits of single-layer neural networks.",
           command="Explain"),
        EQ("Compare symbolic AI, such as an expert system, with machine learning.", 4,
           [MP("Symbolic AI uses rules written by people", ["rules", "written", "IF", "expert", "programmed"]),
            MP("Machine learning learns patterns or rules from data", ["learn", "data", "examples", "patterns"]),
            MP("Rules are brittle or expensive to write and maintain", ["brittle", "expensive", "maintain", "change", "thousands"]),
            MP("Learning needs lots of data, or is harder to explain", ["data", "explain", "black box", "examples", "labelled"])],
           "In symbolic AI, such as an expert system, people write the knowledge down as explicit IF-THEN rules, so its decisions are easy to trace. In machine learning, the program works the rules out for itself from examples, so nobody has to write them. Rules are expensive to write, break when the world changes and become inconsistent at large scale, which is why the expert systems boom ended in the second AI winter. Machine learning avoids that, but it needs large amounts of good data and its decisions can be much harder to explain.",
           command="Compare"),
        EQ("Describe **three** milestones between 1986 and 2011 that made later deep learning possible.", 6,
           [MP("Backpropagation in 1986", ["backprop", "1986", "hidden layers"]),
            MP("What it made possible", ["train", "hidden", "XOR", "deep", "multi-layer"]),
            MP("Convolutional networks reading handwriting, around 1989 or 1998", ["LeCun", "convolution", "handwrit", "cheques", "postcode"]),
            MP("What it showed", ["vision", "real use", "images", "practical"]),
            MP("ImageNet in 2009, or LSTM in 1997, or deep belief nets in 2006", ["ImageNet", "LSTM", "2006", "2009", "data"]),
            MP("Why it mattered", ["labelled", "data", "memory", "sequences", "deep"])],
           "In 1986 Rumelhart, Hinton and Williams showed that backpropagation could train neural networks with hidden layers, solving the problem Minsky and Papert had exposed and making multi-layer networks practical. In 1989 Yann LeCun trained a convolutional neural network to read handwritten postcodes, showing that networks could solve real vision problems; its descendants were reading cheques by the late 1990s. In 2009 ImageNet labelled over 14 million images, giving deep networks the huge quantity of data they need, which made the 2012 breakthrough possible.",
           command="Describe"),
    ],
)

L1_2 = Topic(
    slug="history-of-ai-deep-learning-era",
    title="The Deep Learning Era: 2012 to Today",
    spec="1.2",
    icon="i-sparkle",
    minutes=30,
    exam_title=NEA,
    blurb="How a 2012 image contest started the deep learning revolution, the games, science and language breakthroughs that followed, the arrival of generative AI, and the three ingredients that drove it all.",
    fact="AlexNet, the network that won the 2012 ImageNet contest, was trained on two gaming graphics cards in a bedroom at the home of one of its creators. Gaming hardware turned out to be exactly what deep learning needed.",
    sections=[
        Section("2012: the year everything changed", """
Every year from 2010 the **ImageNet** challenge asked programs to sort a million and more photographs into 1,000 categories. In **2012** a deep convolutional network called **AlexNet**, built by Alex Krizhevsky, Ilya Sutskever and Geoffrey Hinton, made a top-5 error of **15.3%**. The next best entry made **26.2%**.

The gap was so large that within two years almost every computer vision team had switched to deep learning. AlexNet had about 60 million learned numbers, called **parameters**, and was trained on two gaming graphics cards.

!diagram ai-three-ingredients

None of the three ingredients was new on its own. What was new was having all three at once:

| Ingredient | What changed |
| **Data** | The web, smartphones and projects like ImageNet produced labelled examples by the million |
| **Compute** | Graphics processing units (GPUs), built for games, could do thousands of multiplications at the same time |
| **Algorithms** | Better tricks: the ReLU activation, dropout, better ways to start training, and later attention |
"""),
        Section("Seeing, playing and understanding: 2013 to 2017", """
| Year | Breakthrough | Why it mattered |
| **2013** | **word2vec** | Turned words into lists of numbers where meaning becomes geometry: king minus man plus woman lands near queen |
| **2013** | **DeepMind's Atari player** | One network learned dozens of video games from the screen pixels and the score alone |
| **2014** | **GANs** | Two networks compete, one forging images and one spotting fakes, and both improve |
| **2014** | **Attention** | Let a translation network look back at the most relevant words of the input |
| **2015** | **ResNet** | Shortcut connections made networks 152 layers deep trainable, and beat the human error estimate on ImageNet |
| **2016** | **AlphaGo** | Beat Lee Sedol, one of the best Go players in the world, 4 games to 1 in Seoul |
| **2017** | **The Transformer** | The paper *Attention Is All You Need* introduced the architecture behind today's language models |
| **2017** | **AlphaZero** | Taught itself chess, shogi and Go from the rules alone, by playing itself |

!key Move 37 :: In the second game against Lee Sedol, AlphaGo played a move on the fifth line that commentators first thought was a mistake. It turned out to be brilliant, and a move a human professional would almost never consider. It was the moment many people realised these systems could find ideas, not only copy them.
"""),
        Section("The language and generation era: 2018 to today", """
!diagram ai-timeline-modern

### From models to products

- **2018**: Google's **BERT** and OpenAI's first **GPT** showed that a model pretrained on huge amounts of text could then be adapted to many tasks.
- **2020**: **GPT-3**, with 175 billion parameters, could carry out new tasks from a few examples written into its prompt.
- **2020**: DeepMind's **AlphaFold 2** predicted the 3D shapes of proteins with accuracy close to laboratory methods, solving a 50 year old problem in biology.
- **2022**: **Stable Diffusion** released an image generator that runs on a home computer, and in November **ChatGPT** put a language model in a simple chat window. It became one of the fastest growing apps ever.
- **2023**: **GPT-4** accepted images as well as text, and openly released models spread quickly. In November the UK hosted the first **AI Safety Summit** at Bletchley Park, where 28 countries and the EU signed a declaration on the risks of advanced AI.
- **2024**: The **EU AI Act**, the first broad law regulating AI by risk, entered into force. The **Nobel Prize in Physics** went to John Hopfield and Geoffrey Hinton for foundational work on neural networks, and half of the **Nobel Prize in Chemistry** to Demis Hassabis and John Jumper for AlphaFold. **Reasoning models**, which work through a problem step by step before answering, appeared.
- **2025 and beyond**: **AI agents** that plan, use tools and carry out tasks over many steps, and open reasoning models, became the new frontier.
"""),
        Section("Why it keeps accelerating", """
### Compute

The computation used to train the most notable AI models has grown by roughly **four to five times every year** since 2010, according to tracking by the research group Epoch AI. Growth that fast is hard to picture, so the chart below shows what it means.

!diagram ai-growth-curve

### Scale, and the bitter lesson

Researchers kept finding that **bigger models trained on more data with more compute** improved predictably. The computer scientist Rich Sutton called this the **bitter lesson**: over decades, general methods that make use of more computation have beaten approaches built on human cleverness. It is bitter because so much clever hand-designed work was overtaken.

### What has not changed

The core ideas in this course are old: neurons from 1943, learning from examples from 1958, backpropagation from 1986, convolution from 1989. What changed was scale, and a handful of new ideas, attention above all. Understand the ideas and you understand the machines, whatever they are called next year.
"""),
        Section("Hands-on: how fast is exponential?", """
### Run the numbers

If training compute grows four times a year, how long does it take to double, and how much bigger is it after a decade?

```python
import math

growth_per_year = 4        # four times more each year
for years in [1, 2, 5, 10]:
    factor = growth_per_year ** years
    print(f"After {years:2} years: {factor:>12,} times more compute")

doubling_years = math.log(2) / math.log(growth_per_year)
print(f"Doubling time: {doubling_years:.2f} years, about {doubling_years * 12:.0f} months")
```

A million times more in ten years. Compare that with the famous **Moore's law**, under which the number of transistors on a chip doubled roughly every two years: change the code to `growth_per_year = 2 ** 0.5` and see how much slower that is.

### Activity: is it AI?

Sort these into **not AI**, **rules (symbolic AI)** and **learned from data (machine learning)**, and give a reason for each: a pocket calculator, a central heating thermostat, an email spam filter, face unlock on a phone, a satnav finding the shortest route, a video app's recommendations, a chess app, a voice assistant.

### Research task

Choose one milestone from this lesson. Write a 150 word explainer for a Year 7 student: what happened, why it was hard, and what it changed. Use at least two sources and list them.
"""),
        Section("Level check", """
+ Explain why AlexNet in 2012 is called the start of the deep learning revolution
+ Name the three ingredients behind deep learning and give an example of each
+ Describe two breakthroughs from games and two from science
+ Explain what the Transformer is, and when it appeared
+ Describe how fast training compute has grown, and what the bitter lesson says
+ Give two events that show governments responding to AI
"""),
    ],
    keyterms=[
        ("Deep learning", "Machine learning with neural networks of many layers, which learn their own features from raw data."),
        ("AlexNet", "The deep convolutional network that won the 2012 ImageNet challenge by a huge margin."),
        ("GPU", "Graphics processing unit: a chip that performs thousands of calculations at once, ideal for training neural networks."),
        ("Parameter", "A number inside a model, such as a weight, that is learned during training."),
        ("Transformer", "The 2017 neural network architecture, built on attention, behind modern language models."),
        ("Generative AI", "AI that creates new content, such as text, images, audio or video."),
        ("Large language model", "A very large transformer trained to predict the next word on huge amounts of text."),
        ("Bitter lesson", "Rich Sutton's observation that general methods using more computation have beaten hand-crafted cleverness."),
        ("AI agent", "A system that plans and carries out multi-step tasks, often by using tools."),
    ],
    mistakes=[
        "Thinking the 2012 breakthrough came from a brand new idea. Convolutional networks existed in 1989; data and GPUs were what was new.",
        "Believing AI progress is only about bigger models. New ideas such as attention were essential too.",
        "Treating ChatGPT as the first language model. It was a chat interface on top of years of GPT research.",
        "Confusing compute with data. They are separate ingredients, and both grew.",
    ],
    grade="""
### Scaling, measured

In 2020 researchers at OpenAI (Kaplan and colleagues) showed that a language model's error falls along a smooth curve, a **power law**, as its parameters, data and compute grow. In 2022 DeepMind's Chinchilla paper (Hoffmann and colleagues) refined the recipe: for a fixed compute budget, train a smaller model on more data, roughly **20 tokens of text per parameter**. Level 11 uses these numbers to estimate what training a model costs.

### Benchmarks saturate

Every era has a test that seemed hard and then fell: ImageNet between 2012 and 2015, the GLUE and SuperGLUE language tests around 2019, then exam-style and coding tests. When a benchmark saturates, researchers build a harder one. Treat headline scores with care: benchmark questions can leak onto the web and end up in training data, so a model may have seen the answers.
""",
    quiz=[
        Q("What happened at the 2012 ImageNet challenge?",
          ["AlexNet, a deep network, won by a huge margin",
           "A human beat every computer", "The contest was cancelled",
           "ChatGPT was released"], 0,
          "AlexNet made a 15.3% top-5 error against 26.2% for the next best entry."),
        Q("Which three ingredients came together to start the deep learning era?",
          ["Data, compute and algorithms", "Robots, sensors and batteries",
           "Rules, logic and search", "Keyboards, mice and screens"], 0,
          "Labelled data, GPUs and better training tricks arrived together."),
        Q("Why are GPUs good for training neural networks?",
          ["They do thousands of multiplications at the same time",
           "They store more files", "They connect to the internet faster",
           "They need no electricity"], 0,
          "Neural networks are mostly enormous numbers of multiplications that can run in parallel."),
        Q("What did AlphaGo do in 2016?",
          ["Beat Lee Sedol at Go, 4 games to 1", "Won at chess against Kasparov",
           "Translated every language", "Predicted protein structures"], 0,
          "Deep Blue beat Kasparov at chess in 1997; AlphaGo conquered Go in 2016."),
        Q("Which 2017 paper introduced the Transformer?",
          ["Attention Is All You Need", "Computing Machinery and Intelligence",
           "Perceptrons", "Learning Representations by Back-propagating Errors"], 0,
          "It is the architecture behind modern language models."),
        Q("What did AlphaFold 2 achieve in 2020?",
          ["Predicted protein structures with near laboratory accuracy",
           "Beat the best human players at dozens of video games",
           "Generated realistic photographs from short text prompts",
           "Passed the Turing test in front of a panel of judges"], 0,
          "It led to half of the 2024 Nobel Prize in Chemistry."),
        Q("Roughly how fast has training compute for notable models grown since 2010?",
          ["About four to five times every year", "About 1% a year",
           "It has stayed the same", "It halves each year"], 0,
          "At four times a year, compute doubles about every six months."),
        Q("What does the 'bitter lesson' say?",
          ["General methods that use more computation win over time",
           "Hand-written rules always beat learning in the end",
           "Small, carefully designed models are always better",
           "AI progress always stalls once data runs out"], 0,
          "It is bitter because so much careful hand-designed work was overtaken by scale."),
        Q("Who won the 2024 Nobel Prize in Physics for work on neural networks?",
          ["John Hopfield and Geoffrey Hinton", "Alan Turing and Ada Lovelace",
           "Marvin Minsky and Seymour Papert", "Yann LeCun and Fei-Fei Li"], 0,
          "The prize recognised foundational discoveries that enabled machine learning with neural networks."),
        Q("What happened at Bletchley Park in November 2023?",
          ["The first AI Safety Summit, with a declaration on AI risks",
           "The EU AI Act was signed into law by member states",
           "ChatGPT was launched to the public for the first time",
           "A new national computing museum opened to visitors"], 0,
          "Bletchley Park was also where Turing broke codes in the Second World War."),
    ],
    exam=[
        EQ("Explain why AlexNet's win in 2012 is seen as the start of the deep learning revolution.", 4,
           [MP("AlexNet was a deep neural network that won ImageNet", ["AlexNet", "ImageNet", "deep", "won"]),
            MP("It won by a very large margin", ["15.3", "26.2", "large margin", "huge", "far better"]),
            MP("It combined large labelled data with GPUs", ["data", "GPU", "graphics", "compute"]),
            MP("Researchers switched to deep learning as a result", ["switched", "everyone", "within two years", "field changed", "adopted"])],
           "AlexNet was a deep convolutional neural network that entered the 2012 ImageNet challenge and won it by a huge margin, with a top-5 error of 15.3% against 26.2% for the next best method. It showed that a large network, trained on millions of labelled images using graphics cards, could beat years of hand-designed approaches. The result was so clear that within about two years almost every computer vision group had switched to deep learning, and the same approach then spread to speech, language and games.",
           command="Explain"),
        EQ("Describe the three ingredients that drove the deep learning era, with an example of each.", 6,
           [MP("Data", ["data", "labelled", "examples"]),
            MP("An example of data", ["ImageNet", "web", "smartphones", "text", "photos"]),
            MP("Compute", ["compute", "GPU", "processing", "hardware"]),
            MP("An example of compute", ["GPU", "graphics card", "TPU", "parallel", "thousands"]),
            MP("Algorithms", ["algorithm", "method", "technique", "architecture"]),
            MP("An example of an algorithm", ["ReLU", "dropout", "attention", "transformer", "ResNet", "backprop"])],
           "The first ingredient is data: deep networks learn from examples and need millions of them, which the web, smartphones and projects such as ImageNet, with over 14 million labelled images, supplied. The second is compute: graphics processing units, designed for video games, can perform thousands of multiplications at once, which is exactly what training a network needs, and AlexNet was trained on two of them. The third is algorithms: better methods such as the ReLU activation, dropout, residual connections and later attention and the Transformer made deep networks trainable and far more capable.",
           command="Describe"),
        EQ("Discuss whether the growth of AI since 2012 has been driven more by scale or by new ideas.", 6,
           [MP("Scale: compute grew around four to five times a year", ["four", "five", "compute", "grew", "scale"]),
            MP("Scale: bigger models with more data improved predictably, the bitter lesson", ["bigger", "bitter lesson", "more data", "predictabl"]),
            MP("Ideas: the Transformer or attention were essential", ["Transformer", "attention", "2017"]),
            MP("Ideas: other techniques such as ReLU, dropout or residual connections", ["ReLU", "dropout", "residual", "ResNet"]),
            MP("Old ideas only worked once scale arrived", ["1986", "1989", "old ideas", "existed", "backprop"]),
            MP("A judgement weighing both", ["both", "together", "neither alone", "overall", "combination"])],
           "Scale has clearly been a huge driver. Training compute for notable models has grown about four to five times a year since 2010, and researchers repeatedly found that bigger models trained on more data improved predictably, which Rich Sutton called the bitter lesson. Many of the core ideas, such as backpropagation from 1986 and convolutional networks from 1989, only became powerful once that scale arrived. But scale alone was not enough: new ideas were essential, above all attention and the Transformer in 2017, along with techniques such as ReLU, dropout and residual connections that made very deep networks trainable at all. Overall the two worked together: new ideas made it possible to use more compute well, and more compute revealed what those ideas could do.",
           command="Discuss"),
    ],
)

TOPICS = [L1_1, L1_2]
