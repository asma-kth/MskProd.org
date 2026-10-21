"""Level 15: Responsible AI, and the capstone project."""
from mskbuild.models import Topic, Section, Q, EQ, MP

NEA = "Check you could explain this"

L15_1 = Topic(
    slug="responsible-ai",
    title="Responsible AI: Fairness, Safety, Privacy and the Law",
    spec="15.1",
    icon="i-scales",
    minutes=46,
    exam_title=NEA,
    blurb="What can go wrong and how engineers prevent it: real cases of harm, measuring fairness and why its definitions conflict, explaining decisions, privacy with differential privacy and federated learning, adversarial examples, AI safety and alignment, the EU AI Act and data protection law, and AI's wider effects on society.",
    fact="In 2024 the Nobel Prize in Chemistry was shared by Demis Hassabis and John Jumper of Google DeepMind for AlphaFold, which predicts the shapes of proteins, alongside David Baker for designing new proteins. AI's power to help is as real as its power to harm.",
    sections=[
        Section("Why responsibility is part of engineering", """
AI systems now help decide who gets a loan, a job interview, a medical test or a university place. When they go wrong, real people are harmed, often people with the least power to complain.

| Year | Case | What happened |
| 2016 | Criminal risk scores (COMPAS) | A news investigation found that Black defendants who did not reoffend were almost twice as likely as white defendants to have been labelled high risk |
| 2018 | A recruiting tool | A large company dropped an experimental CV-screening model that had learned to mark down CVs containing the word "women's" |
| 2018 | Face analysis (Gender Shades) | Commercial systems misjudged the gender of darker-skinned women up to 34.7% of the time, and of lighter-skinned men 0.8% of the time |
| 2020 | A-level grades in England | An algorithm replaced cancelled exams and lowered about 39% of teachers' predicted grades; after protests, it was withdrawn |

None of these systems was built to discriminate. Each learned from data that reflected an unequal world, or was judged by a measure that hid who it failed. Responsible AI is not a separate subject added at the end: it is part of doing the engineering properly.
"""),
        Section("Measuring fairness", """
"Fair" has several precise meanings, each comparing a different number between groups:

| Definition | Equal across groups | The idea |
| **Demographic parity** | The share of people approved | Opportunities spread equally |
| **Equal opportunity** | The true positive rate: of those who deserve approval, the share approved | Equally good people get equal chances |
| **Equalised odds** | Both the true and false positive rates | Errors fall equally on everyone |
| **Predictive parity** | The precision: of those approved, the share who succeed | An approval means the same for everyone |

!diagram ai-fairness-metrics

In the example in the figure, both groups have the same precision, 75%, so by one definition the model is fair. But group B's applicants who would repay are approved only 60% of the time, against 90% for group A.

!key Fairness definitions conflict :: In 2016 and 2017, researchers proved that when two groups have different base rates, such as different shares of people who would repay, no model short of a perfect one can satisfy predictive parity and equalised odds at the same time. Choosing which kind of fairness matters is a value judgement about the situation, to be made openly, with the people affected, and not left to an optimiser.

!tool fairness-lab
"""),
        Section("Where bias comes from, and what to do", """
Bias can enter at every stage (Level 3): **historical** bias in the world the data records, **representation** bias when some groups are scarce in the data, **measurement** bias when a label is a poor stand-in (arrests are not the same as crimes), and **deployment** bias when a model is used on people unlike those it learned from.

Engineers have three places to intervene:

- **Before training**: collect better data, rebalance or reweight groups, remove proxies.
- **During training**: add a fairness constraint or penalty to the loss.
- **After training**: adjust decision thresholds per group, as the lab above lets you do.

Each has costs, often a little overall accuracy, and some, such as treating groups differently, are restricted by law in some settings. Just as important are the non-technical steps: involving the people affected, auditing results by group before and after release, and being willing to decide that a system should not be built at all.
"""),
        Section("Explaining decisions", """
People affected by a decision often have a right to an explanation, and engineers need explanations to find bugs.

- **Interpretable models**, such as small decision trees or linear models, can be read directly.
- **Feature importance** asks how much each input matters overall, for example by shuffling one feature and seeing how much worse the model gets.
- **Local explanations** such as **LIME** (2016) and **SHAP** (2017) estimate how much each feature pushed one particular decision up or down.
- **Saliency maps** highlight the pixels of an image that most affected a vision model's answer.
- **Counterfactual explanations** say what would have had to be different: "If your income had been £57,500 instead of £38,000, the loan would have been approved."

!diagram ai-explanations

Explanations of complex models are approximations, and a convincing explanation can still be wrong. They help, but they do not replace testing.
"""),
        Section("Privacy", """
Models can leak the data they were trained on. In 2021 researchers extracted names, phone numbers and email addresses that GPT-2 had memorised word for word from its training text. And "anonymised" data is often not anonymous: in 2008, researchers re-identified people in a dataset of film ratings released by Netflix by matching it against public reviews.

Two techniques protect privacy by design:

- **Differential privacy** adds carefully measured random noise to results, so that no answer reveals much about any one person. A parameter ε (epsilon) sets the trade-off: smaller ε means more noise and more privacy. The 2020 US Census used it.

!diagram ai-differential-privacy

- **Federated learning** trains a shared model without collecting the raw data: each phone improves the model on its own data and sends back only the changes, which are averaged on the server. Phone keyboards learn to predict the next word this way.

!diagram ai-federated

The simplest rule of all is **data minimisation**: do not collect, keep or train on personal data you do not need.
"""),
        Section("Robustness and adversarial examples", """
In 2014 researchers showed that adding a carefully designed pattern of noise, too faint for a person to see, made an image classifier change its answer for a photo of a panda from "panda" to "gibbon", with 99% confidence. These **adversarial examples** work against almost every kind of neural network, and in 2018 a few stickers on a real stop sign were enough to make a vision system read it as a speed limit sign.

!diagram ai-adversarial

Defences include **adversarial training** (adding such examples to the training data), checking whether an input looks unlike the training data, and never relying on one model alone where safety matters. The deeper lesson is that a model can score brilliantly on a test set yet fail on inputs that would never fool a person.
"""),
        Section("Safety and alignment", """
**Alignment** is the problem of making AI systems pursue what their designers and users actually intend, not just what they were literally rewarded for (Level 13's reward hacking). As systems become more capable, the questions get more serious:

- Will a model tell people what they want to hear rather than what is true?
- Could it help someone cause serious harm, for example with cyber attacks or dangerous chemistry?
- Does it behave the same when it is not being tested?

Developers evaluate models for dangerous capabilities before release, pay **red teams** to attack them, train them to refuse harmful requests, and study their insides with **interpretability** research, looking for the circuits that implement behaviours. In November 2023, 28 countries and the EU signed the Bletchley Declaration on AI safety at Bletchley Park, and the UK set up a government AI Safety Institute, since renamed the AI Security Institute, to test advanced models.
"""),
        Section("AI and the law", """
Laws already apply to AI, and new ones are arriving.

- **Data protection**: the GDPR, which the UK keeps in its own version, gives people rights over their personal data, including rights around decisions made solely by automated means that have legal or similarly significant effects, and a right to meaningful information about how such decisions are made.
- **Equality law** forbids discrimination by protected characteristics, whether a person or an algorithm does it.
- **The EU AI Act**, in force since August 2024 with its rules applying in stages, sorts AI systems by risk:

!diagram ai-eu-ai-act

Uses with **unacceptable risk**, such as social scoring by governments, have been banned since February 2025. **High-risk** uses, such as screening job applicants, credit scoring, marking exams and safety components of medical devices, must meet requirements for data quality, documentation, human oversight and accuracy. **Limited-risk** systems must be transparent: people must be told they are talking to a chatbot, and deepfakes must be labelled.

Copyright is still being argued in courts and parliaments: whether training on copyrighted books, art and music without permission is lawful, and who owns what an AI produces.
"""),
        Section("AI and society", """
- **Work**: AI automates some tasks and assists with others. Most jobs are bundles of tasks, so many will change more than disappear, but the benefits and costs will not fall evenly.
- **Information**: cheap fluent text, images and voices make misinformation and scams easier, and make provenance (Level 12) more important.
- **Energy and resources**: the International Energy Agency estimated that data centres used about 415 terawatt-hours of electricity in 2024, around 1.5% of the world's electricity, with AI a fast-growing share; cooling also uses water.
- **Power**: training frontier models costs so much that few organisations can do it, which concentrates influence.
- **Benefits**: AI already helps detect disease in scans, predict protein structures, translate between languages, make technology accessible to people with disabilities, and speed up science.

Engineers do not decide all of these questions alone, but they decide many of the details that settle them.
"""),
        Section("Hands-on: auditing a model", """
### Fairness metrics for two groups

```python
# Outcomes of a loan model for two groups of applicants.
# tp: would repay, approved; fn: would repay, refused; fp: approved but did not repay; tn: refused, did not repay
groups = {"group A": {"tp": 360, "fn": 40, "fp": 120, "tn": 480},
          "group B": {"tp": 120, "fn": 80, "fp": 40, "tn": 760}}

print(f"{'':8} {'approved':>9} {'TPR':>6} {'FPR':>6} {'precision':>10}")
for name, g in groups.items():
    n = sum(g.values())
    selection = (g["tp"] + g["fp"]) / n                 # demographic parity compares this
    tpr = g["tp"] / (g["tp"] + g["fn"])                 # equal opportunity compares this
    fpr = g["fp"] / (g["fp"] + g["tn"])                 # equalised odds compares TPR and this
    precision = g["tp"] / (g["tp"] + g["fp"])           # predictive parity compares this
    print(f"{name:8} {selection:9.0%} {tpr:6.0%} {fpr:6.0%} {precision:10.0%}")
```

### Explaining one decision

```python
weights = {"income (thousands)": 0.08, "years at address": 0.3, "missed payments": -1.2}
bias = -4.0

def score(person):
    return bias + sum(weights[k] * person[k] for k in weights)

applicant = {"income (thousands)": 38, "years at address": 2, "missed payments": 1}
s = score(applicant)
print(f"score {s:.2f}: {'approved' if s >= 0 else 'refused'}")
print("contribution of each feature:")
print(f"  {'starting point':20} {bias:+6.2f}")
for k, w in weights.items():
    print(f"  {k:20} {w * applicant[k]:+6.2f}")
print("smallest single change that would approve this application:")
for k, w in weights.items():
    target = applicant[k] - s / w                 # the value of this feature that brings the score to 0
    if target >= 0:
        print(f"  {k}: {applicant[k]} -> {target:.1f}")
    else:
        print(f"  {k}: no possible value is enough on its own")
```

### Differential privacy in one line of noise

```python
import random

random.seed(3)
def laplace(scale):
    # the difference of two exponential random numbers has a Laplace distribution
    return random.expovariate(1 / scale) - random.expovariate(1 / scale)

true_count = 142            # e.g. how many students in a survey said they had been bullied
for epsilon in (0.1, 0.5, 1.0, 5.0):
    answers = [true_count + laplace(1 / epsilon) for _ in range(1000)]
    typical_error = sum(abs(a - true_count) for a in answers) / len(answers)
    print(f"epsilon {epsilon:3}: one released answer {answers[0]:7.1f}; typical error {typical_error:5.1f}")
```

Adding or removing one student changes the true count by at most 1, and with ε = 0.5 the noise is typically about 2, so nobody can tell from the answer whether any one student took part.

### Try this

1. Change group B's numbers so that its true positive rate matches group A's. What happens to its precision?
2. Give the applicant 0 missed payments. Is the loan approved now? What does the counterfactual say?
"""),
        Section("Level check", """
+ Describe real cases where AI systems caused harm, and why
+ Define demographic parity, equal opportunity, equalised odds and predictive parity, and calculate them
+ Explain why fairness definitions can conflict
+ Describe where bias enters and three places to mitigate it
+ Compare ways of explaining a model's decisions, including counterfactuals
+ Explain differential privacy and federated learning
+ Explain adversarial examples and defences against them
+ Explain what alignment means and how developers test for safety
+ Describe the EU AI Act's risk tiers and data protection rights over automated decisions
+ Discuss AI's effects on work, information, energy and power
"""),
    ],
    keyterms=[
        ("Demographic parity", "Equal shares of each group receiving the positive decision."),
        ("Equal opportunity", "Equal true positive rates: deserving people in each group are approved equally often."),
        ("Equalised odds", "Equal true positive and false positive rates across groups."),
        ("Predictive parity", "Equal precision across groups: a positive decision means the same for everyone."),
        ("Counterfactual explanation", "A statement of the smallest change to the inputs that would have changed the decision."),
        ("SHAP", "A method that estimates how much each feature pushed one prediction up or down."),
        ("Differential privacy", "Adding measured noise to results so that no answer reveals much about any individual."),
        ("Federated learning", "Training a shared model on many devices, sending model updates instead of raw data."),
        ("Data minimisation", "Collecting and keeping only the personal data a task needs."),
        ("Adversarial example", "An input altered, often invisibly, to make a model give a wrong answer."),
        ("Alignment", "Making AI systems pursue what people actually intend."),
        ("Red teaming", "Deliberately attacking a system to find harmful behaviour before release."),
        ("EU AI Act", "European law that regulates AI systems according to their level of risk."),
    ],
    mistakes=[
        "Thinking a model is fair because it ignores protected characteristics. Postcodes, names and other proxies can carry the same information.",
        "Assuming one fairness measure settles the question. The definitions conflict, so the choice is a judgement about the situation.",
        "Treating anonymised data as safe. Records can often be re-identified by matching them with other data.",
        "Trusting a high test score as proof of safety. Adversarial and unusual inputs can still break the model.",
        "Believing AI law is only coming in the future. Data protection and equality law already apply to automated decisions.",
    ],
    grade="""
### The impossibility result, in one line

Precision, recall and the false positive rate are linked by the base rate p, the share of a group that is truly positive:

FPR = p ÷ (1 − p) × (1 − precision) ÷ precision × TPR

If two groups have the same precision and the same TPR but different base rates p, the right-hand side differs, so their false positive rates must differ. Equal precision and equal error rates cannot all hold at once unless the base rates are equal or the model is perfect. You can check it with the hands-on numbers: group A has p = 0.4, group B has p = 0.2.

### Model collapse of the commons

As more of the web is written by AI, future models trained on web text learn partly from earlier models, and rare voices, languages and ideas risk being drowned out. Careful data curation, provenance labels and preserving human-written archives are becoming part of responsible AI too.
""",
    quiz=[
        Q("What does equal opportunity require across groups?",
          ["Equal true positive rates", "Equal numbers of people in each group",
           "Equal shares of people approved", "Equal average scores"], 0,
          "Deserving people in every group should be approved equally often."),
        Q("Group A has 48% of applicants approved and group B 16%. Which fairness definition is clearly broken?",
          ["Demographic parity", "Predictive parity", "Equal precision", "Data minimisation"], 0,
          "Demographic parity compares the share of each group approved."),
        Q("Why can a model not usually satisfy every fairness definition at once?",
          ["With different base rates, the definitions contradict", "Computers are too slow to check them all at once",
           "The definitions all measure exactly the same thing", "Fairness can only be measured after the release"], 0,
          "Choosing between them is a value judgement, not a calculation."),
        Q("A model removes the \"gender\" column but still treats women worse. What is the most likely reason?",
          ["Other features act as proxies for gender", "The model has too few layers",
           "The learning rate was too high", "The test set was too large"], 0,
          "Hobbies, job titles or words in a CV can carry the same information."),
        Q("\"If your income had been £57,500 instead of £38,000, the loan would have been approved.\" What kind of explanation is this?",
          ["A counterfactual explanation", "A saliency map", "A global feature importance", "A confusion matrix"], 0,
          "It states the smallest change that would have flipped the decision."),
        Q("In differential privacy, what happens as ε gets smaller?",
          ["More noise is added, giving more privacy and less accuracy", "Less noise is added and privacy falls",
           "The data is deleted after training", "The model trains faster"], 0,
          "ε sets the trade-off between privacy and accuracy."),
        Q("What does federated learning send from each phone to the server?",
          ["Updates to the model, not the raw data", "Every message typed on the phone",
           "A copy of the phone's photos", "Nothing at all"], 0,
          "The server averages the updates into a shared model."),
        Q("What is an adversarial example?",
          ["An input changed slightly, often invisibly, so the model gets it wrong", "A training example with a missing label",
           "A test question copied into the training data", "An example chosen at random from the data"], 0,
          "A faint pattern of noise turned a panda into a \"gibbon\" for an image classifier."),
        Q("Under the EU AI Act, which of these is treated as high-risk?",
          ["Screening job applicants", "A spam filter", "A video game opponent", "Recommending songs"], 0,
          "Employment, credit, education and medical uses must meet strict requirements."),
        Q("Which right gives people protection against decisions made solely by automated means with significant effects?",
          ["A data protection right in the GDPR", "Copyright law", "The right to free speech", "Consumer refund rules"], 0,
          "People are also entitled to meaningful information about the logic involved."),
    ],
    exam=[
        EQ("A university uses a model to decide which applicants to interview. Explain how it could check whether the model is fair, and why this is not straightforward.", 6,
           [MP("Compare outcomes across groups (e.g. sex, ethnicity, disability)", ["compare", "group", "across"]),
            MP("Selection rate / demographic parity", ["selection rate", "demographic parity", "share interviewed", "approved"]),
            MP("True positive rate / equal opportunity among qualified applicants", ["true positive", "equal opportunity", "qualified"]),
            MP("Precision / predictive parity, or error rates / equalised odds", ["precision", "predictive parity", "false positive", "equalised odds", "error rate"]),
            MP("The definitions conflict when base rates differ, so not all can be met", ["conflict", "base rate", "cannot all", "impossib"]),
            MP("Proxies, poor labels, small groups or historical bias complicate it; a value judgement and the affected people are needed", ["proxy", "label", "small", "historical", "judgement", "consult"])],
           "The university should audit the model's decisions separately for different groups, such as sex, ethnicity and disability. It can compare the selection rate, the share of each group invited to interview, which tests demographic parity; the true positive rate among applicants who would succeed, which tests equal opportunity; and the precision and false positive rates, which test predictive parity and equalised odds. This is not straightforward because these definitions conflict: when groups have different base rates, a model cannot satisfy them all, so the university has to decide which matters most here, ideally with the people affected. The labels may themselves be biased, other features may act as proxies for protected characteristics, and small groups give unreliable figures.",
           command="Explain"),
        EQ("Compare differential privacy and federated learning as ways of protecting people's data.", 4,
           [MP("Differential privacy adds measured random noise to results or training", ["noise", "random"]),
            MP("So no output reveals much about any one person; ε sets the privacy/accuracy trade-off", ["one person", "individual", "ε", "epsilon", "trade-off"]),
            MP("Federated learning keeps raw data on the devices and sends only model updates", ["device", "phone", "updates", "raw data", "local"]),
            MP("Federated learning alone can still leak information through updates; the two are often combined", ["leak", "combined", "together", "still"])],
           "Differential privacy adds carefully measured random noise to statistics or to the training process, so that no released result reveals much about whether any one person's data was included; the parameter ε controls how much noise, trading privacy against accuracy. Federated learning instead keeps the raw data on people's own devices: each device improves the model locally and sends only the changes to a server, which averages them. Federated learning stops raw data being collected in one place, but the updates themselves can still leak information, so the two are often combined, with noise added to the updates.",
           command="Compare"),
        EQ("Evaluate the risk-based approach of the EU AI Act.", 5,
           [MP("Systems are sorted into tiers: unacceptable (banned), high, limited and minimal risk", ["tier", "banned", "unacceptable", "high", "limited", "minimal"]),
            MP("High-risk uses (jobs, credit, education, medical) must meet requirements such as data quality, documentation and human oversight", ["data quality", "documentation", "oversight", "requirement"]),
            MP("Strength: focuses effort on uses that can harm people, while leaving low-risk uses free to innovate", ["focus", "proportion", "innovat", "low-risk"]),
            MP("Weakness: classifying systems can be hard, general-purpose models fit awkwardly, and compliance costs burden small firms", ["hard to classify", "general-purpose", "cost", "small", "burden"]),
            MP("A judgement weighing protection against innovation and enforcement", ["judgement", "overall", "balance", "enforce"])],
           "The EU AI Act sorts AI systems by the harm they could do: uses with unacceptable risk, such as government social scoring, are banned; high-risk uses, such as screening job applicants, credit scoring and marking exams, must meet requirements for data quality, documentation, accuracy and human oversight; limited-risk systems such as chatbots must be transparent; and minimal-risk uses such as spam filters face no new rules. Its strength is proportion: the strictest rules fall on uses that affect people's lives, while low-risk innovation is left alone. Its weaknesses are that deciding which tier a system belongs to can be hard, general-purpose models that can be used for anything fit the tiers awkwardly, and compliance costs fall heavily on small companies. Overall it is a sensible framework, but its success will depend on clear guidance and on enforcement.",
           command="Evaluate"),
    ],
)

L15_2 = Topic(
    slug="capstone-build-your-own-ai",
    title="Capstone: Build, Test and Explain Your Own AI",
    spec="15.2",
    icon="i-trophy",
    minutes=60,
    exam_title=NEA,
    blurb="Your final project: choose a problem, plan it on a project canvas, follow eight milestones from data to demo, study a complete worked project that builds a spam classifier from scratch, analyse its errors, check it responsibly, write a model card, and present it. Then a map of everything you have learned, and where to go next.",
    fact="The first spam filters that learned from examples, in the late 1990s, used the same idea as this lesson's worked project: count which words appear in spam and which in genuine messages, and let the evidence add up.",
    sections=[
        Section("Your mission", """
Fourteen levels have taken you from the history of AI to transformers, generative models, agents and the engineering of real systems. The capstone puts it together: **design, build, test and explain an AI system of your own**, the way a professional would.

You will produce:

1. A **working model**, in Python, that does something useful or interesting.
2. An **evaluation**: how well it works, compared with a baseline, with its mistakes analysed.
3. A **model card**: what it is for, how it was built, how well it works and for whom, and its limitations.
4. A short **presentation or demo** for someone else.

The [certificate for this course](/ai/certificate/) unlocks when you score at least 70% on every lesson's quiz. The capstone is how you prove the skills to yourself, and to anyone you show it to.
"""),
        Section("Choose a project", """
Pick a project you care about, small enough to finish. Some ideas, with the levels they draw on:

| Project | What it does | Builds on |
| Message classifier | Sorts messages into spam and genuine, or by topic | Levels 3, 4 and 5 |
| Digit recogniser | Reads handwritten digits from a small drawn grid | Levels 6, 7 and 8 |
| Review sentiment | Decides whether a review is positive or negative | Levels 4 and 9 |
| Book or film recommender | Suggests items from what similar people liked | Levels 4 and 9 |
| Game-playing agent | Learns to play a simple game you design | Level 13 |
| Notes assistant | Answers questions about your own notes with retrieval | Levels 9 and 11 |
| Image filter explorer | Designs kernels that find features in pictures | Level 8 |
| Fairness audit | Measures how a model or dataset treats different groups | Levels 3, 4 and 15 |

A good first project has data you can get or make yourself, a clear way to measure success, and a simple baseline to beat.
"""),
        Section("Plan it on a canvas", """
Before writing code, fill in a **project canvas**. It takes ten minutes and saves days.

!diagram ai-project-canvas

The most important box is **success**: decide now how you will measure whether the model works, and what the baseline scores, so you cannot fool yourself later.
"""),
        Section("Eight milestones", """
!diagram ai-capstone-roadmap

1. **Define**: the problem, the users and the success measure.
2. **Data**: collect or create it, label it, split it into training, validation and test sets, and look at it.
3. **Baseline**: the simplest possible approach, such as always predicting the most common class.
4. **First model**: the simplest model that could work. Get it running end to end before improving anything.
5. **Evaluate**: measure it on the validation set, with a confusion matrix, not only accuracy.
6. **Improve**: look at the mistakes, form a hypothesis, change one thing, and measure again. Keep a log.
7. **Check responsibly**: who could be harmed, does it work equally well for different users, what personal data does it touch?
8. **Present**: test once on the test set, write the model card, and show it to someone.
"""),
        Section("Worked project: a spam classifier from scratch", """
Here is a complete small project, every step in plain Python: data, features, a logistic regression model trained by gradient descent, evaluation on unseen messages, and an explanation of what it learned.

```python
import math, random

# 1. Data: messages labelled 1 for spam and 0 for genuine ("ham")
messages = [
    ("win a free phone now claim your prize", 1), ("you have won cash text claim now", 1),
    ("urgent your account is locked click the link", 1), ("free entry to win a holiday reply yes", 1),
    ("cheap loans approved today no checks", 1), ("claim your free gift card now", 1),
    ("congratulations you won a prize call now", 1), ("limited offer win cash click here", 1),
    ("your parcel is waiting pay the fee at this link", 1), ("earn money fast from home click now", 1),
    ("final notice claim your refund now", 1), ("free ringtones text win to claim", 1),
    ("are we still meeting at four", 0), ("can you send me the homework for maths", 0),
    ("dinner is at seven see you then", 0), ("thanks for the help with the project", 0),
    ("what time does the match start", 0), ("i left my coat at your house", 0),
    ("happy birthday hope you have a great day", 0), ("can you pick up milk on the way home", 0),
    ("the bus is late i will be ten minutes", 0), ("did you finish reading the book", 0),
    ("see you at football practice tomorrow", 0), ("mum says dinner is ready", 0),
    ("free tickets for the school play this friday", 0), ("call me when you get this", 0),
]
random.seed(7)
random.shuffle(messages)
train, test = messages[:20], messages[20:]

# 2. Features: which words appear (a bag of words)
vocab = sorted({w for text, _ in train for w in text.split()})
def features(text):
    words = set(text.split())
    return [1.0 if w in words else 0.0 for w in vocab]

# 3. Model: logistic regression, trained by gradient descent
w = [0.0] * len(vocab)
b = 0.0
def predict(text):
    z = b + sum(wi * xi for wi, xi in zip(w, features(text)))
    return 1 / (1 + math.exp(-z))

for epoch in range(300):
    for text, label in train:
        x = features(text)
        error = predict(text) - label                 # gradient of the cross-entropy loss
        w = [wi - 0.1 * error * xi for wi, xi in zip(w, x)]
        b -= 0.1 * error

# 4. Evaluate on messages the model has never seen
tp = fp = fn = tn = 0
for text, label in test:
    guess = 1 if predict(text) >= 0.5 else 0
    tp += guess == 1 and label == 1
    fp += guess == 1 and label == 0
    fn += guess == 0 and label == 1
    tn += guess == 0 and label == 0
    flag = "" if guess == label else "   <- wrong"
    print(f"{predict(text):.2f}  {'spam' if guess else 'ham ':4}  {text}{flag}")
print(f"test accuracy {(tp + tn) / len(test):.0%}: caught {tp} spam, missed {fn}, false alarms {fp}")

# 5. Explain: the words the model learned to trust most
ranked = sorted(zip(w, vocab))
print("most spammy words:", ", ".join(v for _, v in ranked[-6:][::-1]))
print("most genuine words:", ", ".join(v for _, v in ranked[:6]))
```

### Error analysis

The model missed "cheap loans approved today no checks". Why? None of those words appeared in a spam message in its training set, so it had no evidence either way. That one mistake suggests the most useful next step: **more varied training data**, not a bigger model. It also shows the limits of so small a test set: six messages cannot tell you the real accuracy to within more than a few tens of per cent.

### Its model card

| Section | Entry |
| **Purpose** | Flag likely spam text messages for a person to check. Not for deleting messages automatically. |
| **Data** | 26 short English messages written for this exercise: 12 spam, 14 genuine. |
| **Model** | Logistic regression on which words appear (bag of words), trained by gradient descent. |
| **Performance** | 5 of 6 test messages correct (83%); the test set is far too small for a reliable figure. |
| **Limitations** | Knows only words it has seen; misses spam that uses new words; English only; easily fooled by misspellings. |
| **Risks** | False alarms could hide genuine messages, so a person should review flagged ones. |
"""),
        Section("Check it responsibly", """
Before anyone relies on your project, work through these questions, and write the answers into your model card:

+ Who will use it, and who will it affect who is not using it?
+ What happens when it is wrong, in each direction? Which mistake is worse?
+ Does it work equally well for different groups of people, accents, languages or devices?
+ What personal data does it collect, keep or learn from, and is all of it needed?
+ Could someone misuse it, or attack it with crafted inputs?
+ Can you explain an individual decision to the person it affects?
+ Is there a person who can override it?
"""),
        Section("Present it", """
A good presentation of an AI project answers five questions in order:

1. **What problem**, and for whom?
2. **What did you build**, in one picture?
3. **How well does it work**, compared with the baseline, and where does it fail? Show real mistakes.
4. **What would you do next**, and why?
5. **What should people be careful about**, from your model card?

Share your code with a short README explaining how to run it. A project that someone else can run and understand is worth far more than a slightly more accurate one that nobody can.
"""),
        Section("Everything you have learned", """
!diagram ai-course-map

From here, the paths divide:

- **Machine learning engineer**: build and run models in products. Next: a deep learning library such as PyTorch, cloud GPUs, and Level 14's engineering in practice.
- **Researcher**: invent new methods. Next: the mathematics underneath, linear algebra, probability and calculus, and reading papers.
- **AI product designer**: decide what AI should do for people. Next: user research and design, and Level 15's questions.
- **Policy and law**: shape how society governs AI. Next: law, ethics and economics, with the technical understanding you now have.

Whichever path you take: keep building small things, read widely, test everything, and stay curious about both what AI can do and what it should do.
"""),
        Section("Level check", """
+ Choose a project with available data, a success measure and a baseline
+ Fill in a project canvas
+ Follow the eight milestones from definition to presentation
+ Build, train and evaluate a model from scratch, with a confusion matrix
+ Analyse errors and choose the most useful next step
+ Carry out a responsible AI check
+ Write a model card
+ Present a project clearly, including its limitations
"""),
    ],
    keyterms=[
        ("Capstone project", "A final project that brings together everything a course has taught."),
        ("Project canvas", "A one-page plan of a project's problem, users, data, success measure, model, risks and demo."),
        ("Baseline", "The simplest approach a model must beat to be worth building."),
        ("End to end", "A version of the whole system that runs from raw input to final output, however simple."),
        ("Error analysis", "Studying a model's mistakes to find patterns and decide what to improve."),
        ("Ablation", "Removing one part of a system to measure how much it contributes."),
        ("Model card", "A short document describing a model's purpose, data, performance, limitations and risks."),
        ("README", "A file explaining what a project is and how to run it."),
        ("Reproducible", "Able to be run again by someone else to get the same results."),
    ],
    mistakes=[
        "Choosing a project with no available data. Check the data exists before anything else.",
        "Building a complex model before a baseline. Without one, you cannot tell whether the model helps.",
        "Tuning on the test set. Use the validation set to choose, and the test set once at the end.",
        "Reporting only accuracy. Show the confusion matrix and real mistakes.",
        "Hiding the limitations. A model card that lists them honestly makes a project more credible, not less.",
    ],
    grade="""
### Ablations: what really matters?

Once your model works, remove one ingredient at a time, a feature, a layer, a cleaning step, and measure how much worse it gets. These **ablation** studies show which parts of a system earn their place. Researchers include them in almost every paper, because they turn "it works" into "it works because of this".

### From toy to real

The worked project's 26 messages make the ideas clear but are far too few for a real filter. A real version would use thousands of labelled messages, split by date so the test set comes after the training data, handle misspellings and links, and be evaluated on the cost of each kind of error. The structure, though, would be exactly the same: data, features, model, evaluation, error analysis, model card.
""",
    quiz=[
        Q("What should a good first capstone project have?",
          ["Data you can get, a success measure and a baseline", "The largest model you can find",
           "A dataset of millions of examples", "A finished product on its first day"], 0,
          "Those three make it possible to finish and to know whether it worked."),
        Q("Why build a baseline before the real model?",
          ["To know whether the model is actually any better", "Because baselines are always more accurate",
           "Because the model cannot train without one", "To make the test set bigger"], 0,
          "A model that cannot beat a simple baseline is not worth deploying."),
        Q("When should the test set be used?",
          ["Once, at the end, after all choices are made", "After every change, to pick the best version",
           "Before training, to choose the features", "Never: it is only for documentation"], 0,
          "Choices are made on the validation set, or the test stops being fair."),
        Q("The spam model missed \"cheap loans approved today no checks\". What is the most useful next step?",
          ["Add more varied spam messages to the training data", "Use a model with many more layers",
           "Remove the test set", "Raise the learning rate"], 0,
          "None of those words appeared in training spam: the model lacked evidence, not capacity."),
        Q("Why is a test set of six messages a problem?",
          ["The accuracy measured on it is very unreliable", "Six messages take too long to test",
           "Models cannot be tested on short messages", "It makes the model overfit"], 0,
          "One message more or less right changes the accuracy by about 17 percentage points."),
        Q("What is error analysis?",
          ["Studying the model's mistakes to decide what to improve", "Counting how many errors the code has",
           "Removing all the wrong predictions from the results", "Adding errors to the training data"], 0,
          "Patterns in the mistakes point to the most useful change."),
        Q("Which belongs in a model card?",
          ["The model's limitations and risks", "Your passwords", "Every training message in full",
           "Only the best result you achieved"], 0,
          "Honest limitations help people use the model safely."),
        Q("What does \"end to end\" mean when building a first model?",
          ["A simple version of the whole system runs from input to output", "Every part is as accurate as possible",
           "The model is trained on all the data at once", "The project is finished"], 0,
          "Get it all working simply first, then improve the weakest part."),
        Q("What does an ablation study measure?",
          ["How much each part contributes, by removing it", "How fast the model trains",
           "How many users the model has", "How large the dataset is"], 0,
          "It shows which ingredients earn their place."),
        Q("Which question belongs in a responsible AI check?",
          ["Does it work equally well for different groups of people?", "Which colour should the website be?",
           "How many lines of code does it have?", "Which programming language is fastest?"], 0,
          "Fairness, privacy, misuse and oversight all belong in the check."),
    ],
    exam=[
        EQ("Plan a capstone project that builds a model to sort customer emails into \"complaint\", \"question\" and \"praise\". Describe the main stages.", 6,
           [MP("Define the problem, users and a success measure (e.g. accuracy/F1 per class, compared with a baseline)", ["success", "measure", "metric", "users", "define"]),
            MP("Collect and label example emails, checking label quality", ["collect", "label", "data"]),
            MP("Split into training, validation and test sets", ["split", "training", "validation", "test"]),
            MP("Build a baseline (e.g. most common class or keyword rules)", ["baseline", "most common", "rule"]),
            MP("Train a model (e.g. bag of words with logistic regression) end to end", ["train", "logistic", "bag of words", "model"]),
            MP("Evaluate with a confusion matrix and analyse errors; improve", ["confusion", "error analysis", "mistakes", "improve"]),
            MP("Responsible check and model card; present", ["model card", "responsible", "privacy", "present"])],
           "First I would define the problem: sorting emails so staff can answer complaints quickly, measured by the precision and recall for each class compared with a baseline that always predicts the most common class. Next I would collect several hundred real or realistic emails, label them carefully, and split them into training, validation and test sets. I would build the baseline, then a simple model, such as logistic regression on a bag of words, running end to end. I would evaluate it on the validation set with a confusion matrix, study the misclassified emails to decide what to improve, and change one thing at a time. Finally I would check privacy, since emails contain personal data, test the final model once on the test set, write a model card listing its limitations, and present it.",
           command="Describe"),
        EQ("Explain why error analysis and a model card make an AI project more trustworthy.", 4,
           [MP("Error analysis reveals patterns in the model's mistakes", ["pattern", "mistakes", "errors"]),
            MP("It shows what to improve, e.g. more varied data rather than a bigger model", ["improve", "data", "next step"]),
            MP("A model card documents purpose, data, performance and limitations", ["purpose", "data", "performance", "limitation"]),
            MP("So users know when not to rely on it and can use it safely / honesty builds trust", ["not to rely", "safely", "honest", "trust", "misuse"])],
           "Error analysis looks closely at the model's actual mistakes, revealing patterns such as missing spam that uses words never seen in training, which shows what would really improve it, more varied data rather than a bigger model, and shows the builder understands its behaviour. A model card records the model's purpose, what it must not be used for, its data, its performance overall and for different groups, and its limitations and risks. Together they let users know when the model can be relied on and when it cannot, which makes it safer to use, and honesty about weaknesses makes the whole project more credible.",
           command="Explain"),
    ],
)

TOPICS = [L15_1, L15_2]
