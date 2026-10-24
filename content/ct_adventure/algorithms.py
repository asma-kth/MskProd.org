"""World 4, Algorithms: Think Step by Step!

Algorithms here are written only as flowcharts and as pseudocode in the style
of the OCR Exam Reference Language. Students order steps, program robots,
build and run flowcharts with the standard symbols, drive a car and a snake
with selection inside loops, trace programs and find and fix bugs with tests.
"""

KS3 = "KS3 National Curriculum: understand several key algorithms; use sequence, selection and repetition"
J277_ALG = "OCR J277 2.1.2: designing algorithms with flowcharts and pseudocode"
J277_PROG = "OCR J277 2.2.1: sequence, selection and iteration"
J277_TEST = "OCR J277 2.3.2: testing, test data and trace tables"


def node(nid, t, text, code=None, **kw):
    d = dict(id=nid, t=t, text=text)
    if code is not None:
        d["code"] = code
    d.update(kw)
    return d


def out(nid, text, code):
    return node(nid, "io", text, code)


def proc(nid, text, code=None):
    return node(nid, "process", text, code if code is not None else text)


START = node("start", "start", "Start")
END = node("end", "end", "End")

CAR_CHOICES = dict(
    w=["NOT atFinish()", "atFinish()", "roadAhead()", "NOT roadAhead()"],
    c1=["roadAhead()", "roadOnLeft()", "roadOnRight()", "atFinish()"],
    a1=["forward()", "turnLeft()", "turnRight()"],
    c2=["roadAhead()", "roadOnLeft()", "roadOnRight()", "atFinish()"],
    a2=["forward()", "turnLeft()", "turnRight()"],
    a3=["forward()", "turnLeft()", "turnRight()"],
)
SNAKE_CHOICES = dict(
    w=["NOT allEaten()", "allEaten()", "foodAhead()", "NOT foodAhead()"],
    c1=["foodAhead()", "foodOnLeft()", "foodOnRight()", "allEaten()"],
    a1=["forward()", "turnLeft()", "turnRight()"],
    c2=["foodAhead()", "foodOnLeft()", "foodOnRight()", "allEaten()"],
    a2=["forward()", "turnLeft()", "turnRight()"],
    a3=["forward()", "turnLeft()", "turnRight()"],
)
LOOP_TEMPLATE = ("while {w}\n    if {c1} then\n        {a1}\n    elseif {c2} then\n        {a2}\n"
                 "    else\n        {a3}\n    endif\nendwhile")

LEVELS = [
    # 1 -----------------------------------------------------------------
    dict(
        title="Put It in Order",
        engine="order",
        objective="Put the steps of an algorithm in an order that works.",
        learn=("An algorithm is a precise set of steps that solves a problem. "
               "The steps must be in the right order, or the result goes wrong. "
               "A flowchart shows the steps as boxes joined by arrows, from Start to End."),
        task="Put the steps in order. Watch the flowchart grow as you go.",
        data=dict(rounds=[
            dict(problem="Plant a seed", kicker="Algorithm", flow=True,
                 items=[
                     dict(id="pot", text="Fill a pot with soil", icon="🪴", why="You need a pot of soil before anything else."),
                     dict(id="hole", text="Make a hole in the soil", icon="👆", why="The hole is made in the soil, so the soil comes first."),
                     dict(id="seed", text="Drop the seed in the hole", icon="🌱", why="The seed goes into the hole, so the hole must be made first."),
                     dict(id="cover", text="Cover the seed with soil", icon="🤲", why="You can only cover the seed once it is in the hole."),
                     dict(id="water", text="Water the pot", icon="💧", why="Water last, so the soil settles round the seed."),
                 ],
                 order=["pot", "hole", "seed", "cover", "water"]),
            dict(problem="Log in to a website", kicker="Algorithm", flow=True,
                 items=[
                     dict(id="open", text="Open the website", icon="🌐"),
                     dict(id="user", text="Type your username", icon="👤"),
                     dict(id="pass", text="Type your password", icon="🔑"),
                     dict(id="click", text="Click Log in", icon="🖱️"),
                     dict(id="home", text="See your home page", icon="🏠"),
                 ],
                 order=["open", "user", "pass", "click", "home"],
                 rules=[["open", "user", "You have to open the website before you can type anything into it."],
                        ["open", "pass", "You have to open the website before you can type anything into it."],
                        ["user", "click", "Type your username before you click Log in."],
                        ["pass", "click", "Type your password before you click Log in."],
                        ["click", "home", "You only see your home page after logging in."]]),
            dict(problem="Wash your hands", kicker="Algorithm", flow=True,
                 items=[
                     dict(id="wet", text="Wet your hands", icon="🚰", why="Wet hands first, so the soap can lather."),
                     dict(id="soap", text="Add soap", icon="🧼", why="Soap goes on wet hands, before you scrub."),
                     dict(id="scrub", text="Scrub for 20 seconds", icon="👐", why="Scrubbing spreads the soap, so it comes after adding soap."),
                     dict(id="rinse", text="Rinse off the soap", icon="💦", why="Rinse once you have finished scrubbing."),
                     dict(id="dry", text="Dry your hands", icon="🧻", why="Drying is the very last step."),
                 ],
                 order=["wet", "soap", "scrub", "rinse", "dry"]),
        ]),
        watch=dict(say="Watch: you need a pot of soil before anything else, so that goes first."),
        hints=[
            "Which step has to happen before all the others?",
            "Read your steps from top to bottom like a robot would. Does each step make sense at that moment?",
            "Pixel has moved one step into place.",
        ],
        skill="You put an algorithm's steps in a working order and saw it as a flowchart.",
        cheer=("STEP-TACULAR! Your algorithms work from Start to End. "
               "Every program is built from steps in the right order."),
        remember=dict(q="What is an algorithm?",
                      options=["A precise set of steps that solves a problem",
                               "A type of computer",
                               "A drawing of a website",
                               "A list of random ideas"],
                      answer=0,
                      why="An algorithm is a precise, ordered set of steps that solves a problem."),
        curriculum=[KS3, J277_ALG],
        solution=("Seed: pot, hole, seed, cover, water. Log in: open, username and password (either order), "
                  "click Log in, home page. Hands: wet, soap, scrub, rinse, dry."),
    ),
    # 2 -----------------------------------------------------------------
    dict(
        title="Help the Cat Get Home",
        engine="program",
        objective="Plan a sequence of moves as a program, then run it.",
        learn=("Computers follow instructions exactly, one at a time, in order. "
               "A program for a robot is a sequence of moves, and one wrong move sends it the wrong way. "
               "Planning the whole route before you run it is algorithmic thinking."),
        task="First drive Pixel home with the arrows. Then plan each route as a program and run it.",
        data=dict(mode="absolute", rounds=[
            dict(kind="drive", say="Drive Pixel home with the arrows. Your moves are saved as a program.",
                 grid=["#######",
                       "#S..#.#",
                       "#.#.#.#",
                       "#.#...#",
                       "#...#H#",
                       "#######"],
                 answer=["right", "right", "down", "down", "right", "right", "down"]),
            dict(kind="plan", max=9, say="Now plan first! Build the whole program, then press Run. Pixel hates ponds.",
                 grid=["#######",
                       "#S.~..#",
                       "#.#~#.#",
                       "#.....#",
                       "#~#.#H#",
                       "#######"],
                 answer=["down", "down", "right", "right", "right", "right", "down"]),
            dict(kind="plan", max=13, say="Pixel wants the fish on the way home. Plan a route that collects it.",
                 grid=["#######",
                       "#S...F#",
                       "#.###.#",
                       "#.....#",
                       "#H#####",
                       "#######"],
                 answer=["right", "right", "right", "right", "down", "down", "left", "left", "left", "left", "down"]),
        ]),
        watch=dict(say="Watch: Pixel moves one square for each arrow, in order."),
        hints=[
            "Trace the route with your finger first, one square at a time.",
            "Count the squares in each straight line. Each square is one arrow.",
            "Pixel has added the next move for you.",
        ],
        skill="You planned a precise sequence of moves and ran it as a program.",
        cheer=("HOME SWEET HOME! Your program got Pixel there step by step. "
               "Precise sequences like yours are the heart of every algorithm."),
        remember=dict(q="Why must a program's steps be in exactly the right order?",
                      options=["The computer follows them one at a time, exactly as written",
                               "The computer sorts them into the best order itself",
                               "Order only matters for long programs",
                               "The computer skips steps that look wrong"],
                      answer=0,
                      why="A computer cannot guess what you meant. It carries out each step exactly, in order."),
        curriculum=[KS3, J277_PROG],
        solution=("Round 1: right, right, down, down, right, right, down. Round 2: down, down, right × 4, down. "
                  "Round 3: right × 4 (fish), down, down, left × 4, down."),
    ),
    # 3 -----------------------------------------------------------------
    dict(
        title="Robot Commands",
        engine="program",
        objective="Program a robot with forward and turn commands, and use repeat loops.",
        learn=("Robots usually turn and move forward rather than moving up, down, left and right. "
               "A repeat loop runs the same commands several times, which makes programs shorter. "
               "Count carefully: the robot does exactly what you say."),
        task="Program the robot with forward and turn commands to reach its goal. Use repeat loops to stay within the block limit.",
        data=dict(mode="relative", rounds=[
            dict(kind="plan", max=8, dir="right", say="Reach the battery. Turns happen on the spot.",
                 grid=["######",
                       "#S..##",
                       "###.##",
                       "###..B",
                       "######"],
                 answer=["F", "F", "R", "F", "F", "L", "F", "F"]),
            dict(kind="plan", max=4, dir="right", end=[1, 1],
                 say="Collect all four stars and finish back at the start, using no more than 4 blocks. A repeat block helps!",
                 grid=["#####",
                       "#S.*#",
                       "#*#.#",
                       "#*.*#",
                       "#####"],
                 answer=[dict(repeat=4, do=["F", "F", "R"])]),
            dict(kind="plan", max=6, dir="right", say="Climb down the stairs to the battery in 6 blocks or fewer.",
                 grid=["########",
                       "#S.#####",
                       "##..####",
                       "###..###",
                       "####..##",
                       "#####.B#",
                       "########"],
                 answer=[dict(repeat=4, do=["F", "R", "F", "L"]), "F"]),
        ]),
        watch=dict(say="Watch: forward moves one square the way the robot faces; a turn only changes which way it faces."),
        hints=[
            "Stand up and act it out: which way are you facing after each turn?",
            "Look for a group of commands that repeats, and put it inside one repeat block.",
            "Pixel has added the next command for you.",
        ],
        skill="You programmed a robot with relative moves and used a loop to repeat commands.",
        cheer=("BEEP BEEP, BRILLIANT! You turned long programs into short loops. "
               "Repetition is one of the three building blocks of every algorithm."),
        remember=dict(q="Why use a repeat block instead of writing the same commands again and again?",
                      options=["It makes the program shorter and easier to change",
                               "It makes the robot move faster",
                               "Robots can only follow loops",
                               "It stops the robot from turning"],
                      answer=0,
                      why="A loop writes the repeated commands once and runs them as many times as needed."),
        curriculum=[KS3, J277_PROG],
        solution=("Round 1: F, F, R, F, F, L, F, F. Round 2: repeat 4 [F, F, R]. "
                  "Round 3: repeat 4 [F, R, F, L], then F."),
    ),
    # 4 -----------------------------------------------------------------
    dict(
        title="Flowchart Builder",
        engine="flowbuild",
        objective="Build flowcharts with the standard symbols, then run them with test data.",
        learn=("Flowcharts use standard symbols: an oval for Start and End, a parallelogram for input and output, "
               "a rectangle for a process, and a diamond for a decision. "
               "A decision has two exits, labelled Yes and No, and a loop is an arrow that goes back to a decision."),
        task="Drag each step, with the right symbol, into the numbered boxes. Then run your flowchart with the test data.",
        data=dict(rounds=[
            dict(problem="Ask for a number, then output whether it is odd or even.",
                 flow=[START,
                       node("b1", "slot", "", slot="s1", label="1"),
                       node("b2", "slot", "", slot="s2", label="2"),
                       node("d1", "decision", "", slot="s3", label="3",
                            yes=[node("b4", "slot", "", slot="s4", label="4")],
                            no=[node("b5", "slot", "", slot="s5", label="5")]),
                       END],
                 cards=[
                     dict(id="in", t="io", text="Input number", code="number = int(input())", slot="s1"),
                     dict(id="inbad", t="process", text="Input number", code="number = int(input())", slot=None,
                          why="Input and output always use a parallelogram, not a rectangle."),
                     dict(id="rem", t="process", text="remainder = number MOD 2", code="remainder = number MOD 2", slot="s2",
                          why="Work out the remainder first, straight after the input."),
                     dict(id="dec", t="decision", text="remainder == 0?", code="remainder == 0", slot="s3"),
                     dict(id="decbad", t="process", text="remainder == 0?", slot=None, code="remainder == 0",
                          why="A question with a Yes or No answer goes in a diamond."),
                     dict(id="even", t="io", text='Output "Even"', code='print("Even")', slot="s4",
                          why="A remainder of 0 means the number divides by 2 exactly, so it is even: that is the Yes branch."),
                     dict(id="odd", t="io", text='Output "Odd"', code='print("Odd")', slot="s5",
                          why="A remainder of 1 means odd, which is the No branch."),
                 ],
                 tests=[dict(inputs=["4"], expect=["Even"]), dict(inputs=["7"], expect=["Odd"]), dict(inputs=["0"], expect=["Even"])]),
            dict(problem="Output the numbers 1 to 5, using a loop.",
                 flow=[START,
                       node("b1", "slot", "", slot="s1", label="1"),
                       node("w1", "while", "", slot="s2", label="2", body=[
                           node("b3", "slot", "", slot="s3", label="3"),
                           node("b4", "slot", "", slot="s4", label="4")]),
                       END],
                 cards=[
                     dict(id="c1", t="process", text="count = 1", slot="s1"),
                     dict(id="c0", t="process", text="count = 0", slot=None,
                          why="Starting at 0 would output 0 first. The task says count from 1."),
                     dict(id="cond", t="decision", text="count <= 5?", code="count <= 5", slot="s2"),
                     dict(id="condbad", t="decision", text="count < 5?", code="count < 5", slot=None,
                          why="With count < 5 the loop stops before it outputs 5."),
                     dict(id="show", t="io", text="Output count", code="print(count)", slot="s3",
                          why="Output the number first, then add 1, so 1 is the first number shown."),
                     dict(id="inc", t="process", text="count = count + 1", slot="s4",
                          why="Add 1 after the output, at the end of the loop."),
                     dict(id="dec", t="process", text="count = count - 1", slot=None,
                          why="Taking 1 away means count never reaches 5, so the loop would never end."),
                 ],
                 tests=[dict(inputs=[], expect=["1", "2", "3", "4", "5"])]),
        ]),
        hints=[
            "Inputs and outputs use parallelograms, calculations use rectangles, and questions use diamonds.",
            "Follow the arrows from Start with a test value. What happens at each box?",
            "Pixel has placed one card for you.",
        ],
        skill="You built flowcharts with the standard symbols and tested them with data.",
        cheer=("FLOW-NOMENAL! Your flowcharts use the right symbols and pass every test. "
               "That is exactly how algorithms are designed before they are coded."),
        remember=dict(q="Which flowchart symbol is used for a decision?",
                      options=["A diamond", "A rectangle", "A parallelogram", "An oval"],
                      answer=0,
                      why="A decision is a diamond with two exits, Yes and No."),
        curriculum=[KS3, J277_ALG],
        solution=("Odd or even: Input number, remainder = number MOD 2, decision remainder == 0?, Yes: Output \"Even\", "
                  "No: Output \"Odd\". Count: count = 1, loop while count <= 5?, Output count, count = count + 1."),
    ),
    # 5 -----------------------------------------------------------------
    dict(
        title="Traffic Light Simulator",
        engine="flowbuild",
        objective="Complete a control algorithm and test it in a simulation.",
        learn=("A pelican crossing is controlled by an algorithm: it waits for the button, then changes the traffic lights and the green man in a safe order. "
               "A loop keeps checking the button until someone presses it. "
               "If the steps are in the wrong order, people could get hurt, so the order matters."),
        task="Finish the crossing's flowchart by dragging each step into its box. Then run the simulation.",
        data=dict(rounds=[
            dict(problem="Control a pelican crossing: wait for the button, then stop the traffic safely so people can cross.",
                 sim="pelican",
                 flow=[START,
                       proc("g1", "Lights: green", 'lights("green")'),
                       proc("m1", "Man: red", 'man("red")'),
                       node("u1", "until", "", slot="s1", label="1", body=[proc("w1", "Wait 1 second", "wait(1)")]),
                       node("b2", "slot", "", slot="s2", label="2"),
                       proc("w3", "Wait 3 seconds", "wait(3)"),
                       node("b3", "slot", "", slot="s3", label="3"),
                       node("b4", "slot", "", slot="s4", label="4"),
                       proc("w8", "Wait 8 seconds", "wait(8)"),
                       node("b5", "slot", "", slot="s5", label="5"),
                       END],
                 cards=[
                     dict(id="press", t="decision", text="Button pressed?", code="pressed()", slot="s1"),
                     dict(id="pressbad", t="decision", text="Has 1 second passed?", code="true", slot=None,
                          why="The lights should only change when someone presses the button."),
                     dict(id="redq", t="decision", text="Are the lights red?", code="false", slot=None,
                          why="The lights stay green while the crossing waits, so this question would keep it waiting for ever."),
                     dict(id="amber", t="process", text="Lights: amber", code='lights("amber")', slot="s2",
                          why="Cars get an amber warning before the red light."),
                     dict(id="red", t="process", text="Lights: red", code='lights("red")', slot="s3",
                          why="The traffic must be stopped by a red light before anyone is told to cross."),
                     dict(id="gman", t="process", text="Man: green", code='man("green")', slot="s4",
                          why="The green man only comes on once the traffic lights are red."),
                     dict(id="rman", t="process", text="Man: red", code='man("red")', slot="s5",
                          why="When the crossing time is over, the man goes back to red."),
                     dict(id="green", t="process", text="Lights: green", code='lights("green")', slot=None,
                          why="The lights are already green. They must change to amber, then red, before people cross."),
                 ]),
        ]),
        hints=[
            "Think about safety: what must happen to the cars before people are told to cross?",
            "The loop at box 1 keeps waiting until something happens. What is the crossing waiting for?",
            "Pixel has placed one card for you.",
        ],
        skill="You completed a control algorithm with a loop and tested it in a simulation.",
        cheer=("SAFE CROSSING! Your algorithm stops the traffic before the green man shows. "
               "Real traffic engineers test their algorithms in simulations just like this."),
        remember=dict(q="In the crossing's algorithm, what does the loop do?",
                      options=["It keeps checking the button until someone presses it",
                               "It makes the lights flash faster",
                               "It counts the cars",
                               "It ends the program straight away"],
                      answer=0,
                      why="A condition-controlled loop repeats until its condition, button pressed, becomes true."),
        curriculum=[KS3, J277_ALG],
        solution=("Box 1: Button pressed? Box 2: Lights: amber. Box 3: Lights: red. Box 4: Man: green. Box 5: Man: red."),
    ),
    # 6 -----------------------------------------------------------------
    dict(
        title="Car Driving Challenge",
        engine="botcode",
        objective="Use selection inside a loop so one algorithm drives every track.",
        learn=("A self-driving car repeats the same check again and again: is there road ahead? "
               "A while loop repeats until the car reaches the finish, and if, elseif and else choose what to do each time. "
               "One good algorithm should work on every track, not just one."),
        task="Practise on track 1 with the driving buttons if you like. Then fill the gaps so one algorithm drives all three tracks.",
        data=dict(look="car", maxSteps=400,
                  boards=[
                      dict(name="Track 1", dir="right",
                           grid=["#########",
                                 "#S....###",
                                 "#####.###",
                                 "#####...F",
                                 "#########"]),
                      dict(name="Track 2", dir="right",
                           grid=["##########",
                                 "#S...#####",
                                 "####.#####",
                                 "####....##",
                                 "#######.##",
                                 "#######..F",
                                 "##########"]),
                      dict(name="Track 3", dir="up",
                           grid=["#########",
                                 "#.....###",
                                 "#.###.###",
                                 "#F###.###",
                                 "#####S###",
                                 "#########"]),
                  ],
                  template=LOOP_TEMPLATE, choices=CAR_CHOICES,
                  answer=dict(w="NOT atFinish()", c1="roadAhead()", a1="forward()", c2="roadOnLeft()", a2="turnLeft()", a3="turnRight()")),
        hints=[
            "The loop should keep going while the car is NOT at the finish.",
            "Check for road ahead first. If there is none, check one side and turn that way; otherwise turn the other way.",
            "Pixel has filled one gap for you.",
        ],
        skill="You used selection inside a loop to make one algorithm work on every track.",
        cheer=("VROOM VROOM! One algorithm, three tracks, zero crashes. "
               "Selection inside a loop is how real self-driving systems make decisions."),
        remember=dict(q="Why does the car's algorithm use a while loop?",
                      options=["To keep checking and moving until it reaches the finish",
                               "To make the car go faster",
                               "To choose between left and right",
                               "So the program runs only once"],
                      answer=0,
                      why="The loop repeats the checks until its condition, not at the finish, becomes false."),
        curriculum=[KS3, J277_PROG],
        solution=("while NOT atFinish(): if roadAhead() then forward() elseif roadOnLeft() then turnLeft() else turnRight(). "
                  "Checking roadOnRight() and turning right, else left, also works."),
    ),
    # 7 -----------------------------------------------------------------
    dict(
        title="Fix the Broken Flowchart",
        engine="flowfix",
        objective="Use test data to find and fix the step that makes a flowchart go wrong.",
        learn=("Testing means running an algorithm with chosen data and comparing what it does with what it should do. "
               "When a test fails, follow the path the data took through the flowchart to find the step that went wrong. "
               "Boundary values, like exactly 18, are where bugs often hide."),
        task="Run the tests, then click the step that makes a test fail and choose the fix. Fix all three flowcharts.",
        data=dict(rounds=[
            dict(title="Adult or child ticket",
                 flow=[START,
                       out("in", "Input age", "age = int(input())"),
                       node("d", "decision", "age > 18?", "age > 18",
                            yes=[out("ad", 'Output "Adult"', 'print("Adult")')],
                            no=[out("ch", 'Output "Child"', 'print("Child")')]),
                       END],
                 tests=[dict(inputs=["12"], expect=["Child"]), dict(inputs=["30"], expect=["Adult"]), dict(inputs=["18"], expect=["Adult"])],
                 bug="d",
                 fixes=[dict(text="age >= 18?", code="age >= 18"), dict(text="age < 18?", code="age < 18"),
                        dict(text="age == 18?", code="age == 18"), dict(text="age >= 30?", code="age >= 30")],
                 answer=0,
                 why="Someone who is exactly 18 is an adult, so the test must be age >= 18. The boundary value 18 caught the bug."),
            dict(title="Count to 5",
                 flow=[START,
                       proc("c1", "count = 1"),
                       node("w", "while", "count < 5?", "count < 5", body=[
                           out("o", "Output count", "print(count)"),
                           proc("inc", "count = count + 1")]),
                       END],
                 tests=[dict(inputs=[], expect=["1", "2", "3", "4", "5"])],
                 bug="w",
                 fixes=[dict(text="count <= 5?", code="count <= 5"), dict(text="count > 5?", code="count > 5"),
                        dict(text="count < 4?", code="count < 4"), dict(text="count == 5?", code="count == 5")],
                 answer=0,
                 why="With count < 5 the loop stops when count reaches 5, before outputting it. count <= 5 outputs 5 too."),
            dict(title="Add up three numbers",
                 flow=[START,
                       proc("t0", "total = 0"),
                       proc("k0", "count = 0"),
                       node("u", "until", "count == 3?", "count == 3", body=[
                           out("in", "Input n", "n = int(input())"),
                           proc("p", "total = n"),
                           proc("k", "count = count + 1")]),
                       out("o", "Output total", "print(total)"),
                       END],
                 tests=[dict(inputs=["2", "3", "4"], expect=["9"]), dict(inputs=["5", "5", "5"], expect=["15"])],
                 bug="p",
                 fixes=[dict(text="total = total + n", code="total = total + n"), dict(text="total = n + 1", code="total = n + 1"),
                        dict(text="total = total * n", code="total = total * n"), dict(text="total = count + n", code="total = count + n")],
                 answer=0,
                 why="total = n throws away the running total each time. total = total + n adds each number on."),
        ]),
        hints=[
            "Run the tests first. Which test fails, and what did it output instead?",
            "Follow the failing test's data through the flowchart, box by box. Where does it go the wrong way?",
            "Pixel has pointed to the broken step for you.",
        ],
        skill="You used test data, including boundary values, to find and fix bugs in flowcharts.",
        cheer=("BUG BUSTER! Your tests found every bug, and your fixes passed them all. "
               "Testing with boundary values is what professional developers do."),
        remember=dict(q="Why is 18 a good test value for an 'adult if 18 or over' check?",
                      options=["It is a boundary value, right on the edge of the rule",
                               "It is the biggest possible age",
                               "It is an invalid age",
                               "Any number would test it just as well"],
                      answer=0,
                      why="Boundary values sit exactly on the edge of a rule, which is where > and >= mistakes show up."),
        curriculum=[KS3, J277_TEST],
        solution=("Ticket: change the decision to age >= 18? Count: change the loop to count <= 5? "
                  "Total: change total = n to total = total + n."),
    ),
    # 8 -----------------------------------------------------------------
    dict(
        title="Pseudocode Detective",
        engine="quest",
        objective="Order, debug and trace pseudocode.",
        learn=("Pseudocode is an algorithm written in structured English that looks like code. "
               "OCR's version uses words like if, then, else, endif, for, next, while and endwhile, and = to store a value in a variable. "
               "A trace table follows a program line by line to record what each variable holds."),
        task="Put the pseudocode in order, find and fix a bug, then complete a trace table. There are three stages.",
        data=dict(stages=[
            dict(title="Put the code in order", engine="order", data=dict(
                problem="Output the larger of two numbers.", kicker="Algorithm", code=True,
                items=[
                    dict(id="l1", text='a = int(input("First number: "))'),
                    dict(id="l2", text='b = int(input("Second number: "))'),
                    dict(id="l3", text="if a > b then"),
                    dict(id="l4", text="    print(a)"),
                    dict(id="l5", text="else"),
                    dict(id="l6", text="    print(b)"),
                    dict(id="l7", text="endif"),
                ],
                order=["l1", "l2", "l3", "l4", "l5", "l6", "l7"],
                rules=[["l1", "l3", "Both numbers must be input before the program can compare them."],
                       ["l2", "l3", "Both numbers must be input before the program can compare them."],
                       ["l3", "l4", "The if line comes before the code it controls."],
                       ["l4", "l5", "The code for when a is bigger goes between if and else."],
                       ["l5", "l6", "The code after else runs when a is not bigger."],
                       ["l6", "l7", "endif closes the if statement, so it comes last."]])),
            dict(title="Find and fix the bug", engine="sequence", data=dict(look="number", rounds=[
                dict(type="code", text="This program should add up the numbers 1 to 4 and print 10.",
                     code="total = 0\nfor i = 1 to 3\n    total = total + i\nnext i\nprint(total)",
                     expect=["10"], bug=2,
                     fixes=["for i = 1 to 4", "for i = 0 to 3", "for i = 2 to 4", "for i = 1 to 5"], answer=0,
                     why="The loop must run for i = 1, 2, 3 and 4, so it should go from 1 to 4."),
            ])),
            dict(title="Trace the program", engine="trace", data=dict(rounds=[
                dict(code="x = 3\ntotal = 0\nwhile x > 0\n    total = total + x\n    x = x - 1\nendwhile\nprint(total)",
                     cols=["x", "total", "output"],
                     rows=[["3", "0", ""], ["2", "3", ""], ["1", "5", ""], ["0", "6", ""], ["", "", "6"]],
                     given=[[0, 0], [0, 1]],
                     note="Each row shows the values after one pass of the loop. The last row is the output."),
            ])),
        ]),
        hints=[
            "Read the pseudocode line by line, as the computer would.",
            "In a trace table, change one value at a time, in the order the lines run.",
            "Pixel has done one step of this stage for you.",
        ],
        skill="You ordered, debugged and traced pseudocode written in OCR style.",
        cheer=("CASE CLOSED, DETECTIVE! You can read, fix and trace pseudocode. "
               "That is exactly what GCSE exam questions ask you to do."),
        remember=dict(q="What is a trace table used for?",
                      options=["To record the value of each variable as a program runs, line by line",
                               "To draw a flowchart",
                               "To make a program run faster",
                               "To store the program's code"],
                      answer=0,
                      why="A trace table follows a program step by step, recording variables and output, to check or debug it."),
        curriculum=[KS3, J277_ALG, J277_TEST],
        solution=("Stage 1: the two inputs (either order), if a > b then, print(a), else, print(b), endif. "
                  "Stage 2: line 2 should be for i = 1 to 4. Stage 3: x goes 3, 2, 1, 0; total goes 0, 3, 5, 6; the output is 6."),
    ),
    # 9 -----------------------------------------------------------------
    dict(
        title="Snake Algorithm Challenge",
        engine="botcode",
        objective="Write one algorithm, in pseudocode, that solves several different boards.",
        learn=("A snake that hunts by itself needs an algorithm: look for food ahead, to the left and to the right, then move. "
               "The same few rules, repeated in a loop, can clear any trail of food, but a snake that turns more than twice in a row gets dizzy. "
               "Write it once, then test it on every board."),
        task="Fill the gaps, or type your own pseudocode, so the snake eats all the food on all three boards. Test it, fix it and test again.",
        data=dict(look="snake", maxSteps=500, typing=True,
                  boards=[
                      dict(name="Board 1", dir="right",
                           grid=["#########",
                                 "#S****..#",
                                 "#....*..#",
                                 "#....*..#",
                                 "#########"]),
                      dict(name="Board 2", dir="up",
                           grid=["#########",
                                 "#***....#",
                                 "#..*....#",
                                 "#..*....#",
                                 "#..S....#",
                                 "#########"]),
                      dict(name="Board 3", dir="right",
                           grid=["##########",
                                 "#S***....#",
                                 "#...*....#",
                                 "#...***..#",
                                 "#.....*..#",
                                 "#.....**.#",
                                 "##########"]),
                  ],
                  template=LOOP_TEMPLATE, choices=SNAKE_CHOICES,
                  answer=dict(w="NOT allEaten()", c1="foodAhead()", a1="forward()", c2="foodOnLeft()", a2="turnLeft()", a3="turnRight()")),
        hints=[
            "Keep looping while NOT all the food is eaten.",
            "If there is food ahead, move forward. If not, check one side and turn towards the food.",
            "Pixel has filled one gap for you.",
        ],
        skill="You wrote one algorithm in pseudocode and tested it on several different boards.",
        cheer=("SSSUPER CODER! One algorithm cleared every board. "
               "Writing general solutions, then testing them on lots of cases, is real programming."),
        remember=dict(q="Why test the snake's algorithm on three different boards?",
                      options=["To check it works in general, not just for one layout",
                               "Because the first board might be broken",
                               "To make the snake longer",
                               "Testing once is never allowed"],
                      answer=0,
                      why="An algorithm that passes many different tests is much more likely to be correct in general."),
        curriculum=[KS3, J277_PROG],
        solution=("while NOT allEaten(): if foodAhead() then forward() elseif foodOnLeft() then turnLeft() else turnRight(). "
                  "Checking foodOnRight() and turning right, else left, also works."),
    ),
    # 10 ----------------------------------------------------------------
    dict(
        title="Algorithm Grand Master",
        engine="quest",
        objective="Test, trace and debug algorithms in flowcharts and pseudocode.",
        learn=("Good programmers do not just write algorithms: they test them with normal, boundary, invalid and erroneous data, "
               "trace them to check every step, and debug anything that goes wrong. "
               "This final challenge asks you to do all of that."),
        task="Fix a flowchart with tests, choose test data, trace a program and debug pseudocode. There are four stages.",
        data=dict(stages=[
            dict(title="Fix the pass mark", engine="flowfix", data=dict(rounds=[
                dict(title="Pass or fail",
                     flow=[START,
                           out("in", "Input mark", "mark = int(input())"),
                           node("d", "decision", "mark > 50?", "mark > 50",
                                yes=[out("p", 'Output "Pass"', 'print("Pass")')],
                                no=[out("f", 'Output "Fail"', 'print("Fail")')]),
                           END],
                     tests=[dict(inputs=["30"], expect=["Fail"]), dict(inputs=["75"], expect=["Pass"]), dict(inputs=["50"], expect=["Pass"])],
                     bug="d",
                     fixes=[dict(text="mark >= 50?", code="mark >= 50"), dict(text="mark < 50?", code="mark < 50"),
                            dict(text="mark == 50?", code="mark == 50"), dict(text="mark >= 75?", code="mark >= 75")],
                     answer=0,
                     why="A mark of exactly 50 passes, so the test must be mark >= 50."),
            ])),
            dict(title="Choose the test data", engine="group", data=dict(
                problem="A program accepts whole-number exam marks from 0 to 100.",
                kicker="The rule",
                zones=[dict(id="normal", label="Normal", icon="✅"),
                       dict(id="boundary", label="Boundary", icon="📏"),
                       dict(id="invalid", label="Invalid", icon="🚫"),
                       dict(id="erroneous", label="Erroneous", icon="💥")],
                items=[
                    dict(id="n45", text="45", icon="🔢", zone="normal", why="45 is a typical mark well inside the range: normal data."),
                    dict(id="n72", text="72", icon="🔢", zone="normal", why="72 is a typical mark inside the range: normal data."),
                    dict(id="b0", text="0", icon="🔢", zone="boundary", why="0 is the lowest allowed mark, right on the edge: boundary data."),
                    dict(id="b100", text="100", icon="🔢", zone="boundary", why="100 is the highest allowed mark, right on the edge: boundary data."),
                    dict(id="i-5", text="-5", icon="🔢", zone="invalid", why="-5 is a whole number, but outside 0 to 100, so it should be rejected: invalid data."),
                    dict(id="i150", text="150", icon="🔢", zone="invalid", why="150 is a whole number, but above 100: invalid data."),
                    dict(id="eabc", text='"abc"', icon="🔤", zone="erroneous", why='"abc" is not a number at all, the wrong data type: erroneous data.'),
                    dict(id="etw", text='"twelve"', icon="🔤", zone="erroneous", why='"twelve" is text, not a number: erroneous data.'),
                ])),
            dict(title="Trace the program", engine="trace", data=dict(rounds=[
                dict(code="count = 0\nfor i = 1 to 4\n    if i MOD 2 == 0 then\n        count = count + i\n    endif\nnext i\nprint(count)",
                     cols=["i", "count", "output"],
                     rows=[["", "0", ""], ["1", "0", ""], ["2", "2", ""], ["3", "2", ""], ["4", "6", ""], ["", "", "6"]],
                     given=[[0, 1], [1, 0], [1, 1]],
                     note="Each row after the first shows the values at the end of one pass of the loop."),
            ])),
            dict(title="Debug the pseudocode", engine="sequence", data=dict(look="number", rounds=[
                dict(type="code", text="This program should print Odd, Even, Odd, Even for the numbers 1 to 4.",
                     code='for n = 1 to 4\n    if n MOD 2 == 1 then\n        print("Even")\n    else\n        print("Odd")\n    endif\nnext n',
                     expect=["Odd", "Even", "Odd", "Even"], bug=2,
                     fixes=["    if n MOD 2 == 0 then", "    if n MOD 2 == 2 then", "    if n DIV 2 == 1 then", "    if n == 1 then"], answer=0,
                     why="n MOD 2 == 1 is true for odd numbers, but that branch prints Even. Testing for == 0 sends even numbers to Even."),
            ])),
        ]),
        hints=[
            "Use the tests and the trace to see exactly where an algorithm goes wrong.",
            "Boundary data sits exactly on the edge of the rule; invalid data is the right type but out of range; erroneous data is the wrong type.",
            "Pixel has done one step of this stage for you.",
        ],
        skill="You tested, traced and debugged algorithms in flowcharts and pseudocode.",
        cheer=("ALGORITHM GRAND MASTER! You can design, test, trace and debug like a real programmer. "
               "Every computer scientist started exactly where you are now."),
        remember=dict(q="A program accepts ages from 11 to 16. Which value is boundary data?",
                      options=["16", "13", "25", '"ten"'],
                      answer=0,
                      why="16 is right on the upper edge of the allowed range, so it is boundary data."),
        curriculum=[KS3, J277_ALG, J277_TEST],
        solution=("Stage 1: change the decision to mark >= 50? Stage 2: normal 45 and 72; boundary 0 and 100; invalid -5 and 150; "
                  "erroneous \"abc\" and \"twelve\". Stage 3: count goes 0, 0, 2, 2, 6 and the output is 6. "
                  "Stage 4: line 2 should be if n MOD 2 == 0 then."),
    ),
]
