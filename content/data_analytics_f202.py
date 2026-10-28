"""F202 Spreadsheet data modelling: the non-examined unit of Data Analytics.

F202 is mandatory in both the Certificate (H019) and the Extended Certificate
(H119). It is 75 guided learning hours, 15 of them for completing an OCR-set
assignment that the centre marks and OCR moderates. The five topic areas
follow OCR's published unit structure:

  TA1  Principles of spreadsheet modelling
  TA2  Planning the design of a spreadsheet model
  TA3  Creating the spreadsheet model
  TA4  Delivering the outcomes
  TA5  Evaluation

followed by a guide to the assignment itself: how it is assessed, what to
produce at each stage, and the rules about doing it independently.

Because this is coursework, there is no paper to practise for. The written
questions are headed "Check you could explain this", and every worked example
uses one invented brief, the Harbour Lights festival ticket model, which is
deliberately nothing like any OCR set assignment. The examples show the
quality of each piece of evidence; they never answer anybody's real brief.
The figures in the text come from the same model as the diagrams in
mskbuild/diagrams_f202.py, so the two cannot disagree.

Set assignments are replaced over time, so the pages tell students to check
the current assignment and specification with their teacher.
"""
from mskbuild.models import Topic, Section, Q, EQ, MP

OCR_PAGE = ("https://www.ocr.org.uk/qualifications/cambridge-advanced-nationals/"
            "it-data-analytics-level-3-h019-h119/")
OCR_SPEC = ("https://www.ocr.org.uk/Images/697580-specification-cambridge-advanced-"
            "national-in-it-data-analytics.pdf")

NEA = "Check you could explain this"

# ============================================================== F202 TA1

F_PRINCIPLES = Topic(
    slug="spreadsheet-modelling-principles",
    title="F202 TA1: Principles of Spreadsheet Modelling",
    spec="F202 TA1",
    icon="i-grid",
    minutes=30,
    exam_title=NEA,
    blurb="What a spreadsheet model is, what organisations use models for, when a spreadsheet is the right tool, and the features you will build with.",
    fact="The first spreadsheet program for personal computers, VisiCalc, came out in 1979 for the Apple II. People bought the computer just to run it, which made it one of the first 'killer applications' in computing.",
    sections=[
        Section("What a spreadsheet model is", """
A **spreadsheet model** is a simplified version of a real situation, built from numbers and formulas, so that you can ask what happens when something changes. A table of last year's sales is not a model: it records what happened. A sheet where you type next year's price and read off next year's profit is a model, because the outputs are calculated from inputs you can change.

### The parts of every model

| Part | What it is | Example |
| **Input variable** | A value the user is expected to change, to explore a question | The ticket price |
| **Assumption** | A value the model takes as true, which may turn out to be wrong | 600 people would come if it were free, and 12 fewer come for every £1 on the price |
| **Constant** | A value that does not change while the model is in use | The licensed capacity of 400 people |
| **Process** | A formula that turns inputs into results | Tickets sold, revenue, costs |
| **Output** | A result the client reads and acts on | Profit, the break-even price, a chart |

The worked example used across this unit is invented, and deliberately unlike any OCR brief: **Harbour Lights**, a one-day community music festival deciding what to charge for a ticket. A survey of local residents suggests demand of `600 − 12 × price`. The field is licensed for 400 people. Each attendee costs £5 in wristbands, toilets and security, and the stage, the licence and the insurance cost £4,000 whatever happens.

!diagram f202-model-ipo

!key Garbage in, garbage out :: A model calculates perfectly from whatever it is given. If the demand assumption is wrong, every output is wrong with complete precision. That is why each assumption needs a source you can name, and why evaluating a model means questioning its assumptions as well as checking its formulas.

### Modelling vocabulary

- **What-if analysis**: changing an input to see the effect on the outputs.
- **Goal seeking**: working backwards from the output you want to the input that produces it.
- **Scenario**: a named set of input values, such as pessimistic, expected and optimistic.
- **Sensitivity analysis**: changing one assumption a little at a time to see how much the result depends on it.
- **Forecast**: using the model to predict a future value, such as next month's bank balance.
- **Optimisation**: finding the input that gives the best output, such as the price that makes the most profit, often within limits.
"""),
        Section("What models are used for", """
!diagram f202-model-uses

| Organisation | Question | What the model does |
| A sports club | Can we afford a new minibus? | A cash flow forecast, with the loan repayment worked out by `PMT` |
| A school | What must a trip cost so every expense is covered? | Break-even on the number of students who sign up |
| A café | What happens to profit if milk goes up 20%? | What-if analysis on one cost |
| A charity | How many volunteers do we need on each shift? | A staffing model driven by expected visitors |
| A small online shop | When must we reorder each product? | Stock levels, lead times and reorder points |
| An event organiser | Which ticket price makes the most profit? | Demand that changes with price, plus scenarios |

### Who uses a model, and why that matters

The person who **builds** a model is usually not the person who **uses** it. The client may be a manager who only reads the dashboard. The end users may be volunteers who type the inputs and are not confident with spreadsheets. A model is designed for the people who will use it, which is why planning in TA2 starts with the client and the users rather than with the formulas.
"""),
        Section("Spreadsheets: strengths, limits and risks", """
### Why a spreadsheet

- **Immediate recalculation**: change one cell and everything that depends on it updates, which is exactly what what-if analysis needs.
- **Flexible and quick to build**: a working model can exist in an afternoon.
- **Familiar**: most clients already have spreadsheet software and know the basics.
- **Built-in tools**: functions, charts, validation, Goal Seek, scenarios, pivot tables and macros, with no programming environment to install.
- **Transparent**: a user can click any cell and see the formula behind it.

### When a spreadsheet is the wrong tool

| Need | Better tool | Why |
| Millions of records, edited by many users at once | A database | Integrity rules, controlled access, no practical row limit |
| The same processing of large data, repeated exactly | Python or R | Code can be tested, version controlled and re-run |
| Live reports for a whole organisation | A business intelligence tool such as Power BI or Tableau | Live data connections, permissions, shared dashboards |
| A calculation that must never be altered | A program or a locked system | Somebody can always edit a spreadsheet |

An Excel worksheet holds at most 1,048,576 rows and 16,384 columns, and the older `.xls` format only 65,536 rows. Limits like these are invisible until the day the data is bigger than they are.

### Spreadsheet risk is real

Errors in spreadsheets are common, quiet and expensive, because a wrong formula still produces a confident-looking number.

- In 2020, almost 16,000 positive COVID-19 test results in England were left out of the daily figures, because data was being handled in the old `.xls` format and ran out of rows.
- A widely cited 2010 economics paper on government debt and growth was found in 2013 to contain a spreadsheet error: an average had been calculated over the wrong range of rows, leaving countries out.
- In 2020 scientists renamed a set of human genes, such as MARCH1 and SEPT1, because spreadsheet software kept converting the names into dates.

!warn A number that looks right is not a number that is right :: Every one of those errors produced a believable result. The defence is the same each time: plan the expected results before building, test with data you have worked out by hand, and keep inputs, calculations and outputs where they can be checked.
"""),
        Section("The features you will build with", """
| Feature | What it is for | Example in the festival model |
| **Cell reference** | Using a value from another cell, so it is stored once | `=B3*B10` |
| **Absolute reference** | A reference that must not move when the formula is copied | `=A2*$F$1` |
| **Named range** | A meaningful name for a cell or range | `TicketPrice`, `Capacity` |
| **Formula** | A calculation you write | `=Revenue-TotalCosts` |
| **Function** | A built-in calculation | `SUM`, `MIN`, `IF`, `XLOOKUP` |
| **Data validation** | Restricting what can be entered | The price must be from £5 to £60 |
| **Conditional formatting** | Formatting that changes with the value | Profit turns red below zero |
| **Lookup** | Finding a value in a table | The price of a Concession ticket |
| **Chart** | Showing a pattern visually | Profit against price |
| **Pivot table** | Summarising a long list | Tickets sold by type |
| **What-if tools** | Goal Seek, Scenario Manager, data tables | The price that gives a £1,000 profit |
| **Macro** | Automating a sequence of steps | A button that runs Goal Seek |
| **Protection** | Stopping cells from being changed | Formulas locked, inputs open |
| **Sort and filter** | Putting a list in order, or showing part of it | The bookings for one date |
| **Freeze panes** | Keeping headings visible while scrolling | The header row of a long list |

!diagram f202-cell-references

### Data types and formats

| Type | Stored as | Shown as |
| Number | A value | `400`, `1,250.5` |
| Currency | A number with a currency format | `£27.50` |
| Percentage | A fraction, displayed multiplied by 100 | `0.1` shown as `10%` |
| Date and time | A serial number counting days from a starting date | `14/06/2026`, `19:30` |
| Text | Characters | `Concession`, `HL-2026-0047` |
| Boolean | TRUE or FALSE | The result of `=B3>=5` |

!key Formatting changes what you see, not what is stored :: A cell showing £27.50 may hold 27.4999. Add up a column of cells like that and the total can be a penny different from the values on screen. Where money has to add up exactly, use `ROUND` in the formula rather than relying on the format.
"""),
        Section("Sources and further reading", """
- [OCR Cambridge Advanced National in IT: Data Analytics (H019, H119)](%s): the qualification page, with the specification and assessment materials.
- [The H019 and H119 specification (PDF)](%s): F202's content, topic area by topic area. Check that your version matches.
- [Microsoft Excel help and learning](https://support.microsoft.com/en-us/excel): official guidance on every function and tool.
- [Google Sheets function list](https://support.google.com/docs/table/25273): every Sheets function, with examples.
- [LibreOffice Help](https://help.libreoffice.org/): documentation for LibreOffice Calc, a free alternative.
- [GCF Global Excel tutorials](https://edu.gcfglobal.org/en/excel/): free step-by-step lessons, from the basics upwards.
- [European Spreadsheet Risks Interest Group](https://eusprig.org/): research into spreadsheet errors and how to prevent them.
""" % (OCR_PAGE, OCR_SPEC)),
    ],
    keyterms=[
        ("Spreadsheet model", "A simplified version of a real situation, built from inputs, formulas and outputs, used to ask what happens when something changes."),
        ("Input variable", "A value the user is expected to change in order to explore a question."),
        ("Assumption", "A value the model treats as true, which may later prove to be wrong."),
        ("Constant", "A value that stays fixed while the model is in use."),
        ("What-if analysis", "Changing one or more inputs to see the effect on the outputs."),
        ("Goal seeking", "Working backwards from a target output to the input value that produces it."),
        ("Scenario", "A named set of input values, such as pessimistic, expected and optimistic."),
        ("Sensitivity analysis", "Changing one assumption at a time to see how strongly the result depends on it."),
        ("Relative reference", "A cell reference that changes when the formula is copied."),
        ("Absolute reference", "A cell reference fixed with dollar signs, such as $F$1, so it does not change when copied."),
        ("Mixed reference", "A reference with only the column or only the row fixed, such as $A2 or B$1."),
        ("Named range", "A meaningful name given to a cell or range and used in formulas instead of its address."),
    ],
    grade="""
+ Use the vocabulary precisely: input variable, assumption, constant, process, output
+ Explain why a spreadsheet suits the client's problem, and say where it would not
+ Give every assumption a source the client could check
+ Name each feature and say what it does for this client, not just that you used it
+ Know the risks of spreadsheets and show how your design reduces them
""",
    mistakes=[
        "Calling any table of numbers a model. A model calculates its outputs from inputs you can change.",
        "Typing numbers into formulas, such as =B3*5, so an assumption is hidden where nobody can see or change it.",
        "Listing spreadsheet features with no explanation of what each one does for the client.",
        "Treating the model's output as fact, when it is only as good as its assumptions.",
        "Forgetting that formatting changes the display, not the stored value.",
        "Copying a formula without checking which references should have been absolute.",
    ],
    quiz=[
        Q("What makes a spreadsheet a model rather than a record?",
          ["Its outputs are calculated from inputs that can be changed",
           "It contains a chart", "It has more than one worksheet",
           "It uses colour formatting"], 0,
          "A model answers what-if questions: change an input and the outputs recalculate."),
        Q("In the festival model, 'demand falls by 12 people for every £1' is:",
          ["An assumption", "An output", "A constant", "A macro"], 0,
          "It is taken as true for the model and could turn out to be wrong, so it needs a source."),
        Q("Which tool works backwards from a target output to the input that achieves it?",
          ["Goal Seek", "Conditional formatting", "A pivot table", "Data validation"], 0,
          "Goal Seek changes one input until the formula cell reaches the value you set."),
        Q("C2 contains =A2*$F$1. What does it become when filled down to C3?",
          ["=A3*$F$1", "=A3*$F$2", "=A2*$F$1", "=B3*$F$1"], 0,
          "The relative A2 moves down a row; the absolute $F$1 stays where it is."),
        Q("Why is a named range such as CostPerHead better than $F$1 in a formula?",
          ["It makes the formula readable, and it is absolute already",
           "It calculates faster", "It hides the value from the user",
           "It stops the cell being edited"], 0,
          "=TicketsSold*CostPerHead explains itself. =B10*$F$1 does not."),
        Q("A cell shows £27.50 but holds 27.4999. What is happening?",
          ["The format rounds the display, not the stored value",
           "The cell is corrupted", "The formula has an error",
           "The currency symbol changed the value"], 0,
          "Formatting changes what you see. Use ROUND when stored values must be exact."),
        Q("Which need points to a database rather than a spreadsheet?",
          ["Millions of records edited by many users at once",
           "A quick what-if model for one manager",
           "A chart of monthly sales", "A break-even calculation"], 0,
          "A database enforces integrity and controls access for many users at scale."),
        Q("What is sensitivity analysis?",
          ["Changing one assumption at a time to see how much the output depends on it",
           "Checking the spelling of labels", "Protecting a sheet with a password",
           "Sorting data into order"], 0,
          "It shows which assumptions matter most, and so which data needs checking hardest."),
        Q("Why did almost 16,000 COVID-19 results go missing from England's figures in 2020?",
          ["An old spreadsheet format ran out of rows",
           "A computer virus deleted them",
           "The formulas used relative references",
           "The results were stored as text"], 0,
          "The .xls format holds only 65,536 rows, and nothing warned anybody when the data passed that limit."),
        Q("Which reference keeps the column fixed but lets the row change?",
          ["$A2", "A$2", "$A$2", "A2"], 0,
          "The dollar sign fixes whatever it stands in front of: here, the column."),
    ],
    exam=[
        EQ("Explain the difference between an input variable and an assumption in a spreadsheet model. Use an example of each.", 4,
           [MP("An input variable is a value the user changes to explore a question", ["change", "user", "experiment", "explore", "vary", "what if"]),
            MP("A valid example of an input variable", ["price", "ticket price", "quantity", "order", "number of"]),
            MP("An assumption is a value taken as true that may be wrong or is an estimate", ["taken as true", "estimate", "may be wrong", "not certain", "assumed", "forecast"]),
            MP("A valid example of an assumption, ideally with its source", ["demand", "survey", "inflation", "growth", "cost per", "attendance"])],
           "An input variable is a value the user is expected to change in order to explore a question, such as the ticket price in a pricing model: the whole point of the model is to try different prices and compare the results. An assumption is a value the model takes as true for the purpose of the calculation, even though it is an estimate that may turn out to be wrong, such as the assumption that 12 fewer people will come for every pound added to the price. The difference matters because an assumption needs a source the client can check, here a survey of residents, and an evaluation has to question it, whereas an input variable is simply set by the user.",
           command="Explain"),
        EQ("Explain why named ranges and absolute references make a spreadsheet model more reliable.", 4,
           [MP("An absolute reference does not change when a formula is copied", ["does not change", "fixed", "copied", "dollar", "$", "pinned"]),
            MP("This prevents copied formulas pointing at the wrong or empty cells", ["wrong cell", "empty", "zero", "error", "mistake", "refers to"]),
            MP("A named range makes a formula readable or self-documenting", ["readable", "meaning", "understand", "explains", "check", "self"]),
            MP("Each value is stored once, so changing it updates every formula", ["once", "one place", "updates", "every formula", "change it", "consistent"])],
           "An absolute reference such as $F$1 stays fixed when a formula is copied, so a cost per head stored in one cell is used by every row; with a relative reference the copies would slide down to empty cells and silently calculate zero. A named range does the same job and adds meaning: =TicketsSold*CostPerHead can be read and checked as a sentence, whereas =B10*$F$1 has to be traced cell by cell, so errors are far easier to spot. Both mean each value is stored in exactly one place, so changing an assumption updates every formula that depends on it, with no copies left behind holding an old value.",
           command="Explain"),
        EQ("A small charity is deciding whether to plan its fundraising budget with a spreadsheet model or a database.\n\nJustify the use of a spreadsheet model, and describe one risk the charity must manage.", 6,
           [MP("A spreadsheet recalculates immediately, which suits what-if planning", ["recalculate", "what if", "change", "instantly", "automatically"]),
            MP("It is familiar, available and cheap for a small charity", ["familiar", "already", "cheap", "cost", "available", "no training"]),
            MP("It is quick and flexible to build and change", ["quick", "flexible", "easy to change", "build", "adapt"]),
            MP("The data volume is small, so a database's strengths are not needed", ["small", "few", "volume", "not millions", "one user", "not needed"]),
            MP("A risk: undetected errors, overwriting or version confusion", ["error", "overwrite", "version", "wrong formula", "accident", "copies"]),
            MP("How the risk is managed", ["test", "protect", "validation", "lock", "version control", "check", "hand calculation"])],
           "A spreadsheet model suits the charity because budget planning is a what-if problem: trustees want to see what happens if an event raises less than hoped or a grant is late, and a spreadsheet recalculates every total the moment an input changes. It is also software the charity already has and its volunteers already know, so it costs nothing and needs little training, and it can be built and adapted quickly as plans change during the year. A database would be the better choice for thousands of donor records edited by many people at once, but a budget is a few hundred figures used by one or two people, so its strengths would be wasted. The main risk is an undetected error: a formula that misses a row or a value typed over a formula still produces a believable total, and decisions would be made on it. The charity should manage that by testing the model against totals worked out by hand, validating the input cells, protecting every formula cell, and keeping one clearly named current version so nobody works from an old copy.",
           command="Justify"),
    ],
)

# ============================================================== F202 TA2

F_PLANNING = Topic(
    slug="planning-a-spreadsheet-model",
    title="F202 TA2: Planning the Design of a Spreadsheet Model",
    spec="F202 TA2",
    icon="i-pen",
    minutes=32,
    exam_title=NEA,
    blurb="Turning a client's problem into testable requirements, then designing the structure, the sheets, the data, the processing and the tests before a single formula is written.",
    fact="Field audits of real business spreadsheets, summarised by the researcher Raymond Panko, found errors in most of the spreadsheets examined. That is why professional modellers plan and test as carefully as programmers do.",
    sections=[
        Section("Understanding the client and the requirements", """
Every decision in a model should trace back to something the client needs. Before designing anything, find out:

| Question | Why it matters | Festival example |
| **Who is the client?** | The person whose decision the model supports | The festival committee's chair |
| **Who are the end users?** | They will type the inputs, so the design has to suit them | Three volunteers, none of them confident with spreadsheets |
| **What is the problem?** | The question the model must answer | "What should we charge, and how risky is it?" |
| **What are the inputs?** | Everything that varies or is assumed | Price, survey results, costs, capacity |
| **What are the outputs?** | What the client will read and act on | Profit, tickets sold, break-even price, a chart |
| **What are the constraints?** | Limits the solution must respect | It must run in the committee's spreadsheet software, and be ready by March |

### Requirements that can be tested

A requirement is only useful if you can later prove whether it was met. "The model should be easy to use" cannot be tested. "A volunteer can enter a new price and read the profit without help" can.

| Weak | Strong, and testable |
| Calculate the profit | R1. Calculate profit for any ticket price from £5 to £60, to the nearest penny |
| Show if it is good | R2. Show PROFIT in green or LOSS in red beside the profit figure |
| Compare options | R3. Compare pessimistic, expected and optimistic scenarios side by side, with a chart |
| Find the right price | R4. Find the price that gives a profit the committee types in |
| Safe | R5. Users can edit only the input cells; every formula is protected |
| Easy to use | R6. A volunteer can change the price, or find the price for a target profit, without help |

### Functional and non-functional requirements

- **Functional** requirements say what the model must **do**: calculate, look up, validate, compare, chart.
- **Non-functional** requirements say how **well** it must do it: how easy to use, how secure, how accessible, which software it must run in.

!key Number your requirements :: R1, R2, R3. Every design decision, every test and every paragraph of your evaluation can then point back to a numbered requirement, and whoever marks the work can follow the thread from the brief to the finished model.
"""),
        Section("Designing the structure and the sheets", """
### One job per sheet

!diagram f202-workbook-structure

Separating inputs, data, calculations and outputs is the most valuable design decision in a spreadsheet model. Inputs are in one place, so a user knows where to type. Calculations are in one place, so they can be checked and locked. Outputs are in one place, so the client reads them without wading through the workings.

### Designing each sheet

Sketch every sheet before building it, on paper or in a drawing tool. A good design shows:

- the **layout**: where each label, input, output and chart sits
- the **data types and formats**: currency, percentage, date
- which cells are **inputs**, and how each is validated
- the **colour scheme** and fonts, used consistently
- **navigation**: buttons or hyperlinks between sheets
- **annotations** explaining each choice and the requirement it meets

!diagram f202-input-sheet-mockup

### Design rules that prevent errors

- **No typed numbers inside formulas.** Every assumption lives in a labelled cell, and formulas refer to it.
- **One formula per column.** The same calculation is copied down, not rewritten row by row.
- **Units in every label.** "Fixed costs (£)", "Capacity (people)".
- **Consistent colour coding** for inputs, calculations and outputs, explained in a key.
- **Never colour alone.** The status shows the word PROFIT or LOSS as well as green or red, for users who cannot tell the colours apart.
- **A naming convention** for files, sheets and named ranges, decided before the first save: `festival-model-v03.xlsx`, `TicketPrice`.
"""),
        Section("Planning the data and the processing", """
### The data dictionary

A data dictionary describes every input and stored field before it exists, so building becomes a matter of following the plan.

| Name | Data type | Format | Validation | Example | Source |
| TicketPrice | Currency | £0.00 | Decimal, 5 to 60 | £27.50 | Entered by the user |
| DemandAtZero | Whole number | 0 | Whole number, 100 to 2,000 | 600 | Residents' survey, May |
| LostPerPound | Whole number | 0 | Whole number, 1 to 50 | 12 | Residents' survey, May |
| Capacity | Whole number | 0 | Whole number, 1 to 2,000 | 400 | Premises licence |
| CostPerHead | Currency | £0.00 | Decimal, 0 to 50 | £5.00 | Suppliers' quotes |
| FixedCosts | Currency | £#,##0 | Decimal, 0 to 50,000 | £4,000 | Suppliers' quotes |
| TicketType | Text | Text | List: Adult, Child, Concession, Family | Adult | Lookup table on the Data sheet |

### Where the data comes from

| Source | Example | What to check |
| **Primary**: collected for this purpose | The residents' survey | Was the sample big enough, and representative? |
| **Client records** | Last year's ticket sales | Is it complete, accurate and still relevant? |
| **Secondary**: published by someone else | Official statistics from the [ONS](https://www.ons.gov.uk/) or [data.gov.uk](https://www.data.gov.uk/) | Is it current, from a reliable publisher, and licensed for reuse? |

If the model holds information about identifiable people, such as names on a booking list, the UK GDPR and the Data Protection Act 2018 apply: collect only what the model needs, and keep it secure. The [ICO](https://ico.org.uk/) explains what that means in practice.

### Cleaning data before it goes in

Imported data is rarely ready to use. Plan how you will deal with duplicates, blanks, inconsistent spellings, numbers stored as text and dates in mixed formats, using tools such as Remove Duplicates, `TRIM`, Text to Columns and Find and Replace.

!diagram data-cleaning

### The processing plan

Describe every output in words, then as the formula you intend to write. Writing it in words first catches mistakes in the logic before they become mistakes in the brackets.

| Output | In words | Planned formula |
| TicketsSold | Demand at this price, but never more than the capacity | `=MIN(Capacity, DemandAtZero-LostPerPound*TicketPrice)` |
| Revenue | Tickets sold times the price | `=TicketsSold*TicketPrice` |
| TotalCosts | Fixed costs plus the cost of each attendee | `=FixedCosts+TicketsSold*CostPerHead` |
| Profit | Revenue minus total costs | `=Revenue-TotalCosts` |
| Status | PROFIT if profit is at least zero, otherwise LOSS | `=IF(Profit>=0,"PROFIT","LOSS")` |

Decisions with several outcomes are clearer as a flowchart than as a formula, and the flowchart belongs in the design: the nested IF diagram in TA3 is an example. Plan each **macro** as numbered steps too: what starts it, what it does, and what the user sees when it has finished.

!info Planning is allowed to be wrong :: The planned TicketsSold formula above has a flaw: a high price gives negative tickets. Testing finds it, and TA3 shows the fix. A plan that changes because a test caught something is evidence of a real process, so keep the original plan and record the change.
"""),
        Section("Planning the testing", """
Write the test plan **before** building, from the requirements, and work out every expected result by hand. Tests written after the build are shaped by what the model already does, so they can only confirm it.

### Types of test data

| Type | What it is | Festival example |
| **Normal** | Sensible data the model should accept and process | A price of £27.50 |
| **Boundary** | Values at the edge of what is allowed, on both sides of the limit | £5.00 and £60.00 accepted; £4.99 and £60.01 rejected |
| **Invalid** | The right type of data, outside the allowed range | A price of £75 |
| **Erroneous** | The wrong type of data altogether | A price of "twenty" |

### What to test, beyond the inputs

- every **formula**, against a result calculated by hand
- every **validation rule**, with data on both sides of its boundary
- every **lookup**, including a value that is not in the table
- every **macro** and button
- **protection**: try to type in a locked cell
- the **outputs**: do the chart and the dashboard update when an input changes?
- **usability**: can a real user complete a task without help? This is **user acceptance testing**.

!diagram f202-test-plan

!key What a test plan shows :: Test number, purpose, test data, type of data, expected result, actual result, and the action taken when a test fails. Planning tests you expect to be rejected, such as invalid and erroneous data, shows you understand testing rather than demonstrating that the model works.
"""),
        Section("Sources and further reading", """
- [The H019 and H119 specification (PDF)](%s): what TA2 covers. Check it against your version.
- [diagrams.net](https://app.diagrams.net/): a free tool for drawing sheet designs, flowcharts and structure diagrams.
- [Office for National Statistics](https://www.ons.gov.uk/) and [data.gov.uk](https://www.data.gov.uk/): reliable published data, most of it free to reuse under the Open Government Licence.
- [Information Commissioner's Office](https://ico.org.uk/): what data protection law requires if your model stores personal data.
- [WebAIM contrast checker](https://webaim.org/resources/contrastchecker/): check that the colours in your design are readable.
- [Microsoft Excel help and learning](https://support.microsoft.com/en-us/excel): how each feature you are planning to use works.
""" % OCR_SPEC),
    ],
    keyterms=[
        ("Client", "The person or organisation whose decision the model is built to support."),
        ("End user", "A person who will use the model day to day, such as entering inputs."),
        ("Functional requirement", "Something the model must do, such as calculate a value or validate an input."),
        ("Non-functional requirement", "How well the model must work, such as how easy, secure or accessible it is."),
        ("Data dictionary", "A table describing every field's name, data type, format, validation, example and source."),
        ("Processing plan", "A description of how each output is calculated, in words and as the intended formula."),
        ("Test plan", "A table of planned tests, each with its purpose, test data, type and expected result."),
        ("Normal data", "Sensible data that the model should accept and process correctly."),
        ("Boundary data", "Data at the edge of the allowed range, tested on both sides of each limit."),
        ("Invalid data", "Data of the right type but outside the allowed range, which should be rejected."),
        ("Erroneous data", "Data of the wrong type altogether, which should be rejected."),
        ("User acceptance testing", "Testing in which real users carry out tasks to confirm the model meets their needs."),
    ],
    grade="""
+ Number the requirements and make every one testable
+ Separate inputs, data, calculations and outputs, and explain why
+ Design every sheet, annotated with the requirement each feature meets
+ Complete a data dictionary with types, formats, validation and sources
+ Describe each output in words before writing it as a formula
+ Write the test plan before building, with expected results worked out by hand
""",
    mistakes=[
        "Requirements that cannot be tested, such as 'easy to use'.",
        "Designing only the dashboard and leaving the input and calculation sheets to chance.",
        "Designs with no annotation, so nobody can tell why any choice was made.",
        "A data dictionary without validation rules or sources.",
        "Test plans written after the build, with expected results copied from the model's own output.",
        "Testing only normal data, never the boundaries or invalid entries.",
    ],
    quiz=[
        Q("Which requirement can be tested?",
          ["A volunteer can change the price and read the profit without help",
           "The model should be easy to use", "The model should look professional",
           "The model should be good"], 0,
          "You can watch a volunteer try it and record whether they needed help."),
        Q("Which of these is a functional requirement?",
          ["The model must calculate the break-even price",
           "Only the input cells can be edited", "Text must have strong contrast",
           "It must run in the client's spreadsheet software"], 0,
          "A functional requirement says what the model does. The others say how well, or under what limits."),
        Q("Why separate inputs, calculations and outputs onto different sheets?",
          ["Users know where to type, and the calculations can be checked and locked",
           "It makes the file smaller", "Spreadsheet software requires it",
           "It hides the formulas from the client"], 0,
          "Each part is easier to use, test and protect when it has one place."),
        Q("What does a data dictionary record?",
          ["Each field's name, type, format, validation and source",
           "The result of every formula", "The client's contact details",
           "The test results"], 0,
          "It is the plan for the data, written before the data exists."),
        Q("The valid prices are £5 to £60. Testing with £60.00 uses:",
          ["Boundary data", "Invalid data", "Erroneous data", "Normal data"], 0,
          "It is the edge of the allowed range. £60.01 would be the boundary on the other side."),
        Q("Typing 'twenty' into the price cell is a test with:",
          ["Erroneous data", "Boundary data", "Normal data", "Extreme data"], 0,
          "It is the wrong type of data altogether, so it should be rejected."),
        Q("Why work out expected results by hand before testing?",
          ["Otherwise there is nothing independent to compare the model's output against",
           "It is faster than testing", "The spreadsheet cannot calculate them",
           "It avoids the need for test data"], 0,
          "Copying the model's own answer into the expected column tests nothing."),
        Q("Why should the status show the word PROFIT as well as a green fill?",
          ["So the meaning does not depend on colour alone",
           "Green cannot be printed", "Spreadsheets cannot colour text",
           "Words recalculate faster"], 0,
          "Some users cannot tell red from green. The word carries the meaning for everyone."),
        Q("Which is user acceptance testing?",
          ["The client's users try real tasks to confirm the model meets their needs",
           "The developer checks every formula",
           "The software checks for circular references",
           "Validation rejects bad data"], 0,
          "It tests whether the model works for the people it was built for."),
        Q("Where should an assumption such as cost per head be stored?",
          ["In its own labelled input cell that formulas refer to",
           "Typed into every formula that uses it", "In a cell comment",
           "In the file name"], 0,
          "Stored once and labelled, it can be seen, checked and changed in one place."),
    ],
    exam=[
        EQ("Explain why a test plan should be written before a spreadsheet model is built.", 3,
           [MP("Tests are based on the requirements, not on what the build happens to do", ["requirement", "brief", "not on the build", "what it should do", "independent"]),
            MP("Expected results are worked out independently, by hand", ["expected", "by hand", "calculate", "independent", "before"]),
            MP("Problems are found early, and invalid or boundary cases are planned in", ["early", "boundary", "invalid", "design", "cheaper", "planned"])],
           "A test plan written first is based on the requirements, so it checks what the model should do rather than what the finished build happens to do. Its expected results are worked out by hand before the model exists, which gives an independent answer to compare against; tests written afterwards tend to copy the model's own output and so confirm whatever it does, including its mistakes. Planning the tests also forces the designer to think about boundary, invalid and erroneous data at the design stage, when adding a validation rule or a limit to a formula costs minutes rather than a rebuild.",
           command="Explain"),
        EQ("Describe what should be included in the design of an input sheet for a spreadsheet model.", 4,
           [MP("The layout and position of labels and input cells", ["layout", "position", "where", "label", "sketch"]),
            MP("Data types, formats and units", ["format", "currency", "type", "unit", "£", "percentage"]),
            MP("Validation rules and input messages", ["validation", "rule", "range", "input message", "drop-down", "list"]),
            MP("Colour coding, protection, or annotations linked to requirements", ["colour", "unlocked", "protect", "annotat", "requirement", "key"])],
           "The design should show the layout of the sheet, with every label and input cell in position, so the builder knows exactly where everything goes. Each input should have its data type, format and unit stated, such as currency to two decimal places in pounds. The validation rule for each input should be given, for example a decimal from 5 to 60 with an input message explaining it, or a drop-down list fed from a named range. Finally, the design should show the colour coding that marks input cells as unlocked and editable, and be annotated to explain each choice and the requirement it meets.",
           command="Describe"),
        EQ("A café owner says: \"I want a spreadsheet to help me plan my prices.\"\n\nExplain how you would turn this into requirements that can be tested. Give **two** examples of testable requirements.", 6,
           [MP("Find out more from the client, such as by an interview", ["interview", "ask", "question", "meet", "discuss", "find out"]),
            MP("Identify the users, the inputs and the outputs", ["users", "inputs", "outputs", "who", "what it must show", "data"]),
            MP("Make each requirement specific and measurable", ["specific", "measurable", "testable", "prove", "number", "range"]),
            MP("A first valid testable requirement", ["calculate", "profit", "margin", "for any price", "to the nearest"]),
            MP("A second valid testable requirement", ["without help", "protect", "red", "chart", "compare", "validate", "within"]),
            MP("Number the requirements so tests and evaluation can refer to them", ["number", "R1", "refer", "trace", "test", "evaluat"])],
           "The request is a starting point, not a requirement, so I would interview the owner to find out what decision the model is meant to support, who will use it, what data is available and what they need to see. That identifies the inputs, such as the cost of ingredients for each item and the expected number of sales, and the outputs, such as the profit on each item and in total. I would then rewrite each need so that it is specific and measurable, because a requirement is only useful if I can later prove whether it was met. For example: R1, the model calculates the profit per item and for the whole menu for any price the owner enters, to the nearest penny; and R2, a member of staff can change a price and read the new weekly profit without help. Numbering the requirements means each one can be traced to a test in the test plan and to a verdict in the evaluation.",
           command="Explain"),
    ],
)

# ============================================================== F202 TA3

F_CREATING = Topic(
    slug="creating-a-spreadsheet-model",
    title="F202 TA3: Creating the Spreadsheet Model",
    spec="F202 TA3",
    icon="i-table",
    minutes=36,
    exam_title=NEA,
    blurb="Building the model: formulas and functions, decisions and lookups, validation, protection and macros, what-if analysis with Goal Seek, scenarios and data tables, and the charts that show the answer.",
    fact="Excel stores dates as numbers counting days from 1 January 1900, and it treats 1900 as a leap year, which it was not. The error was copied on purpose from an older spreadsheet, Lotus 1-2-3, so that old files would still give the same answers.",
    sections=[
        Section("Formulas, functions and references", """
### Operators and the order they work in

| Operator | Meaning | Example |
| `+ - * /` | Add, subtract, multiply, divide | `=Revenue-TotalCosts` |
| `^` | Power | `=1.05^3` for three years of 5% growth |
| `&` | Join text | `=A2&" tickets"` |
| `= <> < > <= >=` | Compare, giving TRUE or FALSE | `=Profit>=0` |

Brackets first, then powers, then multiplication and division, then addition and subtraction. `=4000+5*270` is 5,350. Write `=(4000+5)*270` only if that is what you mean.

### Functions worth knowing

| Category | Functions | Example |
| Totals and averages | `SUM`, `AVERAGE`, `MEDIAN`, `MIN`, `MAX` | `=AVERAGE(B2:B31)` |
| Counting | `COUNT`, `COUNTA`, `COUNTBLANK`, `COUNTIF`, `COUNTIFS` | `=COUNTIF(Type,"Child")` |
| Conditional totals | `SUMIF`, `SUMIFS`, `AVERAGEIF`, `MAXIFS` | `=SUMIFS(Revenue,Type,"Adult",Day,"Sat")` |
| Rounding | `ROUND`, `ROUNDUP`, `ROUNDDOWN`, `INT` | `=ROUNDUP(Visitors/50,0)` stewards needed |
| Text | `LEFT`, `RIGHT`, `MID`, `LEN`, `UPPER`, `TRIM`, `CONCAT`, `TEXTJOIN` | `=UPPER(LEFT(A2,3))` |
| Dates | `TODAY`, `DATE`, `YEAR`, `WEEKDAY`, `NETWORKDAYS` | `=FestivalDate-TODAY()` days to go |
| Logic | `IF`, `IFS`, `AND`, `OR`, `NOT`, `IFERROR` | `=IF(AND(Profit>0,TicketsSold<Capacity),"OK","Check")` |
| Lookup | `XLOOKUP`, `VLOOKUP`, `HLOOKUP`, `INDEX`, `MATCH` | `=XLOOKUP(B2,Types,Prices)` |
| Finance | `PMT`, `FV` | `=PMT(6%/12,36,-12000)` is about £365 a month |

### The festival model, as built

```formula
TicketsSold     =MIN(Capacity, MAX(0, DemandAtZero - LostPerPound * TicketPrice))
Revenue         =TicketsSold * TicketPrice
VariableCosts   =TicketsSold * CostPerHead
TotalCosts      =FixedCosts + VariableCosts
Profit          =Revenue - TotalCosts
Status          =IF(Profit >= 0, "PROFIT", "LOSS")
BreakEvenTickets =ROUNDUP(FixedCosts / (TicketPrice - CostPerHead), 0)
```

Every formula refers to a named cell, so it reads as a sentence. `MAX(0, …)` was not in the original design: test 5 found that a price of £60 gave −120 tickets, and this is the fix. `BreakEvenTickets` is the classic break-even calculation: at £27.50 the festival needs `4000 ÷ 22.50`, rounded up to 178 tickets, to cover its costs.

### Tables and structured references

Formatting a list as a table (Ctrl+T in Excel) gives it a name, makes it grow when rows are added, and lets formulas say `Sales[Revenue]` instead of `$D$2:$D$4001`. Charts, pivot tables and validation lists built on a table then pick up new rows by themselves.

!key Build in the order the data flows :: Inputs first, then each calculation in turn, checking each one by hand before building the next. A wrong value found at step two is a minute's work. Found on the dashboard, it could be anywhere.
"""),
        Section("Decisions and lookups", """
### IF, and the logic around it

`=IF(test, value if true, value if false)` chooses between two results.

| Need | Formula |
| One test | `=IF(Profit>=0,"PROFIT","LOSS")` |
| Both conditions must be true | `=IF(AND(Age>=16,Age<=18),"Concession","Standard")` |
| Either condition is enough | `=IF(OR(Type="Child",Type="Concession"),"Reduced","Full")` |
| Several outcomes | A nested `IF`, or `IFS` |

!diagram f202-nested-if

### Lookups

When the answer comes from a table, a lookup is better than a chain of IFs: the table can be read, checked and changed without touching a formula.

!diagram f202-lookup

| Function | Use it when | Watch out for |
| `XLOOKUP` | You have a current version of Excel or Google Sheets | Older versions do not have it |
| `VLOOKUP` | The value you match is in the first column of the table | Count the column number carefully, and use FALSE for an exact match |
| `HLOOKUP` | The table runs across rows instead of down columns | The same as VLOOKUP |
| `INDEX` with `MATCH` | It must work in every program, or look to the left | Two functions to get right instead of one |
| `IFERROR` | A lookup might reasonably find nothing | It hides every error, so use it only where you expect one |

`=INDEX(Prices, MATCH(B2, Types, 0))` does the same job as the XLOOKUP in the diagram, in any spreadsheet program. The `0` asks MATCH for an exact match.
"""),
        Section("Validation, formatting, protection and macros", """
### Data validation

!diagram f202-validation

- Give each input cell an **input message**, so the rule is visible before anybody breaks it.
- Choose the **error style** deliberately. **Stop** refuses the value. **Warning** and **Information** let it through after a message, which suits values that are unusual rather than impossible.
- Feed **drop-down lists** from a named range, so the list can grow without editing the rule.

### Conditional formatting

Formatting that responds to the value: profit in red below zero, a data bar showing tickets sold against capacity, a colour scale across a data table so the best prices stand out. A rule can use a formula, such as `=$D2<0` to shade a whole row when its profit is negative.

Use it to draw the eye to what needs attention, and use it sparingly. A sheet where everything is highlighted highlights nothing.

### Protection

1. Unlock the input cells: Format Cells, Protection, untick **Locked**. Every cell starts locked.
2. Protect the sheet, so that only the unlocked cells can be edited.
3. Protect the workbook structure, so sheets cannot be deleted, moved or renamed.
4. Record any password in the technical documentation, not in the user guide.

!warn Protection is not security :: Sheet protection prevents accidents, not determined people, and its passwords can be removed. Confidential data needs an encrypted file and proper access control, not a protected sheet.

### Macros

A **macro** records or codes a sequence of actions so it can be run with one click. Typical uses in a model: run Goal Seek, reset the inputs to their defaults, clear a form, print the dashboard, or move between sheets.

```vba
' Finds the ticket price that gives the target profit typed on the dashboard
Sub FindPriceForTarget()
    Range("Profit").GoalSeek Goal:=Range("TargetProfit").Value, _
        ChangingCell:=Range("TicketPrice")
End Sub
```

- In Excel, macros are written in **VBA**, and the file must be saved as `.xlsm`. Google Sheets uses **Apps Script** instead, and LibreOffice uses Basic.
- Assign each macro to a clearly labelled button, and test it like any other feature.
- Users see a security warning when they open a file containing macros, so the user guide has to tell them what to do.
"""),
        Section("What-if analysis", """
What-if analysis is the reason a model exists. There are four ways to do it, and each answers a different kind of question.

| Tool | The question it answers | Where it is in Excel |
| **Changing an input** | What happens if the price is £30? | Type a new value |
| **Goal Seek** | What price gives a £1,000 profit? | Data, What-If Analysis, Goal Seek |
| **Scenario Manager** | How do the pessimistic, expected and optimistic cases compare? | Data, What-If Analysis, Scenario Manager |
| **Data table** | What is the profit at every price from £10 to £50? | Data, What-If Analysis, Data Table |

LibreOffice Calc has the same tools under different names: Goal Seek and Scenarios on the Tools menu, and Multiple Operations for data tables. Google Sheets has no built-in Scenario Manager or data table, so there the grid of results is built with ordinary formulas.

!tool what-if-model

!diagram f202-what-if-chart

The chart shows what a single answer cannot. The best price is £27.50, but the curve is flat near the top: £25 and £30 both make £2,000, only £75 less, so the committee can choose a round price and lose very little. Below £16.67 the festival sells out, so lowering the price further only gives money away. And £20 and £35 make the same profit, but £35 does it with half the crowd.

!diagram f202-goal-seek

!diagram f202-scenarios

### Sensitivity analysis

Change each assumption by the same amount, 10% here, and see how far the profit moves.

| Assumption changed by 10% | Profit at £27.50 | Change |
| None: the expected case | £2,075 | — |
| Demand at £0 falls from 600 to 540 | £725 | −£1,350 |
| Fixed costs rise from £4,000 to £4,400 | £1,675 | −£400 |
| Cost per head rises from £5.00 to £5.50 | £1,940 | −£135 |

The model is far more sensitive to the demand assumption than to either cost, so the survey behind it deserves the closest checking, and the evaluation should say so.

For harder questions, such as the most profitable price that still sells at least 300 tickets, Excel's **Solver** add-in and LibreOffice's Solver find the best value of an output while keeping to constraints you set.
"""),
        Section("Charts and pivot tables", """
### Choosing the chart

!diagram data-chart-choice

- A **line or scatter chart** shows one quantity against another, such as profit against price.
- A **column or bar chart** compares categories, such as tickets by type or profit by scenario.
- A **pie chart** shows parts of a whole, and only works with a few slices.
- Every chart needs a **title**, **axis titles with units**, and a **legend only if there is more than one series**.
- Start a column chart's axis at **zero**, or the differences look bigger than they are.
- Build charts from tables or named ranges, so they **update** when the data grows.

### Pivot tables

!diagram f202-pivot

A pivot table is the quickest way to explore a long list: drag fields into rows, columns and values, and change the view in seconds. For figures the client relies on, formulas such as `SUMIFS` are safer, because they always recalculate.
"""),
        Section("Sources and further reading", """
- [Microsoft Excel help and learning](https://support.microsoft.com/en-us/excel): functions, Goal Seek, Scenario Manager, data tables, validation, protection and macros, each with worked examples.
- [Google Sheets function list](https://support.google.com/docs/table/25273): every function in Sheets, including XLOOKUP and the IF family.
- [LibreOffice Help](https://help.libreoffice.org/): Calc's Goal Seek, Scenarios, Multiple Operations and Solver.
- [GCF Global Excel tutorials](https://edu.gcfglobal.org/en/excel/): free lessons on functions, charts, pivot tables and what-if analysis.
- [The what-if model on its own page](/tools/what-if-model/): the interactive model above, with room to explore.
"""),
    ],
    keyterms=[
        ("Formula", "A calculation written by the user, starting with an equals sign."),
        ("Function", "A built-in calculation, such as SUM, IF or XLOOKUP."),
        ("Nested IF", "An IF function placed inside another, to choose between more than two outcomes."),
        ("Lookup", "A function that finds a value in a table, such as XLOOKUP or VLOOKUP."),
        ("Exact match", "A lookup that returns a result only when the value is found exactly."),
        ("Approximate match", "A lookup that returns the largest value not greater than the one searched for, in a sorted table."),
        ("Data validation", "Rules restricting what can be entered into a cell."),
        ("Input message", "A note shown when a validated cell is selected, explaining what to enter."),
        ("Conditional formatting", "Formatting applied automatically when a cell's value meets a rule."),
        ("Cell protection", "Locking cells and protecting the sheet so that only unlocked cells can be edited."),
        ("Macro", "A recorded or coded sequence of actions that runs with one command."),
        ("Goal Seek", "A tool that changes one input cell until a formula cell reaches a target value."),
        ("Scenario Manager", "A tool that stores named sets of inputs and compares their outputs."),
        ("Data table", "A grid showing a formula's result for a range of values of one or two inputs."),
        ("Pivot table", "An interactive summary of a list, grouping and totalling it without formulas."),
    ],
    grade="""
+ Refer to named cells, never to typed numbers, so every formula reads as a sentence
+ Use the right tool for each job: a lookup for a table, IF for a decision, validation for an input
+ Validate every input, with input messages and a deliberate choice of error style
+ Protect the formulas and leave only the inputs editable
+ Use what-if tools to answer the client's question, and explain what each result means
+ Show a range of techniques used well, each one justified by a requirement
""",
    mistakes=[
        "Typing values into formulas, so changing an assumption means hunting through every cell.",
        "VLOOKUP without FALSE, which silently returns approximate matches.",
        "Nested IFs that test the smallest threshold first, so the larger bands are never reached.",
        "Protecting the sheet before unlocking the input cells, so nobody can enter anything.",
        "Running Goal Seek once and reporting the answer without checking it in the model.",
        "Charts with no axis titles or units.",
        "Using IFERROR to hide errors that should have been fixed.",
    ],
    quiz=[
        Q("What does =VLOOKUP(B2,Tickets,2) do when the fourth argument is left out?",
          ["An approximate match, which can return a wrong answer with no error",
           "An exact match", "It always shows an error",
           "It looks in column 4"], 0,
          "Approximate matching is the default. Add FALSE, or use XLOOKUP, for an exact match."),
        Q("Which formula gives 20% for 20 or more, 10% for 10 or more, otherwise 0%?",
          ["=IF(B2>=20,20%,IF(B2>=10,10%,0%))",
           "=IF(B2>=10,10%,IF(B2>=20,20%,0%))",
           "=IF(B2>20,20%,10%)",
           "=IF(B2>=20,10%,IF(B2>=10,20%,0%))"], 0,
          "Test the largest threshold first. The second version gives 25 only 10%."),
        Q("What must you do before protecting a sheet, so users can still enter inputs?",
          ["Unlock the input cells", "Lock the input cells",
           "Hide the formulas", "Remove the validation"], 0,
          "Every cell starts locked. Protection only takes effect on locked cells."),
        Q("Which tool shows the profit for every price from £10 to £50 in one grid?",
          ["A data table", "Goal Seek", "Conditional formatting", "A macro"], 0,
          "A one-variable data table runs the model once for each value in the list."),
        Q("Goal Seek finds £18.04 starting from £20, and £36.96 starting from £35. Why?",
          ["It changes one input from its starting value and stops at the first answer it reaches",
           "The model has an error", "Goal Seek is random",
           "Validation changed the result"], 0,
          "When a model has two answers, the starting value decides which one Goal Seek finds."),
        Q("Which validation error style refuses an invalid value outright?",
          ["Stop", "Warning", "Information", "Input message"], 0,
          "Warning and Information both let the value through once the user confirms it."),
        Q("An Excel workbook containing macros must be saved as:",
          [".xlsm", ".xlsx", ".csv", ".pdf"], 0,
          "The standard .xlsx format cannot store VBA code."),
        Q("What does IFERROR do?",
          ["Returns an alternative value when a formula produces an error",
           "Fixes the error in the formula",
           "Finds every error in the sheet", "Turns off validation"], 0,
          "It hides the error rather than fixing it, so use it only where an error is expected."),
        Q("Why must a pivot table be refreshed?",
          ["It does not recalculate when its source data changes",
           "It deletes itself after a day", "Refreshing adds a chart",
           "Refreshing removes duplicates"], 0,
          "Formulas recalculate automatically; a pivot table has to be told to."),
        Q("Which chart best shows profit against ticket price?",
          ["A line or scatter chart", "A pie chart", "A doughnut chart",
           "A radar chart"], 0,
          "One continuous quantity against another is a line or scatter chart."),
    ],
    exam=[
        EQ("Explain how data validation and cell protection together make a spreadsheet model more robust.", 4,
           [MP("Validation restricts what can be entered, such as a range or a type", ["restrict", "range", "type", "list", "only", "between"]),
            MP("So invalid data is rejected before it reaches the calculations", ["reject", "invalid", "error", "stop", "before", "bad data"]),
            MP("Protection locks formula cells so they cannot be overwritten", ["lock", "formula", "overwrite", "cannot be changed", "protect"]),
            MP("Together, only valid data goes in, and only in the right places", ["together", "only", "input cells", "right place", "both"])],
           "Data validation restricts what each input cell will accept, for example a decimal from 5 to 60 for a ticket price or a choice from a list for a ticket type, so invalid or wrongly typed data is rejected before it can reach any calculation. Cell protection locks every formula cell and protects the sheet, so a user cannot type over a formula by accident, which would replace a calculation with a fixed number and break the model without any warning. Together they mean that data can only be entered in the input cells, and only valid data at that, which removes the two most common ways a working model is broken by its users.",
           command="Explain"),
        EQ("Compare Goal Seek and Scenario Manager as ways of carrying out what-if analysis.", 4,
           [MP("Goal Seek works backwards from a target output to an input", ["backwards", "target", "goal", "find the input", "value you want"]),
            MP("Goal Seek changes only one input and finds one answer", ["one cell", "one input", "single", "one answer", "starting value"]),
            MP("Scenario Manager stores several named sets of input values", ["sets", "several inputs", "named", "stores", "best case", "worst case"]),
            MP("Scenario Manager compares the outputs of the scenarios, such as in a summary", ["compare", "summary", "side by side", "report", "range"])],
           "Goal Seek works backwards: you give it a target for one formula cell, such as a profit of 1,000 pounds, and it changes a single input cell, such as the price, until the target is reached. It answers 'what input do I need?', but it only changes one value and finds one answer, which depends on where it started. Scenario Manager works forwards with several inputs at once: it stores named sets of values, such as pessimistic, expected and optimistic, and produces a summary comparing their outputs side by side. It answers 'what range of results might we see?', which makes it the better tool for judging risk, while Goal Seek is the better tool for setting a target.",
           command="Compare"),
        EQ("A model uses =VLOOKUP(B2,Tickets,2) to find ticket prices. Some prices come out wrong, but no error is shown.\n\nExplain why this happens and how it should be fixed.", 5,
           [MP("The fourth argument is missing, so VLOOKUP makes an approximate match", ["approximate", "fourth", "missing", "TRUE", "default"]),
            MP("Approximate matching needs a sorted table and returns the nearest lower value", ["sorted", "nearest", "lower", "largest", "order"]),
            MP("It always returns something, so no error appears", ["always", "no error", "returns a value", "silent", "something"]),
            MP("Fix: add FALSE, or use XLOOKUP or INDEX with MATCH", ["FALSE", "XLOOKUP", "INDEX", "MATCH", "exact"]),
            MP("Retest every ticket type, and handle values not found", ["test", "each type", "every", "IFERROR", "#N/A", "not found"])],
           "The formula leaves out VLOOKUP's fourth argument, and when it is missing VLOOKUP does an approximate match. Approximate matching assumes the first column is sorted and returns the row with the largest value not greater than the one searched for, so with an unsorted list of ticket type names it can land on the wrong row. Because an approximate match always returns something, there is no error to warn anyone, and the wrong price looks perfectly believable. The fix is to ask for an exact match, =VLOOKUP(B2,Tickets,2,FALSE), or to use =XLOOKUP(B2,Tickets[Type],Tickets[Price]), which matches exactly by default. The lookup should then be retested with every ticket type and with a value that is not in the table, which should now give #N/A, handled with IFERROR and a clear message for the user.",
           command="Explain"),
    ],
)

# ============================================================== F202 TA4

F_DELIVERING = Topic(
    slug="testing-and-delivering-a-spreadsheet-model",
    title="F202 TA4: Testing and Delivering the Outcomes",
    spec="F202 TA4",
    icon="i-check-circle",
    minutes=30,
    exam_title=NEA,
    blurb="Carrying out the tests and fixing what fails, presenting the answer to the client's question, and writing the user guide and the technical documentation.",
    fact="In 2012 a bank's risk model, built partly by copying and pasting between spreadsheets, divided by a sum where it should have divided by an average. It understated the risk on trades that went on to lose billions of dollars.",
    sections=[
        Section("Testing the model", """
Testing is carrying out the test plan, recording what actually happened, fixing what failed, and testing it again.

### Evidence that convinces

- A **screenshot of the inputs and the outputs** for each test, labelled with the test number.
- The **formula view** of the calculation being tested: Formulas, Show Formulas, or Ctrl+` in Excel.
- **Before and after** screenshots of anything that failed and was fixed, plus the retest.
- **Annotations** saying what each screenshot proves.

### Tools that find faults

| Tool | What it does |
| **Trace Precedents** | Draws arrows to the cells a formula uses |
| **Trace Dependents** | Draws arrows to every cell that uses this one |
| **Evaluate Formula** | Steps through a formula one part at a time |
| **Error Checking** | Flags inconsistent formulas and numbers stored as text |
| **Show Formulas** | Displays every formula instead of its result |

### Error values, and what they usually mean

| Error | Meaning | A typical cause in a model |
| `#DIV/0!` | Division by zero | Break-even tickets when the price equals the cost per head |
| `#N/A` | A value is not available | A lookup that found nothing |
| `#VALUE!` | The wrong type of value | Text in a cell used in arithmetic |
| `#REF!` | A reference is no longer valid | A row or sheet the formula used has been deleted |
| `#NAME?` | An unrecognised name | A misspelt function or an undefined named range |
| `#NUM!` | An impossible number | A calculation with no valid answer |
| `#####` | The column is too narrow | Not an error in the value at all: widen the column |
| Circular reference | A formula depends on itself | A cost calculated from the profit it feeds into |

!key A failed test is good evidence :: A log in which every test passes first time is not believable, and suggests the tests were chosen to pass. Record the failure, the cause, the fix and the retest: that is the process the assessment is looking for.

### User acceptance testing

Give the client or real users **tasks**, not a tour: "The committee wants to know the profit if only 400 people would come even for free. Find out." Watch, do not help, and note every hesitation. Then record what they said and what you changed because of it.
"""),
        Section("Presenting the outcomes", """
The client did not ask for a spreadsheet. They asked a question, and the model exists to answer it. Delivering the outcomes means presenting that answer clearly enough to act on.

!diagram f202-dashboard

### A recommendation built from the model

!info A worked recommendation, for the invented festival brief :: At the expected demand, a price of £27.50 makes the most profit, £2,075, from 270 tickets. The profit curve is flat near the top, so a round £25 or £30 makes £2,000, only £75 less. The risk is in the demand survey: if 10% fewer people want to come, profit at £27.50 falls to £725, and in the pessimistic scenario the festival loses £845. I recommend £25. It sells 300 tickets at the expected demand, keeps the event affordable, and does better than £27.50 if demand is weak: £800 rather than £725 with 10% less demand, and a loss of £700 rather than £845 in the pessimistic case. Before deciding, the committee should test the survey with a short pre-sale.

What makes that a strong recommendation:

- It answers the client's question directly, in the first sentence.
- It quotes the model's outputs, with units.
- It states the uncertainty, using the scenarios and the sensitivity analysis.
- It makes a decision and justifies it with the numbers.
- It says what would make the decision more certain.

### Choosing how to present

| Audience | Format |
| A busy client who wants a decision | A one-screen dashboard and a short written recommendation |
| A committee meeting | Three or four slides: the question, the answer, the risk, the recommendation |
| The people entering data | A user guide with annotated screenshots |
| Whoever maintains the model | Technical documentation |
"""),
        Section("The user guide and the technical documentation", """
Two documents, for two different readers.

| | User guide | Technical documentation |
| **Reader** | The people who use the model | Whoever maintains or extends it |
| **Purpose** | Use it correctly without help | Understand how it works and change it safely |
| **Contents** | What the model is for; opening it and enabling macros; entering inputs; running scenarios and Goal Seek; reading the outputs; what each message means; what to do when something goes wrong | The sheet structure; every named range; every formula and why it is there; the validation rules; the macro code, commented; protection, and where passwords are kept; assumptions and their sources; the version history |
| **Style** | Plain English, numbered steps, annotated screenshots | Precise and complete; tables are fine |

### Writing a user guide people can follow

1. One task per section, named the way a user would say it: "Change the ticket price".
2. Numbered steps, one action in each.
3. A screenshot for every step that involves finding something, with the place to click marked.
4. What the user should see when it has worked.
5. The common problems, and the fix for each: "The cell will not accept my value" means the value is outside the allowed range.

Test the guide the way you test the model: give it to somebody who has never seen the model, and watch them follow it.

!key Version control :: Save numbered versions as you go, `festival-model-v01.xlsx`, `v02` and so on, and keep a short log of what changed in each. It protects against lost work, shows how the model developed, and lets you go back when a change makes things worse.
"""),
        Section("Sources and further reading", """
- [Microsoft Excel help and learning](https://support.microsoft.com/en-us/excel): formula auditing, error values and protection.
- [GOV.UK: writing for GOV.UK](https://www.gov.uk/guidance/content-design/writing-for-gov-uk): how to write plain English instructions that people actually follow.
- [Nielsen Norman Group: 10 usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/): principles for designing a dashboard that is easy to use.
- [W3C: introduction to web accessibility](https://www.w3.org/WAI/fundamentals/accessibility-intro/): why accessibility matters, which applies to dashboards and guides as much as to websites.
- [WebAIM contrast checker](https://webaim.org/resources/contrastchecker/): check the colours on your dashboard can be read.
"""),
    ],
    keyterms=[
        ("Test log", "The record of each test carried out, with expected and actual results and any action taken."),
        ("Trace precedents", "An auditing tool that shows the cells a formula takes its values from."),
        ("Trace dependents", "An auditing tool that shows every cell that uses a given cell."),
        ("Error value", "A result such as #DIV/0! or #N/A that shows a formula could not be calculated."),
        ("Circular reference", "A formula that depends, directly or indirectly, on its own cell."),
        ("Dashboard", "A single screen summarising the outputs a client needs to make a decision."),
        ("Recommendation", "A justified decision for the client, drawn from the model's outputs and their uncertainty."),
        ("User guide", "Documentation that tells users how to operate the model, in plain language."),
        ("Technical documentation", "Documentation that explains how the model works, so it can be maintained and changed."),
        ("Version control", "Saving numbered versions with a record of changes, so earlier versions can be recovered."),
    ],
    grade="""
+ Carry out the whole test plan and record actual results honestly, failures included
+ Show the fix and the retest for every failure
+ Use the formula auditing tools and the formula view as evidence
+ Present a recommendation that answers the client's question and states the uncertainty
+ Write a user guide for users and technical documentation for maintainers, and test both
""",
    mistakes=[
        "A test log in which every test passed first time.",
        "Screenshots with no explanation of what they prove.",
        "Presenting the spreadsheet itself as the outcome, with no recommendation.",
        "Reporting one profit figure as if it were certain, ignoring the scenarios.",
        "A user guide written in technical language, or technical documentation with no formulas in it.",
        "Hiding errors with IFERROR instead of fixing their cause.",
    ],
    quiz=[
        Q("A cell shows #####. What is the most likely cause?",
          ["The column is too narrow to display the value", "Division by zero",
           "A lookup found nothing", "A deleted reference"], 0,
          "Widen the column and the value appears. It is not an error in the calculation."),
        Q("What does #REF! usually mean?",
          ["A cell or sheet the formula referred to has been deleted",
           "A function name is misspelt", "The number is too large",
           "The value is text"], 0,
          "The reference no longer points anywhere valid."),
        Q("What does #NAME? usually mean?",
          ["A function or named range is misspelt or not defined",
           "Division by zero", "The column is too narrow",
           "A circular reference"], 0,
          "The spreadsheet does not recognise a word in the formula."),
        Q("Which tool shows the cells a formula takes its values from?",
          ["Trace Precedents", "Trace Dependents", "Freeze Panes", "Goal Seek"], 0,
          "Precedents come before the formula; dependents come after it."),
        Q("Why should a test log include failed tests?",
          ["It shows genuine testing, with the fault, the fix and the retest",
           "Failures earn marks on their own",
           "The plan requires at least one failure", "It makes the log longer"], 0,
          "Finding and fixing faults is the evidence of a real testing process."),
        Q("What is user acceptance testing?",
          ["Real users carry out tasks to check the model meets their needs",
           "The developer tests each formula", "Validation rejects bad data",
           "The software checks for errors automatically"], 0,
          "It tests the model against the people it was built for."),
        Q("Which belongs in the technical documentation rather than the user guide?",
          ["Every named range and formula, with what each does",
           "How to change the ticket price", "What the dashboard numbers mean",
           "How to enable macros when the file opens"], 0,
          "Users need to operate the model; maintainers need to understand it."),
        Q("What makes a recommendation strong?",
          ["It answers the question, quotes the outputs and states the uncertainty",
           "It lists every feature used", "It avoids mentioning risk",
           "It repeats the requirements"], 0,
          "A client acts on a recommendation, so it has to be clear, evidenced and honest about risk."),
        Q("A formula's result depends on its own cell. This is:",
          ["A circular reference", "An absolute reference", "A named range",
           "A nested function"], 0,
          "Spreadsheets warn about circular references because they usually mean a logic error."),
        Q("What is the best evidence that a formula works?",
          ["Its output matches a result worked out by hand for the same inputs",
           "It shows no error value", "It looks reasonable",
           "The client said it was fine"], 0,
          "An independent calculation is the only real check on a formula."),
    ],
    exam=[
        EQ("Describe the evidence that should be recorded when testing a spreadsheet model.", 4,
           [MP("Each test's number, purpose and test data", ["number", "purpose", "test data", "what is tested"]),
            MP("The expected result, worked out before the test", ["expected", "before", "by hand"]),
            MP("The actual result, with screenshots or the formula view", ["actual", "screenshot", "formula view", "show formulas", "evidence"]),
            MP("Failures, with the fix and a retest", ["fail", "fix", "retest", "action", "corrected"])],
           "Each test should be recorded with its number, its purpose and the exact test data used, so it can be repeated. The expected result should have been worked out by hand before the test was run, so there is an independent answer to compare against. The actual result should be recorded and backed by evidence, such as a screenshot of the inputs and outputs and the formula view of the calculation being tested, annotated to say what it shows. Where a test fails, the record should give the cause, the change made and the result of the retest, because a fix that has not been retested has not been shown to work.",
           command="Describe"),
        EQ("Explain the difference between a user guide and technical documentation for a spreadsheet model.", 4,
           [MP("A user guide is for the people who use the model", ["users", "operate", "use it", "end users", "volunteers"]),
            MP("It explains tasks in plain language, with steps and screenshots", ["plain", "steps", "screenshots", "how to", "simple"]),
            MP("Technical documentation is for whoever maintains or changes the model", ["maintain", "developer", "change", "extend", "technical"]),
            MP("It explains how it works: formulas, named ranges, macros, validation", ["formula", "named range", "macro", "validation", "structure", "how it works"])],
           "A user guide is written for the people who will use the model, such as volunteers entering a price, and explains how to carry out each task in plain language, with numbered steps, annotated screenshots and what to do when something goes wrong. Technical documentation is written for whoever has to maintain or change the model later, and explains how it works rather than how to use it: the structure of the sheets, every named range and formula and why it is there, the validation rules, the macro code and the assumptions with their sources. The difference is the reader: one needs to operate the model without help, the other needs to change it without breaking it.",
           command="Explain"),
        EQ("The festival model shows that a ticket price of £27.50 makes the most profit at the expected demand.\n\nExplain why the client should not simply be told to charge £27.50.", 6,
           [MP("The result depends on assumptions, especially the demand survey", ["assumption", "survey", "demand", "estimate", "may be wrong"]),
            MP("Sensitivity: profit depends strongly on demand", ["sensitiv", "10%", "725", "falls", "demand matters"]),
            MP("The pessimistic scenario makes a loss at that price", ["pessimistic", "loss", "845", "worst case", "scenario"]),
            MP("The curve is flat near the top, so other prices are nearly as good", ["flat", "£25", "£30", "2,000", "nearly as", "round"]),
            MP("Other factors outside the model matter", ["afford", "community", "weather", "competitor", "aims", "fair"]),
            MP("The recommendation should give a range or a justified choice with its uncertainty", ["range", "recommend", "uncertain", "pre-sale", "test the survey", "justify"])],
           "£27.50 is only the best price if the model's assumptions are right, and the most important assumption, how many people come at each price, is an estimate from a survey. The sensitivity analysis shows how much rests on it: if 10% fewer people want to come, profit at £27.50 falls from £2,075 to £725, and in the pessimistic scenario the event makes a loss of £845. The profit curve is also flat near the top, so £25 and £30 both make £2,000, only £75 less than the maximum, and £25 actually does better than £27.50 when demand is weak. There are also things the model does not include at all, such as whether the price is affordable for a community event, the weather and competing events. So rather than a single number, the client should be given a recommendation with its reasoning and its risk: for example £25, with the evidence that it gives up little profit in the expected case and loses less if demand disappoints, and a suggestion to test the survey with a pre-sale before committing.",
           command="Explain"),
    ],
)

# ============================================================== F202 TA5

F_EVALUATING = Topic(
    slug="evaluating-a-spreadsheet-model",
    title="F202 TA5: Evaluating a Spreadsheet Model",
    spec="F202 TA5",
    icon="i-scales",
    minutes=26,
    exam_title=NEA,
    blurb="Judging the model against every requirement with evidence, using feedback well, being honest about its limitations, proposing improvements that are specific, and reflecting on how you worked.",
    fact="Research by Jakob Nielsen suggested that testing with about five users finds most of the usability problems in a design, which is why several small rounds of testing beat one big one.",
    sections=[
        Section("Evaluating against the requirements", """
An evaluation is a judgement backed by evidence. Go through the requirements one at a time. For each, say whether it was met, point to the evidence, and say what you would improve.

!diagram f202-evaluation-matrix

### Writing one row well

| Weak | Strong |
| "The model calculates profit well." | "R1 required profit for any price from £5 to £60. It is fully met: tests 1, 2 and 8 match my hand calculations to the penny, and tests 4 and 5 confirm both ends of the range." |
| "Some users found it hard." | "R6 required that a volunteer could find the price for a target profit without help. It is partly met: two of three volunteers could not find Goal Seek in the menus. A dashboard button that runs it would take the menus out of the task." |

!key Verdict, evidence, improvement :: Fully, partly or not met; the test, the feedback or the screenshot that proves it; and what you would change. Three parts, every requirement, every time.
"""),
        Section("Feedback, limitations and improvements", """
### Getting feedback worth using

- Ask the **client** and the **users**, not your friends.
- Ask **specific questions**: "Could you find the break-even price? How long did it take?" rather than "Did you like it?"
- **Watch** someone use the model, as well as asking them about it.
- **Record** what was said, criticism included, and what you did about it.

### The limitations of the model itself

Every model simplifies. Saying where yours does is evidence of understanding, not an admission of failure.

| Limitation | Its effect | An improvement |
| Demand falls by exactly 12 people per £1 | Real demand is rarely a straight line | Fit the line to more survey data, or check it with a pre-sale |
| One price for everybody | It ignores child and concession tickets | Add ticket types with their own demand, using a lookup |
| No weather and no competing events | The biggest risks to attendance are outside the model | Add a weather scenario with lower demand |
| Costs are fixed per head | Security costs really rise in steps, not smoothly | Add a lookup of stewards needed per 100 attendees |
| A survey of 150 residents | A small sample that may not be representative | Collect a larger sample, or compare with similar events |

### Improvements that score

An improvement is specific when it names the change, how it would be made and what it would achieve: "Add a weather drop-down that applies a 30% fall in demand from a lookup table of weather scenarios, so the committee can see the risk of a wet day before setting the price." A list of things you would have done with more time is not an improvement.
"""),
        Section("Reflecting on your own process", """
The last part of an evaluation looks at how you worked, not only at what you made.

- **The plan against reality**: which stages took longer than planned, and why.
- **Decisions you would change**: "I built the dashboard before the calculations were tested, so when test 5 changed the tickets formula I had to rebuild two charts."
- **Skills**: what you can do now that you could not before, with an example from the model.
- **Next time**: what you would do differently, specifically.

!warn Generic reflection earns nothing :: "I learned a lot and managed my time well" could be written by anyone about anything. Reflection counts when it is specific to your model, names a real decision, and says what you would change.
"""),
        Section("Sources and further reading", """
- [The H019 and H119 specification (PDF)](%s): what TA5 expects an evaluation to cover.
- [Nielsen Norman Group: why you only need to test with 5 users](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/): the research behind small, repeated rounds of user testing.
- [Office for National Statistics](https://www.ons.gov.uk/): published data to compare your assumptions against.
- [Microsoft Excel help and learning](https://support.microsoft.com/en-us/excel): how to build the improvements you propose.
""" % OCR_SPEC),
    ],
    keyterms=[
        ("Evaluation", "A judgement of how well the model meets its requirements, backed by evidence."),
        ("Verdict", "Whether a requirement is fully, partly or not met."),
        ("Evidence", "A test result, piece of feedback or screenshot that supports a verdict."),
        ("Limitation", "A way in which the model simplifies or cannot handle the real situation."),
        ("Improvement", "A specific change, how it would be made, and what it would achieve."),
        ("Feedback", "Comments and observations from the client and users about the model."),
        ("Reflection", "An analysis of how you worked, what you would change and why."),
    ],
    grade="""
+ Give every requirement a verdict, with evidence from tests or feedback
+ Use feedback from the client and real users, quoted, criticism included
+ Explain the model's limitations, including its assumptions
+ Propose improvements that name the change, the method and the effect
+ Reflect on your own process specifically, with real decisions you would change
""",
    mistakes=[
        "Saying the model 'works well' without referring to any requirement.",
        "Claiming everything was fully met, with no evidence.",
        "Feedback from friends, or questions like 'did you like it?'",
        "Improvements that are a wish list rather than specific changes.",
        "Ignoring the assumptions, as if correct formulas guaranteed correct answers.",
        "Generic reflection that could describe any project.",
    ],
    quiz=[
        Q("What should every row of an evaluation contain?",
          ["The requirement, a verdict, the evidence and an improvement",
           "A screenshot only", "A description of the formulas",
           "How long each part took"], 0,
          "Verdict, evidence, improvement, for every requirement."),
        Q("Which is evidence that a requirement was met?",
          ["Tests 1, 2 and 8 match the hand calculations",
           "The model looks professional", "I am happy with it",
           "It was finished on time"], 0,
          "Evidence can be checked. Opinions cannot."),
        Q("Who should give feedback on the model?",
          ["The client and the real users", "Friends",
           "Only the developer", "Nobody: the tests are enough"], 0,
          "The people the model was built for are the ones whose experience matters."),
        Q("Which question gets the most useful feedback?",
          ["Could you find the break-even price, and how long did it take?",
           "Did you like it?", "Is it good?", "Would you use it?"], 0,
          "A specific task gives a specific, checkable answer."),
        Q("Which is a limitation of the festival model?",
          ["It assumes demand falls by exactly 12 people for every £1",
           "It uses named ranges", "It has a dashboard",
           "It validates the price"], 0,
          "Real demand is rarely a straight line, so this assumption simplifies reality."),
        Q("What makes an improvement specific?",
          ["It names the change, how it would be made and what it would achieve",
           "It is ambitious", "It would take a long time",
           "It mentions more features"], 0,
          "An improvement without a method and an effect is a wish."),
        Q("Why is 'partly met' acceptable in an evaluation?",
          ["An honest judgement backed by evidence shows understanding",
           "It avoids losing marks", "It means the requirement was wrong",
           "It is the same as fully met"], 0,
          "Honest, evidenced judgement is the point of an evaluation."),
        Q("What does reflection on your process look at?",
          ["How you worked, what you would change and why",
           "The client's business", "The spreadsheet's features",
           "The marking criteria"], 0,
          "It is about your decisions and your methods, not the product alone."),
        Q("Two of three volunteers could not find Goal Seek. Which improvement is best?",
          ["A dashboard button that runs Goal Seek with a macro",
           "Tell users to read the manual", "Remove Goal Seek",
           "Add more colour"], 0,
          "It removes the difficulty itself rather than blaming the users."),
        Q("Why evaluate the assumptions as well as the formulas?",
          ["Correct formulas still give wrong answers if the assumptions are wrong",
           "Assumptions are easier to evaluate", "Formulas cannot be evaluated",
           "Assumptions belong in the user guide"], 0,
          "Garbage in, garbage out: the formulas are only as good as their inputs."),
    ],
    exam=[
        EQ("Explain why an evaluation should be organised around the client's requirements.", 3,
           [MP("The requirements define what success means for this client", ["define", "success", "what the client needs", "criteria", "agreed"]),
            MP("Each requirement can be given a verdict backed by evidence", ["verdict", "evidence", "met", "test", "each"]),
            MP("It shows what is unmet, so improvements are targeted", ["unmet", "partly", "improve", "priorit", "gap", "target"])],
           "The requirements are the agreed definition of success for this client, so judging the model against them evaluates whether it does what it was built to do, rather than whether its maker likes it. Working through them one at a time means each can be given a clear verdict backed by specific evidence, such as a test result or a user's feedback. It also shows exactly which needs are only partly met or not met, so the improvements proposed are targeted at real gaps rather than being a general wish list.",
           command="Explain"),
        EQ("Describe **two** limitations of a spreadsheet model like the festival ticket model, and suggest an improvement for each.", 4,
           [MP("A first limitation of the model", ["straight line", "linear", "demand", "assumption", "one price", "survey"]),
            MP("A specific improvement for it", ["more data", "pre-sale", "ticket types", "lookup", "larger sample", "fit"]),
            MP("A second limitation of the model", ["weather", "competing", "steps", "security", "fixed per head", "sample", "static"]),
            MP("A specific improvement for it", ["scenario", "drop-down", "lookup", "stewards", "per 100", "compare"])],
           "The model assumes demand falls by exactly 12 people for every pound added to the price, but real demand is rarely a straight line, so the model could be improved by collecting more survey responses at different prices and fitting the line to them, or by checking it against a small pre-sale. It also ignores the weather, which is probably the biggest single risk to attendance at an outdoor event, so a weather drop-down could apply a fall in demand taken from a lookup table of weather scenarios, letting the committee see the risk of a wet day before setting the price.",
           command="Describe"),
        EQ("Evaluate the usefulness of user feedback when evaluating a spreadsheet model.", 6,
           [MP("Feedback reveals usability problems the developer cannot see", ["cannot see", "developer", "familiar", "own model", "blind", "know how it works"]),
            MP("Watching real tasks gives specific evidence", ["task", "watch", "observe", "time", "hesitat", "specific"]),
            MP("It shows whether the model meets the client's real needs", ["client", "needs", "priorit", "useful", "decision"]),
            MP("Feedback from friends or a tiny sample can be biased", ["friends", "biased", "small", "polite", "not representative"]),
            MP("Opinions are weaker than observed evidence, and questions must be specific", ["opinion", "vague", "specific question", "liked", "leading"]),
            MP("A justified overall judgement", ["overall", "most useful", "therefore", "only if", "combined with", "valuable"])],
           "User feedback is valuable because the person who built a model is the one person who cannot experience it fresh: they know where every input is and what every output means, so they are blind to the moments a new user hesitates. Watching a real user attempt a task, such as finding the price for a target profit, produces specific evidence, like two of three volunteers being unable to find Goal Seek, which points straight at an improvement. The client's feedback also shows whether the model answers the question they actually needed answered, which testing the formulas cannot. Its usefulness depends on how it is gathered, though. Feedback from friends tends to be polite rather than honest, a sample of one or two users may be unrepresentative, and vague questions such as 'did you like it?' produce opinions rather than evidence. Overall, feedback is one of the most useful sources of evidence in an evaluation, but only when it comes from the real client and users, is gathered with specific tasks and questions, and is recorded honestly alongside the test results rather than replacing them.",
           command="Evaluate"),
    ],
)

# =========================================================== the assignment

F_GUIDE = Topic(
    slug="spreadsheet-modelling-coursework-guide",
    title="F202 Coursework: The Set Assignment Guide",
    spec="F202 set assignment",
    icon="i-flag",
    minutes=24,
    exam_title=NEA,
    blurb="How the F202 set assignment is assessed, what to produce at each stage, the rules about doing it independently, and worked extracts from an invented brief showing evidence at its best.",
    fact="The phrase 'garbage in, garbage out' dates from the early days of computing, and it applies in full to coursework: a beautifully built model resting on an unchecked assumption is still wrong.",
    sections=[
        Section("How F202 is assessed", """
F202 is the **non-examined assessment** unit of the qualification, so there is no written paper. You complete an **OCR-set assignment**, your teacher **marks** it against OCR's marking criteria, and OCR **moderates** a sample of your centre's work to check that the marking matches the national standard.

| Feature | Detail |
| **Unit** | F202 Spreadsheet data modelling |
| **Qualifications** | Mandatory in both the Certificate (H019) and the Extended Certificate (H119) |
| **Size** | 75 guided learning hours, 15 of them for completing the set assignment |
| **Assessment** | OCR-set assignment, centre-assessed and OCR-moderated |
| **The brief** | A scenario with a client, a problem and tasks, published by OCR and given to you by your teacher |

Set assignments are replaced over time, and each is valid for a stated period. Your teacher will give you the version your centre is using, with its tasks, any templates OCR supplies, and your deadlines. Everything on these pages is general teaching: the examples use an invented brief, so they show the **quality** of each kind of evidence without answering yours.

!diagram f202-nea-journey
"""),
        Section("What to produce at each stage", """
| Stage | The evidence you produce | What makes it strong | The common gap |
| **Understand the brief** | Notes on the client, the users, the problem and the purpose | In your own words, with the needs the brief only implies drawn out | Copying the brief back out |
| **Plan (TA2)** | Numbered requirements, sheet designs, a data dictionary, a processing plan, a test plan | Every design choice linked to a requirement; expected results worked out by hand | Designs with no annotation; tests written after the build |
| **Create (TA3)** | The working model, with evidence of how it was built | Named cells, validation, protection, lookups and what-if tools, each one justified | One technique used over and over; numbers typed into formulas |
| **Deliver (TA4)** | The completed test log with fixes and retests, the outputs presented to the client, the user guide | Honest failures with fixes; a recommendation that answers the question | Every test passing first time; no recommendation at all |
| **Evaluate (TA5)** | A verdict for every requirement, feedback, limitations, improvements and reflection | Evidence behind every verdict; specific improvements | "It went well", with nothing to support it |

Keep **dated versions** of your files as you go, `model-v01.xlsx`, `model-v02.xlsx`, and screenshots of work in progress. They show how the model developed, and they protect you if a file is lost or corrupted.
"""),
        Section("Your own work: the rules", """
Coursework rules are set by the JCQ, the body the exam boards act through, and by OCR. Your teacher will explain how they apply in your centre. The main points:

- **Your work must be your own.** You sign a declaration saying so, and your teacher has to be able to confirm it.
- **Your teacher can teach you and guide you**, explain what the marking criteria mean and give general feedback. They cannot tell you exactly what to change, correct your work for you, or give you a model answer to the assignment.
- **Do not share your work** with other students, or use anybody else's.
- **Artificial intelligence.** Copying or paraphrasing text, formulas or designs from an AI tool and submitting them as your own is malpractice. If your centre allows an AI tool for a particular purpose, you must acknowledge it: name the tool, say what you asked and when, and show how you used the response. The JCQ's AI guidance sets this out in full.
- **Reference every source** you use, whether data, images, ideas or quotations, both in the work and in a reference list.

### Referencing in the Harvard style

| Source | The pattern |
| A web page | Organisation or author (year) *Title of the page*. Available at: URL (Accessed: date). |
| A data set | Publisher (year) *Title of the data set*. Available at: URL (Accessed: date). |
| A book | Author, A. (year) *Title*. Place: Publisher. |

!warn Malpractice has serious consequences :: Work found not to be your own can be given no marks, and in serious cases a student can be disqualified from the qualification. If you are unsure whether something is allowed, ask your teacher before you do it.
"""),
        Section("Worked extracts from an invented brief", """
These extracts show each kind of evidence at its best. They come from the Harbour Lights festival model used throughout this unit. Do not copy their wording: your brief, your client and your decisions are different, and it is yours that are assessed.

!info A requirement :: R3. The model must compare pessimistic, expected and optimistic scenarios side by side, so the committee can see the risk before setting the price.

!info A design decision :: Every assumption sits on the Inputs sheet in a shaded, unlocked cell with its own name (`TicketPrice`, `DemandAtZero`, `Capacity`). Volunteers can then only type in the right places (R5), and every formula reads as a sentence, which makes the formulas easier to test (R1) and the technical documentation shorter.

!info A formula, explained :: `=MIN(Capacity, MAX(0, DemandAtZero-LostPerPound*TicketPrice))`. MIN stops the model selling more tickets than the licensed capacity. MAX stops a high price producing a negative number of tickets, which test 5 found in the first version.

!info A test record :: Test 5, boundary data, a price of £60.00. Expected: 0 tickets and a loss of £4,000. Actual: −120 tickets and a loss of £10,600. Cause: the formula had no lower limit. Fix: added MAX(0, …). Retest: 0 tickets and a loss of £4,000. Passed.

!info An evaluation point :: R6 is partly met. Two of three volunteers could not find Goal Seek, which is three menus deep. A dashboard button running a Goal Seek macro would take the menus out of the task, and I would retest with the same volunteers to check it worked.
"""),
        Section("Before you hand in", """
+ Every requirement is numbered, testable, and traced through the design, the tests and the evaluation
+ Every sheet has an annotated design, and every input is in the data dictionary
+ No formula contains a typed-in assumption
+ Every input is validated, and every formula cell is protected
+ The test log includes boundary, invalid and erroneous data, with failures, fixes and retests
+ The outputs answer the client's question, with a recommendation and its uncertainty
+ Somebody who had never seen the model has followed the user guide
+ The evaluation gives a verdict and evidence for every requirement, and specific improvements
+ Every source is referenced, and any permitted use of AI is acknowledged
+ Files are saved as numbered versions, with the final version clearly named
"""),
        Section("Sources and further reading", """
- [OCR: IT Data Analytics (H019, H119)](%s): the qualification page, with the specification and assessment information your teacher works from.
- [The H019 and H119 specification (PDF)](%s): F202's content and how it is assessed.
- [JCQ: instructions for conducting non-examination assessments](https://www.jcq.org.uk/exams-office/non-examination-assessments/): the rules every centre follows for coursework.
- [JCQ: artificial intelligence](https://www.jcq.org.uk/exams-office/malpractice/artificial-intelligence/): what counts as misuse of AI, and how to acknowledge permitted use.
- [Office for National Statistics](https://www.ons.gov.uk/) and [data.gov.uk](https://www.data.gov.uk/): reliable data that is free to reuse, if your brief allows you to bring in data of your own.
""" % (OCR_PAGE, OCR_SPEC)),
    ],
    keyterms=[
        ("Non-examined assessment", "Assessment completed as coursework rather than as a timed written paper."),
        ("OCR-set assignment", "A brief with a scenario and tasks written by OCR and completed by students in centres."),
        ("Centre-assessed", "Marked first by the student's own teachers, against the board's criteria."),
        ("Moderation", "The board checking a sample of a centre's marking against the national standard."),
        ("Malpractice", "Breaking the assessment rules, such as submitting work that is not your own."),
        ("Harvard referencing", "A system that cites sources by author and year in the text, with full details in a reference list."),
    ],
    grade="""
+ Read the brief closely, and write the client's needs in your own words
+ Keep every stage's evidence, including plans that later changed
+ Trace every requirement from the plan, through the tests, to the evaluation
+ Reference every source, and acknowledge any permitted use of AI
+ Save numbered versions, so your process is visible and your work is safe
""",
    mistakes=[
        "Starting to build before the planning is done.",
        "Throwing away the first plan when it changes, instead of recording why it changed.",
        "Copying wording from examples, including the ones on this site.",
        "Using an AI tool to write or build any part of the work you submit.",
        "Forgetting to reference data sources and images.",
        "Keeping one file that is overwritten all the way through.",
    ],
    quiz=[
        Q("What does 'OCR-moderated' mean?",
          ["OCR checks a sample of the centre's marking against the national standard",
           "OCR marks every student's work",
           "The work is sat as an exam",
           "The teacher writes the assignment"], 0,
          "Your teacher marks; OCR checks that marking is consistent with every other centre."),
        Q("Who marks F202 work first?",
          ["Your teacher, against OCR's marking criteria",
           "An OCR examiner", "Another student", "The client in the brief"], 0,
          "It is centre-assessed, then moderated."),
        Q("Which of these can your teacher NOT do?",
          ["Tell you exactly what to change in your work",
           "Explain what the criteria mean", "Give general feedback",
           "Teach the skills before the assignment"], 0,
          "Feedback has to stay general, so the work stays yours."),
        Q("Your centre allows an AI tool for one purpose, and you used it. What must you do?",
          ["Acknowledge it: the tool, what you asked and how you used the answer",
           "Nothing, if you changed the wording", "Delete the conversation",
           "Ask a friend to check it"], 0,
          "Permitted use still has to be acknowledged in full."),
        Q("Why keep numbered versions of your files?",
          ["They show how the model developed, and protect against lost work",
           "They are needed to open the file", "They make the file smaller",
           "They hide mistakes"], 0,
          "Versions are evidence of your process as well as a backup."),
        Q("Why do the examples on this site use an invented festival brief?",
          ["To show the quality of evidence without answering anybody's real assignment",
           "Because OCR assignments are about festivals",
           "Because festivals are easier to model", "So they can be copied"], 0,
          "The examples teach what good looks like. Your decisions must be your own."),
        Q("What should a Harvard reference to a web page include?",
          ["The author or organisation, year, title, URL and date accessed",
           "Only the URL", "Only the title", "The search words you used"], 0,
          "The access date matters because web pages change."),
        Q("How many guided learning hours does F202 have?",
          ["75", "15", "60", "120"], 0,
          "75 in total, of which 15 are for completing the set assignment."),
        Q("Which of these is malpractice?",
          ["Submitting a formula an AI tool wrote as your own work",
           "Asking your teacher what a criterion means",
           "Using ONS data and referencing it",
           "Testing your model with boundary data"], 0,
          "Work produced by an AI tool is not your own work."),
        Q("What should you do if you are unsure whether something is allowed?",
          ["Ask your teacher before doing it", "Do it and mention it later",
           "Ask another student", "Assume it is allowed"], 0,
          "It is far easier to ask first than to undo malpractice afterwards."),
    ],
    exam=[
        EQ("Explain what is meant by an OCR-set assignment that is centre-assessed and OCR-moderated.", 3,
           [MP("OCR writes the assignment and its tasks", ["OCR writes", "OCR sets", "set by OCR", "scenario", "tasks"]),
            MP("The centre's teachers mark the work against OCR's criteria", ["teacher", "centre", "marks", "criteria", "assessed"]),
            MP("OCR checks a sample of the marking against the national standard", ["sample", "check", "standard", "consistent", "moderat"])],
           "An OCR-set assignment is a brief written by OCR, with a scenario, a client and tasks, which every centre uses rather than writing its own. Centre-assessed means the work is marked first by the student's own teachers, using OCR's marking criteria. OCR-moderated means OCR then checks a sample of each centre's marked work, and adjusts the marks if the centre has been more generous or more severe than the national standard, so that a mark means the same thing in every school.",
           command="Explain"),
        EQ("Explain why you must reference the sources you use in your coursework.", 3,
           [MP("It shows which work is yours and which is from others", ["your own", "others", "distinguish", "credit", "whose"]),
            MP("Not doing so can be plagiarism or malpractice", ["plagiar", "malpractice", "cheat", "rules", "zero"]),
            MP("It lets the reader check the source, or shows the data is reliable", ["check", "verify", "reliable", "find", "trust"])],
           "Referencing makes clear which parts of the work are your own and which come from other people, so you get credit for your own thinking and others get credit for theirs. Using someone else's words, images or data without saying so is plagiarism, which is malpractice and can lose you the marks or even the qualification. A reference also lets the reader find and check the source, which matters in a model whose assumptions rest on data: a demand figure taken from a named, reliable publisher is far more convincing than one with no source at all.",
           command="Explain"),
        EQ("Describe what makes test evidence convincing in a spreadsheet modelling assignment.", 4,
           [MP("Tests planned in advance from the requirements, with hand-calculated expected results", ["planned", "before", "expected", "by hand", "requirement"]),
            MP("A range of test data: normal, boundary, invalid and erroneous", ["normal", "boundary", "invalid", "erroneous", "range of"]),
            MP("Screenshots or formula views showing the actual results, annotated", ["screenshot", "formula view", "annotat", "actual", "show formulas"]),
            MP("Failures recorded with the cause, the fix and the retest", ["fail", "fix", "retest", "cause", "honest"])],
           "Convincing test evidence starts with a plan written before the model was built, from the requirements, with every expected result worked out by hand so there is an independent answer to compare with. It uses a range of test data, normal, boundary, invalid and erroneous, so it shows the model rejecting what it should reject as well as calculating what it should calculate. Each actual result is backed by a screenshot or the formula view, annotated to say what it proves. And it records the failures honestly, with the cause, the fix and the retest, because a log where everything passed first time looks like a log written to pass.",
           command="Describe"),
    ],
)

TOPICS = [F_PRINCIPLES, F_PLANNING, F_CREATING, F_DELIVERING, F_EVALUATING, F_GUIDE]
