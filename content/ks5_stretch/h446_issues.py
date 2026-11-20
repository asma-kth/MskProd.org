"""OCR H446 1.5 Legal, moral, cultural and ethical issues: stretch tasks."""
from mskbuild.models import Blitz, Written, Stretch, MP, Pick, Pair, Sort, SortItem

COURSE = "ks5"

LESSONS = [
    Stretch(
        lesson="legal-moral-and-ethical-issues",
        blitz=[
            Blitz("Which act makes spreading malware to impair a computer an offence?",
                  options=["Computer Misuse Act 1990", "Data Protection Act 2018",
                           "Copyright, Designs and Patents Act 1988", "Regulation of Investigatory Powers Act 2000"],
                  explain="Its third offence covers unauthorised acts intended to impair a computer, which includes "
                          "malware and denial of service attacks."),
            Blitz("Which right lets a person ask an organisation to delete their personal data?",
                  options=["Erasure", "Portability", "Rectification", "Restriction"],
                  explain="The right to erasure is one of the rights the Data Protection Act 2018 gives individuals. "
                          "Rectification corrects data and portability moves it."),
            Blitz("Copyright arises automatically, but a patent must be applied for.", kind="tf", answer=True,
                  explain="Copyright protects the expression of an idea from the moment it is made. A patent protects an "
                          "invention and has to be granted."),
            Blitz("Which act governs the interception of communications by public bodies?",
                  options=["Regulation of Investigatory Powers Act 2000", "Freedom of Information Act 2000",
                           "Wireless Telegraphy Act 2006", "Computer Misuse Act 1990"],
                  explain="It sets when surveillance is allowed and when providers can be made to help."),
            Blitz("Which THREE are offences under the Computer Misuse Act 1990?", kind="multi", n=3,
                  options=["Unauthorised access to computer material",
                           "Unauthorised access with intent to commit further offences",
                           "Unauthorised acts that impair a computer's operation", "Copying music without permission",
                           "Keeping personal data for too long"],
                  explain="Those are its three offences. Copying music falls under copyright law, and keeping data too "
                          "long under data protection law."),
            Blitz("What does an open source licence let users do?",
                  options=["View, modify and redistribute the source code", "Only run the compiled program",
                           "Sell the software as their own with no conditions", "Use the software for one year"],
                  explain="Some open licences add copyleft, so changed versions must stay open too."),
            Blitz("Which ethical framework judges an action by its outcomes?",
                  options=["Consequentialism", "Deontology", "Virtue ethics"],
                  explain="An action is justified if its total benefit outweighs its total harm."),
            Blitz("Deontology says an action is right whenever its benefits outweigh its harms.", kind="tf",
                  answer=False,
                  explain="That is consequentialism. Deontology judges actions against duties and rights, whatever the "
                          "outcome."),
            Blitz("Which ethical framework asks what a person of good character would do?", kind="type",
                  accept=["virtue ethics", "virtue", "virtue theory", "virtue ethic"],
                  explain="Virtue ethics focuses on honesty, responsibility and care."),
            Blitz("Put the parts of a strong extended answer in order.", kind="order",
                  options=["One sentence of context", "Three developed paragraphs", "A conclusion that decides"],
                  explain="Context first, then developed arguments with counterpoints, then a judgement with a reason."),
            Blitz("Why can an algorithm trained on historical data be unfair?",
                  options=["It can repeat the bias in that data while appearing objective",
                           "Computers cannot store historical data", "Algorithms always favour the newest data",
                           "Training removes every pattern from the data"],
                  explain="Past decisions carry past bias, and a computer's answer looks neutral, which hides it."),
            Blitz("What is the digital divide?",
                  options=["The gap between people with reliable access to technology and those without",
                           "The split between hardware and software",
                           "The difference between analogue and digital signals", "The border between two networks"],
                  explain="Moving services online can exclude the people who depend on them most."),
        ],
        short=[
            Written("Explain the difference between copyright and a patent.", 2, [
                MP("Copyright arises automatically and protects the expression of an idea",
                   ["automatic", "automatically", "expression", "no need to apply"]),
                MP("A patent protects an invention and must be applied for",
                   ["applied for", "apply", "application", "registered", "invention", "granted"]),
            ], "Copyright arises automatically and protects the expression of an idea, while a patent protects an "
               "invention and must be applied for.",
               command="Explain"),
            Written("Explain why naming an ethical framework improves an extended answer.", 2, [
                MP("It turns an opinion into a reasoned argument",
                   ["argument", "rigorous", "reasoned", "reasoning", "not just an opinion", "justify", "justified"]),
                MP("Which is what the top mark band requires",
                   ["top band", "top level", "higher band", "more marks", "levels", "mark band"]),
            ], "Applying a framework such as consequentialism turns an opinion into a reasoned argument, which is what "
               "the top mark band requires.",
               command="Explain"),
            Written("Describe what the Data Protection Act 2018 requires of organisations that hold personal data.", 2, [
                MP("Data must be processed lawfully, fairly and transparently",
                   ["lawfully", "lawful", "fairly", "transparent", "transparently"]),
                MP("It must be collected for a specified purpose and limited to what is necessary",
                   ["specified purpose", "purpose", "necessary", "adequate", "limited"]),
                MP("It must be kept accurate", ["accurate", "up to date"]),
                MP("It must not be kept longer than necessary",
                   ["no longer", "longer than", "deleted", "kept too long"]),
                MP("It must be kept secure", ["secure", "security"]),
                MP("Serious breaches must be reported within 72 hours", ["72 hours", "breach", "breaches"]),
            ], "Personal data must be processed lawfully, fairly and transparently, collected only for a specified "
               "purpose, kept accurate and secure, and not kept for longer than necessary.",
               command="Describe"),
            Written("Give two reasons why automation can harm some workers even when it creates new jobs.", 2, [
                MP("The new jobs need different skills",
                   ["different skills", "new skills", "retrain", "retraining", "qualifications"]),
                MP("The new jobs are in different places",
                   ["different places", "elsewhere", "other areas", "different areas", "other places", "move",
                    "location"]),
                MP("The costs and the benefits fall on different people",
                   ["different people", "lose their jobs", "lost their jobs", "unemployed", "unemployment"]),
            ], "The new jobs often need different skills that the workers who lost their jobs do not have, and they are "
               "often in different places, so the costs and benefits fall on different people.",
               command="Give"),
        ],
        long=[
            Written("A company uses software to monitor every keystroke made by staff working from home. Discuss the "
                    "legal and ethical issues.", 6, [
                MP("Under the Data Protection Act 2018, monitoring must be lawful, proportionate and transparent",
                   ["data protection", "lawful", "proportionate", "transparent", "consent"]),
                MP("Covert logging is likely to be unlawful, so staff must be told",
                   ["covert", "secret", "secretly", "without telling", "disclosed", "told"]),
                MP("The employer has a legitimate interest in checking work is done",
                   ["legitimate", "productivity", "checking work", "work is being done", "right to check"]),
                MP("Staff have a right to privacy in their own homes", ["privacy", "private"]),
                MP("It captures personal activity such as messages, banking and medical searches",
                   ["messages", "banking", "medical", "personal"]),
                MP("Names and applies an ethical framework",
                   ["deontology", "deontological", "consequentialism", "consequentialist", "virtue"]),
                MP("It can damage trust and morale", ["trust", "morale", "stress", "anxiety", "relationship"]),
                MP("Reaches a reasoned conclusion", ["conclusion", "in conclusion", "overall", "on balance",
                                                     "therefore"]),
            ], "Under the Data Protection Act 2018, monitoring must be lawful, proportionate and transparent, so covert "
               "keystroke logging would almost certainly be unlawful and staff must be told. The employer has a "
               "legitimate interest in checking that work is being done, but staff have a reasonable expectation of "
               "privacy in their own homes, and keystroke logging also captures private messages, banking and medical "
               "searches. A deontological view says this breaches a right to privacy whatever the productivity gain, "
               "while a consequentialist view must weigh the gain against the damage to trust and morale. On balance "
               "the monitoring is not justified unless it is disclosed and limited to what is genuinely necessary.",
               command="Discuss",
               frame=["Legally", "The employer could argue", "Ethically, a", "On balance"]),
            Written("Explain the ethical issues raised when algorithms make decisions about people, such as who is "
                    "offered a loan.", 4, [
                MP("Training on historical data can repeat historical bias",
                   ["bias", "biased", "historical", "past data", "training data", "discrimination", "discriminate"]),
                MP("A computer's decision appears objective, which hides the unfairness",
                   ["objective", "neutral", "trusted", "seems fair", "hidden"]),
                MP("Nobody may be able to explain the decision, so accountability is unclear",
                   ["accountable", "accountability", "explain", "explanation", "responsible", "responsibility",
                    "black box"]),
                MP("Names a specific group that could be harmed",
                   ["minority", "minorities", "group", "groups", "postcode", "women", "ethnic"]),
                MP("Counterpoint: an algorithm can be more consistent than people",
                   ["consistent", "consistently", "human bias", "humans are biased"]),
            ], "An algorithm trained on historical lending data can repeat the bias in that data, so groups refused loans "
               "in the past may keep being refused. Because the decision comes from a computer it appears objective, "
               "which hides the unfairness. If nobody can explain why the system decided as it did, it is unclear who "
               "is accountable and the applicant cannot challenge it. On the other hand, an algorithm applies its rules "
               "consistently, which can be fairer than human judgement if the data is checked for bias.",
               command="Explain",
               frame=["The training data", "Because a computer decides", "If nobody can explain",
                      "On the other hand"]),
        ],
        picks=[
            Pick("A student guesses a teacher's password and reads their files. Which act is broken?",
                 "Computer Misuse Act 1990", "Copyright, Designs and Patents Act 1988",
                 "Unauthorised access to computer material is the first offence under the Computer Misuse Act."),
            Pick("Which has to be applied for?",
                 "A patent", "Copyright",
                 "Copyright exists as soon as the work is made. An invention must be granted a patent."),
            Pick("A website keeps customers' data for years after they leave. Which act does this break?",
                 "Data Protection Act 2018", "Freedom of Information Act 2000",
                 "Personal data must not be kept for longer than necessary. The Freedom of Information Act is about "
                 "information held by public bodies."),
            Pick("Which framework says reading private messages without consent is wrong even if it does good?",
                 "Deontology", "Consequentialism",
                 "Deontology judges actions against duties and rights, whatever the outcome."),
            Pick("Using a neighbour's wifi without permission breaks which act?",
                 "Wireless Telegraphy Act 2006", "Data Protection Act 2018",
                 "Unauthorised use of a wireless network is an offence under the Wireless Telegraphy Act."),
            Pick("Which licence lets you change the source code and share it?",
                 "Open source", "Proprietary",
                 "Proprietary licences only let users run the compiled program."),
            Pick("Which reaches the top band in a levels marked answer?",
                 "Three developed points and a conclusion", "Eight brief points with no conclusion",
                 "Development, balance and a supported conclusion reach the top band. A list of assertions stays in the "
                 "bottom one."),
            Pick("Which act lets you request information held by a public authority?",
                 "Freedom of Information Act 2000", "Data Protection Act 2018",
                 "The Freedom of Information Act covers public authorities. The Data Protection Act lets you see the "
                 "personal data held about you."),
        ],
        pairs=[
            Pair("Consequentialism", "Judge an action by its outcomes"),
            Pair("Deontology", "Judge an action against duties and rights"),
            Pair("Virtue ethics", "What would a person of good character do?"),
            Pair("Digital divide", "Gap between people with and without access"),
            Pair("Algorithmic bias", "Unfair decisions inherited from training data"),
            Pair("Open source", "Source code you may view, change and share"),
        ],
        pair_names=("Term", "Meaning"),
        sort=Sort(
            prompt="Which act does each situation fall under?",
            bins=["Computer Misuse Act", "Data Protection Act", "Copyright Act"],
            items=[
                SortItem("Guessing a colleague's password to read their email", 0,
                         "Unauthorised access to computer material is a Computer Misuse Act offence."),
                SortItem("Launching a denial of service attack on a website", 0,
                         "Impairing the operation of a computer is the act's third offence."),
                SortItem("Spreading ransomware to lock a company's files", 0,
                         "Deliberately spreading malware is covered by the Computer Misuse Act."),
                SortItem("Hacking into a system to steal card details", 0,
                         "Unauthorised access with intent to commit a further offence is the act's second offence."),
                SortItem("A shop keeps customers' details long after they leave", 1,
                         "Personal data must not be kept for longer than necessary."),
                SortItem("A company loses an unencrypted laptop full of patient records", 1,
                         "Personal data must be kept secure."),
                SortItem("A customer asks for their data to be deleted", 1,
                         "The right to erasure comes from the Data Protection Act."),
                SortItem("Selling customer emails to another firm without consent", 1,
                         "Personal data must be processed lawfully and only for a specified purpose."),
                SortItem("Sharing a film online without permission", 2,
                         "Films are protected by copyright."),
                SortItem("Copying a game and selling the copies", 2,
                         "Software is protected by the Copyright, Designs and Patents Act."),
                SortItem("Using a photo from a website in an advert without permission", 2,
                         "The photographer owns the copyright in the photo."),
                SortItem("Installing software on more computers than the licence allows", 2,
                         "Breaking the terms of a software licence is a copyright matter."),
            ]),
    ),
]
