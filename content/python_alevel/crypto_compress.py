"""A Level Python: compression, encryption and hashing, written from scratch."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="compression-encryption-hashing",
    title="Compression, Encryption and Hashing",
    spec="A Level 19",
    icon="i-lock",
    minutes=70,
    blurb="Data exchange from the inside. Write run length encoding, dictionary coding and Huffman coding, break a Caesar cipher by frequency analysis, use the unbreakable one-time pad, build RSA and Diffie-Hellman with tiny numbers, and learn why passwords are salted and stretched, with every algorithm short enough to read.",
    fact="The Caesar cipher is named after Julius Caesar, who used a shift of three to send military messages. It was strong enough then because most enemies could not read at all. Today a computer breaks it in less time than it takes to blink, which is why it is only ever used to teach.",
    sections=[
        Section("Compression: run length and dictionary coding", r"""
**Compression** reduces the number of bits needed to store or send data. Files take less room, and downloads finish sooner. The saving is measured by the **compression ratio**: original size divided by compressed size. A 1000 byte file that becomes 250 bytes has a ratio of 4 to 1.

There are two kinds:

| | Lossless | Lossy |
| The original | can be rebuilt **exactly** | cannot: some information is **discarded for good** |
| Used for | text, program files, data, PNG, ZIP, FLAC | photographs (JPEG), music (MP3), video (MP4) |
| Why | one changed bit could ruin a program | the detail removed is hard for people to notice |

### Run length encoding

**Run length encoding** (RLE) replaces each run of the same symbol with a count and the symbol. `AAAABBBCCD` becomes `4A3B2C1D`.

```python
def rle_encode(text):
    coded, i = "", 0
    while i < len(text):
        j = i
        while j < len(text) and text[j] == text[i]:
            j += 1                              # find the end of the run
        coded += str(j - i) + text[i]
        i = j
    return coded

def rle_decode(coded):
    text, count = "", ""
    for ch in coded:
        if ch.isdigit():
            count += ch
        else:
            text += ch * int(count)
            count = ""
    return text

row = "WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW"
for data in ["AAAABBBCCD", row, "ABCD"]:
    coded = rle_encode(data)
    print(len(data), "->", len(coded), coded[:40], rle_decode(coded) == data)
```

RLE is excellent for data with long runs, such as a row of a simple cartoon image or a diagram. On data with no runs it makes things **worse**: `ABCD` doubles in size.

### Dictionary coding

Text repeats itself: words, phrases, whole sentences. **Dictionary coding** replaces a repeated sequence with a short reference to an earlier one. The popular version, **LZW**, never sends the dictionary at all. The compressor and the decompressor both build the same dictionary as they go, adding a new entry every time they see a sequence that is new.

```python
def lzw_compress(text):
    dictionary = {chr(i): i for i in range(256)}       # to start, one entry for every character
    next_code, current, out = 256, "", []
    for ch in text:
        if current + ch in dictionary:
            current += ch                              # keep growing the known sequence
        else:
            out.append(dictionary[current])
            dictionary[current + ch] = next_code       # learn the new sequence
            next_code += 1
            current = ch
    if current:
        out.append(dictionary[current])
    return out

def lzw_decompress(codes):
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256
    previous = dictionary[codes[0]]
    out = [previous]
    for code in codes[1:]:
        entry = dictionary[code] if code in dictionary else previous + previous[0]
        out.append(entry)
        dictionary[next_code] = previous + entry[0]
        next_code += 1
        previous = entry
    return "".join(out)

sample = "TOBEORNOTTOBEORTOBEORNOT"
codes = lzw_compress(sample)
print(codes)
print(len(sample), "characters became", len(codes), "codes;", lzw_decompress(codes) == sample)

lines = "the cat sat on the mat and the cat sat on the hat " * 4
codes = lzw_compress(lines)
print(len(lines), "characters became", len(codes), "codes;", lzw_decompress(codes) == lines)
```

The codes above 255 are references to sequences learned from earlier in the text. The more repetition there is, the better it does. GIF uses LZW. ZIP, gzip and PNG use a relative called **DEFLATE**, which combines dictionary coding with Huffman coding, covered next. Python's `zlib` module is that algorithm:

```python
import random
import zlib

text = ("the quick brown fox jumps over the lazy dog " * 40).encode()
print(len(text), "bytes became", len(zlib.compress(text)))

rng = random.Random(5)
noise = bytes(rng.randrange(256) for _ in range(2000))
print("random bytes get smaller:", len(zlib.compress(noise)) < len(noise))
```

Data with no pattern cannot be compressed. That is why compressing a file that is already compressed makes no difference.

### Lossy compression

A lossy method keeps what matters most and throws the rest away. The simplest way is to reduce **precision**. This stores a brightness from 0 to 255 using only 3 bits (8 levels):

```python
samples = [12, 47, 83, 130, 131, 200, 254, 90, 61, 17]
levels = 8
step = 256 // levels

coded = [s // step for s in samples]                  # 3 bits each instead of 8
rebuilt = [c * step + step // 2 for c in coded]       # the middle of each band

print("stored   :", coded)
print("rebuilt  :", rebuilt)
print("original :", samples)
print("largest error:", max(abs(a - b) for a, b in zip(samples, rebuilt)))
print("space saved:", 100 * (8 - 3) / 8, "%")
```

The rebuilt values are close but not equal, and the original can **never** be recovered. JPEG and MP3 are far more clever, discarding the detail the eye and ear are worst at noticing, but the idea is the same.
"""),
        Section("Huffman coding", r"""
Ordinary text uses 8 bits for every character, including the rare ones. **Huffman coding** gives **short codes to common symbols and long codes to rare ones**, so the total is smaller. Because the codes have different lengths, they must be chosen so that no code is the **start** of another one (the **prefix property**). Otherwise `01` could be one letter or the first half of `011`, and the decoder could not tell.

### Building the code

1. Count how often each symbol appears.
2. Take the two symbols (or groups) with the **lowest** counts, and join them under a new node whose count is their total.
3. Repeat with the new node included, until there is only one tree.
4. Label every left branch 0 and every right branch 1. A symbol's code is the path from the root down to it.

This is a **greedy algorithm** and uses a **priority queue**: a heap is exactly what finds the two smallest counts each time.

```python
import heapq
from collections import Counter

def build_tree(text):
    heap = [(count, order, symbol) for order, (symbol, count) in enumerate(sorted(Counter(text).items()))]
    heapq.heapify(heap)
    order = len(heap)
    while len(heap) > 1:
        count_a, _, left = heapq.heappop(heap)          # the two rarest
        count_b, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (count_a + count_b, order, (left, right)))
        order += 1
    return heap[0][2]

def assign_codes(tree, prefix="", table=None):
    if table is None:
        table = {}
    if isinstance(tree, str):
        table[tree] = prefix or "0"
    else:
        assign_codes(tree[0], prefix + "0", table)
        assign_codes(tree[1], prefix + "1", table)
    return table

def decode(bits, tree):
    text, node = "", tree
    for bit in bits:
        node = node[int(bit)]
        if isinstance(node, str):                      # reached a leaf: one symbol
            text += node
            node = tree
    return text

text = "ABRACADABRA"
tree = build_tree(text)
codes = assign_codes(tree)
counts = Counter(text)
for symbol in sorted(codes, key=lambda s: (len(codes[s]), s)):
    print(symbol, "appears", counts[symbol], "times, code", codes[symbol])

bits = "".join(codes[ch] for ch in text)
print(bits)
print(len(bits), "bits, against", 8 * len(text), "with 8 bit characters")
print("decoded correctly:", decode(bits, tree) == text)
```

`A` appears five times in eleven letters, so it gets a single bit. The rare `C` and `D` get three. The whole message takes 23 bits instead of 88.

The decoder needs the tree (or the counts to rebuild it), so that must be sent with the data. For a short message it can cost more than it saves. Huffman coding pays off on large files, and is one half of DEFLATE.

!key Lossless, and optimal for symbols one at a time :: Huffman coding is lossless. Among all codes that give each symbol its own whole number of bits, it is the shortest possible. Its weakness is that it cannot see patterns in sequences, which is what dictionary coding does.
"""),
        Section("Encryption: ciphers old and new", r"""
**Encryption** scrambles a message so that only someone holding the right **key** can read it. The original is **plaintext**, the scrambled version is **ciphertext**, and the method is a **cipher**. Good practice (**Kerckhoffs's principle**) is that a system must stay secure even if the attacker knows exactly how it works, so long as the key is secret.

### The Caesar cipher

The **Caesar cipher** shifts every letter along the alphabet by the key, wrapping from Z back to A. Shift by 3 and `A` becomes `D`.

```python
def caesar(text, shift):
    out = ""
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            out += chr((ord(ch) - base + shift) % 26 + base)       # % 26 wraps round
        else:
            out += ch
    return out

secret = caesar("Meet me at the old bridge at noon", 3)
print(secret)
print(caesar(secret, -3))
```

There are only 25 possible keys, so an attacker simply tries them all: a **brute force attack**. A cleverer one uses **frequency analysis**. In English the letter `E` is by far the most common, so whichever letter is most common in a long ciphertext is probably `E`, and that reveals the shift.

```python
from collections import Counter

def caesar(text, shift):
    out = ""
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            out += chr((ord(ch) - base + shift) % 26 + base)
        else:
            out += ch
    return out

def crack(ciphertext):
    letters = [ch for ch in ciphertext.lower() if ch.isalpha()]
    commonest = Counter(letters).most_common(1)[0][0]
    shift = (ord(commonest) - ord("e")) % 26             # assume that letter is an e
    return shift, caesar(ciphertext, -shift)

message = "The weather in Edinburgh is never what you expect, even in the summer"
print(crack(caesar(message, 11)))
```

### The Vigenere cipher

The **Vigenere cipher** uses a *word* as the key. Each letter of the key gives the shift for the matching letter of the message, and the key repeats. The same plaintext letter now becomes different ciphertext letters, so simple frequency analysis fails.

```python
def shift_letter(ch, shift):
    return chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))

def vigenere(text, key, decrypt=False):
    out, position = "", 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[position % len(key)]) - ord("A")
            out += shift_letter(ch, -shift if decrypt else shift)
            position += 1
        else:
            out += ch
    return out

secret = vigenere("ATTACKATDAWN", "LEMON")
print(secret)
print(vigenere(secret, "LEMON", decrypt=True))
```

Notice that the three `A`s in the message came out as `L`, `C` and `W`. It is stronger, but not unbreakable: the key repeats, and an attacker who works out its length can break the message into several Caesar ciphers.

### XOR and the one-time pad

**XOR** has a useful property: `a XOR b XOR b` gives back `a`. So the same operation both encrypts and decrypts. If the key is **truly random, as long as the message, and never used twice**, the result is a **one-time pad**, and it is the only cipher proved to be perfectly secure. Every possible plaintext is equally likely for any ciphertext, so there is nothing for an attacker to find.

```python
import random

rng = random.Random(2024)               # a fixed seed so this example gives the same answer each time
message = b"MEET AT DAWN"
key = bytes(rng.randrange(256) for _ in message)

cipher = bytes(m ^ k for m, k in zip(message, key))
print(cipher.hex())
print(bytes(c ^ k for c, k in zip(cipher, key)))
```

The weakness is the key. It must be shared securely in advance, be as long as everything you will ever send, and **never be reused**. See what happens if it is:

```python
import random

rng = random.Random(2024)
first = b"MEET AT DAWN"
second = b"HOLD AT NOON"
key = bytes(rng.randrange(256) for _ in first)

c1 = bytes(m ^ k for m, k in zip(first, key))
c2 = bytes(m ^ k for m, k in zip(second, key))

mixed = bytes(a ^ b for a, b in zip(c1, c2))      # the key cancels out
print(mixed == bytes(a ^ b for a, b in zip(first, second)))

guess = b"MEET"                                    # the attacker guesses the start of one message...
print(bytes(a ^ b for a, b in zip(mixed, guess)))  # ...and reads the start of the other
```

Reusing the key let the attacker remove it entirely. This is a real mistake, made by real systems.

!warn Never invent your own :: Everything in this section is for understanding. Real systems use well tested ciphers such as **AES**, from libraries that other people have checked for years. Home-made cryptography is almost always breakable.
"""),
        Section("Public key cryptography", r"""
All the ciphers so far are **symmetric**: the sender and the receiver use the **same key**. That has a problem. How does the key get to the receiver in the first place? If you could send it safely, you could send the message safely.

**Asymmetric** (public key) encryption solves it with a **pair** of keys. One is **public**, and given to anyone. The other is **private** and never leaves its owner. What one key locks, only the other unlocks.

- To send a **confidential** message, encrypt with the receiver's **public** key. Only their private key can decrypt it.
- To **sign** a message, encrypt (a hash of) it with *your own private* key. Anyone can check the signature with your public key, which proves it came from you and was not changed.

### RSA with small numbers

**RSA** relies on a one way street: multiplying two big primes together is easy, but finding them again from the product is very hard. Use small ones to see how it works:

1. Pick two primes, p = 61 and q = 53. Their product n = 3233 goes in both keys.
2. Work out (p - 1)(q - 1) = 3120.
3. Pick a public exponent e = 17, with no common factor with 3120.
4. The private exponent d is the **modular inverse** of e: the number where e x d leaves remainder 1 when divided by 3120. That is 2753.

Encrypt a number m as `m ** e % n` and decrypt it as `c ** d % n`. Python's three argument `pow` does the modular arithmetic efficiently.

```python
p, q = 61, 53
n = p * q
phi = (p - 1) * (q - 1)
e = 17
d = pow(e, -1, phi)                    # the modular inverse

print("public key (e, n):", e, n)
print("private key d    :", d)

m = 65
c = pow(m, e, n)
print(m, "encrypts to", c, "and decrypts to", pow(c, d, n))

message = "HELLO"
cipher = [pow(ord(ch), e, n) for ch in message]
print(cipher)
print("".join(chr(pow(x, d, n)) for x in cipher))
```

Look at the cipher list: both `L`s encrypt to the same number, so this *textbook* RSA leaks patterns. Real RSA adds random **padding** first.

### Why the numbers must be huge

Anyone can see n = 3233 in the public key. To get the private key they must factor it back into 61 and 53. For a small number that is instant. Count the steps for bigger ones:

```python
def factor(n):
    steps, f = 0, 2
    while f * f <= n:
        steps += 1
        if n % f == 0:
            return f, n // f, steps
        f += 1
    return n, 1, steps

print(factor(3233))
print(factor(10007 * 10009))
print(factor(100003 * 100019))
```

Each extra digit makes the search about three times longer. Real RSA keys are **2048 bits**, about 617 digits, and no known method factors them in a lifetime.

### Digital signatures

A signature runs RSA backwards. The sender encrypts a **hash** of the message with the private key. The receiver decrypts it with the public key and compares it with their own hash of the message. If they match, the message is genuine and unchanged. (A toy hash is used here; real systems sign a SHA-256 hash.)

```python
n, e, d = 3233, 17, 2753

def toy_hash(message):
    return sum(ord(ch) for ch in message) % n

message = "pay Sam 10 pounds"
signature = pow(toy_hash(message), d, n)               # only the owner of d can do this
print("signature:", signature)
print("genuine message accepted:", pow(signature, e, n) == toy_hash(message))

changed = "pay Sam 90 pounds"
print("changed message accepted:", pow(signature, e, n) == toy_hash(changed))
```

### Agreeing a key in public: Diffie-Hellman

**Diffie-Hellman** lets two people create a shared secret key by talking in the open. Each keeps a private number, sends a public value built from it, and combines the other's value with their own secret. Both arrive at the same number, which no eavesdropper can work out.

```python
P, G = 23, 5                       # public numbers, agreed in the open
alice_secret = 6
bob_secret = 15

alice_sends = pow(G, alice_secret, P)
bob_sends = pow(G, bob_secret, P)
print("sent in the open:", alice_sends, bob_sends)

print("Alice works out:", pow(bob_sends, alice_secret, P))
print("Bob works out:  ", pow(alice_sends, bob_secret, P))
```

### Putting it together: HTTPS

Asymmetric encryption is slow, and symmetric encryption is fast. So when your browser connects to a secure site, they use an asymmetric method to agree a **session key**, and then encrypt all the traffic with a fast symmetric cipher such as AES. The site proves who it is with a **digital certificate**, a public key signed by a trusted **certificate authority**.
"""),
        Section("Hashing and storing passwords", r"""
A **hash function** turns any input into a fixed-size output called a **hash** or **digest**. A good cryptographic hash such as SHA-256 has these properties:

- **Deterministic**: the same input always gives the same hash
- **Fixed length**: 256 bits, whatever the size of the input
- **One way**: there is no practical way to work back from the hash to the input
- **Avalanche effect**: a tiny change in the input changes the hash completely
- **Collision resistant**: it is hard to find two inputs with the same hash

```python
import hashlib

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

def bits_that_differ(a, b):
    return bin(int(a, 16) ^ int(b, 16)).count("1")

one, two = sha("hello"), sha("hellp")
print(one)
print(two)
print("bits that differ:", bits_that_differ(one, two), "out of 256")
```

Changing one letter altered about half of the 256 bits. A hash is **not** encryption: there is no key, and no way to decrypt it. Uses include checking a downloaded file has not changed, detecting tampering, digital signatures, and storing passwords.

### Collisions are possible but rare

An input of any length cannot map to a short hash without collisions, but with a long hash they are astronomically unlikely. Cut the hash down to 16 bits and watch how soon one appears:

```python
import hashlib

def tiny_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()[:4]       # keep only 16 bits

seen = {}
tries = 0
while True:
    message = "msg" + str(tries)
    h = tiny_hash(message)
    tries += 1
    if h in seen:
        print(tries, "tries:", message, "and", seen[h], "both hash to", h)
        break
    seen[h] = message
```

With 65 536 possible values you might expect to need tens of thousands of messages, but a collision typically turns up after a few hundred (122 here). This is the **birthday paradox**, and it is why hashes need to be long.

### Storing passwords

A site should never store passwords themselves, because a stolen database would reveal every one. It stores a **hash**, and checks a login by hashing what was typed. But a plain hash is not enough. Attackers keep tables of the hashes of millions of common passwords.

```python
import hashlib

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

common = ["password", "123456", "qwerty", "letmein", "dragon", "monkey"]
lookup = {sha(word): word for word in common}                # the attacker's table

stolen = {"amy": sha("letmein"), "ben": sha("Tr0ub4dor&3"), "cat": sha("letmein")}
for user, stored in stolen.items():
    print(user, stored[:12], "->", lookup.get(stored, "not in the table"))
```

Two problems show up. Amy's and Cat's hashes are **identical**, which tells the attacker they chose the same password. And the common password falls at once. The fix is a **salt**: a random value, different for each user, stored beside the hash and added to the password before hashing.

```python
import hashlib

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

# in real use the salt is random, for example secrets.token_hex(16)
salts = {"amy": "k9x2", "cat": "q7b1"}
for user in ("amy", "cat"):
    print(user, sha(salts[user] + "letmein")[:12])
```

Same password, different hashes, and a table prepared in advance is useless because it would have to be rebuilt for every salt. The salt is not secret.

The last defence is to make each guess **slow**. This is **key stretching**: hash the result again and again, so that checking one password costs a tenth of a second instead of a microsecond. That is unnoticeable for a genuine login and ruinous for an attacker trying billions.

```python
# varies
import hashlib
import time

def stretch(password, salt, rounds):
    digest = (salt + password).encode()
    for _ in range(rounds):
        digest = hashlib.sha256(digest).digest()
    return digest.hex()

for rounds in (1, 100000):
    start = time.perf_counter()
    stretch("letmein", "k9x2", rounds)
    print(rounds, "round(s) took", round((time.perf_counter() - start) * 1000, 3), "milliseconds")
```

Professional code should not write its own loop. Use a purpose built function, such as PBKDF2 (shown), bcrypt, scrypt or Argon2:

```pylocal
import hashlib
import hmac
import secrets

def hash_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600000)
    return salt, digest

def check_password(password, salt, stored):
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600000)
    return hmac.compare_digest(digest, stored)       # compares in constant time

salt, stored = hash_password("correct horse battery staple")
print(check_password("correct horse battery staple", salt, stored))
print(check_password("wrong guess", salt, stored))
```

### Checking a message has not been altered: HMAC

A plain hash proves a message matches a hash, but anyone can compute one. An **HMAC** mixes a **secret key** into the hash, so that only someone with the key can produce or check it. It proves the message is unchanged *and* came from a holder of the key.

```python
import hashlib
import hmac

key = b"shared secret"
message = b"transfer 100 pounds to account 12345678"
tag = hmac.new(key, message, hashlib.sha256).hexdigest()
print(tag[:20])

altered = b"transfer 900 pounds to account 12345678"
print(hmac.compare_digest(tag, hmac.new(key, message, hashlib.sha256).hexdigest()))
print(hmac.compare_digest(tag, hmac.new(key, altered, hashlib.sha256).hexdigest()))
```
"""),
    ],
    keyterms=[
        ("Lossless compression", "Compression after which the original data can be rebuilt exactly."),
        ("Lossy compression", "Compression that permanently discards some of the data, so the original cannot be rebuilt."),
        ("Compression ratio", "The original size divided by the compressed size."),
        ("Run length encoding (RLE)", "Replacing each run of the same value with a count and the value."),
        ("Dictionary coding", "Replacing repeated sequences of data with short references to entries in a dictionary."),
        ("Huffman coding", "A lossless method that gives shorter bit patterns to more frequent symbols, built from a tree."),
        ("Symmetric encryption", "Encryption in which the same key is used to encrypt and decrypt."),
        ("Asymmetric (public key) encryption", "Encryption that uses a pair of keys: a public key to encrypt and a private key to decrypt."),
        ("One-time pad", "An encryption using a truly random key as long as the message and used only once, which is perfectly secure."),
        ("Digital signature", "A hash of a message encrypted with the sender's private key, proving who sent it and that it has not changed."),
        ("Hash function", "A function that turns data of any size into a fixed size value, which cannot practically be reversed."),
        ("Salt", "A random value, added to a password before it is hashed, so that identical passwords give different hashes."),
        ("Key stretching", "Repeating a hash many times to make each guess of a password slow."),
    ],
    grade="""
These topics are asked as explanations of method, so the marks are for the steps, in order.

+ For RLE, show the pairs, and say it only helps where there are long runs
+ For Huffman coding, say frequent symbols get shorter codes, and that no code is the start of another
+ State the key distinction for encryption: the same key (symmetric) or a pair (asymmetric), and which key is used for what
+ For hashing, name the property you are relying on: one way, fixed length, or collision resistance
+ For passwords, give all three: hashed, salted, and slow to compute
""",
    mistakes=[
        "Saying lossy compression can be reversed. The discarded detail is gone for good.",
        "Assuming RLE always shrinks data. With no runs it can double the size.",
        "Calling hashing a type of encryption. A hash cannot be decrypted because there is no key.",
        "Encrypting with the sender's private key to keep a message secret. That makes a signature; for secrecy use the receiver's public key.",
        "Believing the salt has to be secret. It is stored next to the hash. Its job is to make hashes unique.",
    ],
    quiz=[
        Q("What is the difference between lossless and lossy compression?",
          ["Lossless lets the original be rebuilt exactly; lossy discards data for good", "Lossless files are always smaller", "Lossy compression is used for text and lossless for images", "Lossy compression needs a key"], 0,
          "With lossy compression some information is permanently thrown away, so only an approximation of the original is recovered."),
        Q("Run length encoding turns AAABBBBCC into which of these?",
          ["3A4B2C", "A3B4C2", "9ABC", "3A3B3C"], 0,
          "Each run is replaced by its length followed by the symbol: three A, four B, two C."),
        Q("When would run length encoding make a file larger?",
          ["When the data has few or no repeated runs", "When the data is mostly zeros", "When the file is very large", "When the data is a text file"], 0,
          "Every single symbol becomes a count plus the symbol, which doubles its size."),
        Q("What is the main idea of Huffman coding?",
          ["More frequent symbols get shorter codes", "Every symbol gets a code of the same length", "Repeated words are replaced by a dictionary reference", "Data is encrypted with a public key"], 0,
          "Using fewer bits for the commonest symbols makes the total smaller."),
        Q("Why must no Huffman code be the start of another?",
          ["Otherwise the decoder could not tell where one symbol ends", "Otherwise the tree would be too tall", "Otherwise the file would not be lossless", "Otherwise it would be slow to build"], 0,
          "With the prefix property, reading bits until a code is matched always gives a single unambiguous answer."),
        Q("What is the weakness of a Caesar cipher?",
          ["There are only 25 possible keys and letter frequencies show through", "It needs a very long key", "It cannot encrypt spaces", "It can only be used once"], 0,
          "An attacker can simply try every shift, or use the fact that the commonest letter is probably E."),
        Q("Which cipher is perfectly secure if used correctly?",
          ["The one-time pad", "The Caesar cipher", "The Vigenere cipher", "Any cipher with a 128 bit key"], 0,
          "A truly random key as long as the message and used once leaves nothing for an attacker to find."),
        Q("In public key encryption, how does Ali send Bea a message that only she can read?",
          ["Encrypt it with Bea's public key", "Encrypt it with Ali's private key", "Encrypt it with Ali's public key", "Encrypt it with Bea's private key"], 0,
          "Only Bea holds the matching private key, so only she can decrypt it."),
        Q("What does a digital signature prove?",
          ["Who sent the message, and that it was not changed", "That the message was compressed", "That the message is secret", "That the sender has a strong password"], 0,
          "The signature is made with the sender's private key and checked with their public key, against a hash of the message."),
        Q("Why is a salt added to a password before hashing it?",
          ["So identical passwords give different hashes and prepared tables are useless", "So the password can be decrypted later", "So the hash becomes shorter", "So the password is encrypted"], 0,
          "Each user gets a different salt, so an attacker cannot reuse one table of hashes against every account."),
    ],
    exam=[
        EQ("The data AAAAABBBCCDDDDDD is stored using run length encoding. Show the result of encoding it, and state one disadvantage of run length encoding.", 4, [
            MP("Counts the runs correctly: 5 A, 3 B, 2 C, 6 D", ["5", "3", "2", "6"]),
            MP("Encoded result 5A3B2C6D (a count and a character for each run)", ["5a3b2c6d", "5a 3b 2c 6d", "5 a 3 b 2 c 6 d"]),
            MP("Disadvantage: where there are few or no repeated characters the data can become larger", ["larger", "bigger", "increase", "no runs", "few repeated", "not repeated"]),
            MP("So it is only effective on data containing long runs of the same value", ["long runs", "effective", "only works", "only useful", "suitable"]),
        ], "The data has a run of 5 As, then 3 Bs, 2 Cs and 6 Ds, so it is encoded as 5A3B2C6D. One disadvantage is that where the data has few or no repeated characters, each single character is replaced by a count and the character, so the encoded data can be larger than the original. It is only effective for data that contains long runs of the same value.",
           command="Show"),
        EQ("Explain two differences between lossless compression and lossy compression. Give an example of a file type for which each is suitable.", 4, [
            MP("Lossless allows the original data to be rebuilt exactly, but lossy permanently removes some data", ["exactly", "original", "permanently", "removes", "discard", "lost"]),
            MP("Lossy files are usually much smaller than lossless", ["smaller", "greater compression", "more compression", "reduction", "higher ratio"]),
            MP("An example where lossless is needed: text, program or data files (or PNG)", ["text", "program", "data file", "zip", "png", "document"]),
            MP("An example where lossy is suitable: photographs, music or video (JPEG, MP3, MP4)", ["jpeg", "mp3", "mp4", "photograph", "music", "video", "image", "audio"]),
        ], "Lossless compression allows the original data to be rebuilt exactly, whereas lossy compression permanently discards some of the data so that the original cannot be recovered. Lossy compression can usually reduce a file to a much smaller size than lossless compression. Lossless compression is needed for files such as text documents and programs, where any change to the data would damage them. Lossy compression is suitable for photographs, music and video, as in JPEG and MP3 files, where the detail removed is hard for people to notice.",
           command="Explain"),
        EQ("The table shows how often each of four characters appears in a message of 8 characters. Describe how a Huffman tree is built for this data, and calculate the total number of bits needed to store the message using Huffman codes of A = 0, B = 10, C = 110 and D = 111.", 5, [
            MP("The two characters with the lowest frequencies (C and D) are joined first, to make a node with frequency 2", ["lowest", "smallest", "least", "c and d", "joined", "combined"]),
            MP("The process is repeated, always joining the two lowest frequencies, until there is one tree", ["repeat", "until", "one tree", "single tree", "again"]),
            MP("Left branches are labelled 0 and right branches 1, and the path from the root gives the code", ["0", "1", "branch", "path", "root"]),
            MP("Bits used: A 4 x 1 = 4, B 2 x 2 = 4, C 1 x 3 = 3, D 1 x 3 = 3", ["4 x 1", "2 x 2", "1 x 3", "4 + 4 + 3 + 3"]),
            MP("Total = 14 bits", ["14"]),
        ], "The two characters with the lowest frequencies, C and D, are joined under a new node with a frequency of 2. The process is repeated, each time joining the two lowest frequencies (B with the CD node, giving 4, then A with that node, giving 8), until there is a single tree. The branches are labelled 0 and 1, and the code for each character is the path from the root to it. The message needs A: 4 x 1 = 4 bits, B: 2 x 2 = 4 bits, C: 1 x 3 = 3 bits and D: 1 x 3 = 3 bits, a total of 14 bits.",
           command="Describe",
           figure="""```text
character:  A   B   C   D
frequency:  4   2   1   1
```"""),
        EQ("Explain the difference between symmetric and asymmetric encryption, and describe how asymmetric encryption can be used to send a message that only the receiver can read.", 5, [
            MP("Symmetric: the same key is used to encrypt and to decrypt", ["same key", "one key", "single key"]),
            MP("Asymmetric uses a pair of keys, a public key and a private key", ["pair", "public", "private", "two keys", "different keys"]),
            MP("The sender encrypts the message using the receiver's public key", ["receiver's public", "recipient's public", "public key of the receiver", "uses the public key"]),
            MP("Only the receiver's private key can decrypt it", ["private key", "only the receiver", "only the recipient", "decrypt"]),
            MP("The private key is never shared, so the problem of sending a key securely is avoided", ["never shared", "kept secret", "not shared", "secret", "key distribution"]),
        ], "In symmetric encryption the same key is used to encrypt and to decrypt the message, so the key has to be shared securely first. In asymmetric encryption there is a pair of keys, a public key and a private key. To send a message only the receiver can read, the sender encrypts it using the receiver's public key, which anyone is allowed to have. Only the receiver's private key can decrypt the message. The private key is kept secret and never shared, so there is no need to send a secret key across the network.",
           command="Explain"),
        EQ("A website stores the passwords of its users. Discuss how the website should protect the passwords in case its database is stolen.", 6, [
            MP("The passwords should not be stored as plain text, but as a hash", ["hash", "hashed", "not plain text", "not stored in plain", "one way"]),
            MP("A hash cannot be reversed, so a thief cannot read the passwords; at login the typed password is hashed and compared", ["cannot be reversed", "one way", "compared", "reverse", "decrypt"]),
            MP("A unique random salt should be added before hashing, so that identical passwords have different hashes", ["salt", "unique", "random", "different hashes", "identical"]),
            MP("The salt defeats precomputed tables of hashes (rainbow tables)", ["rainbow", "precomputed", "lookup table", "table", "dictionary attack"]),
            MP("A slow hashing method (key stretching, such as bcrypt or PBKDF2) makes each guess take longer, slowing brute force attacks", ["slow", "stretching", "bcrypt", "pbkdf2", "brute force", "argon", "iterations"]),
            MP("A reasoned conclusion, such as also requiring strong passwords or two factor authentication", ["conclusion", "strong passwords", "two factor", "2fa", "overall", "therefore", "length"]),
        ], "The website should not store the passwords as plain text, because a thief with the database could read every one. It should store only a hash of each password. A hash cannot be reversed, and when a user logs in the password they type is hashed and compared with the stored value. A unique, random salt should be added to each password before it is hashed, so that two users with the same password have different hashes and a precomputed table of hashes of common passwords is of no use. A slow hashing method such as bcrypt or PBKDF2, which repeats the hash many times, should be used so that each guess takes a long time and brute force attacks are impractical. To strengthen this further the site should insist on long passwords and offer two factor authentication, because even a well hashed weak password can be guessed.",
           command="Discuss"),
    ],
)
