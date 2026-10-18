"""Level 7: Neural Networks. Layers, the forward pass, and backpropagation."""
from mskbuild.models import Topic, Section, Q, EQ, MP

NEA = "Check you could explain this"

L7_1 = Topic(
    slug="neural-network-layers",
    title="Neural Networks: Layers, Matrices and the Forward Pass",
    spec="7.1",
    icon="i-layers",
    minutes=38,
    exam_title=NEA,
    blurb="How neurons are wired into layers, why a whole layer is one matrix multiplication, a forward pass worked through by hand, how hidden layers reshape space to solve XOR, and how to count a network's parameters.",
    fact="When a phone unlocks with your face, a neural network runs a forward pass of many millions of multiplications in a few hundredths of a second, using a chip built into the phone for exactly that job.",
    sections=[
        Section("From one neuron to a network", """
A **neural network** connects neurons in **layers**. Every neuron in one layer feeds every neuron in the next, which is called a **fully connected** or **dense** layer.

!diagram ai-mlp-anatomy

| Layer | What it holds |
| **Input layer** | The features, such as 784 pixel brightnesses. It does no computing |
| **Hidden layers** | Neurons whose outputs are passed on, never seen directly. They learn useful intermediate features |
| **Output layer** | One neuron per thing to predict: one number for regression, one probability per class for classification |

A network with at least one hidden layer is often called a **multi-layer perceptron (MLP)**. "Deep" learning simply means many hidden layers. The values computed by the hidden neurons for an input are called its **activations**.
"""),
        Section("A layer is a matrix multiplication", """
Each neuron in a layer computes a weighted sum of the same inputs, with its own weights. Stack each neuron's weights as a row of a **weight matrix** W, and the whole layer is one calculation:

!info A dense layer :: output = f(W x + b), where W has one row per neuron and one column per input

!diagram ai-matmul

To multiply a matrix by a vector, take the dot product of each **row** with the vector. Each row gives one neuron's weighted sum. A layer with 3 inputs and 4 neurons has a 4 × 3 weight matrix and a bias vector of 4 numbers.

!key Why this matters for hardware :: Writing a layer as one matrix multiplication is not just tidy notation. Graphics processors (GPUs) and specialised AI chips are built to multiply huge matrices quickly, thousands of multiplications at the same time. That is why the same chips that render video games train neural networks.

### Batches

Feed a **batch** of examples at once by stacking them as the rows of a matrix X. The layer becomes X Wᵀ + b, and one matrix multiplication handles every example in the batch together.
"""),
        Section("The forward pass, worked through", """
The **forward pass** carries an input through the network, layer by layer, to the output. Here is a tiny network that solves XOR with ReLU hidden neurons:

| Neuron | Calculation |
| Hidden h₁ | ReLU(x₁ + x₂) |
| Hidden h₂ | ReLU(x₁ + x₂ − 1) |
| Output | h₁ − 2h₂ |

| x₁ | x₂ | h₁ | h₂ | Output | XOR |
| 0 | 0 | 0 | 0 | 0 − 0 = **0** | 0 |
| 0 | 1 | 1 | 0 | 1 − 0 = **1** | 1 |
| 1 | 0 | 1 | 0 | 1 − 0 = **1** | 1 |
| 1 | 1 | 2 | 1 | 2 − 2 = **0** | 0 |

Four inputs, four correct answers: what a single neuron could never do.
"""),
        Section("What hidden layers really do", """
The hidden layer **transforms the space**. It moves each input point to a new position, given by the hidden neurons' outputs, where the problem becomes easy.

!diagram ai-xor-solved

In the input space the XOR classes sit on opposite diagonals and no line separates them. In the hidden space (h₁, h₂), the points (0, 1) and (1, 0) land on the same spot, and a single straight line now divides the classes. The output neuron only has to draw that line.

This is the deep idea of deep learning. Each layer re-represents the data so that the next layer's job is simpler. In an image network, early layers turn pixels into edges, later layers turn edges into textures and shapes, and the last layers turn shapes into "cat" or "aeroplane". Nobody programs these features: training discovers them.

### Width and depth

The **universal approximation theorem** (Level 6) says one wide hidden layer is enough in principle. In practice, **depth** is far more efficient: each layer can fold and reuse what the previous one built, so a deep network can represent with thousands of neurons what a shallow one would need millions for.
"""),
        Section("Counting parameters", """
A dense layer from n inputs to m neurons has:

!info Parameters in a dense layer :: n × m weights + m biases

A classic network for handwritten digits, with 784 inputs, hidden layers of 128 and 64 neurons and 10 outputs:

| Layer | Weights | Biases | Total |
| 784 → 128 | 100,352 | 128 | 100,480 |
| 128 → 64 | 8,192 | 64 | 8,256 |
| 64 → 10 | 640 | 10 | 650 |
| **Whole network** | | | **109,386** |

!diagram ai-model-sizes

Stored as 32-bit floating point numbers (4 bytes each), that network takes about 0.44 MB. A model with 70 billion parameters takes 280 GB in that format, which is why large models are stored in 16-bit or smaller formats (Level 14).
"""),
        Section("Hands-on: a network from lists", """
### A dense layer as matrix times vector

```python
def matvec(W, x):
    return [sum(w * xi for w, xi in zip(row, x)) for row in W]

def dense(W, b, x, activation):
    return [activation(z + bias) for z, bias in zip(matvec(W, x), b)]

def relu(z): return max(0.0, z)
def identity(z): return z

# the XOR network from the lesson
W1, b1 = [[1, 1], [1, 1]], [0, -1]
W2, b2 = [[1, -2]], [0]

for x in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    h = dense(W1, b1, x, relu)
    out = dense(W2, b2, h, identity)
    print(f"x = {x} -> hidden {h} -> output {out[0]}")
```

### Counting parameters

```python
def count_parameters(sizes):
    total = 0
    for n_in, n_out in zip(sizes, sizes[1:]):
        layer = n_in * n_out + n_out
        print(f"  {n_in:>5} -> {n_out:<5}: {layer:>11,} parameters")
        total += layer
    return total

for sizes in [[784, 128, 64, 10], [784, 512, 512, 10], [2, 3, 1]]:
    total = count_parameters(sizes)
    print(f"{sizes}: {total:,} parameters, {total * 4 / 1e6:.2f} MB as 32-bit numbers\\n")
```

### A forward pass on a batch

```python
def matmul(A, B):
    # (rows of A) x (columns of B)
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

X = [[0, 0], [0, 1], [1, 0], [1, 1]]          # a batch of four examples
W1_T = [[1, 1], [1, 1]]                       # weights, one column per hidden neuron
hidden = [[max(0, z + b) for z, b in zip(row, [0, -1])] for row in matmul(X, W1_T)]
print("hidden activations for the whole batch:", hidden)
```

### Try this

1. Change the output weights in the XOR network from [1, −2] to [1, −1]. Which input now gets the wrong answer?
2. How many parameters does a network with sizes [3, 4, 4, 1] have? Check with the code.
"""),
        Section("Level check", """
+ Describe input, hidden and output layers, and what makes a layer dense
+ Write a dense layer as output = f(Wx + b) and give the shape of W
+ Carry out a forward pass through a small network by hand
+ Explain how a hidden layer makes XOR linearly separable
+ Explain why depth helps, with the idea of features built from features
+ Count the weights and biases in a network from its layer sizes
"""),
    ],
    keyterms=[
        ("Neural network", "Layers of artificial neurons, each layer feeding the next."),
        ("Dense layer", "A layer in which every neuron receives every output of the previous layer; also called fully connected."),
        ("Hidden layer", "A layer between input and output whose values are internal to the network."),
        ("Multi-layer perceptron (MLP)", "A network of dense layers with at least one hidden layer."),
        ("Weight matrix", "The weights of a whole layer, one row per neuron and one column per input."),
        ("Forward pass", "Computing a network's output from an input, layer by layer."),
        ("Activations", "The outputs of a layer's neurons for a particular input."),
        ("Representation", "The way data is encoded at some layer; each layer re-represents the data for the next."),
        ("Parameter count", "The total number of weights and biases, which sets a model's size and memory."),
        ("Deep learning", "Machine learning with neural networks that have many hidden layers."),
    ],
    mistakes=[
        "Counting the input layer as a layer of neurons. It holds the features and does no computation.",
        "Forgetting the biases when counting parameters: each neuron has one.",
        "Getting the weight matrix the wrong way round. W has one row per neuron (output) and one column per input.",
        "Thinking hidden layers are programmed with features by people. Training discovers them.",
        "Believing bigger is always better. More parameters need more data and compute, and overfit more easily.",
    ],
    grade="""
### Tensors, shapes and broadcasting

Real frameworks work with whole tensors. A batch of 32 examples with 784 features is a (32, 784) tensor; multiplying by a (784, 128) weight matrix gives (32, 128); adding a bias of shape (128,) is **broadcast** across all 32 rows automatically. Most bugs in deep learning code are shape mistakes, so engineers write the expected shape beside every line, and check it.

### The cost of a forward pass

Multiplying an (n × k) matrix by a (k × m) one takes about n × k × m multiplications and as many additions, so roughly 2 × parameters floating point operations (FLOPs) per example for a dense network. A training step costs about three times a forward pass, because the backward pass needs about twice as much work. Level 11 uses exactly this rule of thumb to estimate what it costs to train a large language model.
""",
    quiz=[
        Q("What is a dense layer?",
          ["A layer where every neuron receives every input from the previous layer",
           "A layer with more neurons than any other layer in the network",
           "A layer whose weights are all fixed and never trained",
           "A layer that only connects each neuron to one input"], 0,
          "Dense, or fully connected, layers link every input to every neuron."),
        Q("A layer has 5 inputs and 3 neurons. What shape is its weight matrix?",
          ["3 × 5", "5 × 3", "3 × 3", "5 × 5"], 0,
          "One row per neuron (3) and one column per input (5)."),
        Q("How is a matrix multiplied by a vector?",
          ["Each row of the matrix is dot-producted with the vector",
           "Each entry of the matrix is added to the vector",
           "The matrix is turned into a vector first",
           "Only the first row is used"], 0,
          "Each row is one neuron's weights, so each dot product is one neuron's weighted sum."),
        Q("In the XOR network, h₁ = ReLU(x₁ + x₂) and h₂ = ReLU(x₁ + x₂ − 1). What are h₁ and h₂ for input (1, 1)?",
          ["2 and 1", "1 and 1", "2 and 0", "1 and 0"], 0,
          "h₁ = ReLU(2) = 2 and h₂ = ReLU(1) = 1, so the output h₁ − 2h₂ = 0."),
        Q("How does a hidden layer let a network solve XOR?",
          ["It moves the points to a new space where one line separates them",
           "It adds more training examples to the data",
           "It removes the points that are hard to classify",
           "It changes the labels of two of the points"], 0,
          "In the hidden space (h₁, h₂), the two 1s land together and the classes become linearly separable."),
        Q("How many parameters does a dense layer from 10 inputs to 4 neurons have?",
          ["44", "40", "14", "4"], 0,
          "10 × 4 = 40 weights plus 4 biases."),
        Q("Why are GPUs good at running neural networks?",
          ["Layers are matrix multiplications, which GPUs do massively in parallel",
           "GPUs have more memory than any other kind of chip",
           "GPUs can run Python code faster than processors can",
           "GPUs store the training data permanently"], 0,
          "Thousands of multiply-adds at once is exactly what graphics chips were built for."),
        Q("What do the early layers of an image network typically learn?",
          ["Simple features such as edges and colours", "Whole objects such as faces",
           "The labels of the training images", "Nothing until the last layer has trained"], 0,
          "Later layers combine edges into textures, shapes and finally objects."),
        Q("What does 'deep' mean in deep learning?",
          ["The network has many hidden layers", "The network is trained for a long time",
           "The network understands meaning deeply", "The network uses a lot of data"], 0,
          "Depth is the number of layers, each building on the representation before it."),
        Q("A model has 1 million parameters stored as 32-bit numbers. Roughly how much memory is that?",
          ["4 MB", "1 MB", "32 MB", "4 GB"], 0,
          "Each 32-bit number is 4 bytes, so 1,000,000 × 4 bytes = 4 MB."),
    ],
    exam=[
        EQ("Explain why a layer of a neural network can be written as a single matrix multiplication.", 4,
           [MP("Each neuron computes a weighted sum of the same inputs", ["weighted sum", "same inputs", "dot product"]),
            MP("Each neuron's weights form a row of a matrix", ["row", "matrix"]),
            MP("Multiplying the matrix by the input vector gives every weighted sum at once", ["every neuron", "all the neurons", "at once", "each row", "together"]),
            MP("Then the bias is added and the activation applied, f(Wx + b)", ["bias", "activation", "f(Wx", "Wx + b"])],
           "Every neuron in a layer computes a weighted sum of the same inputs, each with its own weights. If each neuron's weights are written as one row of a matrix W, then multiplying W by the input vector x takes the dot product of every row with x, giving all of the neurons' weighted sums in one operation. Adding the bias vector and applying the activation function gives the whole layer's output, f(Wx + b).",
           command="Explain"),
        EQ("A network has 4 inputs, one hidden layer of 5 neurons and 2 outputs. Calculate its total number of parameters, showing your working.", 4,
           [MP("4 × 5 = 20 weights into the hidden layer", ["4 × 5", "4x5", "20"]),
            MP("5 hidden biases, so 25 for the first layer", ["25", "+ 5"]),
            MP("5 × 2 = 10 weights and 2 biases, so 12 for the second layer", ["12", "5 × 2", "5x2", "10 + 2"]),
            MP("Total 37", ["37"])],
           "The first layer has 4 × 5 = 20 weights and 5 biases, which is 25 parameters. The second layer has 5 × 2 = 10 weights and 2 biases, which is 12 parameters. The total is 25 + 12 = 37 parameters.",
           command="Calculate"),
        EQ("Explain how the hidden layers of a deep image classifier build up an understanding of an image.", 4,
           [MP("Early layers detect simple features such as edges or colours", ["edge", "colour", "simple"]),
            MP("Later layers combine these into textures, parts or shapes", ["combine", "texture", "shape", "part"]),
            MP("The final layers represent whole objects or classes", ["object", "whole", "class", "face", "cat"]),
            MP("These features are learned in training, not programmed", ["learned", "learnt", "not programmed", "training", "automatically"])],
           "Each layer re-represents the image for the next. The early layers learn to detect simple features such as edges, lines and patches of colour. Later layers combine those into more complex features such as textures, corners and parts of objects, like an eye or a wheel. The final layers combine parts into whole objects, so the output layer can decide between classes such as cat or aeroplane. None of these features is programmed by a person: they are learned automatically during training.",
           command="Explain"),
    ],
)

L7_2 = Topic(
    slug="backpropagation",
    title="Backpropagation: How a Network Learns",
    spec="7.2",
    icon="i-repeat",
    minutes=42,
    exam_title=NEA,
    blurb="The algorithm that trains every neural network: the chain rule applied backwards through a computational graph. Worked through by hand, built into a tiny automatic differentiation engine, and used to train a network to learn XOR from scratch.",
    fact="Backpropagation was discovered several times: Seppo Linnainmaa described its core idea in 1970 and Paul Werbos proposed it for neural networks in 1974, but it took the 1986 paper by Rumelhart, Hinton and Williams to make the field pay attention.",
    sections=[
        Section("The credit assignment problem", """
A network makes a wrong prediction. It has a million weights. Which ones were to blame, and by how much should each change?

Gradient descent (Level 5) answers in principle: move every weight against its partial derivative of the loss. The question is how to get a million partial derivatives cheaply. Nudging each weight in turn (Level 5) would take a million and more forward passes per step.

**Backpropagation** gets every one of them in a single backward sweep through the network, costing about twice a forward pass. It is the reason deep learning is possible.
"""),
        Section("The chain rule, in gears", """
If y depends on u, and u depends on x, then a small change in x passes through u to y:

!info The chain rule :: dy/dx = dy/du × du/dx

!diagram ai-chain-gears

Think of gears. If gear B turns 3 times for every turn of gear A, and gear C turns 2 times for every turn of B, then C turns 3 × 2 = 6 times for every turn of A. Rates of change multiply along a chain. A neural network is a long chain of simple steps, so the effect of any weight on the loss is a product of local rates of change along the path from that weight to the loss.
"""),
        Section("Computational graphs: forward then backward", """
Write any calculation as a **computational graph**: a diagram of simple operations, each node taking inputs and producing an output.

!diagram ai-backprop-graph

The example computes the squared error of a one-weight model, L = (w × x + b − y)², with x = 2, w = 0.5, b = 0.1 and target y = 1.

1. **Forward pass**, left to right: compute each node's value. u = w × x = 1, z = u + b = 1.1, e = z − y = 0.1, L = e² = 0.01.
2. **Backward pass**, right to left: start with dL/dL = 1, and at each node multiply the incoming gradient by the node's **local** derivative.

| Node | Local derivative | Gradient arriving | Gradient passed on |
| L = e² | dL/de = 2e = 0.2 | 1 | 0.2 to e |
| e = z − y | de/dz = 1 | 0.2 | 0.2 to z |
| z = u + b | 1 to each input | 0.2 | 0.2 to u, **0.2 to b** |
| u = w × x | du/dw = x = 2 | 0.2 | **0.4 to w** |

So dL/dw = 0.4 and dL/db = 0.2. Every node only needs to know its own simple derivative; the chain rule does the rest. That locality is what makes backpropagation easy to program and fast to run.
"""),
        Section("Through a neuron, with real numbers", """
Now add a sigmoid: z = w × x + b, a = σ(z), L = (a − y)². With x = 2, w = 0.5, b = 0.1, y = 1:

| Step | Forward | Backward |
| z = 0.5 × 2 + 0.1 | **1.1** | dL/dz = dL/da × da/dz = −0.4995 × 0.1874 = **−0.0936** |
| a = σ(1.1) | **0.7503** | dL/da = 2(a − y) = **−0.4995** |
| L = (0.7503 − 1)² | **0.0624** | start: dL/dL = 1 |

The sigmoid's local derivative is a(1 − a) = 0.7503 × 0.2497 = 0.1874. Then dL/dw = dL/dz × x = **−0.1872** and dL/db = dL/dz × 1 = **−0.0936**.

Both gradients are negative, so gradient descent **increases** w and b. With a learning rate of 0.5: w becomes 0.5936 and b becomes 0.1468. Run forward again: a = 0.7915 and the loss falls from 0.0624 to **0.0435**. One step of learning, done by hand.
"""),
        Section("Backpropagation through a whole network", """
For a deep network the same process runs layer by layer, from the output back to the input:

1. **Forward pass**: compute and remember every layer's activations.
2. Compute the loss and its gradient with respect to the output.
3. For each layer, from last to first, turn the gradient arriving at its outputs into gradients for its weights, its biases and its inputs.
4. Update every weight with gradient descent.

Inside each layer, step 3 does three small things:

- multiply the incoming gradient by the activation's derivative, the local slope;
- combine that with the layer's inputs to get the gradients of its weights and biases;
- multiply by the layer's weights, transposed, to get the gradient to pass to the layer below.

Each layer receives "how much the loss would change if my outputs changed" and passes back "how much the loss would change if my inputs changed". That is why it is called **back propagation of errors**.

!diagram ai-training-loop

### The training loop

Forward pass, loss, backward pass, update, repeated for every batch and every epoch. In a framework such as PyTorch, the backward pass is a single call, because the framework records the computational graph during the forward pass automatically:

```pylocal
import torch

model = torch.nn.Sequential(torch.nn.Linear(2, 3), torch.nn.Tanh(), torch.nn.Linear(3, 1))
optimiser = torch.optim.SGD(model.parameters(), lr=0.5)
loss_fn = torch.nn.BCEWithLogitsLoss()

X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
y = torch.tensor([[0.], [1.], [1.], [0.]])

for epoch in range(2000):
    loss = loss_fn(model(X), y)     # forward pass and loss
    optimiser.zero_grad()
    loss.backward()                 # backpropagation: every gradient at once
    optimiser.step()                # gradient descent update
```

This is called **automatic differentiation**, or autograd. The hands-on section builds a tiny version from scratch.
"""),
        Section("When gradients misbehave", """
Backpropagation multiplies many local derivatives together, so the gradient can shrink or grow exponentially with depth.

| Problem | Symptom | Fixes |
| **Vanishing gradients** | Early layers barely change; training stalls | ReLU-family activations, careful initialisation, normalisation layers, residual connections |
| **Exploding gradients** | Loss suddenly jumps to huge values or NaN | Gradient clipping (cap the gradient's size), lower learning rate, normalisation |
| **Bad initialisation** | All neurons learn the same thing, or the network is stuck from the start | Random starting weights scaled to the layer size (Xavier or He initialisation) |

!warn Never start with all weights equal :: If every weight starts at the same value, every hidden neuron computes the same output and receives the same gradient, so they stay identical forever. Random initialisation **breaks the symmetry** so each neuron can learn something different.

!tool network-playground

Use the playground above to watch backpropagation shape a network's decision boundary in real time. Try a spiral with one hidden neuron, then with eight, then with two layers.
"""),
        Section("Hands-on: backpropagation from scratch", """
### A tiny automatic differentiation engine

Each Value remembers how it was made. Calling backward() walks the graph in reverse and applies the chain rule at every node.

```python
import math

class Value:
    def __init__(self, data, parents=()):
        self.data, self.grad = data, 0.0
        self.parents = parents
        self.backward_step = lambda: None

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other))
        def step():
            self.grad += out.grad
            other.grad += out.grad
        out.backward_step = step
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other))
        def step():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out.backward_step = step
        return out

    def __sub__(self, other):
        return self + (-1 * other if isinstance(other, Value) else Value(-other))

    def __rmul__(self, other):
        return self * other

    def sigmoid(self):
        s = 1 / (1 + math.exp(-self.data))
        out = Value(s, (self,))
        def step():
            self.grad += s * (1 - s) * out.grad
        out.backward_step = step
        return out

    def backward(self):
        order, seen = [], set()
        def visit(v):
            if id(v) not in seen:
                seen.add(id(v))
                for p in v.parents:
                    visit(p)
                order.append(v)
        visit(self)
        self.grad = 1.0
        for v in reversed(order):
            v.backward_step()

# the worked example: z = w*x + b, a = sigmoid(z), L = (a - y)^2
w, b = Value(0.5), Value(0.1)
a = (w * 2 + b).sigmoid()
error = a - 1
L = error * error
L.backward()
print(f"loss {L.data:.4f}, dL/dw = {w.grad:.4f}, dL/db = {b.grad:.4f}")
```

The engine reproduces the hand calculation: dL/dw = −0.1872 and dL/db = −0.0936.

### Training a network to learn XOR

Now the real thing: a network with 2 inputs, 3 tanh hidden neurons and a sigmoid output, trained by backpropagation and gradient descent, written out by hand.

```python
import math, random

random.seed(2)
H = 3
w1 = [[random.uniform(-1, 1) for _ in range(2)] for _ in range(H)]
b1 = [random.uniform(-1, 1) for _ in range(H)]
w2 = [random.uniform(-1, 1) for _ in range(H)]
b2 = 0.0
data = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)]
lr = 0.5

def forward(x):
    h = [math.tanh(w1[j][0] * x[0] + w1[j][1] * x[1] + b1[j]) for j in range(H)]
    p = 1 / (1 + math.exp(-(sum(w2[j] * h[j] for j in range(H)) + b2)))
    return h, p

for epoch in range(1, 1001):
    loss = 0.0
    for x, y in data:
        h, p = forward(x)                                   # forward pass
        loss -= y * math.log(p) + (1 - y) * math.log(1 - p)
        d_out = p - y                                       # gradient at the output
        for j in range(H):
            d_h = d_out * w2[j] * (1 - h[j] ** 2)           # back through w2 and tanh
            w2[j] -= lr * d_out * h[j]                      # update output weights
            w1[j][0] -= lr * d_h * x[0]                     # update hidden weights
            w1[j][1] -= lr * d_h * x[1]
            b1[j] -= lr * d_h
        b2 -= lr * d_out
    if epoch in (1, 50, 100, 200, 500, 1000):
        print(f"epoch {epoch:4}: average loss {loss / 4:.4f}")

for x, y in data:
    print(x, "->", round(forward(x)[1], 3), " target", y)
```

With sigmoid outputs and cross-entropy loss, the gradient at the output is simply p − y, one of the neat results that makes this pairing so popular.

### Try this

1. Change random.seed(2) to random.seed(3). Training gets stuck with every output near 0.5. A bad start can trap a network on a flat region; try H = 4 with the same seed.
2. Set lr = 5. What happens to the loss?
3. Use the Value engine to check one of the XOR network's gradients.
"""),
        Section("Level check", """
+ Explain the credit assignment problem and why nudging each weight is too slow
+ State the chain rule and explain it with an example
+ Carry out a forward and backward pass on a small computational graph
+ Calculate the gradients of a single sigmoid neuron and one gradient descent update
+ Describe how backpropagation passes gradients through the layers of a network
+ Describe vanishing and exploding gradients and why weights start random
"""),
    ],
    keyterms=[
        ("Backpropagation", "Computing the gradient of the loss with respect to every weight by applying the chain rule backwards through the network."),
        ("Credit assignment problem", "Working out how much each weight contributed to an error."),
        ("Chain rule", "The rate of change through a chain of functions is the product of each link's rate of change."),
        ("Computational graph", "A calculation drawn as a network of simple operations, used for forward and backward passes."),
        ("Local derivative", "The derivative of one node's output with respect to its inputs, which is all each node needs for backpropagation."),
        ("Automatic differentiation", "Software that records a calculation and computes its derivatives automatically; also called autograd."),
        ("Training loop", "Forward pass, loss, backward pass and update, repeated over batches and epochs."),
        ("Exploding gradient", "A gradient that grows exponentially through the layers, making training unstable."),
        ("Gradient clipping", "Capping the size of a gradient to stop exploding gradients."),
        ("Weight initialisation", "Choosing random starting weights, scaled to each layer's size, so that every neuron can learn something different."),
    ],
    mistakes=[
        "Thinking backpropagation is a different learning method from gradient descent. It only computes the gradients; gradient descent uses them.",
        "Starting every weight at zero or the same value. Every neuron then stays identical.",
        "Forgetting the activation's derivative when passing a gradient back through a layer.",
        "Believing backpropagation is slow. It costs about twice a forward pass, whatever the number of weights.",
        "Thinking the backward pass changes the weights. It computes gradients; the optimiser's step changes the weights.",
    ],
    grade="""
### Reverse mode versus forward mode

There are two ways to apply the chain rule to a graph. **Forward mode** pushes derivatives from one input to all the outputs; **reverse mode** pulls derivatives from one output back to all the inputs. A network has millions of inputs (its weights) and one output (the loss), so reverse mode gets every gradient in one sweep, while forward mode would need one sweep per weight. Backpropagation is reverse-mode automatic differentiation.

### Memory is the price

Reverse mode needs the activations from the forward pass, so training stores every layer's activations for the whole batch. That is often what limits batch size and model size on a GPU. **Gradient checkpointing** saves memory by storing only some activations and recomputing the rest during the backward pass, trading extra compute for less memory, and is standard practice for training large models.
""",
    quiz=[
        Q("What does backpropagation compute?",
          ["The gradient of the loss with respect to every weight",
           "The best learning rate for the network",
           "The output of the network for a new input",
           "The number of layers the network needs"], 0,
          "Gradient descent then uses those gradients to update the weights."),
        Q("If dy/du = 3 and du/dx = 4, what is dy/dx?",
          ["12", "7", "0.75", "1"], 0,
          "The chain rule multiplies the rates: 3 × 4 = 12."),
        Q("In which direction does the backward pass travel through the network?",
          ["From the loss back towards the inputs", "From the inputs towards the loss",
           "From the middle layer outwards", "In a random order each time"], 0,
          "It starts with dL/dL = 1 at the loss and works backwards layer by layer."),
        Q("In the graph u = w × x with x = 2, a gradient of 0.2 arrives at u. What is dL/dw?",
          ["0.4", "0.2", "0.1", "2.2"], 0,
          "Multiply the incoming gradient by the local derivative du/dw = x = 2: 0.2 × 2 = 0.4."),
        Q("What is the local derivative of a sigmoid node whose output is a?",
          ["a(1 − a)", "1 − a", "a²", "1"], 0,
          "σ′(z) = σ(z)(1 − σ(z)), at most 0.25 when a = 0.5."),
        Q("Roughly how much does a backward pass cost compared with a forward pass?",
          ["About twice as much", "About a million times as much",
           "Exactly the same", "Nothing: it is free"], 0,
          "That fixed small multiple, whatever the number of weights, is why backpropagation made deep learning practical."),
        Q("Why do networks start with random weights rather than all zeros?",
          ["Identical weights would make every neuron learn the same thing",
           "Zero weights would make training far too fast to control",
           "Random weights mean no training is needed at all",
           "Computers cannot store a weight of exactly zero"], 0,
          "Randomness breaks the symmetry so each neuron can specialise."),
        Q("A training run's loss suddenly jumps to NaN. What is a likely cause?",
          ["Exploding gradients", "Vanishing gradients", "Too few epochs",
           "The test set being too small"], 0,
          "Gradient clipping or a lower learning rate are the usual fixes."),
        Q("What does loss.backward() do in PyTorch?",
          ["Runs backpropagation to compute every parameter's gradient",
           "Updates every weight using gradient descent",
           "Runs the network's forward pass on new data",
           "Resets every gradient back to zero"], 0,
          "optimiser.step() then applies the update, and zero_grad() clears old gradients."),
        Q("With a sigmoid output and cross-entropy loss, what is the gradient of the loss with respect to the output's z?",
          ["p − y", "y − p", "p(1 − p)", "2(p − y)"], 0,
          "The sigmoid's derivative cancels neatly, which is one reason this pairing is standard."),
    ],
    exam=[
        EQ("Explain what backpropagation is and why it is needed to train neural networks.", 4,
           [MP("Training needs the gradient of the loss for every weight", ["gradient", "every weight", "each weight", "partial derivative"]),
            MP("Calculating each separately / by nudging would be far too slow", ["too slow", "nudg", "separately", "millions"]),
            MP("Backpropagation applies the chain rule backwards from the loss", ["chain rule", "backwards", "from the output", "from the loss"]),
            MP("It gets all the gradients in one backward pass, about twice the cost of a forward pass", ["one pass", "single", "all the gradients", "twice", "efficient", "at once"])],
           "Gradient descent needs the gradient of the loss with respect to every weight in the network, and a network can have millions of weights. Estimating each gradient separately, by nudging one weight at a time, would need millions of forward passes per step and be far too slow. Backpropagation applies the chain rule backwards through the network, from the loss towards the inputs, multiplying local derivatives at each layer. It produces every gradient in a single backward pass, costing only about twice a forward pass, which makes training large networks practical.",
           command="Explain"),
        EQ("A neuron computes z = wx + b and a = σ(z), with loss L = (a − y)². Given dL/da = −0.5 and a = 0.75, calculate dL/dw when x = 2.", 4,
           [MP("da/dz = a(1 − a) = 0.75 × 0.25 = 0.1875", ["0.1875", "0.75 × 0.25", "a(1 - a)", "a(1−a)"]),
            MP("dL/dz = −0.5 × 0.1875 = −0.09375", ["-0.09375", "−0.09375", "-0.094", "−0.094"]),
            MP("dz/dw = x = 2", ["x = 2", "dz/dw = 2", "× 2"]),
            MP("dL/dw = −0.1875", ["-0.1875", "−0.1875", "-0.19", "−0.19"])],
           "The sigmoid's local derivative is da/dz = a(1 − a) = 0.75 × 0.25 = 0.1875. By the chain rule, dL/dz = dL/da × da/dz = −0.5 × 0.1875 = −0.09375. Since z = wx + b, dz/dw = x = 2, so dL/dw = −0.09375 × 2 = −0.1875.",
           command="Calculate"),
        EQ("Describe the steps of the training loop used to train a neural network.", 4,
           [MP("Forward pass: compute the outputs for a batch", ["forward", "output", "predict"]),
            MP("Compute the loss by comparing outputs with targets", ["loss", "compare", "error"]),
            MP("Backward pass: backpropagation computes the gradients", ["backward", "backprop", "gradient"]),
            MP("Update the weights with gradient descent / an optimiser, then repeat for batches and epochs", ["update", "optimiser", "optimizer", "gradient descent", "repeat", "epoch"])],
           "For each batch of training examples, the network first does a forward pass, computing its outputs layer by layer. The loss is calculated by comparing those outputs with the targets. A backward pass then uses backpropagation to compute the gradient of the loss with respect to every weight and bias. Finally an optimiser such as gradient descent or Adam updates every parameter a small step against its gradient. The loop repeats for every batch, and the whole dataset is passed through many times, once per epoch.",
           command="Describe"),
    ],
)

TOPICS = [L7_1, L7_2]
