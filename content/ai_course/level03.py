"""Level 3: Data, the Fuel of AI. Turning the world into numbers, and datasets done well."""
from mskbuild.models import Topic, Section, Q, EQ, MP

NEA = "Check you could explain this"

L3_1 = Topic(
    slug="data-as-numbers",
    title="Everything Is Numbers: Turning the World into Data",
    spec="3.1",
    icon="i-binary",
    minutes=32,
    exam_title=NEA,
    blurb="How examples, features and labels make a dataset, how images, sound and text become numbers, what vectors, matrices and tensors are, and why features must be scaled before a model sees them.",
    fact="A single photo from a 12 megapixel phone camera is about 36 million numbers: 12 million pixels, each with a red, a green and a blue value. To a neural network, your holiday snap is a very long list of numbers between 0 and 255.",
    sections=[
        Section("Examples, features and labels", """
A model never sees a cat, a song or a sentence. It sees numbers. The first job in any AI project is turning the world into a **dataset**: a table of numbers a model can learn from.

!diagram ai-dataset-table

- Each **row** is one **example** (also called a sample, instance or data point).
- Each **column** is a **feature**: one measurable property of the examples.
- In supervised learning one extra column holds the **label**, the answer the model must learn to predict.

### Kinds of feature

| Kind | Meaning | Examples |
| **Numerical, continuous** | Any value in a range | Height 1.62 m, temperature 18.4 °C |
| **Numerical, discrete** | Counts | Number of bedrooms, goals scored |
| **Categorical, nominal** | Categories with no order | Colour, country, favourite sport |
| **Categorical, ordinal** | Categories with an order | Small, medium, large; grade 1 to 9 |
| **Unstructured** | Not a neat column at all | Images, audio, text, video |

Models only do arithmetic, so every kind must end up as numbers. Choosing and building good features is called **feature engineering**, and before deep learning it was most of the work.
"""),
        Section("Images are grids of numbers", """
A greyscale image is a grid of **pixels**, each a brightness from **0** (black) to **255** (white): one byte each. The famous MNIST dataset of handwritten digits uses images 28 pixels square, so each digit is **784 numbers**.

A colour image stores three numbers per pixel, one each for **red**, **green** and **blue**. Stack the three grids and you have a block of numbers: height × width × 3 **channels**.

!diagram ai-image-tensor

| Image | Shape | Numbers |
| MNIST digit | 28 × 28 × 1 | 784 |
| Thumbnail used to train many vision models | 224 × 224 × 3 | 150,528 |
| Full HD video frame | 1080 × 1920 × 3 | 6,220,800 |
| One second of Full HD video at 30 frames a second | 30 × 1080 × 1920 × 3 | 186,624,000 |

That last row is why video models need so much computing power, and why images are usually shrunk before training.
"""),
        Section("Sound, text and categories as numbers", """
### Sound

A microphone measures air pressure thousands of times a second. CD quality audio takes **44,100 samples a second**, each a number. Speech models often turn the sound into a **spectrogram** first: a picture of which frequencies are loud at each moment, which can then be treated like an image.

### Text

Every character already has a number (its Unicode code point: "A" is 65). Models usually work with bigger pieces called **tokens**, each given an ID from a fixed vocabulary. Level 9 shows how modern models split text into tokens and turn each one into a list of meaningful numbers.

### Categories: one-hot encoding

You cannot just number categories, because the numbers imply an order and a size that are not there. If red = 1, green = 2 and blue = 3, a model may conclude blue is "three times" red, or that green is the average of red and blue.

**One-hot encoding** gives each category its own column, with a 1 in the column that applies and 0 everywhere else:

| Colour | is_red | is_green | is_blue |
| red | 1 | 0 | 0 |
| green | 0 | 1 | 0 |
| blue | 0 | 0 | 1 |

For **ordinal** categories, where the order is real (small, medium, large), plain numbers 0, 1, 2 are fine.

!warn One-hot gets big :: A vocabulary of 50,000 words one-hot encoded makes every word a list of 50,000 numbers with a single 1. Worse, every word is equally different from every other: "cat" is as far from "kitten" as from "volcano". Embeddings, in Level 9, fix both problems.
"""),
        Section("Scalars, vectors, matrices and tensors", """
AI engineers describe data by its **shape**.

!diagram ai-tensor-ranks

| Name | Dimensions | Example | Shape |
| **Scalar** | 0 | One temperature: 18.4 | () |
| **Vector** | 1 | One house: size, bedrooms, age | (3,) |
| **Matrix** | 2 | A greyscale image, or a table of 100 houses | (28, 28) or (100, 3) |
| **Tensor** | 3 or more | A colour image; a batch of 32 colour images | (224, 224, 3) or (32, 224, 224, 3) |

"Tensor" is the general word for all of them, which is where the name of the TensorFlow library comes from. Models process data in **batches**, many examples at once, so there is nearly always an extra batch dimension at the front.

### The dot product: the most important sum in AI

Multiply two vectors position by position and add up the results:

!info Dot product :: [1, 2, 3] · [4, 5, 6] = 1×4 + 2×5 + 3×6 = 32

A dot product measures how much two vectors **point the same way**. Large and positive: similar direction. Zero: unrelated. Negative: opposite. Every artificial neuron computes a dot product, and so does every attention score in a transformer. Graphics processors are built to do billions of them a second.
"""),
        Section("Scaling features", """
Features are often on wildly different scales. House size might run from 50 to 300 square metres while bedrooms run from 1 to 6. Any method that measures **distance** will then be dominated by the feature with the biggest numbers, and gradient descent (Level 5) trains slowly and unevenly.

!diagram ai-feature-scaling

### Two standard fixes

| Method | Formula | Result |
| **Min-max normalisation** | (x − min) ÷ (max − min) | Every value between 0 and 1 |
| **Standardisation (z-score)** | (x − mean) ÷ standard deviation | Mean 0, standard deviation 1; values usually between −3 and 3 |

Standardisation copes better with outliers, because one huge value would squash every other min-max value towards 0.

!key Fit on training data only :: Work out the min, max, mean and standard deviation from the **training** data, then apply those same numbers to the validation and test data and to every future input. Computing them from all the data lets information from the test set leak into training.
"""),
        Section("Hands-on: turning things into numbers", """
### An image is a list of lists

```python
# A 7 by 7 greyscale image: 0 is black, 255 is white
image = [
    [  0,   0, 255, 255, 255,   0,   0],
    [  0, 255,   0,   0,   0, 255,   0],
    [255,   0, 255,   0, 255,   0, 255],
    [255,   0,   0,   0,   0,   0, 255],
    [255,   0, 255, 255, 255,   0, 255],
    [  0, 255,   0,   0,   0, 255,   0],
    [  0,   0, 255, 255, 255,   0,   0],
]

def show(img):
    for row in img:
        print("".join("##" if p > 127 else ". " for p in row))

show(image)
flat = [p for row in image for p in row]      # what a simple network sees
print("Shape 7 x 7 becomes a vector of", len(flat), "numbers:", flat[:10], "...")
print("Scaled to 0..1:", [p / 255 for p in flat[:10]], "...")
inverted = [[255 - p for p in row] for row in image]
show(inverted)
```

### One-hot encoding, scaling and distance

```python
import math

def one_hot(value, categories):
    return [1 if c == value else 0 for c in categories]

colours = ["red", "green", "blue"]
for c in colours:
    print(f"{c:6} -> {one_hot(c, colours)}")

# Three houses: (size in square metres, bedrooms)
A, B, C = (100, 2), (102, 5), (130, 2)
print("Unscaled: A to B", round(math.dist(A, B), 2), " A to C", round(math.dist(A, C), 2))

# Min-max scale each feature using ranges from the training data
size_lo, size_hi, bed_lo, bed_hi = 50, 300, 1, 6
def scale(h):
    return ((h[0] - size_lo) / (size_hi - size_lo), (h[1] - bed_lo) / (bed_hi - bed_lo))

sA, sB, sC = scale(A), scale(B), scale(C)
print("Scaled:   A to B", round(math.dist(sA, sB), 2), " A to C", round(math.dist(sA, sC), 2))

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))
print("Dot product [1, 2, 3] . [4, 5, 6] =", dot([1, 2, 3], [4, 5, 6]))
```

Unscaled, house B looks almost identical to A, because a 2 square metre difference is tiny next to the 30 square metre gap to C, and the 3 extra bedrooms barely register. Once scaled, the extra bedrooms count properly and C becomes the nearest. A nearest neighbour model would give different answers before and after scaling.

### Activity: design the features

A school wants to predict whether a student will be late tomorrow. In a group, list ten features you could collect, say what kind each one is, how you would turn it into numbers, and which ones it would be unfair or intrusive to use. Then do the same for predicting whether someone will skip a song.
"""),
        Section("Level check", """
+ Describe a dataset in terms of examples, features and labels
+ Explain how a colour image is stored as numbers, and work out its size from its shape
+ Explain why categories need one-hot encoding, and when plain numbers are fine
+ Name and give the shape of a scalar, vector, matrix and tensor
+ Calculate a dot product and say what it measures
+ Explain why features are scaled and the difference between min-max and standardisation
"""),
    ],
    keyterms=[
        ("Dataset", "A collection of examples, usually a table with one row per example and one column per feature."),
        ("Example", "One row of a dataset: one house, one image, one email. Also called a sample or data point."),
        ("Feature", "One measurable property of the examples, used as an input to the model."),
        ("Feature engineering", "Choosing, building and transforming features so a model can learn from them."),
        ("Pixel", "One point in an image, stored as a brightness or as red, green and blue values from 0 to 255."),
        ("Channel", "One layer of an image's values, such as its red, green or blue values."),
        ("One-hot encoding", "Turning a category into a vector with a 1 in its own position and 0 everywhere else."),
        ("Tensor", "A block of numbers with any number of dimensions; scalars, vectors and matrices are tensors of rank 0, 1 and 2."),
        ("Dot product", "The sum of the products of two vectors' matching entries, measuring how much they point the same way."),
        ("Normalisation", "Rescaling a feature into a fixed range, usually 0 to 1, with (x − min) ÷ (max − min)."),
        ("Standardisation", "Rescaling a feature to mean 0 and standard deviation 1 with (x − mean) ÷ standard deviation."),
    ],
    mistakes=[
        "Numbering categories 1, 2, 3 when they have no order, which tells the model an order and sizes that do not exist.",
        "Forgetting the channels when working out the size of a colour image: height times width times 3.",
        "Scaling with statistics from the whole dataset instead of the training data alone, which leaks the test set into training.",
        "Thinking a model sees an image the way we do. It receives a long list of numbers with no idea that neighbouring pixels belong together, unless the architecture builds that in.",
        "Assuming more features is always better. Irrelevant or duplicated features add noise and make overfitting more likely.",
    ],
    grade="""
### The curse of dimensionality

Every feature adds a dimension. With 784 pixel features, each MNIST digit is a point in 784-dimensional space, and high-dimensional spaces behave strangely. The volume grows so fast that data becomes sparse: to keep the same density of examples, doubling the number of features can require squaring the amount of data. Distances also become less meaningful, because most points end up roughly the same distance apart.

This is why engineers reduce dimensions (Level 4 mentions principal component analysis), choose features carefully, and why deep learning's ability to **learn** compact features from raw data was such a breakthrough. A network's hidden layers are, in effect, automatic feature engineering.
""",
    quiz=[
        Q("In a dataset table, what does each row usually represent?",
          ["One example, such as one house or one image",
           "One feature, such as floor area",
           "One label, such as the price",
           "One model trained on the data"], 0,
          "Rows are examples and columns are features, with one column for the label in supervised learning."),
        Q("How many numbers does a 224 × 224 colour image contain?",
          ["150,528", "50,176", "672", "224"], 0,
          "224 × 224 pixels × 3 channels (red, green, blue) = 150,528."),
        Q("Why is one-hot encoding used for a feature such as 'favourite sport'?",
          ["Numbering sports would imply a false order and sizes",
           "It makes the dataset smaller and faster to train on",
           "Models are not able to store any text in memory",
           "It removes outliers from the feature automatically"], 0,
          "Each sport gets its own 0 or 1 column, so no false order or arithmetic is implied."),
        Q("Which of these is a matrix?",
          ["A greyscale image of 28 × 28 pixels", "A single temperature reading",
           "One house described by three features", "A batch of 32 colour images"], 0,
          "A matrix has two dimensions. One house is a vector; a batch of colour images is a 4-dimensional tensor."),
        Q("What is [2, 0, 1] · [3, 5, 4]?",
          ["10", "9", "15", "24"], 0,
          "2×3 + 0×5 + 1×4 = 6 + 0 + 4 = 10."),
        Q("A dot product of two vectors is large and positive. What does that suggest?",
          ["They point in a similar direction", "They point in opposite directions",
           "They are unrelated", "One of them is zero"], 0,
          "Positive means similar direction, zero means unrelated, negative means opposite."),
        Q("What does min-max normalisation do?",
          ["Rescales a feature so its values lie between 0 and 1",
           "Removes the largest and smallest values",
           "Makes the mean of a feature equal to its maximum",
           "Sorts the values from smallest to largest"], 0,
          "(x − min) ÷ (max − min) maps the minimum to 0 and the maximum to 1."),
        Q("Why should scaling statistics be calculated from the training data only?",
          ["Using the test data would leak information from it into training",
           "The test data is always too small to use",
           "The training data has no outliers", "It makes training faster"], 0,
          "The test set must be unseen to give an honest result, so it cannot shape any part of training, scaling included."),
        Q("Which feature is ordinal?",
          ["T-shirt size: small, medium or large",
           "Eye colour: blue, brown or green",
           "Country of birth: UK, India or Brazil",
           "Height in centimetres: 152, 167 or 181"], 0,
          "Ordinal categories have a real order. Eye colour and country are nominal; height is numerical."),
        Q("CD quality audio has 44,100 samples per second. Roughly how many numbers is a 3 minute mono recording?",
          ["About 7.9 million", "About 132,000", "About 44,100", "About 2.6 million"], 0,
          "44,100 × 180 seconds = 7,938,000 samples."),
    ],
    exam=[
        EQ("Explain how a colour photograph is represented so that a machine learning model can use it.", 4,
           [MP("The image is a grid of pixels", ["grid", "pixels", "pixel"]),
            MP("Each pixel has red, green and blue values / three channels", ["red", "green", "blue", "RGB", "channel"]),
            MP("Each value is a number, usually 0 to 255", ["0 to 255", "0-255", "255", "byte", "number"]),
            MP("Stored as a tensor of height × width × 3, often scaled to 0 to 1", ["height", "width", "tensor", "shape", "scaled", "0 to 1", "flatten"])],
           "The photograph is divided into a grid of pixels. Each pixel is stored as three numbers, one for each of the red, green and blue channels, usually from 0 to 255. Together the values form a tensor with the shape height × width × 3, which is normally scaled to the range 0 to 1 before being given to the model.",
           command="Explain"),
        EQ("A model predicts house prices using floor area in square metres and number of bedrooms. Explain why the features should be scaled, and describe one way to scale them.", 4,
           [MP("The features are on very different scales / ranges", ["different scale", "range", "bigger numbers", "larger values"]),
            MP("The larger feature dominates distances or slows training", ["dominate", "distance", "slow", "outweigh", "unequal"]),
            MP("Min-max: (x − min) ÷ (max − min), or standardise: (x − mean) ÷ standard deviation", ["min", "max", "mean", "standard deviation", "z-score"]),
            MP("Using statistics from the training data only", ["training data", "training set", "train only", "leak"])],
           "Floor area runs to hundreds while bedrooms run from 1 to about 6, so without scaling the floor area would dominate any distance calculation and gradient descent would train slowly and unevenly. Min-max normalisation fixes this by replacing each value with (x − min) ÷ (max − min), putting both features between 0 and 1. The min and max must be taken from the training data only and then applied unchanged to test data and new inputs.",
           command="Explain"),
        EQ("Calculate the dot product of [3, −1, 2] and [1, 4, 2], showing your working, and state what the sign of the answer tells you.", 3,
           [MP("3×1 + (−1)×4 + 2×2", ["3 - 4 + 4", "3 -4 +4", "3×1", "3x1", "(-1)", "-4"]),
            MP("= 3", ["= 3", "is 3", "equals 3", "answer 3"]),
            MP("Positive, so the vectors point in a broadly similar direction", ["positive", "similar direction", "same direction"])],
           "3 × 1 + (−1) × 4 + 2 × 2 = 3 − 4 + 4 = 3. The answer is positive, so the two vectors point in a broadly similar direction, though not strongly.",
           command="Calculate"),
    ],
)

L3_2 = Topic(
    slug="datasets-and-bias",
    title="Datasets, Splits and Bias: Good Data In, Good AI Out",
    spec="3.2",
    icon="i-database",
    minutes=34,
    exam_title=NEA,
    blurb="Where training data comes from, why it is split into training, validation and test sets, how to clean it, the accuracy trap of imbalanced classes, and how bias gets into data and then into AI.",
    fact="A 2021 study by researchers at MIT found that about 6% of the labels in the ImageNet validation set are wrong. Some of the benchmark results the whole field competed on were partly measuring how well models agreed with mistakes.",
    sections=[
        Section("Where data comes from", """
"Garbage in, garbage out" is older than AI, and nowhere truer. A model can only learn what its data contains.

| Source | Examples | Watch out for |
| **Collected** | Sensor readings, app logs, sales records | Missing values, faulty sensors, consent |
| **Public datasets** | MNIST (70,000 handwritten digits), ImageNet, Common Crawl (billions of web pages) | Licences, errors, what and who is missing |
| **Labelled by people** | Crowd workers tagging images, doctors marking scans | Cost, disagreement, labellers' assumptions |
| **Synthetic** | Simulated driving scenes, text generated by another model | Whether it matches the real world |

Personal data is protected by law. In the UK, the **UK GDPR** and the Data Protection Act 2018 require a lawful basis for using it, data minimisation and security, and give people rights over data about them.
"""),
        Section("Training, validation and test sets", """
A model must be judged on data it has **never seen**, or you only learn how well it memorised. So the data is split before training starts.

!diagram ai-data-split

| Set | Typical share | Used for | Exam analogy |
| **Training** | 70 to 80% | Learning the parameters | Practice questions |
| **Validation** | 10 to 15% | Choosing settings, comparing models, deciding when to stop | Mock exams |
| **Test** | 10 to 15% | One final, honest estimate of performance | The real exam, sat once |

If you keep tweaking the model until the **test** score looks good, the test set has quietly become a second validation set, and the final score is too optimistic. It should be used once, at the end.

### Data leakage

**Leakage** is when information that would not be available in real use sneaks into training. Common causes:

- The same item, or a near copy, in both training and test sets
- Several photos of the same patient split across sets, so the model recognises the patient rather than the illness
- Features from the future, such as using "was refunded" to predict "will complain"
- Scaling or cleaning using statistics from the whole dataset

Shuffle before splitting, but **never** shuffle time series: train on the past and test on the future, as the model will be used.
"""),
        Section("Cleaning data", """
Real data is messy. Data scientists often say cleaning takes most of their time.

| Problem | Example | Typical fix |
| **Missing values** | No age recorded | Drop the row, fill with the median, or add a "was missing" feature |
| **Duplicates** | The same customer entered twice | Remove them, before splitting |
| **Outliers** | Age 160 | Correct an obvious typo; keep genuine extremes |
| **Inconsistent formats** | Heights in cm and m; "UK", "U.K." and "Britain" | Convert to one standard |
| **Label noise** | A dog labelled "cat" | Review suspicious labels, get several labellers to agree |

!warn An outlier is not always an error :: A transaction a hundred times larger than usual might be a typo, or it might be the fraud you are trying to catch. Deleting outliers without thinking can delete the most important examples.
"""),
        Section("Class imbalance and the accuracy trap", """
Suppose 1 card payment in 100 is fraud. A "model" that always answers **not fraud** is right 99% of the time and catches no fraud at all.

!diagram ai-imbalance

When one class is rare, **accuracy** mostly measures the imbalance. Better measures, explained fully in Level 4:

- **Recall**: of all the real fraud, how much did we catch?
- **Precision**: of everything we flagged, how much was really fraud?

### Fixes for imbalance

- Measure with precision and recall, not accuracy alone
- **Oversample** the rare class or **undersample** the common one
- Give mistakes on the rare class a bigger **weight** during training
- Collect more examples of the rare class
"""),
        Section("Bias: how unfairness gets into data", """
A model learns the patterns in its data, including the unfair ones. Bias can enter at every stage.

!diagram ai-bias-pipeline

| Type | What happens | Real example |
| **Sampling bias** | The data does not represent the people the system will serve | The 2018 Gender Shades study found commercial face analysis systems misclassified the gender of darker-skinned women up to **34.7%** of the time, against **0.8%** for lighter-skinned men |
| **Historical bias** | The data accurately records an unfair past | An experimental recruiting tool, reported in 2018, learned from ten years of mostly male CVs to mark down CVs containing the word "women's". It was scrapped |
| **Measurement bias** | The feature measured is a poor stand-in for what matters | A 2019 study in *Science* found a widely used US health algorithm used past healthcare **spending** to stand in for health **need**, so it underestimated the needs of Black patients who had less spent on them |
| **Labelling bias** | Labellers' assumptions become the "truth" | Different groups of labellers rate the same text as offensive at very different rates |
| **Feedback loops** | The model's decisions shape the next data | Sending more patrols where a model predicts crime records more crime there, which "confirms" the prediction |

### What engineers do about it

- Check who and what is **missing** from the data before training
- **Audit by subgroup**: a good overall accuracy can hide a much worse result for one group
- Document datasets with a **datasheet** (what was collected, how, by whom, and its gaps), an idea proposed by Timnit Gebru and colleagues in 2018
- Keep people involved in high-stakes decisions, and let those affected challenge them
"""),
        Section("Hands-on: splitting, auditing and the accuracy trap", """
### A reproducible split

```python
import random

random.seed(7)                   # the same "random" shuffle every run
data = [f"photo_{i:02}" for i in range(20)]
random.shuffle(data)

n = len(data)
train = data[:int(0.7 * n)]
valid = data[int(0.7 * n):int(0.85 * n)]
test = data[int(0.85 * n):]
print(len(train), "training:", train[:4], "...")
print(len(valid), "validation:", valid)
print(len(test), "test:", test)
print("Any overlap?", bool(set(train) & set(test)))
```

### The accuracy trap

```python
labels = ["ok"] * 990 + ["fraud"] * 10
predictions = ["ok"] * len(labels)          # a lazy model: never says fraud

accuracy = sum(p == y for p, y in zip(predictions, labels)) / len(labels)
caught = sum(p == y == "fraud" for p, y in zip(predictions, labels))
print(f"Accuracy: {accuracy:.1%}")
print(f"Fraud caught: {caught} of {labels.count('fraud')}  (recall {caught / labels.count('fraud'):.0%})")
```

### Cleaning a messy table

```python
rows = [
    {"name": "Ava", "age": 15, "score": 72},
    {"name": "Ben", "age": None, "score": 65},
    {"name": "Ava", "age": 15, "score": 72},
    {"name": "Cai", "age": 16, "score": None},
    {"name": "Dee", "age": 160, "score": 81},
]

seen, clean = set(), []
for r in rows:
    key = tuple(r.values())
    if key in seen:
        print("Duplicate removed:", r["name"])
        continue
    seen.add(key)
    clean.append(r)

for r in clean:
    if r["age"] is not None and not 10 <= r["age"] <= 19:
        print("Suspicious age for", r["name"], "->", r["age"])

scores = sorted(r["score"] for r in clean if r["score"] is not None)
median = scores[len(scores) // 2]
for r in clean:
    if r["score"] is None:
        r["score"] = median
        print("Filled missing score for", r["name"], "with the median", median)
```

### An audit by subgroup

```python
# How often a face unlock model was right, for two groups of users
results = {"group A": (950, 1000), "group B": (42, 50)}

total_right = sum(r for r, n in results.values())
total = sum(n for r, n in results.values())
print(f"Overall accuracy: {total_right / total:.1%}")
for group, (right, n) in results.items():
    print(f"  {group}: {right / n:.1%} from {n} people")
```

An overall score of 94.5% looks excellent, until the audit shows one group gets 84%: about one failure in six. The smaller group barely moves the average, which is exactly why averages hide unfairness.

### Activity: who is missing?

A company trains a voice assistant on 10,000 hours of speech recorded by its own staff in one city. In groups, list who is likely to be under-represented, what would go wrong for them, and what data you would collect to fix it.
"""),
        Section("Level check", """
+ Describe four sources of training data and a risk of each
+ Explain the purpose of the training, validation and test sets
+ Explain data leakage and give two ways it happens
+ Describe how to deal with missing values, duplicates and outliers
+ Explain why accuracy misleads on imbalanced data
+ Describe three types of bias with a real example of each, and how engineers reduce them
"""),
    ],
    keyterms=[
        ("Training set", "The data a model learns its parameters from."),
        ("Validation set", "Data held back to choose settings and compare models during development."),
        ("Test set", "Data kept unseen until the end, used once for an honest estimate of performance."),
        ("Data leakage", "Information that would not be available in real use getting into training, making results look better than they are."),
        ("Class imbalance", "When one class is far rarer than another, such as fraud among payments."),
        ("Outlier", "A value far from the rest, which may be an error or a genuine and important extreme."),
        ("Label noise", "Training examples whose labels are wrong."),
        ("Sampling bias", "Data that does not represent the population the system will be used on."),
        ("Historical bias", "Data that accurately records an unfair past, which a model then learns to repeat."),
        ("Measurement bias", "Using a feature that is a poor stand-in for the thing that really matters."),
        ("Datasheet for a dataset", "A document describing how a dataset was made, what it contains, and its gaps and intended uses."),
    ],
    mistakes=[
        "Tuning a model on the test set. Once you have used it to make choices, it no longer gives an honest score.",
        "Shuffling time series before splitting, which lets the model peek at the future.",
        "Trusting accuracy on imbalanced data. Always check precision and recall for the rare class.",
        "Deleting every outlier. Some are errors, but some are exactly the cases you need to catch.",
        "Thinking bias only comes from biased people. Accurate data about an unfair world produces a biased model too.",
        "Reporting one overall score without checking how the model does for each group of people it affects.",
    ],
    grade="""
### Data-centric AI

For years research competed on better models for fixed datasets. Andrew Ng and others have argued for **data-centric AI**: hold the model fixed and systematically improve the data. In practice, cleaning labels, adding examples of the cases the model gets wrong and making the data consistent often helps more than a cleverer architecture.

Professional teams also **version** their data the way they version code, so every model can be traced back to exactly which data trained it. When a model misbehaves months later, that record is the first thing anyone asks for.
""",
    quiz=[
        Q("What is the test set for?",
          ["One final, honest estimate of how the model performs on unseen data",
           "Learning the model's parameters",
           "Choosing the best settings during development",
           "Storing data that has been cleaned"], 0,
          "It is used once at the end. Tuning against it makes its score optimistic."),
        Q("What is the validation set used for?",
          ["Choosing settings and comparing models while building",
           "Learning the model's parameters from examples",
           "Giving the final score that is reported to users",
           "Filling in values that are missing from the data"], 0,
          "It is the mock exam: used repeatedly while building, so it cannot also be the final test."),
        Q("Which is an example of data leakage?",
          ["Photos of the same patient appear in both the training and test sets",
           "The training set is larger than the test set",
           "The data is shuffled before splitting",
           "The validation set is used to choose settings"], 0,
          "The model can recognise the patient rather than learn the illness, so the test score is falsely high."),
        Q("Why should time series data not be shuffled before splitting?",
          ["The model would learn from the future to predict the past",
           "Shuffling deletes some of the data points in the series",
           "Time series data cannot be split into different sets",
           "Shuffling makes the test set much too small to be useful"], 0,
          "Real use always predicts the future from the past, so the test must do the same."),
        Q("1 in 200 emails is a phishing attack. A model never flags anything. What is its accuracy?",
          ["99.5%", "0.5%", "50%", "100%"], 0,
          "It is right on the 199 safe emails in every 200, and catches no attacks at all: the accuracy trap."),
        Q("A dataset has a missing age for one student. Which is a sensible fix?",
          ["Fill it with the median age, or drop the row",
           "Set it to 0", "Set it to the largest age in the data",
           "Delete the age column from every row"], 0,
          "0 or the maximum would create false outliers; the median or dropping the row are standard fixes."),
        Q("A face recognition system was trained mostly on photos of lighter-skinned men. Which bias is this?",
          ["Sampling bias", "Measurement bias", "Label noise", "Data leakage"], 0,
          "The data does not represent the people the system will be used on."),
        Q("A recruiting model learns from ten years of past hiring decisions that favoured men. Which bias is this?",
          ["Historical bias", "Sampling bias", "Leakage", "Class imbalance"], 0,
          "The data accurately records an unfair past, and the model learns to repeat it."),
        Q("Why should accuracy be checked for each subgroup of users?",
          ["A good overall score can hide worse results for a small group",
           "Smaller subgroups always get a higher accuracy than average",
           "Checking subgroups raises the model's overall accuracy",
           "The law requires every group to get exactly equal accuracy"], 0,
          "A small group barely moves the average, so its failures stay invisible unless measured separately."),
        Q("What does random.seed(7) do before random.shuffle?",
          ["Makes the shuffle the same every time the program runs",
           "Shuffles the list seven times", "Picks seven random items",
           "Stops the shuffle from changing anything"], 0,
          "A fixed seed makes 'random' results reproducible, so experiments can be repeated and compared."),
    ],
    exam=[
        EQ("Explain why data is split into training, validation and test sets.", 4,
           [MP("The model must be judged on data it has not seen", ["not seen", "unseen", "new data", "never seen"]),
            MP("Training set: learns the parameters", ["training", "learn", "parameters", "fit"]),
            MP("Validation set: tune settings or compare models", ["validation", "tune", "settings", "hyperparameter", "compare", "choose"]),
            MP("Test set: used once for an honest final estimate", ["test", "once", "final", "honest", "unbiased"])],
           "A model has to be judged on data it has never seen, otherwise we only measure how well it memorised. The training set is used to learn the parameters. The validation set is used during development to choose settings and compare models. The test set is kept unseen until the end and used once, so it gives an honest estimate of how the model will perform on new data.",
           command="Explain"),
        EQ("A bank trains a fraud detector on data where 0.5% of transactions are fraud. It reports 99.5% accuracy. Evaluate this claim.", 5,
           [MP("A model that never predicts fraud also scores 99.5%", ["never", "always says", "not fraud", "99.5"]),
            MP("So accuracy mostly measures the imbalance", ["imbalance", "rare", "misleading", "meaningless"]),
            MP("Recall: how much real fraud is caught", ["recall", "caught", "detect", "find"]),
            MP("Precision: how many flagged transactions really are fraud", ["precision", "flagged", "false alarm", "false positive"]),
            MP("A fix: resampling, class weights or more fraud examples", ["oversample", "undersample", "weight", "more examples", "resampl"])],
           "The claim is meaningless on its own. Because only 0.5% of transactions are fraud, a model that never predicts fraud at all would also score 99.5% accuracy while catching nothing, so accuracy here mostly measures the imbalance. The bank should report recall, the share of real fraud that is caught, and precision, the share of flagged transactions that really are fraud. The model could also be improved by oversampling fraud cases or weighting mistakes on them more heavily.",
           command="Evaluate"),
        EQ("Describe **two** different ways bias can enter the data used to train an AI system. Give an example of each.", 4,
           [MP("A first type of bias named and described", ["sampling", "historical", "measurement", "labelling", "feedback"]),
            MP("A valid example of it", ["face", "recruit", "CV", "health", "spending", "police", "labeller"]),
            MP("A second, different type named and described", ["sampling", "historical", "measurement", "labelling", "feedback"]),
            MP("A valid example of the second", ["face", "recruit", "CV", "health", "spending", "police", "labeller"])],
           "Sampling bias happens when the data does not represent the people the system will be used on. For example, face analysis systems trained mostly on lighter-skinned faces were found in 2018 to misclassify darker-skinned women far more often. Historical bias happens when data accurately records an unfair past. For example, a recruiting tool trained on ten years of mostly male CVs learned to mark down CVs containing the word women's.",
           command="Describe"),
    ],
)

TOPICS = [L3_1, L3_2]
