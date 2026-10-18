"""Level 8: Seeing. Convolutions and convolutional neural networks."""
from mskbuild.models import Topic, Section, Q, EQ, MP

NEA = "Check you could explain this"

L8_1 = Topic(
    slug="convolutions",
    title="Convolutions: How Machines See Edges and Shapes",
    spec="8.1",
    icon="i-image",
    minutes=38,
    exam_title=NEA,
    blurb="Why images need a special kind of layer, how a small kernel sliding across an image finds edges, blurs and textures, how stride and padding set the output size, and how many filters over colour channels build a volume of feature maps.",
    fact="Image filters in photo apps, such as blur, sharpen and edge detection, are convolutions with kernels a person designed. A convolutional network uses exactly the same operation, but learns the numbers in its kernels by itself.",
    sections=[
        Section("Why not a plain dense network?", """
A modest 224 × 224 colour photo has 150,528 input numbers (Level 3). A dense first layer of just 1,000 neurons would need **150 million** weights, before the network has learned anything. Worse, a dense layer ignores the structure of an image:

- It treats the pixel in the top-left corner and its neighbour as unrelated inputs, though neighbouring pixels belong together.
- A cat in the corner and a cat in the centre activate completely different weights, so it would have to learn "cat" separately for every position.

Two ideas fix both problems:

| Idea | Meaning | Benefit |
| **Local connections** | Each output looks at a small patch of the image, such as 3 × 3 pixels | Nearby pixels are processed together |
| **Weight sharing** | The same small set of weights is used at every position | Far fewer parameters, and a feature learned in one place is recognised everywhere |

Together they give the **convolution**, the operation at the heart of a **convolutional neural network (CNN)**.
"""),
        Section("The convolution operation", """
A **kernel** (or **filter**) is a small grid of weights, usually 3 × 3. It slides across the image. At each position:

1. Lay the kernel over a patch of the image.
2. Multiply each kernel weight by the pixel under it.
3. Add up the nine products. That sum is one number of the output.

!diagram ai-convolution

Press Play to watch the kernel slide. The output grid, called a **feature map**, records how strongly the kernel's pattern appears at each position.

### A worked patch

| Patch of the image | Kernel | Products |
| 0, 0, 9 | −1, 0, 1 | 0, 0, 9 |
| 0, 0, 9 | −1, 0, 1 | 0, 0, 9 |
| 0, 0, 9 | −1, 0, 1 | 0, 0, 9 |

The sum is 27: a strong response. This kernel subtracts the left column from the right column, so it responds wherever the image gets brighter from left to right: a **vertical edge**. On a flat patch, all the same brightness, the left and right cancel and it outputs 0.

!key It is a dot product again :: Flatten the patch and the kernel into lists of nine numbers and the convolution at one position is their dot product, plus a bias. A convolutional layer is a neuron with nine weights, reused at every position of the image.
"""),
        Section("Kernels that find features", """
Different kernels detect different patterns.

!diagram ai-kernels

| Kernel | Weights | What it finds |
| **Vertical edges** (Sobel) | −1 0 1 / −2 0 2 / −1 0 1 | Left-to-right changes in brightness |
| **Horizontal edges** (Sobel) | −1 −2 −1 / 0 0 0 / 1 2 1 | Top-to-bottom changes |
| **Blur** | every weight 1/9 | The average of the neighbourhood, smoothing noise |
| **Sharpen** | 0 −1 0 / −1 5 −1 / 0 −1 0 | Exaggerates differences from the neighbours |

For decades, computer vision engineers designed kernels like these by hand. The breakthrough of convolutional networks is that the kernel weights are **parameters**: they are learned by backpropagation, like any other weights. When researchers look inside trained networks, the first layer's kernels turn out to be edge detectors, colour blobs and stripe detectors, very like the ones people designed, plus many nobody had thought of.

!tool convolution-lab

Draw a shape in the lab, then try each kernel and watch which parts of your drawing light up in the feature map.
"""),
        Section("Stride, padding and the output size", """
Two settings control how the kernel moves.

- **Stride**: how many pixels the kernel jumps each time. Stride 1 visits every position; stride 2 skips every other one and halves the output size.
- **Padding**: a border of zeros added around the image, so the kernel can be centred on edge pixels too. "Same" padding keeps the output the same size as the input; "valid" (no padding) shrinks it.

!diagram ai-stride-padding

!info Output size :: output = (n + 2p − k) ÷ s + 1, for an n × n input, a k × k kernel, padding p and stride s

| Input n | Kernel k | Padding p | Stride s | Output |
| 6 | 3 | 0 | 1 | (6 − 3) ÷ 1 + 1 = **4** |
| 6 | 3 | 1 | 1 | (6 + 2 − 3) ÷ 1 + 1 = **6** |
| 7 | 3 | 1 | 2 | (7 + 2 − 3) ÷ 2 + 1 = **4** |
| 224 | 7 | 3 | 2 | (224 + 6 − 7) ÷ 2 + 1 = **112** (rounded down) |
"""),
        Section("Colour images and many filters", """
A colour image has three channels, so a kernel for it is a small **block**: 3 × 3 × 3, with 27 weights covering the red, green and blue values of a patch at once, plus a bias. Its output is still a single number per position, so one kernel produces one feature map.

A convolutional layer uses **many** kernels, often 32, 64 or more, each learning to detect a different pattern. Their feature maps are stacked into an output volume, which becomes the input to the next layer.

!diagram ai-conv-volume

!info Parameters in a convolutional layer :: (k × k × input channels + 1) × number of filters

A layer of 64 filters of size 3 × 3 over a colour image has (3 × 3 × 3 + 1) × 64 = **1,792** parameters, whatever the size of the image. Compare that with the 150 million of the dense layer, and you see why convolution made computer vision practical.
"""),
        Section("Hands-on: convolution from scratch", """
### Finding the edges of a bar

```python
image = [[0] * 8 for _ in range(8)]
for row in range(1, 7):
    image[row][3] = image[row][4] = 9           # a bright vertical bar

def conv2d(img, kernel):
    n, k = len(img), len(kernel)
    out = []
    for r in range(n - k + 1):
        row = []
        for c in range(n - k + 1):
            row.append(sum(img[r + i][c + j] * kernel[i][j]
                           for i in range(k) for j in range(k)))
        out.append(row)
    return out

def show(grid):
    for row in grid:
        print(" ".join(f"{v:4}" for v in row))

vertical = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
horizontal = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
print("Vertical edges:")
show(conv2d(image, vertical))
print("Horizontal edges:")
show(conv2d(image, horizontal))
```

The vertical edge kernel lights up down both sides of the bar: positive where the image gets brighter to the right, negative where it gets darker. The horizontal kernel only fires at the bar's top and bottom ends.

### Output sizes and parameter counts

```python
def output_size(n, k, padding=0, stride=1):
    return (n + 2 * padding - k) // stride + 1

print("6x6, 3x3 kernel, no padding:", output_size(6, 3))
print("6x6, 3x3 kernel, padding 1:", output_size(6, 3, padding=1))
print("224x224, 7x7 kernel, padding 3, stride 2:", output_size(224, 7, 3, 2))

def conv_params(k, channels_in, filters):
    return (k * k * channels_in + 1) * filters

def dense_params(inputs, neurons):
    return inputs * neurons + neurons

print(f"Conv layer, 64 filters of 3x3 on RGB: {conv_params(3, 3, 64):,} parameters")
print(f"Dense layer, 224x224x3 to 1,000 neurons: {dense_params(224 * 224 * 3, 1000):,} parameters")
```

### Try this

1. Add a blur kernel, with every weight 1/9, and run it on the bar. What happens to the bar's edges?
2. Make the bar diagonal instead. Which kernel responds more strongly now?
3. Design a 3 × 3 kernel that responds to a single bright pixel surrounded by dark ones.
"""),
        Section("Level check", """
+ Explain two problems with using dense layers for images, and how local connections and weight sharing fix them
+ Calculate one output value of a convolution by hand
+ Describe what edge, blur and sharpen kernels do, and explain how CNNs get their kernels
+ Use the formula to work out the output size for a given stride and padding
+ Explain how kernels work on colour images and what a layer of many filters produces
+ Calculate the number of parameters in a convolutional layer
"""),
    ],
    keyterms=[
        ("Convolution", "Sliding a small kernel across an image and taking the weighted sum of each patch it covers."),
        ("Kernel (filter)", "A small grid of weights, such as 3 × 3, that detects one pattern wherever it appears."),
        ("Feature map", "The grid of outputs produced by one kernel, showing where its pattern appears."),
        ("Weight sharing", "Using the same kernel weights at every position, so a pattern learned once is found everywhere."),
        ("Local connection", "Each output depends only on a small patch of the input."),
        ("Stride", "How many pixels the kernel moves between positions."),
        ("Padding", "A border of zeros added around the input so the kernel can cover the edges."),
        ("Channel", "One layer of an input or output volume, such as red, or one feature map."),
        ("Convolutional neural network (CNN)", "A network built mainly from convolutional layers, the standard architecture for images."),
        ("Edge detector", "A kernel that responds to sudden changes in brightness, such as the Sobel kernels."),
    ],
    mistakes=[
        "Thinking a kernel's weights are designed by people in a CNN. They are learned by backpropagation.",
        "Forgetting that a kernel on a colour image covers all three channels, so a 3 × 3 kernel has 27 weights, not 9.",
        "Leaving the padding out of the output size formula, or forgetting to round down when the stride does not divide evenly.",
        "Believing a convolutional layer's parameter count depends on the image size. It depends only on the kernel size, channels and number of filters.",
        "Confusing a feature map with the kernel. The kernel is the small grid of weights; the feature map is its output.",
    ],
    grade="""
### Convolution or cross-correlation?

Strictly, the operation in this lesson is **cross-correlation**: a true mathematical convolution flips the kernel first. Because a CNN learns its kernels, the flip makes no difference (it would simply learn the flipped kernel), so deep learning libraries implement cross-correlation and call it convolution. It is worth knowing when you read signal-processing texts.

### Translation equivariance

Because the same kernel is applied everywhere, shifting the input shifts the feature map by the same amount: convolution is **translation equivariant**. That is the built-in assumption, the inductive bias, that makes CNNs so data-efficient for images. Pooling and the final layers then make the overall answer roughly **invariant** to position: a cat is a cat wherever it sits. Vision transformers (Level 10) drop this assumption and must learn it from much more data.
""",
    quiz=[
        Q("Why is a dense layer a poor first layer for photos?",
          ["It needs an enormous number of weights and ignores where pixels are",
           "It cannot take numbers between 0 and 255 as its inputs",
           "It only works on black and white images, never colour",
           "It can only have a single neuron in each of its layers"], 0,
          "150,528 inputs times 1,000 neurons is 150 million weights, with no idea which pixels are neighbours."),
        Q("What does weight sharing in a convolutional layer mean?",
          ["The same kernel weights are used at every position in the image",
           "Several networks share the same training data",
           "Every neuron has exactly the same bias",
           "Weights are copied from one layer to the next"], 0,
          "So a pattern learned in one place is detected anywhere, with very few parameters."),
        Q("A 3 × 3 patch is all 4s and the kernel is all 1s. What is the output?",
          ["36", "12", "4", "9"], 0,
          "Nine products of 4 × 1, added up: 36."),
        Q("Which kernel detects vertical edges?",
          ["−1 0 1 / −2 0 2 / −1 0 1", "1/9 in every position", "0 −1 0 / −1 5 −1 / 0 −1 0",
           "−1 −2 −1 / 0 0 0 / 1 2 1"], 0,
          "It compares the column on the right with the column on the left. The last option finds horizontal edges."),
        Q("What size is the output of a 3 × 3 kernel on a 6 × 6 image, with no padding and stride 1?",
          ["4 × 4", "6 × 6", "3 × 3", "2 × 2"], 0,
          "(6 − 3) ÷ 1 + 1 = 4."),
        Q("What does padding of 1 do for a 3 × 3 kernel with stride 1?",
          ["Keeps the output the same size as the input", "Halves the output size",
           "Doubles the number of filters", "Removes the edges of the image"], 0,
          "(n + 2 − 3) ÷ 1 + 1 = n: the 'same' padding."),
        Q("How many weights does one 3 × 3 kernel have when it works on an RGB image?",
          ["27", "9", "3", "81"], 0,
          "3 × 3 positions times 3 channels = 27, plus one bias."),
        Q("A convolutional layer has 32 filters of size 3 × 3 over 3 input channels. How many parameters does it have?",
          ["896", "864", "288", "32"], 0,
          "(3 × 3 × 3 + 1) × 32 = 28 × 32 = 896."),
        Q("What is a feature map?",
          ["The output grid showing where one kernel's pattern appears",
           "A list of the features a dataset contains",
           "The kernel's own small grid of weights",
           "A map of the computer's memory"], 0,
          "Each kernel produces one feature map; a layer's maps stack into a volume."),
        Q("How does a CNN get the weights for its kernels?",
          ["It learns them by backpropagation during training",
           "Engineers copy them from photo editing software",
           "They are chosen at random and never changed",
           "They are calculated from the image's colours"], 0,
          "Trained first-layer kernels often end up as edge and colour detectors, discovered automatically."),
    ],
    exam=[
        EQ("Explain how a convolutional layer processes an image.", 4,
           [MP("A small kernel / filter of weights", ["kernel", "filter"]),
            MP("Slides across the image, position by position", ["slide", "across", "each position", "move"]),
            MP("At each position multiplies the patch by the weights and sums", ["multipl", "sum", "add", "dot product", "weighted"]),
            MP("Producing a feature map showing where the pattern occurs", ["feature map", "output grid", "where", "pattern"])],
           "A convolutional layer uses small kernels, grids of weights such as 3 × 3. Each kernel slides across the image, one position at a time according to the stride. At each position it multiplies every weight by the pixel beneath it and adds the products, plus a bias, giving one number. The numbers from all the positions form a feature map, showing how strongly the kernel's pattern, such as a vertical edge, appears at each place in the image. A layer with many kernels produces many feature maps.",
           command="Explain"),
        EQ("Calculate the output size of a convolution on a 32 × 32 input with a 5 × 5 kernel, padding 2 and stride 1, and the number of parameters if the input has 3 channels and the layer has 16 filters.", 4,
           [MP("(32 + 4 − 5) ÷ 1 + 1", ["32 + 4 - 5", "32+4-5", "(32 + 2 × 2 − 5)", "31 + 1"]),
            MP("Output is 32 × 32", ["32 × 32", "32x32", "32 by 32"]),
            MP("(5 × 5 × 3 + 1) = 76 per filter", ["76", "5 × 5 × 3", "75 + 1"]),
            MP("× 16 = 1,216 parameters", ["1216", "1,216"])],
           "Output size = (n + 2p − k) ÷ s + 1 = (32 + 4 − 5) ÷ 1 + 1 = 32, so the output is 32 × 32. Each filter has 5 × 5 × 3 = 75 weights plus 1 bias, which is 76 parameters, so 16 filters have 76 × 16 = 1,216 parameters.",
           command="Calculate"),
        EQ("Explain why convolutional networks need far fewer parameters than dense networks for images.", 3,
           [MP("Each output connects only to a small local patch", ["local", "small patch", "small region", "3 × 3"]),
            MP("The same kernel weights are shared across every position", ["shared", "same weights", "reused", "every position"]),
            MP("So the count depends on kernel size and filters, not image size", ["not the image size", "independent", "kernel size", "filters", "does not depend"])],
           "In a convolutional layer each output depends only on a small local patch of the image, such as 3 × 3 pixels, rather than on every pixel. The same kernel weights are also shared across every position in the image. So the number of parameters depends only on the kernel size, the number of input channels and the number of filters, not on the size of the image, which keeps it to thousands instead of hundreds of millions.",
           command="Explain"),
    ],
)

L8_2 = Topic(
    slug="convolutional-networks",
    title="Convolutional Networks: From Pixels to Predictions",
    spec="8.2",
    icon="i-cube",
    minutes=40,
    exam_title=NEA,
    blurb="How convolutions, ReLU and pooling stack into a full image classifier, what each layer learns, the famous architectures from LeNet to ResNet, the residual connections that made very deep networks trainable, and the tricks that make vision models work in practice.",
    fact="In 2015 a ResNet with 152 layers made only 3.57% top-5 errors on the ImageNet challenge, lower than the roughly 5% error rate estimated for a careful human on the same task.",
    sections=[
        Section("Pooling: keeping the strongest signal", """
After a convolution and ReLU, a **pooling** layer shrinks each feature map. **Max pooling** with a 2 × 2 window and stride 2 keeps only the largest value in each 2 × 2 block.

!diagram ai-pooling

| Benefit | Why |
| Smaller maps | A quarter of the values, so later layers are cheaper |
| Tolerance to small shifts | Moving a feature by one pixel usually keeps the same maximum |
| Larger view for later layers | Each value now summarises a bigger patch of the original image |

Pooling has **no parameters** to learn. **Average pooling** takes the mean instead of the maximum, and **global average pooling** averages each whole feature map down to a single number, which modern networks use just before the final layer.
"""),
        Section("The CNN architecture", """
A classic CNN repeats a pattern of convolution, ReLU and pooling, then finishes with dense layers:

!diagram ai-cnn-architecture

1. **Convolution + ReLU**: detect features.
2. **Pooling**: shrink the maps, keeping the strongest signals.
3. Repeat, with more filters each time.
4. **Flatten** the final volume into one long vector.
5. **Dense layers** combine the features, ending in **softmax** over the classes.

Two trends run through the network: the **spatial size shrinks** (32 × 32, then 16 × 16, then 8 × 8) while the **number of channels grows** (3, then 16, then 32). The network trades "where" for "what": fewer positions, but richer descriptions of each.
"""),
        Section("What each layer learns", """
Each value in a deeper layer depends on a larger patch of the original image, called its **receptive field**. Two stacked 3 × 3 convolutions see a 5 × 5 patch; three see 7 × 7; pooling doubles the growth.

!diagram ai-receptive-field

So deeper layers can detect larger and more complex things. Researchers who visualised trained networks (Matthew Zeiler and Rob Fergus, 2013) found a clear hierarchy:

| Depth | Typical features |
| Layer 1 | Edges at different angles, colour blobs |
| Layer 2 | Corners, curves, simple textures |
| Layer 3 | Repeating patterns, mesh, text-like marks |
| Layer 4 | Object parts: eyes, wheels, legs |
| Layer 5 | Whole objects and faces |

No one told the network to look for eyes or wheels. Those detectors emerged because they helped reduce the loss.
"""),
        Section("Famous architectures", """
| Year | Network | Key idea | Size |
| 1998 | **LeNet-5** (Yann LeCun) | Convolution and pooling for handwritten digits; read millions of bank cheques | About 60 thousand parameters |
| 2012 | **AlexNet** | Deep CNN on GPUs with ReLU and dropout; won ImageNet by a huge margin | 8 layers, about 60 million parameters |
| 2014 | **VGG-16** | Only small 3 × 3 kernels, stacked deep | 16 layers, 138 million parameters |
| 2014 | **GoogLeNet** (Inception) | Parallel kernels of several sizes in each block | 22 layers, about 7 million parameters |
| 2015 | **ResNet** | Residual (shortcut) connections | Up to 152 layers and beyond |
| 2019 | **EfficientNet** | Scaling depth, width and resolution together | Small and very accurate |
| 2020 | **Vision Transformer (ViT)** | Treats image patches like words, using attention (Level 10) | From tens of millions of parameters up |
"""),
        Section("Residual connections", """
Before 2015, adding more layers past about 20 made networks **worse**, even on their training data: the gradients could not get through. The ResNet team, led by Kaiming He, added a **shortcut** that carries a block's input straight past it and adds it to the output:

!info Residual block :: output = F(x) + x, where F is a couple of convolution layers

!diagram ai-resnet-block

The block now only has to learn the **change** F(x) to make to its input, and if no change helps it can push F towards zero and pass x through untouched. During backpropagation, the gradient flows straight back along the shortcut, so even the earliest layers receive a strong learning signal. Residual connections are now everywhere, including inside every transformer.
"""),
        Section("Making vision models work in practice", """
### Data augmentation

Show the network modified copies of each training image: flipped, cropped, rotated slightly, with brightness and colour changed. The label stays the same, so the network learns that these changes do not matter, and it sees far more variety than the dataset contains.

!diagram ai-augmentation

### Other essentials

- **Dropout**: during training, randomly switch off a fraction of neurons (often half) at each step, so the network cannot rely on any single one. It is a strong defence against overfitting.
- **Batch normalisation**: rescale each layer's outputs to a steady mean and spread during training, which makes deep networks train faster and more reliably.
- **Transfer learning**: start from a network already trained on ImageNet, keep its convolutional layers as a feature extractor, and train only a new final layer on your own small dataset. A few hundred images can then be enough.

### Beyond "what is in the picture?"

| Task | Output | Example |
| **Classification** | One label for the image | "golden retriever" |
| **Object detection** | A box and a label for every object | A self-driving car finding pedestrians; YOLO (2015) does it in real time |
| **Segmentation** | A label for every pixel | Outlining a tumour on a scan; U-Net (2015) |
| **Face recognition** | An embedding per face, compared by distance | Phone unlock |
"""),
        Section("Hands-on: a hand-built CNN", """
### Max pooling

```python
def max_pool(grid, size=2):
    out = []
    for r in range(0, len(grid), size):
        row = []
        for c in range(0, len(grid[0]), size):
            row.append(max(grid[r + i][c + j] for i in range(size) for j in range(size)))
        out.append(row)
    return out

feature_map = [[1, 3, 0, 2],
               [4, 6, 1, 0],
               [0, 2, 8, 5],
               [1, 1, 3, 7]]
print(max_pool(feature_map))
```

### Line detector: convolution, ReLU, pooling, decision

This tiny CNN has two fixed kernels, one for horizontal lines and one for vertical lines. It convolves, applies ReLU, takes the global maximum of each feature map, and picks the larger.

```python
def conv2d(img, k):
    n = len(img)
    return [[sum(img[r + i][c + j] * k[i][j] for i in range(3) for j in range(3))
             for c in range(n - 2)] for r in range(n - 2)]

def relu_max(grid):
    return max(max(0, v) for row in grid for v in row)

horizontal = [[-1, -1, -1], [2, 2, 2], [-1, -1, -1]]
vertical = [[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]]

def blank():
    return [[0] * 6 for _ in range(6)]

h_line, v_line, cross = blank(), blank(), blank()
for i in range(1, 5):
    h_line[2][i] = 1
    v_line[i][3] = 1
    cross[2][i] = cross[i][2] = 1

for name, img in [("horizontal line", h_line), ("vertical line", v_line), ("cross", cross)]:
    h = relu_max(conv2d(img, horizontal))
    v = relu_max(conv2d(img, vertical))
    verdict = "horizontal" if h > v else "vertical" if v > h else "both equally"
    print(f"{name:15}: horizontal score {h}, vertical score {v} -> {verdict}")
```

A real CNN does exactly this, except that it learns dozens of kernels per layer instead of using two we chose, stacks many layers, and learns the final decision too.

### Data augmentation by flipping

```python
image = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]
flipped = [row[::-1] for row in image]          # mirror left to right
rotated = [list(row) for row in zip(*image[::-1])]  # rotate 90 degrees clockwise
print("original:", image)
print("flipped: ", flipped)
print("rotated: ", rotated)
```

### Try this

1. Add a diagonal line image. What do the two detectors say? Design a third kernel for diagonals.
2. Pool the feature map with size 4. What single number do you get, and what does it mean?
"""),
        Section("Level check", """
+ Explain max pooling and give three benefits of pooling
+ Describe the layers of a classic CNN and how the shape of the data changes through it
+ Explain receptive fields and the hierarchy of features a CNN learns
+ Name three famous CNN architectures and the key idea each introduced
+ Explain how residual connections work and why they let networks go deeper
+ Describe data augmentation, dropout and transfer learning
"""),
    ],
    keyterms=[
        ("Pooling", "Shrinking a feature map by summarising each small block, usually by its maximum."),
        ("Max pooling", "Keeping only the largest value in each window, such as each 2 × 2 block."),
        ("Flatten", "Turning a volume of feature maps into one long vector for the dense layers."),
        ("Receptive field", "The patch of the original image that one value in a layer depends on."),
        ("Feature hierarchy", "Simple features in early layers combining into complex ones in later layers."),
        ("Residual connection", "A shortcut that adds a block's input to its output, so the block learns only the change: F(x) + x."),
        ("Data augmentation", "Training on modified copies of the data, such as flipped or cropped images, to add variety."),
        ("Dropout", "Randomly switching off neurons during training so the network cannot rely on any one of them."),
        ("Batch normalisation", "Rescaling a layer's outputs during training to keep their mean and spread steady."),
        ("Object detection", "Finding every object in an image, with a bounding box and a label for each."),
        ("Segmentation", "Labelling every pixel of an image with the class it belongs to."),
    ],
    mistakes=[
        "Thinking pooling layers learn something. They have no parameters at all.",
        "Expecting the spatial size to grow through a CNN. It shrinks while the number of channels grows.",
        "Believing deeper always meant better before ResNet. Plain networks got worse past about 20 layers.",
        "Applying augmentation that changes the label, such as flipping a 6 into a 9, or a left arrow into a right arrow.",
        "Forgetting to switch dropout off when using the model. It is only for training.",
    ],
    grade="""
### Why residual connections fix the gradient

In a plain deep network the gradient reaching layer 1 is a product of one factor per layer, so it vanishes or explodes. With a residual block y = F(x) + x, the derivative of y with respect to x is F′(x) + 1. The "+ 1" means that even if F′ is tiny, the gradient passes back almost unchanged along the identity path, and stacking blocks adds paths of every length instead of multiplying one long chain. A ResNet behaves somewhat like an ensemble of many shallower networks.

### The cost of convolution

A convolutional layer's parameter count is small, but its compute is not: a 3 × 3 kernel with 64 input and 64 output channels on a 112 × 112 map needs about 3 × 3 × 64 × 64 × 112 × 112, roughly 460 million multiply-adds, for one image. Efficient architectures such as MobileNet split it into a cheap per-channel convolution and a 1 × 1 convolution that mixes channels (a **depthwise separable** convolution), cutting the cost about eightfold, which is how vision models run on phones.
""",
    quiz=[
        Q("What does 2 × 2 max pooling do to the block [1, 3 / 4, 6]?",
          ["Outputs 6", "Outputs 3.5", "Outputs 14", "Outputs 1"], 0,
          "Max pooling keeps the largest value in the block."),
        Q("How many parameters does a max pooling layer have?",
          ["None", "One per window", "Four for a 2 × 2 window", "The same as the convolution before it"], 0,
          "Pooling just takes a maximum or an average; there is nothing to learn."),
        Q("Through a classic CNN, what happens to the feature maps?",
          ["They get smaller in width and height while the channels increase",
           "They get larger in width and height while the channels decrease",
           "They stay exactly the same size throughout the network",
           "They are turned into text before the final layer"], 0,
          "The network trades position detail for richer descriptions: 'where' for 'what'."),
        Q("What is a receptive field?",
          ["The patch of the original image that one value in a layer depends on",
           "The number of filters in a convolutional layer",
           "The region of an image a person is looking at",
           "The output of the final softmax layer"], 0,
          "It grows with depth, so deeper layers can recognise larger, more complex things."),
        Q("Which features do the first layers of a trained CNN typically detect?",
          ["Edges and colour blobs", "Whole faces", "Words and letters only", "The class labels"], 0,
          "Later layers build parts and whole objects from these simple features."),
        Q("What does a residual connection compute?",
          ["F(x) + x", "F(x) × x", "F(F(x))", "x − F(x)"], 0,
          "The block learns only the change to its input, and the gradient can flow straight along the shortcut."),
        Q("Which network introduced residual connections in 2015?",
          ["ResNet", "LeNet-5", "AlexNet", "VGG-16"], 0,
          "ResNets with 152 layers won ImageNet 2015 with 3.57% top-5 error."),
        Q("Which is a sensible data augmentation for photos of cats and dogs?",
          ["Flipping each image left to right", "Changing the label to the other animal",
           "Deleting half of the images", "Turning every image upside down and relabelling it"], 0,
          "A mirrored cat is still a cat, so the label stays correct."),
        Q("What is dropout?",
          ["Randomly switching off neurons during training", "Removing layers that do not learn",
           "Deleting training examples that are wrong", "Stopping training early"], 0,
          "It stops the network relying on any single neuron and reduces overfitting."),
        Q("A school has 300 labelled photos of local birds. What is the most practical approach?",
          ["Transfer learning from a network pretrained on ImageNet",
           "Training a huge CNN from scratch on the 300 photos",
           "Using a dense network on the raw pixels instead",
           "Collecting no data and guessing the labels"], 0,
          "The pretrained convolutional layers already detect useful features; only a new final layer needs training."),
    ],
    exam=[
        EQ("Describe the structure of a typical convolutional neural network for classifying images.", 5,
           [MP("Convolutional layers with filters detect features", ["convolution", "filter", "kernel"]),
            MP("ReLU activation after each convolution", ["ReLU", "activation"]),
            MP("Pooling layers shrink the feature maps", ["pool", "shrink", "downsample", "max pool"]),
            MP("Repeated, with spatial size shrinking and channels growing", ["repeat", "smaller", "more channels", "more filters", "deeper"]),
            MP("Flatten, dense layers and softmax output", ["flatten", "dense", "fully connected", "softmax"])],
           "A typical CNN starts with convolutional layers, in which many filters slide over the image to detect features, each followed by a ReLU activation. Pooling layers, usually 2 × 2 max pooling, then shrink the feature maps. This pattern of convolution, ReLU and pooling is repeated several times, so the maps get smaller in width and height while the number of channels grows. Finally the volume is flattened into a vector, passed through one or more dense layers, and a softmax output layer gives a probability for each class.",
           command="Describe"),
        EQ("Explain how residual connections allow very deep networks to be trained.", 4,
           [MP("A shortcut adds the block's input to its output: F(x) + x", ["F(x) + x", "shortcut", "skip", "adds the input"]),
            MP("The block only has to learn the change / can pass the input through", ["change", "difference", "residual", "pass through", "identity"]),
            MP("Gradients flow back directly along the shortcut", ["gradient", "flow", "directly", "backpropagat"]),
            MP("So they do not vanish, and early layers still learn", ["vanish", "early layers", "deep", "100", "152"])],
           "A residual connection adds a shortcut around a block of layers, so the block's output is F(x) + x: its input added to whatever the layers compute. The layers therefore only need to learn the change to make to the input, and if nothing helps they can learn to pass the input through unchanged. During backpropagation the gradient flows straight back along the shortcut, so it does not vanish as it passes through many layers, and even the earliest layers receive a strong learning signal. This let networks grow from about 20 layers to more than 150.",
           command="Explain"),
        EQ("Explain how transfer learning helps when only a small dataset is available.", 3,
           [MP("Start from a network pretrained on a large dataset such as ImageNet", ["pretrained", "pre-trained", "ImageNet", "large dataset"]),
            MP("Its early layers already detect general features such as edges and shapes", ["features", "edges", "shapes", "general"]),
            MP("Only a new final layer, or a little fine-tuning, is trained on the small dataset", ["final layer", "last layer", "new layer", "fine-tun", "only train"])],
           "Transfer learning starts from a network that has already been trained on a huge dataset such as ImageNet. Its convolutional layers have already learned to detect general features such as edges, textures, shapes and object parts, which are useful for almost any image task. So only a new final layer, plus perhaps a little fine-tuning of the later layers, needs to be trained on the small dataset, which can work well with only a few hundred examples and far less computing.",
           command="Explain"),
    ],
)

TOPICS = [L8_1, L8_2]
