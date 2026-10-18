"""Artificial Intelligence: Zero to Hero. A course taught in numbered levels.

One module per level, each holding two lessons. TOPICS is the teaching order;
INPUTS and EXPECT are only read by tools/check_python_examples.py. Passing every
lesson's quiz unlocks the printable certificate at /ai/certificate/.
"""
from mskbuild.models import Unit, Course
from . import level01, level02, level03, level04, level05

# (module, unit slug, title, blurb, icon, stage label)
LEVELS = [
    (level01, "level-1", "Level 1: The Story of AI",
     "From Ada Lovelace's question in 1843 to systems that write, draw and reason: the key dates, the people, the two AI winters and why deep learning took off in 2012.",
     "i-book", "Level 1 · Beginner"),
    (level02, "level-2", "Level 2: What AI Is",
     "What AI means, how AI, machine learning, deep learning and generative AI fit together, AI as an agent, and the three ways machines learn: supervised, unsupervised and reinforcement, plus the self-supervised trick behind modern AI.",
     "i-brain", "Level 2 · Beginner"),
    (level03, "level-3", "Level 3: Data, the Fuel of AI",
     "How the world becomes numbers: features and labels, images, sound and text as tensors, scaling, splitting data into training, validation and test sets, cleaning it, and how bias gets in.",
     "i-database", "Level 3 · Beginner"),
    (level04, "level-4", "Level 4: Classic Machine Learning",
     "Your first real models: regression lines and planes, k-nearest neighbours, logistic regression, decision trees and forests, the confusion matrix, and k-means clustering, all built from scratch.",
     "i-chart", "Level 4 · Explorer"),
    (level05, "level-5", "Level 5: Learning by Descent",
     "How every modern model learns: loss functions, derivatives and gradients, loss landscapes in 3D, and gradient descent with learning rates, batches, momentum and Adam.",
     "i-route", "Level 5 · Explorer"),
]

UNITS = [Unit(slug, title, blurb, mod.TOPICS, icon=icon, term=term)
         for mod, slug, title, blurb, icon, term in LEVELS]
TOPICS = [t for u in UNITS for t in u.topics]
INPUTS = {}
for _mod, *_ in LEVELS:
    INPUTS.update(getattr(_mod, "INPUTS", {}))
EXPECT = {}
for _mod, *_ in LEVELS:
    EXPECT.update(getattr(_mod, "EXPECT", {}))

COURSE = Course(
    slug="ai",
    seo="AI course",
    extra_cta=("Your certificate", "/ai/certificate/", "i-trophy"),
    title="Artificial Intelligence: Zero to Hero",
    short="AI",
    stage="All",
    board="",
    code="",
    goal="Certificate",
    icon="i-sparkle",
    accent="var(--purple)",
    levels=True,
    blurb="A complete course in how artificial intelligence works and how to build it, in fifteen levels: the history and key dates, data, classic machine learning, gradient descent, artificial neurons, neural networks and backpropagation, convolutional networks, embeddings, attention and transformers, large language models, generative AI, reinforcement learning and agents, AI engineering and architecture, and responsible AI. Every lesson has diagrams, hands-on Python that runs in your browser, interactive labs, a quiz and questions to explain. Pass every quiz to earn your printable MsKprod certificate.",
    intro="",
    journey=[
        ("Go in order",
         "Every level uses the one before. Gradient descent needs the idea of a loss, backpropagation needs gradient descent, and attention needs embeddings. Skipping ahead is how AI starts to feel like magic.", ""),
        ("Run every example, then break it",
         "Each lesson's Python runs in your browser. Run it, predict what a change will do, make the change, and see whether you were right.", ""),
        ("Do the maths by hand once",
         "Work one neuron, one gradient step and one attention score on paper. After that the code is just the same sums done many times.", ""),
        ("Play with the labs",
         "The interactive labs let you drag points, turn weights and watch a model learn in 3D. Ten minutes of play builds an intuition no paragraph can.", ""),
        ("Build your own AI",
         "Level 15 is a capstone: you design, train, test and explain a model of your own, from data to a working demo.", ""),
        ("Earn your certificate",
         "Score at least 70% on every lesson quiz and your certificate unlocks. Put your name on it, choose a colour and print it.", ""),
    ],
    units=UNITS,
)
