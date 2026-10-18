"""Level 5: Learning by Descent. Loss functions, gradients and gradient descent."""
from mskbuild.models import Topic, Section, Q, EQ, MP

NEA = "Check you could explain this"

L5_1 = Topic(
    slug="loss-and-gradients",
    title="Loss Functions and Gradients: Measuring Wrongness",
    spec="5.1",
    icon="i-gauge",
    minutes=36,
    exam_title=NEA,
    blurb="How a model measures its own mistakes with a single number, why cross-entropy punishes confident errors, what a loss landscape looks like in 3D, and how derivatives and gradients point the way downhill.",
    fact="Every large language model is trained by making one number smaller: the average cross-entropy loss of its next-word predictions. Months of computing and billions of parameters, all in the service of nudging that single number down.",
    sections=[
        Section("What a loss function is", """
To improve, a model needs to know how wrong it is, as one number. That number is the **loss** (also called the cost or error), and the formula that produces it is the **loss function**. Training means changing the parameters to make the loss as small as possible.

The crucial shift in thinking: during training the data is fixed and the **parameters** vary. So the loss is a function of the parameters. Each choice of w gives a different line, and each line has a different loss.

!diagram ai-loss-curve

For the revision data from Level 4, with b held at 33.2, a slope of 3 badly underestimates, a slope of 10 badly overestimates, and the loss is lowest at w ≈ 6.5. Plotted against w, the mean squared error makes a bowl, and training means finding the bottom of the bowl.
"""),
        Section("Common loss functions", """
| Task | Loss function | Formula for one example |
| Regression | **Mean squared error** | (y − prediction)² |
| Regression with outliers | **Mean absolute error** | the size of (y − prediction) |
| Yes or no classification | **Binary cross-entropy** (log loss) | −[y × log p + (1 − y) × log(1 − p)] |
| Choosing one of many classes | **Categorical cross-entropy** | −log(probability given to the correct class) |

Here p is the probability the model gave to "yes", and y is 1 for yes and 0 for no. The loss over a dataset is the average over all the examples.

### Why cross-entropy?

Cross-entropy only looks at the probability the model gave to the **right** answer, and takes the negative logarithm.

!diagram ai-cross-entropy

| Probability given to the right answer | Loss, −ln p |
| 0.99 | 0.01 |
| 0.9 | 0.11 |
| 0.5 | 0.69 |
| 0.1 | 2.30 |
| 0.01 | 4.61 |

Being confidently wrong is punished brutally: the loss heads to infinity as p heads to 0. That pushes a classifier to be honest about uncertainty. A language model's training loss is exactly this, averaged over every next-word prediction it makes.
"""),
        Section("The loss landscape", """
With two parameters, w and b, the loss is a **surface** over the w-b plane: a landscape whose height at each point is the loss of that line.

!diagram ai-loss-surface

- Every point on the floor is one possible model.
- The height above it is how wrong that model is.
- Training is a search for the lowest point.

For linear regression the landscape is a single smooth bowl. For a neural network it is a landscape in millions or billions of dimensions, with valleys, ridges, plateaus and saddles. Nobody can picture that, but the maths of finding the way down is the same in any number of dimensions.

A **contour map** of the landscape, like a walking map of a hill, joins points of equal loss. The rings close in on the minimum.
"""),
        Section("Slopes and derivatives", """
To walk downhill you need to know which way is down. In one dimension, that is the **slope**, and in calculus the slope of a curve at a point is its **derivative**.

!diagram ai-tangent

For the loss L(w) = (w − 3)², the derivative is dL/dw = 2(w − 3):

| w | Slope 2(w − 3) | Meaning |
| 1 | −4 | Downhill is to the right: increase w |
| 3 | 0 | The bottom: no slope at all |
| 5 | +4 | Downhill is to the left: decrease w |

So the derivative tells us two things: its **sign** says which way is uphill, so we move the other way, and its **size** says how steep the slope is.

### Three rules you will use

- **Power rule**: the derivative of x² is 2x, of x³ is 3x², of xⁿ is nx to the power n − 1.
- **Constant multiple**: the derivative of 5x² is 5 × 2x = 10x.
- **Chain rule**: for a function inside a function, multiply the derivatives. The derivative of (w − 3)² is 2(w − 3) × 1. Level 7 shows that backpropagation is the chain rule applied over and over.
"""),
        Section("Gradients: slopes in many directions", """
With many parameters, we take the slope in each direction separately. Each one is a **partial derivative**, written ∂L/∂w, "the rate the loss changes as w changes, with everything else held still". Collected into a vector, they make the **gradient**, written ∇L.

!diagram ai-gradient-field

!key The gradient points uphill :: The gradient points in the direction in which the loss increases fastest. So the **negative** gradient points steepest **downhill**. Every learning step in deep learning moves the parameters a little way along the negative gradient.

### The gradient of the mean squared error

For the line prediction = wx + b, with error = prediction − y for each example:

!info Gradients of MSE :: ∂L/∂w = the average of 2 × error × x, and ∂L/∂b = the average of 2 × error

These are easy to read. If the predictions are too high, the errors are positive, both gradients are positive, and stepping against them lowers w and b. The bigger an example's x, the more it pushes on w.
"""),
        Section("Numerical gradients: checking with tiny nudges", """
You can estimate a derivative without any calculus: nudge the parameter a tiny amount h up and down, and see how much the loss changes.

!info Central difference :: slope ≈ [L(w + h) − L(w − h)] ÷ 2h, with h very small, such as 0.0001

This is how engineers check that their gradient code is correct, called **gradient checking**. But it is far too slow to train with: a model with a billion parameters would need two billion loss calculations for a single step. **Backpropagation** (Level 7) gets every partial derivative at once for the cost of about one extra pass through the model, which is what makes deep learning possible at all.
"""),
        Section("Hands-on: losses and gradients in code", """
### The loss curve, drawn in text

```python
hours = [1, 2, 2, 3, 4, 5, 6, 6, 7, 8]
score = [38, 45, 50, 52, 61, 64, 70, 75, 78, 86]
b = 33.2

def loss(w):
    return sum((w * x + b - y) ** 2 for x, y in zip(hours, score)) / len(hours)

for w in [3, 4, 5, 6, 6.5, 7, 8, 9, 10]:
    L = loss(w)
    print(f"w = {w:4}: loss {L:7.1f} " + "#" * int(L / 10))
```

### Calculus versus nudging

```python
def L(w):
    return (w - 3) ** 2

def exact_slope(w):
    return 2 * (w - 3)

def nudge_slope(w, h=0.0001):
    return (L(w + h) - L(w - h)) / (2 * h)

for w in [1, 3, 5, 10]:
    print(f"w = {w:2}: exact {exact_slope(w):6.2f}   by nudging {nudge_slope(w):6.2f}")
```

### The gradient of the revision model

```python
hours = [1, 2, 2, 3, 4, 5, 6, 6, 7, 8]
score = [38, 45, 50, 52, 61, 64, 70, 75, 78, 86]

def gradients(w, b):
    n = len(hours)
    dw = sum(2 * (w * x + b - y) * x for x, y in zip(hours, score)) / n
    db = sum(2 * (w * x + b - y) for x, y in zip(hours, score)) / n
    return dw, db

for w, b in [(0, 0), (10, 40), (6.52, 33.23)]:
    dw, db = gradients(w, b)
    print(f"at w={w:5}, b={b:5}: dL/dw = {dw:8.2f}, dL/db = {db:7.2f}")
```

At (0, 0) both gradients are large and negative, so increasing w and b reduces the loss. At (10, 40) they are positive: the line is too high. At the least squares answer they are almost exactly zero, which is how you recognise the bottom of the bowl.

### Cross-entropy

```python
import math

for p in [0.99, 0.9, 0.7, 0.5, 0.3, 0.1, 0.01]:
    print(f"p(correct) = {p:4}: loss = {-math.log(p):.3f}")
```
"""),
        Section("Level check", """
+ Explain what a loss function is and why it is a function of the parameters
+ Choose a suitable loss for regression and for classification
+ Calculate cross-entropy for a prediction and explain why confident mistakes cost so much
+ Describe a loss landscape and what its lowest point represents
+ Calculate a derivative with the power rule and explain what its sign and size mean
+ Explain what the gradient is and why we step in the opposite direction
"""),
    ],
    keyterms=[
        ("Loss function", "A formula giving one number that measures how wrong a model's predictions are; training minimises it."),
        ("Mean squared error", "The average of the squared differences between predictions and true values."),
        ("Cross-entropy", "A classification loss: the negative logarithm of the probability given to the correct answer."),
        ("Loss landscape", "The surface formed by the loss over every possible setting of the parameters."),
        ("Minimum", "The lowest point of the loss: the best parameters for the training data."),
        ("Derivative", "The slope of a function at a point: how fast its output changes as its input changes."),
        ("Partial derivative", "The slope with respect to one parameter while all the others are held fixed."),
        ("Gradient", "The vector of all the partial derivatives; it points in the direction of steepest increase."),
        ("Chain rule", "The derivative of a function of a function is the product of their derivatives."),
        ("Gradient checking", "Comparing gradients from code with estimates made by nudging each parameter slightly."),
    ],
    mistakes=[
        "Thinking the loss is a function of the input data. During training the data is fixed and the loss changes with the parameters.",
        "Stepping in the direction of the gradient. The gradient points uphill; descent goes the opposite way.",
        "Using mean squared error for a classifier that outputs probabilities. Cross-entropy trains them far better.",
        "Assuming a zero gradient always means the best answer. It can also be a saddle point or a local minimum.",
        "Believing numerical gradients are used for training. They are only used to check code, because they are far too slow.",
    ],
    grade="""
### Where cross-entropy comes from

Cross-entropy comes from **information theory**, founded by Claude Shannon in 1948. The information in an event with probability p is −log₂ p bits: a fair coin flip carries 1 bit, a 1 in 1,024 event carries 10. Cross-entropy measures how many bits, on average, you would need to encode what really happened using the model's probabilities. A perfect model needs the fewest. So when a language model's loss falls, it is literally becoming a better compressor of text, which is why some researchers describe prediction and compression as two sides of the same coin.

### Maximum likelihood

Minimising cross-entropy is the same as choosing the parameters that make the training data most probable under the model, called **maximum likelihood estimation**. Minimising mean squared error is maximum likelihood too, if the noise is assumed to follow a normal distribution. Behind the formulas sits one idea: choose the model under which what you saw was most likely.
""",
    quiz=[
        Q("During training, what is the loss a function of?",
          ["The model's parameters, with the data held fixed",
           "The input data, with the parameters held fixed",
           "The number of layers in the model",
           "The time the model has been training"], 0,
          "Each setting of the parameters gives a different model and so a different loss."),
        Q("Which loss is the usual choice for a classifier that outputs probabilities?",
          ["Cross-entropy", "Mean squared error", "Mean absolute error",
           "Accuracy"], 0,
          "Cross-entropy uses the probability given to the correct class and punishes confident mistakes heavily."),
        Q("A model gives the correct class a probability of 0.5. What is its cross-entropy loss, −ln 0.5?",
          ["About 0.69", "About 0.05", "About 2.30", "Exactly 0.5"], 0,
          "ln 0.5 ≈ −0.693, so the loss is about 0.69."),
        Q("What happens to cross-entropy loss as the probability given to the right answer approaches 0?",
          ["It grows towards infinity", "It falls towards 0",
           "It stays at a constant value", "It becomes negative"], 0,
          "−ln p grows without limit as p shrinks, so confident mistakes are punished brutally."),
        Q("What is the derivative of L(w) = (w − 3)² at w = 5?",
          ["4", "−4", "2", "0"], 0,
          "dL/dw = 2(w − 3) = 2 × 2 = 4: the slope is uphill to the right, so w should decrease."),
        Q("The derivative of the loss at the current w is negative. What should training do to w?",
          ["Increase it", "Decrease it", "Leave it unchanged",
           "Set it to zero"], 0,
          "A negative slope means the loss falls as w rises, so step to the right."),
        Q("In which direction does the gradient point?",
          ["The direction of steepest increase in loss",
           "The direction of steepest decrease in loss",
           "Towards the origin of the parameter space",
           "Along a contour of equal loss"], 0,
          "So gradient descent steps the opposite way, along the negative gradient."),
        Q("What is a partial derivative?",
          ["The slope with respect to one parameter, with the others held fixed",
           "Half of the full derivative of the loss",
           "A derivative calculated on part of the data",
           "The derivative of the final layer only"], 0,
          "Collecting the partial derivatives for every parameter gives the gradient vector."),
        Q("Why are numerical gradients not used to train large models?",
          ["They need two loss calculations for every single parameter",
           "They always give the wrong answer for neural networks",
           "They only work for models with one parameter",
           "They cannot be calculated on a computer"], 0,
          "With a billion parameters that is two billion passes per step. Backpropagation gets them all at once."),
        Q("What does a contour on a loss contour map join?",
          ["Points with the same loss", "Points with the same gradient",
           "The steps of the training run", "Models with the same number of parameters"], 0,
          "Like height contours on a walking map, the rings close in on the minimum."),
    ],
    exam=[
        EQ("Explain why cross-entropy is a better loss than accuracy for training a classifier.", 4,
           [MP("Cross-entropy uses the predicted probability of the correct class", ["probability", "confidence", "how sure"]),
            MP("It gives larger loss for confident wrong answers", ["confident", "punish", "large loss", "infinity", "heavily"]),
            MP("It changes smoothly, so gradients exist / small improvements are rewarded", ["smooth", "gradient", "small change", "continuous", "derivative"]),
            MP("Accuracy only counts right or wrong / is flat so gives no gradient", ["right or wrong", "flat", "no gradient", "does not change", "step", "count"])],
           "Cross-entropy uses the probability the model gave to the correct class, so it measures how confident the model was as well as whether it was right, and it punishes confident wrong answers very heavily. Because it changes smoothly as the probabilities change, it has a gradient, so even a small improvement lowers the loss and gradient descent knows which way to move. Accuracy only counts right or wrong, so it stays flat while the model improves slightly, giving no gradient to learn from.",
           command="Explain"),
        EQ("For L(w) = (w − 4)², calculate dL/dw at w = 1 and explain what the answer tells you.", 3,
           [MP("dL/dw = 2(w − 4)", ["2(w - 4)", "2(w−4)", "2(w-4)", "2w - 8", "2w-8"]),
            MP("At w = 1 it is −6", ["-6", "−6", "minus 6", "negative 6"]),
            MP("Negative, so the loss falls as w increases: increase w", ["increase", "right", "bigger", "raise"])],
           "dL/dw = 2(w − 4), so at w = 1 it is 2 × (1 − 4) = −6. The slope is negative, which means the loss decreases as w increases, so to reduce the loss w should be increased, towards the minimum at w = 4. The size, 6, shows the slope is fairly steep, so w is a long way from the minimum.",
           command="Calculate"),
        EQ("Describe what the gradient of a loss function is and how it is used in training.", 4,
           [MP("The vector of partial derivatives of the loss for every parameter", ["partial", "every parameter", "each parameter", "vector"]),
            MP("It points in the direction of steepest increase in loss", ["steepest", "uphill", "increase"]),
            MP("Training moves the parameters in the opposite direction", ["opposite", "negative gradient", "downhill", "against"]),
            MP("By a small step, scaled by the learning rate, repeatedly", ["learning rate", "small step", "repeat", "many times", "step size"])],
           "The gradient is the vector of partial derivatives of the loss with respect to every parameter. It points in the direction in which the loss increases most steeply. In training, each parameter is moved a small step in the opposite direction, along the negative gradient, with the size of the step set by the learning rate. Repeating this many times walks the parameters downhill towards a minimum of the loss.",
           command="Describe"),
    ],
)

L5_2 = Topic(
    slug="gradient-descent",
    title="Gradient Descent: How Models Learn by Rolling Downhill",
    spec="5.2",
    icon="i-route",
    minutes=38,
    exam_title=NEA,
    blurb="The algorithm that trains almost every model in AI: step against the gradient, again and again. Learning rates, batches and epochs, reading loss curves, valleys and saddle points in 3D, and the momentum and Adam optimisers.",
    fact="The idea of gradient descent was described by the French mathematician Augustin-Louis Cauchy in 1847, more than a century before the first neural network. It now runs on millions of processors, every second of every day.",
    sections=[
        Section("The algorithm", """
Imagine standing on a mountain in thick fog, trying to reach the valley floor. You cannot see the valley, but you can feel the slope under your feet. So you take a step in the steepest downhill direction, feel the slope again, and repeat.

!info Gradient descent :: Repeat: parameters ← parameters − learning rate × gradient

1. Start with random (or zero) parameters.
2. Calculate the loss and its gradient on the training data.
3. Move every parameter a small step against its gradient.
4. Repeat until the loss stops improving.

!diagram ai-descent-steps

Press Play to watch it work. Far from the minimum the slope is steep, so the steps are big. Close to it the slope flattens, so the steps shrink on their own, and the ball settles gently into the bottom.
"""),
        Section("The learning rate", """
The **learning rate**, often written η (eta), sets the size of each step. It is the most important setting in all of deep learning.

!diagram ai-learning-rates

| Learning rate | What happens |
| Too small | Progress is painfully slow; training may run out of time long before the bottom |
| About right | Steady progress to the minimum |
| Too large | Each step overshoots the valley and lands higher up the other side; the loss bounces or explodes |

There is no formula for the right value. Engineers try values spaced by factors of about 3 or 10 (0.1, 0.03, 0.01, 0.003) and watch the loss. Large models also change the learning rate during training with a **schedule**: a short **warm-up** from almost zero, then a slow **decay**, often following a cosine curve, so the final steps are small and careful.

Settings like this, which are chosen by people rather than learned, are called **hyperparameters**. The learning rate, the number of layers and k in k-nearest neighbours are all hyperparameters.
"""),
        Section("Batches, epochs and stochastic gradient descent", """
Calculating the gradient over the **whole** dataset for every single step is accurate but slow when there are millions of examples. Instead:

| Method | Gradient calculated from | Character |
| **Batch gradient descent** | Every example | Smooth, accurate, slow per step |
| **Stochastic gradient descent (SGD)** | One random example | Very noisy, very fast per step |
| **Mini-batch gradient descent** | A random batch, often 32 to 4,096 examples | The standard compromise, and what GPUs are built for |

One pass through the whole training set is an **epoch**. With 50,000 examples and a batch size of 100, one epoch is 500 steps.

The noise in mini-batch gradients is not only a cost. It jiggles the parameters out of narrow dips and flat regions and seems to help models generalise, which is one reason the method works as well as it does.
"""),
        Section("Watching training: loss curves", """
Engineers watch two curves while a model trains: the loss on the **training** data and the loss on the **validation** data.

!diagram ai-training-curves

- Both falling together: the model is still learning patterns that generalise.
- Training still falling but validation rising: the model has started to **overfit**, memorising the training examples.
- **Early stopping** keeps the parameters from the epoch with the lowest validation loss and stops there.

!warn Read the curve, not one number :: A training loss that suddenly shoots up usually means the learning rate is too high. A loss that will not fall at all can mean a bug, such as labels shuffled out of line with their examples. A validation loss lower than the training loss can happen early on, especially when training uses tricks such as dropout.
"""),
        Section("Valleys, saddles and plateaus in 3D", """
The bowl of linear regression has one bottom. The landscape of a neural network does not.

!diagram ai-landscape-3d

| Feature | What it is | Problem for descent |
| **Local minimum** | A dip that is not the lowest point overall | The ball can settle in it |
| **Saddle point** | A pass between hills: downhill in some directions, uphill in others | The gradient is near zero, so progress stalls |
| **Plateau** | A wide flat region | Tiny gradients, very slow progress |
| **Ravine** | A long narrow valley | Steps zigzag from wall to wall |

Two balls starting in different places can roll into different valleys, which is why the starting values matter. Surprisingly, in very high dimensions bad local minima are rarer than people feared: with millions of directions, there is almost always some direction still leading down. Saddles and plateaus cause more trouble.

!tool loss-landscape

Rotate the landscape in the lab above, drop balls in different places and change the learning rate and the optimiser. Watch plain gradient descent zigzag down the ravine, and momentum carry a ball through a shallow dip.
"""),
        Section("Momentum and Adam", """
Plain gradient descent forgets its past: each step depends only on the slope right here.

### Momentum

**Momentum** gives the ball a memory, like a heavy ball rolling downhill. It keeps a running **velocity**: the gradients add up while they agree, so the ball speeds along a consistent slope, and zigzags cancel out across a ravine. It can even roll through small dips.

!info Momentum :: velocity ← 0.9 × velocity + gradient, then parameters ← parameters − learning rate × velocity

!diagram ai-momentum

### Adam

**Adam** (adaptive moment estimation, 2014, by Diederik Kingma and Jimmy Ba) combines momentum with a separate, automatically adjusted step size for every parameter: parameters whose gradients are consistently large take smaller steps, and rarely updated ones take larger steps. It is forgiving about the learning rate and is the default optimiser for most deep learning, including large language models, usually in a variant called **AdamW**.
"""),
        Section("Hands-on: gradient descent from scratch", """
### Training the revision model

Level 4 found the best line with a formula: w ≈ 6.52, b ≈ 33.23. Gradient descent should find the same line without one.

```python
hours = [1, 2, 2, 3, 4, 5, 6, 6, 7, 8]
score = [38, 45, 50, 52, 61, 64, 70, 75, 78, 86]
n = len(hours)

w, b = 0.0, 0.0
learning_rate = 0.03

for epoch in range(1, 1001):
    dw = sum(2 * (w * x + b - y) * x for x, y in zip(hours, score)) / n
    db = sum(2 * (w * x + b - y) for x, y in zip(hours, score)) / n
    w -= learning_rate * dw
    b -= learning_rate * db
    if epoch in (1, 2, 5, 10, 50, 100, 500, 1000):
        loss = sum((w * x + b - y) ** 2 for x, y in zip(hours, score)) / n
        print(f"epoch {epoch:4}: w = {w:6.3f}  b = {b:6.3f}  loss = {loss:9.3f}")
```

### Too small, about right, too big

```python
hours = [1, 2, 2, 3, 4, 5, 6, 6, 7, 8]
score = [38, 45, 50, 52, 61, 64, 70, 75, 78, 86]
n = len(hours)

def train(learning_rate, epochs):
    w = b = 0.0
    for _ in range(epochs):
        dw = sum(2 * (w * x + b - y) * x for x, y in zip(hours, score)) / n
        db = sum(2 * (w * x + b - y) for x, y in zip(hours, score)) / n
        w, b = w - learning_rate * dw, b - learning_rate * db
        if abs(w) > 1e6:
            return "exploded!"
    loss = sum((w * x + b - y) ** 2 for x, y in zip(hours, score)) / n
    return f"w = {w:.2f}, b = {b:.2f}, loss = {loss:.2f}"

for lr in [0.001, 0.01, 0.03, 0.05]:
    print(f"learning rate {lr:5}: after 500 epochs {train(lr, 500)}")
```

### Momentum through a ravine

The function f(x, y) = x² + 20y² is a long narrow valley. Compare plain descent with momentum, using the same learning rate and number of steps.

```python
def grad(x, y):
    return 2 * x, 40 * y

def descend(momentum, steps=60, lr=0.01):
    x, y = -9.0, 1.0
    vx = vy = 0.0
    for _ in range(steps):
        gx, gy = grad(x, y)
        vx = momentum * vx + gx
        vy = momentum * vy + gy
        x, y = x - lr * vx, y - lr * vy
    return x, y, x ** 2 + 20 * y ** 2

for m in [0.0, 0.5, 0.9]:
    x, y, f = descend(m)
    print(f"momentum {m}: ended at ({x:7.3f}, {y:7.3f}), loss {f:.5f}")
```

### Try this

1. In the first program, start from w = 20, b = −50. Does it still find the same line?
2. Find the largest learning rate that does not explode. The maths says it is just under 0.04 for this data.
3. In the momentum program, try `lr=0.045`. Plain descent now does well and momentum 0.9 overshoots. Why can too much momentum be a problem?
"""),
        Section("Level check", """
+ Write the gradient descent update and explain each part
+ Describe the effect of a learning rate that is too small and one that is too large
+ Explain batch, stochastic and mini-batch gradient descent, and calculate steps per epoch
+ Interpret training and validation loss curves, and explain early stopping
+ Describe local minima, saddle points, plateaus and ravines
+ Explain how momentum and Adam improve on plain gradient descent
"""),
    ],
    keyterms=[
        ("Gradient descent", "Repeatedly moving the parameters a small step against the gradient of the loss."),
        ("Learning rate", "The hyperparameter that sets how big each gradient descent step is."),
        ("Hyperparameter", "A setting chosen by people rather than learned, such as the learning rate or the batch size."),
        ("Epoch", "One complete pass through the training data."),
        ("Mini-batch", "A small random subset of the training data used to estimate the gradient for one step."),
        ("Stochastic gradient descent", "Gradient descent using the gradient from one example or a small random batch at each step."),
        ("Early stopping", "Stopping training when the validation loss stops improving, and keeping the best parameters."),
        ("Local minimum", "A point lower than everything near it but not the lowest point overall."),
        ("Saddle point", "A point where the gradient is zero but the loss rises in some directions and falls in others."),
        ("Momentum", "An optimiser that keeps a running velocity of past gradients, so steps build up along consistent slopes."),
        ("Adam", "An optimiser combining momentum with an automatically adapted step size for each parameter; the usual default."),
    ],
    mistakes=[
        "Thinking a bigger learning rate always trains faster. Too big and the loss bounces or explodes.",
        "Confusing an epoch with a step. An epoch is a full pass through the data, which may be hundreds of steps.",
        "Stopping as soon as the training loss is low. Watch the validation loss, or the model may be overfitting.",
        "Assuming gradient descent always finds the best possible parameters. It finds a low point near where it started.",
        "Believing the noise in stochastic gradient descent is purely a problem. It also helps the model escape flat regions and generalise.",
    ],
    grade="""
### Why descent works in a billion dimensions

A neural network's loss landscape is not a bowl, and nothing guarantees that gradient descent finds the global minimum. It works in practice for several reasons researchers are still unpicking: in huge dimensions most critical points are saddles rather than traps; heavily over-parameterised networks have vast connected valleys of near-equally good solutions; and the noise of mini-batches steers training towards wide, flat valleys, whose solutions tend to generalise better than those in sharp, narrow ones.

### Second-order methods

Gradient descent uses only the slope. **Newton's method** also uses the curvature (the second derivatives, collected in a matrix called the Hessian) to jump straight towards the bottom of a bowl. For a model with n parameters the Hessian has n² entries, which is impossible for a billion parameters, so deep learning uses cheap approximations of curvature instead. Adam's per-parameter step sizes are one such approximation.
""",
    quiz=[
        Q("What is the gradient descent update for a parameter?",
          ["parameter ← parameter − learning rate × gradient",
           "parameter ← parameter + learning rate × gradient",
           "parameter ← gradient ÷ learning rate",
           "parameter ← learning rate − gradient"], 0,
          "Subtracting moves against the gradient, which points uphill."),
        Q("What happens if the learning rate is far too large?",
          ["Steps overshoot the minimum and the loss bounces or explodes",
           "Training becomes slow but always reaches the minimum",
           "The model stops using its training data altogether",
           "The gradients all become exactly zero at once"], 0,
          "Each step lands higher up the opposite side of the valley than it started."),
        Q("A dataset has 60,000 examples and the batch size is 200. How many steps make one epoch?",
          ["300", "200", "60,000", "12,000,000"], 0,
          "60,000 ÷ 200 = 300 steps to pass through every example once."),
        Q("Which is a hyperparameter?",
          ["The learning rate", "A weight inside the model", "A bias inside the model",
           "The gradient of the loss"], 0,
          "Hyperparameters are set by people before training; weights and biases are learned."),
        Q("Training loss keeps falling but validation loss has started rising. What is happening?",
          ["The model is starting to overfit", "The learning rate is too small",
           "The model is underfitting", "The data has been scaled twice"], 0,
          "It is memorising the training data. Early stopping keeps the parameters from the best validation epoch."),
        Q("What is a saddle point?",
          ["A flat point that is low in some directions and high in others",
           "The lowest point anywhere in the whole loss landscape",
           "A point where the loss becomes infinitely large",
           "The place on the landscape where training always starts"], 0,
          "Like the pass between two hills: downhill in two directions, uphill in two others."),
        Q("Why does mini-batch gradient descent use random batches rather than the whole dataset?",
          ["Each step is far cheaper, and the noise can help training",
           "Using every example would give the wrong gradient",
           "Random batches guarantee the global minimum is found",
           "The whole dataset cannot be stored on any computer"], 0,
          "A batch gives a good-enough estimate of the gradient for a fraction of the cost."),
        Q("How does momentum help in a long narrow ravine?",
          ["Zigzags across the ravine cancel while progress along it builds up",
           "It makes the learning rate larger every step",
           "It stops the model from overfitting the data",
           "It recalculates the gradient on the whole dataset"], 0,
          "The velocity averages recent gradients, so consistent directions add up and alternating ones cancel."),
        Q("What does Adam add to momentum?",
          ["A separately adapted step size for every parameter",
           "A way to find the exact minimum in one step",
           "Labels for data that has none",
           "A second, larger learning rate for the bias"], 0,
          "It scales each parameter's step using a running average of its squared gradients."),
        Q("Two balls start at different points on the same loss landscape. Why might they end in different places?",
          ["They can roll into different valleys", "One of them has a different loss function",
           "Gradient descent is completely random", "Only one can use the training data"], 0,
          "Gradient descent finds a low point near its starting point, so the starting values matter."),
    ],
    exam=[
        EQ("Describe the gradient descent algorithm.", 4,
           [MP("Start with random or initial values for the parameters", ["random", "initial", "start", "zero"]),
            MP("Calculate the gradient of the loss", ["gradient", "derivative", "slope"]),
            MP("Update each parameter by subtracting learning rate × gradient", ["subtract", "minus", "learning rate", "opposite", "against"]),
            MP("Repeat until the loss stops decreasing / converges", ["repeat", "until", "converge", "stops", "many times", "iterat"])],
           "Gradient descent starts with random or initial values for the parameters. It calculates the loss on the training data and the gradient of the loss with respect to each parameter. It then updates every parameter by subtracting the learning rate multiplied by its gradient, a small step downhill. These steps are repeated until the loss stops decreasing, when the parameters have converged near a minimum.",
           command="Describe"),
        EQ("Explain the effect of choosing a learning rate that is too small and one that is too large.", 4,
           [MP("Too small: very small steps", ["small step", "tiny", "too small"]),
            MP("So training is very slow / may not reach the minimum in time", ["slow", "long time", "many epochs", "not reach", "time"]),
            MP("Too large: steps overshoot the minimum", ["overshoot", "jump over", "past the minimum", "too far"]),
            MP("So the loss oscillates or diverges / explodes", ["oscillat", "bounce", "diverge", "explode", "increase"])],
           "If the learning rate is too small, every step is tiny, so training is very slow and may run out of time before reaching the minimum. If it is too large, each step overshoots the minimum and lands on the other side of the valley, so the loss oscillates and can even increase every step until it diverges, or explodes, to enormous values.",
           command="Explain"),
        EQ("A model's training loss falls steadily, while its validation loss falls until epoch 20 and then rises. Explain what is happening and what the engineer should do.", 4,
           [MP("Up to epoch 20 the model learns patterns that generalise", ["generalis", "generaliz", "learning", "both fall"]),
            MP("After epoch 20 it is overfitting / memorising the training data", ["overfit", "memoris", "memoriz", "noise"]),
            MP("Use early stopping", ["early stopping", "stop at", "stop training"]),
            MP("Keep the parameters from epoch 20, the lowest validation loss", ["epoch 20", "lowest validation", "best", "checkpoint"])],
           "Until epoch 20 both losses fall, so the model is learning patterns that generalise to new data. After that the validation loss rises while the training loss keeps falling, which means the model is overfitting: memorising the training examples, including their noise. The engineer should use early stopping, keeping the parameters saved at epoch 20, where the validation loss was lowest, and could also add regularisation or more data.",
           command="Explain"),
    ],
)

TOPICS = [L5_1, L5_2]
