"""Artificial Intelligence: Zero to Hero. A course taught in numbered levels.

One module per level, each holding two lessons. TOPICS is the teaching order;
INPUTS and EXPECT are only read by tools/check_python_examples.py. Passing every
lesson's quiz unlocks the printable certificate at /ai/certificate/.
"""
from mskbuild.models import Unit, Course
from . import (level01, level02, level03, level04, level05, level06, level07,
               level08, level09, level10, level11, level12, level13, level14,
               level15)

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
    (level06, "level-6", "Level 6: The Artificial Neuron",
     "The building block of every network: weights, bias and a weighted sum, decision boundaries, logic gates, the perceptron and the XOR problem, then the activation functions that give networks their power.",
     "i-gate", "Level 6 · Builder"),
    (level07, "level-7", "Level 7: Neural Networks",
     "Neurons wired into layers: matrix multiplication, the forward pass, hidden layers that reshape space, counting parameters, and backpropagation, built from scratch and used to train a network live.",
     "i-layers", "Level 7 · Builder"),
    (level08, "level-8", "Level 8: Seeing: Convolutional Networks",
     "How machines see: kernels that slide across an image to find edges and textures, stride, padding and pooling, feature maps stacked into volumes, and the networks from LeNet to ResNet that turned pixels into predictions.",
     "i-image", "Level 8 · Practitioner"),
    (level09, "level-9", "Level 9: Language as Numbers",
     "How text becomes maths: tokens and byte pair encoding, embeddings where meaning becomes geometry, cosine similarity and word analogies, then language models from n-grams to recurrent networks, LSTMs and the bottleneck that led to attention.",
     "i-language", "Level 9 · Practitioner"),
    (level10, "level-10", "Level 10: Attention and Transformers",
     "The idea that changed AI: attention that lets every word look at every other, queries, keys and values, masks and multi-head attention, then positional encoding and the transformer block that powers every modern language model.",
     "i-target", "Level 10 · Advanced"),
    (level11, "level-11", "Level 11: Large Language Models",
     "How a transformer becomes an assistant: pretraining on trillions of tokens, compute and scaling laws, instruction tuning and RLHF, then using models well with sampling, prompting, retrieval, tools, LoRA fine-tuning, quantisation and fair evaluation.",
     "i-sparkle", "Level 11 · Advanced"),
    (level12, "level-12", "Level 12: Generative AI",
     "Machines that create: autoencoders and latent spaces, variational autoencoders, GANs and their troubles, diffusion models that turn noise into pictures, text guidance and latent diffusion, CLIP, multimodal models, and telling real from generated.",
     "i-palette", "Level 12 · Advanced"),
    (level13, "level-13", "Level 13: Reinforcement Learning and Agents",
     "Learning from rewards: returns, values, the Bellman equation, Q-learning and deep RL; game search with minimax, alpha-beta and Monte Carlo tree search; AlphaGo and AlphaZero; and AI agents that plan, use tools and act safely.",
     "i-route", "Level 13 · Expert"),
    (level14, "level-14", "Level 14: AI Engineering and Architecture",
     "Turning models into products: framing problems and metrics, data pipelines and leakage, tuning and training at scale, deployment, drift and model cards; then designing AI systems for speed, cost and safety, with a complete worked design.",
     "i-tools", "Level 14 · Expert"),
    (level15, "level-15", "Level 15: Responsible AI and Your Capstone",
     "Building AI that deserves trust: fairness measures that conflict, explanations, privacy, attacks and the law; then the capstone, where you plan, build, test and document an AI of your own from scratch, and finish the course.",
     "i-scales", "Level 15 · Hero"),
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
    blurb="A complete course in how artificial intelligence works and how to build it, in fifteen levels: the history and key dates, data, classic machine learning, gradient descent, artificial neurons, neural networks and backpropagation, convolutional networks, embeddings, attention and transformers, large language models, generative AI, reinforcement learning and agents, AI engineering and architecture, and responsible AI. Every lesson has diagrams, hands-on Python that runs in your browser, interactive labs, a quiz and questions to explain. Pass every quiz to earn your printable MskProd certificate.",
    intro="",
    units=UNITS,
)
