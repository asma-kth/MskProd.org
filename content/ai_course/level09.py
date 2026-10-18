"""Level 9: Language as Numbers. Tokens, embeddings and sequence models."""
from mskbuild.models import Topic, Section, Q, EQ, MP

NEA = "Check you could explain this"

L9_1 = Topic(
    slug="tokens-and-embeddings",
    title="Tokens and Embeddings: Turning Words into Meaningful Numbers",
    spec="9.1",
    icon="i-language",
    minutes=38,
    exam_title=NEA,
    blurb="How text is split into tokens with byte pair encoding, why one-hot vectors cannot capture meaning, how embeddings place words in a space where meaning becomes geometry, cosine similarity, vector arithmetic like king − man + woman, and how embeddings are learned.",
    fact="In 1957 the linguist J. R. Firth wrote, \"You shall know a word by the company it keeps.\" Sixty years later that one sentence describes exactly how word embeddings are learned: from the words that appear around them.",
    sections=[
        Section("From text to tokens", """
A model cannot read letters. Text is first split into **tokens**, and each token is given an ID number from a fixed **vocabulary**.

!diagram ai-tokenisation

| Approach | Example: "unbelievably fast" | Problem |
| **Characters** | u, n, b, e, l, i, … | Sequences become very long, and single letters carry little meaning |
| **Words** | unbelievably, fast | Hundreds of thousands of words, and any word not seen in training is unknown |
| **Subwords** | un, believ, ably, fast | The best of both: common words stay whole, rare words split into familiar pieces |

Modern language models use subword tokens, with vocabularies of roughly 30,000 to 200,000 tokens. A rule of thumb for English: a token is about three quarters of a word, so 100 tokens is roughly 75 words.

!warn Tokens explain some strange mistakes :: A model sees "strawberry" as one or two tokens, not ten letters, which is one reason language models have struggled to count letters in words. Text in many non-English languages also splits into more tokens per word, so it costs more to process.
"""),
        Section("Byte pair encoding", """
The most common way to build a subword vocabulary is **byte pair encoding (BPE)**, an old data compression trick adapted for neural translation in 2015.

1. Start with every word split into single characters.
2. Count every pair of neighbouring symbols across the whole corpus.
3. Merge the most frequent pair into a new symbol, and add it to the vocabulary.
4. Repeat until the vocabulary reaches the size you want.

On a tiny corpus of "low" ×5, "lower" ×2, "newest" ×6 and "widest" ×3:

| Step | Most frequent pair | Merged into | Words afterwards |
| 1 | e + s (9 times) | es | low, lower, n e w es t, w i d es t |
| 2 | es + t (9 times) | est | n e w est, w i d est |
| 3 | l + o (7 times) | lo | lo w, lo w e r |
| 4 | lo + w (7 times) | low | low, low e r |
| 5 | n + e (6 times) | ne | ne w est |

After a few merges, frequent endings like "est" and whole frequent words like "low" are single tokens, while a word the tokenizer has never seen can still be built from pieces. The hands-on section runs this algorithm.
"""),
        Section("Why one-hot is not enough", """
Level 3 turned categories into **one-hot** vectors. For a 50,000-token vocabulary, each token becomes a list of 50,000 numbers with a single 1.

That has two fatal problems:

- **Size**: almost every number is zero, which wastes memory and compute.
- **No meaning**: every pair of one-hot vectors is exactly the same distance apart. "Cat" is as far from "kitten" as from "volcano", so nothing the model learns about cats helps it with kittens.

We want vectors where **similar meanings are close together**.
"""),
        Section("Embeddings: meaning as geometry", """
An **embedding** gives each token a dense vector of a few hundred or thousand learned numbers: 768 in the original BERT, 12,288 in GPT-3. The vectors are stored as the rows of an **embedding matrix**, and looking up a token simply means reading its row.

!diagram ai-embedding-3d

In a good embedding space:

- Words with similar meanings sit close together: cat near kitten near dog.
- Groups form: animals, foods, vehicles, places.
- **Directions** carry meaning: the step from "man" to "woman" is roughly the same as the step from "king" to "queen".

Real embeddings have hundreds of dimensions, which no one can picture. The 3D views here use a few hand-placed words to show the idea; researchers squash real embeddings down to 2D or 3D with methods such as t-SNE or UMAP to look at them.

!tool embedding-space

Turn the space in the lab, pick a word to see its nearest neighbours, and try your own analogies.
"""),
        Section("Measuring similarity: cosine", """
How close are two embeddings? The standard measure is the **cosine similarity**: the cosine of the angle between the two vectors.

!info Cosine similarity :: cos θ = (a · b) ÷ (|a| × |b|), the dot product divided by the two lengths

| Value | Angle | Meaning |
| 1 | 0° | Pointing the same way: very similar |
| 0 | 90° | Unrelated |
| −1 | 180° | Opposite |

!diagram ai-cosine

Dividing by the lengths means only the **direction** counts, not how long the vectors are. This is how search engines, recommendation systems and the retrieval step of AI assistants (Level 11) find the closest matches among millions of items.
"""),
        Section("Vector arithmetic and analogies", """
In 2013 Tomas Mikolov and colleagues at Google released **word2vec** and showed a striking property: you can do arithmetic with meaning.

!info The famous example :: vector("king") − vector("man") + vector("woman") ≈ vector("queen")

!diagram ai-word-analogy

The difference vector from "man" to "woman" captures something like a gender direction. Adding it to "king" lands near "queen". Similar patterns appear for capital cities (Paris − France + Italy ≈ Rome) and verb tenses (walking − walk + swim ≈ swimming).

!warn Embeddings learn our biases too :: Because embeddings are learned from human writing, they absorb its stereotypes. A 2016 study found that word2vec vectors trained on news text completed "man is to computer programmer as woman is to ..." with "homemaker". Engineers measure and reduce these biases before using embeddings in products.
"""),
        Section("How embeddings are learned", """
Embeddings rest on the **distributional hypothesis**: words that appear in similar contexts have similar meanings. "I fed the ___" might be followed by cat, dog or kitten, so those words should end up close together.

**word2vec** turned that into a training task:

- **Skip-gram**: given a word, predict the words around it.
- **CBOW** (continuous bag of words): given the surrounding words, predict the word in the middle.

The embeddings are the weights that make these predictions work. No one labels any meanings: the structure emerges from billions of words of ordinary text.

In a modern language model the embedding matrix is simply the first layer, learned along with every other parameter while the model learns to predict the next token. Later layers then refine each token's vector using its context, so that "bank" ends up with a different vector in "river bank" and "bank account". That is the job of attention, in Level 10.
"""),
        Section("Hands-on: tokens and embeddings in code", """
### Byte pair encoding

```python
from collections import Counter

corpus = {"low": 5, "lower": 2, "newest": 6, "widest": 3}
words = {tuple(w): n for w, n in corpus.items()}       # start from characters

for step in range(1, 7):
    pairs = Counter()
    for symbols, n in words.items():
        for a, b in zip(symbols, symbols[1:]):
            pairs[(a, b)] += n
    best = max(pairs, key=pairs.get)
    merged = {}
    for symbols, n in words.items():
        out, i = [], 0
        while i < len(symbols):
            if i + 1 < len(symbols) and (symbols[i], symbols[i + 1]) == best:
                out.append(symbols[i] + symbols[i + 1])
                i += 2
            else:
                out.append(symbols[i])
                i += 1
        merged[tuple(out)] = n
    words = merged
    print(f"merge {step}: {best[0]} + {best[1]} ({pairs[best]} times) ->",
          ", ".join(" ".join(s) for s in words))
```

### Cosine similarity and analogies

These embeddings are made by hand with four meaningful dimensions, royal, female, young and animal, so you can see why the arithmetic works. Learned embeddings have hundreds of dimensions with no labels.

```python
import math

emb = {
    "king":   [0.95, 0.05, 0.1, 0.0],  "queen":    [0.95, 0.95, 0.1, 0.0],
    "prince": [0.85, 0.05, 0.6, 0.0],  "princess": [0.85, 0.95, 0.6, 0.0],
    "man":    [0.10, 0.05, 0.1, 0.0],  "woman":    [0.10, 0.95, 0.1, 0.0],
    "boy":    [0.05, 0.05, 0.85, 0.0], "girl":     [0.05, 0.95, 0.85, 0.0],
    "cat":    [0.0, 0.5, 0.2, 0.95],   "kitten":   [0.0, 0.5, 0.9, 0.95],
    "dog":    [0.0, 0.5, 0.2, 0.9],    "puppy":    [0.0, 0.5, 0.9, 0.9],
}

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

def nearest(vector, exclude=()):
    scores = [(cosine(vector, v), w) for w, v in emb.items() if w not in exclude]
    return sorted(scores, reverse=True)[:3]

print("closest to cat:", [(w, round(s, 3)) for s, w in nearest(emb["cat"], {"cat"})])

def analogy(a, b, c):
    # a - b + c
    v = [x - y + z for x, y, z in zip(emb[a], emb[b], emb[c])]
    return nearest(v, {a, b, c})[0][1]

print("king - man + woman =", analogy("king", "man", "woman"))
print("kitten - cat + dog =", analogy("kitten", "cat", "dog"))
print("prince - boy + girl =", analogy("prince", "boy", "girl"))
```

### Try this

1. Add "lion" and "cub" to the embeddings, and check that cub − lion + cat gives kitten.
2. Run more BPE merges. Which whole words become single tokens first, and why those?
"""),
        Section("Level check", """
+ Compare character, word and subword tokenisation and explain why subwords are used
+ Carry out two steps of byte pair encoding on a small corpus
+ Explain two problems with one-hot vectors for words
+ Describe what an embedding is and what nearness and direction mean in an embedding space
+ Calculate a cosine similarity and interpret it
+ Explain how word2vec learns embeddings, and why embeddings can contain bias
"""),
    ],
    keyterms=[
        ("Token", "A piece of text, often part of a word, that a language model treats as one unit."),
        ("Vocabulary", "The fixed set of tokens a model knows, each with an ID number."),
        ("Tokeniser", "The program that splits text into tokens and turns them into IDs."),
        ("Byte pair encoding (BPE)", "Building a vocabulary by repeatedly merging the most frequent pair of neighbouring symbols."),
        ("Embedding", "A learned dense vector representing a token, placed so that similar meanings are close."),
        ("Embedding matrix", "The table of every token's embedding, one row per token."),
        ("Cosine similarity", "The cosine of the angle between two vectors: 1 for the same direction, 0 for unrelated."),
        ("Distributional hypothesis", "Words that appear in similar contexts have similar meanings."),
        ("word2vec", "A 2013 method that learns word embeddings by predicting words from their neighbours."),
        ("Contextual embedding", "A token's vector after the model has adjusted it for the words around it."),
    ],
    mistakes=[
        "Thinking a token is always a whole word. Most tokens are common words or pieces of words.",
        "Using one-hot vectors as if they carried meaning. Every one-hot vector is equally far from every other.",
        "Believing embeddings are written by people. They are learned from patterns in text.",
        "Expecting every analogy to work. The famous examples are among the best; many others fail.",
        "Forgetting that embeddings inherit the biases in the text they were learned from.",
    ],
    grade="""
### The embedding layer is just a matrix multiply

Looking up row i of the embedding matrix E is exactly the same as multiplying a one-hot vector for token i by E. So an embedding layer is a dense layer with no bias and no activation, applied to one-hot input, implemented as a fast lookup. Many language models also **tie** their weights, reusing the same matrix (transposed) in the final layer that turns hidden vectors back into scores for every token, which saves a large share of the parameters in small models.

### Sentence and document embeddings

The same idea extends from words to whole sentences, paragraphs and images. Models are trained so that texts with similar meanings get nearby vectors, regardless of wording: "How do I reset my password?" lands near "I forgot my login details". These **sentence embeddings** power semantic search and retrieval-augmented generation (Level 11), and models such as CLIP (Level 12) put images and text in the same space, so a picture of a dog lands near the words "a photo of a dog".
""",
    quiz=[
        Q("Why do modern language models use subword tokens?",
          ["Common words stay whole while rare words split into known pieces",
           "Subwords are always shorter than single characters",
           "They remove the need for a vocabulary entirely",
           "Each subword token is exactly one letter long"], 0,
          "Subwords avoid both enormous word vocabularies and very long character sequences."),
        Q("Roughly how many English words is 400 tokens?",
          ["About 300", "About 400", "About 100", "About 1,600"], 0,
          "A token averages about three quarters of a word: 400 × 0.75 = 300."),
        Q("In byte pair encoding, what is merged at each step?",
          ["The most frequent pair of neighbouring symbols",
           "The two longest words in the corpus",
           "Every pair of vowels in every word",
           "The two least common letters in the corpus"], 0,
          "Frequent pairs such as e + s become single symbols, then grow into longer pieces."),
        Q("What is wrong with one-hot vectors for words?",
          ["Every word is equally far from every other, so meaning is lost",
           "They can only represent a handful of different words",
           "They contain negative numbers that confuse the model",
           "They change every time the model is used"], 0,
          "They are also huge and mostly zeros."),
        Q("In a good embedding space, where is 'kitten'?",
          ["Close to 'cat'", "Equally far from every word", "At the origin", "Far from all animals"], 0,
          "Similar meanings are placed close together."),
        Q("Two vectors point in exactly the same direction. What is their cosine similarity?",
          ["1", "0", "−1", "It depends on their lengths"], 0,
          "Cosine similarity ignores length; the same direction gives the maximum, 1."),
        Q("Two vectors are a = [1, 0] and b = [0, 1]. What is their cosine similarity?",
          ["0", "1", "−1", "0.5"], 0,
          "Their dot product is 0: they are at right angles, unrelated."),
        Q("What does vector('king') − vector('man') + vector('woman') land closest to in word2vec?",
          ["vector('queen')", "vector('prince')", "vector('man')", "vector('kingdom')"], 0,
          "The man to woman step is roughly a gender direction, added to king."),
        Q("What is the distributional hypothesis?",
          ["Words that appear in similar contexts have similar meanings",
           "Every word should appear equally often in the training data",
           "Embeddings should be spread evenly through the space",
           "Longer words carry more meaning than short words"], 0,
          "It is why predicting a word's neighbours is enough to learn its meaning."),
        Q("Why can word embeddings contain stereotypes?",
          ["They are learned from human writing that contains those stereotypes",
           "Programmers deliberately add stereotypes to every model",
           "The maths of cosine similarity creates them",
           "Embeddings are copied from dictionaries"], 0,
          "Engineers measure and reduce such biases before deploying embeddings."),
    ],
    exam=[
        EQ("Explain what a word embedding is and why it is more useful than a one-hot vector.", 4,
           [MP("An embedding is a dense vector of learned numbers for each word / token", ["dense", "vector", "learned", "list of numbers"]),
            MP("Similar meanings have nearby vectors", ["similar", "close", "near"]),
            MP("One-hot vectors are all equally distant / carry no meaning", ["equally", "same distance", "no meaning", "unrelated"]),
            MP("One-hot vectors are huge and sparse; embeddings are compact", ["huge", "large", "sparse", "zeros", "compact", "smaller"])],
           "A word embedding represents each word, or token, as a dense vector of a few hundred learned numbers, positioned so that words with similar meanings have nearby vectors and directions in the space carry meaning. A one-hot vector, by contrast, has one position per word in the vocabulary, so it is huge and almost entirely zeros, and every pair of one-hot vectors is exactly the same distance apart, so it carries no information about meaning. With embeddings, what a model learns about one word helps it with similar words.",
           command="Explain"),
        EQ("Calculate the cosine similarity of a = [3, 4] and b = [4, 3].", 3,
           [MP("Dot product 3 × 4 + 4 × 3 = 24", ["24"]),
            MP("Lengths are both 5", ["5", "√25", "sqrt(25)"]),
            MP("24 ÷ 25 = 0.96", ["0.96", "24/25", "24 / 25"])],
           "The dot product is 3 × 4 + 4 × 3 = 24. Each vector has length √(9 + 16) = 5. So the cosine similarity is 24 ÷ (5 × 5) = 24 ÷ 25 = 0.96: the vectors point in very similar directions.",
           command="Calculate"),
        EQ("Describe how byte pair encoding builds a vocabulary of tokens.", 4,
           [MP("Start from individual characters", ["character", "letters", "single"]),
            MP("Count pairs of neighbouring symbols across the corpus", ["count", "pair", "adjacent", "neighbour"]),
            MP("Merge the most frequent pair into a new token", ["merge", "most frequent", "most common"]),
            MP("Repeat until the vocabulary reaches its target size", ["repeat", "until", "target", "size"])],
           "Byte pair encoding starts with every word in the training text split into individual characters. It counts how often each pair of neighbouring symbols occurs across the whole corpus, then merges the most frequent pair into a single new symbol, which is added to the vocabulary. This is repeated, so frequent pieces grow into longer tokens and common words become single tokens, until the vocabulary reaches the chosen size.",
           command="Describe"),
    ],
)

L9_2 = Topic(
    slug="sequence-models",
    title="Sequence Models: Predicting the Next Word",
    spec="9.2",
    icon="i-repeat",
    minutes=38,
    exam_title=NEA,
    blurb="What a language model is, from simple n-gram counts to recurrent neural networks that carry a memory from word to word, why they forget, how LSTMs fixed that, and the bottleneck in sequence-to-sequence translation that led to attention.",
    fact="Claude Shannon generated surprisingly readable fake English in 1948 by choosing each word based on the word before it, using statistics he counted by hand from books. It was the first language model.",
    sections=[
        Section("What a language model does", """
A **language model** assigns probabilities to text. Its core job is to answer: given the words so far, how likely is each possible next token?

!diagram ai-next-token

To **generate** text, a model repeats one simple loop:

1. Predict the probability of every possible next token.
2. Choose one, usually by sampling from those probabilities.
3. Add it to the text, and go back to step 1.

Generating one token at a time, each time feeding the output back in as input, is called **autoregressive** generation. Every chatbot works this way: an essay is hundreds of next-token predictions in a row.
"""),
        Section("N-gram models: counting what comes next", """
The simplest language model just counts. A **bigram** model estimates the chance of each word from the word before it:

!info Bigram probability :: P(next word | previous word) = count(previous, next) ÷ count(previous)

In the sentence set "the cat sat on the mat . the dog sat on the log . the cat saw the dog . the dog saw the cat on the mat .", the word "the" appears 9 times before another word:

| After "the" | Count | Probability |
| cat | 3 | 0.33 |
| dog | 3 | 0.33 |
| mat | 2 | 0.22 |
| log | 1 | 0.11 |

An **n-gram** model looks at the previous n − 1 words. Longer contexts predict better but become hopelessly **sparse**: most five-word sequences never appear in any training text at all, so the counts are zero. Smoothing tricks help, but n-gram models can never use more than a few words of context.
"""),
        Section("Perplexity: how surprised is the model?", """
Language models are compared by **perplexity**, which measures how surprised a model is by real text:

!info Perplexity :: perplexity = e to the power of the average cross-entropy loss per token

A perplexity of 20 means the model is, on average, as uncertain as if it were choosing uniformly among 20 equally likely words. Lower is better. On a standard benchmark of news text, the best n-gram models scored perplexities well over 100; neural language models brought that down to the teens and below.
"""),
        Section("Recurrent neural networks", """
A **recurrent neural network (RNN)** reads a sequence one token at a time and carries a **hidden state**, a vector that acts as its memory of everything so far.

!info The RNN update :: new hidden state = tanh(W × old hidden state + U × current input + b)

!diagram ai-rnn-unrolled

The same weights W and U are used at every step, so an RNN can handle sequences of any length. Drawn "unrolled", it looks like a very deep network with one layer per word, and it is trained with backpropagation through that unrolled graph, called **backpropagation through time**.

### Why plain RNNs forget

The gradient from a word 50 steps back passes through 50 multiplications by W and 50 tanh slopes. Just as in deep networks (Level 6), it usually vanishes, so a plain RNN struggles to connect "The keys to the cabinet, which I left in the kitchen last week, ___" back to "keys" when choosing between "is" and "are".
"""),
        Section("LSTMs: learning what to remember", """
The **long short-term memory** network (LSTM), invented by Sepp Hochreiter and Jürgen Schmidhuber in 1997, adds a separate **cell state**, a memory line running along the sequence that information can travel on almost unchanged, plus three **gates** that learn what to do with it:

!diagram ai-lstm-cell

| Gate | Question it answers |
| **Forget gate** | Which parts of the memory should be erased? |
| **Input gate** | Which new information should be written in? |
| **Output gate** | Which parts of the memory should be passed on now? |

Each gate is a sigmoid layer outputting values between 0 (block) and 1 (let through), multiplied with the information it controls. Because the cell state is updated by addition rather than repeated multiplication, gradients survive over hundreds of steps. The simpler **GRU** (2014) merges some of the gates and works about as well.

LSTMs powered the 2016 version of Google Translate, speech recognition in phones and much more, until transformers replaced them.
"""),
        Section("Sequence to sequence, and the bottleneck", """
For translation, a **sequence-to-sequence** model (2014) uses two RNNs:

- an **encoder** reads the whole source sentence and squeezes it into its final hidden state, one fixed-size vector;
- a **decoder** generates the translation word by word, starting from that vector.

!diagram ai-seq2seq

The weakness is obvious from the picture: the meaning of the entire sentence, however long, must pass through **one vector**, the **bottleneck**. Translation quality fell sharply for long sentences.

In 2014 Dzmitry Bahdanau, Kyunghyun Cho and Yoshua Bengio let the decoder **look back** at every encoder state, weighting them by relevance at each step. They called it **attention**. Three years later, a team at Google asked what would happen if you kept the attention and threw the recurrence away. That is Level 10.
"""),
        Section("Hands-on: language models from scratch", """
### A bigram model that writes

```python
import random
from collections import Counter

text = ("the cat sat on the mat . the dog sat on the log . the cat saw the dog . "
        "the dog saw the cat on the mat .").split()
pairs = Counter(zip(text, text[1:]))
starts = Counter(text[:-1])

def next_word_probs(word):
    return {b: c / starts[word] for (a, b), c in pairs.items() if a == word}

print("after 'the':", {w: round(p, 2) for w, p in next_word_probs("the").items()})
print("after 'sat':", next_word_probs("sat"))

random.seed(3)
word, sentence = "the", ["the"]
for _ in range(14):
    probs = next_word_probs(word)
    word = random.choices(list(probs), weights=list(probs.values()))[0]
    sentence.append(word)
print("generated:", " ".join(sentence))
```

Every pair of neighbouring words is plausible, yet the whole makes little sense, because a bigram model only ever sees one word back.

### Perplexity

```python
import math
from collections import Counter

train = ("the cat sat on the mat . the dog sat on the log . the cat saw the dog . "
         "the dog saw the cat on the mat .").split()
vocab = set(train)
pairs = Counter(zip(train, train[1:]))
starts = Counter(train[:-1])

def prob(prev, word):
    # add-one smoothing, so unseen pairs are unlikely but not impossible
    return (pairs[(prev, word)] + 1) / (starts[prev] + len(vocab))

def perplexity(sentence):
    words = sentence.split()
    loss = -sum(math.log(prob(a, b)) for a, b in zip(words, words[1:])) / (len(words) - 1)
    return math.exp(loss)

for s in ["the cat sat on the mat", "the dog sat on the log", "mat the on sat cat the"]:
    print(f"{s:24} perplexity {perplexity(s):5.2f}")
```

### A recurrent memory

This one-number RNN state remembers that it saw a "1", and that memory fades with every step, which is the forgetting problem in miniature.

```python
import math

w_hidden, w_input = 0.7, 1.5
h = 0.0
sequence = [1, 0, 0, 0, 0, 0, 1, 0, 0]
for t, x in enumerate(sequence):
    h = math.tanh(w_hidden * h + w_input * x)
    print(f"step {t}: input {x}  hidden state {h:.3f} " + "#" * int(h * 30))
```

### Try this

1. Train the bigram model on a paragraph of your own and generate from it.
2. Change w_hidden to 0.95 and then 0.3. How long does the memory last now?
"""),
        Section("Level check", """
+ Explain what a language model predicts and how autoregressive generation works
+ Calculate bigram probabilities from counts
+ Explain what perplexity measures and whether lower or higher is better
+ Describe how an RNN carries a hidden state, and why plain RNNs forget
+ Describe the three gates of an LSTM and why its cell state helps
+ Explain the bottleneck in sequence-to-sequence models and how attention began
"""),
    ],
    keyterms=[
        ("Language model", "A model that assigns probabilities to text, usually by predicting the next token."),
        ("Autoregressive generation", "Producing text one token at a time, feeding each output back in as input."),
        ("N-gram", "A sequence of n words; an n-gram model predicts a word from the n − 1 before it."),
        ("Sparsity", "Most possible word sequences never appear in training data, so their counts are zero."),
        ("Perplexity", "e to the power of the average cross-entropy per token: how many choices the model is effectively unsure between."),
        ("Recurrent neural network (RNN)", "A network that processes a sequence step by step, carrying a hidden state forward."),
        ("Hidden state", "The vector an RNN passes from step to step as its memory of the sequence so far."),
        ("Backpropagation through time", "Training an RNN by backpropagating through its unrolled steps."),
        ("LSTM", "Long short-term memory: an RNN with a cell state and gates that learn what to forget, store and output."),
        ("Sequence to sequence", "An encoder network that reads an input sequence and a decoder that generates an output sequence."),
        ("Bottleneck", "Forcing all of a sequence's information through one fixed-size vector."),
    ],
    mistakes=[
        "Thinking a language model looks up answers. It predicts likely next tokens, one at a time.",
        "Believing higher perplexity is better. Lower means the model is less surprised by real text.",
        "Assuming an RNN uses different weights at each step. The same weights are reused at every step.",
        "Thinking LSTMs have no limit to their memory. They remember far longer than plain RNNs, but still struggle with very long texts.",
        "Forgetting that a bigram model ignores everything except the previous word.",
    ],
    grade="""
### Teacher forcing and exposure bias

When training a sequence model, the input at each step is the **real** previous token from the training text, not the model's own guess. This is called **teacher forcing**, and it makes training fast and parallel. But at generation time the model must eat its own outputs, including its mistakes, which it never practised: a mismatch called **exposure bias**. A single odd word can push the model into territory unlike anything it trained on, which is one reason long generations can drift.

### Why RNNs were slow to train

An RNN must compute step 2 after step 1, step 3 after step 2, and so on, so a 1,000-token sequence takes 1,000 sequential steps that cannot run in parallel, leaving most of a GPU idle. The transformer's attention compares all positions at once, turning a sequence into one big matrix multiplication. That parallelism, more than any other single factor, is why transformers could be trained on vastly more data and replaced RNNs almost everywhere after 2017.
""",
    quiz=[
        Q("What does a language model predict?",
          ["The probability of each possible next token", "The meaning of each word in a dictionary",
           "The grammar rules of the language", "The exact sentence a person will say next"], 0,
          "Generation repeats that prediction, one token at a time."),
        Q("What is autoregressive generation?",
          ["Producing one token at a time and feeding each one back in",
           "Generating the whole text in a single step",
           "Correcting the text after it has been written",
           "Translating text back into its original language"], 0,
          "Each new token is added to the input for predicting the next."),
        Q("'the' appears 10 times before another word, followed by 'cat' 4 times. What is P(cat | the) in a bigram model?",
          ["0.4", "4", "0.1", "0.04"], 0,
          "count(the, cat) ÷ count(the) = 4 ÷ 10."),
        Q("Why can n-gram models not use long contexts?",
          ["Most long word sequences never appear, so the counts are zero",
           "Computers cannot store sequences longer than three words",
           "Long contexts always make the predictions less accurate",
           "Words further back have no effect on the next word"], 0,
          "This sparsity problem is what neural language models overcame."),
        Q("Model A has perplexity 12 on a test text and model B has 45. Which is better?",
          ["Model A", "Model B", "They are equal", "It cannot be told"], 0,
          "Lower perplexity means the model is less surprised by real text."),
        Q("What does an RNN carry from one step to the next?",
          ["A hidden state vector that acts as its memory", "A copy of the whole dataset",
           "A new set of weights for each step", "The final answer"], 0,
          "The same weights are reused at every step; the hidden state changes."),
        Q("Why do plain RNNs struggle with long sentences?",
          ["Gradients vanish over many steps, so early words are forgotten",
           "They cannot read more than ten words at a time",
           "They use different weights for every word in the text",
           "They have no way to output more than one word"], 0,
          "The gradient passes through one multiplication per step and shrinks."),
        Q("What does the forget gate in an LSTM do?",
          ["Decides which parts of the cell state to erase", "Deletes training examples",
           "Resets the model after each sentence", "Chooses the next word"], 0,
          "The input gate decides what to write and the output gate what to pass on."),
        Q("What was the bottleneck in early sequence-to-sequence translation?",
          ["The whole source sentence had to fit into one fixed-size vector",
           "The decoder could only produce one word per sentence",
           "The vocabulary held fewer than one hundred words",
           "The encoder could not read punctuation marks"], 0,
          "Long sentences lost information, which attention fixed by letting the decoder look back."),
        Q("Who first generated text with word statistics, in 1948?",
          ["Claude Shannon", "Alan Turing", "John McCarthy", "Geoffrey Hinton"], 0,
          "His paper founding information theory included the first n-gram style language model."),
    ],
    exam=[
        EQ("Explain how a language model generates a paragraph of text.", 4,
           [MP("It predicts a probability for every possible next token", ["probabilit", "next token", "next word", "predict"]),
            MP("It chooses / samples one token", ["choose", "sample", "pick", "select"]),
            MP("The chosen token is added to the input / context", ["add", "append", "feed back", "input"]),
            MP("Repeated one token at a time until finished: autoregressive", ["repeat", "one at a time", "autoregressive", "loop", "until"])],
           "Given the text so far, the language model predicts a probability for every token in its vocabulary being the next one. It then chooses one token, usually by sampling from those probabilities. The chosen token is appended to the text, and the longer text becomes the input for the next prediction. Repeating this loop one token at a time, which is called autoregressive generation, builds up the whole paragraph.",
           command="Explain"),
        EQ("Compare a bigram model with a recurrent neural network as language models.", 4,
           [MP("A bigram model counts pairs of words / uses only the previous word", ["count", "previous word", "one word", "pair"]),
            MP("It suffers from sparsity / cannot use long context", ["sparse", "sparsity", "unseen", "long context", "zero"]),
            MP("An RNN carries a hidden state summarising all previous words", ["hidden state", "memory", "all previous", "whole sequence"]),
            MP("RNNs generalise through learned weights but forget over long sequences / vanishing gradients", ["vanish", "forget", "long", "learned", "generalis"])],
           "A bigram model simply counts how often each word follows each other word, so it predicts the next word from only the previous one, and it cannot handle combinations it never saw because their counts are zero. A recurrent neural network instead reads the sequence one token at a time and carries a hidden state vector that summarises everything so far, so in principle it can use the whole context, and its learned weights let it generalise to new combinations. However, plain RNNs suffer from vanishing gradients, so in practice they forget words more than a few dozen steps back, which LSTMs improved.",
           command="Compare"),
        EQ("Explain the bottleneck problem in sequence-to-sequence models and how attention addressed it.", 4,
           [MP("The encoder compresses the whole input into one fixed-size vector", ["one vector", "single vector", "fixed-size", "fixed size", "final hidden state"]),
            MP("Information is lost for long sentences", ["long", "lost", "worse", "information"]),
            MP("Attention lets the decoder look at all encoder states", ["look", "all", "every", "encoder states", "back"]),
            MP("Weighted by how relevant each is at each step", ["weight", "relevant", "relevance", "focus"])],
           "In a sequence-to-sequence model the encoder reads the whole source sentence and squeezes it into its final hidden state, a single fixed-size vector, which is all the decoder receives. However long the sentence, its meaning must pass through that one vector, so information is lost and translation quality falls for long sentences. Attention removes the bottleneck by letting the decoder look back at every one of the encoder's hidden states at each step, weighting them by how relevant each is to the word being produced, so it can focus on the right part of the source.",
           command="Explain"),
    ],
)

TOPICS = [L9_1, L9_2]
