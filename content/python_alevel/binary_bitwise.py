"""A Level Python: binary arithmetic, bitwise operations and floating point."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="binary-and-bitwise-operations",
    title="Binary, Bitwise Operations and Floating Point",
    spec="A Level 10",
    icon="i-binary",
    minutes=60,
    blurb="Two's complement, subtraction by addition and overflow, then AND, OR, XOR and the shifts with masks, flags and packed colours, then the mantissa and exponent of floating point numbers, and what Unicode adds to ASCII.",
    fact="The Boeing 787 had a bug in which its generators shut down if left powered for 248 days without a restart. A counter of hundredths of a second, held in a signed 32 bit integer, overflows after 248.55 days. Two's complement overflow is a real hazard, and not only an exam topic.",
    sections=[
        Section("Two's complement", r"""
Python's integers can be as big as memory allows. A real processor's cannot: it holds an integer in a fixed number of bits, a **word**. To see what the hardware does you must keep to a fixed width, and in Python the way is to **mask**, with `& 0xFF` for 8 bits.

### The problem with signs

How do you store -5 in 8 bits? Using the first bit as a sign, with the other seven for the **magnitude**, wastes a code on a second zero (+0 and -0) and makes arithmetic awkward, because addition has to check the signs. **Two's complement** removes both problems.

!diagram py-twos-complement

In two's complement the leftmost bit has a **negative** place value. In 8 bits the columns are -128, 64, 32, 16, 8, 4, 2, 1. That one change is everything: a number is just the sum of the columns that hold a 1.

To **negate** a number: **invert every bit, then add 1**.

```python
def to_twos_complement(value, bits):
    return format(value & (2 ** bits - 1), "0" + str(bits) + "b")

def from_twos_complement(pattern):
    number = int(pattern, 2)
    if pattern[0] == "1":
        number = number - 2 ** len(pattern)
    return number

for value in [5, -5, 127, -128, 0, -1]:
    pattern = to_twos_complement(value, 8)
    print(str(value).rjust(4), pattern, from_twos_complement(pattern))
```

Negating 5 by hand: 5 is `00000101`. Invert it: `11111010`. Add 1: `11111011`, which is -5. The sum of its columns is -128 + 64 + 32 + 16 + 8 + 2 + 1 = -5.

| Bits | Unsigned range | Two's complement range |
| 8 | 0 to 255 | -128 to 127 |
| 16 | 0 to 65 535 | -32 768 to 32 767 |
| 32 | 0 to 4 294 967 295 | -2 147 483 648 to 2 147 483 647 |

The range is **asymmetric**: there is one more negative number than positive, because zero uses up one of the positive codes.

### Subtraction is addition

A processor needs no subtraction circuit. To work out 7 - 5, it adds 7 and -5, and ignores the **carry** out of the top bit.

```python
def from_twos_complement(pattern):
    number = int(pattern, 2)
    if pattern[0] == "1":
        number = number - 2 ** len(pattern)
    return number

a = 7
b = -5
total = (a + (b & 0xFF)) & 0xFF         # add the 8 bit patterns, and keep only 8 bits
print(format(a, "08b"), "+", format(b & 0xFF, "08b"), "=", format(total, "08b"))
print("which is", from_twos_complement(format(total, "08b")))
```

The sum of the two patterns is nine bits long, `1 00000010`. The carry out of the top is thrown away, because the register has only eight bits, and what is left, `00000010`, is 2.

### Overflow

If the true answer does not fit in the number of bits, the pattern wraps round and the sign is wrong. This is **overflow**.

```python
def from_twos_complement(pattern):
    number = int(pattern, 2)
    if pattern[0] == "1":
        number = number - 2 ** len(pattern)
    return number

total = (100 + 100) & 0xFF
pattern = format(total, "08b")
print(pattern, from_twos_complement(pattern))
```

100 + 100 is 200, which is above 127, the biggest 8 bit value. Its pattern is `11001000`, which has the sign bit set, so it reads as -56. **Adding two positive numbers and getting a negative one is the sign of overflow.**

### Hexadecimal

Four bits make one hexadecimal digit, so hex is a short way to write binary. It is used for memory addresses, colours and machine code because every byte is exactly two hex digits.

```python
print(hex(255), hex(172), format(172, "08b"))
print(int("AC", 16), int("10101100", 2))
print(format(0b10101100, "02X"))
```

`1010 1100` split into two nibbles is `A` and `C`, which is `AC`.
"""),
        Section("Bitwise operations", r"""
A **bitwise** operation works on each bit position of its operands separately, as a logic gate does.

| Operator | Name | What it does | Example |
| `&` | AND | each result bit is 1 when both bits are 1 | `0b1100 & 0b1010` is `0b1000` |
| `\|` | OR | each result bit is 1 when at least one bit is 1 | `0b1100 \| 0b1010` is `0b1110` |
| `^` | XOR | each result bit is 1 when the bits are **different** | `0b1100 ^ 0b1010` is `0b0110` |
| `~` | NOT | flips every bit, 0 to 1 and 1 to 0 | `~0b1100` flips them all |
| `<<` | Shift left | moves every bit to the left, filling with 0 | `3 << 2` is 12 |
| `>>` | Shift right | moves every bit to the right, dropping the end | `12 >> 2` is 3 |

```python
a = 0b1100
b = 0b1010
print(format(a & b, "04b"), format(a | b, "04b"), format(a ^ b, "04b"))
print(format(~a & 0b1111, "04b"))
print(3 << 2, 12 >> 2)
```

`~a` in Python gives a negative number, since Python's integers have no width, so to see an 8 bit or 4 bit NOT you mask it: `~a & 0b1111`.

### Shifts

A **left shift** moves every bit one place to the left, filling with 0. That doubles the number, exactly as adding a zero multiplies a denary number by ten. A **right shift** halves it, dropping the lowest bit.

```python
x = 5
print(x << 1, x << 2, x << 3)           # 10 20 40: times 2, 4, 8
print(100 >> 1, 100 >> 2, 101 >> 1)      # 50 25 50: divide by 2, 4, and drop the remainder
print((200 << 1) & 0xFF)                 # 144: in 8 bits, 400 overflows and wraps
```

### Masks: reading and changing individual bits

A **mask** is a number with 1s in the positions you care about. The four masks you must know, applied to a byte called `flags`:

| To | Use | Because |
| **Test** a bit | `flags & mask` | the result is non zero only if that bit is 1 |
| **Set** a bit to 1 | `flags \| mask` | OR with 1 gives 1, and OR with 0 changes nothing |
| **Clear** a bit to 0 | `flags & ~mask` | AND with 0 gives 0, and AND with 1 changes nothing |
| **Toggle** a bit | `flags ^ mask` | XOR with 1 flips the bit, with 0 changes nothing |

```python
BOLD = 0b0001
ITALIC = 0b0010
UNDERLINE = 0b0100

style = 0
style = style | BOLD                    # set bold
style = style | UNDERLINE               # set underline
print(format(style, "04b"))             # 0101

print(bool(style & ITALIC), bool(style & BOLD))      # False True

style = style & ~BOLD                   # clear bold
style = style ^ ITALIC                  # toggle italic: it was off, so it comes on
print(format(style, "04b"))             # 0110
```

Eight yes or no settings fit in **one byte** this way, instead of eight variables. File permissions work like this, and so do the flags register in a processor and the options passed to many programming functions.

### Where else it appears

```python
# Is a number odd? Its lowest bit is 1.
print(7 & 1, 8 & 1)

# Is a number a power of two? Exactly one bit is set, so clearing the lowest leaves nothing.
for n in [8, 12, 64]:
    print(n, n & (n - 1) == 0)

# A subnet mask keeps the network part of an IP address.
ip = (192 << 24) | (168 << 16) | (1 << 8) | 77
mask = 0xFFFFFF00
network = ip & mask
print(".".join(str((network >> shift) & 0xFF) for shift in (24, 16, 8, 0)))

# A colour packed into one number: red, green and blue, a byte each.
colour = (255 << 16) | (128 << 8) | 0
print(hex(colour), (colour >> 16) & 0xFF, (colour >> 8) & 0xFF, colour & 0xFF)

# Parity: XOR every bit, to give a bit that makes the count of 1s even.
def parity_bit(byte):
    bit = 0
    while byte:
        bit = bit ^ (byte & 1)
        byte = byte >> 1
    return bit

print(parity_bit(0b1011001), parity_bit(0b1011000))

# Encrypt with XOR, and decrypt with the same key.
secret = [ord(c) ^ 0b0101 for c in "HELLO"]
print("".join(chr(c ^ 0b0101) for c in secret))
```

**XOR is its own inverse**: `(x ^ key) ^ key` is `x`. That one property is behind parity checks, simple encryption and the one time pad.
"""),
        Section("Floating point and characters", r"""
### Why 0.1 is not 0.1

A computer stores a real number as a **binary fraction**, and some denary fractions cannot be written exactly as one. A third cannot be written exactly in denary, 0.3333 and so on, and in the same way one tenth is a **recurring** binary fraction, 0.0001100110011 and so on. It is cut off, and the stored value is a very slightly different number.

```python
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print((0.1).hex())

import math
print(math.isclose(0.1 + 0.2, 0.3))
```

Never test floating point numbers for equality. Test whether they are close enough.

### Mantissa and exponent

**Floating point** stores a number the way scientific notation does. It splits it into a **mantissa**, which holds the digits, and an **exponent**, which says where the point goes:

```text
value = mantissa × 2 to the power of the exponent
```

The **mantissa** gives the **precision** and the **exponent** gives the **range**. With a fixed number of bits in total, adding a bit to the mantissa gives more accurate numbers, and adding one to the exponent gives bigger and smaller ones, and one is paid for by the other.

The A Level format is a two's complement mantissa with the binary point **after the sign bit**, and a two's complement exponent:

```python
def twos(pattern):
    value = int(pattern, 2)
    if pattern[0] == "1":
        value = value - 2 ** len(pattern)
    return value

def decode(mantissa, exponent):
    m = twos(mantissa) / 2 ** (len(mantissa) - 1)
    e = twos(exponent)
    return m * 2 ** e

print(decode("01101000", "0011"))      # 0.1101 is 0.8125, times 2 to the 3
print(decode("10011000", "0010"))      # a negative mantissa
```

### Normalisation

The same number can be written many ways, as 0.5 × 4 and 0.25 × 8 are both 2. To use the bits of the mantissa properly, a floating point number is **normalised**: shifted so that the mantissa starts `01` if positive, or `10` if negative. The first two bits are different. Each shift left means the exponent drops by one, so the value does not change.

```python
def twos(pattern):
    value = int(pattern, 2)
    if pattern[0] == "1":
        value = value - 2 ** len(pattern)
    return value

def normalise(mantissa, exponent):
    e = twos(exponent)
    while mantissa[0] == mantissa[1] and "1" in mantissa:
        mantissa = mantissa[1:] + "0"
        e = e - 1
    return mantissa, format(e & 0b1111, "04b")

print(normalise("00011010", "0100"))
```

`00011010` with exponent 4 becomes `01101000` with exponent 2, after two shifts. Both mean 3.25. The normalised form uses all of the precision available.

!warn The exponent goes down as the mantissa shifts left :: Shifting the mantissa left makes it bigger, so the exponent must get smaller by the same amount to leave the value unchanged. Do it the wrong way round, and the number is quadrupled instead.

### Seeing the real format

Most computers use the IEEE 754 standard. A 32 bit float is 1 sign bit, an 8 bit exponent and a 23 bit mantissa.

```python
import struct

def float_bits(x):
    raw = struct.unpack(">I", struct.pack(">f", x))[0]
    pattern = format(raw, "032b")
    return pattern[0], pattern[1:9], pattern[9:]

sign, exponent, mantissa = float_bits(0.15625)
print(sign, exponent, mantissa)
```

### Characters

A character is stored as a number. **ASCII** uses 7 bits, 128 codes, which holds English letters, digits and punctuation. **Unicode** is a table of more than a hundred thousand characters in every writing system, plus emoji, each with a **code point**. **UTF-8** stores a code point in **one to four bytes**, and its first 128 codes are identical to ASCII, so every ASCII file is already valid UTF-8.

```python
for character in ["A", "é", "€", "😀"]:
    print(character, ord(character), len(character.encode("utf-8")), "bytes")
```
"""),
    ],
    keyterms=[
        ("Two's complement", "A way of storing signed integers in which the leftmost bit has a negative place value, so negative numbers are found by inverting the bits and adding one."),
        ("Overflow", "An error that occurs when the result of a calculation is too large to be stored in the number of bits available."),
        ("Bitwise operation", "An operation that acts on each bit position of its operands independently, such as AND, OR, XOR or NOT."),
        ("Mask", "A binary pattern used with a bitwise operation to test, set, clear or toggle selected bits."),
        ("Logical shift", "Moving every bit of a binary number a number of places left or right, filling the gap with zeros."),
        ("Mantissa", "The part of a floating point number that holds its significant digits, and so determines its precision."),
        ("Exponent", "The part of a floating point number that gives the power of two it is multiplied by, and so determines its range."),
        ("Normalisation", "Adjusting a floating point number so that the mantissa starts with 01 or 10, which maximises the precision."),
        ("Rounding error", "The small difference between a real number and its stored value, because the number of bits is limited."),
        ("Unicode", "A character set that gives a unique code point to the characters of nearly every writing system."),
    ],
    grade="""
Binary questions are marks for method as well as for the answer, so write every step down.

+ Show the working for a negative number: write the positive, invert, add one, then state the answer
+ For subtraction, say that the second number is converted to two's complement and added, and that the carry is ignored
+ Name the mask, and the operator that goes with it: AND to test or clear, OR to set, XOR to toggle
+ In floating point, say that the mantissa decides the precision and the exponent the range
+ Check a normalised answer starts 01 or 10, and that the exponent was reduced for each shift left
""",
    mistakes=[
        "Forgetting to add 1 after inverting the bits when making a number negative.",
        "Reading a two's complement pattern with a leading 1 as a large positive number.",
        "Writing the answer to a floating point question without adjusting the exponent after shifting the mantissa.",
        "Using AND to set a bit and OR to clear it, which are the other way round.",
        "Comparing floating point numbers for equality instead of checking that they are close.",
    ],
    quiz=[
        Q("What is the range of numbers that can be stored in 8 bit two's complement?",
          ["-128 to 127", "-127 to 127", "0 to 255", "-255 to 255"], 0,
          "The leftmost bit has the value -128, so the lowest is -128 and the highest is 127."),
        Q("What is the 8 bit two's complement representation of -5?",
          ["11111011", "10000101", "11111010", "00000101"], 0,
          "5 is 00000101. Invert it to get 11111010, then add 1 to get 11111011."),
        Q("What denary number does the 8 bit two's complement pattern 10000000 represent?",
          ["-128", "128", "-1", "0"], 0,
          "Only the -128 column has a 1, so the value is -128."),
        Q("Which bitwise operation would you use to clear a particular bit, leaving the rest unchanged?",
          ["AND with a mask that has a 0 in that position", "OR with a mask that has a 1 in that position",
           "XOR with a mask that has a 1 in that position", "NOT, applied to the whole byte"], 0,
          "ANDing a bit with 0 always gives 0, and ANDing the others with 1 leaves them as they are."),
        Q("What is `0b1100 ^ 0b0110`, written in binary?",
          ["1010", "1110", "0100", "0110"], 0,
          "XOR gives 1 where the bits differ: the four columns give 1, 0, 1, 0."),
        Q("What is the effect of shifting a binary number left by 2 places?",
          ["It is multiplied by 4", "It is divided by 4", "It is multiplied by 2", "It is increased by 2"], 0,
          "Each left shift doubles it, so two shifts multiply it by 2 twice."),
        Q("What is the hexadecimal value of the binary number 10101100?",
          ["AC", "CA", "A5", "BC"], 0,
          "The nibbles are 1010, which is A, and 1100, which is C."),
        Q("In a floating point number, what does adding a bit to the mantissa, and taking one from the exponent, do?",
          ["It increases the precision but reduces the range", "It increases the range but reduces the precision",
           "It increases both the range and the precision", "It does not change either of them"], 0,
          "The mantissa gives accuracy and the exponent gives size, and the total number of bits is fixed."),
        Q("Why does `0.1 + 0.2 == 0.3` give False in Python?",
          ["0.1 cannot be stored exactly in binary, so the results differ by a tiny amount", "Python has a bug in its addition of decimals",
           "The numbers are stored as text, and text cannot be added", "A float can only hold whole numbers exactly"], 0,
          "One tenth is a recurring fraction in binary, so the stored value is rounded, and the rounding errors do not cancel."),
        Q("How does UTF-8 relate to ASCII?",
          ["Its first 128 codes are the same as ASCII, and it uses more bytes for other characters",
           "It uses exactly 8 bits for every character, just as ASCII does",
           "It replaces all of the ASCII codes with new ones", "It can only store characters used in English"], 0,
          "An ASCII text file is already valid UTF-8, which is part of the reason it became the standard."),
    ],
    exam=[
        EQ("Write the 8 bit two's complement representation of the denary number -45. Show your working.", 3, [
            MP("45 in binary is 00101101", ["00101101", "101101"]),
            MP("The bits are inverted to give 11010010, and 1 is added", ["11010010", "invert", "flip", "ones complement", "add 1", "add one"]),
            MP("The answer is 11010011", ["11010011"]),
        ], "45 in 8 bit binary is 00101101. To make it negative, invert every bit, giving 11010010, and add 1, which gives 11010011. This is -128 + 64 + 16 + 2 + 1, which is -45, so the answer is 11010011.",
           command="Write"),
        EQ("Calculate 25 - 18 in 8 bit binary by using two's complement. Show your working.", 4, [
            MP("25 is 00011001 and 18 is 00010010", ["00011001", "00010010"]),
            MP("-18 is found by inverting 00010010 to 11101101 and adding 1, giving 11101110", ["11101110", "11101101", "invert"]),
            MP("The two are added: 00011001 plus 11101110", ["added", "add", "plus", "+"]),
            MP("The carry out of the 8th bit is ignored, giving 00000111, which is 7", ["00000111", "carry", "ignored", "discarded", "7"]),
        ], "25 is 00011001 and 18 is 00010010. To get -18, invert 00010010 to give 11101101 and add 1 to give 11101110. Adding 00011001 and 11101110 gives 1 00000111, and the carry out of the eighth bit is ignored, so the result is 00000111, which is 7.",
           command="Calculate"),
        EQ("A byte called settings holds eight on or off options. Bit 0 is the least significant bit. Bit 3 means that sound is on. Describe how bitwise operations can be used to check whether sound is on, and to turn sound off without changing the other seven bits.", 4, [
            MP("A mask with only bit 3 set, 00001000, is used", ["00001000", "mask", "8", "bit 3 set", "1 << 3"]),
            MP("To check, the byte is ANDed with the mask and the result is not zero if sound is on", ["and", "not zero", "non zero", "non-zero", "result"]),
            MP("To turn it off, the byte is ANDed with the inverse of the mask, 11110111", ["11110111", "inverse", "not mask", "invert", "clear"]),
            MP("This sets bit 3 to 0 and leaves the other bits as they were", ["other bits", "unchanged", "remain", "same", "not change", "leaves"]),
        ], "A mask is made with only bit 3 set, 00001000. To check whether sound is on, the byte is ANDed with the mask, and if the result is not zero then bit 3 is 1 and sound is on. To turn sound off, the byte is ANDed with the inverse of the mask, 11110111. That sets bit 3 to 0, and since every other bit is ANDed with 1, the other seven bits remain as they were.",
           command="Describe"),
        EQ("A floating point number is stored using an 8 bit mantissa and a 4 bit exponent. Both are in two's complement, and the binary point of the mantissa is after the first bit. The mantissa is 01011000 and the exponent is 0011. Calculate the denary value of the number.", 3, [
            MP("The mantissa is 0.1011000 in binary, which is 0.6875", ["0.6875", "0.1011", "11/16"]),
            MP("The exponent is 3", ["exponent is 3", "3", "0011"]),
            MP("The value is 0.6875 times 8, which is 5.5", ["5.5", "times 8", "x 8", "* 8", "2^3", "2 to the power of 3"]),
        ], "The mantissa 01011000 with the point after the first bit is 0.1011000, which is a half plus an eighth plus a sixteenth, 0.6875. The exponent 0011 is 3, so the mantissa is multiplied by 2 to the power of 3, which is 8. The value is 0.6875 times 8, which is 5.5.",
           command="Calculate"),
        EQ("Explain why the result of adding 0.1 and 0.2 in many programming languages is not exactly 0.3, and how a programmer should compare floating point numbers.", 3, [
            MP("Some decimal fractions, such as 0.1, cannot be stored exactly in binary", ["cannot be stored exactly", "recurring", "not exact", "approximation", "binary fraction", "cannot be represented"]),
            MP("The stored values are rounded, so a small error occurs in the result", ["rounded", "rounding", "error", "tiny difference", "limited number of bits", "precision"]),
            MP("So two values should be compared by checking that the difference is smaller than a small tolerance, not for equality", ["tolerance", "close", "difference", "small amount", "within", "not equality", "not equal"]),
        ], "Decimal fractions such as 0.1 and 0.2 are recurring fractions in binary, so they cannot be stored exactly in a mantissa with a limited number of bits, and each is stored as a rounded approximation. The small errors mean that the sum is a tiny amount away from 0.3. A programmer should therefore compare floating point values by checking that the difference between them is smaller than a small tolerance, rather than testing for equality.",
           command="Explain"),
    ],
)
