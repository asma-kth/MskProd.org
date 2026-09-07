"""Original practice examination papers with full mark schemes.

Real past papers are the copyright of the exam boards and cannot be republished,
so every paper here is written from scratch to match the structure, question
style, command words and mark allocation of the real assessments. Links to the
official past papers on each board's own site are given alongside them.
"""
from dataclasses import dataclass, field
from typing import List

from mskbuild import render
from mskbuild.models import EQ, MP
from mskbuild.render import layout, crumbs, crumbs_ld, ico, esc, write, SITE_URL


@dataclass
class Paper:
    slug: str
    title: str
    course: str
    board: str
    code: str
    minutes: int
    marks: int
    blurb: str
    advice: str
    questions: List[EQ]
    calculator: str = "No calculator is permitted."
    accent: str = "var(--teal)"


OFFICIAL = [
    ("OCR GCSE Computer Science J277 past papers",
     "https://www.ocr.org.uk/qualifications/gcse/computer-science-j277-from-2020/assessment/"),
    ("OCR A Level Computer Science H446 past papers",
     "https://www.ocr.org.uk/qualifications/as-and-a-level/computer-science-h046-h446-from-2015/assessment/"),
    ("OCR Cambridge National Creative iMedia J834 assessment materials",
     "https://www.ocr.org.uk/qualifications/cambridge-nationals/creative-imedia-level-1-2-j834/assessment/"),
]

# ==================================================== J277/01 Computer Systems

J277_P1 = Paper(
    slug="j277-paper-1-a",
    title="GCSE Computer Science Paper 1: Computer Systems",
    course="GCSE Computer Science",
    board="OCR",
    code="J277/01 style",
    minutes=90,
    marks=80,
    accent="var(--teal)",
    blurb="A full length original paper covering systems architecture, memory and storage, networks, network security, systems software and the impacts of technology.",
    advice="Answer every question. The number of marks tells you how many creditworthy points the examiner wants, so a four mark question needs four separate developed points. Show all working in calculations and state the unit.",
    questions=[
        EQ("State what is meant by the term embedded system and give one example.", 2, [
            MP("A computer built into a larger device to perform one dedicated task", ["built into", "dedicated", "one task", "specific task", "part of a device"]),
            MP("Gives a valid example", ["washing machine", "microwave", "traffic light", "thermostat", "pacemaker", "camera", "dishwasher"]),
        ], "An embedded system is a computer built into a larger device in order to carry out one specific dedicated task rather than a range of different tasks. An example is the controller inside a washing machine, which manages the wash cycle and does nothing else."),

        EQ("Describe the purpose of the Program Counter and the Accumulator within the CPU.", 4, [
            MP("The Program Counter holds the address of the next instruction to be fetched", ["program counter", "address", "next instruction"]),
            MP("It is incremented during the fetch stage so it points at the following instruction", ["incremented", "increased", "points at", "next"]),
            MP("The Accumulator holds the result of calculations performed by the ALU", ["accumulator", "result", "alu", "calculation"]),
            MP("That result can then be used again or written back to memory", ["used again", "written back", "stored", "memory", "further"]),
        ], "The Program Counter holds the memory address of the next instruction that is to be fetched, and during the fetch stage its value is copied into the Memory Address Register and the Program Counter is then incremented so that it already points at the following instruction. The Accumulator holds the result of any calculation carried out by the Arithmetic Logic Unit, so that the value is immediately available to be used in a further operation or written back to main memory."),

        EQ("A computer has 4 GB of RAM. Explain what happens when the user opens more applications than the RAM can hold, and describe the effect on performance.", 6, [
            MP("RAM becomes full so there is no space for the new application", ["full", "no space", "runs out", "insufficient"]),
            MP("The operating system uses virtual memory, an area of secondary storage", ["virtual memory", "secondary storage", "hard disk", "swap file", "page file"]),
            MP("Data not recently used is moved out of RAM to that area", ["moved out", "transferred", "swapped out", "least recently used", "not being used"]),
            MP("It is swapped back into RAM when it is needed again", ["swapped back", "moved back", "returned", "read back"]),
            MP("Secondary storage is far slower to access than RAM", ["slower", "much slower", "not as fast"]),
            MP("The processor spends time waiting, which the user experiences as slowdown, and heavy swapping is called disk thrashing", ["waiting", "slowdown", "slow", "thrashing", "idle", "less work"]),
        ], "When RAM becomes full there is no physical memory available for the new application, so the operating system falls back on virtual memory, which is an area of secondary storage set aside for the purpose and known as the swap file or page file. The operating system identifies data belonging to applications that have not been used recently and writes it out to that area, freeing physical RAM for the program being opened. If the user then returns to one of those applications, the data has to be read back into RAM, which usually means writing something else out to make room. Because secondary storage is thousands of times slower to access than RAM, every one of these transfers takes a substantial amount of time during which the processor has nothing useful to do, and the user experiences the machine becoming increasingly unresponsive. When the shortage is severe enough that the system spends more time moving data than executing instructions, the condition is known as disk thrashing. The most effective solution is to install more RAM so that all the open applications fit in physical memory."),

        EQ("An image is 640 pixels wide and 480 pixels high with a colour depth of 24 bits. Calculate the file size in megabytes. Show your working.", 4, [
            MP("Multiplies colour depth by width by height", ["24 x 640", "640 x 480", "colour depth x width x height"]),
            MP("Obtains 7,372,800 bits", ["7372800", "7,372,800"]),
            MP("Divides by 8 to obtain 921,600 bytes", ["921600", "921,600", "divide by 8"]),
            MP("States approximately 0.92 MB", ["0.92", "921.6", "0.9216"]),
        ], "The file size in bits is colour depth multiplied by width multiplied by height, which is 24 x 640 x 480 = 7,372,800 bits. Dividing by 8 converts this to 921,600 bytes. Dividing by 1000 gives 921.6 kilobytes, and dividing by 1000 again gives approximately 0.92 megabytes."),

        EQ("Explain the difference between lossy and lossless compression, and state which should be used for a spreadsheet of financial records.", 5, [
            MP("Lossy permanently removes some of the data", ["removes", "permanently", "discards", "deletes"]),
            MP("The original cannot be recovered from a lossy file", ["cannot be recovered", "not restored", "irreversible", "gone"]),
            MP("Lossless reduces size without removing any data, by encoding it more efficiently", ["no data", "nothing removed", "efficiently", "repetition", "all data kept"]),
            MP("The original is restored exactly when a lossless file is decompressed", ["exactly", "perfectly", "restored", "identical"]),
            MP("Lossless must be used for the spreadsheet because losing any figure would corrupt the records", ["lossless", "figures", "corrupt", "values", "accurate", "every"]),
        ], "Lossy compression reduces file size by permanently discarding data that is judged least noticeable, such as very high frequencies in audio or subtle colour differences in an image, and because that data is deleted the original file can never be recovered from the compressed version. Lossless compression reduces size without discarding anything at all, instead recording the information more efficiently by identifying repetition and encoding it compactly, so decompressing the file restores the original exactly, byte for byte. A spreadsheet of financial records must use lossless compression, because every figure in it is significant and there is no redundant detail that could be discarded without changing the meaning. Applying lossy compression would alter or destroy values, producing records that are inaccurate and worthless."),

        EQ("Describe two differences between a star topology and a mesh topology.", 4, [
            MP("In a star topology every device connects to a central switch", ["central", "switch", "hub", "one point", "all connect to"]),
            MP("In a mesh topology devices connect to many other devices", ["many", "multiple", "each other", "several connections"]),
            MP("A star has a single point of failure at the central switch", ["single point of failure", "switch fails", "whole network fails"]),
            MP("A mesh has no single point of failure because data can be rerouted", ["no single point", "reroute", "alternative", "another path", "redundancy"]),
        ], "In a star topology every device is connected to a single central switch, so all traffic passes through that switch, whereas in a mesh topology each device is connected to several others, creating multiple possible routes between any two points. This produces a significant difference in reliability. A star topology has a single point of failure: if the central switch fails then every device loses connectivity, although a single broken cable affects only the one device attached to it. A mesh topology has no single point of failure, because if one connection is lost the data is simply rerouted along an alternative path and the network continues to function."),

        EQ("Explain how a firewall helps to protect a network.", 3, [
            MP("It inspects traffic entering and leaving the network", ["inspects", "examines", "checks", "incoming", "outgoing", "traffic"]),
            MP("It compares that traffic against a set of rules", ["rules", "criteria", "set of", "policy"]),
            MP("Traffic that does not meet the rules is blocked", ["blocks", "blocked", "prevents", "rejected", "denied"]),
        ], "A firewall sits between a network and the outside world and examines every packet of data attempting to enter or leave. Each packet is compared against a set of rules that specify which addresses, ports and types of traffic are permitted, and anything that does not meet those rules is blocked rather than being passed on. This prevents many attacks from reaching the network at all and also stops malware that is already inside from communicating with external servers."),

        EQ("A company is choosing between a hard disk drive and a solid state drive for laptops used by staff who travel frequently. Recommend one and justify your recommendation.", 6, [
            MP("Recommends a solid state drive", ["solid state", "ssd", "flash"]),
            MP("An SSD has no moving parts", ["no moving parts", "nothing moves", "no platter", "flash memory"]),
            MP("It is therefore far more durable if the laptop is knocked or dropped", ["durable", "dropped", "knocked", "shock", "damage", "travel"]),
            MP("It is faster to read and write, so the laptop boots and loads files more quickly", ["faster", "quicker", "boot", "loads", "access time"]),
            MP("It uses less power, extending battery life away from a mains supply", ["power", "battery", "energy", "longer"]),
            MP("Acknowledges the higher cost per gigabyte as the trade off", ["cost", "expensive", "price", "per gigabyte", "trade off"]),
        ], "The company should choose solid state drives. The decisive factor is durability: staff who travel frequently will carry the laptops in bags, use them on trains and inevitably knock or drop them, and a hard disk drive contains platters spinning at thousands of revolutions per minute with a read write head hovering nanometres above them, which makes it highly vulnerable to physical shock. A solid state drive stores data in flash memory with no moving parts at all, so it is far more likely to survive the same treatment, and the cost of a failed drive is not the hardware but the lost work and the time a member of staff spends unable to do their job. Solid state drives are also significantly faster to read and write, so machines boot and open files more quickly, which matters when someone has fifteen minutes on a train, and they draw less power, which extends battery life away from mains electricity. The clear trade off is cost, since solid state storage is considerably more expensive per gigabyte, but for laptops that leave the office the reliability and battery benefits justify it."),

        EQ("Explain the difference between an IP address and a MAC address.", 4, [
            MP("An IP address identifies a device on a network and is assigned by the network", ["ip", "on a network", "assigned by the network", "identifies"]),
            MP("It can change, for example when the device joins a different network", ["change", "changes", "different network", "not fixed"]),
            MP("A MAC address identifies a specific piece of hardware and is assigned by the manufacturer", ["mac", "hardware", "manufacturer", "network card"]),
            MP("It is fixed and is used for delivery within a local network", ["fixed", "does not change", "local network", "within", "switch"]),
        ], "An IP address identifies a device's position on a network and is assigned by that network, which means it is not permanent and will change when the device connects somewhere else, such as moving from a home network to a school one. It is used to route data between different networks across the internet. A MAC address identifies one specific piece of network hardware, is assigned by the manufacturer when the network interface card is made and does not change. It is used by switches to deliver data to the correct device once it has arrived on the local network. Both are needed: the IP address gets the data to the right network and the MAC address gets it to the right device on that network."),

        EQ("Describe two tasks carried out by an operating system.", 4, [
            MP("Memory management, allocating memory to programs and keeping them separate", ["memory", "allocates", "separate", "ram"]),
            MP("Explains a consequence, such as one program being unable to overwrite another's data", ["overwrite", "crash", "separate", "protects", "isolated"]),
            MP("A second task such as peripheral management using device drivers", ["peripheral", "driver", "input", "output", "hardware", "user management", "file management"]),
            MP("Explains what that task involves", ["translates", "commands", "organises", "accounts", "permissions", "folders", "communicates"]),
        ], "One task is memory management. The operating system decides which programs and data are held in RAM and where, allocating memory to each program as it opens, keeping the areas belonging to different programs separate so that one cannot overwrite another's data and cause it to crash, and freeing that memory when the program closes. A second task is peripheral management. The operating system communicates with input and output devices through device drivers, which translate its generic instructions into the specific commands that a particular printer, scanner or graphics card understands, which is why the same operating system can support thousands of different devices."),

        EQ("A school is considering replacing its desktop computers every two years rather than every five years. Discuss the impacts of this decision.", 8, [
            MP("Identifies an environmental impact such as increased e-waste", ["e-waste", "waste", "environmental", "disposal", "landfill"]),
            MP("Explains the harm, such as toxic materials or resources used in manufacturing", ["toxic", "lead", "mercury", "rare earth", "mining", "resources", "manufacturing"]),
            MP("Identifies an economic impact, since replacing more often costs the school more", ["cost", "expensive", "budget", "money", "spend"]),
            MP("Notes what the money could otherwise be spent on", ["instead", "other", "teachers", "resources", "elsewhere"]),
            MP("Identifies a benefit such as better performance and support for current software", ["faster", "performance", "modern software", "up to date", "supported"]),
            MP("Identifies a security benefit, since older machines may no longer receive updates", ["security", "updates", "unsupported", "patches", "vulnerable"]),
            MP("Presents both sides rather than only one", ["however", "on the other hand", "although", "but", "against this"]),
            MP("Reaches a supported conclusion", ["conclusion", "overall", "therefore", "recommend", "should"]),
        ], "Replacing computers every two years has significant environmental costs. Each replacement cycle sends the previous machines into the waste stream, and electronic equipment contains toxic substances including lead, mercury and cadmium, much of which is exported to countries with weaker environmental regulation where informal recycling exposes workers and contaminates land and water. Manufacturing the replacements is equally damaging, since it consumes rare earth metals extracted by mining that destroys habitats, and doubling the replacement rate doubles that impact. There is also a clear financial cost. A school budget is fixed, so spending more than twice as often on hardware means spending less on something else, whether that is teaching staff, textbooks or building maintenance, and computers replaced after two years are typically still perfectly capable of running the software a school actually uses. Against this there are real benefits. Newer machines are faster and will run current software that older hardware may struggle with, which matters in subjects such as computing and design where students need to use professional tools. More importantly, manufacturers and operating system vendors eventually stop issuing security updates for older hardware, and a school network full of unsupported machines holding student data is a genuine security risk rather than a theoretical one. Newer machines are also generally more energy efficient, which partially offsets the manufacturing cost over their lifetime. On balance the school should not move to a two year cycle. A four or five year cycle keeps machines within their supported lifetime while producing far less waste and freeing budget for other purposes, and a better approach would be to replace machines when they genuinely become inadequate or unsupported rather than on a fixed schedule, and to ensure that retired machines are refurbished and donated or properly recycled rather than discarded."),

        EQ("Explain what is meant by a brute force attack and describe one method of preventing it.", 4, [
            MP("Every possible combination of characters is tried until the password is found", ["every possible", "all combinations", "tries", "guesses", "systematically"]),
            MP("This is normally automated so millions of attempts can be made", ["automated", "software", "millions", "computer", "rapidly"]),
            MP("Prevention: limit the number of login attempts allowed", ["limit", "attempts", "lock", "three attempts", "lockout"]),
            MP("Or use long complex passwords, or two factor authentication", ["long", "complex", "strong password", "two factor", "2fa"]),
        ], "A brute force attack works by systematically trying every possible combination of characters until the correct password is found. It is carried out automatically by software capable of making millions of attempts per second, which is why short or simple passwords fall very quickly. The most effective prevention is to limit the number of failed login attempts allowed, locking the account or imposing a delay after a small number of failures, because this makes an attack requiring millions of attempts completely impractical however fast the attacker's computer is. This should be combined with requiring long passwords, since each additional character multiplies the number of combinations that must be tried, and with two factor authentication, which means that even a correctly guessed password is not sufficient to gain access."),

        EQ("State two pieces of legislation relevant to computing and describe what each one protects.", 4, [
            MP("Data Protection Act 2018 named", ["data protection", "gdpr"]),
            MP("It controls how organisations collect, store and use personal data", ["personal data", "organisations", "collect", "store", "use"]),
            MP("Computer Misuse Act 1990 or Copyright, Designs and Patents Act 1988 named", ["computer misuse", "copyright designs and patents", "copyright act"]),
            MP("Describes what that act protects", ["unauthorised access", "hacking", "intellectual property", "creators", "copying"]),
        ], "The Data Protection Act 2018 controls how organisations collect, store and use personal data. It requires that data is used lawfully and fairly, collected only for a stated purpose, kept accurate and secure, and not retained longer than necessary, and it gives individuals the right to see the data held about them. The Computer Misuse Act 1990 makes it a criminal offence to gain unauthorised access to a computer system or the data on it, to do so with the intention of committing a further offence, and to make unauthorised modifications such as deleting files or spreading malware. It covers hacking even where nothing is changed or taken."),

        EQ("Explain why a computer needs both RAM and ROM.", 4, [
            MP("RAM is volatile so its contents are lost when the power is removed", ["volatile", "lost", "erased", "power off"]),
            MP("At switch on RAM is empty and cannot hold the start up instructions", ["empty", "nothing in it", "at switch on", "cannot hold"]),
            MP("ROM is non volatile so the boot program is still present", ["non volatile", "kept", "retained", "still there", "boot"]),
            MP("ROM alone is insufficient because it is read only and programs must write data", ["read only", "cannot write", "must write", "changes", "not enough"]),
        ], "RAM is volatile, which means everything in it is lost the moment the power is removed, so when a computer is switched on its RAM contains nothing at all and it has no instructions to follow. ROM is non volatile, so the small boot program stored in it survives being powered down and is available immediately at switch on. That program checks the hardware and then loads the operating system from secondary storage into RAM. ROM alone would not be sufficient, because it is read only in normal operation and running programs constantly need to write and change data, which requires the read and write capability that RAM provides. The two are therefore complementary rather than alternatives."),

        EQ("Explain two ways in which a school could reduce the environmental impact of its computer use.", 4, [
            MP("Configure machines to sleep or shut down when not in use", ["sleep", "shut down", "power saving", "switch off", "standby"]),
            MP("This reduces electricity consumption significantly across many machines", ["electricity", "energy", "consumption", "reduces", "many machines"]),
            MP("Extend the life of hardware or refurbish and donate old machines", ["extend", "longer", "refurbish", "donate", "reuse", "recycle"]),
            MP("This reduces e-waste and the resources consumed by manufacturing replacements", ["e-waste", "waste", "manufacturing", "resources", "landfill"]),
        ], "The first way is to configure every machine to enter a low power sleep state after a short period of inactivity and to shut down automatically at the end of the day. A school may have several hundred computers, and each one left running overnight and at weekends consumes electricity continuously for no benefit, so the saving across the whole site is substantial both financially and in terms of carbon emissions. The second way is to keep hardware in use for longer and to dispose of it responsibly when it is finally replaced. Manufacturing a computer consumes rare earth metals extracted through environmentally damaging mining and accounts for a large share of the device's total lifetime environmental impact, so extending a machine's working life from three years to five reduces that impact considerably. When machines are finally retired, refurbishing and donating those that still work, and using a certified recycler for those that do not, keeps toxic materials out of landfill and out of the informal export trade."),

        EQ("Describe what is meant by phishing and explain how a user can identify a phishing message.", 5, [
            MP("A fraudulent message pretending to be from a legitimate organisation", ["fraudulent", "fake", "pretends", "impersonates", "legitimate organisation"]),
            MP("Designed to trick the user into revealing personal information", ["trick", "reveal", "personal information", "password", "bank details"]),
            MP("Warning sign: a sense of urgency such as an account being closed", ["urgency", "urgent", "immediately", "24 hours", "threat", "act now"]),
            MP("Warning sign: a link whose address does not match the real organisation", ["link", "address", "url", "does not match", "spelling"]),
            MP("Warning sign: a generic greeting or a request for a password", ["dear customer", "generic", "greeting", "asks for a password", "no name"]),
        ], "Phishing is a form of social engineering in which an attacker sends a fraudulent message, usually by email or text, that appears to come from a legitimate organisation such as a bank, a delivery company or a school, in order to trick the recipient into revealing personal information such as a password or bank details, or into clicking a link that installs malware. A user can identify a phishing message by several signs. It will typically create a sense of urgency, warning that an account will be closed or a payment has failed unless action is taken immediately, because panic stops people checking carefully. The link in the message will point to an address that does not belong to the real organisation, often with an extra word or a substituted character that is easy to miss. It will frequently use a generic greeting such as Dear Customer rather than the recipient's actual name, and above all it will ask for information that no legitimate organisation ever requests by email, particularly a password. The safest response is never to click the link but to go to the organisation's website by typing the address directly."),

        EQ("Explain how the number of cores affects the performance of a processor.", 4, [
            MP("Each core can fetch, decode and execute instructions independently", ["independently", "each core", "own", "separately"]),
            MP("So several instructions can be processed at the same time", ["same time", "simultaneously", "parallel", "at once"]),
            MP("The software must be written to divide work between cores to benefit", ["written", "multi threaded", "divided", "designed to use", "software"]),
            MP("A single threaded program uses one core and leaves the others idle", ["single threaded", "one core", "idle", "unused"]),
        ], "A core is effectively a complete processing unit with its own arithmetic logic unit, control unit and registers, so each core can fetch, decode and execute instructions independently of the others. This means a quad core processor can genuinely work on four sequences of instructions at the same time rather than switching between them, and for suitable work it completes far more instructions per second than a single core processor at the same clock speed. However the benefit depends entirely on the software. A program has to be written as multiple threads for its work to be divided between cores, and a single threaded program will run on one core while the other three sit idle, gaining nothing at all. Even in multi threaded programs some parts must run sequentially because they depend on earlier results, and coordinating the cores adds overhead, so doubling the cores never quite doubles the performance."),

        EQ("A charity stores personal details of its donors. Explain three things it must do under the Data Protection Act 2018.", 6, [
            MP("Use the data fairly, lawfully and only for the purpose stated", ["fairly", "lawfully", "stated purpose", "specified", "told them"]),
            MP("Collect only data that is adequate and not excessive for that purpose", ["adequate", "not excessive", "only what is needed", "relevant", "minimum"]),
            MP("Keep the data accurate and up to date", ["accurate", "up to date", "correct"]),
            MP("Keep it secure so it cannot be lost or stolen", ["secure", "protected", "encrypted", "not stolen", "safe"]),
            MP("Not keep it for longer than necessary", ["longer than necessary", "delete", "not indefinitely", "retention"]),
            MP("Allow donors to see the data held about them and have errors corrected", ["see", "access", "request", "corrected", "rectify"]),
        ], "First, the charity must process the data fairly and lawfully and use it only for the purpose it stated when the data was collected. If donors gave their details in order to make a donation, the charity cannot then sell those details to another organisation or use them for an unrelated purpose without consent. Second, it must collect only data that is adequate and relevant for that purpose and not excessive, so it should not ask for a donor's date of birth or occupation unless there is a genuine need for it, and it must keep the data accurate and up to date, correcting it when told of a change. Third, it must keep the data secure, protecting it with appropriate measures such as encryption, access controls and backups so that it cannot be lost, stolen or accessed by anyone who should not see it, and it must not retain it for longer than necessary, deleting records when they are no longer needed. Donors also have the right to request a copy of the data held about them and to have inaccuracies corrected, and a serious breach must be reported to the Information Commissioner within seventy two hours."),
    ],
)

# ============================= J277/02 Computational thinking and programming

J277_P2 = Paper(
    slug="j277-paper-2-a",
    title="GCSE Computer Science Paper 2: Computational Thinking, Algorithms and Programming",
    course="GCSE Computer Science",
    board="OCR",
    code="J277/02 style",
    minutes=90,
    marks=80,
    accent="var(--purple)",
    blurb="A full length original paper covering computational thinking, algorithms, searching and sorting, programming fundamentals, robust programs, Boolean logic and IDEs.",
    advice="You may answer programming questions in OCR reference language, Python or another high level language, but be consistent within each answer. Show your trace tables in full, because method marks are awarded for the working.",
    questions=[
        EQ("Define the term algorithm.", 2, [
            MP("A sequence of steps or instructions", ["steps", "instructions", "sequence", "set of"]),
            MP("In a specific order, to solve a problem or complete a task", ["order", "solve a problem", "complete a task", "achieve"]),
        ], "An algorithm is a sequence of unambiguous instructions, arranged in a specific order, which solves a problem or completes a task. It must be complete, so no step is missing, and finite, so that it eventually stops."),

        EQ("Explain what is meant by abstraction and give an example of how it could be used in a program that finds the quickest route between two railway stations.", 4, [
            MP("Abstraction is removing detail that is not relevant to the problem", ["removing", "detail", "not relevant", "unnecessary", "hiding"]),
            MP("Only the information needed to solve the problem is kept", ["kept", "needed", "relevant", "remains", "focus"]),
            MP("Gives examples of removed detail such as scenery or station buildings", ["scenery", "buildings", "colour", "type of train", "weather", "passengers"]),
            MP("Identifies what is retained such as stations, connections and journey times", ["stations", "connections", "journey time", "distance", "links"]),
        ], "Abstraction is the process of removing detail that is not relevant to the problem being solved, so that only the information genuinely needed remains and the problem becomes simpler and quicker to solve. In a program finding the quickest route between two railway stations, details such as what the stations look like, the type of train used on each service, the weather and the number of passengers would all be removed, because none of them affect which sequence of connections is fastest. What would be retained is the set of stations, which stations connect directly to which others, and the journey time for each connection, which turns a complex real network into a simple set of points and weighted links that a routing algorithm can process."),

        EQ("Complete a trace table for the following algorithm and state the final output.\n\ntotal = 0, count = 0, for i = 1 to 6: if i MOD 3 == 0 then total = total + i and count = count + 1, next i, print(total), print(count)", 5, [
            MP("Identifies that the condition is true when i is a multiple of 3", ["multiple of 3", "divisible by 3", "3 and 6", "mod 3"]),
            MP("Shows total becoming 3 when i is 3", ["3", "total = 3"]),
            MP("Shows total becoming 9 when i is 6", ["9", "total = 9"]),
            MP("Shows count reaching 2", ["count = 2", "2"]),
            MP("States the output is 9 then 2", ["9", "2", "outputs"]),
        ], "The loop runs with i taking the values 1 to 6. The condition i MOD 3 equals 0 is true only when i is 3 and when i is 6. When i is 3, total becomes 0 plus 3 which is 3, and count becomes 1. When i is 6, total becomes 3 plus 6 which is 9, and count becomes 2. For all other values of i the condition is false and neither variable changes. The final output is therefore 9 followed by 2."),

        EQ("Describe how a binary search would find the value 23 in the sorted list [4, 8, 15, 16, 23, 42, 50].", 4, [
            MP("The middle item is examined first, which is 16", ["middle", "16", "midpoint"]),
            MP("23 is greater than 16, so the lower half is discarded", ["greater", "larger", "discard", "lower half", "left half"]),
            MP("The middle of the remaining items is examined, which is 42", ["42", "middle of the remaining", "next middle"]),
            MP("23 is less than 42, so the upper half is discarded, leaving 23 which is found", ["less", "smaller", "discard", "upper", "found", "23"]),
        ], "Binary search begins by examining the middle item of the list, which is 16. The target 23 is greater than 16, so it cannot lie in the lower half, and everything from 4 up to and including 16 is discarded, leaving 23, 42 and 50. The middle of that remaining section is 42. The target 23 is less than 42, so the upper half is discarded, leaving only 23. That item is examined, it matches the target, and the search stops after three comparisons rather than the five a linear search would have required."),

        EQ("Show the state of the list [9, 4, 7, 2] after each complete pass of a bubble sort.", 4, [
            MP("After pass 1 the list is [4, 7, 2, 9]", ["4, 7, 2, 9", "4 7 2 9"]),
            MP("After pass 2 the list is [4, 2, 7, 9]", ["4, 2, 7, 9", "4 2 7 9"]),
            MP("After pass 3 the list is [2, 4, 7, 9]", ["2, 4, 7, 9", "2 4 7 9"]),
            MP("A further pass makes no swaps, showing the list is sorted", ["no swaps", "sorted", "final pass", "confirms"]),
        ], "Pass 1: comparing 9 and 4 gives a swap to [4, 9, 7, 2]; comparing 9 and 7 gives a swap to [4, 7, 9, 2]; comparing 9 and 2 gives a swap to [4, 7, 2, 9]. Pass 2: comparing 4 and 7 gives no swap; comparing 7 and 2 gives a swap to [4, 2, 7, 9]; comparing 7 and 9 gives no swap. Pass 3: comparing 4 and 2 gives a swap to [2, 4, 7, 9]; the remaining comparisons give no swaps. A fourth pass makes no swaps at all, which tells the algorithm the list is fully sorted."),

        EQ("Explain one advantage and one disadvantage of a merge sort compared with a bubble sort.", 4, [
            MP("Merge sort is much faster on large lists", ["faster", "quicker", "more efficient", "large lists"]),
            MP("Because it repeatedly halves the problem rather than repeatedly passing through the whole list", ["halves", "divide", "fewer comparisons", "n log n", "passes"]),
            MP("Merge sort uses more memory", ["more memory", "extra memory", "additional space"]),
            MP("Because the sub lists have to be stored during the merging process", ["sub lists", "stored", "copies", "not in place"]),
        ], "The advantage of merge sort is speed on large lists. It uses divide and conquer, repeatedly splitting the list in half until each part contains a single item and then merging the sorted parts back together, which requires far fewer comparisons than bubble sort's repeated passes through the entire list and, importantly, gives consistent performance regardless of how disordered the starting data is. The disadvantage is memory. Merge sort has to create and hold the sub lists it produces while dividing and merging, so it requires additional memory roughly proportional to the size of the list, whereas bubble sort sorts in place using only a single temporary variable and therefore needs almost no extra memory at all."),

        EQ("Write a program that asks the user for 10 numbers, stores them in an array, and then outputs the largest number and the average.", 6, [
            MP("Declares an array or list to hold the values", ["array", "list", "[]", "declare"]),
            MP("Uses a count controlled loop that runs 10 times", ["for", "range(10)", "0 to 9", "1 to 10", "10 times"]),
            MP("Reads input and converts it to a number", ["int(input", "input", "convert"]),
            MP("Stores each value and maintains a running total", ["append", "array[i]", "total", "sum"]),
            MP("Finds the largest by initialising from the first element and comparing", ["largest", "max", "greater than", "numbers[0]", "compare"]),
            MP("Outputs the largest and the average", ["print", "output", "average", "/ 10"]),
        ], "numbers = []\ntotal = 0\n\nfor i in range(10):\n    value = int(input(\"Enter a number: \"))\n    numbers.append(value)\n    total = total + value\n\nlargest = numbers[0]\nfor n in numbers:\n    if n > largest:\n        largest = n\n\nprint(\"Largest:\", largest)\nprint(\"Average:\", total / 10)\n\nThe loop runs exactly ten times, reading each number, converting it from the text that input returns into an integer, storing it in the array and adding it to a running total. The largest is found by initialising the variable to the first element rather than to zero, which matters because the numbers could all be negative, and then comparing each value against it. The average is the total divided by ten."),

        EQ("Explain the difference between a variable and a constant, and give one reason for using a constant.", 3, [
            MP("A variable's value can change while the program runs", ["change", "changes", "can vary", "altered"]),
            MP("A constant's value is fixed once set and cannot be changed", ["fixed", "cannot change", "unchanged", "set once"]),
            MP("A reason such as preventing accidental change or only needing to edit one line", ["accidental", "one place", "single edit", "clarity", "meaningful", "readable"]),
        ], "A variable is a named memory location whose value can be changed at any point while the program is running, such as a score that increases during a game. A constant is given a value once and that value cannot be altered afterwards, such as a VAT rate or the maximum number of players. A constant is used because it prevents the value being changed accidentally elsewhere in the program, and because if the value ever does need updating it appears in only one place so a single line has to be edited rather than every occurrence being found."),

        EQ("A program should accept an age between 11 and 18. Design a test plan containing four tests, giving the test data, its type and the expected result.", 6, [
            MP("Includes normal data within the range", ["normal", "typical", "14", "15", "within"]),
            MP("Includes boundary data at the edge of the accepted range", ["boundary", "11", "18", "edge"]),
            MP("Includes boundary data just outside the accepted range", ["10", "19", "just outside", "boundary"]),
            MP("Includes erroneous data of the wrong type", ["erroneous", "letters", "text", "abc", "blank", "wrong type"]),
            MP("States the type of each piece of data", ["normal", "boundary", "erroneous", "invalid", "type"]),
            MP("States an expected result for every test", ["expected", "accepted", "rejected", "error message"]),
        ], "Test 1 uses the value 14, which is normal data comfortably inside the range, and the expected result is that it is accepted. Test 2 uses the value 11, which is boundary data at the lower edge of the accepted range, and the expected result is that it is accepted because the range is inclusive. Test 3 uses the value 19, which is boundary data just outside the upper edge, and the expected result is that it is rejected with an error message asking the user to try again. Test 4 uses the entry abc, which is erroneous data of the wrong type entirely, and the expected result is that the program rejects it with a clear message rather than crashing when it attempts to convert text into a number. A fifth useful test would be the value 10, checking the lower boundary from outside, since an error at one end of a range does not guarantee an error at the other."),

        EQ("Explain the difference between a syntax error and a logic error, giving an example of each.", 4, [
            MP("A syntax error breaks the rules of the programming language", ["rules", "syntax", "grammar", "invalid"]),
            MP("The program will not run at all until it is corrected", ["will not run", "cannot run", "does not execute"]),
            MP("A logic error means the program runs but produces the wrong result", ["runs", "wrong result", "incorrect", "unexpected"]),
            MP("Gives valid examples such as a missing bracket and a wrong operator", ["missing bracket", "colon", "spelling", "wrong operator", "plus instead", "greater than"]),
        ], "A syntax error is a mistake in the way the code is written, such as a missing colon at the end of an if statement or an unclosed bracket, and because the code breaks the rules of the language the program will not run at all until it is fixed. A logic error is different: the code is perfectly valid and the program runs without complaint, but the instructions do not do what the programmer intended, so the output is wrong. An example is writing total = total minus price when calculating a shopping basket, or using a greater than sign where greater than or equal to was needed, which produces the wrong answer only at the boundary value. Logic errors are more dangerous because nothing alerts the programmer to them and they can only be found by careful testing."),

        EQ("Complete a truth table for Q = (A OR B) AND NOT C, for all eight combinations of inputs.", 5, [
            MP("Lists all eight input combinations", ["eight", "000", "111", "all combinations"]),
            MP("Includes an intermediate column for A OR B", ["a or b", "intermediate"]),
            MP("Includes an intermediate column for NOT C", ["not c", "intermediate"]),
            MP("Q is 0 whenever C is 1", ["c is 1", "0 when c", "not c is 0"]),
            MP("Q is 1 for the combinations 010, 100 and 110", ["010", "100", "110", "three"]),
        ], "There are eight input combinations, counted in binary from 000 to 111. The intermediate column A OR B is 0 only when both A and B are 0, and 1 otherwise. The intermediate column NOT C is 1 whenever C is 0 and 0 whenever C is 1. Q is the AND of those two columns, so Q is 1 only when at least one of A and B is 1 and C is 0. Q is therefore 1 for the input combinations 010, 100 and 110, and 0 for the other five combinations, namely 000, 001, 011, 101 and 111."),

        EQ("Explain two differences between a compiler and an interpreter.", 4, [
            MP("A compiler translates the whole program before it is run", ["whole program", "all at once", "before", "entire"]),
            MP("An interpreter translates and executes one line at a time as the program runs", ["one line", "line by line", "as it runs", "each statement"]),
            MP("A compiler reports all errors together at the end of translation", ["all errors", "together", "at the end", "list"]),
            MP("An interpreter stops at the first error it encounters", ["first error", "stops", "immediately", "halts"]),
        ], "A compiler translates the entire source program into machine code in one operation before it is run, producing an executable file that can then be distributed and run without the compiler or the source. An interpreter translates and executes the program one statement at a time, every time it is run, so both the source code and the interpreter are needed. The second difference is how errors are reported. A compiler attempts to translate the whole program and then presents all the errors it found together, which can be a long list. An interpreter stops as soon as it reaches the first error and reports that one immediately, which makes locating and fixing problems during development considerably easier."),

        EQ("Describe two features of an integrated development environment and explain how each helps a programmer.", 4, [
            MP("An editor with syntax highlighting", ["editor", "syntax highlighting", "colours", "highlighting"]),
            MP("Which makes structure visible and typing errors stand out", ["structure", "visible", "errors stand out", "misspelled", "unclosed"]),
            MP("Error diagnostics identifying the line and type of error", ["error diagnostics", "line number", "type of error", "reports"]),
            MP("Or debugging tools such as breakpoints allowing variables to be inspected", ["breakpoint", "debug", "step", "watch", "inspect"]),
        ], "The first feature is the editor with syntax highlighting, which colours keywords, strings and comments differently. This makes the structure of the code immediately visible and causes typing errors to stand out, since a misspelled keyword loses its colour and an unclosed quotation mark turns the rest of the line into a string. The second feature is error diagnostics combined with debugging tools. Error diagnostics report the line number and the type of any error found, which means the programmer can go straight to the problem instead of searching. Debugging tools such as breakpoints pause the program at a chosen line so the values held in variables can be inspected, and stepping runs one line at a time so the flow can be watched, which is the only reliable way to find logic errors."),

        EQ("Explain why input validation should be used in a program that asks a user for a percentage mark.", 4, [
            MP("Users may enter data of the wrong type or outside a sensible range", ["wrong type", "letters", "negative", "over 100", "invalid"]),
            MP("Without validation the program may crash", ["crash", "error", "stop", "fails"]),
            MP("Or produce incorrect results from meaningless data", ["incorrect", "meaningless", "wrong results", "nonsense"]),
            MP("Validation checks the input is acceptable and allows the user to try again", ["checks", "range check", "type check", "try again", "error message", "rejects"]),
        ], "Input validation is needed because a user may enter something the program cannot sensibly use, whether by accident or deliberately. They might type letters instead of digits, enter a negative mark, enter a value above 100, or leave the field blank. Without validation the program would attempt to use that input directly, and converting text into a number would cause it to crash, while a mark of 500 would produce a meaningless average that the program would report as though it were correct. Validation applies a type check to confirm a whole number was entered and a range check to confirm it lies between 0 and 100 inclusive, rejecting anything that fails with a clear message so the user can correct it, which makes the program robust rather than fragile."),

        EQ("Explain the difference between a function and a procedure, and give one benefit of using subroutines.", 4, [
            MP("A function returns a value to the code that called it", ["returns", "return value", "gives back"]),
            MP("A procedure carries out a task without returning a value", ["does not return", "no value", "just performs"]),
            MP("Benefit: code is written once and can be called many times", ["once", "reuse", "many times", "not repeated"]),
            MP("So a change only has to be made in one place, or each part can be tested separately", ["one place", "easier to maintain", "test", "separately", "debug"]),
        ], "A function is a subroutine that returns a value to the part of the program that called it, so its result can be assigned to a variable or used in a further calculation. A procedure carries out a task, such as displaying a menu, but does not return any value. The main benefit of using subroutines of either kind is that code needed in several places is written once and simply called wherever it is required, so the program is shorter and, more importantly, any correction or change is made in a single place rather than being repeated in every copy. Subroutines also make a program much easier to test, because each one performs a single well defined task that can be checked independently until it is known to work."),

        EQ("Explain how a while loop differs from a for loop and give one situation where each would be the correct choice.", 4, [
            MP("A for loop repeats a known number of times", ["known", "fixed", "set number", "specific"]),
            MP("A while loop repeats while a condition remains true", ["condition", "while", "until", "true"]),
            MP("A situation for a for loop such as processing every item in a list of known length", ["list", "every item", "array", "10 times", "each"]),
            MP("A situation for a while loop such as validating input until it is acceptable", ["validation", "until valid", "password", "menu", "quit", "unknown"]),
        ], "A for loop repeats a known, fixed number of times, decided before the loop begins, or once for each item in a collection. A while loop repeats for as long as its condition remains true, so the number of iterations is not known in advance and depends on what happens while the program runs. A for loop would be the correct choice for calculating the total of an array of thirty marks, because the number of repetitions is known from the length of the array. A while loop would be the correct choice for repeatedly asking a user to enter a valid password, because there is no way to know in advance how many attempts they will need."),

        EQ("Explain what is meant by decomposition and describe how it could be used when writing a program to manage a school library.", 5, [
            MP("Decomposition means breaking a large problem into smaller sub problems", ["breaking", "smaller", "sub problems", "split", "divide"]),
            MP("Each sub problem is easier to understand and solve", ["easier", "simpler", "manageable"]),
            MP("Gives a valid sub problem such as searching for a book", ["search", "find a book", "look up", "catalogue"]),
            MP("Gives a second valid sub problem such as issuing or returning a book", ["issue", "borrow", "return", "loan", "due date"]),
            MP("States a benefit such as parts being testable separately or by different people", ["separately", "different people", "test", "independently", "reuse"]),
        ], "Decomposition means breaking a large complex problem down into smaller sub problems, each of which is small enough to be understood and solved on its own. For a school library system, one sub problem would be searching the catalogue for a book by title, author or subject. A second would be issuing a book, which involves recording who has borrowed it and calculating the due date. Further sub problems would include returning a book and clearing the loan, calculating and recording overdue fines, adding new stock to the catalogue and producing reports for the librarian. Breaking the problem down this way means each part can be written and tested independently, different people can work on separate parts at the same time, and a fault can be traced to one small section rather than searched for across the whole program."),

        EQ("A program uses a linear search on an unsorted list of 5000 names. Explain why a binary search could not be used instead, and state what would need to change.", 4, [
            MP("Binary search requires the data to be sorted", ["sorted", "in order", "must be sorted", "ordered"]),
            MP("It works by discarding half the list based on a comparison with the middle item", ["half", "middle", "discard", "compare"]),
            MP("On unsorted data that assumption is invalid so the result would be wrong", ["invalid", "wrong", "incorrect", "cannot assume", "fails"]),
            MP("The list would have to be sorted first, which itself takes time", ["sort first", "sorted first", "takes time", "cost of sorting"]),
        ], "A binary search cannot be used because it requires the data to be in sorted order. The algorithm compares the target with the middle item and then discards the entire half of the list in which the target cannot lie, and this reasoning is only valid if the list is ordered. On unsorted data there is no guarantee that the target is not in the half being discarded, so the search would frequently report that an item is absent when it is actually present. To use a binary search the list would first have to be sorted, which itself takes time. Whether that is worthwhile depends on how often the list is searched: sorting once and then performing many fast binary searches is a clear gain, but sorting 5000 names in order to perform a single search would take longer than simply scanning the list once."),
    ],
)

# ================================================= H446/01 Computer Systems

H446_P1 = Paper(
    slug="h446-paper-1-a",
    title="A Level Computer Science Paper 1: Computer Systems",
    course="A Level Computer Science",
    board="OCR",
    code="H446/01 style",
    minutes=110,
    marks=0,
    accent="var(--deep)",
    blurb="An original paper in the style of H446/01, covering processors, software and development, exchanging data, data types and structures, and legal and ethical issues.",
    advice="The extended response questions are levels marked, so structure, balance and a supported conclusion matter as much as the content. Use precise technical vocabulary, because a single correct term communicates more than a paragraph of description.",
    questions=[
        EQ("Describe the role of the Current Instruction Register and the status register within the processor.", 4, [
            MP("The CIR holds the instruction currently being decoded and executed", ["cir", "current instruction", "being decoded", "currently"]),
            MP("The instruction is copied into it from the MDR, freeing the MDR for data", ["mdr", "copied", "freeing", "available for data"]),
            MP("The status register holds flags set by the last operation", ["flags", "status", "last operation", "set by"]),
            MP("Such as zero, negative, carry and overflow, used by conditional branches", ["zero", "carry", "overflow", "negative", "conditional", "branch"]),
        ], "The Current Instruction Register holds the instruction that the processor is currently decoding and executing. During the fetch stage the instruction arrives from memory into the Memory Data Register and is then copied into the CIR, which frees the MDR to carry any data that the instruction subsequently requires. The status register holds a set of flags that are updated by each operation the ALU performs, including the zero flag when a result is zero, the negative flag when it is negative, and the carry and overflow flags when an arithmetic operation exceeds the available bits. These flags are what conditional branch instructions test in order to decide whether to jump."),

        EQ("Explain how pipelining increases the throughput of a processor and describe the effect of a conditional branch.", 5, [
            MP("Instruction processing is divided into stages such as fetch, decode and execute", ["stages", "divided", "fetch decode execute"]),
            MP("Different instructions occupy different stages simultaneously", ["simultaneously", "at the same time", "overlap", "while"]),
            MP("Throughput approaches one instruction completed per cycle once the pipeline is full", ["one per cycle", "throughput", "each cycle", "full"]),
            MP("A taken branch means the instructions already fetched are the wrong ones", ["branch", "wrong instructions", "not the next", "taken"]),
            MP("The pipeline is flushed and refilled, wasting the work already done", ["flushed", "flush", "discarded", "wasted", "refilled"]),
        ], "Pipelining divides the processing of an instruction into separate stages, typically fetch, decode and execute, and allows different instructions to occupy different stages at the same time. While one instruction is being executed, the next is being decoded and a third is being fetched, so although each individual instruction still takes three cycles to pass through, one instruction completes on every cycle once the pipeline is full, roughly tripling throughput without any increase in clock speed. A conditional branch disrupts this. The processor has already fetched and begun decoding the instructions that follow sequentially in memory, but if the branch is taken then execution should continue from somewhere else entirely, so those instructions are not the correct ones. The pipeline must be flushed, discarding the partly processed instructions, and refilled from the branch target, which wastes several cycles. Branch prediction reduces the cost by guessing the likely outcome from previous behaviour and speculatively filling the pipeline accordingly."),

        EQ("Compare RISC and CISC architectures, and explain why RISC is dominant in mobile devices.", 6, [
            MP("RISC has a small instruction set of simple fixed length instructions", ["small", "simple", "fixed length", "reduced"]),
            MP("CISC has a large instruction set with complex variable length instructions", ["large", "complex", "variable length"]),
            MP("RISC instructions usually complete in one cycle while CISC take several", ["one cycle", "single cycle", "several cycles", "multiple"]),
            MP("More instructions are needed per task in RISC, but complexity moves to the compiler", ["more instructions", "compiler", "complexity", "software"]),
            MP("Uniform instructions make RISC far easier to pipeline effectively", ["pipeline", "uniform", "easier", "same length"]),
            MP("Simpler hardware consumes less power, which is decisive for battery powered devices", ["power", "battery", "energy", "less heat", "efficient"]),
        ], "A RISC processor uses a small instruction set of simple instructions that are of fixed length and typically execute in a single clock cycle, whereas a CISC processor uses a large instruction set containing complex, powerful instructions of variable length that may take several cycles each. This produces a fundamental trade off in where complexity is placed. A CISC program needs fewer instructions to accomplish a given task, because one instruction may perform work that would take several in RISC, and that complexity is built into the hardware, often implemented internally using microcode. A RISC program needs more instructions, and the compiler must therefore be considerably more sophisticated in order to construct complex operations from simple ones, so the complexity moves into software. RISC is dominant in mobile devices for two connected reasons. First, its instructions are uniform in length and duration, which makes them exceptionally well suited to pipelining, so despite each instruction doing less work the processor sustains high throughput. Second, and decisively, simpler hardware requires fewer transistors and draws substantially less power per instruction executed, which directly determines battery life and also means less heat is generated, an essential consideration in a thin sealed device with no fan."),

        EQ("Explain the difference between paging and segmentation in memory management.", 4, [
            MP("Paging divides memory into fixed size pages mapped to equally sized frames", ["fixed size", "pages", "frames", "equal"]),
            MP("Segmentation divides memory into variable sized segments", ["variable", "different sizes", "segments"]),
            MP("Paging is decided by the operating system regardless of program structure", ["operating system", "regardless", "no relation", "physical"]),
            MP("Segmentation follows the logical structure of the program, such as functions or arrays", ["logical", "structure", "function", "array", "module"]),
        ], "Paging divides memory into fixed size blocks called pages, with physical memory divided into frames of identical size, so any page may be placed in any free frame and a page table records the mapping. The division is made by the operating system purely on the basis of size and takes no account of what the memory contains, so a single function may be split across a page boundary. Segmentation instead divides memory into variable sized segments that correspond to the logical structure of the program, so one segment may hold a particular procedure, another an array and another the stack. Because segments vary in size, allocating and releasing them leaves gaps of differing sizes between them, producing external fragmentation, whereas paging produces internal fragmentation because the last page of any allocation is rarely completely full."),

        EQ("Describe two scheduling algorithms used by an operating system, giving a strength and a weakness of each.", 6, [
            MP("Round robin gives each process a fixed time slice in turn", ["round robin", "time slice", "quantum", "in turn"]),
            MP("Strength: it is fair and responsive with no starvation", ["fair", "responsive", "no starvation", "equal"]),
            MP("Weakness: it ignores priority and context switching adds overhead", ["priority", "ignores", "overhead", "context switch"]),
            MP("Shortest job first runs the process with the shortest total time next", ["shortest job", "shortest first", "smallest"]),
            MP("Strength: it gives the best average waiting time", ["average waiting", "best average", "throughput", "efficient"]),
            MP("Weakness: it can starve long processes and requires run times to be known in advance", ["starve", "starvation", "known in advance", "estimate", "long processes"]),
        ], "Round robin scheduling places every ready process in a queue and gives each the processor for a fixed time slice before pre-empting it and moving it to the back of the queue. Its strength is fairness and responsiveness: every process receives processor time regularly, none can be starved and none can monopolise the processor, which makes an interactive system feel consistently responsive. Its weakness is that it takes no account of priority or urgency, so a time critical process waits exactly as long as a trivial one, and the frequent context switching consumes processor time that does no useful work. Shortest job first selects the process with the shortest total execution time to run next. Its strength is that it produces the lowest possible average waiting time, because completing many short jobs quickly reduces the total time processes spend waiting. Its weaknesses are significant, however: it requires the run time of each process to be known or estimated in advance, which is often unrealistic, and if short processes keep arriving a long process may never reach the front of the queue and is said to be starved."),

        EQ("Explain why HTTPS uses both symmetric and asymmetric encryption.", 5, [
            MP("Asymmetric encryption uses a freely distributable public key and a private key", ["public key", "private key", "asymmetric", "pair"]),
            MP("This solves the key distribution problem, since no secret needs to be transmitted", ["key distribution", "no secret", "openly", "solves"]),
            MP("Asymmetric encryption is computationally slow", ["slow", "slower", "computationally expensive", "overhead"]),
            MP("It is therefore used only to exchange a symmetric session key securely", ["session key", "exchange", "agree", "symmetric key"]),
            MP("The actual data is then encrypted symmetrically, which is much faster", ["faster", "actual data", "bulk", "symmetric", "quicker"]),
        ], "Symmetric encryption is fast and therefore well suited to encrypting the volume of data involved in a web session, but it requires both parties to hold the same secret key, and transmitting that key over an untrusted network exposes it to interception, which is the key distribution problem. Asymmetric encryption solves that problem completely, because the public key can be published openly and only the matching private key can decrypt what it encrypts, so no secret ever has to be transmitted. However, asymmetric encryption is computationally expensive and far too slow to use for an entire session. HTTPS therefore combines them: at the start of the connection asymmetric encryption is used to securely agree a symmetric session key, with the server's identity verified by a digital certificate issued by a certificate authority, and once both parties hold that session key all the actual data for the session is encrypted symmetrically. This obtains the secure key exchange of asymmetric encryption together with the speed of symmetric encryption."),

        EQ("A table stores OrderID, CustomerName, CustomerAddress, ProductID, ProductName and Price. Explain why this table is not in third normal form and describe how it should be restructured.", 6, [
            MP("CustomerName and CustomerAddress depend on the customer rather than the order", ["customer", "depends on the customer", "not the order", "repeated"]),
            MP("ProductName and Price depend on ProductID, not on OrderID", ["productid", "depends on", "product", "not orderid"]),
            MP("These are transitive dependencies, breaking third normal form", ["transitive", "third normal form", "3nf", "non key attribute"]),
            MP("This causes redundancy and update anomalies", ["redundancy", "repeated", "update anomaly", "inconsistent", "anomalies"]),
            MP("Create separate Customers and Products tables", ["customers table", "products table", "separate tables", "split"]),
            MP("The Orders table holds foreign keys to both", ["foreign key", "links", "references", "orders table"]),
        ], "The table is not in third normal form because it contains transitive dependencies: attributes that depend on other non key attributes rather than directly on the primary key. CustomerName and CustomerAddress depend on which customer placed the order rather than on the order itself, so a customer who places twenty orders has their name and address stored twenty times. ProductName and Price depend on ProductID rather than on OrderID, so the same product details are repeated in every order line containing that product. The consequences are redundancy and anomalies. Correcting a customer's address requires updating every one of their order records, and missing one leaves the database inconsistent, which is an update anomaly. A new product cannot be recorded until somebody orders it, which is an insertion anomaly, and deleting the last order for a product destroys all record of that product, which is a deletion anomaly. The correct structure is separate tables. A Customers table holds CustomerID as its primary key with the name and address. A Products table holds ProductID as its primary key with the name and price. An Orders table holds OrderID with a CustomerID foreign key, and because an order may contain several products a further OrderLines table holds OrderID and ProductID as foreign keys together with the quantity, resolving the many to many relationship between orders and products."),

        EQ("Convert the denary number -37 into 8 bit two's complement, showing your working.", 3, [
            MP("Converts 37 to binary as 00100101", ["00100101"]),
            MP("Inverts the bits to give 11011010", ["11011010", "invert", "flip"]),
            MP("Adds one to give 11011011", ["11011011", "add 1", "plus one"]),
        ], "First convert 37 into 8 bit binary: 32 + 4 + 1 = 37, giving 00100101. Then invert every bit, producing 11011010. Finally add one, giving 11011011. This can be checked by evaluating it with the most significant bit as a negative place value: -128 + 64 + 16 + 8 + 2 + 1 = -37."),

        EQ("Explain the trade off between range and precision in a floating point representation.", 4, [
            MP("The mantissa determines the precision of the value", ["mantissa", "precision", "significant", "accuracy"]),
            MP("The exponent determines the range of magnitudes representable", ["exponent", "range", "magnitude", "how large"]),
            MP("The total number of bits available is fixed", ["fixed", "total", "limited", "same number"]),
            MP("So increasing one necessarily reduces the other", ["reduces", "at the expense", "cannot increase both", "trade off"]),
        ], "In a floating point representation the mantissa holds the significant digits of the number and therefore determines how precisely a value can be represented, while the exponent determines how far the binary point can be shifted and therefore the range of magnitudes that can be expressed. Because the total number of bits allocated to a floating point value is fixed, every bit given to the exponent is taken from the mantissa and vice versa. Widening the exponent allows extremely large and extremely small numbers to be represented but leaves fewer mantissa bits, so each value is stored to fewer significant figures and rounding errors grow. Widening the mantissa gives greater accuracy for each stored value but restricts the magnitudes that can be represented at all. The designer must therefore choose the split according to whether the application demands extreme magnitudes or high accuracy over a moderate range."),

        EQ("Explain how a hash table achieves average constant time lookup and describe what happens when a collision occurs.", 5, [
            MP("A hash function converts the key into an index in the underlying array", ["hash function", "index", "converts", "maps"]),
            MP("The item is stored at and retrieved from that index directly with no searching", ["directly", "no search", "immediately", "single access"]),
            MP("So lookup time does not increase as the number of items grows", ["does not increase", "regardless", "constant", "same time"]),
            MP("A collision occurs when two different keys hash to the same index", ["collision", "same index", "two keys"]),
            MP("Resolved by chaining, storing a list at that slot, or by probing for the next free slot", ["chaining", "linked list", "probing", "next free", "open addressing"]),
        ], "A hash table applies a hash function to the key, which deterministically converts it into an index within the underlying array. The item is stored at that index when it is inserted, and to retrieve it the same hash function is applied to the search key, producing the same index, so the item is found by a single direct array access with no searching of the structure at all. Because the position is calculated rather than searched for, the time taken does not grow as the number of stored items increases, which is what gives average constant time performance. A collision occurs when two different keys produce the same index. Under separate chaining, each slot holds a linked list and colliding items are appended to it, so lookup hashes to the slot and then searches only that short list. Under open addressing, the colliding item is placed in the next free slot instead, which avoids additional structures but tends to produce clusters of occupied slots that lengthen subsequent searches. In both cases performance degrades as the load factor rises, which is why the table is rehashed into a larger array once occupancy passes a threshold."),

        EQ("Explain what is meant by a race condition and describe one way of preventing it.", 4, [
            MP("Two or more threads access shared data at the same time", ["threads", "shared data", "same time", "concurrent"]),
            MP("The result depends on the unpredictable order in which their operations interleave", ["order", "interleave", "unpredictable", "timing", "depends on"]),
            MP("This can produce incorrect results that occur only intermittently", ["incorrect", "intermittent", "sometimes", "hard to reproduce", "occasionally"]),
            MP("Prevention such as locking the shared resource so only one thread accesses it at a time", ["lock", "mutex", "semaphore", "one at a time", "exclusive", "synchronisation"]),
        ], "A race condition occurs when two or more threads access shared data concurrently and at least one of them modifies it, so that the final result depends on the precise order in which their individual operations happen to interleave. A typical example is two threads each reading a counter, adding one and writing it back: if both read before either writes, one increment is lost. The defining difficulty is that the outcome is timing dependent, so the fault may appear only occasionally and may be impossible to reproduce under a debugger, which makes it exceptionally hard to diagnose. Prevention requires enforcing mutual exclusion, typically by using a lock or mutex around the section of code that accesses the shared resource, so that only one thread may enter it at a time and any other thread attempting to do so is made to wait. The cost is reduced parallelism within that section and the risk of deadlock if two threads acquire locks in different orders."),

        EQ("Discuss the ethical issues raised by a company using an algorithm trained on historical hiring decisions to filter job applications.", 9, [
            MP("The system learns patterns from historical data", ["historical", "past decisions", "learns", "trained"]),
            MP("Any discrimination present in past decisions is reproduced by the system", ["discrimination", "bias", "reproduced", "repeats", "unfair"]),
            MP("The output appears objective, so it is trusted and challenged less", ["objective", "appears", "trusted", "neutral", "not questioned"]),
            MP("Names a group likely to be disadvantaged", ["gender", "ethnicity", "age", "disability", "background", "women", "postcode"]),
            MP("Removing protected characteristics is insufficient because proxy variables carry the information", ["proxy", "correlate", "still infers", "indirectly", "not enough"]),
            MP("Accountability is unclear because no one can explain an individual rejection", ["accountability", "explain", "who is responsible", "opaque", "black box"]),
            MP("Recognises genuine benefits such as consistency, speed and reduced individual prejudice", ["consistent", "faster", "efficient", "volume", "individual prejudice", "benefit"]),
            MP("Applies an ethical framework or presents a substantive counterargument", ["deontological", "consequentialist", "rights", "however", "on the other hand", "against this"]),
            MP("Reaches a supported conclusion with specific safeguards", ["conclusion", "should", "audit", "human review", "transparency", "recommend", "overall"]),
        ], "The central problem is that a system trained on a company's historical hiring decisions learns the patterns present in those decisions, and it has no way of distinguishing patterns that reflect genuine job relevance from patterns that reflect past prejudice. If the company historically hired few women into technical roles, the model learns that applications resembling those of successful past candidates are preferable, and it will systematically downgrade applications from women without any instruction to consider gender at all. Attempting to solve this by removing protected characteristics from the input data is insufficient, because proxy variables carry the same information: the name of a school, membership of a sports club, a postcode or a gap in employment history can all correlate strongly with gender, ethnicity or socioeconomic background, and the model will find and use those correlations. The harm is amplified by how such decisions are perceived. An outcome produced by an algorithm carries an appearance of objectivity that a human decision does not, so it is scrutinised less and challenged less, and an applicant who suspects unfairness has no articulated reason to contest. This leads directly to accountability. If no one within the company can explain why a specific applicant was rejected, then in practice no one is answerable for it, and neither the applicant nor a tribunal can test whether the decision was lawful under equality legislation. A deontological analysis weighs heavily against the system as described: applicants have a right to be assessed on their own merits rather than on statistical resemblance to previous hires, and that right does not depend on whether the aggregate outcome is efficient. There are nonetheless real benefits, and a consequentialist analysis is more finely balanced. A large employer may receive thousands of applications for a single role, and human screening at that volume is itself inconsistent, subject to fatigue and demonstrably affected by individual prejudice such as name bias. An algorithm applies identical criteria to every application, processes them in seconds, and can be audited in a way that a hundred individual recruiters' judgements cannot. Overall the company should not deploy the system in the form described, but the appropriate response is regulation rather than abandonment. The defensible position is to use algorithmic screening only with specific safeguards: auditing outputs for disparate impact across protected characteristics rather than merely excluding those characteristics from the inputs, requiring that every rejection can be explained in terms a candidate would understand, retaining meaningful human review of borderline and rejected applications rather than treating the output as final, and retraining on data that has itself been examined and corrected for historical bias. Without those safeguards the system does not remove human prejudice from hiring, it automates it, scales it and conceals it."),

        EQ("Explain two advantages of using a dynamic linked library rather than statically linking library code into an executable.", 4, [
            MP("The executable is smaller because the library code is not included", ["smaller", "not included", "reference only", "size"]),
            MP("One copy of the library serves every program that uses it, saving memory and disk space", ["one copy", "shared", "several programs", "memory", "disk space"]),
            MP("An update to the library benefits every program without any of them being rebuilt", ["update", "benefits every", "without rebuilding", "recompile", "security fix"]),
            MP("Acknowledges the run time dependency as the trade off", ["dependency", "missing", "must be present", "incompatible", "trade off"]),
        ], "The first advantage is size and memory efficiency. With dynamic linking the executable contains only a reference to the library rather than a copy of its code, so the file itself is considerably smaller, and because a single copy of the library serves every program on the system that uses it, both disk space and memory are saved compared with statically linking the same code into a dozen separate executables. The second advantage is maintenance. When a defect or a security vulnerability is found in the library, replacing that one shared file fixes the problem for every program that depends on it, with none of them needing to be recompiled or redistributed. Under static linking each affected program would have to be rebuilt and reissued individually, which in practice means many never are. The trade off is a run time dependency: if the library is missing, or has been replaced with an incompatible version, the program will fail to start or behave unpredictably."),

        EQ("Explain what is meant by an admissible heuristic and why A star requires one to guarantee an optimal path.", 4, [
            MP("A heuristic estimates the remaining cost from a node to the goal", ["estimate", "remaining", "to the goal", "cost"]),
            MP("An admissible heuristic never overestimates that cost", ["never overestimates", "underestimate", "at most", "does not exceed"]),
            MP("A star selects nodes by f equals g plus h, the cost so far plus the estimate", ["f = g + h", "g plus h", "cost so far", "estimate"]),
            MP("If the heuristic overestimated, a shorter path could be discarded before being explored", ["overestimate", "discarded", "not explored", "miss", "suboptimal"]),
        ], "A heuristic in A star is a function that estimates the cost of travelling from a given node to the goal, and it is what allows the search to be directed towards the destination rather than expanding equally in every direction. A heuristic is admissible if it never overestimates the true remaining cost, so its estimate is always less than or equal to the actual cost of the best remaining path. A star expands nodes in order of f, which is g plus h, where g is the actual cost accumulated from the start and h is the heuristic estimate. Admissibility guarantees optimality because it ensures the algorithm never dismisses a node whose true total cost is lower than the one it chooses. If the heuristic overestimated the remaining cost for some node, that node's f value would be inflated, so it could be passed over in favour of a node that actually lies on a longer path, and the algorithm would return a suboptimal route while believing it optimal. Straight line distance is the standard admissible heuristic for geographic pathfinding, because no real route between two points can be shorter than the straight line between them."),

        EQ("Explain the difference between the waterfall and agile methodologies and identify a scenario in which each would be the better choice.", 6, [
            MP("Waterfall completes each stage fully before beginning the next", ["sequential", "each stage", "completed before", "in order"]),
            MP("Agile works in short iterations delivering working software repeatedly", ["iterations", "cycles", "sprints", "incremental", "repeatedly"]),
            MP("Waterfall produces comprehensive documentation at every stage", ["documentation", "documented", "records", "signed off"]),
            MP("Agile involves the customer continuously and adapts to changing requirements", ["customer", "continuous", "changing requirements", "feedback", "adapts"]),
            MP("Waterfall suits a scenario with fixed requirements and a documentation obligation", ["fixed requirements", "regulated", "safety critical", "documentation required", "contract"]),
            MP("Agile suits a scenario with uncertain or evolving requirements and an available customer", ["uncertain", "evolving", "start up", "available customer", "will change"]),
        ], "Waterfall is a sequential methodology in which analysis, design, implementation, testing and evaluation are each completed and formally signed off before the next begins, producing comprehensive documentation at every stage. Agile is iterative: the work is divided into short cycles, each of which delivers a working increment that the customer reviews, and their feedback shapes what is built next. The consequences differ sharply. Waterfall gives strong managerial control and a complete audit trail but handles change extremely badly, since altering a requirement after design is complete means revisiting earlier stages at substantial cost, and the client sees nothing running until late. Agile treats change as normal rather than exceptional and surfaces misunderstandings within weeks, but it requires continuous customer availability, makes the final cost and date harder to predict, and produces lighter documentation that can hinder maintenance years later. Waterfall would be the better choice for control software in a medical device, where the requirements are fixed by regulation and cannot change, and where a regulator requires documented evidence that every requirement was specified, designed for and tested before approval is granted. Agile would be the better choice for a start up building a consumer application, where nobody yet knows exactly what users want, the requirements will certainly change as the product is tested with real people, and the ability to release, learn and adjust quickly matters far more than a fixed specification."),
    ],
)

# ======================================== H446/02 Algorithms and Programming

H446_P2 = Paper(
    slug="h446-paper-2-a",
    title="A Level Computer Science Paper 2: Algorithms and Programming",
    course="A Level Computer Science",
    board="OCR",
    code="H446/02 style",
    minutes=110,
    marks=0,
    accent="var(--purple)",
    blurb="An original paper in the style of H446/02, covering computational thinking, programming techniques, computational methods and algorithms including complexity and pathfinding.",
    advice="Write code in OCR reference language or a high level language of your choice, but be consistent. On algorithm questions, show the trace in full. On extended questions, justify every choice against the scenario given.",
    questions=[
        EQ("Explain the difference between representational abstraction and abstraction by generalisation.", 4, [
            MP("Representational abstraction removes detail until only what is needed remains", ["removes", "detail", "only what is needed", "simplify"]),
            MP("Gives an example such as a map or a simulation model", ["map", "underground", "model", "diagram", "simulation"]),
            MP("Abstraction by generalisation groups things sharing characteristics so one solution serves all", ["group", "shared", "common", "one solution", "categorise"]),
            MP("Gives an example such as a superclass covering several related types", ["superclass", "class", "inheritance", "vehicle", "shape"]),
        ], "Representational abstraction removes detail from a situation until only the information needed to solve the specific problem remains. A map of the Underground is the standard example, discarding real distances, geography and everything above ground while retaining exactly what a passenger needs: the order of stations and where lines interchange. Abstraction by generalisation instead groups different things according to characteristics they share so that a single solution serves all of them. Defining a Shape superclass with an area method, from which Circle, Square and Triangle inherit, is an example: code written to work with Shape then works with every kind of shape, including ones added later, without being rewritten."),

        EQ("Write a recursive function that returns the nth term of the Fibonacci sequence, and explain why an iterative version would be preferable for large values of n.", 6, [
            MP("Defines a function with n as a parameter", ["def", "function", "(n)"]),
            MP("Includes correct base cases for n equal to 0 and 1", ["base case", "n <= 1", "if n", "0 or 1", "return n"]),
            MP("Returns the sum of the two previous terms recursively", ["return", "n-1", "n-2", "fibonacci(n-1)", "recursive"]),
            MP("The recursive version recalculates the same values many times", ["recalculates", "repeated", "same values", "many times", "exponential"]),
            MP("Each call adds a stack frame, so deep recursion risks a stack overflow", ["stack frame", "stack overflow", "memory", "deep"]),
            MP("An iterative version runs in linear time using constant memory", ["linear", "constant memory", "loop", "faster", "efficient"]),
        ], "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n - 1) + fibonacci(n - 2)\n\nThe base case returns n directly when n is 0 or 1, which stops the recursion, and the general case returns the sum of the two preceding terms. An iterative version is strongly preferable for large n for two reasons. First, the naive recursive version recalculates the same subproblems an enormous number of times: computing the tenth term requires computing the eighth twice, the seventh three times and so on, and the total number of calls grows exponentially, so even a modest n such as 40 takes a noticeable time and n of 60 is entirely impractical. Second, every call adds a stack frame holding its parameters and return address, and those frames accumulate until the recursion unwinds, so deep recursion risks exhausting the stack. An iterative version keeps only the two most recent terms in variables and loops forward, which runs in linear time with constant memory and handles large n instantly."),

        EQ("Explain what is meant by passing a parameter by reference and state one advantage and one disadvantage.", 4, [
            MP("The memory address of the data is passed rather than a copy", ["address", "reference", "pointer", "not a copy", "location"]),
            MP("Changes made inside the subroutine affect the original data", ["affect the original", "changes", "modifies", "persists"]),
            MP("Advantage: no copy is made, so it is efficient for large data structures", ["no copy", "efficient", "large", "memory", "faster"]),
            MP("Disadvantage: side effects are possible, making the program harder to reason about", ["side effects", "unexpected", "harder", "unintended", "risk"]),
        ], "Passing by reference means the subroutine is given the memory address of the caller's data rather than a copy of the data itself, so any modification the subroutine makes is made directly to the original and persists after the subroutine returns. The advantage is efficiency: no copy is created, so passing a large array or object costs the same as passing a single address rather than duplicating potentially megabytes of data, and it also allows the subroutine to return several results by modifying the variables it was given. The disadvantage is that side effects become possible, since a subroutine can alter data the caller did not expect it to touch, and this makes the program considerably harder to reason about and to debug because a variable's value can change without any assignment appearing in the calling code."),

        EQ("Describe the operation of a quicksort and explain when its worst case occurs.", 6, [
            MP("A pivot element is chosen from the list", ["pivot", "chosen", "select"]),
            MP("The list is partitioned so smaller values are on one side and larger on the other", ["partition", "smaller", "larger", "either side", "divided"]),
            MP("Each partition is then sorted recursively by the same method", ["recursively", "repeat", "same method", "each partition"]),
            MP("Average time complexity is O(n log n)", ["n log n", "average", "log"]),
            MP("The worst case is O(n squared) when the pivot is consistently the smallest or largest element", ["n squared", "worst case", "smallest", "largest", "poor pivot"]),
            MP("This occurs for example when the first element is the pivot and the data is already sorted", ["already sorted", "first element", "sorted data", "reverse"]),
        ], "Quicksort selects one element of the list as the pivot and then partitions the remaining elements so that all values smaller than the pivot are placed to its left and all larger values to its right, which puts the pivot into its final correct position. The two partitions are then sorted recursively by exactly the same method, and because a single item partition is already sorted, the recursion terminates. On average each partition divides the data roughly in half, giving about log n levels of recursion with n comparisons at each level, so the average time complexity is O(n log n), and in practice quicksort usually outperforms merge sort because its constant factors are smaller and it partitions in place. The worst case is O(n squared) and occurs when the pivot chosen is consistently the smallest or largest remaining element, because each partition then removes only one item rather than halving the data, producing n levels of recursion. The classic way this happens is choosing the first element as the pivot on data that is already sorted or reverse sorted, which is why practical implementations select the pivot at random or as the median of three sampled values."),

        EQ("Explain how Dijkstra's algorithm determines the shortest path in a weighted graph, and state one limitation.", 6, [
            MP("The source distance is set to zero and all others to infinity", ["zero", "infinity", "source", "initialise"]),
            MP("The unvisited node with the smallest known distance is selected", ["smallest", "lowest", "unvisited", "current"]),
            MP("For each neighbour, the distance through the current node is calculated", ["neighbour", "distance through", "calculate", "via"]),
            MP("If smaller than the recorded distance it is updated, along with the predecessor", ["smaller", "updated", "replace", "predecessor", "previous"]),
            MP("The node is marked visited and the process repeats until the destination is reached", ["marked visited", "repeats", "until", "destination"]),
            MP("Limitation: it cannot handle negative edge weights", ["negative", "cannot handle", "negative weights", "limitation"]),
        ], "Dijkstra's algorithm initialises the distance to the source node as zero and to every other node as infinity, with all nodes unvisited. It then repeatedly selects the unvisited node with the smallest recorded distance and treats it as the current node. For each unvisited neighbour of that node it calculates the distance reached by travelling through the current node, which is the current node's distance plus the weight of the connecting edge, and if this is smaller than the neighbour's recorded distance then the record is updated and the current node is stored as that neighbour's predecessor. The current node is then marked as visited, since its distance is now known to be final, and the process repeats until the destination has been visited or no reachable unvisited node remains. The path itself is recovered by following the chain of predecessors backwards from the destination. The principal limitation is that the algorithm cannot handle negative edge weights, because its correctness rests on the assumption that once a node is marked visited no shorter route to it can be found later, and a negative edge encountered subsequently could invalidate exactly that assumption."),

        EQ("A program must find whether a value exists in a collection of 2 million items, and this operation is performed thousands of times per second. Compare the suitability of a linear search, a binary search and a hash table.", 6, [
            MP("Linear search is O(n) and would examine up to 2 million items per query", ["o(n)", "linear", "2 million", "every item"]),
            MP("It requires no ordering but is far too slow at this frequency", ["no ordering", "unsorted", "too slow", "impractical"]),
            MP("Binary search is O(log n), needing about 21 comparisons", ["log n", "21", "20", "about 20", "halves"]),
            MP("But it requires the collection to be kept sorted, which costs time on insertion", ["sorted", "must be sorted", "insertion", "maintain order"]),
            MP("A hash table gives average O(1) because the position is calculated from the key", ["o(1)", "constant", "calculated", "hash function"]),
            MP("Recommends the hash table for pure membership testing, noting it provides no ordering", ["hash table", "recommend", "no ordering", "range queries", "best"]),
        ], "A linear search has complexity O(n), so with two million items it would examine on average a million entries per query, and at thousands of queries per second this is entirely impractical however simple it is to implement. Its only advantage is that it requires no ordering and no preparation. A binary search has complexity O(log n), reducing the work to about twenty one comparisons since two to the power twenty one exceeds two million, which is an improvement of roughly five orders of magnitude. Its precondition is that the collection is maintained in sorted order, which means either a one off sort at O(n log n) if the data is static, or an ongoing insertion cost, since inserting into a sorted array requires shifting subsequent elements. A hash table gives average O(1) lookup, because the hash function calculates the storage position directly from the key so no searching occurs at all, and the time taken does not increase with the size of the collection. For pure membership testing at this frequency the hash table is clearly the best choice, provided a good hash function is used and the load factor is kept low enough that collisions remain rare. The one consideration against it is that a hash table imposes no useful ordering, so if the system also needs sorted output or range queries then a balanced binary search tree, giving O(log n) for both lookup and in order traversal, would be the better overall structure."),

        EQ("Explain what is meant by a heuristic and describe a situation where using one is appropriate.", 4, [
            MP("A rule of thumb producing an acceptable solution quickly", ["rule of thumb", "good enough", "acceptable", "approximate"]),
            MP("It does not guarantee the optimal solution", ["not guaranteed", "not optimal", "may not be best"]),
            MP("Appropriate where an exhaustive search would take unacceptably long", ["too long", "exhaustive", "impractical", "infeasible", "unacceptable"]),
            MP("Gives a valid example such as pathfinding or the travelling salesman problem", ["pathfinding", "a star", "satnav", "travelling salesman", "chess", "scheduling"]),
        ], "A heuristic is a rule of thumb that guides a search towards a good solution quickly, without any guarantee that the solution found is the best one available. It is appropriate whenever finding the genuinely optimal answer would require exploring so many possibilities that the computation is infeasible within an acceptable time. Route finding illustrates this well. A satnav could in principle evaluate every possible sequence of roads between two points and select the shortest, but the number of possibilities in a national road network is astronomically large. Instead the A star algorithm uses the straight line distance to the destination as a heuristic to decide which routes look most promising and explores those first, ignoring directions that lead away from the target. A route is produced in a fraction of a second and is optimal or very close to it, and a driver waiting at a junction is far better served by an excellent answer immediately than a perfect one after an hour of computation."),

        EQ("Explain why a queue is the appropriate data structure for a breadth first search and a stack is appropriate for a depth first search.", 4, [
            MP("Breadth first explores all nodes at the current depth before going deeper", ["all nodes", "current depth", "level by level", "before going deeper"]),
            MP("A queue is first in first out, so nodes are processed in the order discovered", ["first in first out", "fifo", "order discovered", "oldest"]),
            MP("Depth first explores as far as possible along one path before backtracking", ["as far as possible", "deep", "one path", "backtrack"]),
            MP("A stack is last in first out, so the most recently discovered node is explored next", ["last in first out", "lifo", "most recent", "newest"]),
        ], "Breadth first search must visit every node at the current depth before moving on to any node at the next depth, which means nodes should be processed in exactly the order in which they were discovered. A queue is first in first out, so the node that has been waiting longest is always the next one taken, and since nodes at the current level are discovered before nodes at the next level, the queue naturally produces level by level exploration. Depth first search must follow one path as far as it goes before backtracking to try an alternative, which means the node most recently discovered should be the next one explored. A stack is last in first out, so pushing each newly discovered node and popping the top gives exactly that behaviour, and when a path reaches a dead end the stack automatically returns to the most recent unexplored branch, which is the backtracking the algorithm requires."),

        EQ("A student writes a program that reads a large file line by line, and inside the loop it opens the file again to count the total number of lines. Explain why this is inefficient and describe how the program should be restructured.", 5, [
            MP("The file is opened and read completely on every iteration of the loop", ["every iteration", "each time", "repeatedly", "reopened"]),
            MP("This turns a linear operation into a quadratic one", ["quadratic", "n squared", "much slower", "far more work"]),
            MP("File access is far slower than in memory operations", ["file access", "slow", "disk", "input output", "slower than memory"]),
            MP("The count does not change, so it should be calculated once before the loop", ["once", "before the loop", "does not change", "outside the loop"]),
            MP("Store the result in a variable and reuse it inside the loop", ["variable", "store", "reuse", "then use it"]),
        ], "The problem is that the total number of lines does not change while the loop runs, yet the program recalculates it on every single iteration by reopening and completely re-reading the file. If the file contains n lines, the outer loop runs n times and each iteration reads n lines, so the program performs n squared read operations instead of n, turning a linear task into a quadratic one. This is particularly costly because file access involves the operating system and secondary storage and is orders of magnitude slower than operations on data already in memory, so the effect on a large file is severe. The correct restructuring is an application of thinking ahead: any calculation whose result does not change during a loop should be moved out of it. The program should count the lines once before the loop begins, or better still read the file once into a list and take its length, store that value in a variable, and then simply refer to that variable inside the loop. This reduces the program to a single pass over the file."),

        EQ("Explain the difference between time complexity and space complexity, and give an example of an algorithm where the two conflict.", 5, [
            MP("Time complexity describes how the number of operations grows with input size", ["operations", "time", "grows", "input size"]),
            MP("Space complexity describes how the memory required grows with input size", ["memory", "space", "storage", "grows"]),
            MP("Gives a valid example such as merge sort against bubble sort", ["merge sort", "bubble sort", "quicksort", "example"]),
            MP("Merge sort is faster at O(n log n) but requires O(n) additional memory", ["n log n", "faster", "o(n) space", "extra memory", "sub lists"]),
            MP("Bubble sort is slower at O(n squared) but sorts in place using O(1) memory", ["n squared", "slower", "in place", "constant memory", "o(1)"]),
        ], "Time complexity describes how the number of operations an algorithm performs grows as the size of its input increases, while space complexity describes how the amount of memory it requires grows with that input. The two frequently conflict, because many techniques for reducing time work by storing additional information. Sorting provides a clear example. Merge sort has time complexity O(n log n) in every case, which is dramatically better than bubble sort's O(n squared), so on a million items merge sort is faster by a factor of tens of thousands. However, merge sort must create and hold the sub lists produced during the divide and merge phases, giving it space complexity O(n), whereas bubble sort operates entirely within the original array using a single temporary variable and therefore has space complexity O(1). On a general purpose machine sorting a large array the time saving is overwhelmingly worth the memory, but on an embedded device with a few kilobytes of RAM the additional allocation may simply be unavailable, and the slower in place algorithm becomes the only viable option."),

        EQ("Discuss the benefits and difficulties of designing a program to use concurrent processing.", 9, [
            MP("Independent parts of a task can execute simultaneously", ["simultaneously", "at the same time", "parallel", "independent"]),
            MP("Total elapsed time falls and processor resources are used more fully", ["elapsed time", "faster", "fully used", "utilisation", "reduced"]),
            MP("The system can remain responsive while long work continues in the background", ["responsive", "background", "interface", "user"]),
            MP("Only the parallelisable fraction benefits, and Amdahl's law caps the speedup", ["amdahl", "fraction", "sequential", "cap", "limit"]),
            MP("Data dependencies force some operations to wait for earlier results", ["dependencies", "wait", "depends on", "earlier results"]),
            MP("Race conditions produce results dependent on unpredictable interleaving", ["race condition", "interleaving", "timing", "unpredictable", "shared data"]),
            MP("Locking introduces the risk of deadlock", ["deadlock", "lock", "waiting for each other", "mutex"]),
            MP("Synchronisation overhead grows with the number of threads", ["overhead", "synchronisation", "coordination", "grows"]),
            MP("Reaches a supported conclusion about when concurrency is justified", ["conclusion", "justified", "worth it", "when", "overall", "therefore"]),
        ], "The principal benefit of concurrency is that parts of a task which do not depend on one another can execute at the same time rather than sequentially, so the total elapsed time falls and the available processor cores are used fully rather than sitting idle. Work such as rendering the individual frames of an animation, applying a filter to a large set of images or serving independent requests on a web server parallelises almost perfectly, because each unit of work is entirely self contained. A second benefit is responsiveness: running long computation on a separate thread allows a user interface to continue reacting to input rather than freezing, which is often the reason concurrency is introduced even when no speedup is expected. The difficulties are substantial and they are of two kinds. The first kind concerns how much benefit is actually available. Only the portion of the work that can genuinely be divided gains anything, and Amdahl's law states that whatever fraction must remain sequential sets a hard ceiling on the achievable speedup no matter how many processors are added, so a task that is twenty per cent sequential can never be more than five times faster. Data dependencies restrict division further, because any operation requiring the result of a previous one must wait for it, and the coordination overhead of creating threads, distributing work and gathering results grows as more threads are added, eventually outweighing the gain. The second kind of difficulty concerns correctness, and it is the more serious. Where threads share mutable data, race conditions become possible: if two threads read, modify and write the same value without synchronisation, the final result depends on the precise order in which their operations interleave, so the program may produce the right answer in testing and the wrong one occasionally in production, and such faults are extremely difficult to reproduce and diagnose. Preventing this requires locks, which introduce the possibility of deadlock when two threads each hold a resource the other is waiting for, and which reduce the very parallelism they were introduced to protect. Concurrent code is therefore markedly harder to write, test, debug and reason about than sequential code. Concurrency is justified when the work divides into genuinely independent units, when the sequential fraction is small, and when the resulting time saving is large enough to repay the substantial additional complexity. Where those conditions do not hold, and particularly where correctness matters more than speed, a straightforward sequential design is usually the better engineering decision."),

        EQ("Explain what is meant by a precondition, and describe why documenting preconditions matters.", 4, [
            MP("A condition that must be true before a subroutine is called for it to work correctly", ["must be true", "before", "called", "correctly"]),
            MP("Gives a valid example such as a sorted array for a binary search", ["sorted", "binary search", "not empty", "positive", "example"]),
            MP("If it is not met the subroutine may return an incorrect result rather than raising an error", ["incorrect", "wrong result", "no error", "silently", "fails"]),
            MP("Documenting it makes the caller's obligation explicit and prevents misuse", ["explicit", "caller", "obligation", "prevents", "misuse", "clear"]),
        ], "A precondition is a statement that must be true at the moment a subroutine is called if that subroutine is to behave correctly. It expresses an assumption the subroutine relies on rather than one it checks, so it places an obligation on the calling code. A binary search, for example, has the precondition that the array passed to it is sorted in ascending order, because it decides which half of the range to discard on precisely that assumption. Documenting preconditions matters because a violated precondition frequently produces no error at all: a binary search on unsorted data runs perfectly happily and simply returns wrong answers, reporting that present items are absent. A fault that announces itself is far cheaper than one that quietly corrupts results, so making the obligation explicit in the documentation lets the caller guarantee it, and it also allows a maintainer to understand why the subroutine is written as it is rather than adding defensive checks that would slow it down unnecessarily."),

        EQ("Explain how polymorphism allows new functionality to be added to a program without modifying existing code.", 5, [
            MP("Objects of different classes respond to the same method call", ["same method", "different classes", "same interface"]),
            MP("Each class provides its own implementation of that method", ["own implementation", "own version", "overrides", "different behaviour"]),
            MP("Existing code calls the method without needing to know the object's type", ["without knowing", "does not check", "any type", "regardless"]),
            MP("A new class can therefore be added simply by writing it", ["new class", "just write", "add a class", "only"]),
            MP("The existing loops and functions continue to work unchanged", ["unchanged", "no modification", "still work", "no changes needed"]),
        ], "Polymorphism means that objects of different classes, related through a common superclass or interface, all respond to the same method call, with each class providing its own implementation of that method. Existing code can therefore call the method on a collection of such objects without ever examining what type each one actually is, because the correct implementation is selected at run time by the object itself. The consequence is that adding new functionality requires only that a new class be written which implements the expected interface. A game loop that calls update on every object in a list continues to work correctly when a new kind of enemy is added, because the new class simply provides its own update, and not a single line of the loop needs to change. Without polymorphism the loop would need a conditional branch for every possible type, and adding a new type would mean finding and modifying every such loop throughout the program, which is both laborious and a reliable source of defects when one is missed."),
    ],
)

# ============================================= R093 Creative iMedia paper

R093_P1 = Paper(
    slug="r093-paper-a",
    title="Creative iMedia R093: Creative iMedia in the Media Industry",
    course="Creative iMedia",
    board="OCR",
    code="R093 style",
    minutes=75,
    marks=0,
    accent="var(--lilac-deep)",
    blurb="An original paper in the style of the R093 examined unit, covering the media industry, factors influencing product design, pre-production planning and distribution.",
    advice="Read the scenario carefully and refer to it directly in your answers. Marks are awarded for applying knowledge to the situation described, not for general statements about media production.",
    questions=[
        EQ("Identify two job roles in the post-production stage of a video project and describe what each does.", 4, [
            MP("First valid post-production role named", ["video editor", "sound editor", "vfx", "colourist", "quality assurance"]),
            MP("Description of what that role does", ["assembles", "edits", "mixes", "effects", "grades", "tests"]),
            MP("Second valid post-production role named", ["video editor", "sound editor", "vfx", "colourist", "quality assurance"]),
            MP("Description of what that role does", ["assembles", "edits", "mixes", "effects", "grades", "tests"]),
        ], "A video editor works in post-production, assembling the recorded footage into the finished sequence by selecting the best takes, trimming shots to length, ordering them and adding transitions so the piece flows as intended. A sound editor also works in post-production, editing and mixing the audio, balancing dialogue against music and effects, removing unwanted noise and adding any sound effects required so that the finished soundtrack is clear and consistent throughout."),

        EQ("Explain why a client brief is produced at the start of a media project.", 4, [
            MP("It sets out what the client requires from the product", ["requires", "needs", "wants", "specification"]),
            MP("Including the purpose, target audience and deadline", ["purpose", "audience", "deadline", "budget", "format"]),
            MP("It gives the designer a clear basis for their decisions", ["basis", "decisions", "guides", "informs", "reference"]),
            MP("It prevents misunderstandings and work having to be redone", ["misunderstanding", "redone", "wrong", "disagreement", "avoid"]),
        ], "A client brief sets out in writing exactly what the client requires from the product, typically including its purpose, the target audience, the deadline, the budget, the formats needed, any brand guidelines that must be followed and any content that must be included. It matters because it gives the designer a clear and agreed basis for every decision they subsequently make, so that choices about style, content and layout can be justified against something concrete rather than assumed. It also protects both parties: without a written brief, a designer may produce work based on a reasonable interpretation that turns out to differ from what the client had in mind, and the work then has to be redone at cost to somebody. The brief also serves as the reference against which the finished product is reviewed."),

        EQ("A company is producing a poster advertising a new energy drink aimed at 16 to 24 year olds. Describe three factors that would influence the design and explain the effect of each.", 6, [
            MP("The target audience influences the style and tone", ["audience", "16 to 24", "young", "style", "tone"]),
            MP("Explains a consequence such as bold energetic visuals suiting that age group", ["bold", "energetic", "bright", "modern", "suits", "appeal"]),
            MP("The purpose influences what must be communicated", ["purpose", "advertise", "persuade", "sell", "promote"]),
            MP("Explains that the product name and brand must be prominent", ["prominent", "name", "brand", "stand out", "recognisable"]),
            MP("The client requirements or brand guidelines constrain colour and logo use", ["brand guidelines", "colours", "logo", "client", "existing"]),
            MP("Where the poster will be displayed affects legibility and size of key elements", ["where", "displayed", "distance", "legible", "size", "location"]),
        ], "The first factor is the target audience of 16 to 24 year olds, which influences the style and tone directly. That group responds to bold, high energy visuals, contemporary typography and imagery associated with sport, music or nightlife, so a muted or formal design would fail regardless of how well executed it was. The second factor is the purpose, which is to advertise and persuade. This means the product name, the packaging and the brand identity must be immediately prominent, because a viewer who finds the poster striking but cannot recall what was being advertised has not been persuaded of anything. The third factor is where the poster will be displayed. If it is intended for bus shelters and station platforms it will be seen from several metres away and for only a few seconds, so the key elements must be legible at that distance and the amount of text must be minimal, whereas a poster in a magazine can carry more detail. Brand guidelines set by the client are a further constraint, since the colours, logo and typeface may already be fixed by the company's existing visual identity."),

        EQ("Describe the purpose of a visualisation diagram and state three pieces of information it should contain.", 4, [
            MP("It shows how a static product such as a poster will look", ["static", "poster", "how it will look", "single design"]),
            MP("Contains dimensions and the position of each element", ["dimensions", "size", "position", "placement", "layout"]),
            MP("Contains the colours to be used", ["colours", "colour", "hex", "palette"]),
            MP("Contains the fonts and any images or text to be included", ["fonts", "typeface", "images", "text", "content"]),
        ], "A visualisation diagram is an annotated sketch showing how a static product such as a poster, magazine cover or packaging design will look, produced before any work begins so that the client can see and approve the intended design while it is still cheap to change. It should contain the dimensions and orientation of the product, the position of every element on the page, the colours to be used given as specific values rather than vague descriptions, the fonts to be used with their sizes, and details of the images and text that will appear along with any effects or treatments applied to them."),

        EQ("Explain why a storyboard is used when planning a moving image product, and state four pieces of information each frame should include.", 6, [
            MP("It plans the sequence of shots before filming", ["sequence", "shots", "before filming", "plan"]),
            MP("It allows the client and crew to see how the product will look and flow", ["client", "crew", "see", "flow", "how it will look"]),
            MP("Includes the shot type", ["shot type", "close up", "long shot", "mid shot"]),
            MP("Includes the camera angle or movement", ["angle", "movement", "pan", "zoom", "tilt", "tracking"]),
            MP("Includes the duration of the shot", ["duration", "length", "seconds", "timing"]),
            MP("Includes the dialogue, sound or transition", ["dialogue", "sound", "music", "transition", "cut", "fade"]),
        ], "A storyboard plans the sequence of shots for a moving image product before any filming takes place, setting out what will be seen in each shot and in what order. It allows the client to see and approve how the finished product will look and flow while changes are still easy and inexpensive, and it gives the crew a clear plan on the day so that no required shot is missed and time is not wasted deciding what to film. Each frame should include a sketch of the composition together with the shot type such as a close up or long shot, the camera angle and any camera movement such as a pan or a zoom, the duration of the shot in seconds so that the total running time can be controlled, and the dialogue, sound effects or music accompanying it along with the transition into the next shot."),

        EQ("A student wants to use a piece of music found online in a promotional video. Explain the legal issues and describe two ways they could obtain suitable music legally.", 5, [
            MP("The music is protected by copyright", ["copyright", "protected", "owned"]),
            MP("Using it without permission breaches the Copyright, Designs and Patents Act 1988", ["permission", "copyright designs and patents", "1988", "illegal", "infringement"]),
            MP("The video could be removed or the client could face legal action", ["removed", "taken down", "legal action", "sued", "fine"]),
            MP("First legal option such as royalty free or licensed music", ["royalty free", "licensed", "stock", "purchase", "buy a licence"]),
            MP("Second legal option such as Creative Commons with attribution or composing their own", ["creative commons", "attribution", "compose", "own music", "original"]),
        ], "Music is protected by copyright automatically from the moment it is created, and that copyright belongs to the composer and usually also to the recording artist and the label. Using it in a promotional video without permission infringes the Copyright, Designs and Patents Act 1988, and because a promotional video is a commercial use the consequences are real: the video would be removed by any platform it was uploaded to, and the copyright holder could demand payment or take legal action for damages against the student and the client. Crediting the artist does not resolve this, because attribution is not permission. The first legal alternative is to obtain a licence, either by purchasing royalty free music from a stock library under a licence that explicitly permits commercial use, or by licensing a specific track directly from the rights holder. The second is to use music released under a Creative Commons licence that permits commercial use, following exactly whatever attribution conditions that licence requires, or to compose and record original music, which gives the client clear ownership with no ongoing conditions at all."),

        EQ("Explain why a work plan should include contingency time, and describe one other element a work plan should contain.", 4, [
            MP("Tasks frequently take longer than estimated", ["longer", "overrun", "delayed", "underestimated"]),
            MP("Unexpected problems occur such as illness or equipment failure", ["illness", "equipment", "failure", "unexpected", "problems"]),
            MP("Without contingency any delay pushes back the final deadline", ["deadline", "pushed back", "missed", "knock on", "late"]),
            MP("Another element such as tasks with durations, dependencies, milestones or responsibilities", ["tasks", "durations", "dependencies", "milestones", "who is responsible", "deadlines"]),
        ], "A work plan should include contingency time because estimates are never exact and creative tasks in particular routinely take longer than expected, since the amount of revision required cannot be known in advance. Unexpected problems also occur on almost every project: equipment fails, a location becomes unavailable, a contributor is ill or the client requests a change part way through. If every task is scheduled back to back with no slack, then any single delay pushes back everything that follows and the final deadline is missed. Another essential element is the list of tasks themselves with their durations and dependencies, showing which tasks must be completed before others can begin and who is responsible for each, together with the milestones at which progress is reviewed. A Gantt chart presents this visually so that overlapping work and the critical path can be seen at a glance."),

        EQ("A logo must be used on a website with a coloured background and printed on large banners. Recommend suitable file formats and justify your recommendations.", 5, [
            MP("Recommends SVG as the scalable master format", ["svg", "vector", "scalable"]),
            MP("Because a vector can be enlarged to banner size with no loss of quality", ["no loss", "any size", "banner", "sharp", "enlarged"]),
            MP("Recommends PNG for the website", ["png"]),
            MP("Because PNG supports transparency so the logo sits on the coloured background", ["transparency", "transparent", "background"]),
            MP("Explains why JPG is unsuitable", ["jpg", "no transparency", "white box", "lossy", "artefacts"]),
        ], "The logo should be created and held as an SVG, which is a vector format storing the design as mathematical shapes rather than a fixed grid of pixels. This means it can be output at any size, from a browser tab icon to a banner several metres across, and redrawn perfectly sharp at every one, which no fixed resolution image could achieve. For the website a PNG export should also be supplied, because PNG is lossless and supports transparency, so the area around the letterforms allows the coloured background of the page to show through rather than sitting inside a solid rectangle. A JPG would be unsuitable for either purpose: it does not support transparency, so the logo would appear in a white box on the coloured background, and it uses lossy compression, which produces visible artefacts around the sharp edges of a logo, particularly noticeable when enlarged for print."),

        EQ("Explain the difference between RGB and CMYK, and state which should be used for a printed leaflet.", 4, [
            MP("RGB mixes red, green and blue light and is used for screens", ["rgb", "light", "screen", "display"]),
            MP("CMYK mixes cyan, magenta, yellow and black ink and is used for print", ["cmyk", "ink", "print"]),
            MP("The two produce different ranges of colour", ["different", "range", "gamut", "not the same"]),
            MP("CMYK should be used for the leaflet, otherwise colours will shift when printed", ["cmyk", "shift", "different", "duller", "not match"]),
        ], "RGB creates colour by mixing red, green and blue light and is the colour mode used by anything that emits light, so it is correct for screens, websites and video. CMYK creates colour by mixing cyan, magenta, yellow and black inks on paper and is the colour mode used for printing. The two produce different ranges of reproducible colour, and some vivid colours achievable with light simply cannot be reproduced with ink. A printed leaflet must therefore be prepared in CMYK. If it is designed in RGB and sent to a printer without conversion, the printing process will convert it automatically to the nearest available ink colours, and the result frequently looks noticeably duller or shifted, particularly in bright blues and greens, with the designer having had no opportunity to see or correct the change."),

        EQ("Describe two considerations that would affect how a video is prepared for distribution on social media.", 4, [
            MP("Aspect ratio must match the platform, often vertical for mobile", ["aspect ratio", "vertical", "9:16", "square", "platform"]),
            MP("Because users view on phones held vertically", ["phones", "vertical", "mobile", "held"]),
            MP("File size and duration limits imposed by the platform", ["file size", "duration", "limit", "length", "maximum"]),
            MP("Captions should be added because many users watch without sound", ["captions", "subtitles", "without sound", "muted", "accessibility"]),
        ], "The first consideration is aspect ratio and file specification. Each platform has its own requirements for aspect ratio, maximum duration and maximum file size, and a video that does not meet them will either be rejected or automatically cropped in a way the creator did not intend. Because most social media viewing happens on phones held vertically, a vertical or square format usually fills the screen far better than a widescreen export and performs noticeably better as a result. The second consideration is captions. A large proportion of social media video is watched with the sound off, particularly in public places, so a video that depends entirely on its audio will be scrolled past. Adding burned in captions or subtitles means the message still reaches those viewers, and it also makes the content accessible to people with hearing impairments, which is both good practice and increasingly expected."),

        EQ("Explain why a mood board is created during the planning of a media product.", 3, [
            MP("It collects images, colours, fonts and textures capturing the intended feel", ["images", "colours", "fonts", "textures", "feel", "collects"]),
            MP("It allows the designer and client to agree a visual direction before work begins", ["agree", "client", "direction", "before", "shared"]),
            MP("It is far quicker and cheaper to change than finished work", ["quicker", "cheaper", "easier to change", "early", "less work"]),
        ], "A mood board gathers together images, colours, typefaces, textures and examples of existing work that capture the look and feel the product is aiming for, providing a visual reference for something very difficult to convey in words. Its purpose is to establish a shared understanding between designer and client before any production work starts, because a client asking for something modern and a designer hearing that word may have entirely different images in mind. Discovering and resolving that disagreement over a mood board takes an afternoon, whereas discovering it after two weeks of finished artwork means starting again, so the mood board significantly reduces both the risk and the cost of the project."),

        EQ("A production company is filming on location in a public park. Describe two things they must arrange before filming, and explain why each is necessary.", 4, [
            MP("A risk assessment identifying hazards and control measures", ["risk assessment", "hazards", "control measures", "health and safety"]),
            MP("Because they have a legal duty to protect the crew and the public", ["legal duty", "protect", "safety", "harm", "responsible"]),
            MP("Permission from the landowner or local authority to film", ["permission", "landowner", "council", "authority", "permit", "licence"]),
            MP("And model release forms from any recognisable people appearing", ["model release", "release form", "permission", "recognisable", "appear"]),
        ], "First, the company must carry out a risk assessment before filming. This identifies the hazards present on the location, such as uneven ground, trailing cables, weather, water or members of the public moving through the shot, records who might be harmed by each and sets out the control measures put in place. This is necessary because the company has a legal duty of care towards its crew, its performers and the public, and without a documented assessment it has neither protected them properly nor any defence if an incident occurs. Second, the company must obtain permission to film from the landowner or the local authority responsible for the park, which usually means applying for a filming permit in advance. This is necessary because filming without consent may be trespass or may breach local by-laws, and the production could be stopped part way through with the loss of an entire day. They must also obtain model release forms from any recognisable individual appearing in the footage, since a person's image cannot be used commercially without their written permission."),
    ],
)

ALL_PAPERS = [J277_P1, J277_P2, H446_P1, H446_P2, R093_P1]
for _p in ALL_PAPERS:
    _p.marks = sum(q.marks for q in _p.questions)

# Durations are scaled from the real papers so the time pressure matches:
# J277 allows 90 minutes for 80 marks, H446 150 minutes for 140, R093 75 for 70.
_RATIO = {"J277/01 style": 1.125, "J277/02 style": 1.125,
          "H446/01 style": 1.071, "H446/02 style": 1.071, "R093 style": 1.071}
for _p in ALL_PAPERS:
    _p.minutes = int(round(_p.marks * _RATIO.get(_p.code, 1.1)))

# The Key Stage 3 end of unit assessments live in their own module because they
# are not written to a board specification, but they are ordinary papers as far
# as this page is concerned. They set their own marks and timings.
from content.ks3_papers import ALL_KS3_PAPERS  # noqa: E402
ALL_PAPERS = ALL_KS3_PAPERS + ALL_PAPERS


def _paper_page(paper):
    path = "/exam-papers/%s/" % paper.slug
    trail = [("Home", "/"), ("Exam papers", "/exam-papers/"), (paper.title, None)]

    qs = render.render_exam(paper.slug, paper.questions,
                            title="Questions",
                            lead="Write a full answer to every question, then mark the whole paper at the end. Marking as you go teaches you far less.",
                            heading_level="h2")

    body = """<div class="wrap">
  %s
  <div class="wrap-narrow" style="width:100%%;max-width:900px;margin-inline:auto">
    <header class="topic-header">
      <div class="badge-row">
        <span class="badge badge-spec">%s %s</span>
        <span class="badge">%s %d minutes</span>
        <span class="badge">%s %d marks</span>
        <span class="badge">%s Original paper</span>
      </div>
      <h1>%s</h1>
      <p class="lead">%s</p>
    </header>

    <div class="card" style="margin-bottom:var(--sp-5)">
      <div class="grid grid-2" style="gap:var(--sp-4);align-items:center">
        <div data-timer="%d">
          <h3 style="font-size:var(--step-1);margin-bottom:.4rem">Exam timer</h3>
          <p style="margin:0 0 .8rem;color:var(--ink-3);font-size:.92rem">Sit this to the clock. Working under time pressure is a separate skill from knowing the content, and it is the one most students never practise.</p>
          <div style="display:flex;align-items:center;gap:.8rem;flex-wrap:wrap">
            <span data-timer-face style="font-family:var(--font-mono);font-size:2rem;font-weight:700;color:var(--accent-strong)">00:00</span>
            <button class="btn btn-primary btn-sm" type="button" data-timer-btn>Start</button>
            <button class="btn btn-secondary btn-sm" type="button" data-timer-reset>Reset</button>
          </div>
        </div>
        <div>
          <h3 style="font-size:var(--step-1);margin-bottom:.4rem">Instructions</h3>
          <ul style="margin:0;font-size:.93rem;color:var(--ink-3);padding-left:1.2rem">
            <li>Answer <b>every</b> question.</li>
            <li>The marks tell you how many creditworthy points are wanted.</li>
            <li>%s</li>
            <li>%s</li>
          </ul>
        </div>
      </div>
    </div>

    %s

    <div class="note note-exam" style="margin-top:var(--sp-6)">
      <div class="note-title">%s About this paper</div>
      <p>This is an original paper written to match the structure, question style, command words and mark allocation of the real %s %s assessment. It is not a past paper. Real past papers are the copyright of the exam board and cannot be republished here, so links to the official papers on the board's own site are provided on the <a href="/exam-papers/">exam papers page</a>.</p>
    </div>
  </div>
</div>""" % (crumbs(trail), esc(paper.board), esc(paper.code), ico("i-clock"), paper.minutes,
             ico("i-paper"), paper.marks, ico("i-pen"), esc(paper.title), esc(paper.blurb),
             paper.minutes, esc(paper.calculator), esc(paper.advice), qs,
             ico("i-info"), esc(paper.board), esc(paper.code))

    ld = [crumbs_ld(trail), {
        "@context": "https://schema.org", "@type": "LearningResource",
        "name": paper.title, "description": paper.blurb,
        "url": SITE_URL + path, "learningResourceType": "Practice examination",
        "educationalLevel": paper.course, "inLanguage": "en-GB",
        "isAccessibleForFree": True,
    }]
    greeting = ("Sit this one properly. Timer on, no notes, every question answered. "
                "Ninety minutes done honestly teaches you more than a week of rereading.")
    return path, layout(title=paper.title,
                        description=paper.blurb,
                        path=path, body=body, active="/exam-papers/",
                        greeting=greeting, jsonld=ld,
                        scripts=["/assets/js/quiz.js"], show_progress=True)


def build(register, add_search, *_):
    cards = []
    ks3_cards = []
    for p in ALL_PAPERS:
        path, html = _paper_page(p)
        write(path, html)
        register(path, 0.8, "monthly")
        add_search(p.title, path, "%s practice paper, %d marks" % (p.board, p.marks),
                   (p.title + " " + p.course + " " + p.blurb).lower())
        (ks3_cards if p.course == "Key Stage 3" else cards).append(
            '<a class="tile" href="%s">'
            '<span class="tile-icon">%s</span><h3>%s</h3><p>%s</p>'
            '<span class="tile-meta"><span>%d marks</span><span>%d minutes</span><span>%s</span></span></a>'
            % (path, ico("i-paper"), esc(p.title), esc(p.blurb),
               p.marks, p.minutes, esc(p.board + " " + p.code)))

    links = "".join(
        '<li><a href="%s" target="_blank" rel="noopener">%s %s</a></li>' % (url, esc(name), ico("i-external"))
        for name, url in OFFICIAL)

    body = """<div class="wrap">%s</div>
<section class="hero"><div class="wrap">
  <div class="hero-grid">
    <div>
      <span class="eyebrow">%s Practice papers</span>
      <h1>Sit a full paper. Mark it honestly.</h1>
      <p class="lead">Original full length papers written to match the real format exactly, each with a built in timer,
      a complete mark scheme and a model answer for every question. Doing one properly teaches you more in ninety
      minutes than a week of rereading notes.</p>
    </div>
    <div class="stat-row">
      <div class="stat"><b>%d</b><span>Papers</span></div>
      <div class="stat"><b>%d</b><span>Questions</span></div>
      <div class="stat"><b>%d</b><span>Marks to practise</span></div>
      <div class="stat"><b>Free</b><span>No sign up</span></div>
    </div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head">
    <h2>GCSE and A Level papers</h2>
    <p>Each one is timed to the same marks per minute as the real assessment, so the pressure is genuine.</p>
  </div>
  <div class="grid grid-2">%s</div>
</div></section>

<section class="section section-alt"><div class="wrap">
  <div class="section-head">
    <h2>Key Stage 3 end of unit assessments</h2>
    <p>Two assessment points a year across Years 7, 8 and 9, written in the same style as a GCSE paper
    so that the format is completely familiar long before it counts.</p>
  </div>
  <div class="grid grid-2">%s</div>
</div></section>

<section class="section section-alt"><div class="wrap">
  <div class="grid grid-2" style="gap:var(--sp-6)">
    <div class="col-block">
      <h2 style="font-size:var(--step-2)">Why these are original papers</h2>
      <p style="color:var(--ink-3)">Real past papers belong to the exam boards and are protected by copyright, so they
      cannot lawfully be republished on this site. Every paper here is instead written from scratch to match the real
      thing on the measures that matter: the structure, the balance of topics, the command words, the mark allocations
      and the timing. Each comes with a full mark scheme written in the same style as a real one, plus a model answer,
      so you can mark your own work properly.</p>
      <p style="color:var(--ink-3);margin-bottom:0">Use these alongside the official past papers, not instead of them.
      The official papers are free to download from each board's own website.</p>
    </div>
    <div class="col-block">
      <h2 style="font-size:var(--step-2)">Official past papers</h2>
      <p style="color:var(--ink-3)">Download the genuine past papers and mark schemes directly from the exam board:</p>
      <ul class="checklist">%s</ul>
      <p class="muted" style="font-size:.86rem;margin-top:var(--sp-3);margin-bottom:0">These links go to the exam board's own
      website and open in a new tab. Some materials, particularly recent Cambridge National papers, are held on the
      board's secure teacher portal and your teacher will be able to access them for you.</p>
    </div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head">
    <h2>How to get the most out of a paper</h2>
    <p>Most students do papers badly, and then wonder why doing lots of them did not help.</p>
  </div>
  <div class="journey">
    <div class="journey-step"><div class="journey-dot">1</div><div class="journey-body">
      <h3>Do it in one sitting, timed, with no notes</h3>
      <p>Stopping to look something up turns an exam into an open book exercise. If you cannot answer it, leave a gap and move on, exactly as you would in May.</p></div></div>
    <div class="journey-step"><div class="journey-dot">2</div><div class="journey-body">
      <h3>Mark it against the mark scheme, not against your feelings</h3>
      <p>Award a mark only where you actually made the point. Being generous to yourself now costs you real marks later.</p></div></div>
    <div class="journey-step"><div class="journey-dot">3</div><div class="journey-body">
      <h3>Write down every mark you dropped and why</h3>
      <p>Not the question, the reason. Did you not know it, misread the command word, run out of time, or know it but fail to say it clearly? Each of those needs a different fix.</p></div></div>
    <div class="journey-step"><div class="journey-dot">4</div><div class="journey-body">
      <h3>Revise from that list, not from the specification</h3>
      <p>Your dropped marks are your revision plan. Going back to page one and reading everything again is comfortable and almost useless.</p></div></div>
    <div class="journey-step"><div class="journey-dot">5</div><div class="journey-body">
      <h3>Redo the questions you got wrong, a week later</h3>
      <p>Not the whole paper. Just those questions, from memory. If you can now answer them fully, the gap is genuinely closed.</p></div></div>
  </div>
</div></section>""" % (
        crumbs([("Home", "/"), ("Exam papers", None)]),
        ico("i-paper"), len(ALL_PAPERS),
        sum(len(p.questions) for p in ALL_PAPERS),
        sum(p.marks for p in ALL_PAPERS),
        "".join(cards), "".join(ks3_cards), links)

    ld = [crumbs_ld([("Home", "/"), ("Exam papers", None)])]
    write("/exam-papers/", layout(
        title="Practice Exam Papers",
        description="Original full length practice papers for OCR GCSE Computer Science J277, OCR A Level H446 and Creative iMedia R093, each with a timer, a complete mark scheme and model answers, plus links to the official past papers.",
        path="/exam-papers/", body=body, active="/exam-papers/",
        greeting="Papers are where revision turns into marks. Pick one, set the timer, and do it properly with no notes.",
        jsonld=ld))
    register("/exam-papers/", 0.9, "monthly")
    add_search("Practice exam papers", "/exam-papers/",
               "Original full papers with mark schemes",
               "exam papers past papers practice mark scheme timed j277 h446 r093")
