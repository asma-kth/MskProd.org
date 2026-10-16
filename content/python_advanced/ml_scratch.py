"""Advanced Python: machine learning written from scratch."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="machine-learning-from-scratch",
    title="Machine Learning from Scratch",
    spec="Advanced 9",
    icon="i-brain",
    minutes=75,
    blurb="Machine learning with no libraries, so nothing is hidden. Split data into training and test sets, classify with k-nearest neighbours, fit a line by gradient descent, train a perceptron and a small neural network to learn XOR, then measure a model with a confusion matrix and see how bias in the data becomes bias in the answers.",
    fact="The perceptron, the ancestor of every neural network, was demonstrated in 1958 on a machine that filled a room and learned to tell the left of a card from the right. A newspaper reported it as the embryo of a computer that would one day walk, talk and be conscious. The hype faded for decades, but the idea outlasted it.",
    sections=[
        Section("What it means for a machine to learn", r"""
In ordinary programming you write the **rules**, give the program **data**, and it produces **answers**. In **machine learning** you give the program the **data and the answers**, and it works out the **rules** for itself. The rules, once found, are used on new data. That is a **model**.

There are three main kinds:

| Kind | The program is given | Example |
| **Supervised** | examples with the correct answer (a **label**) | photos marked "cat" or "dog", then asked about a new photo |
| **Unsupervised** | data with no answers, and has to find structure | grouping customers by how they shop |
| **Reinforcement** | rewards and penalties for actions it tries | a program learning to play a game |

Supervised learning has two jobs. **Classification** predicts a category (apple or lemon). **Regression** predicts a number (a house price).

The inputs the model looks at are its **features**, and the answer is the **label**. To tell apples from lemons, the features might be weight and sweetness.

### Training and testing

A model that is tested on the examples it learned from will look brilliant, because it may simply have memorised them. What matters is how well it does on data it **has never seen**. So the data is split in two before anything else:

- the **training set**, used to build the model
- the **test set**, kept back, and used once at the end to measure how good the model really is

Here is a made-up fruit data set, with the two kinds of fruit overlapping, as real data does:

```python
import random
from collections import Counter

rng = random.Random(11)

def make_fruit(label, weight, sweetness, count):
    return [((rng.gauss(weight, 25), rng.gauss(sweetness, 0.8)), label) for _ in range(count)]

data = make_fruit("apple", 150, 7, 60) + make_fruit("lemon", 150, 4, 60)
rng.shuffle(data)

train, test = data[:80], data[80:]

for features, label in data[:4]:
    print([round(f, 1) for f in features], label)
print(len(train), "examples to learn from,", len(test), "kept back to test")

majority = Counter(label for _, label in train).most_common(1)[0][0]
guess_rate = sum(label == majority for _, label in test) / len(test)
print("always guessing", majority, "is right", round(guess_rate * 100), "% of the time")
```

That last line is the **baseline**: what you would score by always giving the most common answer. A model that cannot beat it has learned nothing.

!key Never test on training data :: If the same data is used to build and to judge, you cannot tell learning from memorising. The test set must be kept apart and used only to judge the finished model.
"""),
        Section("k-nearest neighbours", r"""
The simplest classifier needs no training at all. To classify a new item, **find the k items in the training set that are most similar to it, and let them vote**. This is **k-nearest neighbours** (k-NN).

1. Measure the **distance** from the new item to every training item. For two features this is the ordinary distance on a graph (Euclidean distance), which `math.dist` gives.
2. Take the `k` nearest.
3. The most common label among them is the prediction.

```python
import math
import random
from collections import Counter

rng = random.Random(11)

def make_fruit(label, weight, sweetness, count):
    return [((rng.gauss(weight, 25), rng.gauss(sweetness, 0.8)), label) for _ in range(count)]

data = make_fruit("apple", 150, 7, 60) + make_fruit("lemon", 150, 4, 60)
rng.shuffle(data)
train, test = data[:80], data[80:]

def knn_predict(train, point, k):
    nearest = sorted(train, key=lambda item: math.dist(item[0], point))[:k]
    return Counter(label for _, label in nearest).most_common(1)[0][0]

def accuracy(train, test, k):
    right = sum(knn_predict(train, point, k) == label for point, label in test)
    return right / len(test)

print("k   accuracy on the test set")
for k in (1, 3, 5, 9, 15):
    print(str(k).ljust(3), accuracy(train, test, k))
```

The results look odd: more neighbours make it **worse**. The reason is the features. Weight is measured in grams and varies by tens, and sweetness varies by one or two. The distance is dominated by weight, which does not help tell the fruits apart, and drowns out sweetness, which does. The remedy is **feature scaling**: squash every feature into the same range, here 0 to 1, using the training data's minimum and maximum.

```python
import math
import random
from collections import Counter

rng = random.Random(11)

def make_fruit(label, weight, sweetness, count):
    return [((rng.gauss(weight, 25), rng.gauss(sweetness, 0.8)), label) for _ in range(count)]

data = make_fruit("apple", 150, 7, 60) + make_fruit("lemon", 150, 4, 60)
rng.shuffle(data)
train, test = data[:80], data[80:]

def knn_predict(train, point, k):
    nearest = sorted(train, key=lambda item: math.dist(item[0], point))[:k]
    return Counter(label for _, label in nearest).most_common(1)[0][0]

def accuracy(train, test, k):
    return sum(knn_predict(train, point, k) == label for point, label in test) / len(test)

lows = [min(point[i] for point, _ in train) for i in range(2)]
highs = [max(point[i] for point, _ in train) for i in range(2)]

def rescale(point):
    return tuple((point[i] - lows[i]) / (highs[i] - lows[i]) for i in range(2))

train_scaled = [(rescale(point), label) for point, label in train]
test_scaled = [(rescale(point), label) for point, label in test]

print("k   accuracy with scaled features")
for k in (1, 3, 5, 9, 15):
    print(str(k).ljust(3), accuracy(train_scaled, test_scaled, k))

print()
print("k = 1 on the data it learned from:", accuracy(train_scaled, train_scaled, 1))
print("k = 1 on data it has not seen:    ", accuracy(train_scaled, test_scaled, 1))
```

Now more neighbours helps, and accuracy reaches about 97%.

The last two lines show **overfitting**. With `k = 1`, every training item is its own nearest neighbour, so the model scores 100% on the data it has seen. It has memorised, noise and all, and scores lower on new data. A good model **generalises**: it learns the pattern, not the particular examples. Larger k smooths over the noise.

| | k-NN |
| Training | none: it just stores the data |
| Predicting | slow: it measures the distance to every stored item |
| Needs | scaled features, and a choice of k |
| Good for | small data sets, and as a first baseline |
"""),
        Section("Fitting a line by gradient descent", r"""
**Regression** predicts a number. The simplest model is a straight line, `y = m * x + c`, and learning means finding the best **m** (the slope) and **c** (the intercept).

"Best" needs to be made precise. For every example, the **error** is the prediction minus the true value. The **cost** is the average of the squared errors (the **mean squared error**). Squaring makes every error positive, and punishes big ones. Learning is the search for the m and c with the smallest cost.

**Gradient descent** finds it by walking downhill. Think of the cost as a landscape over every possible (m, c). From where you stand, work out which direction is steepest *uphill* (the **gradient**) and take a step the other way. Repeat. The size of each step is the **learning rate**.

```python
import random
import statistics

rng = random.Random(5)
xs = [x / 10 for x in range(50)]
ys = [2 * x + 1 + rng.gauss(0, 0.3) for x in xs]       # the truth is y = 2x + 1, plus noise

def fit(xs, ys, rate, steps):
    m = c = 0.0
    n = len(xs)
    costs = []
    for _ in range(steps):
        errors = [(m * x + c) - y for x, y in zip(xs, ys)]
        costs.append(sum(e * e for e in errors) / n)
        gradient_m = 2 / n * sum(e * x for e, x in zip(errors, xs))
        gradient_c = 2 / n * sum(errors)
        m -= rate * gradient_m                          # a step downhill
        c -= rate * gradient_c
    return m, c, costs

print("rate     slope  intercept   first cost   last cost")
for rate in (0.001, 0.02, 0.1):
    m, c, costs = fit(xs, ys, rate, 500)
    print(str(rate).ljust(8), round(m, 3), round(c, 3), "     ", "%.4g" % costs[0], "      ", "%.4g" % costs[-1])

exact = statistics.linear_regression(xs, ys)
print("exact answer:", round(exact.slope, 3), round(exact.intercept, 3))
```

Three learning rates, three behaviours. At `0.001` the steps are tiny, and after 500 of them it has not yet arrived. At `0.02` and `0.1` it has reached the same answer as the exact method, a slope close to 2 and an intercept close to 1, which is the line the data was made from, blurred by noise. Gradient descent is not needed for a straight line, as there is a formula, but the same loop trains every neural network, including those with billions of numbers to find.

What if the steps are too big?

```python
import random

rng = random.Random(5)
xs = [x / 10 for x in range(50)]
ys = [2 * x + 1 + rng.gauss(0, 0.3) for x in xs]

def final_cost(rate, steps):
    m = c = 0.0
    n = len(xs)
    cost = 0.0
    for _ in range(steps):
        errors = [(m * x + c) - y for x, y in zip(xs, ys)]
        cost = sum(e * e for e in errors) / n
        m -= rate * 2 / n * sum(e * x for e, x in zip(errors, xs))
        c -= rate * 2 / n * sum(errors)
    return cost

for steps in (1, 10, 30, 60):
    print(steps, "steps at a rate of 0.2 -> cost", "%.4g" % final_cost(0.2, steps))
```

It leaps from one side of the valley to the other, each time higher. The cost **explodes** instead of shrinking. Choosing the learning rate is one of the first jobs in training any model: too small and it is slow, too large and it never settles.
"""),
        Section("The perceptron and a small neural network", r"""
A **neuron** in a neural network is a very small calculation. It takes some inputs, multiplies each by a **weight**, adds them up with a **bias**, and passes the total through an **activation function**:

`output = activation(w1 * x1 + w2 * x2 + bias)`

In the **perceptron**, the activation is a simple threshold: if the total is above zero, the output is 1, otherwise 0. **Learning** means adjusting the weights. After each example, if the answer was wrong, nudge every weight in the direction that would have made it more right:

`weight = weight + rate * error * input`

```python
def train_perceptron(samples, epochs=20, rate=0.1):
    w = [0.0, 0.0]
    bias = 0.0
    for _ in range(epochs):
        for (x1, x2), target in samples:
            output = 1 if w[0] * x1 + w[1] * x2 + bias > 0 else 0
            error = target - output
            w[0] += rate * error * x1
            w[1] += rate * error * x2
            bias += rate * error
    return w, bias

def predict(w, bias, x1, x2):
    return 1 if w[0] * x1 + w[1] * x2 + bias > 0 else 0

inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
for name, targets in (("AND", [0, 0, 0, 1]), ("OR", [0, 1, 1, 1]), ("XOR", [0, 1, 1, 0])):
    w, bias = train_perceptron(list(zip(inputs, targets)))
    answers = [predict(w, bias, *point) for point in inputs]
    print(name, "wanted", targets, "got", answers, "-> correct" if answers == targets else "-> WRONG")
```

The perceptron learned AND and OR, and **cannot** learn XOR (exclusive or: one or the other but not both), however long it trains. A single neuron draws one straight line to separate the 0s from the 1s, and for XOR no straight line can do it. The problem is **not linearly separable**. This limit, shown in 1969, nearly ended research into neural networks.

### Adding a hidden layer

The fix is to add a **hidden layer** of neurons between the inputs and the output. Each hidden neuron draws its own line, and the output neuron combines them, so the network can make curved boundaries. Two things change:

- the activation becomes the smooth **sigmoid**, `1 / (1 + e^-x)`, which gives a value between 0 and 1 and has a slope that can be calculated
- the weights are learned by **backpropagation**: work out the error at the output, then use the chain rule from calculus to share the blame backwards, finding how much each weight contributed to it. Then nudge each weight downhill, as in gradient descent.

This is a network with two inputs, two hidden neurons and one output, trained on XOR:

```python
import math
import random

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def train_xor(seed, epochs=3000, rate=0.5):
    r = random.Random(seed)
    w1 = [[r.uniform(-1, 1) for _ in range(2)] for _ in range(2)]     # input -> hidden weights
    b1 = [0.0, 0.0]
    w2 = [r.uniform(-1, 1) for _ in range(2)]                         # hidden -> output weights
    b2 = 0.0
    examples = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)]

    for _ in range(epochs):
        for (x1, x2), target in examples:
            hidden = [sigmoid(w1[j][0] * x1 + w1[j][1] * x2 + b1[j]) for j in range(2)]
            output = sigmoid(w2[0] * hidden[0] + w2[1] * hidden[1] + b2)

            d_output = (output - target) * output * (1 - output)       # error at the output
            for j in range(2):
                d_hidden = d_output * w2[j] * hidden[j] * (1 - hidden[j])   # blame passed back
                w2[j] -= rate * d_output * hidden[j]
                w1[j][0] -= rate * d_hidden * x1
                w1[j][1] -= rate * d_hidden * x2
                b1[j] -= rate * d_hidden
            b2 -= rate * d_output

    def run(x1, x2):
        hidden = [sigmoid(w1[j][0] * x1 + w1[j][1] * x2 + b1[j]) for j in range(2)]
        return sigmoid(w2[0] * hidden[0] + w2[1] * hidden[1] + b2)
    return run

points = [(0, 0), (0, 1), (1, 0), (1, 1)]
print("seed   outputs for (0,0) (0,1) (1,0) (1,1)")
learned = 0
for seed in range(1, 6):
    run = train_xor(seed)
    answers = [round(run(*p), 2) for p in points]
    ok = answers[0] < 0.1 and answers[1] > 0.9 and answers[2] > 0.9 and answers[3] < 0.1
    learned += ok
    print(str(seed).ljust(6), answers, "learned" if ok else "stuck")
print(learned, "of 5 starts learned XOR")
```

The outputs are close to 0, 1, 1, 0: the network has solved the problem the perceptron could not. Notice that one of the five starting points got **stuck**, with outputs near 0.5 for two of the cases. Training starts from random weights, and gradient descent can settle in a **local minimum**, a valley that is not the deepest one. That is why real training is usually repeated, and why results can differ between runs.

!key What the network "knows" :: It is only the nine numbers, six weights and three biases. There is no rule for XOR in the code anywhere. The knowledge is in the **weights**, found by trial and correction. A large network is the same idea, with billions of weights.
"""),
        Section("Measuring a model, and being fair", r"""
### More than accuracy

**Accuracy**, the fraction of answers that were right, can be very misleading. Suppose 5 patients in 100 have a disease, and a "test" always says *healthy*. It is 95% accurate and **finds nobody**. When one outcome is rare, you need to see *what kind* of mistakes were made. They are laid out in a **confusion matrix**, with one class taken as "positive":

| | Predicted positive | Predicted negative |
| **Actually positive** | true positive (TP) | false negative (FN): missed |
| **Actually negative** | false positive (FP): false alarm | true negative (TN) |

- **accuracy** = (TP + TN) / everything
- **precision** = TP / (TP + FP): *of those it flagged, how many were right?*
- **recall** = TP / (TP + FN): *of the real ones, how many did it find?*

Which matters more depends on the cost of each mistake. For a cancer screening, a missed case (low recall) is far worse than a false alarm. For a spam filter, deleting a real email (a false positive) is worse than letting some spam through.

```python
import math
import random
from collections import Counter

rng = random.Random(11)

def make_fruit(label, weight, sweetness, count):
    return [((rng.gauss(weight, 25), rng.gauss(sweetness, 0.8)), label) for _ in range(count)]

data = make_fruit("apple", 150, 7, 60) + make_fruit("lemon", 150, 4, 60)
rng.shuffle(data)
train, test = data[:80], data[80:]

lows = [min(point[i] for point, _ in train) for i in range(2)]
highs = [max(point[i] for point, _ in train) for i in range(2)]

def rescale(point):
    return tuple((point[i] - lows[i]) / (highs[i] - lows[i]) for i in range(2))

train = [(rescale(point), label) for point, label in train]
test = [(rescale(point), label) for point, label in test]

def knn_predict(point, k=5):
    nearest = sorted(train, key=lambda item: math.dist(item[0], point))[:k]
    return Counter(label for _, label in nearest).most_common(1)[0][0]

tp = fp = fn = tn = 0
for point, label in test:
    guess = knn_predict(point)
    if guess == "lemon" and label == "lemon":
        tp += 1
    elif guess == "lemon":
        fp += 1
    elif label == "lemon":
        fn += 1
    else:
        tn += 1

print("true positives", tp, "| false positives", fp, "| false negatives", fn, "| true negatives", tn)
print("accuracy ", (tp + tn) / (tp + fp + fn + tn))
print("precision", round(tp / (tp + fp), 3))
print("recall   ", round(tp / (tp + fn), 3))

# the accuracy paradox: 5 sick patients in 100, and a test that always says healthy
actual = [1] * 5 + [0] * 95
predicted = [0] * 100
accuracy = sum(a == p for a, p in zip(actual, predicted)) / 100
found = sum(1 for a, p in zip(actual, predicted) if a == 1 and p == 1)
print()
print("always saying healthy: accuracy", accuracy, "| patients found", found, "of 5")
```

### Bias in, bias out

A model learns from the data it is given, so it learns every unfairness in it. It has no way of knowing which patterns are real and which are accidents of who was included. Here, a bank trains a model on past loans, and the group B customers, who are a small minority, repay with less income than group A:

```python
def make_people():
    people = []
    for i in range(90):                         # group A: 90 people
        income = 5 + i * 0.55
        people.append(("A", income, income > 30))
    for i in range(10):                         # group B: only 10 people, who repay from a lower income
        income = 5 + i * 5.5
        people.append(("B", income, income > 15))
    return people                               # (group, income, would repay)

people = make_people()

def best_threshold(people):
    best = None
    for candidate in (x / 2 for x in range(0, 120)):
        correct = sum((income > candidate) == repays for _, income, repays in people)
        if best is None or correct > best[1]:
            best = (candidate, correct)
    return best

threshold, correct = best_threshold(people)
print("the model learned: approve if income is above", threshold)
print("overall accuracy:", correct / len(people))
for group in "AB":
    members = [p for p in people if p[0] == group]
    right = sum((income > threshold) == repays for _, income, repays in members)
    print("group", group, ":", right, "of", len(members), "decisions correct")
```

The model is 97% accurate, which sounds excellent, and it is wrong about **three in ten** of group B. Group A dominated the data, so the model fitted group A. The average hid it. This is why a model should be evaluated **separately for each group** it affects.

### Responsible machine learning

| Issue | The risk | A response |
| **Biased data** | the model repeats and amplifies past unfairness | check who is in the data; test each group separately |
| **Lack of explanation** | nobody can say why a decision was made, which is a problem if someone is refused a loan | prefer simple models where it matters; give reasons |
| **Privacy** | models are trained on personal data, and can leak it | collect only what is needed; follow data protection law |
| **Wrong use** | a model built for one purpose is used for another | document what it is for |
| **Accountability** | who is responsible when it is wrong? | keep a human responsible, and a way to challenge decisions |
| **Energy** | training a large model can use as much electricity as a small town | use the smallest model that does the job |

!exam Discuss with both sides :: Questions on machine learning decisions reward a benefit (speed, consistency, scale) and a risk (bias from the training data, no explanation, privacy), applied to the scenario in the question, with a reasoned conclusion.
"""),
    ],
    keyterms=[
        ("Machine learning", "Programs that find their own rules from data, instead of being given the rules by a programmer."),
        ("Supervised learning", "Learning from examples that have been labelled with the correct answer."),
        ("Unsupervised learning", "Finding structure in data that has no labels."),
        ("Feature and label", "A feature is an input the model looks at. The label is the answer it is trying to predict."),
        ("Training and test sets", "The data used to build the model, and the separate data kept back to measure how well it works on new examples."),
        ("Overfitting", "When a model fits its training data, including the noise, so well that it does badly on new data."),
        ("k-nearest neighbours", "A classifier that gives a new item the most common label among the k most similar items in the training data."),
        ("Gradient descent", "Repeatedly changing the parameters of a model a small step in the direction that reduces its error."),
        ("Learning rate", "The size of each step in gradient descent."),
        ("Perceptron", "A single artificial neuron that outputs 1 if the weighted sum of its inputs plus a bias is above zero."),
        ("Backpropagation", "Calculating how much each weight in a neural network contributed to the error, so that every weight can be adjusted."),
        ("Confusion matrix", "A table of true and false positives and negatives that shows what kind of mistakes a classifier makes."),
        ("Precision and recall", "The fraction of the items flagged that were right, and the fraction of the real items that were found."),
    ],
    grade="""
Machine learning questions combine definitions with judgment about data and fairness.

+ Define supervised and unsupervised learning by what is provided: labelled examples, or none
+ Say why there are separate training and test sets: to measure performance on data the model has not seen
+ For overfitting, say the model learned the noise and does worse on new data
+ For a metric, give the formula and say which mistake it counts: precision for false alarms, recall for misses
+ For ethics, link bias in the output to bias in the training data, and suggest a check
""",
    mistakes=[
        "Testing a model on the data that it was trained on, and reporting that accuracy as if it were the real performance.",
        "Judging a model by accuracy alone when one outcome is rare.",
        "Using unscaled features in k-nearest neighbours, so that one feature drowns out the others.",
        "Setting a learning rate so large that gradient descent diverges.",
        "Saying a model is unbiased because it is run by a computer. It learns whatever is in its training data.",
    ],
    quiz=[
        Q("What is the difference between supervised and unsupervised learning?",
          ["Supervised uses labelled examples; unsupervised has no labels", "Supervised needs a human watching the program run", "Unsupervised is faster", "Supervised only works with numbers"], 0,
          "A supervised model is given the right answers to learn from. An unsupervised one has to find structure on its own."),
        Q("Why is data split into a training set and a test set?",
          ["To measure how well the model works on data it has not seen", "To make the program run twice as fast", "To store the data in two places", "To stop the data being copied"], 0,
          "Testing on the training data would only show how well it had memorised."),
        Q("What is overfitting?",
          ["The model fits the training data, noise included, so does badly on new data", "The model is too small to learn anything", "The training takes too long", "The test set is too large"], 0,
          "It has memorised instead of generalising."),
        Q("How does the k-nearest neighbours algorithm classify a new item?",
          ["By the most common label among the k closest items in the training data", "By drawing a straight line through the data", "By choosing the label at random", "By averaging all the labels"], 0,
          "The k nearest neighbours vote."),
        Q("Why should features be scaled before using k-nearest neighbours?",
          ["So that a feature with large values does not dominate the distance", "To make the labels numbers", "To reduce the amount of data", "To remove the test set"], 0,
          "Weight in grams would otherwise swamp sweetness measured from 1 to 10."),
        Q("In gradient descent, what happens if the learning rate is too large?",
          ["The steps overshoot, and the error can grow instead of shrinking", "It takes a bit longer", "It finds the answer faster", "It gives exactly the same answer"], 0,
          "Each step jumps past the lowest point, sometimes landing higher than before."),
        Q("Why can a single perceptron not learn XOR?",
          ["The two classes cannot be separated by a single straight line", "It has too many inputs", "XOR needs a negative number", "A perceptron cannot learn anything"], 0,
          "XOR is not linearly separable. A hidden layer is needed."),
        Q("What does a model with a precision of 0.9 tell you?",
          ["Nine in ten of the items it flagged as positive really were", "It found nine in ten of all the positives", "It is right nine times in ten about everything", "It was trained on 90 items"], 0,
          "Precision is TP / (TP + FP): how many of the alarms were real."),
        Q("A disease test always says 'healthy'. Only 5 in 100 people are ill. What is wrong with saying the test is 95% accurate?",
          ["The accuracy is high but the test finds none of the ill patients (recall 0)", "The accuracy is actually 5%", "Accuracy cannot be calculated", "There is nothing wrong"], 0,
          "Accuracy hides the fact that every positive case was missed."),
        Q("A loan model is accurate overall but wrong far more often for a small group. What is the most likely cause?",
          ["The small group was under-represented in the training data", "The computer made a calculation error", "The model was too complicated", "The learning rate was too low"], 0,
          "The model fitted the majority, and the overall accuracy hid the poor results for the minority."),
    ],
    exam=[
        EQ("Explain the difference between supervised learning and unsupervised learning.", 4, [
            MP("In supervised learning the training data is labelled with the correct answers", ["labelled", "labels", "correct answers", "known answers", "labelled data"]),
            MP("The model learns the link between the inputs and the labels so it can predict the label for new data", ["predict", "new data", "link", "learns", "relationship"]),
            MP("In unsupervised learning the data has no labels", ["no labels", "unlabelled", "not labelled", "without labels"]),
            MP("The model finds patterns or groups (such as clusters) in the data by itself", ["patterns", "groups", "clusters", "structure", "by itself"]),
        ], "In supervised learning the training data is labelled with the correct answers, and the model learns the relationship between the inputs and the labels so that it can predict the label for new data. In unsupervised learning the data has no labels, and the model finds patterns or groups, such as clusters, in the data by itself.",
           command="Explain"),
        EQ("Explain why the data used to train a machine learning model is kept separate from the data used to test it.", 3, [
            MP("The test data has not been seen by the model", ["not seen", "new data", "unseen", "not used to train", "has not been"]),
            MP("So it shows how well the model works on new data (how well it generalises)", ["generalise", "new data", "real", "performance", "how well"]),
            MP("Testing on the training data could hide overfitting, where the model has only memorised the examples", ["overfit", "memoris", "memoriz", "hide", "learned the noise"]),
        ], "The test data has not been seen by the model while it was being trained, so the results show how well the model will work on new data, which is how well it generalises. If the model was tested on the data it was trained on, the result could hide overfitting, where the model has only memorised the training examples and would do badly on new data.",
           command="Explain"),
        EQ("A classifier is tested on 200 items. The confusion matrix is shown. Calculate the accuracy, the precision and the recall of the classifier. Show your working.", 4, [
            MP("Accuracy = (40 + 130) / 200 = 0.85 (85%)", ["0.85", "85%", "170 / 200", "170/200"]),
            MP("Precision = TP / (TP + FP) = 40 / 50", ["tp / (tp + fp)", "40 / 50", "40/50", "true positives"]),
            MP("Precision = 0.8 (80%)", ["0.8", "80%"]),
            MP("Recall = TP / (TP + FN) = 40 / 60 = 0.67 (66.7%)", ["0.67", "66.7", "40 / 60", "40/60", "0.666"]),
        ], "The accuracy is the number of correct answers divided by the total, (40 + 130) / 200 = 170 / 200 = 0.85, or 85%. The precision is TP / (TP + FP) = 40 / (40 + 10) = 40 / 50 = 0.8, or 80%. The recall is TP / (TP + FN) = 40 / (40 + 20) = 40 / 60 = 0.67, or 66.7%.",
           command="Calculate",
           figure="""```text
                      predicted positive   predicted negative
actually positive           40                   20
actually negative           10                  130
```"""),
        EQ("Describe how the k-nearest neighbours algorithm decides which class a new item belongs to.", 4, [
            MP("The distance from the new item to every item in the training data is calculated", ["distance", "every item", "all the items", "measure"]),
            MP("The k items that are closest (the nearest neighbours) are selected", ["closest", "nearest", "k items", "k neighbours", "selected"]),
            MP("The class of each of those k items is counted", ["count", "class of each", "vote", "labels"]),
            MP("The new item is given the class that is most common among them (majority vote)", ["most common", "majority", "most frequent", "most votes", "assigned"]),
        ], "The distance from the new item to every item in the training data is calculated, using the values of its features. The k items that are closest to it, its nearest neighbours, are selected. The class of each of those k items is counted, like a vote, and the new item is given the class that is most common among them.",
           command="Describe"),
        EQ("A bank wants to use a machine learning model to decide automatically whether to approve loans. Discuss the benefits and the ethical issues of doing so.", 6, [
            MP("Decisions can be made very quickly, and for a large number of applications, at low cost", ["quick", "fast", "large number", "scale", "cost", "efficient"]),
            MP("The model is consistent, applying the same rule to every applicant without tiredness or personal prejudice", ["consistent", "same rule", "tired", "personal", "human error"]),
            MP("The model learns from past data, so any bias in the data (such as unfair past decisions or too few people from some groups) is copied into its decisions", ["bias", "past data", "training data", "unfair", "under-represent", "discriminat"]),
            MP("It may be very hard to explain why a person was refused, so they cannot challenge or understand the decision", ["explain", "reason", "challenge", "understand", "transparent", "black box"]),
            MP("Personal data is used, which raises privacy and data protection issues", ["privacy", "personal data", "data protection", "gdpr"]),
            MP("A reasoned conclusion: it can be used, provided the model is tested for fairness for each group and a human can review and overturn decisions", ["conclusion", "tested for fairness", "human", "review", "overall", "provided", "i would"]),
        ], "The model could make decisions very quickly for a large number of applications at a low cost, and it would apply the same rule to every applicant, without tiredness or personal prejudice. However, it learns from past data, so any bias in that data, such as unfair earlier decisions or too few examples from some groups of people, would be copied into its decisions. It may also be very hard to explain why a particular person was refused, so they could not understand or challenge the decision, and the model uses a great deal of personal data, which raises privacy and data protection issues. The bank could use it, provided that the model is tested for fairness for each group of people, and that a person is able to review and overturn its decisions.",
           command="Discuss"),
    ],
)
