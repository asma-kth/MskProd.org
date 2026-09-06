"""End of unit assessment papers for Key Stage 3.

Two assessment points a year, matching the school's long term plan. The autumn
paper covers the units taught up to that point in the year and the summer paper
covers the whole year, weighted towards the later units. Every question is
original, written to the same structure and mark scheme conventions as the GCSE
papers so that assessment feels familiar long before Year 10.
"""
from content.papers import Paper
from mskbuild.models import EQ, MP

# ============================================================ Year 7 Autumn

Y7_AUTUMN = Paper(
    slug="ks3-year-7-autumn",
    title="Year 7 Computing: Autumn Assessment",
    course="Key Stage 3",
    board="MskProd",
    code="Year 7 Autumn",
    minutes=0,
    marks=0,
    accent="var(--lilac-deep)",
    blurb="Your first assessment in computing. It covers using computers, hardware and software, files and folders, staying safe on the school network, and programming in Scratch.",
    advice="Answer every question, even if you are not sure. The number of marks tells you how many separate points to make, so a three mark question needs three things, not one thing said three times. Write in full sentences.",
    calculator="No calculator is permitted.",
    questions=[
        EQ("State what is meant by the term hardware.", 1, [
            MP("The physical parts of a computer that you can touch", ["physical", "touch", "parts you can see", "you can hold", "solid parts"]),
        ], "Hardware means the physical parts of a computer system, the pieces you can actually touch, such as the keyboard, the screen and the hard drive.", "State"),

        EQ("Name one input device and one output device.", 2, [
            MP("Names a valid input device", ["keyboard", "mouse", "microphone", "scanner", "camera", "sensor", "touchscreen", "controller"]),
            MP("Names a valid output device", ["monitor", "screen", "printer", "speaker", "headphones", "projector", "motor"]),
        ], "A keyboard is an input device, because it lets data go into the computer. A printer is an output device, because it takes the results out of the computer and puts them onto paper.", "Name"),

        EQ("State one difference between system software and application software.", 2, [
            MP("System software runs the computer itself, for example the operating system", ["operating system", "runs the computer", "controls the computer", "needed to work", "windows", "android"]),
            MP("Application software lets the user carry out a task", ["task", "browser", "word processor", "game", "job done", "photo editor", "app for a job"]),
        ], "System software runs the computer itself. The operating system, such as Windows or Android, is the main example, and without it the computer would not work at all. Application software is installed so that the user can carry out a particular task, such as a browser for looking at web pages or a word processor for writing.", "State"),

        EQ("A student saves every piece of work straight onto the desktop with names like new1, new2 and new3. Describe two problems this will cause, and state one thing they should do instead.", 3, [
            MP("The names do not say what is in the file, so work is hard to find", ["hard to find", "cannot find", "difficult to find", "does not say", "no idea what", "waste time looking"]),
            MP("The wrong file could be handed in, or work could be overwritten by mistake", ["wrong file", "hand in", "overwrite", "lose work", "muddled", "mixed up", "save over"]),
            MP("They should use sensible file names and folders for each subject and topic", ["sensible name", "meaningful name", "folder", "subject", "organise", "hierarchy", "name that says"]),
        ], "The first problem is that names like new1 tell you nothing about what is inside the file, so finding a particular piece of work later means opening one file after another until the right one appears. The second problem is that it becomes very easy to hand in the wrong file, or to save over work that was already there, because nothing on the screen distinguishes one file from another. Instead they should give every file a name that says what it is, such as year7-networks-homework, and store files in folders arranged by subject and then by topic.", "Describe"),

        EQ("Give three reasons why you should log off a school computer when you have finished using it.", 3, [
            MP("Anything done afterwards on that account looks as though you did it", ["look like you", "blamed", "appear that you", "your name", "pretend to be you", "in trouble"]),
            MP("Someone else could read, change or delete your work", ["read your files", "delete", "change your work", "see your files", "access your work", "copy your work"]),
            MP("Someone could send messages or post something as you", ["send messages", "post", "email", "message as you", "impersonate", "say things"]),
        ], "The first reason is that your account is yours, so anything done while you are still logged in looks exactly as though you did it, and you would have to explain it. The second reason is that anyone who sits down at the machine can open, change or delete your work, and a whole term of work can disappear in seconds. The third reason is that they could send messages or post things using your account, which could get you into serious trouble and would be very hard to prove was not you.", "Give"),

        EQ("Explain why the order of the blocks in a Scratch script matters. Use an example in your answer.", 3, [
            MP("A computer carries out instructions in the order they are given", ["in order", "one after another", "order they are given", "top to bottom", "sequence", "step by step"]),
            MP("Swapping two blocks changes what the program actually does", ["different result", "changes what", "wrong place", "does not work", "not what you wanted", "wrong output"]),
            MP("Gives a sensible example", ["move 100 steps", "turn 90", "sprite ends up", "draws the wrong", "says hello", "moves first", "turns first"]),
        ], "A computer is extremely literal. It carries out the blocks in exactly the order they are joined together, from the top of the script downwards, and it never works out what you meant. That means putting the right blocks in the wrong order is just as wrong as using the wrong blocks. For example, if a sprite is told to move 100 steps and then turn 90 degrees it walks along one side of a square and then faces a new direction, but if the turn block is put first the sprite turns on the spot and then walks off in a completely different direction, so the finished drawing is wrong.", "Explain"),

        EQ("Explain why a variable is used to keep the score in a Scratch game.", 3, [
            MP("A variable is a named store that holds a value while the program runs", ["stores a value", "named box", "holds the score", "store", "keeps a value", "remembers"]),
            MP("The score has to change during the game", ["change", "goes up", "increase", "change score by 1", "add one", "not fixed"]),
            MP("The stored value can then be tested or displayed, for example to decide when the player wins", ["display", "show", "test", "compare", "if score", "win", "check the value", "on the stage"]),
        ], "A variable is a named box that holds a value while the program is running, and the value inside it can be changed. The score has to change constantly during a game, going up by one every time the player collects something, so it cannot simply be written into the blocks as a fixed number. Because the value is stored under a name, the program can also read it back, for example showing it on the stage and testing whether the score has reached ten so that the game can say the player has won.", "Explain"),

        EQ("Describe how you would use a repeat block to make a sprite draw a pentagon, and give one advantage of using a loop rather than joining the same blocks five times.", 4, [
            MP("Uses a repeat block set to five", ["repeat 5", "repeat five", "five times", "loop five"]),
            MP("Inside the loop the sprite moves a set number of steps", ["move 100 steps", "move steps", "move forward", "moves a set"]),
            MP("Inside the loop the sprite turns 72 degrees", ["72", "360 divided by 5", "turn 72 degrees", "exterior angle"]),
            MP("The script is shorter and easier to change or correct", ["shorter", "fewer blocks", "less blocks", "easier to change", "easier to read", "one place", "quicker to build"]),
        ], "I would use a repeat block set to five, and inside it put a move 100 steps block followed by a turn 72 degrees block. Each time round the loop the sprite draws one side and then turns ready for the next one, and after five repeats the shape closes because the five turns add up to 360 degrees. The advantage of the loop is that the script is far shorter and much easier to change. If I decide to draw a hexagon instead I only have to change two numbers in one place, whereas with the blocks written out five times I would have to add another pair of blocks and edit every turn.", "Describe"),

        EQ("A quiz sprite asks 'What colour is the sky?' and should say 'Correct' if the answer is blue, and 'Try again' if it is not. Write the blocks you would use.", 3, [
            MP("Uses an ask and wait block so the reply is stored in answer", ["ask", "answer", "ask and wait", "asks the question"]),
            MP("Uses an if then else block with the condition answer = blue", ["if", "else", "answer = blue", "condition", "if then else"]),
            MP("Says Correct when true and Try again when false", ["say correct", "correct", "try again", "well done"]),
        ], "When the green flag is clicked, use an ask 'What colour is the sky?' and wait block, which stores what the player types in the answer box. Then use an if answer = blue then, else block. Inside the if part put say 'Correct' for two seconds, and inside the else part put say 'Try again' for two seconds. Only one of the two paths runs, so the sprite gives exactly one reply each time.", "Write"),

        EQ("A Scratch game should stop when lives reaches 0, but it carries on forever. Explain two possible causes of this bug, and describe how you would check each one.", 4, [
            MP("The condition may be wrong, for example using the wrong operator or the wrong way round", ["wrong operator", "wrong way round", "less than", "greater than", "condition is wrong", "should be =", "not 0"]),
            MP("Nothing in the game may actually reduce lives, so the condition is never true", ["never changes", "not reduced", "change lives by -1", "never reaches 0", "nothing reduces", "does not go down"]),
            MP("Check by showing the variable on the stage and watching it while playing", ["show the variable", "display", "watch", "tick the box", "stage", "see the value"]),
            MP("Check by clicking the blocks one at a time or adding a say block to see what is happening", ["click the blocks", "one at a time", "say block", "test each", "step through", "add a say"]),
        ], "One possible cause is that the condition is wrong. If the block says repeat until lives greater than 0 rather than lives = 0, the loop will never end, because the test is the wrong way round. The other likely cause is that nothing in the game ever reduces lives, so it stays at three forever and the stopping condition is never true. To check the first, I would read the condition carefully and try it with lives set to zero by hand. To check the second, I would tick the box next to the lives variable so that it shows on the stage, then play the game and watch whether the number actually goes down when the sprite is hit. Clicking individual blocks to see what each one does is the quickest way to find the block that is missing.", "Explain"),

        EQ("Describe how an event and a broadcast are used so that clicking a start button sprite makes a second sprite begin moving.", 4, [
            MP("An event block starts a script when something happens", ["event", "starts a script", "triggers", "hat block", "when something happens"]),
            MP("The button uses a when this sprite clicked block", ["when this sprite clicked", "sprite clicked", "clicking the button", "click the sprite"]),
            MP("The button then broadcasts a message", ["broadcast", "send a message", "message", "broadcast start"]),
            MP("The second sprite has a when I receive block that runs its movement", ["when i receive", "receive", "picks up the message", "then moves", "other sprite runs"]),
        ], "An event block is a block that starts a script when something particular happens. On the button sprite I would use a when this sprite clicked block, and underneath it a broadcast start block, which sends a message that every sprite in the project can hear. On the second sprite I would use a when I receive start block, and join the movement blocks underneath it. Clicking the button therefore triggers the message, the message triggers the second script, and the two sprites work together without either one needing to know anything about the other's blocks.", "Describe"),

        EQ("A student's Scratch program does not do what they expected. Describe four checks they could make to find the problem.", 4, [
            MP("Check the order of the blocks", ["order", "sequence", "right order", "wrong order"]),
            MP("Check that every variable is set at the start", ["set to 0", "variable is set", "reset", "set at the start", "left over from last time"]),
            MP("Check the conditions are the right way round", ["condition", "greater than", "less than", "right way round", "wrong operator", "wrong symbol"]),
            MP("Check the script is on the correct sprite, and click blocks one at a time to see what they do", ["right sprite", "correct sprite", "wrong sprite", "click the blocks", "one at a time", "test each block"]),
        ], "First they should read the order of the blocks, because a script with the right blocks in the wrong order is one of the most common faults. Second they should check that every variable is set at the start, since a score or a timer left over from the last game causes strange behaviour the moment the green flag is clicked. Third they should look closely at every condition, because a greater than sign where a less than sign was meant makes the program do exactly the opposite of what was intended. Fourth they should check the script is attached to the sprite they think it is, and then click each block on its own and watch what happens, which shows very quickly which block is not doing its job.", "Describe"),
    ],
)

# ============================================================ Year 7 Summer

Y7_SUMMER = Paper(
    slug="ks3-year-7-summer",
    title="Year 7 Computing: Summer Assessment",
    course="Key Stage 3",
    board="MskProd",
    code="Year 7 Summer",
    minutes=0,
    marks=0,
    accent="var(--lilac-deep)",
    blurb="The whole of Year 7, with most of the marks on the units taught after Christmas: Python, what is inside the computer, binary, and vector graphics.",
    advice="Show your working in every calculation, because marks are given for the method as well as the answer. In the programming questions, write real Python and keep your indentation clear.",
    calculator="No calculator is permitted.",
    questions=[
        EQ("State how many bits there are in one byte.", 1, [
            MP("8", ["8", "eight"]),
        ], "There are 8 bits in one byte.", "State"),

        EQ("Name the component that carries out the instructions in a program, and name the component that holds the programs and data that are in use right now.", 2, [
            MP("CPU or processor", ["cpu", "processor", "central processing unit"]),
            MP("RAM or main memory", ["ram", "memory", "main memory", "random access memory"]),
        ], "The component that carries out the instructions is the CPU, the central processing unit. The component that holds the programs and data in use right now is RAM, which is wiped as soon as the power is switched off.", "Name"),

        EQ("State what the Python function `int()` does, and state why it is needed after `input()`.", 2, [
            MP("It converts a value into a whole number", ["converts", "whole number", "integer", "changes it to a number", "turns text into a number"]),
            MP("input always gives back text, which cannot be used in a calculation", ["text", "string", "cannot add", "cannot do maths", "always text", "not a number"]),
        ], "The int function converts a value into a whole number. It is needed after input because input always hands back text, even when the user typed digits, and text cannot be used in a calculation. Without the conversion, adding one to the answer would either cause an error or join the characters together instead of doing arithmetic.", "State"),

        EQ("Convert the binary number 10110100 into denary. Show your working.", 3, [
            MP("Writes the place values 128 64 32 16 8 4 2 1 above the digits", ["128 64 32 16 8 4 2 1", "place value", "column headings", "128 64 32"]),
            MP("Identifies the columns holding a 1 as 128, 32, 16 and 4", ["128 + 32 + 16 + 4", "128 32 16 4", "columns with a 1"]),
            MP("Gives the answer 180", ["180"]),
        ], "First I write the place values 128, 64, 32, 16, 8, 4, 2 and 1 above the eight digits. The digits 1 appear in the 128, 32, 16 and 4 columns. Adding those place values gives 128 + 32 + 16 + 4, which is 180. The answer is 180.", "Calculate"),

        EQ("Convert the denary number 73 into 8 bit binary. Show your working.", 3, [
            MP("Takes 64 first, leaving 9", ["64", "73 - 64", "leaving 9", "9 left"]),
            MP("Then 8 fits leaving 1, and then 1 fits leaving 0", ["8", "9 - 8", "leaving 1", "then 1", "1 fits"]),
            MP("Gives the answer 01001001 written as 8 bits", ["01001001", "1001001"]),
        ], "Working from the left, 128 does not fit into 73 so I write 0. 64 does fit, so I write 1 and 73 minus 64 leaves 9. 32 and 16 do not fit, so I write 0 and 0. 8 fits, so I write 1 and 9 minus 8 leaves 1. 4 and 2 do not fit, so I write 0 and 0. 1 fits, so I write 1 and nothing is left. The answer is 01001001, and checking it gives 64 + 8 + 1, which is 73.", "Calculate"),

        EQ("Explain why computers use binary rather than the ten digits people use for counting.", 3, [
            MP("A circuit can easily be in one of two states, on or off", ["on or off", "two states", "switch", "current or no current", "high or low", "electricity"]),
            MP("Those two states are easy to tell apart reliably", ["reliable", "easy to tell apart", "not confused", "clear difference", "fewer mistakes"]),
            MP("Ten different levels would be far harder to build and easier to get wrong", ["ten levels", "harder to build", "voltage", "expensive", "errors", "difficult to make"]),
        ], "The reason is electrical. Everything inside a computer is built from circuits that are either on or off, and those two states are extremely easy to tell apart even when the components are tiny and the signal is weak. Binary needs only two digits, so 1 can mean on and 0 can mean off. Building circuits that could reliably tell ten different voltage levels apart would be far more expensive and far more likely to make mistakes, so two states are used and everything else is built up from them.", "Explain"),

        EQ("Describe the three steps that the CPU repeats over and over while the computer is switched on.", 3, [
            MP("Fetch the next instruction from memory", ["fetch", "gets the instruction", "collects", "from memory"]),
            MP("Decode it to work out what it means", ["decode", "works out what it means", "understands", "interprets"]),
            MP("Execute it, actually carrying out the instruction", ["execute", "carries it out", "does the work", "performs", "runs it"]),
        ], "The CPU fetches the next instruction from memory, then decodes it to work out what that instruction actually means, then executes it by carrying out the work, which might be a calculation, a comparison or moving data. It then goes straight back to the beginning and fetches the next one. This cycle never stops while the computer is on, and a processor running at 3 GHz goes round it three billion times a second.", "Describe"),

        EQ("A student writes `tickets = input('How many tickets? ')` and then `total = tickets * 3`. Instead of the cost, the program prints the number typed in three times over. Explain why this happens, and how to fix it.", 3, [
            MP("input hands back text rather than a number", ["text", "string", "not a number", "always text"]),
            MP("Multiplying text by 3 repeats the characters three times", ["repeats", "three times", "joins", "copies the text", "repeated"]),
            MP("Convert the input with int so the multiplication is arithmetic", ["int", "convert", "integer", "int input", "change it to a number"]),
        ], "The problem is that input always hands back text, so tickets holds the characters typed rather than a number. In Python, multiplying a piece of text by 3 does not do arithmetic, it repeats the text three times, which is exactly what the student is seeing on the screen. The fix is to convert the input into a whole number first, by writing tickets = int(input('How many tickets? ')), after which total = tickets * 3 does real arithmetic and gives the cost.", "Explain"),

        EQ("Write a Python program that asks the user for a mark out of 100, then prints Pass if the mark is 50 or more and prints Fail if it is not.", 4, [
            MP("Uses input to get the mark and converts it to a whole number", ["input", "int", "int input", "asks the user"]),
            MP("Uses an if statement with the condition mark >= 50", ["mark >= 50", ">= 50", "50 or more", "greater than or equal", "if mark"]),
            MP("Prints Pass when the condition is true", ["print pass", "pass"]),
            MP("Uses else to print Fail otherwise", ["else", "print fail", "otherwise fail"]),
        ], "The program is mark = int(input('Enter your mark: ')). Then if mark >= 50: print('Pass'). Then else: print('Fail'). The int function is needed because input gives text and the comparison needs a number. The two lines under the if and the else must be indented by four spaces, and there must be a colon at the end of both the if line and the else line.", "Write"),

        EQ("Compare bitmap and vector images. Give two differences, and state which of the two should be used for a photograph.", 4, [
            MP("A bitmap is stored as a grid of pixels, each with its own colour", ["pixels", "grid", "dots", "each pixel"]),
            MP("A vector is stored as instructions for drawing shapes", ["instructions", "shapes", "maths", "coordinates", "commands", "how to draw"]),
            MP("A bitmap becomes blocky when enlarged but a vector stays sharp at any size", ["blocky", "pixelated", "stays sharp", "any size", "quality", "redrawn"]),
            MP("A photograph should be stored as a bitmap", ["bitmap", "raster", "jpg", "photograph is a bitmap"]),
        ], "A bitmap image is stored as a grid of pixels, with the colour of every single pixel recorded, while a vector image is stored as a list of instructions for drawing shapes, such as a circle at a certain position with a certain radius and fill colour. The second difference follows from the first. Enlarging a bitmap makes it blocky, because there is no extra detail to show and the existing pixels simply get bigger, whereas a vector stays perfectly sharp at any size because the shapes are worked out and drawn again each time. A photograph should be stored as a bitmap, because it is full of irregular detail and slight colour changes that could not sensibly be described as a set of shapes.", "Compare"),

        EQ("Describe two things that make a logo effective, and explain why each one matters.", 4, [
            MP("It is simple", ["simple", "not complicated", "few shapes", "clean", "uncluttered"]),
            MP("So it is still recognisable when it is very small, such as on a browser tab", ["small", "tab", "recognisable", "icon", "tiny", "far away"]),
            MP("A second feature, such as working in one colour, being distinctive, or suiting the audience", ["one colour", "black and white", "distinctive", "different from", "suits the audience", "appropriate", "scalable"]),
            MP("Explains why that second feature matters", ["stands out", "not confused", "remembered", "printed", "engraved", "photocopy", "any size", "sharp", "suits"]),
        ], "The first thing is simplicity. A logo has to be recognisable at sixteen pixels across on a browser tab as well as a metre wide on a banner, and a complicated design turns into a smudge the moment it is made small. The second thing is that it should work in a single colour. Logos end up printed cheaply, stamped, engraved or photocopied, and a design that only reads when every colour is present fails completely in all of those situations. Testing a logo small and in black and white early on saves redesigning it later.", "Describe"),

        EQ("Explain how a photograph is stored on a computer, and explain why a photograph taken at a higher resolution takes up more storage space.", 4, [
            MP("The image is a grid of pixels", ["pixels", "grid", "dots", "squares"]),
            MP("The colour of each pixel is stored as a binary number", ["binary", "number", "code", "stored as numbers", "1s and 0s"]),
            MP("A higher resolution means there are more pixels in the image", ["more pixels", "higher resolution", "more dots", "greater number"]),
            MP("Every extra pixel needs its own number, so the file is bigger", ["each pixel needs", "more numbers", "bigger file", "more data", "more storage", "larger file"]),
        ], "A photograph is stored as a grid of tiny squares called pixels, and the colour of each pixel is recorded as a binary number. The computer also stores the width and height so that it knows how to arrange the pixels back into a picture. Resolution means how many pixels the image contains, so a photograph taken at a higher resolution simply has more of them. Since every single pixel needs its own binary number to record its colour, doubling the number of pixels doubles the number of values stored, and the file gets bigger. That is why a higher quality photograph always takes up more space.", "Explain"),

        EQ("A student records a 30 second sound clip and takes a photograph on the same phone. Explain how both of these are stored using only 1s and 0s, and explain what makes each file larger.", 5, [
            MP("Everything on a computer is stored as binary numbers", ["binary", "1s and 0s", "ones and zeros", "numbers"]),
            MP("Sound is measured, or sampled, many times a second", ["sampled", "samples", "measured", "measurements", "44100", "thousands of times"]),
            MP("Each measurement of the wave is stored as a number", ["height of the wave", "each measurement", "stored as a number", "value", "wave"]),
            MP("An image is a grid of pixels and each pixel colour is stored as a number", ["pixels", "grid", "each pixel", "colour is a number"]),
            MP("More samples per second, or more pixels and more colours, means more numbers and a bigger file", ["more samples", "sample rate", "more pixels", "more colours", "bigger", "more numbers", "larger file"]),
        ], "Everything a computer stores is stored as binary numbers, so both files are really just very long lists of 1s and 0s. Sound is a wave, so the phone measures the height of that wave thousands of times every second, which is called sampling, and each measurement is written down as a number. CD quality takes 44,100 measurements every second. A photograph is a grid of pixels, and the colour of each pixel is also written down as a number, so the picture becomes a long list of colour values. In both cases better quality means more numbers. Taking more samples every second gives a recording that follows the original wave more closely, and using more pixels or more bits for each pixel colour gives a sharper picture with more shades, but each of those choices means more values to store and so a bigger file.", "Explain"),
    ],
)

# ============================================================ Year 8 Autumn

Y8_AUTUMN = Paper(
    slug="ks3-year-8-autumn",
    title="Year 8 Computing: Autumn Assessment",
    course="Key Stage 3",
    board="MskProd",
    code="Year 8 Autumn",
    minutes=0,
    marks=0,
    accent="var(--purple)",
    blurb="Digital literacy and online safety, and computational thinking: decomposition, abstraction, flowcharts, pseudocode, trace tables and test data.",
    advice="Read each question twice and underline the command word. Describe means say what happens, explain means say why it happens. In the trace table question you must show the values, not just the final answer.",
    calculator="No calculator is permitted.",
    questions=[
        EQ("Name the law that makes it a criminal offence to log into someone else's account without their permission.", 1, [
            MP("Computer Misuse Act 1990", ["computer misuse", "misuse act", "computer misuse act 1990"]),
        ], "The Computer Misuse Act 1990. The offence is the unauthorised access itself, so it applies even if nothing is changed and it was meant as a joke.", "Name"),

        EQ("State what is meant by an active digital footprint and by a passive digital footprint.", 2, [
            MP("Active: data you deliberately put online yourself", ["post", "deliberate", "on purpose", "choose to share", "upload", "comments", "yourself"]),
            MP("Passive: data collected about you without you doing anything", ["without you", "collected about you", "automatically", "location", "pages you visit", "tracked", "in the background"]),
        ], "An active digital footprint is made up of the things you deliberately put online yourself, such as photographs, comments, videos and profiles. A passive digital footprint is the data collected about you without you doing anything at all, such as which pages you visit, how long you stay on them, your location and what you search for.", "State"),

        EQ("State what is meant by pattern recognition, and give one example of using it.", 2, [
            MP("Spotting things that are the same or similar so a solution can be reused", ["same", "similar", "repeat", "reuse", "spotting patterns", "in common"]),
            MP("Gives a sensible example", ["width x height", "area", "same steps", "every level", "each shape", "same code", "similar problems"]),
        ], "Pattern recognition means spotting the things that are the same or similar in a problem, so that one solution can be used again rather than solving each part separately. For example, if a program has to work out the area of six different rectangles, you notice that every one of them follows width multiplied by height, so you write that calculation once and use it six times instead of writing six separate pieces of code.", "State"),

        EQ("An email says 'Your account will be closed in 24 hours' and asks you to confirm your password by clicking a link. Describe three things about this message that show it is a phishing attempt.", 3, [
            MP("It creates urgency to stop you thinking", ["urgent", "24 hours", "rush", "threat", "closed", "pressure", "panic", "scare"]),
            MP("It asks for a password, which no genuine organisation does", ["password", "never ask", "details", "personal information", "no company asks"]),
            MP("A suspicious link, a generic greeting, or spelling and grammar mistakes", ["link", "address does not match", "dear customer", "spelling", "grammar", "fake website", "not the real"]),
        ], "The first sign is the urgency. Saying the account will close in 24 hours is designed to panic you into acting before you have had time to think, and real organisations do not work that way. The second sign is that it asks for a password. No legitimate company ever asks you to confirm your password by email, so this on its own is enough to know the message is fake. The third sign is the link, which will lead to an address that is not quite the company's real one, and messages like this often also use a generic greeting such as Dear customer and contain spelling mistakes.", "Describe"),

        EQ("Explain the difference between misinformation and disinformation, and describe one check you could make before sharing a story.", 3, [
            MP("Misinformation is false information shared by someone who believes it is true", ["believes it is true", "by mistake", "not on purpose", "thinks it is true", "accident", "unaware"]),
            MP("Disinformation is false information spread deliberately to mislead", ["deliberate", "on purpose", "mislead", "knows it is false", "intentional", "trick"]),
            MP("Describes a sensible check", ["other sources", "news organisation", "check the date", "who published", "evidence", "reported elsewhere", "fact check"]),
        ], "Misinformation is false information shared by someone who genuinely believes it is true, so the person passing it on is mistaken rather than dishonest. Disinformation is false information spread deliberately in order to mislead people, so the person creating it knows perfectly well that it is untrue. The difference is the intention behind it. Before sharing a story I would check whether it is being reported by other independent news organisations, because a genuine major story is always covered in more than one place, and I would check the date, since old stories are constantly recirculated as though they had just happened.", "Explain"),

        EQ("Explain why two factor authentication keeps an account safe even if the password has been stolen.", 3, [
            MP("A second piece of proof is needed as well as the password", ["second", "two things", "as well as the password", "extra step", "another check"]),
            MP("The second factor is usually something you have, such as a phone or an app code", ["phone", "app", "code", "text message", "device", "fingerprint"]),
            MP("An attacker with only the password still cannot get in", ["cannot log in", "not enough", "still blocked", "needs your phone", "denied", "cannot get in"]),
        ], "Two factor authentication means that a password on its own is never enough to log in, because the account also demands a second piece of proof. That second factor is normally something you physically have, such as a code sent to your phone, a code produced by an authenticator app, or your fingerprint. An attacker who has stolen or guessed the password is somewhere else entirely and does not have your phone, so they are stopped at the second step, and the code arriving unexpectedly also warns you that the password is no longer secret.", "Explain"),

        EQ("A student is receiving unkind messages in a game chat. Describe three things they should do.", 3, [
            MP("Do not reply", ["do not reply", "not respond", "ignore", "no reply"]),
            MP("Screenshot the messages so there is evidence", ["screenshot", "evidence", "save the messages", "record", "proof"]),
            MP("Block and report the account, and tell a trusted adult", ["block", "report", "tell an adult", "teacher", "parent", "trusted adult"]),
        ], "They should not reply, because a reaction is exactly what the person sending the messages wants and replying usually makes it worse. They should take screenshots of everything first, because messages can be deleted and evidence is what makes a report worth acting on. Then they should block and report the account through the game itself, and tell an adult they trust, such as a parent or a teacher. Reporting is not telling tales and they are not the one in trouble.", "Describe"),

        EQ("Describe the purpose of the rectangle, the diamond and the parallelogram in a flowchart.", 3, [
            MP("Rectangle: a process, such as a calculation or an action", ["process", "action", "calculation", "step", "something is done"]),
            MP("Diamond: a decision, a question with two labelled exits", ["decision", "question", "yes and no", "condition", "two branches", "choice"]),
            MP("Parallelogram: input or output", ["input", "output", "data in", "results", "print", "enter"]),
        ], "The rectangle is a process box, used for an action or a calculation such as adding one to a total. The diamond is a decision, which holds a question and always has exactly two exits, labelled yes and no, so the flow splits down one of two paths. The parallelogram is used for input and output, so it covers asking the user to enter something and displaying a result on the screen.", "Describe"),

        EQ("A school wants a program that records how many students order a school dinner each day and then shows the busiest day. Describe how decomposition would help you plan this program.", 4, [
            MP("Decomposition means breaking the problem into smaller problems", ["break", "smaller", "split", "parts", "chunks", "sections"]),
            MP("Identifies getting the number for each day as one part", ["input the number", "each day", "collect the data", "ask for the number", "enter"]),
            MP("Identifies storing the numbers as another part", ["store", "list", "save", "record", "file", "array"]),
            MP("Identifies finding and displaying the busiest day, and notes each part can be built and tested separately", ["busiest", "largest", "maximum", "display", "output", "tested separately", "one at a time", "easier"]),
        ], "Decomposition means breaking a big problem into smaller problems that are each small enough to solve. Here the program breaks into four clear jobs: asking for the number of dinners ordered on each day, storing those five numbers so they are not lost, working out which of them is the largest, and displaying that day on the screen. Once the problem is split up like this, each part can be written and tested on its own, so a fault in the part that finds the largest number cannot be confused with a fault in the part that collects the data. It also makes the work much easier to share between two people.", "Describe"),

        EQ("Complete a trace table for this algorithm and state the final value of total.\n\ntotal = 0, then for i = 1 to 5, if i is odd then total = total + i, next i, print(total)", 4, [
            MP("Identifies that the condition is true when i is 1, 3 and 5", ["odd", "1 3 and 5", "1 3 5"]),
            MP("Shows total becoming 1 and then 4", ["total = 4", "then 4", "1 then 4", "4"]),
            MP("Shows total reaching 9", ["9", "total = 9"]),
            MP("Shows that total does not change when i is 2 or 4", ["2 and 4", "no change", "unchanged", "stays the same", "even"]),
        ], "The loop runs with i taking the values 1, 2, 3, 4 and 5. The condition is true only when i is odd, so it is true for 1, 3 and 5. When i is 1, total becomes 0 plus 1, which is 1. When i is 2 the condition is false, so total stays at 1. When i is 3, total becomes 1 plus 3, which is 4. When i is 4 nothing changes, so total is still 4. When i is 5, total becomes 4 plus 5, which is 9. The final value printed is 9.", "Complete"),

        EQ("Write pseudocode for a program that asks the user for three numbers and then prints the average.", 4, [
            MP("Inputs three numbers", ["input", "enter a number", "ask", "three numbers"]),
            MP("Adds them into a total", ["total", "add", "sum", "+"]),
            MP("Divides the total by 3", ["divide", "3", "divided by 3", "/ 3"]),
            MP("Prints or outputs the average", ["print", "output", "display", "average"]),
        ], "total = 0. Then for i = 1 to 3, number = input('Enter a number'), total = total + number, next i. Then average = total / 3. Then print('The average is ' + average). Using a loop keeps it short, but writing three separate input lines and adding them together is equally acceptable as long as the total is divided by three and the answer is printed.", "Write"),

        EQ("A program accepts a mark between 0 and 100. Give one example each of normal, boundary and erroneous test data, and explain why boundary data is the most useful of the three.", 4, [
            MP("A normal value that should be accepted", ["normal", "typical", "45", "50", "72", "in the middle"]),
            MP("A boundary value at the edge of what is allowed", ["boundary", "0", "100", "1", "99", "edge", "limit"]),
            MP("An erroneous value that should be rejected", ["erroneous", "hello", "abc", "letters", "text", "-5", "negative", "150", "101"]),
            MP("Boundary data is where mistakes hide, because it tests the exact limits of the condition", ["edge", "mistakes hide", "greater than", "off by one", "limits", "where errors", "wrong side", "exactly"]),
        ], "Normal test data would be 45, a typical mark that should simply be accepted. Boundary test data would be 0 and 100, the two values right at the edge of what is allowed, and 101 just outside it. Erroneous test data would be hello, which is not a number at all and should be politely rejected rather than crashing the program. Boundary data is the most useful because that is exactly where programming mistakes hide. A condition written as greater than 0 rather than greater than or equal to 0 works perfectly for 45 and fails only at the edge, so testing in the middle of the range would never find it.", "Give"),

        EQ("A student is about to post a set of holiday photographs on a public account. Explain why they should think carefully before doing this.", 5, [
            MP("The posts add to a permanent active digital footprint", ["digital footprint", "permanent", "forever", "stays online", "trail", "record"]),
            MP("Other people can screenshot or copy them, so deleting later does not remove them", ["screenshot", "copies", "cannot delete", "others save", "deleting does not", "still out there"]),
            MP("Universities and employers do look at public accounts", ["employer", "university", "job", "college", "future", "look you up"]),
            MP("Photographs can give away personal information such as location or that the house is empty", ["location", "where you live", "address", "tagged", "empty house", "away from home", "school uniform"]),
            MP("Suggests a sensible action, such as checking privacy settings or turning off location tagging", ["privacy settings", "private account", "who can see", "think before", "turn off location", "ask first"]),
        ], "Everything posted on a public account becomes part of a permanent active digital footprint. Even if the photographs are deleted later, anyone who has seen them can screenshot or download them first, so deleting the original does not delete the copies. That matters because universities and employers do look at public social media, and something posted at thirteen can still be found years later. The photographs themselves also give away more than the student intends: location tags show exactly where they were, and a set of holiday pictures posted while the family is still away tells everybody that the house is empty. Before posting, they should check the privacy settings so that only people they know can see the pictures, turn off location tagging, wait until they are home, and ask anyone else in the photographs whether they mind appearing.", "Explain"),
    ],
)

# ============================================================ Year 8 Summer

Y8_SUMMER = Paper(
    slug="ks3-year-8-summer",
    title="Year 8 Computing: Summer Assessment",
    course="Key Stage 3",
    board="MskProd",
    code="Year 8 Summer",
    minutes=0,
    marks=0,
    accent="var(--purple)",
    blurb="The whole of Year 8, with most of the marks on Python, spreadsheets, networks and cyber security, and web development.",
    advice="Where a question says write a formula or write code, write it exactly as you would type it. Where a question asks you to compare, you must write about both things, not just one of them.",
    calculator="No calculator is permitted.",
    questions=[
        EQ("Name the network device that joins the computers within one network and sends data only to the device it is meant for.", 1, [
            MP("Switch", ["switch"]),
        ], "A switch. It connects the devices within a single network and, unlike a hub, it sends each piece of data only to the device it is addressed to.", "Name"),

        EQ("State one difference between a for loop and a while loop, and give an example of a situation where a while loop is the better choice.", 2, [
            MP("A for loop repeats a known number of times, a while loop repeats while a condition is true", ["known number", "set number", "condition", "until", "as long as", "fixed number"]),
            MP("Gives a situation where the number of repeats is not known in advance", ["password", "until the input is valid", "until correct", "player quits", "unknown", "validation", "keep asking"]),
        ], "A for loop repeats a known number of times, such as exactly ten times or once for every item in a list, while a while loop keeps repeating for as long as its condition stays true. A while loop is the better choice when you do not know in advance how many repeats are needed, for example when asking the user for a password and continuing to ask until they type the right one.", "State"),

        EQ("A spreadsheet holds test marks in cells B2 to B31. Write a formula that shows the average mark, and write a formula that shows the highest mark.", 2, [
            MP("=AVERAGE(B2:B31)", ["average b2 b31", "=average", "average b2"]),
            MP("=MAX(B2:B31)", ["max b2 b31", "=max", "max b2"]),
        ], "The average is =AVERAGE(B2:B31) and the highest mark is =MAX(B2:B31). Both must start with an equals sign, otherwise the spreadsheet treats what has been typed as ordinary text, and both use a range written as the first cell, a colon, then the last cell.", "Write"),

        EQ("Explain why data sent across a network is split into packets.", 3, [
            MP("The data is broken into small pieces that travel separately", ["small", "separate", "split", "pieces", "chunks"]),
            MP("One large file cannot block the network for everybody else", ["block", "hog", "share", "other users", "fairer", "queue", "at the same time"]),
            MP("If a packet is lost only that packet is resent, and packets can take different routes", ["resent", "resend", "lost", "different routes", "reassembled", "only that packet"]),
        ], "Data is split into packets because sending one enormous file as a single lump would tie up the connection completely and everybody else would have to wait until it had finished. Small packets from different users can be interleaved, so everyone gets a share of the line. Splitting the data also makes the transfer far more reliable, because packets can take different routes to the destination and if one is lost or damaged only that single packet has to be sent again rather than the whole file. Each packet carries the destination address, the sender's address and a packet number so that the receiving computer can put them back in the right order.", "Explain"),

        EQ("Describe what happens between a user typing a web address into a browser and the page appearing on the screen.", 3, [
            MP("The browser asks a DNS server for the IP address that matches the name", ["dns", "ip address", "looks up", "translates", "domain name"]),
            MP("A request is sent to the web server at that IP address", ["request", "web server", "sends", "asks the server"]),
            MP("The server sends the page back in packets, which are reassembled and displayed", ["packets", "reassembled", "sends back", "displayed", "in order", "browser shows"]),
        ], "The browser first asks a DNS server to look up the IP address that matches the name that has been typed, because computers route data by number rather than by name. The DNS server replies with an address such as 93.184.216.34. The browser then sends a request to the web server at that address. The server responds with the page, which is broken into packets that may travel by different routes and arrive out of order. The user's computer reassembles them in the correct order using the packet numbers, and the browser then renders the HTML and CSS into the page you see.", "Describe"),

        EQ("Explain the difference between a relative and an absolute cell reference, and give one situation where an absolute reference is needed.", 3, [
            MP("A relative reference changes when the formula is copied", ["changes", "updates", "moves", "b2 becomes b3", "adjusts"]),
            MP("An absolute reference uses dollar signs and stays the same when copied", ["dollar", "$", "fixed", "locked", "stays the same", "does not change"]),
            MP("Needed when every row must use the same cell, such as a rate stored once", ["vat", "tax rate", "one cell", "same cell", "discount", "at the top", "exchange rate", "price per"]),
        ], "A relative reference such as B2 changes when the formula is copied, so copying it down one row makes it B3 and copying it right one column makes it C2. That is usually what you want, because a column of totals should refer to a different row each time. An absolute reference such as $B$2 has dollar signs that lock it, so it stays exactly the same wherever the formula is copied. An absolute reference is needed when every row has to refer to the same single cell, for example a VAT rate or a price per ticket stored once at the top of the sheet. Without the dollar signs the reference would slide down the sheet and the later rows would multiply by empty cells.", "Explain"),

        EQ("Explain why every meaningful image on a web page should have alt text.", 3, [
            MP("A screen reader reads the alt text aloud to the user", ["screen reader", "read aloud", "blind", "visually impaired", "cannot see"]),
            MP("It is displayed if the image fails to load", ["does not load", "fails to load", "broken", "missing", "slow connection"]),
            MP("Without it those users lose the information the image carries", ["miss", "cannot tell", "no idea", "excluded", "meaning", "information", "accessible"]),
        ], "Alt text is the description written into the alt attribute of an image tag. Software that reads a page aloud, used by people who are blind or have very limited vision, reads the alt text in place of the picture, so it is the only way those users receive whatever the image is communicating. It also appears on the screen when the image itself fails to load, for example on a very slow connection. Without alt text the image is simply a gap, and any information it carried is lost, which is why alt text is treated as part of building an accessible site rather than as an optional extra.", "Explain"),

        EQ("A student writes a while loop that keeps printing the same number and never stops. Explain what has gone wrong, and how to fix it.", 3, [
            MP("Nothing inside the loop changes the value being tested", ["never changes", "not updated", "nothing changes", "same value", "not increased"]),
            MP("The condition therefore stays true and the loop never ends", ["always true", "never false", "infinite", "never ends", "forever"]),
            MP("Fix it by changing that variable inside the loop, for example count = count + 1", ["count = count + 1", "add one", "increase", "increment", "update the variable", "+ 1"]),
        ], "A while loop keeps running for as long as its condition is true, and the condition is only rechecked at the top of each pass. If nothing inside the loop changes the variable that the condition tests, that condition can never become false, so the loop runs forever and the same value is printed over and over. The fix is to make sure something inside the loop changes the value being tested, such as adding the line count = count + 1 inside the loop so that count eventually reaches the limit and the loop stops.", "Explain"),

        EQ("Write a Python program that asks the user for five numbers, stores them in a list, and then prints the largest number and the average.", 4, [
            MP("Creates a list and uses a loop that repeats five times", ["list", "range 5", "loop", "five times", "for"]),
            MP("Converts each input to a number and appends it to the list", ["int", "input", "append", "add to the list", "convert"]),
            MP("Uses max to find the largest value", ["max", "largest", "maximum"]),
            MP("Uses sum divided by len for the average and prints both results", ["sum", "len", "average", "divide", "print"]),
        ], "numbers = [] to start with an empty list. Then for i in range(5): numbers.append(int(input('Enter a number: '))). The int is needed because input hands back text. Then print('The largest is', max(numbers)) and print('The average is', sum(numbers) / len(numbers)). Using len rather than typing 5 means the program still works if the number of values is changed later.", "Write"),

        EQ("Write the HTML needed for a page section with a level one heading saying Bike Club, a paragraph of text, and an image of a bicycle with suitable alt text.", 4, [
            MP("Correct h1 element containing the words Bike Club", ["h1>bike club</h1>", "h1", "heading"]),
            MP("Paragraph opened and closed with p tags", ["<p>", "</p>", "paragraph"]),
            MP("An img element with a src attribute naming the file", ["<img", "src=", "src", "image tag"]),
            MP("An alt attribute that actually describes the picture", ["alt=", "alt text", "describing", "description"]),
        ], "The HTML is <h1>Bike Club</h1>, then <p>We meet every Thursday after school and ride together for an hour.</p>, then <img src='bike.jpg' alt='A blue mountain bike leaning against a gate'>. The h1 element marks the most important heading on the page, the p element wraps the paragraph and must be closed, and the img element is self closing and needs a src attribute giving the file name plus an alt attribute describing what the picture shows.", "Write"),

        EQ("Describe two measures a school could take to reduce the risk of ransomware, and explain how each one helps.", 4, [
            MP("Keep regular backups of important data, stored separately", ["backup", "copies", "separate copy", "offline"]),
            MP("Files can then be restored without paying the criminals", ["restore", "without paying", "recover", "not pay", "copy back"]),
            MP("Use anti malware software and install software updates", ["anti malware", "antivirus", "updates", "patch", "scan"]),
            MP("These detect and remove known threats and close the weaknesses malware uses", ["detects", "removes", "known", "closes", "vulnerabilities", "holes", "blocks", "prevents"]),
        ], "The first measure is to keep regular backups of everything important, held separately from the main network so that the ransomware cannot encrypt them as well. If an attack succeeds, the school can wipe the affected machines and restore the files from the backup, which removes the entire point of the attack because there is no reason to pay for a key to data you already have. The second measure is to run anti malware software and to install operating system and application updates promptly. Anti malware scans files against known threats and removes them before they run, and updates close the security weaknesses that ransomware relies on to get in, since most successful attacks use flaws that were fixed months earlier.", "Describe"),

        EQ("Explain two reasons why a programmer would split a long program into functions.", 4, [
            MP("Code written once can be called many times", ["reuse", "use it again", "many times", "call it", "written once"]),
            MP("The program is shorter and there is less repeated code", ["shorter", "less code", "repetition", "duplicate", "not repeat"]),
            MP("A fault only has to be corrected in one place", ["one place", "fix once", "easier to fix", "single place", "one line"]),
            MP("Each function can be tested on its own and the program is easier to read", ["tested", "test each", "easier to read", "easier to understand", "clearer", "on its own"]),
        ], "The first reason is reuse. A calculation that is needed in six different places is written once as a function and then called six times, which makes the program considerably shorter and removes the repeated code. That also means a mistake in that calculation only has to be corrected in one place rather than hunted down in six, which is where most bugs in long programs come from. The second reason is that the program becomes far easier to read and to test. Each function has one clear job and a name that says what it does, so the main part of the program reads almost like English, and each function can be tested on its own before it is trusted in the finished program.", "Explain"),

        EQ("A school is connecting the computers in a new classroom. Compare wired and wireless connections, and recommend which the school should use.", 5, [
            MP("Wired connections are faster and more consistent", ["faster", "quicker", "consistent", "higher speed", "steady"]),
            MP("Wired connections are more reliable, as the signal is not weakened by distance or walls", ["reliable", "interference", "walls", "distance", "signal", "drop out"]),
            MP("Wired connections are more secure, since physical access is needed", ["secure", "physical access", "plug in", "through the air", "intercept"]),
            MP("Wireless is cheaper and quicker to install and lets devices move around", ["cheaper", "no cables", "install", "move", "tablets", "laptops", "convenient"]),
            MP("Gives a clear recommendation and justifies it for this situation", ["recommend", "should use", "therefore", "conclusion", "best", "wired because", "wireless because"]),
        ], "A wired connection is faster and far more consistent, because the data travels along a cable that nothing else is sharing, and it is more reliable since the signal is not weakened by distance, walls or interference from other equipment. It is also more secure, because an attacker would have to get into the room and physically plug in rather than simply being close enough to pick up a signal travelling through the air. Wireless has real advantages too. It is much cheaper and quicker to install because no cables have to be run through walls and floors, and it lets tablets and laptops be moved around the room or taken to another part of the school. For a room of fixed desktop computers that never move, the school should use wired connections, because speed, reliability and security matter more than mobility and the machines are staying where they are. A wireless access point should be added as well, so that visiting laptops and tablets can still connect.", "Compare"),
    ],
)


# ============================================================ Year 9 Autumn

Y9_AUTUMN = Paper(
    slug="ks3-year-9-autumn",
    title="Year 9 Computing: Autumn Assessment",
    course="Key Stage 3",
    board="MskProd",
    code="Year 9 Autumn",
    minutes=0,
    marks=0,
    accent="var(--lilac-deep)",
    blurb="Covers the law and your data, binary and hexadecimal, binary addition, units of storage, and how text, images and sound are represented. This is the first assessment that looks and feels like a GCSE paper.",
    advice="Read the command word before you start writing. State needs a fact. Describe needs a fact plus a detail. Explain needs a reason, usually a sentence containing the word because. Show your working in every conversion, because method marks are available even when the final answer is wrong.",
    calculator="No calculator is permitted.",
    questions=[
        EQ("State what is meant by personal data.", 1, [
            MP("Information that can be used to identify a living person", ["identify", "identifiable", "about a person", "who someone is", "living individual"]),
        ], "Personal data is any information that can be used to identify a living person, such as a name together with an address, a date of birth, a photograph or an email address.", "State"),

        EQ("The Data Protection Act gives you the right to see the data an organisation holds about you. State two other rights it gives you.", 2, [
            MP("The right to have inaccurate data corrected", ["corrected", "rectified", "put right", "fixed", "accurate"]),
            MP("The right to have your data deleted, or to object to how it is used", ["deleted", "erased", "removed", "forgotten", "object", "withdraw consent", "stop them using"]),
        ], "You have the right to have data corrected if it is wrong, and the right to have your data deleted when there is no longer a good reason for the organisation to keep it. You can also object to your data being used for particular purposes, such as marketing.", "State"),

        EQ("Convert the denary number 173 into 8 bit binary. Show your working.", 2, [
            MP("Shows a correct method, for example place values or repeated division", ["128", "place value", "64 32 16", "divide", "remainder", "subtract"]),
            MP("Gives the answer 10101101", ["10101101"]),
        ], "Writing the place values 128, 64, 32, 16, 8, 4, 2, 1 above the columns: 128 fits into 173 leaving 45, 64 does not fit, 32 fits leaving 13, 16 does not fit, 8 fits leaving 5, 4 fits leaving 1, 2 does not fit and 1 fits leaving 0. Reading the columns gives 10101101.", "Convert"),

        EQ("Convert the binary number 11010110 into hexadecimal. Show your working.", 2, [
            MP("Splits the binary into two groups of four bits, 1101 and 0110", ["1101", "0110", "groups of four", "nibbles", "split"]),
            MP("Gives the answer D6", ["D6", "d6"]),
        ], "Split the eight bits into two groups of four, giving 1101 and 0110. The group 1101 is 8 + 4 + 1, which is 13, and 13 is written as D in hexadecimal. The group 0110 is 4 + 2, which is 6. So the answer is D6.", "Convert"),

        EQ("Add the binary numbers 01101100 and 00110101. Give your answer in binary.", 3, [
            MP("Shows column addition with carries", ["carry", "column", "working", "1 + 1"]),
            MP("Gives the answer 10100001", ["10100001"]),
            MP("Answer is exactly 8 bits with no overflow", ["8 bits", "eight bits", "no overflow", "fits"]),
        ], "Adding from the right: 0 plus 1 is 1, 0 plus 0 is 0, 1 plus 1 is 0 carry 1, 1 plus 0 plus the carry is 0 carry 1, 0 plus 1 plus the carry is 0 carry 1, 1 plus 1 plus the carry is 1 carry 1, 1 plus 0 plus the carry is 0 carry 1, and 0 plus 0 plus the carry is 1. The answer is 10100001, which is 161 in denary, and 108 plus 53 does equal 161. It fits into eight bits, so there is no overflow.", "Add"),

        EQ("Explain what is meant by overflow in binary addition.", 2, [
            MP("The result of the addition needs more bits than are available", ["too big", "more bits", "does not fit", "exceeds", "beyond"]),
            MP("A carry comes out of the leftmost column and is lost, so the stored answer is wrong", ["carry", "leftmost", "lost", "wrong answer", "incorrect", "ninth bit"]),
        ], "Overflow happens when the answer to an addition is too large to fit into the number of bits available. A carry is produced out of the leftmost column, but with only eight bits there is no ninth bit to hold it, so the carry is lost and the value that gets stored is not the correct answer.", "Explain"),

        EQ("A photograph is 800 pixels wide and 600 pixels high and uses a colour depth of 8 bits. Calculate the file size in kilobytes. Show your working.", 3, [
            MP("Multiplies width by height by colour depth", ["800 x 600", "480000", "x 8", "width x height"]),
            MP("Converts bits to bytes by dividing by 8", ["divide by 8", "/ 8", "bytes", "480000 bytes"]),
            MP("Gives 480 KB", ["480", "480 kb", "480 kilobytes"]),
        ], "The number of pixels is 800 multiplied by 600, which is 480000. Each pixel needs 8 bits, so the image data is 480000 multiplied by 8, which is 3840000 bits. Dividing by 8 gives 480000 bytes, and dividing by 1000 gives 480 kilobytes.", "Calculate"),

        EQ("Explain why increasing the colour depth of an image increases its file size.", 3, [
            MP("Colour depth is the number of bits used to store each pixel", ["bits per pixel", "each pixel", "number of bits"]),
            MP("Every pixel in the image needs those extra bits, not just some of them", ["every pixel", "all pixels", "each one", "whole image"]),
            MP("So the total number of bits, and therefore the file size, goes up", ["total bits", "file size", "larger", "bigger", "more storage"]),
        ], "Colour depth is the number of bits stored for each individual pixel, so it decides how many different colours a pixel can be. Increasing the colour depth adds bits to every single pixel in the image, not just to a few of them, so an image with a million pixels gains a million extra bits for each extra bit of colour depth. The total number of bits is width times height times colour depth, so raising the colour depth raises the file size in direct proportion.", "Explain"),

        EQ("Describe how a computer stores the character 'K' using a character set.", 3, [
            MP("A character set gives every character a unique binary code", ["character set", "unique", "code", "number for each", "ascii"]),
            MP("The computer stores the binary code, not the shape of the letter", ["stores the code", "binary", "not the shape", "number", "just a number"]),
            MP("Software uses the same character set to turn the code back into the letter when displaying it", ["same character set", "converts back", "displays", "looks up", "decodes"]),
        ], "A character set such as ASCII gives every character a unique number, and K is 75. The computer converts that number into binary, 01001011, and stores those eight bits. The shape of the letter is never stored: only the code is. When the character needs to be shown on screen, software looks the code up in the same character set and draws the matching symbol, which is why both machines have to agree on the character set for text to appear correctly.", "Describe"),

        EQ("Explain why hexadecimal is used instead of binary when programmers write down memory addresses.", 3, [
            MP("One hexadecimal digit represents exactly four bits", ["four bits", "one digit four", "nibble", "16 is 2 to the 4"]),
            MP("So a value is written in a quarter of the characters", ["shorter", "quarter", "fewer digits", "briefer", "compact"]),
            MP("Shorter values are easier to read and less likely to be mistyped or misread", ["easier to read", "fewer errors", "mistakes", "misread", "mistype", "remember"]),
        ], "Sixteen is two to the power of four, so one hexadecimal digit stands for exactly four bits and a whole byte becomes just two hexadecimal digits. A memory address written as eight ones and zeros is easy to lose your place in, and a single misread digit gives a completely different address. Written in hexadecimal the same value takes a quarter of the characters, so it is far quicker to read aloud, write down and compare, and far harder to get wrong.", "Explain"),

        EQ("A sound file is recorded at a sample rate of 44100 Hz with a bit depth of 16, in mono, for 30 seconds. Calculate the file size in megabytes. Show your working.", 4, [
            MP("Multiplies sample rate by bit depth", ["44100 x 16", "705600"]),
            MP("Multiplies by the number of seconds", ["x 30", "30 seconds", "21168000"]),
            MP("Divides by 8 to get bytes", ["divide by 8", "/ 8", "2646000"]),
            MP("Gives approximately 2.6 MB", ["2.6", "2646", "2.65", "2.646"]),
        ], "The formula is sample rate times bit depth times seconds times channels. That gives 44100 times 16 times 30 times 1, which is 21168000 bits. Dividing by 8 gives 2646000 bytes, dividing by 1000 gives 2646 kilobytes, and dividing by 1000 again gives approximately 2.6 megabytes.", "Calculate"),

        EQ("Describe two effects of increasing the sample rate when recording sound.", 4, [
            MP("More samples are taken every second", ["more samples", "measured more often", "higher rate", "more measurements"]),
            MP("The digital recording is a closer match to the original analogue sound", ["closer", "more accurate", "better quality", "more like the original", "truer"]),
            MP("The file size increases", ["bigger", "larger", "more storage", "file size goes up"]),
            MP("More processing power or bandwidth is needed to play or send it", ["processing", "bandwidth", "slower", "more work", "streaming"]),
        ], "Increasing the sample rate means the height of the wave is measured more often, so the steps of the digital version are narrower and the recording follows the shape of the original analogue wave far more closely, which improves the sound quality. The cost is size. Every extra sample is another set of bits to store, so the file grows in direct proportion to the sample rate, and a larger file takes longer to send over a network and needs more processing to play back.", "Describe"),

        EQ("A student says that all files should be stored in the highest possible quality. Discuss whether this is a good idea, giving reasons for and against.", 6, [
            MP("Higher quality means more detail is kept, which matters for editing and for professional use", ["more detail", "quality", "editing", "professional", "better"]),
            MP("Higher quality files are much larger", ["larger", "bigger", "more storage", "file size"]),
            MP("Large files fill storage quickly and cost more to store", ["fills storage", "runs out", "cost", "expensive", "space"]),
            MP("Large files take longer to send, upload or stream, especially on a slow connection", ["slower", "longer to send", "upload", "stream", "bandwidth", "buffering"]),
            MP("Most uses do not need the extra quality, as people cannot tell the difference on a phone screen or through earphones", ["cannot tell", "no difference", "not needed", "small screen", "earphones", "waste"]),
            MP("Reaches a reasoned conclusion, for example match the quality to the purpose", ["depends", "purpose", "match", "conclusion", "therefore", "should"]),
        ], "There is a real argument for high quality. Keeping more detail matters when a file is going to be edited, printed large or used professionally, because quality lost at the point of capture can never be recovered afterwards. Against that, quality costs size, and the cost is not small: doubling the sample rate or the colour depth roughly doubles the file. Large files fill storage quickly, which either means paying for more or deleting things, and they take much longer to upload, download or stream, which is a serious problem on a slow or metered connection. There is also the question of whether anybody notices. On a phone screen or through cheap earphones, most people genuinely cannot tell a very high quality file from a moderate one, so the extra bits buy nothing. The sensible conclusion is to match the quality to the purpose: capture and archive at high quality when the file will be edited or printed, and store or share a smaller version for everyday use.", "Discuss"),
    ],
)


# ============================================================ Year 9 Summer

Y9_SUMMER = Paper(
    slug="ks3-year-9-summer",
    title="Year 9 Computing: Summer Assessment",
    course="Key Stage 3",
    board="MskProd",
    code="Year 9 Summer",
    minutes=0,
    marks=0,
    accent="var(--lilac-deep)",
    blurb="The last assessment before GCSE. It covers the whole of Year 9: data representation, Python programming, app design, artificial intelligence and 3D modelling, and it is written in GCSE style throughout.",
    advice="This paper is deliberately set at the level you will meet in Year 10. Answer in full sentences, use the correct technical vocabulary, and make one clear point for each mark available. If a question asks you to justify or evaluate, you must reach a conclusion and say why.",
    calculator="No calculator is permitted.",
    questions=[
        EQ("State what is meant by an algorithm.", 1, [
            MP("A sequence of steps followed to complete a task or solve a problem", ["sequence of steps", "set of steps", "instructions", "series of steps", "method"]),
        ], "An algorithm is a sequence of steps that can be followed in order to complete a task or solve a problem.", "State"),

        EQ("A program contains the line total = total + price. Explain what this line does.", 2, [
            MP("The expression on the right is worked out first", ["right first", "works out", "evaluated", "calculates"]),
            MP("The result is then stored back into the variable total, replacing its old value", ["stored", "assigned", "replaces", "back into total", "new value"]),
        ], "The computer first works out the value on the right hand side, adding the current contents of total to the current contents of price. That result is then assigned to the variable total, replacing whatever total held before. The equals sign here means assignment, not equality.", "Explain"),

        EQ("Describe the difference between a for loop and a while loop, and give one situation where each is the better choice.", 4, [
            MP("A for loop repeats a known, fixed number of times", ["known number", "fixed", "set number", "count controlled", "how many times"]),
            MP("A while loop repeats until a condition stops being true, and may run any number of times", ["condition", "until", "unknown number", "condition controlled", "as long as"]),
            MP("Gives a sensible use for a for loop, such as working through every item in a list", ["every item", "list", "ten times", "each of", "known length"]),
            MP("Gives a sensible use for a while loop, such as asking for input until it is valid", ["until valid", "input", "password", "keeps asking", "not known"]),
        ], "A for loop repeats a set number of times that is known before the loop starts, so it is count controlled. A while loop keeps repeating for as long as a condition is true, and nothing decides in advance how many times that will be, so it is condition controlled. A for loop is the right choice for working through every item in a list of forty names, because the number of repeats is known. A while loop is the right choice for asking a user to enter a password until they get it right, because you cannot know in advance how many attempts they will need.", "Describe"),

        EQ("A program uses a list called scores. Explain why a list is a better choice than creating a separate variable for each score.", 3, [
            MP("A list holds many values under one identifier", ["one name", "one identifier", "many values", "single variable", "together"]),
            MP("A loop can work through every item, so the code is much shorter", ["loop", "shorter", "iterate", "each item", "less code"]),
            MP("The number of items can change without rewriting the program", ["any number", "change", "grow", "flexible", "not fixed"]),
        ], "A list stores many values under a single identifier and gives each one an index, so a program can hold thirty scores in one place instead of thirty separately named variables. That means a loop can work through every score with two or three lines of code, where separate variables would need thirty lines that all say almost the same thing. It also means the program still works when the number of scores changes, because nothing in the code depends on there being exactly thirty of them.", "Explain"),

        EQ("Describe two things a designer should do before writing any code for a new app.", 4, [
            MP("Identify who the users are and what they need the app to do", ["users", "audience", "requirements", "what they need", "purpose"]),
            MP("Break the problem down into smaller parts, or write the algorithm out first", ["decompose", "break down", "smaller parts", "algorithm", "plan", "flowchart"]),
            MP("Sketch the interface, for example as wireframes or a storyboard", ["wireframe", "sketch", "storyboard", "layout", "design the screens", "mock up"]),
            MP("Decide how the app will be tested and what success would look like", ["testing", "test plan", "success criteria", "how to check", "evaluate"]),
        ], "First, work out who is going to use the app and what they actually need it to do, and write those needs down as success criteria, because everything afterwards is judged against them. Second, sketch the interface before coding it, as wireframes or a storyboard showing each screen and how the user moves between them. Sketching is fast and changing a sketch costs nothing, whereas changing a built screen costs hours. Planning the algorithm and the test plan at this stage matters for the same reason: mistakes found on paper are cheap and mistakes found in code are not.", "Describe"),

        EQ("Explain what is meant by machine learning.", 3, [
            MP("A system is trained on data rather than being given explicit rules", ["trained", "training data", "examples", "not programmed with rules", "learns from data"]),
            MP("It finds patterns in the data", ["patterns", "relationships", "spots", "identifies"]),
            MP("It uses those patterns to make predictions or decisions about new, unseen data", ["predict", "new data", "unseen", "decisions", "classify"]),
        ], "Machine learning is an approach in which a system is trained on a large quantity of example data rather than being given a set of rules written by a programmer. During training it finds statistical patterns in that data, and it then applies those patterns to make predictions or decisions about new data it has never seen before. Nobody writes a rule saying what a cat looks like: the system is shown many labelled pictures and works out the pattern itself.", "Explain"),

        EQ("An artificial intelligence system used to shortlist job applicants was found to favour male candidates. Explain how this could have happened.", 4, [
            MP("The system was trained on historic data from the organisation", ["training data", "historic", "past", "previous hires", "old data"]),
            MP("That data reflected past decisions that were themselves biased", ["biased data", "past bias", "mostly men", "reflected", "unfair decisions"]),
            MP("The system learned the pattern in the data rather than judging fairness", ["learns the pattern", "copies", "repeats", "no understanding", "does not know"]),
            MP("So the bias in the training data is reproduced and applied at scale", ["reproduces", "repeats it", "at scale", "amplifies", "carries on"]),
        ], "A shortlisting system is trained on data about who the organisation has hired and promoted in the past. If most of those people were men, then the pattern in the data is that successful candidates look like the men already there, and that is precisely the pattern the system learns. The system has no concept of fairness and no way of knowing that the historic decisions were themselves biased: it simply finds the statistical relationship in what it was shown and applies it. The result is that a bias which used to be one interviewer's is now applied consistently to every single application, which makes it both harder to spot and much larger in effect.", "Explain"),

        EQ("Describe the difference between a bitmap image and a vector image.", 3, [
            MP("A bitmap is stored as a grid of pixels, each with its own colour value", ["pixels", "grid", "each pixel", "colour value", "map of bits"]),
            MP("A vector is stored as instructions or coordinates describing shapes", ["instructions", "coordinates", "shapes", "maths", "equations", "objects"]),
            MP("A vector can be scaled without losing quality, a bitmap becomes blocky", ["scale", "resize", "blocky", "pixelated", "no quality loss", "any size"]),
        ], "A bitmap image is stored as a grid of pixels with a colour value recorded for every single pixel, which is why photographs are bitmaps. A vector image is stored instead as a set of instructions describing the shapes it contains, such as the coordinates of a line's endpoints and the thickness and colour to draw it in. Because a vector is redrawn from those instructions at whatever size is needed, it stays perfectly sharp at any scale, while enlarging a bitmap simply makes each pixel bigger and the image looks blocky.", "Describe"),

        EQ("Describe how a 3D model is built from vertices, edges and faces.", 3, [
            MP("A vertex is a single point in 3D space, defined by x, y and z coordinates", ["vertex", "point", "coordinates", "x y z", "position"]),
            MP("An edge is a straight line joining two vertices", ["edge", "line", "joins", "between two", "connects"]),
            MP("A face is a flat surface enclosed by edges, and many faces form the mesh of the model", ["face", "surface", "enclosed", "polygon", "mesh", "makes the shape"]),
        ], "A vertex is a single point in three dimensional space, fixed by its x, y and z coordinates. An edge is a straight line joining two vertices together. A face is a flat surface bounded by three or more edges, usually a triangle. The complete set of faces is called the mesh, and the mesh is what gives the model its shape, which is why a model with more faces can show finer detail but takes longer to render.", "Describe"),

        EQ("Explain why rendering a 3D animation takes so much processing power.", 3, [
            MP("Every frame has to be calculated separately", ["each frame", "every frame", "frame by frame", "many frames"]),
            MP("An animation needs a large number of frames, typically 24 or more each second", ["24", "25", "30", "frames per second", "per second", "thousands of frames"]),
            MP("Each frame requires calculating lighting, shadows, textures and reflections for every visible surface", ["lighting", "shadows", "textures", "reflections", "every surface", "each pixel"]),
        ], "Rendering means calculating the final image from the model, and it has to be done separately for every frame. An animation runs at around 24 to 30 frames every second, so even a two minute sequence is several thousand complete images. Each of those images requires the computer to work out, for every visible surface, how light falls on it, what shadows are cast, how the texture appears at that angle and what is reflected in it. Multiplying that amount of calculation by thousands of frames is why studios render on large farms of machines rather than on one computer.", "Explain"),

        EQ("Evaluate the use of artificial intelligence to mark students' written exam answers.", 6, [
            MP("AI can mark very quickly and at a very large scale", ["fast", "quickly", "scale", "thousands", "instant"]),
            MP("It applies the same standard to every script, so it is consistent", ["consistent", "same standard", "no tiredness", "not subjective", "fair in that sense"]),
            MP("It is cheaper than employing human examiners", ["cheaper", "cost", "less expensive", "saves money"]),
            MP("It may not understand an unusual but correct answer", ["unusual", "creative", "different wording", "valid but", "does not understand", "misses"]),
            MP("Bias in the training data could disadvantage particular groups of students", ["bias", "unfair", "disadvantage", "training data", "certain groups"]),
            MP("Reaches a justified conclusion, for example AI marking with human moderation", ["conclusion", "therefore", "should", "combination", "human check", "moderation", "alongside"]),
        ], "The case for it is strong on practicalities. An automated marker can process thousands of scripts in the time a human takes to mark a handful, it applies exactly the same standard to the first script and the four hundredth, and it does not get tired or distracted, which removes a genuine source of unfairness in human marking. It is also far cheaper, and results could be returned much sooner. The case against rests on what marking actually is. A written answer can be correct in a way the mark scheme did not anticipate, and a system trained to recognise expected phrasing may not credit an unusual but valid response, which penalises exactly the strongest candidates. There is also a risk of bias: if the training data under represents certain groups of students, their writing may be systematically marked lower, and because the same system marks everything, that bias applies at national scale. The most defensible position is not to choose one or the other. Automated marking is reasonable for short, factual responses where the mark scheme is closed, but extended answers should still be marked or at least moderated by humans, with a sample checked every session and a clear route for a student to have a script looked at by a person.", "Evaluate"),
    ],
)


ALL_KS3_PAPERS = [Y7_AUTUMN, Y7_SUMMER, Y8_AUTUMN, Y8_SUMMER, Y9_AUTUMN, Y9_SUMMER]

# Key Stage 3 assessments are not timed to a real board specification, so mark
# totals come from the questions themselves and the time allowance uses one and
# a half minutes per mark, which is the pace these papers were written for.
for _p in ALL_KS3_PAPERS:
    _p.marks = sum(q.marks for q in _p.questions)
    _p.minutes = int(round(_p.marks * 1.5 / 5.0) * 5)
