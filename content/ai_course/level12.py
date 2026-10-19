"""Level 12: Generative AI. Autoencoders, GANs, diffusion and multimodal models."""
from mskbuild.models import Topic, Section, Q, EQ, MP

NEA = "Check you could explain this"

L12_1 = Topic(
    slug="autoencoders-and-gans",
    title="Autoencoders and GANs: Machines That Create",
    spec="12.1",
    icon="i-palette",
    minutes=40,
    exam_title=NEA,
    blurb="How generative models differ from classifiers, autoencoders that squeeze data through a bottleneck, latent spaces you can walk through, variational autoencoders, and generative adversarial networks: a forger and a detective trained against each other, their troubles, and their uses and misuses.",
    fact="By Ian Goodfellow's own account, he came up with generative adversarial networks in 2014 while arguing with friends in a bar in Montreal, went home, and wrote a version that worked that same night.",
    sections=[
        Section("Telling apart, or making new", """
Most of this course so far has been about **discriminative** models: given an input, predict a label. A **generative** model learns what the data itself looks like, well enough to produce new examples that could have come from it.

| | Discriminative | Generative |
| **Learns** | Which label goes with an input | What the data looks like |
| **Answers** | "Is this a cat or a dog?" | "Draw me a new cat." |
| **Examples** | Spam filters, image classifiers | Language models, image generators, music generators |

A language model (Level 11) is a generative model of text: it learns the probability of every sequence of tokens and samples new ones. This level is about generating images, sound and more, where the data is a grid of numbers rather than a sequence of tokens.
"""),
        Section("Autoencoders: squeeze, then rebuild", """
An **autoencoder** is two networks back to back. The **encoder** squeezes the input into a much smaller vector, the **latent code**; the **decoder** tries to rebuild the original from that code alone. Training minimises the **reconstruction error** between input and output.

!diagram ai-autoencoder

A 28 × 28 image has 784 numbers; squeezed through a **bottleneck** of 32, the network cannot copy the image, so it must learn which features matter most: the slant of a stroke, the width of a loop. Uses include:

- **Compression**: store or send the small code instead of the image.
- **Denoising**: train with noisy inputs and clean targets, and the network learns to remove noise.
- **Anomaly detection**: an autoencoder trained only on normal data rebuilds unusual data badly, so a large reconstruction error flags something odd, such as a faulty machine part.
"""),
        Section("Latent space", """
The latent codes form a **latent space**. Because the decoder must rebuild similar inputs from codes, similar inputs end up with nearby codes, just as similar words had nearby embeddings in Level 9.

!diagram ai-latent-space

Walking in a straight line between two codes and decoding each step **morphs** one output into another. Moving in a particular direction can change one property at a time: in a model of faces, one direction might add a smile and another add glasses.
"""),
        Section("Variational autoencoders", """
A plain autoencoder's latent space has gaps: decode a random point between the codes it learned and you may get nonsense. A **variational autoencoder (VAE)**, introduced in 2013, fixes this so that you can **sample** new data:

!diagram ai-vae

1. The encoder outputs a **mean** and a **spread** for each latent number, describing a small cloud rather than a single point.
2. A code is **sampled** from that cloud: z = mean + spread × a random number.
3. The decoder rebuilds the input from z.
4. The loss adds a second term that pulls every cloud towards a standard bell curve centred on zero.

That second term packs the clouds together into one smooth region with no gaps. To create something new, pick a random point from the standard bell curve and decode it.
"""),
        Section("Generative adversarial networks", """
A **generative adversarial network (GAN)**, from 2014, trains two networks against each other:

- The **generator** turns random noise into fake data. It never sees a real example.
- The **discriminator** is shown real examples and fakes, and learns to tell them apart.

!diagram ai-gan

It is a contest between a forger and a detective. Each time the detective gets better at spotting fakes, the gradient of its verdict tells the forger exactly how to change its fakes to be more convincing. They take turns: a few steps training the discriminator, then a few training the generator to make the discriminator answer "real".

!diagram ai-gan-training

In theory the contest ends when the generator's fakes are distributed exactly like the real data. Then the best the discriminator can do is guess, and it outputs 0.5 for everything.
"""),
        Section("Why GANs are hard to train", """
Two networks chasing each other do not always settle down:

- **Mode collapse**: the generator finds a few outputs that fool the discriminator and produces only those, ignoring the variety of the real data.
- **Oscillation**: the two networks circle around each other instead of converging.
- **Vanishing gradients**: if the discriminator becomes too good too fast, its verdicts saturate and give the generator almost no signal to learn from.

!diagram ai-mode-collapse

Because there is no single loss that falls steadily, judging progress is hard too. The usual measure, the **Fréchet Inception Distance (FID)** from 2017, compares statistics of real and generated images inside a trained image classifier: lower is better.
"""),
        Section("GANs in the world", """
| Year | Model | Milestone |
| 2014 | GAN | Blurry but recognisable digits and faces |
| 2015 | DCGAN | Convolutional GANs that train reliably |
| 2016 | pix2pix | Image-to-image translation: sketches to photos, day to night |
| 2017 | CycleGAN | Translation without paired examples: horses into zebras |
| 2017 | Progressive GAN | Photorealistic faces at 1024 × 1024 pixels |
| 2018 | StyleGAN | Control over pose, hair and age; the faces behind thispersondoesnotexist.com |

The same power enables harm. **Deepfakes**, a word coined in 2017, put real people's faces and voices into fake videos, and have been used for fraud, harassment and misinformation. Level 15 covers detection, watermarking and the law; Lesson 12.2 shows the newer method that has largely replaced GANs for image generation.
"""),
        Section("Hands-on: an autoencoder and a GAN", """
### A two-into-one autoencoder

Forty points lie close to the line y = 2x. The encoder squeezes each point's two numbers into one, and the decoder rebuilds two numbers from that one. To rebuild well, the network has to discover the line.

```python
import random

random.seed(1)
data = []
for _ in range(40):
    t = random.uniform(-1, 1)
    data.append((t + random.gauss(0, 0.05), 2 * t + random.gauss(0, 0.05)))

enc = [0.3, -0.2]          # encoder: z = enc . x       (2 numbers squeezed into 1)
dec = [0.1, 0.4]           # decoder: x' = dec * z      (1 number expanded back into 2)
lr = 0.05
for epoch in range(301):
    total = 0.0
    for x in data:
        z = enc[0] * x[0] + enc[1] * x[1]
        rec = [dec[0] * z, dec[1] * z]
        err = [rec[0] - x[0], rec[1] - x[1]]
        total += err[0] ** 2 + err[1] ** 2
        g_dec = [2 * err[0] * z, 2 * err[1] * z]
        g_z = 2 * (err[0] * dec[0] + err[1] * dec[1])
        g_enc = [g_z * x[0], g_z * x[1]]
        dec = [d - lr * g for d, g in zip(dec, g_dec)]
        enc = [e - lr * g for e, g in zip(enc, g_enc)]
    if epoch % 60 == 0:
        print(f"epoch {epoch:3}: reconstruction error {total / len(data):.4f}")

print("decoder direction:", [round(d / dec[0], 2) for d in dec], "(the line y = 2x is [1, 2])")
for x in sorted(data)[:3] + sorted(data)[-3:]:
    z = enc[0] * x[0] + enc[1] * x[1]
    print(f"point ({x[0]:5.2f}, {x[1]:5.2f}) -> latent {z:5.2f} -> rebuilt ({dec[0] * z:5.2f}, {dec[1] * z:5.2f})")
```

### A GAN in one dimension

The real data are numbers with mean 4 and spread 1.25. The generator starts by producing numbers with mean 0 and spread 1, and only ever learns from the discriminator's verdicts.

```python
import math, random

random.seed(2)
def sigmoid(v):
    return 1 / (1 + math.exp(-max(-30.0, min(30.0, v))))

real_mean, real_sd = 4.0, 1.25          # the "real data" the generator never sees directly
a, b = 1.0, 0.0                         # generator: x = a * noise + b
w1, w2, c = 0.0, 0.0, 0.0               # discriminator: D(x) = sigmoid(w1 u + w2 u^2 + c), u = x / 4

def D(x):
    u = x / 4
    return sigmoid(w1 * u + w2 * u * u + c), u

for step in range(1501):
    # 1. the discriminator learns to say 1 for real examples and 0 for fakes
    gw1 = gw2 = gc = 0.0
    for _ in range(8):
        for x, label in ((random.gauss(real_mean, real_sd), 1), (a * random.gauss(0, 1) + b, 0)):
            d, u = D(x)
            gw1 += (d - label) * u
            gw2 += (d - label) * u * u
            gc += d - label
    w1 -= 1.0 * gw1 / 8
    w2 -= 1.0 * gw2 / 8
    c -= 1.0 * gc / 8
    # 2. the generator learns to make the discriminator say 1
    ga = gb = 0.0
    for _ in range(8):
        z = random.gauss(0, 1)
        d, u = D(a * z + b)
        g_x = -(1 - d) * (w1 + 2 * w2 * u) / 4      # how -log D changes as the fake moves
        ga += g_x * z
        gb += g_x
    a -= 0.05 * ga / 8
    b -= 0.05 * gb / 8
    if step % 250 == 0:
        print(f"step {step:4}: fakes have mean {b:5.2f} and spread {abs(a):4.2f};  D(4) = {D(4)[0]:.2f}")
print(f"real data:  mean {real_mean:5.2f} and spread {real_sd:4.2f}")
```

Watch the spread overshoot and swing back: the two players chase each other around the answer, and D(4) hovers near 0.5 once the fakes are convincing.

### Try this

1. In the autoencoder, change the data to lie along y = −x. Which direction does the decoder find?
2. In the GAN, change the generator's learning rate from 0.05 to 0.5. What happens to the spread?
"""),
        Section("Level check", """
+ Distinguish discriminative and generative models, with examples
+ Describe an autoencoder, its bottleneck and its reconstruction loss
+ Give three uses of autoencoders
+ Explain what a latent space is and what interpolating in it does
+ Explain how a VAE makes its latent space suitable for sampling
+ Describe how a GAN's generator and discriminator are trained against each other
+ Explain mode collapse and why GAN training is unstable
+ Discuss the benefits and harms of generated images
"""),
    ],
    keyterms=[
        ("Generative model", "A model that learns what data looks like, so it can produce new examples."),
        ("Discriminative model", "A model that learns to predict a label from an input."),
        ("Autoencoder", "An encoder and a decoder trained to rebuild their input through a small bottleneck."),
        ("Latent code", "The small vector an encoder produces; the compressed description of one input."),
        ("Latent space", "The space of all latent codes, in which similar inputs lie close together."),
        ("Reconstruction error", "How different an autoencoder's output is from its input."),
        ("Variational autoencoder (VAE)", "An autoencoder whose codes are sampled from learned clouds pulled towards a standard bell curve, so new data can be sampled."),
        ("Generative adversarial network (GAN)", "A generator and a discriminator trained against each other."),
        ("Generator", "The network in a GAN that turns random noise into fake data."),
        ("Discriminator", "The network in a GAN that learns to tell real data from fakes."),
        ("Mode collapse", "When a generator produces only a few kinds of output instead of the data's full variety."),
        ("Deepfake", "Realistic generated media that puts a real person's face or voice into something they never did."),
    ],
    mistakes=[
        "Thinking an autoencoder is useful because its output matches its input. The point is the small code it is forced to learn.",
        "Believing the generator copies training images. It never sees them; it learns only from the discriminator's verdicts.",
        "Assuming a GAN's losses fall steadily like a classifier's. They rise and fall as the two networks compete.",
        "Thinking a discriminator at 0.5 is broken. When the fakes match the real data perfectly, 0.5 is the best possible answer.",
        "Sampling from a plain autoencoder's latent space and expecting good results. Only a VAE's latent space is shaped for sampling.",
    ],
    grade="""
### The optimal discriminator

For a fixed generator, the best possible discriminator can be written down exactly. If p~data~(x) is how likely x is under the real data and p~g~(x) under the generator, then

D*(x) = p~data~(x) ÷ (p~data~(x) + p~g~(x))

Where the generator makes too many of something, D* is below 0.5; where it makes too few, above 0.5. Training the generator against this D* turns out to minimise the **Jensen–Shannon divergence**, a measure of the difference between the two distributions, which is zero exactly when they are equal, and then D*(x) = 0.5 everywhere.

### Wasserstein GANs

When the real and fake distributions barely overlap, the Jensen–Shannon divergence stops changing and the generator's gradients vanish. **Wasserstein GANs** (2017) instead measure the "earth mover's distance": how much probability has to be moved, and how far, to turn one distribution into the other. It keeps shrinking smoothly as the fakes improve, which made GAN training far more stable.
""",
    quiz=[
        Q("What does a generative model learn?",
          ["What the data looks like, so it can produce new examples", "Which label goes with each input",
           "How to compress files without any loss", "Which features to delete from the data"], 0,
          "A discriminative model learns labels; a generative model learns the data itself."),
        Q("Why does an autoencoder have a small bottleneck in the middle?",
          ["So it cannot simply copy the input and must learn its key features", "To make training faster",
           "To stop the decoder seeing any information", "To increase the number of parameters"], 0,
          "With too few numbers to copy everything, it has to keep what matters most."),
        Q("An autoencoder trained on normal engine sounds rebuilds a new sound badly. What might that mean?",
          ["The sound is unusual, and the engine may be faulty", "The autoencoder has learned perfectly",
           "The sound must be louder than usual", "The bottleneck is too large"], 0,
          "Large reconstruction error is a sign of data unlike the training data: anomaly detection."),
        Q("What happens when you decode points along a straight line between two latent codes?",
          ["The output morphs smoothly from one example to the other", "The decoder always outputs noise",
           "The two examples are averaged pixel by pixel", "The model forgets both examples"], 0,
          "Nearby codes decode to similar outputs, so the path gives a smooth morph."),
        Q("What extra term does a variational autoencoder add to its loss?",
          ["A pull of each code's cloud towards a standard bell curve", "A penalty on the size of the images",
           "A reward for using fewer layers", "A count of the training examples"], 0,
          "It packs the latent space smoothly, so random samples decode to sensible outputs."),
        Q("In a GAN, what does the generator receive as input?",
          ["Random noise", "Real training images", "The labels of the images", "The discriminator's weights"], 0,
          "It learns to turn noise into convincing data using only the discriminator's verdicts."),
        Q("How does the generator learn to improve its fakes?",
          ["From the gradient of the discriminator's verdict on its fakes", "By copying the real images it is shown",
           "From a list of mistakes written by people", "By deleting its worst fakes"], 0,
          "The gradient shows how to change each fake to look more real to the discriminator."),
        Q("A GAN's generator produces only two kinds of face, though the data has many. What is this called?",
          ["Mode collapse", "Overfitting", "Vanishing gradients", "Data augmentation"], 0,
          "The generator found a few outputs that fool the discriminator and stopped exploring."),
        Q("When a GAN's generator perfectly matches the real data, what does the best discriminator output?",
          ["0.5 for every input", "1 for every input", "0 for every input", "Random numbers"], 0,
          "Real and fake are then indistinguishable, so it can only guess."),
        Q("Which of these is a misuse of generative models?",
          ["A video putting a real politician's face onto words they never said", "Turning a sketch into a photo",
           "Removing noise from an old photograph", "Creating faces of people who do not exist for a game"], 0,
          "Deepfakes of real people can deceive, defraud and harass."),
    ],
    exam=[
        EQ("Describe how an autoencoder is trained, and explain one use of it.", 4,
           [MP("An encoder compresses the input into a small latent code / bottleneck", ["encoder", "compress", "latent", "bottleneck", "small"]),
            MP("A decoder rebuilds the input from the code", ["decoder", "rebuild", "reconstruct"]),
            MP("Trained to minimise the reconstruction error between input and output", ["reconstruction", "error", "difference", "loss"]),
            MP("A use, explained: compression, denoising or anomaly detection", ["compress", "denois", "anomal", "unusual", "fault"])],
           "An autoencoder has an encoder that compresses the input, such as an image, into a much smaller latent code, and a decoder that tries to rebuild the original from that code. Both are trained together by gradient descent to minimise the reconstruction error, the difference between the input and the rebuilt output, so the code is forced to capture the most important features. One use is anomaly detection: an autoencoder trained only on normal data rebuilds unusual data badly, so a large reconstruction error flags, for example, a faulty machine part.",
           command="Describe"),
        EQ("Explain how a generative adversarial network is trained.", 5,
           [MP("A generator turns random noise into fake data", ["generator", "noise", "fake"]),
            MP("A discriminator is trained to tell real data from fakes", ["discriminator", "real", "tell apart", "classif"]),
            MP("The generator is trained to make the discriminator classify its fakes as real", ["fool", "classify as real", "say real", "think"]),
            MP("They are trained alternately / take turns", ["altern", "turn", "then"]),
            MP("Using the gradient of the discriminator's output with respect to the fakes", ["gradient", "backprop"]),
            MP("Ideally until fakes match the data and the discriminator outputs 0.5", ["0.5", "match", "indistinguishable", "guess"])],
           "A GAN has two networks. The generator takes random noise and turns it into fake data; the discriminator is shown both real examples and fakes and is trained to output 1 for real and 0 for fake. Training alternates between them: the discriminator takes a step to get better at spotting fakes, then the generator takes a step to make the discriminator call its fakes real, using the gradient of the discriminator's verdict, backpropagated through the discriminator into the generator. Ideally the contest continues until the fakes are distributed like the real data and the discriminator can only guess, outputting 0.5.",
           command="Explain"),
        EQ("Explain why a variational autoencoder can generate new data when a plain autoencoder usually cannot.", 3,
           [MP("A plain autoencoder's latent space has gaps; random points decode to nonsense", ["gap", "nonsense", "random point", "anywhere"]),
            MP("A VAE's encoder outputs a mean and spread, and codes are sampled from that cloud", ["mean", "spread", "variance", "sample", "distribution"]),
            MP("An extra loss term pulls the clouds towards a standard bell curve, filling the space smoothly", ["standard", "bell", "normal", "KL", "smooth"]),
            MP("So a random sample from the standard bell curve decodes to a sensible new example", ["random sample", "new example", "decode", "new data"])],
           "A plain autoencoder maps each input to a single point, and the points it learns are scattered with gaps between them, so a random latent point often decodes to nonsense. A VAE's encoder instead outputs a mean and a spread, and the code is sampled from that small cloud, while an extra loss term pulls every cloud towards a standard bell curve centred on zero. This packs the codes into one smooth region without gaps, so a random sample from the standard bell curve decodes to a sensible new example.",
           command="Explain"),
    ],
)

L12_2 = Topic(
    slug="diffusion-and-multimodal",
    title="Diffusion Models and Multimodal AI",
    spec="12.2",
    icon="i-image",
    minutes=44,
    exam_title=NEA,
    blurb="How diffusion models learn to turn noise into pictures by learning to remove it, guidance by text prompts, latent diffusion, CLIP's shared space for images and words, models that see, hear and speak, and how generated media can be labelled.",
    fact="The first diffusion model, in 2015, borrowed its maths from the physics of how ink spreads through water. It took until 2020 for the method to make convincing images, and until 2021 for it to beat GANs.",
    sections=[
        Section("Destroy, then learn to repair", """
A **diffusion model** learns to generate by learning to undo damage.

- The **forward process** takes a real image and adds a little random noise, again and again, for hundreds of steps, until nothing is left but noise. This part needs no learning at all.
- The **reverse process** is learned: a network is trained to remove a little noise at a time. Run it from pure noise and an image appears.

!diagram ai-diffusion-forward

After t steps, the noisy image is a mix of the original and fresh noise:

!info The forward process :: noisy image = √ᾱ~t~ × image + √(1 − ᾱ~t~) × noise, where ᾱ~t~ falls from 1 towards 0 as t grows

With the 2020 schedule of 1,000 steps, after step 250 the mix is 0.72 × image + 0.69 × noise; after step 500, 0.28 × image + 0.96 × noise; and by step 1,000, almost pure noise.
"""),
        Section("Training the denoiser", """
Training is a simple loop:

1. Take a training image and pick a random step t.
2. Make random noise, and mix it with the image as the forward process would at step t.
3. Ask the network: given this noisy image and the number t, what noise was added?
4. The loss is the squared difference between the real noise and the predicted noise.

!diagram ai-denoiser-training

The network is usually a **U-Net**, a convolutional network that shrinks the image to find its overall layout and then grows it back, with skip connections carrying fine detail across; newer models use transformers instead. Because the network only ever has to remove a little noise, every training example is a small, well-defined task.
"""),
        Section("Generating: noise to picture", """
To generate, start with pure random noise and repeat: predict the noise, remove some of it, and add back a little less noise than before. Over 20 to 1,000 steps an image condenses out of the static.

!diagram ai-diffusion-reverse

Early steps decide the overall layout and colours; later steps add edges and fine detail. Because every run starts from different random noise, every run gives a different image.

The lab below does exactly this to points on a plane: drag the steps, pick a shape, and watch noise flow into it.

!tool diffusion-lab
"""),
        Section("Steering with words", """
To draw "a red fox in the snow", the denoiser needs to know what was asked. The prompt is turned into embeddings by a **text encoder**, and the denoiser reads them through **cross-attention** (Level 10): every patch of the image can attend to every word.

**Classifier-free guidance** (2021) makes the image follow the prompt more closely. At each step the network predicts the noise twice, once with the prompt and once without, and the step is pushed further in the direction the prompt made:

!info Classifier-free guidance :: noise used = noise without prompt + w × (noise with prompt − noise without prompt), with a guidance scale w often around 7

!diagram ai-guidance

A higher guidance scale follows the prompt more literally but gives less varied, sometimes over-saturated images.
"""),
        Section("Latent diffusion", """
A 512 × 512 colour image holds 786,432 numbers, and denoising all of them for every step is slow. **Latent diffusion** (2021), the method behind Stable Diffusion (2022), first trains an autoencoder (Lesson 12.1) that squeezes an image into a 64 × 64 × 4 latent: 16,384 numbers, 48 times fewer. Diffusion then happens entirely in that latent space, and the decoder turns the final latent into the picture.

!diagram ai-latent-diffusion

| Year | Model | Milestone |
| 2020 | DDPM | Diffusion makes convincing images |
| 2021 | Guided diffusion | Diffusion beats GANs on image quality |
| 2022 | DALL·E 2, Imagen, Midjourney, Stable Diffusion | Text-to-image for everyone; Stable Diffusion's weights are released openly |
| 2024 | Video diffusion transformers | Minute-long video clips from text |
"""),
        Section("CLIP: one space for pictures and words", """
How does a text encoder know which words go with which pictures? **CLIP** (2021) was trained on 400 million images with their captions from the web. It has two encoders, one for images and one for text, trained with **contrastive learning**:

!diagram ai-clip

In every batch, the true image–caption pairs, on the diagonal, are pushed to have high cosine similarity, and every mismatched pair is pushed low. The result is one shared space where a photo of a dog lands near the words "a photo of a dog".

That enables **zero-shot classification**: to sort images into new categories, embed captions such as "a photo of a fox" and "a photo of a hare", and pick the caption closest to the image, with no extra training.
"""),
        Section("Models that see, hear and speak", """
A **multimodal** model works with more than one kind of data: text, images, audio or video.

| Input | Output | Example task |
| Image + text | Text | Describe a photo, read a chart, answer a question about a diagram |
| Text | Image | Generate an illustration from a description |
| Speech | Text | Speech recognition: Whisper (2022) was trained on 680,000 hours of audio |
| Text | Speech | Natural-sounding reading aloud in many voices |
| Text | Video | Short clips generated by diffusion over space and time |

The common trick is to turn every kind of data into tokens or embeddings: image patches (Level 10's Vision Transformer), slices of audio, frames of video. Once everything is a sequence of vectors, one transformer can attend across all of them.
"""),
        Section("Real or generated?", """
Generated images and voices are now good enough to fool people, and detectors that guess from the pixels alone are unreliable. Two other approaches help:

- **Watermarking**: the generator hides a signal in its output, invisible to people but detectable by software, as Google DeepMind's SynthID (2023) does for images, audio and text.
- **Provenance**: standards such as **C2PA** content credentials attach signed records of how a file was made and edited, so a photo can show that it came from a real camera.

Generative AI also raises questions of **consent and copyright**: models are trained on artists' work, photographers' photos and people's faces, often without asking. Level 15 returns to these questions.
"""),
        Section("Hands-on: diffusion from scratch", """
### How much image is left?

```python
import math

T = 1000
betas = [0.0001 + (0.02 - 0.0001) * t / (T - 1) for t in range(T)]   # a little more noise each step
alpha_bar, keep = [], 1.0
for b in betas:
    keep *= 1 - b
    alpha_bar.append(keep)

for t in [1, 50, 100, 250, 500, 750, 1000]:
    signal = math.sqrt(alpha_bar[t - 1])
    noise = math.sqrt(1 - alpha_bar[t - 1])
    print(f"after step {t:4}: noisy image = {signal:.3f} x image + {noise:.3f} x noise")
```

### Noise into a ring

The training data are 60 points on a ring. With so little data, the best possible denoiser can be written exactly: a softmax-weighted average of the data points, weighted by how well each explains the noisy point. That is the same softmax you used for attention. Each generated point starts as pure random noise.

```python
import math, random

random.seed(0)
data = [(math.cos(2 * math.pi * k / 60), math.sin(2 * math.pi * k / 60)) for k in range(60)]   # a ring

T = 40
def alpha_bar(t):                       # how much of the clean point survives after t steps
    return math.cos((t / T + 0.008) / 1.008 * math.pi / 2) ** 2

def denoise(x, t):
    # The best possible guess of the clean point: a softmax-weighted average of the data
    a, s = math.sqrt(alpha_bar(t)), math.sqrt(1 - alpha_bar(t))
    scores = [-((x[0] - a * d[0]) ** 2 + (x[1] - a * d[1]) ** 2) / (2 * s * s) for d in data]
    m = max(scores)
    w = [math.exp(v - m) for v in scores]
    total = sum(w)
    return (sum(wi * d[0] for wi, d in zip(w, data)) / total,
            sum(wi * d[1] for wi, d in zip(w, data)) / total)

def generate():
    x = (random.gauss(0, 1), random.gauss(0, 1))          # start from pure noise
    for t in range(T, 0, -1):
        a, s = math.sqrt(alpha_bar(t)), math.sqrt(1 - alpha_bar(t))
        x0 = denoise(x, t)
        eps = ((x[0] - a * x0[0]) / s, (x[1] - a * x0[1]) / s)         # the noise it thinks is there
        a2, s2 = math.sqrt(alpha_bar(t - 1)), math.sqrt(1 - alpha_bar(t - 1))
        x = (a2 * x0[0] + s2 * eps[0], a2 * x0[1] + s2 * eps[1])        # remove a little of it
    return x

def plot(points):
    grid = [[" "] * 41 for _ in range(19)]
    for x, y in points:
        col, row = round(20 + x * 13), round(9 - y * 6)
        if 0 <= row < 19 and 0 <= col < 41:
            grid[row][col] = "o"
    for r in grid:
        print("|" + "".join(r) + "|")

samples = [generate() for _ in range(80)]
plot(samples)
radius = sum(math.hypot(x, y) for x, y in samples) / len(samples)
print(f"average distance from the centre: {radius:.3f} (the ring has radius 1)")
```

### Zero-shot matching, CLIP style

The embeddings below are made up, four numbers each, to show the idea; CLIP's have 512.

```python
import math

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

photo = [0.9, 0.1, 0.8, 0.0]            # pretend image embedding: a dog on a beach
captions = {
    "a photo of a dog": [0.8, 0.0, 0.3, 0.1],
    "a photo of a cat": [0.1, 0.9, 0.2, 0.0],
    "a photo of a beach": [0.3, 0.0, 0.9, 0.1],
    "a photo of a dog on a beach": [0.7, 0.0, 0.7, 0.05],
    "a diagram of a car engine": [0.0, 0.1, 0.0, 0.9],
}
for text, vec in sorted(captions.items(), key=lambda kv: -cosine(photo, kv[1])):
    print(f"{cosine(photo, vec):.3f}  {text}")
```

### Try this

1. In the ring program, change T to 5 and then to 200. How does the picture change?
2. Replace the ring with two clusters, 30 points near (−1, 0) and 30 near (1, 0). What do the generated points do?
"""),
        Section("Level check", """
+ Describe the forward and reverse processes of a diffusion model
+ Explain how the denoiser is trained to predict noise
+ Explain how text steers generation through cross-attention and classifier-free guidance
+ Explain why latent diffusion is faster than diffusion on pixels
+ Describe how CLIP is trained with contrastive learning and how zero-shot classification works
+ Give examples of multimodal models and how they turn every kind of data into vectors
+ Explain watermarking and provenance for generated media
"""),
    ],
    keyterms=[
        ("Diffusion model", "A generative model that creates data by learning to remove noise, step by step."),
        ("Forward process", "Adding noise to data over many steps until only noise remains; it involves no learning."),
        ("Reverse process", "The learned, step-by-step removal of noise that turns pure noise into data."),
        ("Noise schedule", "How much noise is added at each step of the forward process."),
        ("U-Net", "A convolutional network that shrinks and then regrows an image, with skip connections, used as a denoiser."),
        ("Classifier-free guidance", "Pushing each denoising step further in the direction the prompt makes, to follow the prompt more closely."),
        ("Latent diffusion", "Running diffusion on an autoencoder's small latent version of an image instead of its pixels."),
        ("CLIP", "A pair of image and text encoders trained so that matching images and captions have similar embeddings."),
        ("Contrastive learning", "Training that pulls matching pairs together and pushes mismatched pairs apart."),
        ("Zero-shot classification", "Classifying into categories never trained on, by comparing with embeddings of their descriptions."),
        ("Multimodal model", "A model that works with more than one kind of data, such as text, images and audio."),
        ("Watermark", "A hidden signal in generated content that software can detect."),
        ("Provenance", "A signed record of where a piece of media came from and how it was edited."),
    ],
    mistakes=[
        "Thinking a diffusion model pastes together pieces of training images. It starts from random noise and removes it step by step.",
        "Believing the forward process is learned. Adding noise is fixed; only the removal is learned.",
        "Assuming more guidance is always better. High guidance scales reduce variety and can make images look harsh.",
        "Thinking latent diffusion makes lower-quality images because the latent is small. The decoder restores the detail.",
        "Trusting that a detector can always spot generated media. Watermarks and provenance records are more reliable than guessing from pixels.",
    ],
    grade="""
### Memorising versus generalising

The ring program's denoiser is perfect for its 60 training points, and that is a problem: every generated point lands exactly on a training point, so it can only ever reproduce its data. Real diffusion models generalise because their networks cannot store billions of images exactly and are forced to learn smooth rules instead. Researchers have still found that large models occasionally reproduce near-copies of images that appeared many times in their training data, which matters for privacy and copyright.

### Fewer steps

A thousand network evaluations per image is slow. Deterministic samplers such as **DDIM** (2020), the update the ring program uses, give good images in 20 to 50 steps, and **distillation** trains a student to jump through several steps at once, down to one to four steps. **Flow matching**, used by several recent image models, learns straighter paths from noise to data that need fewer steps to follow.
""",
    quiz=[
        Q("What does the forward process of a diffusion model do?",
          ["Adds noise to an image step by step until only noise remains", "Removes noise from an image step by step",
           "Compresses an image into a latent code", "Turns a text prompt into embeddings"], 0,
          "It needs no learning; the network learns to reverse it."),
        Q("What is the denoising network usually trained to predict?",
          ["The noise that was added to the image", "The text prompt of the image",
           "The label of the image", "The next pixel of the image"], 0,
          "The loss is the squared difference between the real and predicted noise."),
        Q("Why does every generation run give a different image?",
          ["Each run starts from different random noise", "The network's weights change during generation",
           "The prompt is shuffled before each run", "The model picks a random training image"], 0,
          "Different starting noise leads the reverse process to a different picture."),
        Q("How does a text prompt influence the denoiser?",
          ["Through cross-attention from the image to the prompt's embeddings", "It is added to the final image as pixels",
           "It replaces the random starting noise", "It chooses which training image to copy"], 0,
          "Every part of the image can attend to every word, as in Level 10."),
        Q("What happens when the classifier-free guidance scale is raised?",
          ["Images follow the prompt more closely but vary less", "Images ignore the prompt",
           "Generation needs no steps at all", "The images become larger"], 0,
          "The step is pushed further in the direction the prompt makes."),
        Q("Why is latent diffusion faster than diffusion on pixels?",
          ["It denoises a small latent with far fewer numbers than the image", "It skips the decoder",
           "It uses only one denoising step", "It works on black-and-white images only"], 0,
          "A 64 × 64 × 4 latent holds 16,384 numbers, 48 times fewer than a 512 × 512 colour image."),
        Q("How is CLIP trained?",
          ["Matching pairs of images and captions are pulled together, others apart", "By generating images from captions",
           "By predicting the next word of each caption", "By sorting images into 1,000 labelled classes"], 0,
          "This contrastive learning gives one shared space for pictures and words."),
        Q("How can CLIP classify images into categories it was never trained on?",
          ["By picking the caption embedding closest to the image embedding", "By retraining the model on each new category first",
           "By asking people to label the images", "By guessing at random"], 0,
          "Captions such as \"a photo of a fox\" are embedded and compared: zero-shot classification."),
        Q("A 512 × 512 colour image holds how many numbers?",
          ["786,432", "262,144", "16,384", "1,536"], 0,
          "512 × 512 pixels × 3 colour channels = 786,432."),
        Q("What does a C2PA content credential provide?",
          ["A signed record of how a file was made and edited", "A guarantee that an image is beautiful",
           "Faster image generation", "A copy of the training data"], 0,
          "Provenance shows where media came from instead of guessing from the pixels."),
    ],
    exam=[
        EQ("Explain how a diffusion model is trained and how it generates a new image.", 6,
           [MP("Forward process: noise is added to a training image over many steps", ["add noise", "adds noise", "forward", "noisier"]),
            MP("A random step is chosen and the image mixed with noise for that step", ["random step", "step t", "mix"]),
            MP("The network is trained to predict the noise that was added", ["predict the noise", "predicts the noise", "noise that was added"]),
            MP("Loss: squared difference between the real and predicted noise", ["squared", "difference", "loss"]),
            MP("Generation starts from pure random noise", ["pure noise", "random noise", "start from noise", "starts from noise"]),
            MP("The predicted noise is removed a little at a time over many steps until an image appears", ["remove", "step by step", "many steps", "gradually"])],
           "During training, a training image has noise added as the forward process would after a randomly chosen step t, so the image is partly destroyed. The network, usually a U-Net, is given the noisy image and the step number and trained to predict exactly what noise was added, with the loss being the squared difference between the real noise and its prediction. To generate a new image, the model starts from pure random noise and repeatedly predicts the noise present and removes a little of it, over many steps, so that an image gradually emerges; starting from different noise gives a different image.",
           command="Explain"),
        EQ("Explain how CLIP is trained and how it can be used to classify images without further training.", 4,
           [MP("An image encoder and a text encoder map images and captions into one shared space", ["two encoders", "image encoder", "text encoder", "shared space"]),
            MP("Trained on many image–caption pairs: matching pairs are pulled together, mismatched pairs pushed apart", ["matching", "contrastive", "pull", "push", "mismatch"]),
            MP("To classify, captions such as 'a photo of a ...' are written for each category and embedded", ["a photo of", "caption", "each category", "label"]),
            MP("The category whose caption embedding is most similar to the image embedding is chosen", ["most similar", "closest", "cosine", "highest"])],
           "CLIP has an image encoder and a text encoder that map into one shared embedding space. It was trained on hundreds of millions of images with their captions using contrastive learning: in each batch, the true image–caption pairs are pushed to have high cosine similarity and every mismatched pair low. To classify an image into new categories, a caption such as \"a photo of a fox\" is written for each category and embedded, the image is embedded, and the category whose caption is most similar to the image is chosen, with no extra training: zero-shot classification.",
           command="Explain"),
        EQ("Evaluate two ways of telling whether an image was made by AI.", 4,
           [MP("Detectors that guess from the pixels can be fooled and become outdated as generators improve", ["detector", "pixels", "unreliable", "fooled", "outdated"]),
            MP("Watermarking hides a signal in generated content that software can detect", ["watermark", "hidden signal", "SynthID"]),
            MP("Watermarks only work if the generator adds them, and may be removed by editing", ["only if", "removed", "editing", "all generators", "cropping"]),
            MP("Provenance records such as C2PA credentials show how media was made, but can be stripped / need wide adoption", ["provenance", "C2PA", "credential", "stripped", "adopt"])],
           "One approach is a detector that looks at an image's pixels for signs of generation, but such detectors are unreliable: they make mistakes on new generators and can be fooled by small edits, so they become outdated as generators improve. A second approach is watermarking, where the generator hides a signal in its output that software can later detect, as SynthID does; this is far more reliable when present, but only works if the generator adds it, and heavy editing may remove it. Provenance records such as C2PA content credentials complement this by recording how a genuine photo was made and edited, but they need cameras and apps to adopt them, and metadata can be stripped, so no single method is enough on its own.",
           command="Evaluate"),
    ],
)

TOPICS = [L12_1, L12_2]
