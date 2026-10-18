"""Level 2: What AI Is. Definitions, the AI family, agents, and how machines learn."""
from mskbuild.models import Topic, Section, Q, EQ, MP

NEA = "Check you could explain this"

L2_1 = Topic(
    slug="what-is-ai",
    title="What AI Is, and What It Is Not",
    spec="2.1",
    icon="i-brain",
    minutes=28,
    exam_title=NEA,
    blurb="What people mean by artificial intelligence, how AI, machine learning, deep learning and generative AI fit inside each other, the difference between writing rules and learning them, and what today's AI is good and bad at.",
    fact="Hans Moravec noticed in 1988 that the things humans find hard, such as chess and algebra, are easy for computers, while the things a toddler does without thinking, such as walking across a cluttered room or picking up a sock, are fiendishly hard. It is called Moravec's paradox, and robots still feel it.",
    sections=[
        Section("Defining artificial intelligence", """
There is no single agreed definition, which is part of why arguments about AI get heated. Three useful ones:

| Source | Definition |
| **John McCarthy**, who coined the term | "The science and engineering of making intelligent machines, especially intelligent computer programs" |
| **A practical definition** | Computer systems that do tasks which would need intelligence if a person did them: seeing, understanding language, reasoning, learning and deciding |
| **The EU AI Act (2024)** | In summary, a machine-based system that works with some level of autonomy and **infers** from the input it receives how to produce outputs such as predictions, content, recommendations or decisions |

The key word in the legal definition is **infers**. A calculator follows a fixed formula. An AI system works out *how* to turn its input into an output, usually because it learned how from examples.

### Narrow, general and super

| Kind | Meaning | Exists? |
| **Narrow AI** | Very good at one task or a family of tasks: recognising faces, translating, playing Go | Yes, everywhere |
| **General AI (AGI)** | As capable as a person across almost any intellectual task, able to learn new ones | Not yet, and experts disagree on when or whether |
| **Superintelligence** | Far beyond the best humans at nearly everything | Hypothetical |

Today's large language models are a puzzle for this table. They are far more general than earlier narrow AI, writing code, poems and maths, yet still fail at some things a child can do. Most researchers describe them as broad but not yet general.

!key The working definition for this course :: AI is building systems that turn inputs into useful outputs by recognising patterns, mostly patterns they learned from data. That is less mysterious than the films, and far more useful.
"""),
        Section("The AI family: AI, machine learning, deep learning, generative AI", """
The four terms you hear most fit inside each other like nesting bowls.

!diagram ai-family

| Term | What it is | Example |
| **Artificial intelligence** | The whole field: any technique that makes a machine act intelligently, including hand-written rules and search | A chess program searching moves, a route planner |
| **Machine learning (ML)** | AI that learns its behaviour from data instead of being given rules | A spam filter that learns from emails people have marked |
| **Deep learning** | Machine learning with **neural networks** of many layers | Face unlock, speech recognition |
| **Generative AI** | Deep learning models that **create** new content: text, images, audio, video, code | A chatbot, an image generator |

### Fields named after tasks

AI is also divided by the **task**, and each task can be tackled with any method:

- **Computer vision**: understanding images and video
- **Natural language processing (NLP)**: understanding and producing human language
- **Speech**: turning sound into words and back
- **Robotics**: sensing and moving in the physical world
- **Planning and search**: finding a sequence of actions that reaches a goal
- **Recommendation**: predicting what a person will want next

Since about 2012, deep learning has become the best method for almost all of them, which is why the words are often used as if they meant the same thing. They do not.
"""),
        Section("Traditional programming versus machine learning", """
This is the most important idea in the whole course.

!diagram ai-rules-vs-learning

In **traditional programming**, a person writes the rules. The computer applies the rules to data and produces answers.

In **machine learning**, a person supplies data **and the answers**, and the computer works out the rules. The rules it learns are called a **model**. The model is then used to produce answers for new data it has never seen.

### Why learn the rules?

Try writing rules to recognise a cat in a photo. Pointy ears? Some cats have folded ears, and so do foxes. Whiskers? Hidden in half the photos. Fur colour? Every colour. Every rule has exceptions, and the exceptions have exceptions.

But it is easy to collect a hundred thousand photos labelled "cat" and "not cat". Machine learning turns that pile of examples into a model that recognises cats better than any rule list could.

!info When rules are still better :: If the rules are known, simple and must be exactly right, write them. VAT at 20%, a bank's opening hours or the rules of chess should never be learned. Machine learning is for problems where the rules are too many, too fuzzy or unknown.
"""),
        Section("Perceive, decide, act: AI as an agent", """
In the most widely used AI textbook, *Artificial Intelligence: A Modern Approach*, Stuart Russell and Peter Norvig define AI as the study of **agents**: things that perceive their environment and act on it to achieve goals.

!diagram ai-agent-loop

| Agent | Sensors (perceive) | Decides | Actuators (act) |
| Self-driving car | Cameras, radar, GPS | Where to steer, when to brake | Steering, brakes, accelerator |
| Robot vacuum | Bump sensors, cliff sensors, camera | Which way to go next | Wheels, brushes |
| Chess program | The board position | Which move scores best | Making the move |
| Video recommender | What you watched, skipped and liked | What to show next | The thumbnails on your screen |
| AI assistant | Your message, files, search results | What to say or which tool to use | Text, actions in other apps |

### From simple to clever

- A **simple reflex agent** reacts to what it senses now: a thermostat switches the heating on below 19 °C.
- A **model-based agent** keeps track of things it cannot currently see: a robot remembers where the stairs were.
- A **goal-based agent** plans actions to reach a goal: a satnav.
- A **utility-based agent** weighs how good each outcome is: a satnav that trades speed against tolls.
- A **learning agent** improves its own behaviour from experience. Most of this course is about how that learning works.
"""),
        Section("What today's AI is good and bad at", """
| Good at | Weak at |
| Finding patterns in huge amounts of data | Common sense that nobody wrote down |
| Recognising images, speech and handwriting | Situations unlike anything in its training data |
| Producing fluent text, images and code | Knowing when it is wrong: it can state falsehoods confidently, called **hallucination** |
| Doing the same task millions of times without tiring | Explaining *why* it made a decision |
| Games with clear rules and scores | Learning from one or two examples, as a child can |
| Predicting what usually happens next | Telling cause from coincidence |

!warn Fluent is not the same as right :: A language model is trained to produce text that is likely, not text that is true. Most of the time likely and true agree. When they do not, the model sounds just as sure of itself. Always check facts that matter.

### Moravec's paradox

Reasoning that humans find hard can be easy for computers, while perception and movement that humans find effortless can be very hard. A computer beat the world chess champion in 1997. A robot that can tidy any child's bedroom still does not exist.
"""),
        Section("Hands-on: a spam filter written two ways", """
### Rules versus learning, in code

Both filters below decide whether a message is spam. The first uses rules a person wrote. The second counts how often each word appeared in eight labelled examples and learns which words point to spam.

```python
def rule_filter(message):
    rules = ["win", "free", "prize", "click"]       # written by a person
    return any(word in message.lower().split() for word in rules)

training = [
    ("win a free prize now", "spam"),
    ("claim your free gift card today", "spam"),
    ("cheap pills click here", "spam"),
    ("you have won cash reply now", "spam"),
    ("are we still meeting for lunch", "ham"),
    ("here are the notes from class", "ham"),
    ("can you send me the homework", "ham"),
    ("happy birthday see you at the party", "ham"),
]

# Learning: count each word's appearances in spam and in normal mail (ham)
counts = {"spam": {}, "ham": {}}
for message, label in training:
    for word in message.split():
        counts[label][word] = counts[label].get(word, 0) + 1

def learned_filter(message):
    score = 0
    for word in message.lower().split():
        score += counts["spam"].get(word, 0) - counts["ham"].get(word, 0)
    return score > 0

tests = ["claim your cash now", "send me the class notes",
         "free pizza at lunch for the team", "you won a gift card"]
for t in tests:
    by_rules = "spam" if rule_filter(t) else "ham"
    by_learning = "spam" if learned_filter(t) else "ham"
    print(f"{t:34} rules: {by_rules:5} learned: {by_learning}")
```

The rules miss two spam messages because they contain none of the four magic words, and they flag a perfectly normal message about free pizza. The learned filter gets all four right because it weighs **every** word, using evidence from the examples.

### Try this

1. Add the test `"click here for the class notes"`. Which filter gets it right?
2. Look at `counts["ham"]["the"]`. The learned filter has decided "the" is a sign of normal mail, only because it appeared in three normal messages. What does that tell you about learning from only eight examples?
3. Add four more labelled messages of your own and run it again.

### Activity: spot the AI

List ten pieces of technology you used in the last 24 hours. For each, decide whether it uses **no AI**, **rules**, or **learning from data**, and what its sensors, decisions and actions are. Compare your list with a partner's and argue about the borderline cases.
"""),
        Section("Level check", """
+ Give two definitions of AI and explain what the word "infers" adds
+ Explain the difference between narrow AI and general AI, with examples
+ Draw the AI family as nested circles and give an example for each ring
+ Explain how machine learning differs from traditional programming
+ Describe an AI system as an agent: its sensors, decisions and actions
+ Give three things today's AI is good at and three it is weak at
"""),
    ],
    keyterms=[
        ("Artificial intelligence (AI)", "Computer systems that do tasks which would need intelligence if a person did them, usually by recognising patterns."),
        ("Narrow AI", "AI that performs one task or a family of related tasks very well. All AI that exists today is at most broad, not general."),
        ("Artificial general intelligence (AGI)", "A hypothetical AI as capable as a person across almost any intellectual task."),
        ("Machine learning", "AI that learns its behaviour from data instead of following rules a person wrote."),
        ("Deep learning", "Machine learning that uses neural networks with many layers."),
        ("Generative AI", "Models that create new content, such as text, images, audio, video or code."),
        ("Model", "The learned rules: a function with adjustable numbers that turns inputs into outputs."),
        ("Agent", "Something that perceives its environment through sensors and acts on it through actuators to achieve goals."),
        ("Hallucination", "A confident output from an AI model that is false or made up."),
        ("Moravec's paradox", "The observation that reasoning is easy for computers while perception and movement, effortless for people, are hard."),
    ],
    mistakes=[
        "Using AI, machine learning and deep learning as if they mean the same thing. Each is a smaller part of the one before.",
        "Thinking all AI learns. Route planners, chess searchers and expert systems are AI with no learning at all.",
        "Believing that a fluent answer must be a correct one. Language models are trained to be likely, not to be true.",
        "Assuming AI understands the way people do. It finds patterns in data, which can look like understanding and sometimes is not.",
        "Thinking machine learning should replace all rules. If the rules are known and must be exact, write them.",
    ],
    grade="""
### How engineers decide whether a problem needs ML

Before any model is built, a good engineer asks four questions:

1. **Is there a pattern to learn?** If the outcome is random, no model can predict it.
2. **Is it hard to write the rules?** If a short rule list would work, use it: it is cheaper, faster and easier to test.
3. **Is there data?** Usually thousands of examples, with labels if the task is supervised.
4. **Can mistakes be tolerated?** A model will be wrong some of the time. A film recommendation can afford that. A dose of medicine needs a human check.

Google's well-known *Rules of Machine Learning* guide opens with exactly this advice: do not be afraid to launch a product without machine learning.
""",
    quiz=[
        Q("What does the word 'infers' add to the EU AI Act's definition of an AI system?",
          ["It works out how to produce outputs instead of following a fixed formula",
           "It must be connected to the internet to count as AI",
           "It must be able to hold a spoken conversation with people",
           "It must be built and sold by a large technology company"], 0,
          "A calculator applies a formula. An AI system infers how to turn input into output, usually from what it learned."),
        Q("Which is an example of narrow AI?",
          ["A program that recognises faces in photos",
           "A machine as capable as a person at almost any task",
           "A robot that is better than humans at everything",
           "A human expert using a computer"], 0,
          "Narrow AI is very good at one task or family of tasks. Every working AI system today is narrow or, at most, broad."),
        Q("How do AI, machine learning and deep learning relate?",
          ["Deep learning is part of machine learning, which is part of AI",
           "They are three names for the same thing",
           "AI is part of deep learning, which is part of machine learning",
           "They are separate fields with nothing in common"], 0,
          "They nest: all deep learning is machine learning, and all machine learning is AI, but not the other way round."),
        Q("In machine learning, what goes in and what comes out of training?",
          ["Data and answers go in; rules, called a model, come out",
           "Rules and data go in; answers come out",
           "Only rules go in; data comes out",
           "Answers go in; data comes out"], 0,
          "Traditional programming turns rules and data into answers. Machine learning turns data and answers into rules."),
        Q("Which problem is best solved with hand-written rules rather than machine learning?",
          ["Calculating VAT at 20% on a bill",
           "Recognising handwriting", "Translating between languages",
           "Detecting faces in photos"], 0,
          "The rule is known, simple and must be exact, so writing it is cheaper and more reliable than learning it."),
        Q("In the agent view of AI, what are actuators?",
          ["The parts the agent uses to act on its environment",
           "The parts the agent uses to sense its environment",
           "The data used to train the agent", "The goals the agent is given"], 0,
          "Sensors perceive and actuators act: a car's cameras are sensors, its brakes and steering are actuators."),
        Q("A thermostat switches the heating on whenever the room is below 19 °C. What kind of agent is it?",
          ["A simple reflex agent", "A learning agent", "A utility-based agent",
           "A general AI"], 0,
          "It reacts only to what it senses right now, with one fixed rule and no memory, planning or learning."),
        Q("What is a hallucination in AI?",
          ["A confident output that is false or made up", "A picture generated by AI",
           "An error message from the computer", "A dream the model has while training"], 0,
          "Language models produce likely text. When likely and true disagree, they can state falsehoods fluently."),
        Q("What does Moravec's paradox say?",
          ["Reasoning is easy for computers while perception and movement are hard",
           "Computers will never beat humans at chess",
           "Every AI system eventually becomes general",
           "More data always makes a model worse"], 0,
          "Chess fell to computers in 1997, yet a robot that can tidy any bedroom still does not exist."),
        Q("Which task is generative AI?",
          ["Writing a new image from a text description",
           "Sorting emails into spam and not spam",
           "Predicting tomorrow's temperature",
           "Finding the shortest route"], 0,
          "Generative AI creates new content. Sorting emails and predicting temperatures are prediction tasks."),
    ],
    exam=[
        EQ("Explain the difference between traditional programming and machine learning.", 4,
           [MP("In traditional programming a person writes the rules", ["person writes", "programmer writes", "written rules", "rules are written", "explicit rules", "hand-written"]),
            MP("The computer applies the rules to data to give answers", ["rules and data", "apply", "answers", "output"]),
            MP("In machine learning the computer is given data and answers / examples", ["data and answers", "examples", "labelled", "labels"]),
            MP("It learns the rules, the model, itself", ["learns the rules", "model", "works out", "learns"])],
           "In traditional programming a person writes the rules, and the computer applies those rules to data to produce answers. In machine learning the person supplies data together with the correct answers, as labelled examples, and the computer works out the rules for itself. The learned rules are called a model, which is then used to produce answers for new data it has never seen.",
           command="Explain"),
        EQ("A school wants software that recognises which student is in a photo. Discuss whether it should use hand-written rules or machine learning.", 6,
           [MP("Rules for faces are very hard to write", ["hard to write", "too many rules", "exceptions", "fuzzy", "cannot describe"]),
            MP("Faces vary: lighting, angle, expression, glasses, hair", ["lighting", "angle", "expression", "glasses", "vary", "different"]),
            MP("Machine learning can learn patterns from labelled photos", ["learn", "labelled", "examples", "photos", "data"]),
            MP("It needs enough photos of each student", ["enough", "many photos", "data needed", "lots of"]),
            MP("It will sometimes be wrong, so mistakes need handling", ["wrong", "mistakes", "errors", "accuracy", "check"]),
            MP("Privacy or consent concerns about storing faces", ["privacy", "consent", "biometric", "GDPR", "permission"])],
           "Hand-written rules would be almost impossible here, because nobody can describe a particular face precisely enough, and the same face changes with lighting, angle, expression, glasses and hair. Every rule would have exceptions. Machine learning suits the problem, because it can learn the patterns that distinguish each student from labelled photos. However, it needs several photos of every student, it will sometimes misidentify someone, so there must be a way to handle mistakes, and storing biometric data about children raises serious privacy and consent issues under data protection law. Machine learning is the right technique, but only with consent, security and a human fallback.",
           command="Discuss"),
        EQ("Describe a self-driving car as an AI agent.", 3,
           [MP("Sensors such as cameras, radar or GPS perceive the environment", ["camera", "radar", "lidar", "GPS", "sensor"]),
            MP("It decides what to do, such as when to brake or where to steer", ["decide", "brake", "steer", "plan", "choose"]),
            MP("Actuators such as steering, brakes or accelerator act", ["actuator", "steering", "brakes", "accelerator", "wheels", "motor"])],
           "A self-driving car perceives its environment through sensors such as cameras, radar and GPS. Its software decides what to do next, such as when to brake, how fast to go and where to steer, to reach its goal safely. It then acts on the world through actuators: the steering, brakes and accelerator.",
           command="Describe"),
    ],
)

L2_2 = Topic(
    slug="how-machines-learn",
    title="How Machines Learn: Supervised, Unsupervised and Reinforcement",
    spec="2.2",
    icon="i-bulb",
    minutes=30,
    exam_title=NEA,
    blurb="What it means for a program to learn, the three main kinds of machine learning, the self-supervised trick behind modern AI, and your first learning program.",
    fact="The labels for modern language models cost nothing: the label for every word is simply the word that comes next in the text. That is why they can learn from trillions of words that nobody ever labelled.",
    sections=[
        Section("What it means for a machine to learn", """
In 1997 the computer scientist Tom Mitchell gave the definition still used in textbooks:

!info Mitchell's definition :: A program learns from experience **E** with respect to a task **T** and a performance measure **P** if its performance at T, as measured by P, improves with experience E.

| | Spam filter | Chess program | Weather model |
| **Task T** | Sort emails into spam and not spam | Win games | Predict tomorrow's rainfall |
| **Performance P** | Percentage sorted correctly | Percentage of games won | Average error in millimetres |
| **Experience E** | Emails people have labelled | Games played | Years of weather records |

### Model, parameters, training and inference

A **model** is a function with adjustable numbers inside it, called **parameters** or **weights**. **Training** means adjusting those numbers until the model's outputs match the examples well. **Inference** means using the trained model on new inputs.

!diagram ai-train-infer

Training is slow and expensive and happens once, or now and then. Inference is quick and cheap and happens every time someone uses the model. A large language model may take months to train and then answer millions of questions a day.
"""),
        Section("Supervised learning: learning from labelled examples", """
In **supervised learning**, every training example has an input and the correct output, called the **label**. The model learns to map inputs to labels.

!diagram ai-learning-types

The inputs are described by **features**: the measurable properties the model can use.

| Problem | Features (input) | Label (output) | Type |
| Is this email spam? | The words in it, the sender | spam or not spam | **Classification** |
| Which digit is this? | 784 pixel brightnesses | 0 to 9 | **Classification** |
| What will this house sell for? | Size, bedrooms, location | A price in pounds | **Regression** |
| How long will this delivery take? | Distance, time of day, weather | Minutes | **Regression** |

- **Classification** predicts a category.
- **Regression** predicts a number.

Supervised learning is the workhorse of industry, but labels are expensive: someone has to mark every example. ImageNet's 14 million labels took tens of thousands of crowd workers years to produce.
"""),
        Section("Unsupervised learning: finding structure without answers", """
In **unsupervised learning** there are no labels. The algorithm looks for structure in the inputs alone.

| Technique | What it finds | Example |
| **Clustering** | Groups of similar examples | Customer segments for a shop: bargain hunters, weekend browsers, loyal regulars |
| **Dimensionality reduction** | A few numbers that capture most of many | Squashing 1,000 survey answers down to 3 personality scores to plot them |
| **Anomaly detection** | Examples unlike the rest | A card payment that does not fit your usual pattern |
| **Association** | Things that happen together | People who buy pasta often buy parmesan |

The catch: nobody tells the algorithm what a good answer is, so a person has to decide whether the structure it found is meaningful. Clustering will always find clusters, even in random noise.
"""),
        Section("Reinforcement learning: learning from rewards", """
In **reinforcement learning (RL)** an **agent** takes **actions** in an **environment** and receives **rewards**. Nobody tells it the right action. It learns by trial and error which actions lead to the most reward over time.

| Example | Actions | Reward |
| Learning to play an arcade game | Joystick moves | The game score |
| A robot learning to walk | Motor movements | Distance travelled without falling |
| AlphaGo | Placing stones | +1 for a win, -1 for a loss, only at the end |
| Tuning a chatbot's style | Choosing how to reply | A score from a model of what people preferred |

Two things make RL hard. The reward is often **delayed**: a Go game lasts about 200 moves and the reward comes only at the end, so which moves deserved the credit? And the agent must balance **exploring** new actions against **exploiting** the ones it already knows work. Level 13 builds a reinforcement learner from scratch.
"""),
        Section("Self-supervised learning: the trick behind modern AI", """
Labels are expensive. Rewards are slow. So how did language models learn from trillions of words?

**Self-supervised learning** creates labels from the data itself. Hide part of the input and train the model to predict the hidden part. The hidden part *is* the label, and it costs nothing.

!diagram ai-self-supervised

- **Next-word prediction**: "The cat sat on the ..." The label is the word that really came next. This is how GPT-style models are trained.
- **Masked words**: "The cat [MASK] on the mat." Predict the missing word. This is how BERT was trained.
- **Images**: hide patches of a photo and predict them, or predict whether two crops come from the same photo.

To predict the next word well across all of the internet, a model has to pick up grammar, facts, styles of writing and some reasoning. Prediction turns out to be a remarkably powerful teacher.

### Two more terms you will meet

- **Transfer learning**: start from a model trained on a huge general task, then train it a little more on your small specific task. Almost all practical AI works this way now.
- **Semi-supervised learning**: a few labelled examples plus many unlabelled ones.
"""),
        Section("Hands-on: your first learning program", """
### Learning a threshold

Twelve students recorded their hours of revision and whether they passed. The program tries every possible threshold and **learns** the one that best separates pass from fail. That search is training, in miniature.

```python
# (hours of revision, passed: 1 = yes, 0 = no)
data = [(1, 0), (2, 0), (2.5, 0), (3, 0), (3.5, 0), (3, 1),
        (4, 1), (4.5, 1), (5, 1), (6, 1), (7, 1), (8, 1)]

def accuracy(threshold):
    correct = 0
    for hours, passed in data:
        prediction = 1 if hours >= threshold else 0
        correct += prediction == passed
    return correct / len(data)

candidates = [t / 2 for t in range(0, 21)]      # 0, 0.5, 1, ... 10
for t in candidates[2:11]:
    print(f"threshold {t:>4}: accuracy {accuracy(t):.0%}")

best = max(candidates, key=accuracy)
print("Learned rule: predict a pass if hours >=", best)
print("Prediction for 3.8 hours:", "pass" if 3.8 >= best else "fail")
```

The learned threshold is one parameter. A large language model has billions of them, but the principle is the same: search for the parameter values that make the fewest mistakes on the examples.

### Learning by nearest neighbour

Another way to learn is simply to remember the examples and, for a new input, copy the label of the most similar one.

```python
import math

# (weight in grams, skin smoothness 1 to 10), label
fruit = [((150, 9), "apple"), ((170, 8), "apple"), ((140, 9), "apple"),
         ((130, 3), "orange"), ((160, 2), "orange"), ((145, 4), "orange")]

def nearest(item):
    best = min(fruit, key=lambda f: math.dist(f[0], item))
    return best[1]

for mystery in [(155, 8), (150, 3), (138, 7)]:
    print(mystery, "is probably an", nearest(mystery))
```

This is the **nearest neighbour** classifier. Level 4 improves it by letting several neighbours vote, and shows why the features need to be on similar scales.

### Activity: which kind of learning?

Decide whether each is supervised, unsupervised, reinforcement or self-supervised learning, and say what the labels or rewards are: predicting exam grades from past records; grouping songs by sound; a drone learning to hover; predicting the next frame of a video; sorting X-rays labelled by doctors; finding unusual network traffic; training a model to fill in missing words.
"""),
        Section("Level check", """
+ State Mitchell's definition of learning and apply it to a new example
+ Explain the difference between a model, its parameters, training and inference
+ Describe supervised learning and the difference between classification and regression
+ Describe unsupervised learning, with two techniques and examples
+ Describe reinforcement learning and explain why delayed rewards make it hard
+ Explain how self-supervised learning creates its own labels
"""),
    ],
    keyterms=[
        ("Training", "Adjusting a model's parameters until its outputs match the training examples well."),
        ("Inference", "Using a trained model to produce outputs for new inputs."),
        ("Parameter (weight)", "One of the adjustable numbers inside a model that training sets."),
        ("Feature", "A measurable property of an example that the model uses as input."),
        ("Label", "The correct output for a training example in supervised learning."),
        ("Supervised learning", "Learning from examples that include the correct answers."),
        ("Classification", "Predicting which category an input belongs to."),
        ("Regression", "Predicting a number."),
        ("Unsupervised learning", "Finding structure, such as clusters, in data that has no labels."),
        ("Reinforcement learning", "An agent learning which actions earn the most reward by trial and error."),
        ("Self-supervised learning", "Learning by hiding part of the data and predicting it, so the data provides its own labels."),
        ("Transfer learning", "Starting from a model trained on a large general task and adapting it to a specific one."),
    ],
    mistakes=[
        "Confusing classification and regression. If the answer is a category it is classification, even when the categories are numbered.",
        "Thinking unsupervised learning finds the 'right' groups. It finds groups, and a person must judge whether they mean anything.",
        "Mixing up training and inference. Training sets the parameters; inference uses them and changes nothing.",
        "Thinking reinforcement learning is told the right answer. It only receives rewards, often long after the action that earned them.",
        "Believing language models were trained on labelled data. Their labels come free from the text itself.",
    ],
    grade="""
### Inductive bias: why every learner makes assumptions

No learner can generalise without assumptions. The threshold learner assumes one cut-off separates the classes. Nearest neighbour assumes similar inputs have similar labels. A convolutional network assumes nearby pixels matter together. These built-in assumptions are called **inductive bias**, and choosing a model is choosing its assumptions.

The **no free lunch theorem** (Wolpert, 1996) makes this precise: averaged over every possible problem, no learning algorithm beats any other. A method wins only because its assumptions fit the problems we actually have. That is why engineers try several models, and why understanding the assumptions matters more than memorising algorithm names.
""",
    quiz=[
        Q("In Mitchell's definition, what is P for a spam filter?",
          ["The percentage of emails it sorts correctly",
           "The emails people have labelled",
           "Sorting emails into spam and not spam",
           "The number of emails received"], 0,
          "T is the task, E the experience (labelled emails) and P the performance measure (percentage correct)."),
        Q("What is inference?",
          ["Using a trained model to produce outputs for new inputs",
           "Adjusting the parameters to fit the examples",
           "Collecting and labelling the training data",
           "Deleting a model after use"], 0,
          "Training sets the parameters. Inference uses them, quickly, every time the model is asked something."),
        Q("Predicting the price of a house from its size and location is an example of:",
          ["regression", "classification", "clustering", "reinforcement learning"], 0,
          "The output is a number, a price, so it is regression."),
        Q("Which is unsupervised learning?",
          ["Grouping customers into segments by their shopping habits",
           "Predicting a house price from labelled sales",
           "Teaching a robot to walk with rewards",
           "Sorting X-rays that doctors have labelled"], 0,
          "No labels are given: the algorithm finds the groups itself."),
        Q("Why are delayed rewards a problem in reinforcement learning?",
          ["It is hard to tell which earlier actions deserve the credit",
           "The agent cannot take actions until the reward arrives",
           "Delayed rewards are always negative",
           "The environment stops while it waits"], 0,
          "In Go the reward comes after about 200 moves. Which of them won the game? This is the credit assignment problem."),
        Q("How does self-supervised learning get its labels?",
          ["By hiding part of the data and using the hidden part as the label",
           "By paying people to label every example",
           "By rewarding the model for good answers",
           "By copying labels from another model"], 0,
          "The next word in real text is a free label, which is why language models can learn from trillions of words."),
        Q("In machine learning, what is a feature?",
          ["A measurable property of an example used as input",
           "The correct answer for an example",
           "A bug in the model", "The model's final prediction"], 0,
          "Weight and smoothness are the features in the fruit example; apple or orange is the label."),
        Q("What is transfer learning?",
          ["Adapting a model trained on a large general task to a specific task",
           "Copying training data from one computer to another",
           "Moving a model from training to inference",
           "Training two models at the same time"], 0,
          "It saves enormous amounts of data and compute, which is why nearly all practical AI now starts from a pretrained model."),
        Q("A model learns to predict whether a photo shows a cat or a dog from 50,000 labelled photos. Which kind of learning is this?",
          ["Supervised classification", "Supervised regression",
           "Unsupervised clustering", "Reinforcement learning"], 0,
          "Labelled examples make it supervised, and a category as the output makes it classification."),
        Q("What does a nearest neighbour classifier do with a new input?",
          ["Gives it the label of the most similar training example",
           "Averages all the labels in the training data",
           "Asks a person for the label",
           "Picks a label at random"], 0,
          "It remembers the examples and copies the label of the closest one, measured by distance between feature values."),
    ],
    exam=[
        EQ("Apply Mitchell's definition of learning to a program that learns to recommend films.", 3,
           [MP("Task: recommending films a person will like", ["recommend", "suggest", "films a person"]),
            MP("Performance: e.g. percentage of recommendations watched or rated highly", ["percentage", "watched", "rated", "clicked", "accuracy", "how often"]),
            MP("Experience: records of what people watched or rated", ["history", "watched", "ratings", "records", "past", "data"])],
           "The task T is recommending films that a person will enjoy. The performance measure P could be the percentage of recommended films that people go on to watch, or rate highly. The experience E is the record of what people have watched, finished, skipped and rated. The program learns if its recommendations are watched more often as that record grows.",
           command="Apply"),
        EQ("Compare supervised and unsupervised learning.", 4,
           [MP("Supervised learning uses labelled examples / correct answers", ["labelled", "labels", "correct answers", "answers"]),
            MP("Unsupervised learning has no labels", ["no labels", "unlabelled", "without labels", "no answers"]),
            MP("Supervised predicts a known output, such as a class or number", ["predict", "classification", "regression", "output"]),
            MP("Unsupervised finds structure such as clusters or anomalies", ["clusters", "groups", "structure", "patterns", "anomal"])],
           "Supervised learning trains on examples that include the correct answer, the label, so the model learns to predict a known kind of output, either a category in classification or a number in regression. Unsupervised learning has no labels, so instead of predicting answers it looks for structure in the inputs, such as clusters of similar examples or unusual anomalies. Supervised learning needs costly labelling, while unsupervised results need a person to judge whether the structure found is meaningful.",
           command="Compare"),
        EQ("Explain why self-supervised learning made large language models possible.", 4,
           [MP("Labelling trillions of words by hand would be impossible / too costly", ["impossible", "cost", "expensive", "too much", "by hand"]),
            MP("Self-supervised learning hides part of the text and predicts it", ["hide", "predict", "next word", "masked", "missing"]),
            MP("So the labels come free from the text itself", ["free", "text itself", "data itself", "no labelling", "automatically"]),
            MP("Predicting text well requires learning grammar, facts or patterns", ["grammar", "facts", "patterns", "knowledge", "reasoning"])],
           "Large language models learn from trillions of words, and paying people to label that much text would be impossible. Self-supervised learning avoids labelling altogether: the model is shown text with the next word hidden and learns to predict it, so every word in the text is a free label. To predict the next word well across so much varied text, the model has to pick up grammar, facts and patterns of reasoning, which is what makes it useful.",
           command="Explain"),
    ],
)

TOPICS = [L2_1, L2_2]
