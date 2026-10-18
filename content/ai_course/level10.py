"""Level 10: Attention and Transformers."""
from mskbuild.models import Topic, Section, Q, EQ, MP

NEA = "Check you could explain this"

L10_1 = Topic(
    slug="attention",
    title="Attention: Learning Where to Look",
    spec="10.1",
    icon="i-target",
    minutes=40,
    exam_title=NEA,
    blurb="How attention lets every token look at every other token: queries, keys and values, scaled dot-product attention worked through by hand, the attention matrix, causal masks, cross-attention and multi-head attention.",
    fact="In a recurrent network, information from the first word of a 1,000-word text has to survive 999 steps to reach the last word. With attention it takes one step, however far apart the two words are.",
    sections=[
        Section("Why context changes meaning", """
Read these two sentences:

- The animal didn't cross the street because **it** was too tired.
- The animal didn't cross the street because **it** was too wide.

In the first, "it" is the animal. In the second, it is the street. One word changed, five words after "it", and the meaning of "it" flipped.

An embedding from Level 9 gives "it" the same vector in both sentences. To understand language, each token's vector has to be updated with information from the other tokens that matter to it. **Attention** does exactly that: every token looks at every other token, decides how relevant each one is, and takes in a weighted mix of their information.

!diagram ai-attention-lines

An RNN passes information along one step at a time, so distant words fade. Attention connects any two tokens directly, however far apart they are.
"""),
        Section("Queries, keys and values", """
Attention borrows its vocabulary from searching a library:

| Part | In a library | In attention |
| **Query** | What you type into the search box | What this token is looking for |
| **Key** | The label on each book's spine | What each token offers, to be matched against queries |
| **Value** | What is inside the book | The information each token passes on |

Each token's embedding x is multiplied by three learned weight matrices to make three new vectors:

!info Three projections :: q = x × W~Q~,  k = x × W~K~,  v = x × W~V~

!diagram ai-qkv

The same three matrices are used for every token. Training adjusts them so that a token's query lines up with the keys of the tokens it needs: a pronoun's query might come to match the keys of nouns, and a verb's query might match its subject.
"""),
        Section("Scaled dot-product attention, step by step", """
For one token, attention takes four steps:

1. **Score**: take the dot product of its query with every key. Vectors pointing the same way give large scores.
2. **Scale**: divide every score by √d~k~, the square root of the length of the keys.
3. **Softmax**: turn the scores into weights between 0 and 1 that add up to 1.
4. **Blend**: add up the value vectors, each multiplied by its weight.

!diagram ai-attention-steps

Here is the query of "it", q = [2, 1], against four keys. The keys have 2 numbers, so the scores are divided by √2 ≈ 1.41:

| Token | Key | q · k | ÷ √2 | e^x^ | Weight |
| animal | [2, 1] | 5 | 3.54 | 34.31 | **0.735** |
| cross | [0, 1] | 1 | 0.71 | 2.03 | 0.043 |
| street | [1, −1] | 1 | 0.71 | 2.03 | 0.043 |
| it | [1, 1] | 3 | 2.12 | 8.34 | 0.179 |

Each weight is its e^x^ divided by the column total, 46.71, so the weights add up to 1. If the values are animal [4, 0], cross [2, 2], street [0, 4] and it [1, 1], the output is

0.735 × [4, 0] + 0.043 × [2, 2] + 0.043 × [0, 4] + 0.179 × [1, 1] = **[3.20, 0.44]**

The new vector for "it" is now mostly made of "animal".

!key Why divide by √d~k~? :: Dot products grow with the length of the vectors. For two random vectors of 64 numbers, the dot product is typically about 8 times (√64) larger than for vectors of one number. Big scores push softmax to give almost all the weight to one token, where its gradient is almost zero and learning stalls. Dividing by √d~k~ keeps the scores in a range where softmax still learns.
"""),
        Section("Every token at once: the attention matrix", """
In **self-attention** every token does this at the same time. Stack all the queries as the rows of a matrix Q, the keys as K and the values as V, and the whole calculation is two matrix multiplications and a softmax:

!info Scaled dot-product attention :: Attention(Q, K, V) = softmax(Q × K^T^ ÷ √d~k~) × V

Here K^T^ is K **transposed**, its rows turned into columns, so that Q × K^T^ holds the dot product of every query with every key. After the softmax this is the **attention matrix**: one row per token, showing how much it attends to every token. Every row adds up to 1.

!diagram ai-attention-heatmap

Because it is all matrix multiplication, a GPU computes attention for every token in parallel. That is the speed advantage over an RNN, which must read one token after another.

Try it yourself: drag the query and the keys, and watch the scores, the softmax and the blended value change.

!tool attention-lab
"""),
        Section("Masking: no peeking at the future", """
A model that generates text predicts each token from the tokens before it. In training it is shown whole sentences at once, so something must stop each token attending to the tokens after it, or it could simply copy the answer it is meant to predict.

The fix is a **causal mask**. Before the softmax, every score where the key comes after the query is set to minus infinity. Since e to the power of minus infinity is 0, those weights become exactly 0, and the remaining weights in each row still add up to 1.

!diagram ai-causal-mask

Transformers use attention in three ways:

| Kind | Queries from | Keys and values from | Used for |
| **Self-attention** | The sequence | The same sequence | Understanding a whole text at once |
| **Masked self-attention** | The sequence | Only the same and earlier positions | Generating text one token at a time |
| **Cross-attention** | The text being written | The input text | Translation: looking back at the source sentence |

Cross-attention is the 2014 idea from Level 9: while writing each word, the decoder looks back at the whole source sentence.
"""),
        Section("Multi-head attention", """
One attention calculation gives each token one weighted mix. But a word has many relationships at once: "it" needs the noun it refers to, a verb needs its subject, and every word benefits from its neighbours. **Multi-head attention** runs several attention calculations, called **heads**, side by side, each with its own W~Q~, W~K~ and W~V~.

!diagram ai-multi-head

1. Each of the h heads projects the tokens down to d~model~ ÷ h numbers and computes attention on its own.
2. The h outputs are joined end to end, **concatenated**, back to d~model~ numbers per token.
3. A final matrix, W~O~, mixes what the heads found.

The original transformer used 8 heads of 64 numbers, so d~model~ = 512. Because each head works on fewer numbers, 8 heads cost about the same as one big one.

Researchers who look inside trained models find heads with recognisable jobs: heads that attend to the previous token, heads that link a pronoun to its noun, and **induction heads**, which spot that a pattern appeared earlier in the text and predict that it will repeat.
"""),
        Section("Hands-on: attention from scratch", """
### One query, four keys

This is the worked example from the table above, in code. Check every number against the table.

```python
import math

def softmax(xs):
    m = max(xs)                      # subtract the largest for numerical safety
    exps = [math.exp(x - m) for x in xs]
    total = sum(exps)
    return [e / total for e in exps]

words  = ["animal", "cross", "street", "it"]
keys   = [[2, 1], [0, 1], [1, -1], [1, 1]]
values = [[4, 0], [2, 2], [0, 4], [1, 1]]
query  = [2, 1]                      # the query of "it"

d_k = len(query)
scores = [sum(q * k for q, k in zip(query, key)) / math.sqrt(d_k) for key in keys]
weights = softmax(scores)
output = [sum(w * v[i] for w, v in zip(weights, values)) for i in range(2)]

for word, s, w in zip(words, scores, weights):
    print(f"{word:7} score {s:5.2f}  weight {w:.3f}  " + "#" * round(w * 40))
print("weights add up to", round(sum(weights), 6))
print("new vector for 'it':", [round(x, 2) for x in output])
```

### Self-attention with matrices, with and without a mask

Every token gets a query, a key and a value from the same three matrices, and the whole attention matrix comes out at once. The weights here are random, so the pattern means nothing yet: training is what gives it meaning.

```python
import math, random

def matmul(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def transpose(A):
    return [list(col) for col in zip(*A)]

def softmax(xs):
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    return [e / sum(exps) for e in exps]

def self_attention(X, W_Q, W_K, W_V, causal=False):
    Q, K, V = matmul(X, W_Q), matmul(X, W_K), matmul(X, W_V)
    d_k = len(Q[0])
    scores = matmul(Q, transpose(K))
    for i in range(len(X)):
        for j in range(len(X)):
            scores[i][j] /= math.sqrt(d_k)
            if causal and j > i:
                scores[i][j] = float("-inf")    # e to the power of -inf is 0
    A = [softmax(row) for row in scores]
    return A, matmul(A, V)

random.seed(4)
tokens = ["the", "cat", "sat", "down"]
d_model, d_k = 4, 3
X = [[random.uniform(-1, 1) for _ in range(d_model)] for _ in tokens]
W_Q, W_K, W_V = ([[random.uniform(-1, 1) for _ in range(d_k)] for _ in range(d_model)]
                 for _ in range(3))

for causal in (False, True):
    A, out = self_attention(X, W_Q, W_K, W_V, causal)
    print("causal mask:", causal)
    print("        " + "".join(f"{t:>7}" for t in tokens))
    for t, row in zip(tokens, A):
        print(f"{t:>7} " + "".join(f"{w:7.2f}" for w in row) + f"   sum {sum(row):.2f}")
    print("output:", len(out), "tokens x", len(out[0]), "numbers")
    print()
```

With the mask, everything above the diagonal is 0, and "the" can only attend to itself. The last row is the same in both runs, because the last token may see everything either way.

### Several heads

```python
import math, random

def matmul(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def softmax(xs):
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    return [e / sum(exps) for e in exps]

def head(X, d_head, seed):
    rnd = random.Random(seed)          # every head has its own weights
    W = [[[rnd.uniform(-1.5, 1.5) for _ in range(d_head)] for _ in X[0]] for _ in range(3)]
    Q, K, V = (matmul(X, w) for w in W)
    A = [softmax([sum(q * k for q, k in zip(Q[i], K[j])) / math.sqrt(d_head)
                  for j in range(len(X))]) for i in range(len(X))]
    return A, matmul(A, V)

random.seed(0)
tokens = ["she", "saw", "the", "bird"]
d_model, h = 6, 3
X = [[random.uniform(-1, 1) for _ in range(d_model)] for _ in tokens]
outputs = []
for n in range(h):
    A, out = head(X, d_model // h, seed=10 + n)
    outputs.append(out)
    focus = [tokens[max(range(len(tokens)), key=lambda j: A[i][j])] for i in range(len(tokens))]
    print(f"head {n + 1}: each token attends most to", dict(zip(tokens, focus)))
concat = [sum((o[i] for o in outputs), []) for i in range(len(tokens))]
print("each head gives", d_model // h, "numbers; joined:", len(concat[0]), "numbers per token")
```

### Try this

1. In the first program, change the query to [6, 3]. The scores triple. What happens to the weight on "animal", and why does that show the reason for scaling?
2. Change the key of "street" to [2, 1] so it matches "animal". How do the weights and the output change?
3. In the second program, count the zeros in the masked matrix. How many would there be for 10 tokens?
"""),
        Section("Level check", """
+ Explain why a word's meaning depends on its context, and how attention uses context
+ Describe the roles of queries, keys and values, and how each is made
+ Calculate attention weights from scores using softmax, and the blended output
+ Explain why scores are divided by √d~k~
+ Explain what a causal mask does and why generation needs it
+ Distinguish self-attention, masked self-attention and cross-attention
+ Describe how multi-head attention splits, computes and recombines
"""),
    ],
    keyterms=[
        ("Attention", "A way for each token to build its new vector from a weighted mix of the information in other tokens."),
        ("Query", "The vector a token uses to search the other tokens: what it is looking for."),
        ("Key", "The vector each token is matched against queries with: what it offers."),
        ("Value", "The information a token passes on when other tokens attend to it."),
        ("Scaled dot-product attention", "softmax(Q × K^T^ ÷ √d~k~) × V: dot-product scores, scaled, turned into weights, used to blend the values."),
        ("Attention weights", "The softmax outputs: for each token, numbers between 0 and 1 that add up to 1."),
        ("Self-attention", "Attention in which the queries, keys and values all come from the same sequence."),
        ("Cross-attention", "Attention in which the queries come from one sequence and the keys and values from another."),
        ("Causal mask", "Setting the scores for later positions to minus infinity, so no token can attend to the future."),
        ("Multi-head attention", "Several attention heads with their own weights, run side by side and combined."),
        ("Head", "One attention calculation inside multi-head attention, with its own W~Q~, W~K~ and W~V~."),
    ],
    mistakes=[
        "Thinking someone sets the attention weights by hand. W~Q~, W~K~ and W~V~ are learned, so the model learns what to attend to.",
        "Forgetting the softmax. Raw dot products are scores, not weights, until softmax makes them positive and add up to 1.",
        "Mixing up keys and values. Keys decide how much attention a token gets; values are what it passes on.",
        "Thinking a causal mask deletes tokens from the input. They are still there; only attention to later positions is blocked.",
        "Assuming more heads means more parameters. Each head works on d~model~ ÷ h numbers, so the total stays about the same.",
    ],
    grade="""
### Attention as a soft dictionary

A Python dictionary does hard lookup: a key matches exactly or not at all, and you get one value back. Attention is a **soft** lookup: every key matches a little, and you get back a blend of all the values, weighted by how well each key matched. Because the blend is smooth, gradient descent can adjust the queries and keys, so the network learns what to look up.

### The cost of attention

Every token attends to every token, so n tokens need an n × n attention matrix: double the context and the work quadruples. That quadratic cost long limited context windows to a few thousand tokens. **FlashAttention** (2022) computes exactly the same result in tiles that fit the GPU's fastest memory, and **sliding-window** and **sparse** attention let each token attend to only some of the others. Together with similar engineering, they are how modern models handle contexts of hundreds of thousands of tokens.
""",
    quiz=[
        Q("In attention, what does a token's query represent?",
          ["What the token is looking for in other tokens", "The information the token passes on",
           "The position of the token in the sentence", "The token's ID number in the vocabulary"], 0,
          "Keys are what tokens offer to be matched, and values are what they pass on."),
        Q("How is the score between a query and a key calculated?",
          ["Their dot product", "Their difference", "The larger of the two", "Their average"], 0,
          "Vectors that point the same way give a large dot product, so a high score."),
        Q("Why are the scores divided by √d~k~?",
          ["To stop large dot products pushing softmax to extremes", "To make every score a whole number",
           "To let the model run on more GPUs", "To remove the need for a softmax"], 0,
          "Big scores make softmax put nearly all the weight on one token, where the gradients almost vanish."),
        Q("After the softmax, what is true of one token's attention weights?",
          ["Each is between 0 and 1, and they add up to 1", "Each is a whole number between 1 and 10",
           "They add up to the number of tokens", "They can be any positive or negative number"], 0,
          "Softmax makes every weight positive and divides by the total."),
        Q("Three scaled scores are 2, 0 and 0. Roughly what weight does softmax give the first token?",
          ["0.79", "0.67", "1.00", "0.33"], 0,
          "e^2^ ≈ 7.39 and e^0^ = 1, so the weight is 7.39 ÷ (7.39 + 1 + 1) ≈ 0.79."),
        Q("What is the output of attention for one token?",
          ["A weighted sum of all the value vectors", "The key with the highest score",
           "The average of all the queries", "The token's original embedding"], 0,
          "Each value is multiplied by its weight, and the results are added."),
        Q("What does a causal mask do?",
          ["Stops each token attending to tokens that come after it", "Removes rare words from the vocabulary",
           "Hides the labels from the model in testing", "Blocks the first token from attending to anything"], 0,
          "Scores for later positions become minus infinity, so their weights are 0."),
        Q("In cross-attention in a translation model, where do the keys and values come from?",
          ["The encoded source sentence", "The words the decoder has written so far",
           "A separate dictionary of translations", "Random noise added for robustness"], 0,
          "The queries come from the decoder, so each output word can look back at the source."),
        Q("Why does multi-head attention use several heads?",
          ["Each head can learn a different kind of relationship", "Each head handles a different sentence",
           "Extra heads let the model skip the softmax", "One head is needed for each word in the vocabulary"], 0,
          "One head might track the previous word while another links pronouns to nouns."),
        Q("A transformer has d~model~ = 512 and 8 heads. How many numbers does each head's query have?",
          ["64", "512", "4,096", "8"], 0,
          "512 ÷ 8 = 64, and the 8 outputs are concatenated back to 512."),
    ],
    exam=[
        EQ("Explain how scaled dot-product attention calculates the new vector for one token.", 4,
           [MP("The token's query is compared with every key by a dot product, giving a score", ["dot product", "score", "query", "key"]),
            MP("The scores are divided by the square root of d_k", ["square root", "√", "scale", "divide"]),
            MP("Softmax turns the scores into weights between 0 and 1 that add up to 1", ["softmax", "add up to 1", "sum to 1", "weights"]),
            MP("The output is the weighted sum of the value vectors", ["weighted sum", "values", "blend", "multiplied by"])],
           "First the token's query vector is compared with the key vector of every token by taking dot products, which gives a score for each: the more the vectors point the same way, the higher the score. The scores are divided by the square root of the key length, d_k, so they do not grow too large. Softmax then turns the scores into weights between 0 and 1 that add up to 1. Finally each token's value vector is multiplied by its weight and the results are added, so the new vector is a weighted blend of the values, dominated by the most relevant tokens.",
           command="Explain"),
        EQ("Explain why a transformer that generates text needs a causal mask during training.", 3,
           [MP("In training, the whole sequence is processed at once / in parallel", ["whole", "at once", "parallel", "same time"]),
            MP("Without a mask a token could attend to later tokens, including the one it must predict, and copy it", ["see", "later", "future", "copy", "cheat", "answer"]),
            MP("The mask sets later scores to minus infinity so their weights are 0, matching generation where later tokens do not exist yet", ["minus infinity", "-inf", "zero", "0", "generation", "do not exist"])],
           "During training, a whole sentence is fed in at once so that every position can be trained in parallel. Without a mask, the token at each position could attend to the tokens after it, including the very token it is supposed to predict, so it would learn to copy rather than to predict. The causal mask sets every score for a later position to minus infinity before the softmax, which makes those weights exactly 0, so each token sees only earlier tokens, just as it will when generating, when later tokens do not exist yet.",
           command="Explain"),
        EQ("Describe the roles of the query, key and value vectors in attention.", 3,
           [MP("The query represents what a token is looking for", ["query", "looking for", "search"]),
            MP("Keys are matched against the query to decide how relevant each token is / how much attention it gets", ["key", "match", "relevan", "how much"]),
            MP("Values carry the information that is passed on / blended into the output", ["value", "information", "passed", "blend", "output"]),
            MP("All three are made by multiplying the token's embedding by learned weight matrices", ["learned", "weight matri", "multiplied", "W_Q", "W"])],
           "Each token's embedding is multiplied by three learned weight matrices to make a query, a key and a value. The query represents what the token is looking for. Every token's key is compared with the query, and how well they match decides how much attention that token receives. The values carry the actual information: the output is a blend of the values, weighted by those attention scores.",
           command="Describe"),
    ],
)

L10_2 = Topic(
    slug="transformers",
    title="Transformers: The Architecture Behind Modern AI",
    spec="10.2",
    icon="i-layers",
    minutes=42,
    exam_title=NEA,
    blurb="The 2017 transformer and what followed it: positional encoding, the transformer block with residual connections, layer normalisation and feed-forward layers, the residual stream, counting GPT-2's 124 million parameters, the three families of transformer, and why this one architecture took over AI.",
    fact="The 2017 paper \"Attention Is All You Need\" listed its eight authors with a footnote saying that they had contributed equally and that the order was random. Its title has been borrowed by many later papers, all called something \"Is All You Need\".",
    sections=[
        Section("Attention is all you need", """
In June 2017 eight researchers working at Google published "Attention Is All You Need". Their model, the **transformer**, threw recurrence away completely and built a translator from attention and simple feed-forward layers. It beat the best translation systems of the time while training in a fraction of the time, because every position in a sentence could be processed in parallel.

| Year | Model | What it showed |
| 2017 | Transformer | Attention alone beats recurrent networks at translation |
| 2018 | GPT (OpenAI) and BERT (Google) | Pretrain one transformer on huge amounts of text, then adapt it to many tasks |
| 2019 | GPT-2 | 1.5 billion parameters writing convincing paragraphs |
| 2020 | GPT-3 | 175 billion parameters, learning new tasks from a few examples in the prompt |
| 2020 | Vision Transformer (ViT) | The same architecture classifies images, treating patches as tokens |
| 2021 | AlphaFold 2 | Attention-based networks predict the 3D shapes of proteins |
| 2022 | ChatGPT | A transformer tuned to follow instructions reaches an estimated 100 million users in about two months |

This lesson takes the architecture apart, piece by piece.
"""),
        Section("Giving attention a sense of order", """
Attention compares every token with every other token, but nothing in the calculation knows where a token is. Shuffle the words and every token gets exactly the same weights, so "dog bites man" and "man bites dog" would look identical.

The fix is to add a **positional encoding** to each token's embedding before the first layer. The original transformer used waves: position p gets a vector whose numbers are sines and cosines of p at different frequencies.

!info Sinusoidal positional encoding :: number 2i of the vector for position p is sin(p ÷ 10000^2i/d^), and number 2i + 1 is cos(p ÷ 10000^2i/d^), where d is the length of the vector

!diagram ai-positional-encoding

The first numbers oscillate quickly and the later ones slowly, like the second, minute and hour hands of a clock. Every position gets its own pattern, and nearby positions get similar patterns.

GPT-2 took a simpler route and learned a position vector for each of its 1,024 positions. Many recent models use **rotary position embeddings (RoPE)**, which rotate each query and key by an angle that depends on its position, so the score between two tokens depends on how far apart they are.
"""),
        Section("Inside a transformer block", """
A transformer is a stack of identical **blocks**. Each block has two sublayers, and each sublayer is wrapped in a residual connection and a normalisation step:

!diagram ai-transformer-block

1. **Multi-head self-attention**: the tokens exchange information.
2. **Add and normalise**: add the sublayer's input back onto its output (the residual connection from Level 8's ResNets), then apply **layer normalisation**, which rescales each token's vector to a mean of 0 and a standard deviation of 1.
3. **Feed-forward network**: the same small two-layer network, applied to every token separately. It widens each vector to 4 × d~model~ numbers, applies an activation such as ReLU or GELU, and narrows it back.
4. **Add and normalise** again.

The output has exactly the same shape as the input: one vector of d~model~ numbers for each token. That is what lets blocks stack. GPT-2 small stacks 12 of them, and GPT-3 stacks 96.
"""),
        Section("The residual stream", """
A helpful way to picture a transformer is as a **residual stream**. Each token has a lane, a vector of d~model~ numbers flowing up through the network, and every sublayer reads from the stream and **adds** its result back in.

!diagram ai-residual-stream

- **Attention** is the only place where information moves **between** lanes, from one token to another.
- The **feed-forward** layers work on each lane **on its own**. Research suggests that much of a model's factual knowledge is stored in their weights.

By the top of the stack, the vector in the last token's lane holds everything needed to predict what comes next.
"""),
        Section("From vectors to the next word", """
After the last block, each token's vector is multiplied by an **unembedding** matrix with one column for every token in the vocabulary. That gives a score, called a **logit**, for every possible next token, and softmax turns the logits into probabilities, exactly as in Level 9. Many models reuse the embedding matrix here (**weight tying**), so the same numbers turn tokens into vectors at the bottom and vectors back into tokens at the top.

Here is where every one of GPT-2 small's parameters lives (d~model~ = 768, 12 blocks, 50,257 tokens, 1,024 positions):

| Part | Calculation | Parameters |
| Token embeddings | 50,257 × 768 | 38,597,376 |
| Position embeddings | 1,024 × 768 | 786,432 |
| Attention, per block | 4 × 768^2^ weights + 4 × 768 biases | 2,362,368 |
| Feed-forward, per block | 8 × 768^2^ weights + 5 × 768 biases | 4,722,432 |
| Two layer norms, per block | 4 × 768 | 3,072 |
| All 12 blocks | 12 × 7,087,872 | 85,054,464 |
| Final layer norm | 2 × 768 | 1,536 |
| **Total** | | **124,439,808** |

About two thirds of the parameters are in the blocks, and two thirds of each block is its feed-forward network. Attention moves information around; the feed-forward layers do most of the storing.
"""),
        Section("Three families of transformer", """
The same block is used in three different arrangements:

| Family | Attention | Trained to | Examples | Good at |
| **Encoder-only** | Full: every token sees every token | Fill in hidden (masked) words | BERT (2018) | Understanding: classifying, searching, tagging |
| **Encoder-decoder** | Encoder full; decoder masked, plus cross-attention | Turn one sequence into another | The 2017 transformer, T5 (2019) | Translating, summarising |
| **Decoder-only** | Masked: each token sees only earlier tokens | Predict the next token | The GPT series and most chatbots | Generating text, code and conversation |

!diagram ai-transformer-family

Decoder-only models turned out to be the most general, because almost any task can be written as text in, text out: translation is "Translate into French: …", and classification is "Is this review positive or negative? …".
"""),
        Section("Why transformers won", """
- **Parallel training**: a whole sequence is processed in one pass of matrix multiplications, which GPUs are built for. An RNN has to go one step at a time.
- **Short paths**: any token reaches any other token in one attention step, so long-range connections are easy to learn.
- **They scale**: performance kept improving as models, data and computing power grew, as Level 11 explores.
- **One architecture for everything**: text, images, audio, protein sequences and robot actions can all be turned into sequences of tokens.

The Vision Transformer shows how far the idea stretches. It cuts an image into square patches and treats each patch as a token:

!diagram ai-vit-patches

The weakness is cost. Every token attends to every token, so the attention matrix grows with the **square** of the number of tokens:

!diagram ai-attention-cost
"""),
        Section("Hands-on: a transformer from scratch", """
### Positional encodings

```python
import math

def positional_encoding(pos, d_model):
    pe = []
    for i in range(d_model // 2):
        angle = pos / 10000 ** (2 * i / d_model)
        pe += [math.sin(angle), math.cos(angle)]
    return pe

print("pos  " + " ".join(f"{'d' + str(i):>5}" for i in range(8)))
for pos in range(6):
    print(f"{pos:3}  " + " ".join(f"{v:5.2f}" for v in positional_encoding(pos, 8)))

print()
here = positional_encoding(10, 16)
for gap in [0, 1, 2, 4, 8, 16]:
    there = positional_encoding(10 + gap, 16)
    sim = sum(a * b for a, b in zip(here, there))
    print(f"position 10 against position {10 + gap:2}: dot product {sim:5.2f}")
```

Column d0 changes fast and d6 barely moves, like clock hands. The dot product falls as positions get further apart, which is how attention can tell near from far.

### A stack of transformer blocks

Each block below is the real recipe: layer norm, masked self-attention, add; layer norm, feed-forward, add. Each block has its own random weights.

```python
import math, random

random.seed(7)
def rand_matrix(rows, cols, scale=0.5):
    return [[random.uniform(-scale, scale) for _ in range(cols)] for _ in range(rows)]
def matmul(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]
def add(A, B):
    return [[a + b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]
def softmax(xs):
    m = max(xs)
    e = [math.exp(x - m) for x in xs]
    return [v / sum(e) for v in e]
def layer_norm(X):
    out = []
    for row in X:
        mean = sum(row) / len(row)
        sd = math.sqrt(sum((v - mean) ** 2 for v in row) / len(row) + 1e-5)
        out.append([(v - mean) / sd for v in row])
    return out
def attention(X, W_Q, W_K, W_V, W_O):
    Q, K, V = matmul(X, W_Q), matmul(X, W_K), matmul(X, W_V)
    d = len(Q[0])
    A = [softmax([sum(q * k for q, k in zip(Q[i], K[j])) / math.sqrt(d) if j <= i else -math.inf
                  for j in range(len(X))]) for i in range(len(X))]
    return matmul(matmul(A, V), W_O)
def feed_forward(X, W1, W2):
    hidden = [[max(0.0, v) for v in row] for row in matmul(X, W1)]   # ReLU
    return matmul(hidden, W2)

d_model, d_ff = 4, 16
def make_block():
    return {"attention": [rand_matrix(d_model, d_model) for _ in range(4)],
            "feed_forward": [rand_matrix(d_model, d_ff), rand_matrix(d_ff, d_model)]}

def block(X, p):
    X = add(X, attention(layer_norm(X), *p["attention"]))        # tokens share information
    X = add(X, feed_forward(layer_norm(X), *p["feed_forward"]))  # each token on its own
    return X

X = rand_matrix(3, d_model, 1.0)        # 3 tokens, 4 numbers each
for n, p in enumerate([make_block() for _ in range(3)], start=1):
    X = block(X, p)
    print(f"after block {n}: {len(X)} tokens x {len(X[0])} numbers, first token",
          [round(v, 2) for v in X[0]])
```

The shape never changes: 3 tokens of 4 numbers go in, and 3 tokens of 4 numbers come out, which is why the blocks can be stacked as deep as you like.

### Counting GPT-2's parameters

```python
def gpt2_parameters(n_layers, d, vocab=50257, context=1024):
    embeddings = vocab * d + context * d
    attention = 4 * d * d + 4 * d          # W_Q, W_K, W_V, W_O and their biases
    feed_forward = 8 * d * d + 5 * d       # d -> 4d -> d, with biases
    norms = 4 * d                          # two layer norms, each a scale and a shift
    return embeddings + n_layers * (attention + feed_forward + norms) + 2 * d

for name, layers, d in [("small", 12, 768), ("medium", 24, 1024),
                        ("large", 36, 1280), ("XL", 48, 1600)]:
    print(f"GPT-2 {name:6} {layers:2} blocks, d = {d:4}: {gpt2_parameters(layers, d):>13,} parameters")
```

These are exactly the sizes of the four GPT-2 models released in 2019.

### Try this

1. Remove the two `add(X, ...)` calls in the block, keeping only the sublayer outputs. Stack 12 blocks instead of 3. What happens to the numbers?
2. GPT-3 has 96 blocks with d = 12,288 and the same 50,257-token vocabulary, with 2,048 positions. Use the function to estimate its size. How close is it to 175 billion?
"""),
        Section("Level check", """
+ Explain why attention needs positional encoding, and describe two ways of adding it
+ Draw and label a transformer block, including the residual connections
+ Explain what layer normalisation and the feed-forward network do
+ Describe the residual stream and which sublayer moves information between tokens
+ Count the parameters of a transformer from its sizes
+ Compare encoder-only, encoder-decoder and decoder-only transformers
+ Explain why transformers replaced RNNs, and the cost of long contexts
"""),
    ],
    keyterms=[
        ("Transformer", "A neural network built from stacked blocks of attention and feed-forward layers, introduced in 2017."),
        ("Positional encoding", "A vector added to each token's embedding that tells the model where the token is."),
        ("Transformer block", "Multi-head attention and a feed-forward network, each with a residual connection and layer normalisation."),
        ("Feed-forward network", "Two linear layers with an activation between them, applied to each token separately."),
        ("Layer normalisation", "Rescaling each token's vector to mean 0 and standard deviation 1, then applying a learned scale and shift."),
        ("Residual stream", "The per-token vectors flowing up through the network, which every sublayer reads from and adds to."),
        ("Logit", "The raw score for one vocabulary token, before softmax turns the scores into probabilities."),
        ("Weight tying", "Reusing the embedding matrix as the unembedding matrix that produces the logits."),
        ("Encoder-only", "A transformer in which every token sees every other, such as BERT, used for understanding tasks."),
        ("Decoder-only", "A transformer with masked attention trained to predict the next token, such as GPT."),
        ("Vision Transformer (ViT)", "A transformer that classifies images by treating patches of pixels as tokens."),
    ],
    mistakes=[
        "Thinking a transformer reads text left to right like an RNN. It processes every position at once; only the mask limits what each position can see.",
        "Forgetting positional information. Without it, attention cannot tell \"dog bites man\" from \"man bites dog\".",
        "Believing every transformer generates text. Encoder-only models such as BERT are built for understanding, not generation.",
        "Thinking the feed-forward layers mix information between tokens. They work on each token on its own; only attention moves information between tokens.",
        "Assuming long contexts are cheap. The attention matrix grows with the square of the number of tokens.",
    ],
    grade="""
### Pre-norm and post-norm

The 2017 transformer normalised **after** each residual addition (post-norm). Deep post-norm stacks are hard to train without carefully warming up the learning rate, so most modern models normalise the **input** of each sublayer instead (pre-norm), as the code above does. That leaves the residual stream itself untouched: a clean path for gradients to travel down, exactly as in a ResNet. Many models also swap layer norm for the simpler **RMSNorm**, and ReLU for **GELU** or **SwiGLU**.

### The KV cache

When generating, a decoder-only model would naively recompute the keys and values of every earlier token at every step. Because of the mask, those never change, so they are stored in a **KV cache** and only the newest token's query, key and value are computed. Each new token becomes cheap, but the cache grows with the context and is a large part of the memory needed to serve a model to many users.

### Mixture of experts

Some large models replace each feed-forward network with many smaller **expert** networks and a **router** that sends each token to just one or two of them. The model can hold far more parameters than it uses on any single token, gaining knowledge without a matching rise in the computation per token.
""",
    quiz=[
        Q("What did the 2017 transformer remove that earlier translation models relied on?",
          ["Recurrence: processing tokens one at a time", "Word embeddings",
           "Training with gradient descent", "The softmax function"], 0,
          "Without recurrence, every position can be processed in parallel."),
        Q("Why does a transformer need positional encoding?",
          ["Attention on its own ignores word order", "To reduce the size of the vocabulary",
           "To make the training data more varied", "To decide which tokens to mask out"], 0,
          "Without it, \"dog bites man\" and \"man bites dog\" would look identical."),
        Q("What does the feed-forward network in a transformer block do?",
          ["Processes each token's vector on its own", "Moves information between tokens",
           "Converts tokens into ID numbers", "Chooses which tokens to mask out"], 0,
          "Only attention moves information between tokens."),
        Q("What does a residual connection do in a transformer block?",
          ["Adds the sublayer's input to its output", "Removes tokens that are not needed",
           "Multiplies the output by the learning rate", "Sends the output back to the first layer"], 0,
          "It keeps a clean path for information and gradients, as in a ResNet."),
        Q("Why must a block's output have the same shape as its input?",
          ["So that blocks can be stacked one on top of another", "So that the vocabulary stays the same size",
           "So that the model uses less memory", "So that softmax can be skipped"], 0,
          "GPT-2 small stacks 12 identical blocks, and GPT-3 stacks 96."),
        Q("Which family of transformer does BERT belong to?",
          ["Encoder-only", "Decoder-only", "Encoder-decoder", "Recurrent"], 0,
          "BERT sees the whole sentence at once and is trained to fill in masked words."),
        Q("Which kind of transformer is trained to predict the next token using masked attention?",
          ["Decoder-only, such as GPT", "Encoder-only, such as BERT",
           "A convolutional network, such as ResNet", "An LSTM, such as early Google Translate"], 0,
          "Its causal mask means each token sees only the tokens before it."),
        Q("How does a Vision Transformer read an image?",
          ["It cuts the image into patches and treats each patch as a token",
           "It reads the pixels one at a time from left to right",
           "It turns the image into a written description first",
           "It looks only at the colour of the centre pixel"], 0,
          "A 224 × 224 image cut into 16 × 16 patches becomes 196 tokens."),
        Q("A context grows from 1,000 to 4,000 tokens. Roughly how many times bigger does the attention matrix get?",
          ["16 times", "4 times", "2 times", "It stays the same size"], 0,
          "The matrix is n × n, so 4 times as many tokens gives 4^2^ = 16 times as many entries."),
        Q("In GPT-2 small, which part holds the most parameters?",
          ["The feed-forward networks in its blocks", "The token embedding table",
           "The attention layers in its blocks", "The final layer normalisation"], 0,
          "12 × 4,722,432 ≈ 56.7 million, against 38.6 million in the token embeddings and 28.3 million in attention."),
    ],
    exam=[
        EQ("Describe the structure of one transformer block.", 4,
           [MP("Multi-head self-attention, in which tokens exchange information", ["attention"]),
            MP("A residual connection adds each sublayer's input to its output", ["residual", "add", "skip"]),
            MP("Layer normalisation rescales each token's vector", ["norm"]),
            MP("A feed-forward network is applied to each token separately", ["feed-forward", "feed forward", "each token", "separately"]),
            MP("The output has the same shape as the input, so blocks can be stacked", ["same shape", "stack", "same size"])],
           "A transformer block has two sublayers. The first is multi-head self-attention, in which every token gathers information from the other tokens. The second is a feed-forward network, two linear layers with an activation between them, applied to each token's vector separately. Each sublayer is wrapped in a residual connection that adds its input to its output, and in layer normalisation, which rescales each token's vector to mean 0 and standard deviation 1. The output has the same shape as the input, one vector per token, so many identical blocks can be stacked.",
           command="Describe"),
        EQ("Explain why transformers replaced recurrent neural networks for language tasks.", 4,
           [MP("Transformers process every token in parallel, using matrix multiplications that suit GPUs", ["parallel", "at once", "GPU", "matrix"]),
            MP("RNNs must process tokens one after another, which is slow to train", ["sequential", "one at a time", "one after another", "slow", "step"]),
            MP("Attention connects any two tokens directly, in one step", ["any two", "directly", "one step", "long-range", "distance"]),
            MP("RNNs forget distant words because of vanishing gradients", ["vanish", "forget", "long sequences"]),
            MP("Transformers keep improving as they are scaled up with more data and computing power", ["scale", "more data", "bigger", "compute"])],
           "An RNN must read a sequence one token after another, because each hidden state depends on the one before, so training cannot be spread across a GPU and is slow. A transformer processes every token at once with large matrix multiplications, which GPUs do extremely quickly, so it can be trained on far more data. Attention also connects any two tokens directly in a single step, whereas in an RNN information from a distant word has to pass through many steps and gradients vanish, so it is forgotten. Because transformers train efficiently, they could be scaled up, and their performance kept improving with size.",
           command="Explain"),
        EQ("Compare encoder-only and decoder-only transformers.", 3,
           [MP("In an encoder-only model every token attends to every other token / full attention", ["every token", "all tokens", "full", "whole sentence", "both directions"]),
            MP("Encoder-only models such as BERT are trained to fill in masked words and used for understanding tasks such as classification", ["BERT", "masked word", "fill in", "classif", "understand"]),
            MP("Decoder-only models use a causal mask, so each token sees only earlier tokens", ["causal", "mask", "earlier", "previous", "before"]),
            MP("Decoder-only models such as GPT are trained to predict the next token and used for generation", ["GPT", "next token", "generat"])],
           "Both are built from the same transformer blocks. In an encoder-only model such as BERT, every token can attend to every other token, before and after it, and the model is trained by filling in words that have been hidden, so it is suited to understanding tasks such as classifying text or searching. A decoder-only model such as GPT uses a causal mask, so each token sees only the tokens before it, and it is trained to predict the next token, which makes it suited to generating text one token at a time.",
           command="Compare"),
    ],
)

TOPICS = [L10_1, L10_2]
