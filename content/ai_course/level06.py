"""Level 6: The Artificial Neuron. Weighted sums, decisions, and activation functions."""
from mskbuild.models import Topic, Section, Q, EQ, MP

NEA = "Check you could explain this"

L6_1 = Topic(
    slug="artificial-neuron",
    title="The Artificial Neuron: Weights, Bias and a Decision",
    spec="6.1",
    icon="i-gate",
    minutes=36,
    exam_title=NEA,
    blurb="The building block of every neural network: inputs, weights, a bias, a sum and an activation. How one neuron draws a line, imitates a logic gate and learns with the perceptron rule, and the XOR problem it cannot solve alone.",
    fact="The human brain has about 86 billion neurons joined by roughly 100 trillion synapses. The largest artificial networks now have trillions of parameters, but each of their neurons is vastly simpler than a real one.",
    sections=[
        Section("From brain cells to maths", """
A biological **neuron** receives signals from other neurons through its **dendrites**. If the combined signal in the cell body is strong enough, the neuron **fires**, sending a pulse down its **axon** to the next neurons. The junctions, called **synapses**, have different strengths, and learning changes those strengths.

!diagram ai-neuron-bio

An artificial neuron keeps only that skeleton:

| Biological | Artificial |
| Signals arriving at the dendrites | **Inputs** x₁, x₂, … xₙ |
| Synapse strengths | **Weights** w₁, w₂, … wₙ |
| How easily the cell fires | **Bias** b |
| Adding up the signals in the cell body | **Weighted sum** z = w₁x₁ + w₂x₂ + … + wₙxₙ + b |
| Firing or staying quiet | **Activation function** a = f(z) |

!warn Inspired by, not a copy of :: Real neurons communicate with timed pulses, chemistry and thousands of connections each, and are far more complicated than this. The artificial neuron is a convenient mathematical unit that happens to have been inspired by biology.
"""),
        Section("Inside an artificial neuron", """
!diagram ai-neuron-anatomy

### A worked example: will Sam enjoy this film?

The inputs describe the film. The weights describe Sam's taste. The bias describes how keen Sam is on films in general.

| Input | Value x | Weight w | w × x |
| How much action (0 to 1) | 0.9 | 1.5 | 1.35 |
| How much comedy (0 to 1) | 0.2 | 0.8 | 0.16 |
| Length in hours | 2.5 | −0.6 | −1.50 |
| Bias | | | −0.50 |
| **Weighted sum z** | | | **−0.49** |

Passing z through the sigmoid (Level 4) gives σ(−0.49) ≈ **0.38**: a 38% chance Sam enjoys it. The action helps, but at two and a half hours it is just too long.

!key Read the weights :: A positive weight means "more of this input makes a yes more likely", a negative weight means the opposite, and a large weight means the input matters a lot. Sam loves action (1.5), quite likes comedy (0.8) and dislikes long films (−0.6).

The weighted sum is a **dot product** (Level 3) of the input vector and the weight vector, plus the bias: z = w · x + b. That one line of maths, repeated billions of times, is most of what a neural network computes.
"""),
        Section("A neuron draws a line", """
With two inputs, the neuron says yes when w₁x₁ + w₂x₂ + b > 0 and no when it is below 0. The boundary, where w₁x₁ + w₂x₂ + b = 0, is a **straight line**.

!diagram ai-neuron-boundary

- The **weights** set the angle of the line. The weight vector (w₁, w₂) points at right angles to the line, towards the "yes" side.
- The **bias** slides the line without turning it.
- With three inputs the boundary is a flat plane, and with more it is a hyperplane: a single neuron can only ever separate classes with something flat.

!tool neuron-lab

Move the sliders and watch the line turn and slide. Then press **Train** and the perceptron rule below moves them for you.
"""),
        Section("Neurons as logic gates", """
In 1943 McCulloch and Pitts showed that simple threshold units can compute logic. With a step activation (output 1 if z > 0, otherwise 0):

| Gate | w₁ | w₂ | b | Why it works |
| **AND** | 1 | 1 | −1.5 | Only 1 + 1 = 2 beats 1.5 |
| **OR** | 1 | 1 | −0.5 | Any single 1 beats 0.5 |
| **NAND** | −1 | −1 | 1.5 | The opposite of AND |
| **NOT** (one input) | −1 | | 0.5 | Input 0 gives 0.5 > 0; input 1 gives −0.5 |

!diagram ai-neuron-gates

Because NAND alone can build any logic circuit, a network of neurons can in principle compute anything a digital computer can. The interesting question is not whether networks can compute, but whether they can **learn** the right weights.
"""),
        Section("The perceptron learning rule", """
Frank Rosenblatt's 1958 **perceptron** learned its weights from examples with a beautifully simple rule. For each training example:

1. Predict: output = 1 if w · x + b > 0, otherwise 0.
2. Error = target − output, which is +1, 0 or −1.
3. Update every weight: wᵢ ← wᵢ + learning rate × error × xᵢ, and the bias: b ← b + learning rate × error.

If the prediction is right, the error is 0 and nothing changes. If it said 0 but should have said 1, each weight grows in proportion to its input, pushing z up next time. If it said 1 but should have said 0, the weights shrink.

!info The perceptron convergence theorem :: If a straight line can separate the two classes perfectly, the perceptron rule is guaranteed to find one in a finite number of steps.

That guarantee is also the catch. If no straight line can separate the classes, the perceptron never settles.
"""),
        Section("The XOR problem", """
**XOR** (exclusive or) outputs 1 when exactly one input is 1.

| x₁ | x₂ | XOR |
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

!diagram ai-xor

The two "1" points sit on one diagonal and the two "0" points on the other. No single straight line can put both 1s on one side and both 0s on the other, so no single neuron can compute XOR. Minsky and Papert's 1969 book *Perceptrons* made this famous, and it helped trigger the first AI winter.

The fix was known in principle: use two neurons to draw two lines, and a third to combine them. A **hidden layer**. What was missing until 1986 was a way to train the hidden neurons. Level 7 builds that network and the algorithm that trains it.
"""),
        Section("Hands-on: build and train a neuron", """
### A neuron in four lines

```python
import math

def neuron(inputs, weights, bias):
    z = sum(x * w for x, w in zip(inputs, weights)) + bias
    return 1 / (1 + math.exp(-z))             # sigmoid activation

film = [0.9, 0.2, 2.5]                        # action, comedy, hours
sam = [1.5, 0.8, -0.6]
print(f"Chance Sam enjoys it: {neuron(film, sam, -0.5):.2f}")
print(f"The same film cut to 1.5 hours: {neuron([0.9, 0.2, 1.5], sam, -0.5):.2f}")
```

### Logic gates

```python
def step_neuron(inputs, weights, bias):
    z = sum(x * w for x, w in zip(inputs, weights)) + bias
    return 1 if z > 0 else 0

gates = {"AND": ([1, 1], -1.5), "OR": ([1, 1], -0.5), "NAND": ([-1, -1], 1.5)}
for name, (weights, bias) in gates.items():
    outputs = [step_neuron([a, b], weights, bias) for a in (0, 1) for b in (0, 1)]
    print(f"{name:4}: inputs 00 01 10 11 give {outputs}")
```

### The perceptron learns OR, then fails at XOR

```python
def train_perceptron(data, epochs=12, lr=1.0):
    w1 = w2 = b = 0.0
    for epoch in range(1, epochs + 1):
        mistakes = 0
        for (x1, x2), target in data:
            output = 1 if w1 * x1 + w2 * x2 + b > 0 else 0
            error = target - output
            if error:
                mistakes += 1
                w1 += lr * error * x1
                w2 += lr * error * x2
                b += lr * error
        print(f"  epoch {epoch:2}: w = ({w1:+.0f}, {w2:+.0f}), b = {b:+.0f}, mistakes {mistakes}")
        if mistakes == 0:
            return "learned it"
    return "never settled"

OR = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 1)]
XOR = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)]
print("OR:")
print(" ", train_perceptron(OR))
print("XOR:")
print(" ", train_perceptron(XOR, epochs=6))
```

### Try this

1. Find weights and a bias that make a neuron output 1 only when **both** inputs are 0 (NOR).
2. Train the perceptron on AND. How many epochs does it take?
3. Change Sam's weights so that the long film is predicted to be enjoyable. Which weight did you change, and what does it say about the new Sam?
"""),
        Section("Level check", """
+ Label the parts of an artificial neuron and match them to a biological neuron
+ Calculate a neuron's weighted sum and output for given inputs, weights and bias
+ Explain how the weights and the bias change a neuron's decision boundary
+ Give weights and a bias that make a neuron act as AND, OR or NOT
+ Apply the perceptron learning rule to one example by hand
+ Explain why a single neuron cannot compute XOR, and what fixes it
"""),
    ],
    keyterms=[
        ("Artificial neuron", "A unit that computes a weighted sum of its inputs plus a bias and passes it through an activation function."),
        ("Weight", "A number multiplying one input; its sign and size set how much and which way that input pushes the output."),
        ("Bias", "A number added to the weighted sum, shifting how easily the neuron outputs a high value."),
        ("Weighted sum", "z = w₁x₁ + w₂x₂ + … + b, the dot product of weights and inputs plus the bias."),
        ("Activation function", "The function applied to the weighted sum to give the neuron's output."),
        ("Step function", "An activation that outputs 1 if its input is above 0 and 0 otherwise."),
        ("Perceptron", "Rosenblatt's 1958 single neuron with a step activation, trained by the perceptron learning rule."),
        ("Linearly separable", "Able to be split into classes by a straight line, plane or hyperplane."),
        ("XOR problem", "The fact that no single neuron can compute exclusive or, because its classes are not linearly separable."),
        ("Hidden layer", "A layer of neurons between the inputs and the output, whose values are not seen directly."),
    ],
    mistakes=[
        "Forgetting the bias. Without it, every boundary must pass through the origin.",
        "Thinking a bigger input always increases the output. If its weight is negative, it decreases it.",
        "Believing artificial neurons work like real ones. They are a simple mathematical idea inspired by biology.",
        "Thinking the perceptron rule can learn anything. It only succeeds when the classes are linearly separable.",
        "Mixing up the weighted sum z and the output a. The activation function turns one into the other.",
    ],
    grade="""
### The geometry behind the weights

The decision boundary of a neuron is the set of points where w · x + b = 0. Because a dot product with w measures how far a point lies along the direction of w, the boundary is perpendicular to w, at a distance of |b| ÷ |w| from the origin. Doubling every weight and the bias leaves the line exactly where it is, but makes the sigmoid output change more sharply across it: the model becomes more confident without changing its mind. That is why weight decay (Level 4) also acts as a brake on overconfidence.

### Hebb's rule and modern learning

Donald Hebb's 1949 idea, often summarised as "cells that fire together wire together", strengthens a connection when both neurons are active. The perceptron rule adds the crucial ingredient Hebb lacked: an **error signal**. Change the weights only when the output is wrong, in the direction that reduces the error. Gradient descent and backpropagation are the grown-up version of that same idea.
""",
    quiz=[
        Q("What does an artificial neuron compute first, before its activation function?",
          ["A weighted sum of its inputs plus a bias", "The largest of its inputs",
           "The average of its weights", "A random number between 0 and 1"], 0,
          "z = w₁x₁ + w₂x₂ + … + b, which is then passed through the activation function."),
        Q("Inputs are [2, 3], weights are [0.5, −1] and the bias is 1. What is the weighted sum?",
          ["−1", "1", "3", "−2"], 0,
          "2 × 0.5 + 3 × (−1) + 1 = 1 − 3 + 1 = −1."),
        Q("What does a negative weight mean?",
          ["More of that input pushes the output down",
           "That input is ignored by the neuron",
           "That input must always be negative",
           "The neuron has made an error"], 0,
          "Sam's −0.6 weight on length means longer films make enjoyment less likely."),
        Q("What does changing the bias do to a neuron's decision boundary?",
          ["Slides it without turning it", "Turns it without sliding it",
           "Curves it", "Removes it"], 0,
          "The weights set the angle; the bias shifts the line parallel to itself."),
        Q("Which weights and bias make a step neuron compute AND?",
          ["w = (1, 1), b = −1.5", "w = (1, 1), b = −0.5", "w = (−1, −1), b = 1.5",
           "w = (1, 1), b = 0.5"], 0,
          "Only when both inputs are 1 does the sum, 2, beat 1.5."),
        Q("In the perceptron rule, what happens when the prediction is correct?",
          ["The weights do not change", "Every weight doubles",
           "The bias is reset to zero", "The learning rate increases"], 0,
          "The error is 0, so error × input is 0 for every weight."),
        Q("A perceptron outputs 0 for an example whose target is 1. What does the rule do?",
          ["Increases each weight in proportion to its input", "Decreases every weight",
           "Leaves the weights alone and changes only the input", "Deletes the example"], 0,
          "Error = +1, so wᵢ ← wᵢ + learning rate × xᵢ, pushing z up next time."),
        Q("Why can no single neuron compute XOR?",
          ["Its classes cannot be separated by one straight line",
           "XOR has too many inputs for one neuron",
           "Neurons cannot output the value 0",
           "XOR needs a negative learning rate"], 0,
          "The 1s lie on one diagonal and the 0s on the other. It takes two lines, so a hidden layer."),
        Q("What does the perceptron convergence theorem guarantee?",
          ["If a separating line exists, the rule finds one in finite steps",
           "The perceptron can learn any function at all",
           "The perceptron always reaches zero loss on XOR",
           "Training always takes exactly one epoch"], 0,
          "The guarantee only holds when the classes are linearly separable."),
        Q("Which part of an artificial neuron plays the role of synapse strength?",
          ["The weights", "The inputs", "The activation function", "The output"], 0,
          "Learning changes synapse strengths in the brain and weights in a network."),
    ],
    exam=[
        EQ("A neuron has inputs x = [1, 0, 2], weights w = [0.4, 1.2, −0.3] and bias b = 0.1. Calculate its weighted sum and its output with a step activation that outputs 1 when z > 0.", 3,
           [MP("1 × 0.4 + 0 × 1.2 + 2 × (−0.3) + 0.1", ["0.4 + 0 - 0.6", "0.4 - 0.6", "0.4+0-0.6", "0.4 + 0 − 0.6", "0.4 − 0.6"]),
            MP("z = −0.1", ["-0.1", "−0.1", "minus 0.1"]),
            MP("Output 0, because z is not above 0", ["output 0", "output is 0", "outputs 0", "gives 0", "= 0"])],
           "z = 1 × 0.4 + 0 × 1.2 + 2 × (−0.3) + 0.1 = 0.4 + 0 − 0.6 + 0.1 = −0.1. Because z is not greater than 0, the step activation outputs 0.",
           command="Calculate"),
        EQ("Explain how a perceptron learns using the perceptron learning rule.", 4,
           [MP("It makes a prediction from the weighted sum / step function", ["predict", "weighted sum", "step", "output"]),
            MP("The error is the target minus the prediction", ["target", "error", "minus", "difference"]),
            MP("Each weight changes by learning rate × error × input", ["learning rate", "error × input", "error x input", "in proportion"]),
            MP("No change when correct; repeated over the examples until no mistakes", ["no change", "correct", "repeat", "until", "epoch", "no mistakes"])],
           "For each training example the perceptron calculates its weighted sum and uses a step function to predict 0 or 1. It works out the error as the target minus the prediction. Each weight is then changed by the learning rate multiplied by the error and by that weight's input, and the bias by the learning rate times the error, so a wrong answer pushes the weighted sum towards the right side. When the prediction is correct the error is zero and nothing changes. This is repeated over all the examples, epoch after epoch, until it makes no mistakes.",
           command="Explain"),
        EQ("Explain why a single neuron cannot learn the XOR function, and how a neural network overcomes this.", 4,
           [MP("A single neuron's boundary is a straight line", ["straight line", "linear", "one line", "hyperplane"]),
            MP("XOR's outputs are not linearly separable / 1s on one diagonal", ["not linearly separable", "diagonal", "cannot be separated", "no line"]),
            MP("A hidden layer of neurons draws more than one line / transforms the inputs", ["hidden layer", "two lines", "two neurons", "transform"]),
            MP("An output neuron combines the hidden neurons' outputs", ["combine", "output neuron", "third neuron", "next layer"])],
           "A single neuron outputs 1 on one side of a straight line, its decision boundary, and 0 on the other. XOR's two 1 outputs lie on one diagonal of the square and its two 0 outputs on the other, so no single straight line can separate them: XOR is not linearly separable. A network overcomes this with a hidden layer: two hidden neurons each draw a line, for example one acting like OR and one like AND, and an output neuron combines their outputs so that it fires when OR is true but AND is not.",
           command="Explain"),
    ],
)

L6_2 = Topic(
    slug="activation-functions",
    title="Activation Functions: The Bend That Makes Networks Powerful",
    spec="6.2",
    icon="i-flow",
    minutes=34,
    exam_title=NEA,
    blurb="Why a network without activation functions is just one straight line however deep it is, the sigmoid, tanh, ReLU and GELU functions, how ReLUs build any curve, vanishing gradients, and softmax for turning scores into probabilities.",
    fact="ReLU, the activation behind most deep networks, is just max(0, z): it keeps positive numbers and replaces negative ones with zero. One of the most important ideas in deep learning fits in eight characters.",
    sections=[
        Section("Why a neuron needs a bend", """
Remove the activation function and each layer just multiplies by a matrix and adds a vector. Stack two such layers:

!info Linear layers collapse :: W₂(W₁x + b₁) + b₂ = (W₂W₁)x + (W₂b₁ + b₂), which is just one layer with weights W₂W₁

However many linear layers you stack, the result is still one linear function: one straight line, one flat plane. Depth would be pointless.

An activation function puts a **bend** (a non-linearity) into every neuron. Bends can be combined into curves, and curves can be combined into any shape. That is where a neural network's power comes from.
"""),
        Section("The activation functions you will meet", """
!diagram ai-activations

| Function | Formula | Output range | Where it is used |
| **Step** | 1 if z > 0, else 0 | 0 or 1 | The original perceptron; no gradient, so not trainable by descent |
| **Sigmoid** | 1 ÷ (1 + e^-z^) | 0 to 1 | Output layer for yes or no probabilities |
| **Tanh** | (e^z^ − e^-z^) ÷ (e^z^ + e^-z^) | −1 to 1 | Older hidden layers and recurrent networks; centred on zero |
| **ReLU** | max(0, z) | 0 to ∞ | The default for hidden layers |
| **Leaky ReLU** | z if z > 0, else 0.01z | −∞ to ∞ | Avoids neurons that stop learning |
| **GELU** | z × (probability a standard normal value is below z) | about −0.17 to ∞ | Transformers, including BERT and the GPT family |
"""),
        Section("ReLU: the bend that made deep learning work", """
The **rectified linear unit**, ReLU(z) = max(0, z), became the standard around 2010 to 2012, and AlexNet's success in 2012 relied on it. It has three big advantages:

- **Cheap**: one comparison, no exponentials.
- **Strong gradients**: for any positive z its slope is exactly 1, so the learning signal passes through many layers without shrinking.
- **Sparse**: for negative z it outputs exactly 0, so only some neurons are active for a given input, which makes networks efficient.

Its weakness: a neuron whose z is negative for every input outputs 0 and has slope 0 everywhere, so it can never recover. These are **dead neurons**. **Leaky ReLU** keeps a small slope for negative z to fix this, and smooth variants such as **GELU** and **SiLU** (also called Swish) work slightly better in very large models.
"""),
        Section("Building curves from ReLUs", """
Each ReLU neuron adds one "hinge": a point where the line is allowed to change direction. Add several, each with its own weight and bias, and you can trace almost any curve.

!diagram ai-relu-sum

This is the idea behind the **universal approximation theorem**: a network with one hidden layer of enough neurons can approximate any continuous function as closely as you like. Each hidden neuron contributes one bend, and the output layer adds them up with weights.

The theorem says such a network **exists**. It does not say gradient descent will find it, or how many neurons it needs. In practice, **deep** networks, with many layers each folding the space again, need far fewer neurons than one enormous shallow layer.
"""),
        Section("Derivatives and vanishing gradients", """
Training needs each activation's slope (Level 5), and the slopes multiply together as the error signal passes back through the layers (Level 7).

!diagram ai-activation-derivs

The sigmoid's slope is σ(z) × (1 − σ(z)), which is never more than **0.25**. Pass a gradient back through ten sigmoid layers and it is multiplied by at most 0.25 ten times:

!info Vanishing gradients :: 0.25¹⁰ ≈ 0.00000095, so the first layers barely learn at all

This **vanishing gradient problem** is a big reason deep networks were so hard to train before about 2010. ReLU's slope of 1 for positive inputs, together with better starting weights, normalisation layers and the shortcut connections of ResNets (Level 8), is what made networks with dozens and then hundreds of layers trainable.
"""),
        Section("Softmax: scores into probabilities", """
A classifier choosing among many classes ends with one output per class, a raw score called a **logit**. **Softmax** turns the logits into probabilities:

!info Softmax :: probability of class i = exp(zᵢ) ÷ (the sum of exp(z) over every class), where exp(z) means e^z^

!diagram ai-softmax

- Every output is between 0 and 1, and they add up to exactly 1.
- The order is kept: the biggest logit gets the biggest probability.
- Exponentials exaggerate differences: a logit 2 higher gives about 7.4 times the probability.

### Temperature

Dividing the logits by a **temperature** T before softmax controls how peaked the result is. T below 1 sharpens it towards the top choice; T above 1 flattens it towards an even spread. Language models use exactly this to decide how adventurous their word choices are (Level 11).

### Choosing activations

| Layer | Usual choice |
| Hidden layers | ReLU, or GELU in transformers |
| Output for a number (regression) | None: the raw z |
| Output for yes or no, or several independent yes or no labels | Sigmoid |
| Output for one class out of many | Softmax |
"""),
        Section("Hands-on: activations in code", """
### The functions, side by side

```python
import math

def sigmoid(z): return 1 / (1 + math.exp(-z))
def tanh(z): return math.tanh(z)
def relu(z): return max(0.0, z)
def leaky_relu(z): return z if z > 0 else 0.01 * z
def gelu(z): return 0.5 * z * (1 + math.erf(z / math.sqrt(2)))

print("   z  sigmoid   tanh   relu  leaky   gelu")
for z in [-3, -1, -0.5, 0, 0.5, 1, 3]:
    print(f"{z:4}  {sigmoid(z):7.3f} {tanh(z):6.3f} {relu(z):6.2f} {leaky_relu(z):6.2f} {gelu(z):6.3f}")
```

### Vanishing gradients

```python
import math

def sigmoid(z): return 1 / (1 + math.exp(-z))
def sigmoid_slope(z): return sigmoid(z) * (1 - sigmoid(z))

gradient = 1.0
for layer in range(1, 11):
    gradient *= sigmoid_slope(0)          # 0.25, the best case
    print(f"after {layer:2} sigmoid layers: {gradient:.8f}")
print("through 10 ReLU layers with positive inputs:", 1.0 ** 10)
```

### Softmax and temperature

```python
import math

def softmax(logits, temperature=1.0):
    exps = [math.exp(z / temperature) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

classes = ["cat", "dog", "fox", "owl"]
logits = [2.0, 1.0, 0.1, -1.0]
for T in [0.5, 1.0, 2.0]:
    probs = softmax(logits, T)
    shown = ", ".join(f"{c} {p:.2f}" for c, p in zip(classes, probs))
    print(f"T = {T}: {shown}   (sum {sum(probs):.2f})")
```

### A bump built from three ReLUs

```python
def relu(z): return max(0.0, z)

def bump(x):
    # three hidden neurons, then a weighted sum: up from 1, down from 2, flat after 3
    return 1.0 * relu(x - 1) - 2.0 * relu(x - 2) + 1.0 * relu(x - 3)

for i in range(9):
    x = i * 0.5
    print(f"x = {x:3}: {bump(x):4.1f} " + "#" * int(bump(x) * 20))
```

### Try this

1. Add a fourth ReLU to the bump so that it rises again after x = 3.5.
2. What happens to softmax at T = 0.1? And at T = 100?
3. Find the z at which the sigmoid's slope is largest. Why does it make sense that it is there?
"""),
        Section("Level check", """
+ Show that stacking linear layers without activations gives a single linear function
+ Sketch the sigmoid, tanh, ReLU and leaky ReLU functions and state their ranges
+ Give three reasons ReLU became the default activation for hidden layers
+ Explain how a sum of ReLUs can approximate a curve, and what the universal approximation theorem says
+ Explain the vanishing gradient problem using the sigmoid's maximum slope
+ Calculate softmax for a few logits and explain the effect of temperature
"""),
    ],
    keyterms=[
        ("Non-linearity", "A bend in a function. Activation functions add one to every neuron so that layers do not collapse into one."),
        ("Sigmoid", "1 ÷ (1 + e^-z^), squashing any number into the range 0 to 1."),
        ("Tanh", "The hyperbolic tangent, an S-shaped function from −1 to 1, centred on zero."),
        ("ReLU", "The rectified linear unit, max(0, z): the default activation for hidden layers."),
        ("Leaky ReLU", "Like ReLU but with a small slope for negative inputs, so neurons cannot die."),
        ("GELU", "A smooth ReLU-like activation used in transformers."),
        ("Dead neuron", "A ReLU neuron whose input is negative for every example, so it outputs 0 and never learns."),
        ("Universal approximation theorem", "A network with one hidden layer of enough neurons can approximate any continuous function."),
        ("Vanishing gradient", "A learning signal that shrinks layer by layer until the early layers barely learn."),
        ("Logit", "A raw output score before it is turned into a probability."),
        ("Softmax", "A function turning a list of logits into probabilities that are all positive and add up to 1."),
        ("Temperature", "A number the logits are divided by before softmax; low values sharpen the probabilities, high values flatten them."),
    ],
    mistakes=[
        "Thinking more layers always help without activations. Without a non-linearity, any number of layers equals one.",
        "Using a step function in a network trained by gradient descent. Its slope is zero everywhere, so nothing learns.",
        "Putting softmax on a regression output. Regression outputs a raw number with no activation.",
        "Believing the universal approximation theorem means any network will learn anything. It only says a suitable network exists.",
        "Forgetting that softmax outputs depend on all the logits together. Raising one logit lowers every other probability.",
    ],
    grade="""
### Numerical stability in softmax

e to the power 1,000 overflows a computer's floating point numbers. Real implementations subtract the largest logit from every logit before exponentiating: softmax(z) = softmax(z − max(z)), which gives exactly the same probabilities because the common factor cancels. Libraries also combine softmax with the logarithm in cross-entropy (the log-softmax) to avoid ever computing tiny probabilities directly. If you implement these yourself and see NaN, "not a number", in your loss, this is usually why.

### Why the slope of 1 matters so much

In a network of depth L, the gradient reaching the first layer is roughly a product of L factors, one per layer. If the typical factor is a little below 1 the product vanishes; a little above 1 and it explodes. Good initialisation schemes (Xavier for tanh, He for ReLU) choose the starting weights' spread so the typical factor is close to 1, layer after layer. Residual connections (Level 8) add a path where the factor is exactly 1, which is why networks hundreds of layers deep can train at all.
""",
    quiz=[
        Q("What happens if a deep network has no activation functions?",
          ["All its layers collapse into one linear function",
           "It becomes able to learn any function at all",
           "It trains much faster and more accurately",
           "Its outputs are always exactly zero"], 0,
          "W₂(W₁x + b₁) + b₂ is just another linear function, so depth adds nothing."),
        Q("What is ReLU(−3)?",
          ["0", "−3", "3", "0.05"], 0,
          "ReLU(z) = max(0, z), so every negative input becomes 0."),
        Q("What is the output range of tanh?",
          ["−1 to 1", "0 to 1", "0 to infinity", "−infinity to infinity"], 0,
          "Tanh is S-shaped like the sigmoid but centred on zero."),
        Q("Why did ReLU help deep networks train?",
          ["Its slope is 1 for positive inputs, so gradients do not shrink",
           "It outputs probabilities that always add up to 1",
           "It uses exponentials, which are very fast to compute",
           "It stops any neuron from ever outputting zero"], 0,
          "A slope of 1 passes the learning signal back through many layers intact."),
        Q("What is a dead ReLU neuron?",
          ["One whose input is negative for every example, so it never learns",
           "One that outputs the same positive value for every input",
           "One that has been deleted from the network on purpose",
           "One whose weights have all been set to exactly one"], 0,
          "Output 0 and slope 0 everywhere means no gradient ever reaches its weights. Leaky ReLU avoids this."),
        Q("What is the largest possible slope of the sigmoid function?",
          ["0.25", "1", "0.5", "4"], 0,
          "σ(z)(1 − σ(z)) peaks at z = 0, where it is 0.5 × 0.5 = 0.25."),
        Q("A gradient passes back through 5 sigmoid layers, each multiplying it by 0.25. What fraction is left?",
          ["About 0.001", "0.25", "1.25", "About 0.1"], 0,
          "0.25⁵ ≈ 0.00098: the vanishing gradient problem."),
        Q("Which activation is usual for the output layer of a classifier choosing one class out of ten?",
          ["Softmax", "ReLU", "Tanh", "No activation"], 0,
          "Softmax gives ten probabilities that add up to 1."),
        Q("Softmax is applied to logits [3, 1, 1]. Which statement is true?",
          ["The first probability is the largest and all three add up to 1",
           "All three probabilities are exactly equal to each other",
           "The probabilities add up to 5, the sum of the logits",
           "The second and third probabilities are both zero"], 0,
          "Softmax keeps the order, makes every output positive and normalises the total to 1."),
        Q("What does a high softmax temperature, such as T = 5, do?",
          ["Flattens the probabilities towards an even spread",
           "Sharpens them so the top choice gets nearly all of it",
           "Makes the probabilities add up to 5",
           "Reverses the order of the classes"], 0,
          "Dividing logits by a large T shrinks their differences before exponentiating."),
    ],
    exam=[
        EQ("Explain why neural networks need non-linear activation functions.", 4,
           [MP("Without them each layer is a linear function / matrix multiply", ["linear", "matrix", "straight line"]),
            MP("Stacked linear layers collapse into a single linear layer", ["collapse", "single layer", "one layer", "equivalent to one"]),
            MP("So depth adds nothing / can only model straight lines or planes", ["depth", "straight", "planes", "only linear", "pointless"]),
            MP("Non-linear activations add bends that combine into curves / any function", ["bend", "curve", "any function", "complex", "non-linear"])],
           "Without an activation function, each layer only multiplies its inputs by a matrix and adds a bias, which is a linear function. Stacking linear functions gives another linear function, so however many layers the network had it would collapse to a single linear layer, and depth would add nothing: it could only ever model straight lines and flat planes. A non-linear activation puts a bend into every neuron, and many bends can be combined into curves that can approximate almost any function.",
           command="Explain"),
        EQ("Compare the sigmoid and ReLU activation functions for use in the hidden layers of a deep network.", 5,
           [MP("Sigmoid squashes outputs into 0 to 1", ["0 to 1", "0 and 1", "squash"]),
            MP("Sigmoid's slope is at most 0.25 / saturates for large inputs", ["0.25", "saturat", "flat", "small slope"]),
            MP("So gradients vanish through many sigmoid layers", ["vanish", "shrink", "early layers"]),
            MP("ReLU outputs max(0, z) with slope 1 for positive inputs", ["max(0", "slope 1", "slope of 1", "gradient of 1"]),
            MP("ReLU is cheap but can produce dead neurons", ["cheap", "fast", "dead", "die", "zero for negative"])],
           "The sigmoid squashes its input into the range 0 to 1, but its slope is never more than 0.25 and is almost zero for large positive or negative inputs, where it saturates. In a deep network the gradients are multiplied by these small slopes layer after layer, so they vanish and the early layers barely learn. ReLU outputs max(0, z), whose slope is exactly 1 for any positive input, so gradients pass back without shrinking, and it is very cheap to compute because it needs no exponential. Its drawback is that a neuron whose input is always negative outputs 0 with zero slope and dies. Overall ReLU is much better for hidden layers, which is why it is the default.",
           command="Compare"),
        EQ("A classifier outputs the logits [2, 0, 0] for three classes. Calculate the softmax probability of the first class, given that e² ≈ 7.39.", 3,
           [MP("e⁰ = 1 for the other two classes", ["e0 = 1", "e^0", "= 1", "1 + 1"]),
            MP("7.39 ÷ (7.39 + 1 + 1) = 7.39 ÷ 9.39", ["9.39", "7.39 / 9.39", "7.39/9.39", "7.39 ÷ 9.39"]),
            MP("≈ 0.79", ["0.79", "79%", "0.787"])],
           "e⁰ = 1, so the sum of the exponentials is 7.39 + 1 + 1 = 9.39. The probability of the first class is 7.39 ÷ 9.39 ≈ 0.79, and the other two classes get about 0.11 each.",
           command="Calculate"),
    ],
)

TOPICS = [L6_1, L6_2]
