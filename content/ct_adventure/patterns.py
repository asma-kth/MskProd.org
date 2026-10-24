"""World 3, Pattern Recognition: Spot the Pattern!

Every level asks the student to find what repeats or what changes by a rule,
then use it: to fill gaps, to predict far ahead, to spot the step that breaks a
pattern (a bug), and finally to replace repeated code with a loop.
"""

KS3 = "KS3 Computing: computational thinking (pattern recognition)"
J277 = "OCR J277 2.1.1: computational thinking"
J277_ITER = "OCR J277 2.2.1: iteration (count- and condition-controlled loops)"
J277_ERR = "OCR J277 2.1.2 and 2.3.2: finding logic errors and testing"

LIGHTS = [
    dict(id="R", label="Red"),
    dict(id="RA", label="Red and amber"),
    dict(id="G", label="Green"),
    dict(id="A", label="Amber"),
]
COLOURS = [
    dict(id="r", label="Red", c="#EF4444"),
    dict(id="y", label="Yellow", c="#FACC15"),
    dict(id="b", label="Blue", c="#3B82F6"),
    dict(id="g", label="Green", c="#22C55E"),
    dict(id="p", label="Purple", c="#A855F7"),
    dict(id="o", label="Orange", c="#F97316"),
]

LEVELS = [
    # 1 -----------------------------------------------------------------
    dict(
        title="Finish the Sequence",
        engine="sequence",
        objective="Find the part of a pattern that repeats and use it to predict what comes next.",
        learn=("A pattern is something that repeats or changes in a regular way. "
               "Once you spot the part that repeats, you can predict what comes next. "
               "Computer scientists look for patterns so one rule can solve many problems."),
        task="Fill each gap with the shape that keeps the pattern going. Then say which part repeats.",
        data=dict(
            look="emoji",
            palette=["⭐", "🌙", "☀️", "☁️"],
            rounds=[
                dict(type="fill", seq=["⭐", "🌙", "⭐", "🌙", "⭐", "🌙", None, None], answers=["⭐", "🌙"],
                     why="Star, moon, star, moon: after every moon comes a star."),
                dict(type="fill", palette=["🍎", "🍌", "🍇", "🍒"],
                     seq=["🍎", "🍎", "🍌", "🍎", "🍎", "🍌", "🍎", None, None], answers=["🍎", "🍌"],
                     why="Apple, apple, banana repeats: two apples, then a banana."),
                dict(type="fill", palette=["🔺", "🟦", "🟢", "⭐"],
                     seq=["🔺", "🟦", "🟦", "🔺", "🟦", "🟦", "🔺", None, None, "🔺"], answers=["🟦", "🟦"],
                     why="Triangle, square, square repeats, so two squares come before the next triangle."),
                dict(type="ask", seq=["🔺", "🟦", "🟦", "🔺", "🟦", "🟦"], q="Which part repeats to make this whole pattern?",
                     options=["🔺 🟦 🟦", "🔺 🟦", "🟦 🟦", "🔺 🟦 🟦 🔺"], answer=0,
                     hint="Look for the smallest group you could copy over and over to build the whole row.",
                     why="🔺 🟦 🟦 is the smallest group that repeats to make the whole pattern."),
            ],
        ),
        watch=dict(say="Watch: after every moon comes a star, so the first gap is a star.", moves=[[0, "⭐"]]),
        hints=[
            "Say the pattern out loud: star, moon, star, moon...",
            "Find the smallest group that repeats, then keep repeating it.",
            "Pixel has filled one gap for you.",
        ],
        skill="You spotted the repeating part of a pattern and used it to predict what comes next.",
        cheer=("PAW-SOME pattern spotting! Finding what repeats lets you predict what comes next. "
               "Computers use the same trick."),
        remember=dict(q="What is pattern recognition?",
                      options=["Spotting similarities and things that repeat",
                               "Breaking a problem into smaller parts",
                               "Removing details that do not matter",
                               "Writing steps in the right order"],
                      answer=0,
                      why="Pattern recognition means looking for things that are the same or that repeat, so a solution can be reused."),
        curriculum=[KS3, J277],
        solution=("Round 1: star, moon. Round 2: apple, banana. Round 3: square, square. "
                  "The part that repeats is triangle, square, square."),
    ),
    # 2 -----------------------------------------------------------------
    dict(
        title="Colour Code Challenge",
        engine="sequence",
        objective="Use the length of a repeating pattern to work out any position.",
        learn=("Patterns can be made of colours, sounds or moves, not just shapes. "
               "If you know how long the repeating part is, you can work out any position without drawing them all. "
               "That saves a lot of work."),
        task="Finish each colour code. In the last round, predict a bead far along the string.",
        data=dict(
            look="colour",
            palette=COLOURS[:4],
            rounds=[
                dict(type="fill", seq=["r", "y", "b", "r", "y", "b", "r", None, None, None], answers=["y", "b", "r"],
                     why="Red, yellow, blue repeats, so after red comes yellow, then blue, then red."),
                dict(type="fill", seq=["r", "r", "g", "b", "r", None, "g", "b", None, "r", "g", "b"], answers=["r", "r"],
                     why="The code is red, red, green, blue. Every green has two reds before it."),
                dict(type="ask", palette=[COLOURS[4], COLOURS[5], COLOURS[3], COLOURS[0]], tiles=True,
                     seq=["p", "o", "o", "g", "p", "o", "o", "g"],
                     q="If this pattern keeps going, what colour is bead number 20?",
                     options=["p", "o", "g", "r"], answer=2,
                     hint="The repeat is 4 beads long, so beads 4, 8, 12, 16 and 20 are all the last bead of a repeat.",
                     why=("The repeating part is 4 beads long. 20 ÷ 4 = 5 exactly, so bead 20 is the last bead "
                          "of a repeat: green.")),
            ],
        ),
        watch=dict(say="Watch: red, yellow, blue repeats, so after red comes yellow.", moves=[[0, "y"]]),
        hints=[
            "Count how many beads are in the part that repeats.",
            "For a far-away bead, divide its number by the length of the repeating part and look at what is left over.",
            "Pixel has filled in one bead for you.",
        ],
        skill="You used the length of a repeating pattern to predict any position.",
        cheer=("COLOUR-FUL genius! You predicted a bead without drawing them all. "
               "That is pattern recognition saving time."),
        remember=dict(q="A pattern repeats every 3 beads: red, yellow, blue. What colour is bead 9?",
                      options=["Blue", "Red", "Yellow", "Green"],
                      answer=0,
                      why="9 ÷ 3 = 3 with nothing left over, so bead 9 is the last bead of a repeat: blue."),
        curriculum=[KS3, J277],
        solution=("Round 1: yellow, blue, red. Round 2: red and red. Round 3: the repeat is 4 beads long and "
                  "20 ÷ 4 = 5, so bead 20 is green."),
    ),
    # 3 -----------------------------------------------------------------
    dict(
        title="Number Detective",
        engine="sequence",
        objective="Find the rule behind a number pattern and use it.",
        learn=("Number patterns follow a rule, such as 'add 3' or 'double it'. "
               "Find the rule by comparing each number with the one before it. "
               "Once you have the rule, you can carry on the pattern for ever."),
        task="Type the missing numbers in each pattern. Then choose the rule.",
        data=dict(
            look="number",
            rounds=[
                dict(type="fill", seq=[3, 6, 9, 12, None, None], answers=[15, 18], why="The rule is add 3: 12 + 3 = 15, and 15 + 3 = 18."),
                dict(type="fill", seq=[50, 45, 40, None, 30, None], answers=[35, 25], why="The rule is take away 5: 40 − 5 = 35, and 30 − 5 = 25."),
                dict(type="fill", seq=[1, 2, 4, 8, None, None], answers=[16, 32], why="Each number is double the one before: 8 × 2 = 16, and 16 × 2 = 32."),
                dict(type="ask", seq=[1, 2, 4, 8, 16, 32], q="What is the rule for this pattern?",
                     options=["Double the number each time", "Add 2 each time", "Add 1, then 2, then 3", "Multiply by 4 each time"],
                     answer=0, hint="Try each rule on the first few numbers: does 1 become 2, and 2 become 4?", why="Each number is twice the one before it: 1 × 2 = 2, 2 × 2 = 4, and so on."),
            ],
        ),
        watch=dict(say="Watch: 3, 6, 9, 12 goes up by 3 each time, so the next number is 15.", moves=[[0, 15]]),
        hints=[
            "Work out the difference between each number and the next.",
            "If the differences keep growing, try multiplying instead of adding.",
            "Pixel has typed one number for you.",
        ],
        skill="You found the rule behind a number pattern and used it to fill the gaps.",
        cheer=("NUMBER ONE detective! You cracked every rule. "
               "Spotting rules like these is how programs make predictions."),
        remember=dict(q="What comes next: 2, 5, 8, 11, ...?",
                      options=["14", "13", "15", "22"],
                      answer=0,
                      why="The rule is add 3, so 11 + 3 = 14."),
        curriculum=[KS3, J277],
        solution="Round 1: 15, 18 (add 3). Round 2: 35, 25 (take away 5). Round 3: 16, 32 (double). The rule is double each time.",
    ),
    # 4 -----------------------------------------------------------------
    dict(
        title="Animal Patterns",
        engine="group",
        objective="Group things by the key features they share, then use the pattern on something new.",
        learn=("Things that share the same key features belong to the same group. "
               "Spotting the shared pattern lets you sort things you have never seen before. "
               "Look for the features that matter, not the ones that only look similar."),
        task="Sort each animal into its group by its key features. Then use the pattern to place a strange new animal.",
        data=dict(
            problem=("Mammals have fur or hair and feed their babies milk. Birds have feathers. "
                     "Fish breathe with gills and have fins. Reptiles have dry, scaly skin and breathe air."),
            kicker="Key features",
            zones=[
                dict(id="mammal", label="Mammals", icon="🐾"),
                dict(id="bird", label="Birds", icon="🪶"),
                dict(id="fish", label="Fish", icon="🐟"),
                dict(id="reptile", label="Reptiles", icon="🦎"),
            ],
            items=[
                dict(id="dog", text="Dog", icon="🐕", zone="mammal", why="A dog has fur and feeds its puppies milk: a mammal."),
                dict(id="whale", text="Whale", icon="🐋", zone="mammal",
                     why="A whale lives in the sea, but it breathes air and feeds its calves milk, so it is a mammal."),
                dict(id="bat", text="Bat", icon="🦇", zone="mammal", why="A bat flies, but it has fur and feeds its babies milk: a mammal."),
                dict(id="penguin", text="Penguin", icon="🐧", zone="bird", why="A penguin cannot fly, but it has feathers, so it is a bird."),
                dict(id="eagle", text="Eagle", icon="🦅", zone="bird", why="An eagle has feathers: a bird."),
                dict(id="parrot", text="Parrot", icon="🦜", zone="bird", why="A parrot has feathers: a bird."),
                dict(id="shark", text="Shark", icon="🦈", zone="fish", why="A shark breathes with gills and has fins: a fish."),
                dict(id="clownfish", text="Clownfish", icon="🐠", zone="fish", why="A clownfish breathes with gills and has fins: a fish."),
                dict(id="snake", text="Snake", icon="🐍", zone="reptile", why="A snake has dry, scaly skin and breathes air: a reptile."),
                dict(id="crocodile", text="Crocodile", icon="🐊", zone="reptile",
                     why="A crocodile swims a lot, but it has scaly skin and breathes air: a reptile."),
                dict(id="turtle", text="Turtle", icon="🐢", zone="reptile",
                     why="A turtle can swim, but it breathes air and has scaly skin: a reptile."),
            ],
            followup=dict(q="A platypus has fur and feeds its babies milk, but it lays eggs. Which group does the pattern put it in?",
                          options=["Mammals", "Birds", "Reptiles", "Fish"],
                          answer=0,
                          why="Fur and milk are the key mammal features, so a platypus is a mammal, even though it lays eggs."),
        ),
        hints=[
            "Ignore where the animal lives. Look at its body: fur, feathers, gills or scales?",
            "A whale and a bat are tricky. What do they feed their babies?",
            "Pixel has sorted one animal for you.",
        ],
        skill="You grouped things by the key features they share, then used the pattern on something new.",
        cheer=("ROAR-SOME sorting! You looked past where animals live to the features that really matter. "
               "That is pattern recognition at its best."),
        remember=dict(q="Why is a whale a mammal and not a fish?",
                      options=["It breathes air and feeds its babies milk",
                               "It lives in the sea",
                               "It is very big",
                               "It has a tail"],
                      answer=0,
                      why="Breathing air and feeding babies milk are the key mammal features."),
        curriculum=[KS3, J277],
        solution=("Mammals: dog, whale, bat. Birds: penguin, eagle, parrot. Fish: shark, clownfish. "
                  "Reptiles: snake, crocodile, turtle. The platypus is a mammal."),
    ),
    # 5 -----------------------------------------------------------------
    dict(
        title="Robot Dance",
        engine="dance",
        objective="Spot a repeating pattern of moves and write it as a loop.",
        learn=("Dances are full of patterns: the same moves repeat again and again. "
               "Spot the repeating moves and you can describe a long dance in a few words, like 'do this 3 times'. "
               "Programmers call that a loop."),
        task="Watch the dance, spot the pattern, and program what comes next. In the last round, write the whole dance as a loop.",
        data=dict(
            moves=[
                dict(id="left", text="Lean left", icon="👈"),
                dict(id="right", text="Lean right", icon="👉"),
                dict(id="up", text="Arms up", icon="🙌"),
                dict(id="jump", text="Jump", icon="🦘"),
                dict(id="spin", text="Spin", icon="🌀"),
                dict(id="wave", text="Wave", icon="👋"),
            ],
            rounds=[
                dict(type="next", shown=["left", "right", "up", "left", "right", "up"], answer=["left", "right", "up"],
                     say="Watch the robot dance, then program the next three moves."),
                dict(type="gap", shown=["jump", "spin", "spin", "jump", None, "spin", "jump", "spin", None], answer=["spin", "spin"],
                     say="Two moves are missing from this dance. Fill them in."),
                dict(type="loop", target=["left", "left", "spin", "left", "left", "spin", "left", "left", "spin"],
                     units=3, answer=dict(times=3, unit=["left", "left", "spin"]),
                     say="Write this whole dance as one loop: a few moves, repeated."),
            ],
        ),
        hints=[
            "Watch the dance again and say the moves out loud.",
            "Find the shortest group of moves that repeats.",
            "Pixel has programmed one move for you.",
        ],
        skill="You spotted a repeating pattern of moves and wrote it as a loop.",
        cheer=("GROOVY! You found the pattern and turned a long dance into a short loop. "
               "Loops are patterns that computers repeat for you."),
        remember=dict(q="Why do programmers use loops for repeating patterns?",
                      options=["One short rule can repeat the steps as many times as needed",
                               "Loops make programs slower",
                               "Computers cannot repeat steps without loops",
                               "Loops remove the pattern"],
                      answer=0,
                      why="A loop writes the repeating part once and says how many times to do it."),
        curriculum=[KS3, J277_ITER],
        solution=("Round 1: lean left, lean right, arms up. Round 2: spin, spin. "
                  "Round 3: repeat 3 times: lean left, lean left, spin."),
    ),
    # 6 -----------------------------------------------------------------
    dict(
        title="Snake Pattern Game",
        engine="snakepat",
        objective="Continue a pattern by choosing the right next item every time.",
        learn=("The snake's body shows the order it has eaten its fruit, and that order is a pattern. "
               "Spot what repeats, then eat the fruit that keeps the pattern going. "
               "Eat the wrong fruit and the pattern breaks!"),
        task="Steer the snake with the arrows to eat the fruit that comes next in the pattern. Finish all three rounds.",
        data=dict(
            w=9, h=9,
            rocks=[[4, 1], [1, 6], [7, 6]],
            fruits=[
                dict(id="apple", icon="🍎", text="apple"),
                dict(id="banana", icon="🍌", text="banana"),
                dict(id="grapes", icon="🍇", text="grapes"),
                dict(id="cherry", icon="🍒", text="cherry"),
            ],
            rounds=[
                dict(eaten=["apple", "banana", "apple"], answer=["banana", "apple", "banana", "apple"]),
                dict(eaten=["grapes", "grapes", "cherry", "grapes", "grapes"], answer=["cherry", "grapes", "grapes", "cherry"]),
                dict(eaten=["cherry", "apple", "apple", "banana", "cherry", "apple"], answer=["apple", "banana", "cherry", "apple"]),
            ],
        ),
        hints=[
            "Read the snake's body from its tail to its head. Which fruits repeat?",
            "The strip above the board shows the fruit eaten so far. What comes after the last one?",
            "Pixel has lit up the next fruit for you.",
        ],
        skill="You continued a pattern by choosing the right next item every time.",
        cheer=("SSS-SPECTACULAR! Your snake kept the pattern perfectly. "
               "Spotting patterns fast is a real computer science superpower."),
        remember=dict(q="A snake ate: apple, banana, banana, apple, banana, banana, apple. What should it eat next?",
                      options=["Banana", "Apple", "Grapes", "Cherry"],
                      answer=0,
                      why="The repeating part is apple, banana, banana, so a banana comes after an apple."),
        curriculum=[KS3, J277],
        solution=("Round 1: banana, apple, banana, apple. Round 2: cherry, grapes, grapes, cherry. "
                  "Round 3: apple, banana, cherry, apple."),
    ),
    # 7 -----------------------------------------------------------------
    dict(
        title="Traffic Light Detective",
        engine="sequence",
        objective="Use a repeating cycle to fill gaps, predict the future and spot a fault.",
        learn=("UK traffic lights follow a fixed cycle: red, red and amber, green, amber, then red again. "
               "Because the cycle repeats, you can work out what the light will show at any time. "
               "A step that breaks the cycle means the light is faulty."),
        task="Fill in the missing lights, predict the light at a later time, and find the faulty step.",
        data=dict(
            look="lights",
            palette=LIGHTS,
            rounds=[
                dict(type="fill", seq=["R", "RA", "G", "A", "R", None, "G", None, "R", "RA", None], answers=["RA", "A", "G"],
                     why="The cycle is red, red and amber, green, amber, then back to red."),
                dict(type="ask", tiles=True, text="Red lasts 30 seconds, red and amber 2 seconds, green 25 seconds and amber 3 seconds.",
                     seq=["R", "RA", "G", "A"],
                     q="The light turns red at 0 seconds. What does it show at 95 seconds?",
                     options=["R", "RA", "G", "A"], answer=2,
                     hint="Take away one whole 60-second cycle from 95 seconds first, then count through red, red and amber, green.",
                     why=("One cycle lasts 30 + 2 + 25 + 3 = 60 seconds, so 95 seconds is 35 seconds into the second cycle. "
                          "That is after 30 seconds of red and 2 of red and amber, so the light is green.")),
                dict(type="odd", text="This log from a faulty light shows each step in order.",
                     seq=["R", "RA", "G", "A", "R", "RA", "A", "A", "R", "RA", "G"], wrong=6, fix="G",
                     why="After red and amber always comes green. Step 7 shows amber, so the light skipped green."),
            ],
        ),
        hints=[
            "Say the cycle out loud: red, red and amber, green, amber, red...",
            "One full cycle takes 60 seconds. Take away whole cycles first.",
            "Pixel has done one step for you.",
        ],
        skill="You used a repeating cycle to fill gaps, predict the future and spot a fault.",
        cheer=("GREEN LIGHT GENIUS! You predicted the lights and caught the fault. "
               "Engineers test traffic systems in exactly this way."),
        remember=dict(q="What comes after red and amber on a UK traffic light?",
                      options=["Green", "Red", "Amber", "Flashing amber"],
                      answer=0,
                      why="The UK cycle is red, red and amber, green, amber."),
        curriculum=[KS3, J277],
        solution=("Round 1: red and amber, amber, green. Round 2: green (95 seconds is 35 seconds into a 60-second cycle). "
                  "Round 3: step 7 is the fault; it should be green."),
    ),
    # 8 -----------------------------------------------------------------
    dict(
        title="Find the Bug",
        engine="sequence",
        objective="Find where output breaks its pattern, then fix the line that caused it.",
        learn=("When a program's output should follow a pattern, a value that breaks the pattern points to a bug. "
               "Debugging means finding where the pattern breaks, then working out which line caused it. "
               "Testing against the pattern you expect catches bugs fast."),
        task="Find where each output breaks its pattern and fix it. In the code rounds, click the line with the bug, then choose the fix.",
        data=dict(
            look="number",
            rounds=[
                dict(type="odd", text="This program should print the 5 times table.",
                     seq=[5, 10, 15, 20, 26, 30, 35], wrong=4, fix=25,
                     why="The 5 times table goes up by 5 each time, so 20 + 5 = 25, not 26."),
                dict(type="odd", look="colour", palette=COLOURS[:4], text="A light show should flash red, green, blue, over and over.",
                     seq=["r", "g", "b", "r", "g", "g", "r", "g", "b"], wrong=5, fix="b",
                     why="Red, green, blue repeats, so the sixth flash should be blue."),
                dict(type="code", text="This program should print the even numbers 2, 4, 6, 8 and 10.",
                     code="for i = 1 to 5\n    print(i + 2)\nnext i",
                     expect=["2", "4", "6", "8", "10"], bug=2,
                     fixes=["    print(i * 2)", "    print(i + 1)", "    print(2)", "    print(i * i)"], answer=0,
                     why="Each even number is double the counter: 1 × 2 = 2, 2 × 2 = 4, and so on."),
                dict(type="code", text="This program should count down 5, 4, 3, 2, 1.",
                     code="n = 5\nwhile n > 1\n    print(n)\n    n = n - 1\nendwhile",
                     expect=["5", "4", "3", "2", "1"], bug=2,
                     fixes=["while n > 0", "while n > 2", "while n < 1", "while n == 1"], answer=0,
                     why="With n > 1 the loop stops before printing 1. Using n > 0 lets it print 1 and then stop."),
            ],
        ),
        hints=[
            "Compare each value with the one before it. Where does the pattern change?",
            "In the code, find the line that makes or controls the numbers. Bugs in a pattern usually live there.",
            "Pixel has done one step for you.",
        ],
        skill="You found where output broke its pattern and fixed the line that caused it.",
        cheer=("BUG SQUASHED! You found and fixed every bug by spotting where the pattern broke. "
               "That is real debugging."),
        remember=dict(q="A times-table program prints 4, 8, 12, 15, 20. What does the 15 tell you?",
                      options=["There is a bug: the pattern says it should be 16",
                               "The program is correct",
                               "The pattern changed on purpose",
                               "The computer ran out of memory"],
                      answer=0,
                      why="The 4 times table adds 4 each time, so 12 + 4 = 16. A value that breaks the pattern points to a bug."),
        curriculum=[KS3, J277_ERR],
        solution=("Round 1: 26 should be 25. Round 2: the sixth flash should be blue. Round 3: line 2 should be "
                  "print(i * 2). Round 4: line 2 should be while n > 0."),
    ),
    # 9 -----------------------------------------------------------------
    dict(
        title="Code Pattern Detective",
        engine="codepat",
        objective="Replace repeated code with a loop.",
        learn=("When lines of code repeat with only a small change, that is a pattern a loop can replace. "
               "Find what stays the same and what changes, and use the loop counter for the part that changes. "
               "One short loop is easier to read and to fix than many copied lines."),
        task="Turn each long program into a short loop by filling the gaps. Run it to check it prints exactly the same.",
        data=dict(rounds=[
            dict(long='print("Hip hip hooray!")\nprint("Hip hip hooray!")\nprint("Hip hip hooray!")\nprint("Hip hip hooray!")\nprint("Hip hip hooray!")',
                 template='for i = 1 to {a}\n    print("Hip hip hooray!")\nnext i',
                 blanks=dict(a="5")),
            dict(long="print(7 * 1)\nprint(7 * 2)\nprint(7 * 3)\nprint(7 * 4)\nprint(7 * 5)",
                 template="for i = 1 to {a}\n    print({b})\nnext i",
                 blanks=dict(a="5", b="7 * i")),
            dict(long=('print("10 green bottles")\nprint("9 green bottles")\nprint("8 green bottles")\n'
                       'print("7 green bottles")\nprint("6 green bottles")'),
                 template='for i = {a} to {b} step {c}\n    print(str(i) + " green bottles")\nnext i',
                 blanks=dict(a="10", b="6", c="-1")),
        ]),
        hints=[
            "Compare the lines. Which part stays the same, and which part changes each time?",
            "Use the loop counter i wherever the number changes. To count down, the step is negative.",
            "Pixel has filled one gap for you.",
        ],
        skill="You replaced repeated code with a loop by spotting what stays the same and what changes.",
        cheer=("LOOP-TASTIC! Three long programs became three tiny loops. "
               "You spotted patterns in code like a real programmer."),
        remember=dict(q="What does the counter i do in a for loop?",
                      options=["It changes each time round, so it can stand for the part of the pattern that changes",
                               "It stops the program",
                               "It counts the number of errors",
                               "It must always be 1"],
                      answer=0,
                      why="The counter takes a new value on each pass, which is what makes each line of output different."),
        curriculum=[KS3, J277_ITER],
        solution=("Round 1: for i = 1 to 5. Round 2: for i = 1 to 5 with print(7 * i). "
                  "Round 3: for i = 10 to 6 step -1."),
    ),
    # 10 ----------------------------------------------------------------
    dict(
        title="Pattern Master",
        engine="quest",
        objective="Recognise patterns in shapes, numbers and code, and use each rule to predict.",
        learn=("Pattern recognition works everywhere: in shapes, numbers, cycles and code. "
               "A pattern master spots the rule, tests it, and uses it to predict. "
               "Open the three locks of the Pattern Vault to prove it."),
        task="Open each lock of the Pattern Vault by cracking its pattern. There are three locks.",
        data=dict(look="vault", stages=[
            dict(title="The shape lock", engine="sequence", data=dict(
                look="emoji", palette=["🔷", "🔶", "🔴", "🟡"],
                rounds=[
                    dict(type="fill", seq=["🔷", "🔶", "🔶", "🔷", "🔶", "🔶", "🔷", None, None], answers=["🔶", "🔶"],
                         why="Blue, orange, orange repeats."),
                    dict(type="odd", seq=["🔴", "🟡", "🔴", "🟡", "🔴", "🔴", "🔴", "🟡"], wrong=5, fix="🟡",
                         why="Red and yellow take turns, so the sixth shape should be yellow."),
                ])),
            dict(title="The number lock", engine="sequence", data=dict(
                look="number",
                rounds=[
                    dict(type="ask", input=True, seq=[4, 7, 10, 13], q="The rule is add 3. What is the 10th number in this pattern?",
                         answer=31, hint="From the 1st number to the 10th is 9 steps of the rule.", why="From the 1st number to the 10th is 9 steps of add 3: 4 + 9 × 3 = 31."),
                    dict(type="ask", input=True, seq=[2, 6, 18, 54], q="What number comes next?",
                         answer=162, hint="Divide each number by the one before it.", why="Each number is three times the one before: 54 × 3 = 162."),
                ])),
            dict(title="The code lock", engine="codepat", data=dict(rounds=[
                dict(long="print(3)\nprint(6)\nprint(9)\nprint(12)",
                     template="for i = 1 to {a}\n    print({b})\nnext i",
                     blanks=dict(a="4", b="3 * i")),
            ])),
        ]),
        hints=[
            "Find the rule first: what repeats, or how each item changes from the one before.",
            "For the 10th number, count how many steps of the rule it takes to get there from the 1st.",
            "Pixel has done one step for you.",
        ],
        skill="You recognised patterns in shapes, numbers and code, and used each rule to predict.",
        cheer=("VAULT CRACKED! You are a Pattern Master. "
               "Spotting rules in shapes, numbers and code is a superpower every programmer needs."),
        remember=dict(q="The pattern 5, 9, 13, 17 adds 4 each time. What is the 6th number?",
                      options=["25", "21", "29", "24"],
                      answer=0,
                      why="From the 1st number to the 6th is 5 steps of add 4: 5 + 5 × 4 = 25."),
        curriculum=[KS3, J277_ITER],
        solution=("Shape lock: orange, orange, then the sixth shape should be yellow. Number lock: 31, then 162. "
                  "Code lock: for i = 1 to 4 with print(3 * i)."),
    ),
]
