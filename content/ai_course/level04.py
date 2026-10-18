"""Level 4: Classic Machine Learning. Regression, classification and clustering."""
from mskbuild.models import Topic, Section, Q, EQ, MP

NEA = "Check you could explain this"

L4_1 = Topic(
    slug="regression",
    title="Regression: Predicting Numbers with a Line",
    spec="4.1",
    icon="i-chart",
    minutes=36,
    exam_title=NEA,
    blurb="Your first real model: a straight line with two parameters. How to measure its errors, find the best line by least squares, extend it to many features, and recognise underfitting and overfitting.",
    fact="The method of least squares was published by Adrien-Marie Legendre in 1805, and Carl Friedrich Gauss used it to predict where the lost dwarf planet Ceres would reappear in the sky. Every regression model since is a descendant of that prediction.",
    sections=[
        Section("The problem: predict a number", """
Ten students recorded their hours of revision and their test score. Can we predict the score of a student who revises for 4.5 hours?

!diagram ai-regression-line

The simplest model is a straight line:

!info The linear model :: predicted score = **w** × hours + **b**

- **w** is the **weight**, or slope: how many extra marks each hour of revision is worth.
- **b** is the **bias**, or intercept: the predicted score for zero hours.

These two numbers are the model's **parameters**. Learning means finding the values of w and b that make the line fit the data best. Once we have them, prediction is one multiplication and one addition, which is why linear models are still everywhere: they are fast, cheap and easy to explain.

!key Regression predicts a number :: The name comes from Francis Galton, who noticed in the 1880s that very tall parents tended to have children closer to average height: their heights "regressed" towards the mean. The name stuck to the method.
"""),
        Section("Measuring error: residuals and mean squared error", """
For each student, the **residual** is the actual score minus the predicted score. In the diagram above, residuals are the coloured vertical sticks between each point and the line.

To score a line we need one number for all the residuals together. Adding them does not work, because positive and negative residuals cancel out. So we square them first:

!info Mean squared error :: MSE = the average of (actual − predicted)²

| Hours | Actual | Predicted | Residual | Squared |
| 2 | 50 | 46.3 | 3.7 | 13.7 |
| 4 | 61 | 59.3 | 1.7 | 2.9 |
| 7 | 78 | 78.8 | −0.8 | 0.6 |

The MSE of these three is (13.7 + 2.9 + 0.6) ÷ 3 ≈ 5.7.

### Why square?

- Squares are never negative, so errors cannot cancel.
- Squaring punishes big errors much more than small ones: an error of 10 costs 100, but two errors of 5 cost only 50.
- The maths of squares is smooth, which makes the best line easy to find.

Two relatives: the **root mean squared error** (RMSE) is the square root of the MSE, back in the original units (marks), and the **mean absolute error** (MAE) averages the sizes of the residuals without squaring, so it is less affected by a few big misses.
"""),
        Section("Finding the best line: least squares", """
The **least squares** line is the one with the smallest possible MSE. For a single feature there is an exact formula:

!info Least squares :: w = Σ(x − x̄)(y − ȳ) ÷ Σ(x − x̄)²   and   b = ȳ − w × x̄

Here x̄ and ȳ are the mean of the hours and the mean of the scores, and Σ means "add up over every student". The top of the fraction measures how hours and scores vary **together**; the bottom measures how much the hours vary on their own. The formula for b guarantees the line passes through the point (x̄, ȳ).

For the ten students this gives **w ≈ 6.52** and **b ≈ 33.2**: every hour of revision is worth about six and a half marks, and a student who did none would be predicted 33.

!tool correlation-lab

Drag a point far from the others in the lab above and watch the line swing towards it. Squaring makes least squares very sensitive to **outliers**.

!warn Formulas run out :: An exact formula like this exists only for simple models. For a neural network with millions of parameters there is none, so we search for good values step by step instead. That search, gradient descent, is Level 5.
"""),
        Section("More features: planes and hyperplanes", """
House prices depend on more than one thing. With several features, the model gives each one its own weight:

!info Multiple linear regression :: price = w₁ × floor area + w₂ × bedrooms + w₃ × distance to station + b

With two features the model is no longer a line but a flat **plane** floating above the floor of a 3D graph, and least squares tilts it to pass as close as possible to all the points.

!diagram ai-regression-plane

With more than two features the plane becomes a **hyperplane**, which we cannot picture but which the maths handles exactly the same way. A model with 500 features has 500 weights and one bias.

### Reading the weights

If w₁ = 2,100, each extra square metre adds about £2,100 to the predicted price, **with the other features held fixed**. A negative weight on distance means homes further from the station are predicted to be cheaper. Weights can only be compared with each other if the features were scaled first (Level 3).
"""),
        Section("Curves, underfitting and overfitting", """
Real relationships are often curved. A trick keeps the model linear in its parameters while letting it bend: add **powers** of a feature as new features, such as hours² and hours³. This is **polynomial regression**.

But flexibility is dangerous.

!diagram ai-fit-three

| | Underfitting | Good fit | Overfitting |
| Model | Too simple | Right complexity | Too complex |
| Training error | High | Low | Very low, even zero |
| Test error | High | Low | High |
| What it learned | Not even the main pattern | The pattern | The pattern **and the noise** |

An overfitted model has memorised its training examples, including their random noise, so it fails on new data. This tension is the **bias-variance trade-off**: simple models are consistently wrong (high bias), while very flexible models change wildly with each sample of data (high variance).

### Regularisation

**Regularisation** adds a penalty for large weights to the error being minimised, so the model only uses big weights when the data really demands them. **Ridge regression** penalises the sum of squared weights; **lasso** penalises the sum of their sizes and tends to set useless weights to exactly zero. The same idea, called weight decay, is used to train neural networks.
"""),
        Section("Judging a regression model", """
| Measure | Meaning | Good value |
| **MAE** | Average size of the errors, in the original units | Small |
| **RMSE** | Like MAE but punishes big errors more; same units | Small |
| **R²** | The fraction of the variation in y the model explains: 1 − MSE ÷ variance of y | Close to 1 |

R² compares the model with the laziest possible baseline: always predicting the mean. R² = 0 means no better than the mean, R² = 1 means perfect, and a negative R² means worse than just guessing the average.

!key Always compare with a baseline :: An RMSE of 2 marks sounds good. It is excellent if scores vary by 40 marks and useless if they vary by 3. Report the baseline beside the model.

Finally, plot the residuals. If they show a pattern, such as a curve or a funnel shape, the model has missed something systematic.
"""),
        Section("Hands-on: build a regression model from scratch", """
### Least squares, by hand

```python
hours = [1, 2, 2, 3, 4, 5, 6, 6, 7, 8]
score = [38, 45, 50, 52, 61, 64, 70, 75, 78, 86]

n = len(hours)
mean_x = sum(hours) / n
mean_y = sum(score) / n
w = (sum((x - mean_x) * (y - mean_y) for x, y in zip(hours, score))
     / sum((x - mean_x) ** 2 for x in hours))
b = mean_y - w * mean_x
print(f"Model: score = {w:.2f} x hours + {b:.2f}")
print(f"Prediction for 4.5 hours: {w * 4.5 + b:.1f}")

predicted = [w * x + b for x in hours]
mse = sum((y - p) ** 2 for y, p in zip(score, predicted)) / n
mae = sum(abs(y - p) for y, p in zip(score, predicted)) / n
baseline = sum((y - mean_y) ** 2 for y in score) / n      # MSE of always guessing the mean
print(f"MSE {mse:.2f}, RMSE {mse ** 0.5:.2f}, MAE {mae:.2f}")
print(f"Baseline MSE {baseline:.2f}, so R squared = {1 - mse / baseline:.3f}")
```

### Overfitting, caught in the act

A "memoriser" predicts the score of whichever training student revised the most similar number of hours. On its own training data it is perfect. Watch what happens on students it has not seen.

```python
train = [(1, 38), (2, 45), (3, 52), (5, 64), (6, 70), (7, 78), (8, 86)]
test = [(2, 50), (4, 61), (6, 75)]

def fit_line(data):
    n = len(data)
    mx = sum(x for x, y in data) / n
    my = sum(y for x, y in data) / n
    w = sum((x - mx) * (y - my) for x, y in data) / sum((x - mx) ** 2 for x, y in data)
    return w, my - w * mx

w, b = fit_line(train)

def line(x):
    return w * x + b

def memoriser(x):
    nearest = min(train, key=lambda pair: abs(pair[0] - x))
    return nearest[1]

def mse(model, data):
    return sum((y - model(x)) ** 2 for x, y in data) / len(data)

for name, model in [("line", line), ("memoriser", memoriser)]:
    print(f"{name:10} training MSE {mse(model, train):6.2f}   test MSE {mse(model, test):6.2f}")
```

The memoriser's training error is zero and its test error is several times the line's. A perfect training score is a warning sign, not a triumph.

### Try this

1. Add a student who revised 10 hours and scored 20, then refit. How far does the line move?
2. Change the memoriser to average its **two** nearest students. Does it overfit less?
"""),
        Section("Level check", """
+ Write the equation of a linear model and explain what w and b mean
+ Calculate residuals and the mean squared error for a few points
+ Explain why errors are squared, and what RMSE, MAE and R² measure
+ Use the least squares formulas, and explain why the line passes through the mean point
+ Describe a model with several features as a plane or hyperplane, and interpret a weight
+ Explain underfitting, overfitting and how regularisation helps
"""),
    ],
    keyterms=[
        ("Regression", "Predicting a number, such as a price or a score."),
        ("Weight (slope)", "The number a feature is multiplied by in a linear model; how much the prediction changes per unit of the feature."),
        ("Bias (intercept)", "The constant added in a linear model; the prediction when every feature is zero."),
        ("Residual", "The actual value minus the predicted value for one example."),
        ("Mean squared error (MSE)", "The average of the squared residuals, the most common measure of regression error."),
        ("Least squares", "Choosing the parameters that make the sum of squared residuals as small as possible."),
        ("R²", "The fraction of the variation in the target explained by the model, compared with always predicting the mean."),
        ("Hyperplane", "The flat surface a linear model forms when it has more than two features."),
        ("Overfitting", "Learning the noise in the training data as well as the pattern, so the model does badly on new data."),
        ("Underfitting", "A model too simple to capture even the main pattern."),
        ("Regularisation", "A penalty on large weights that discourages overfitting."),
    ],
    mistakes=[
        "Adding up residuals to measure error. Positive and negative residuals cancel, so square them or take their sizes first.",
        "Treating a low training error as proof of a good model. Only the error on unseen data tells you that.",
        "Comparing weights of features measured in different units. Scale the features first.",
        "Assuming a straight line fits because the R² is high. Plot the residuals and look for patterns.",
        "Extrapolating far beyond the data. The revision model predicts 98 marks for 10 hours and 124 for 14, which is impossible.",
    ],
    grade="""
### The normal equation, and why we still use gradient descent

With many features, least squares has a matrix formula, the **normal equation**: w = (XᵀX)⁻¹Xᵀy, where X holds one row per example and y the targets. Ridge regression simply adds a multiple of the identity matrix before inverting, which also makes the maths stable.

So why do engineers train even linear models with gradient descent? Inverting a matrix gets very expensive as the number of features grows, roughly with its cube; datasets can be too large to fit in memory at once; and almost every other model, including every neural network, has no formula at all. Gradient descent works for all of them, a few examples at a time.

### Correlation is not causation

A regression weight measures association, not cause. Ice cream sales predict drownings because hot weather drives both. Answering "what would happen if we changed x?" needs experiments or the tools of **causal inference**, a field of its own.
""",
    quiz=[
        Q("In the model score = 6.5 × hours + 33, what does 6.5 represent?",
          ["The extra marks predicted for each extra hour of revision",
           "The predicted score for a student who did no revision",
           "The average score of all the students in the data",
           "The error of the model on the training data"], 0,
          "6.5 is the weight, the slope of the line. The bias, 33, is the prediction for zero hours."),
        Q("A student's actual score is 70 and the model predicted 64. What is the residual?",
          ["6", "−6", "134", "36"], 0,
          "Residual = actual − predicted = 70 − 64 = 6. Its square, 36, is what goes into the MSE."),
        Q("Why are residuals squared before averaging?",
          ["So positive and negative errors cannot cancel out",
           "So the model trains with fewer parameters",
           "So small errors count more than large ones",
           "So the answer is always a whole number"], 0,
          "Squaring also punishes large errors more heavily, the opposite of the third option."),
        Q("Three residuals are 2, −2 and 4. What is the mean squared error?",
          ["8", "4/3", "2", "24"], 0,
          "(4 + 4 + 16) ÷ 3 = 24 ÷ 3 = 8."),
        Q("Which point does the least squares line always pass through?",
          ["The point made by the mean of x and the mean of y",
           "The point with the largest residual in the data",
           "The origin, where x and y are both zero",
           "The first and last points in the data"], 0,
          "b = ȳ − w × x̄ guarantees the line passes through (x̄, ȳ)."),
        Q("What shape is a linear regression model with two input features?",
          ["A flat plane", "A straight line", "A curve", "A sphere"], 0,
          "Each feature adds a dimension: one feature gives a line, two give a plane, more give a hyperplane."),
        Q("A model scores almost zero error on its training data but large errors on the test data. What has happened?",
          ["Overfitting", "Underfitting", "Regularisation", "Scaling"], 0,
          "It has learned the noise in the training examples as well as the pattern."),
        Q("What does an R² of 0 mean?",
          ["The model is no better than always predicting the mean",
           "The model makes no errors at all on the data",
           "The model has no parameters left to learn",
           "The model explains all of the variation"], 0,
          "R² compares the model's error with the baseline of always guessing the mean. 1 would be perfect."),
        Q("What does regularisation do?",
          ["Penalises large weights to discourage overfitting",
           "Removes outliers from the training data",
           "Splits the data into training and test sets",
           "Adds polynomial features to make curves"], 0,
          "Ridge penalises squared weights and lasso penalises their sizes; both make the model simpler."),
        Q("Why do neural networks need gradient descent instead of a least squares formula?",
          ["No exact formula exists for their best parameters",
           "Gradient descent always finds a perfect fit",
           "Least squares only works on images",
           "Formulas cannot be run on a computer"], 0,
          "An exact formula exists only for simple models like linear regression."),
    ],
    exam=[
        EQ("Explain what the mean squared error measures and why the errors are squared.", 4,
           [MP("It measures the average error of a regression model", ["average", "mean", "how wrong", "error"]),
            MP("Residual: actual minus predicted", ["actual", "predicted", "residual", "difference"]),
            MP("Squaring stops positive and negative errors cancelling", ["cancel", "negative", "positive"]),
            MP("Squaring punishes large errors more", ["large", "big", "punish", "penal", "more heavily"])],
           "The mean squared error measures how wrong a regression model is on average. For each example the residual, the actual value minus the predicted value, is squared, and the squares are averaged. Squaring stops positive and negative errors from cancelling each other out, and it punishes large errors much more heavily than small ones, so the model is pushed hardest to fix its biggest mistakes.",
           command="Explain"),
        EQ("A model is trained to predict house prices. It has a very low error on the training data and a high error on the test data. Explain what has happened and describe two ways to fix it.", 5,
           [MP("The model is overfitting", ["overfit", "over-fit", "over fit"]),
            MP("It has learned the noise or memorised the training data", ["noise", "memoris", "memoriz", "too closely"]),
            MP("So it does not generalise to new data", ["generalis", "generaliz", "new data", "unseen"]),
            MP("Fix: a simpler model or fewer features", ["simpler", "fewer features", "less complex", "lower degree"]),
            MP("Fix: regularisation, or more training data", ["regularis", "regulariz", "more data", "penalty", "ridge", "lasso"])],
           "The model is overfitting: it has learned the random noise in the training examples as well as the real pattern, effectively memorising them, so it does not generalise to houses it has not seen. One fix is to use a simpler model, such as fewer features or a lower degree polynomial. Another is regularisation, which adds a penalty for large weights so the model only becomes complex when the data really demands it. Collecting more training data also helps.",
           command="Explain"),
        EQ("A linear model predicts price = 2,100 × floor area − 4,500 × distance to station + 60,000. Interpret the two weights.", 3,
           [MP("Each extra square metre adds about £2,100", ["2,100", "2100", "square metre", "per square"]),
            MP("Each extra km from the station lowers the price by about £4,500", ["4,500", "4500", "lower", "less", "cheaper", "reduce"]),
            MP("With the other feature held fixed", ["held", "fixed", "constant", "other feature", "same"])],
           "Each extra square metre of floor area adds about £2,100 to the predicted price, and each extra kilometre from the station reduces it by about £4,500. Each weight describes the effect of its feature with the other feature held fixed.",
           command="Interpret"),
    ],
)

L4_2 = Topic(
    slug="classification-and-clustering",
    title="Classification, Trees, Neighbours and Clusters",
    spec="4.2",
    icon="i-grid",
    minutes=40,
    exam_title=NEA,
    blurb="How models sort things into categories: decision boundaries, k-nearest neighbours, logistic regression, decision trees and forests, the confusion matrix, and k-means clustering for data with no labels at all.",
    fact="Gradient boosted decision trees, an idea from around 2000, still win most machine learning competitions on spreadsheet-style data. On tables of numbers, deep learning often loses to a forest of small, well-tuned trees.",
    sections=[
        Section("Classification and decision boundaries", """
A classifier sorts inputs into categories. Picture each example as a point, with one axis per feature, coloured by its class. A classifier carves this space into **regions**, one per class, and the edges between regions are **decision boundaries**.

!diagram ai-boundaries

Different algorithms draw different kinds of boundary:

| Algorithm | Boundary shape | Strength | Weakness |
| **Logistic regression** | A straight line (a hyperplane) | Fast, gives probabilities, easy to explain | Cannot bend |
| **k-nearest neighbours** | Any shape, following the data | No training at all | Slow to predict, needs scaled features |
| **Decision tree** | Boxes with edges parallel to the axes | Readable as a list of rules | Overfits if grown deep |
"""),
        Section("k-nearest neighbours", """
**k-nearest neighbours (kNN)** is the simplest classifier there is, and a surprisingly good one.

1. Store all the training examples. That is the whole of training.
2. For a new point, measure its distance to every stored example.
3. Take the **k** closest, its nearest neighbours.
4. Predict the class most of them belong to.

!diagram ai-knn

The choice of **k** matters. With k = 1 the model copies its single nearest neighbour, so one mislabelled example creates a little island of wrong answers: overfitting. A very large k smooths everything towards the most common class: underfitting. An odd k avoids ties between two classes.

!warn Scale first :: kNN depends entirely on distance, so a feature measured in thousands drowns out one measured in single digits. Always scale features before using it (Level 3).
"""),
        Section("Logistic regression: probabilities from a line", """
Despite its name, **logistic regression** classifies. It computes a linear score exactly like regression, then squashes the score into a probability between 0 and 1 using the **sigmoid** function.

!info Logistic regression :: z = w₁x₁ + w₂x₂ + … + b, then probability = σ(z) = 1 ÷ (1 + e^-z^)

!diagram ai-sigmoid

- A large positive z gives a probability near 1, a large negative z gives one near 0, and z = 0 gives exactly 0.5.
- The model predicts the class when the probability passes a **threshold**, usually 0.5. The boundary where z = 0 is a straight line.
- It is trained with **log loss** (cross-entropy), which punishes confident wrong answers severely. Level 5 explains why.

Look closely and you will see a weighted sum, a bias, and a squashing function. That is exactly an **artificial neuron**, which is Level 6.
"""),
        Section("Decision trees and forests", """
A **decision tree** asks a sequence of yes or no questions about the features, and each answer leads down a branch until a **leaf** gives the prediction.

!diagram ai-decision-tree

### How a tree chooses its questions

At each step the tree tries every feature and every threshold, and picks the question that splits the examples into the **purest** groups. Purity is measured with **Gini impurity**:

!info Gini impurity :: Gini = 1 − (sum of the squares of the class proportions)

A group of all one class has Gini 0. A 50 : 50 mix of two classes has Gini 1 − (0.5² + 0.5²) = 0.5. The tree picks the split that lowers the average impurity the most, weighted by group size, then repeats inside each branch.

### Forests

A single deep tree overfits. Two ensemble methods fix that:

- A **random forest** trains hundreds of trees, each on a random sample of the data and features, and lets them vote. The errors of individual trees cancel out.
- **Gradient boosting** builds trees one after another, each trained to correct the mistakes of those before. Libraries such as XGBoost and LightGBM are the standard tool for tabular data in industry.
"""),
        Section("Evaluating classifiers: the confusion matrix", """
For a yes or no classifier there are four possible outcomes:

| | Predicted yes | Predicted no |
| **Actually yes** | True positive (TP) | False negative (FN) |
| **Actually no** | False positive (FP) | True negative (TN) |

From these four counts:

| Measure | Formula | Question it answers |
| **Accuracy** | (TP + TN) ÷ all | How often is it right overall? |
| **Precision** | TP ÷ (TP + FP) | When it says yes, how often is it right? |
| **Recall** | TP ÷ (TP + FN) | Of all the real yeses, how many did it find? |
| **F1 score** | 2 × precision × recall ÷ (precision + recall) | One number balancing the two |

Raising the threshold makes the model more cautious: precision usually rises and recall falls. Which matters more depends on the cost of each mistake. Missing a cancer (a false negative) is far worse than an extra scan (a false positive), so a screening model favours recall. A spam filter that bins real emails is worse than one that lets a little spam through, so it favours precision.

!tool confusion-matrix
"""),
        Section("Clustering with k-means", """
With no labels at all, **k-means** finds k groups of similar points.

1. Choose k, and place k **centroids** (cluster centres), for example at k random data points.
2. **Assign** every point to its nearest centroid.
3. **Update**: move each centroid to the mean of the points assigned to it.
4. Repeat steps 2 and 3 until nothing changes.

!diagram ai-kmeans-steps

Each round can only reduce the total squared distance from points to their centroids, so the algorithm always settles down, usually within a handful of rounds.

!tool kmeans-lab

### Its limits

- You must choose **k**. The **elbow method** plots the total distance for k = 1, 2, 3 and so on, and looks for the point where adding clusters stops helping much.
- Different starting centroids can give different answers, so it is run several times and the best result kept.
- It assumes clusters are roughly round and similar in size, and it will happily split random noise into k clusters.
"""),
        Section("Hands-on: classify and cluster from scratch", """
### k-nearest neighbours

```python
import math

# (sweetness, crunchiness) of foods, labelled by type
data = [((9, 2), "fruit"), ((8, 3), "fruit"), ((7, 1), "fruit"), ((8, 1), "fruit"),
        ((2, 9), "vegetable"), ((3, 8), "vegetable"), ((1, 7), "vegetable"),
        ((2, 6), "vegetable"), ((6, 6), "nut"), ((5, 7), "nut"), ((5, 9), "nut")]

def knn(point, k):
    nearest = sorted(data, key=lambda item: math.dist(item[0], point))[:k]
    votes = {}
    for _, label in nearest:
        votes[label] = votes.get(label, 0) + 1
    return max(votes, key=votes.get), [label for _, label in nearest]

for food in [(7, 3), (3, 6), (6, 8)]:
    for k in (1, 3, 5):
        guess, neighbours = knn(food, k)
        print(f"{food} with k={k}: {guess:10} neighbours {neighbours}")
```

### Choosing a split with Gini impurity

```python
def gini(labels):
    n = len(labels)
    return 1 - sum((labels.count(c) / n) ** 2 for c in set(labels))

# Hours of sleep and whether the student felt alert
sleep = [4, 5, 5, 6, 7, 7, 8, 8, 9, 10]
alert = ["no", "no", "no", "no", "yes", "no", "yes", "yes", "yes", "yes"]

best = None
for threshold in sorted(set(sleep)):
    left = [a for s, a in zip(sleep, alert) if s < threshold]
    right = [a for s, a in zip(sleep, alert) if s >= threshold]
    if not left or not right:
        continue
    score = (len(left) * gini(left) + len(right) * gini(right)) / len(alert)
    print(f"split at sleep < {threshold:2}: weighted Gini {score:.3f}")
    if best is None or score < best[0]:
        best = (score, threshold)
print("Best question: is sleep <", best[1], "hours?")
```

### k-means

```python
import math

points = [(1, 1), (1.5, 2), (2, 1.2), (8, 8), (9, 8.5), (8.5, 9.5), (1, 8), (2, 9), (1.5, 9.5)]
centroids = [(1, 1), (2, 1.2), (8, 8)]          # deliberately poor starting places

for step in range(1, 10):
    clusters = [[] for _ in centroids]
    for p in points:
        nearest = min(range(len(centroids)), key=lambda i: math.dist(p, centroids[i]))
        clusters[nearest].append(p)
    new = [(sum(x for x, y in c) / len(c), sum(y for x, y in c) / len(c)) for c in clusters]
    print(f"round {step}:", [(round(x, 2), round(y, 2)) for x, y in new])
    if new == centroids:
        print("No change, so k-means has converged.")
        break
    centroids = new
```

Two starting centroids were placed inside the same group, yet within a few rounds one of them migrates to the empty group at the top left.

### Activity: build a human decision tree

As a class, think of an animal. A volunteer may only ask yes or no questions about features, such as "does it have fur?". Record the questions on the board as a tree. Which first question splits the class's animals most evenly, and why is that the best first question?
"""),
        Section("Level check", """
+ Explain what a decision boundary is and sketch the boundaries of three algorithms
+ Describe the kNN algorithm and the effect of choosing k
+ Explain how logistic regression turns a linear score into a probability
+ Calculate Gini impurity and explain how a tree chooses a split
+ Calculate precision and recall from a confusion matrix and say when each matters more
+ Describe the k-means algorithm and two of its limitations
"""),
    ],
    keyterms=[
        ("Classifier", "A model that predicts which category an input belongs to."),
        ("Decision boundary", "The edge between the regions a classifier assigns to different classes."),
        ("k-nearest neighbours", "Classifying a point by a vote of the k training examples closest to it."),
        ("Logistic regression", "A classifier that passes a linear score through the sigmoid function to give a probability."),
        ("Sigmoid", "The S-shaped function 1 ÷ (1 + e^-z^) that squashes any number into the range 0 to 1."),
        ("Decision tree", "A model that predicts by asking a sequence of yes or no questions about the features."),
        ("Gini impurity", "A measure of how mixed the classes in a group are; 0 means all one class."),
        ("Random forest", "Many decision trees trained on random samples of the data, voting together."),
        ("Precision", "Of the examples predicted positive, the fraction that really are positive."),
        ("Recall", "Of the examples that really are positive, the fraction the model found."),
        ("k-means", "A clustering algorithm that repeatedly assigns points to the nearest of k centroids and moves each centroid to the mean of its points."),
        ("Centroid", "The centre of a cluster: the mean of the points in it."),
    ],
    mistakes=[
        "Thinking logistic regression is a regression model. It is a classifier that outputs probabilities.",
        "Using kNN on features with very different scales, so one feature decides every distance.",
        "Growing a decision tree until every leaf is pure. It will memorise the training data.",
        "Judging a classifier by accuracy alone when false positives and false negatives have very different costs.",
        "Believing k-means discovers the true number of groups. You choose k, and it will always produce k clusters.",
    ],
    grade="""
### Support vector machines

Before deep learning, the most celebrated classifier was the **support vector machine** (SVM, 1990s). Of all the straight lines that separate two classes, it chooses the one with the widest **margin**, the gap to the nearest points on either side, which tends to generalise well. The **kernel trick** lets an SVM draw curved boundaries by implicitly mapping the data into a higher-dimensional space where a flat boundary works.

### Why trees still win on tables

On images, sound and text, deep learning dominates because those inputs have structure (neighbouring pixels, word order) that networks exploit. Spreadsheet-style data has no such structure, features are often on wildly different scales, and datasets are often small. Gradient boosted trees handle all of that with little tuning. A good engineer tries a boosted tree baseline on any table before reaching for a neural network.
""",
    quiz=[
        Q("What is a decision boundary?",
          ["The edge between regions a classifier assigns to different classes",
           "The largest value a feature is allowed to take",
           "The point where training stops improving",
           "The split between training and test data"], 0,
          "Points on one side are given one class and points on the other side another."),
        Q("In kNN with k = 5, a new point's nearest neighbours are 3 cats and 2 dogs. What is predicted?",
          ["Cat", "Dog", "A tie, so no prediction", "60% cat"], 0,
          "The majority of the 5 neighbours are cats, so the prediction is cat."),
        Q("What is the risk of using k = 1 in k-nearest neighbours?",
          ["One mislabelled example creates wrong answers around it",
           "The model becomes far too slow to train",
           "Every point is given the most common class",
           "Features no longer need to be scaled"], 0,
          "k = 1 copies a single neighbour, so it overfits to noise; very large k underfits instead."),
        Q("What does the sigmoid function do in logistic regression?",
          ["Squashes a score into a probability between 0 and 1",
           "Splits the data into a training set and a test set",
           "Finds the k nearest training examples to a point",
           "Removes features that the model does not need"], 0,
          "σ(z) = 1 ÷ (1 + e^-z^): large positive z goes towards 1 and large negative z towards 0."),
        Q("A group contains 3 apples and 1 orange. What is its Gini impurity?",
          ["0.375", "0.25", "0.5", "0.75"], 0,
          "1 − (0.75² + 0.25²) = 1 − (0.5625 + 0.0625) = 0.375."),
        Q("How does a random forest reduce overfitting?",
          ["Many trees trained on random samples vote, so their errors cancel",
           "It grows a single tree much deeper than usual",
           "It removes every feature except the most useful one",
           "It trains one tree on the test set as well"], 0,
          "Averaging many different trees reduces the variance of any single one."),
        Q("A model finds 40 of the 50 real fraud cases and flags 10 genuine payments by mistake. What is its recall?",
          ["80%", "20%", "40%", "50%"], 0,
          "Recall = TP ÷ (TP + FN) = 40 ÷ 50 = 80%. Precision would be 40 ÷ 50 = 80% too here."),
        Q("For a cancer screening test, which mistake is usually worse, and so which measure is favoured?",
          ["A false negative, so recall is favoured",
           "A false positive, so precision is favoured",
           "A true positive, so accuracy is favoured",
           "A true negative, so the F1 score is favoured"], 0,
          "Missing a real cancer costs far more than an extra check, so finding every case matters most."),
        Q("In k-means, what happens in the update step?",
          ["Each centroid moves to the mean of the points assigned to it",
           "Each point moves to the centroid it is nearest to",
           "The number of clusters k increases by one",
           "The points with the largest distances are deleted"], 0,
          "Assign points to the nearest centroid, then move centroids to the mean of their points, and repeat."),
        Q("Why is k-means usually run several times with different starting centroids?",
          ["Different starts can settle on different, worse clusterings",
           "It needs several runs before it can find any clusters",
           "Each run adds one more cluster to the result",
           "Running it again makes the clusters more equal in size"], 0,
          "It always converges, but sometimes to a poor arrangement, so the best of several runs is kept."),
    ],
    exam=[
        EQ("Describe how the k-nearest neighbours algorithm classifies a new example.", 4,
           [MP("Calculate the distance from the new example to every training example", ["distance", "every", "all training"]),
            MP("Select the k closest examples", ["k closest", "k nearest", "nearest", "closest"]),
            MP("Count the classes of those neighbours / vote", ["vote", "count", "majority"]),
            MP("Predict the most common class among them", ["most common", "majority", "most frequent", "most of"])],
           "The algorithm calculates the distance, usually the straight-line distance, from the new example to every example in the training data. It selects the k closest of these, its nearest neighbours. It then counts which class each neighbour belongs to, a vote, and predicts the class that is most common among the k neighbours.",
           command="Describe"),
        EQ("A spam filter is tested on 1,000 emails. It correctly flags 90 of the 100 spam emails and wrongly flags 30 genuine emails. Calculate its precision and recall, and explain which matters more for a spam filter.", 5,
           [MP("Recall = 90 ÷ 100 = 90%", ["90%", "0.9", "90 / 100", "90/100"]),
            MP("Precision = 90 ÷ 120", ["90/120", "90 / 120", "90 ÷ 120", "120"]),
            MP("Precision = 75%", ["75%", "0.75"]),
            MP("Precision matters more", ["precision matters", "precision is more", "favour precision", "precision"]),
            MP("Because binning genuine emails is worse than letting some spam through", ["genuine", "real email", "important email", "miss", "lose"])],
           "Recall is TP ÷ (TP + FN) = 90 ÷ 100 = 90%. Precision is TP ÷ (TP + FP) = 90 ÷ (90 + 30) = 90 ÷ 120 = 75%. Precision matters more for a spam filter, because a genuine email sent to the spam folder may be important and never seen, whereas a spam email that gets through is only a mild annoyance. So the threshold should be raised to cut false positives.",
           command="Calculate"),
        EQ("Explain how a decision tree chooses which question to ask first.", 4,
           [MP("It tries every feature and possible threshold", ["every feature", "each feature", "all features", "threshold", "possible split"]),
            MP("It measures how pure / mixed the resulting groups are", ["pure", "purity", "mixed", "impurity"]),
            MP("Using Gini impurity or entropy", ["Gini", "entropy", "information gain"]),
            MP("It picks the split that lowers impurity the most, weighted by group size", ["lowest", "most", "largest reduction", "best", "weighted"])],
           "The tree considers every feature and every possible threshold for it. For each candidate question it splits the training examples into two groups and measures how mixed the classes in each group are, using Gini impurity or entropy. It chooses the question that reduces the impurity the most, averaged over the two groups and weighted by their sizes, so that the groups are as pure as possible.",
           command="Explain"),
    ],
)

TOPICS = [L4_1, L4_2]
