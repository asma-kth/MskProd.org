"""OCR Cambridge Advanced National in IT: Data Analytics, H019 and H119.

The two externally assessed units, and the mandatory coursework unit:

  F200  Fundamentals of data analytics   75 GLH   written exam, 1h 15m, 60 marks
  F201  Big data and machine learning    70 GLH   written exam, 1h 30m, 60 marks
  F202  Spreadsheet data modelling       75 GLH   OCR-set assignment, centre-assessed
                                                  and OCR-moderated

F200 and F202 are mandatory in both the Certificate (H019) and the Extended
Certificate (H119). F201 is part of the Extended Certificate. F202 lives in
content/data_analytics_f202.py, because it is coursework and is written
differently: no paper to practise for, and every worked example built on one
invented brief.

The topic area headings follow OCR's published unit structure. Awarding bodies
revise specifications, so check the current H019 and H119 specification on
ocr.org.uk against this before relying on a heading or a mark total; the
teaching content itself is standard data analytics and does not move.

The exam-style questions here match the command words, tariffs and scenario
style of the real papers, and the extended answers use the same
levels-of-response shape. They are practice in that form, not copies of OCR
past papers, which are OCR's copyright.
"""
from mskbuild.models import Topic, Section, Unit, Course, Q, EQ, MP
from content.data_analytics_f202 import TOPICS as F202_TOPICS

# ============================================================== F200 TA1

D_UNDERSTANDING = Topic(
    slug="understanding-data",
    title="F200 TA1: Understanding Data",
    spec="F200 TA1",
    icon="i-database",
    minutes=28,
    blurb="What data actually is, how it differs from information and knowledge, the types it comes in, and the formats it is stored in.",
    fact="A supermarket's loyalty scheme once worked out that a customer was pregnant before her family knew, purely from a change in which unscented products she bought. No single purchase said anything. The pattern across all of them did.",
    sections=[
        Section("Data, information, knowledge and wisdom", """
These four words are used loosely in conversation and precisely in this unit. The difference is what has been added at each stage.

| Term | What it is | Example |
| **Data** | Raw facts and figures, with no context | `37.2`, `A1402`, `2026-03-14` |
| **Information** | Data given context and structure, so it means something | "Patient A1402's temperature was 37.2 °C on 14 March 2026" |
| **Knowledge** | Information combined with experience and interpretation | "That reading is within the normal range for this patient" |
| **Wisdom** | Knowledge applied to make a judgement about what to do | "No action needed, but review if it rises for three consecutive days" |

Each step upward adds something and loses something. Data is precise and useless on its own. Wisdom is useful and cannot be stored in a database.

### Why this matters in practice

An organisation that collects data and never turns it into information has spent money on storage and gained nothing. The whole point of an analytics pipeline is to move left to right across that table, and most of the technical work is in the first two steps.

!key The exam phrasing :: A question asking for the difference between data and information wants the word **context**. Data on its own carries no meaning; information is data that has been given structure, units, labels and a reference point.
"""),
        Section("Types and classifications of data", """
### Quantitative and qualitative

- **Quantitative** data is numerical: counts, measurements, amounts. It can be calculated with.
- **Qualitative** data is descriptive: words, categories, opinions, images. It can be counted and grouped but not averaged.

### Discrete and continuous

- **Discrete** values can only take particular values, usually whole numbers: the number of students in a class, the number of orders.
- **Continuous** values can take any value in a range, limited only by the precision of measurement: height, temperature, time taken.

### Levels of measurement

| Level | What it allows | Example |
| **Nominal** | Named categories with no order | Payment method, country, colour |
| **Ordinal** | Ordered categories with uneven gaps | Satisfaction: poor, fair, good, excellent |
| **Interval** | Ordered with equal gaps, no true zero | Temperature in °C, calendar years |
| **Ratio** | Ordered, equal gaps, a true zero | Height, weight, income, duration |

The level decides which calculations are legitimate. A mean of nominal data is meaningless. A mean of ordinal data is common and technically dubious: the gap between "poor" and "fair" is not the gap between "good" and "excellent".

### Structure

| Structure | What it means | Examples |
| **Structured** | Fits a fixed schema of rows and columns | Relational database tables, CSV files, spreadsheets |
| **Semi-structured** | Has tags or markers but no fixed schema | JSON, XML, email, log files |
| **Unstructured** | No predefined model at all | Free text, images, audio, video, documents |

Most of the data an organisation holds is unstructured, and most of the data it actually analyses is structured. Closing that gap is a large part of what data engineering is.

### Other distinctions worth the vocabulary

- **Primary** data: collected by you, for this purpose. **Secondary** data: collected by somebody else for theirs.
- **Internal** data: generated by the organisation. **External** data: bought, licensed or taken from open sources.
- **Metadata**: data about data. The file size, the capture time, the camera, the column types, the author, the schema.
- **Open data**: published for anyone to use, often by government, usually under a permissive licence.
"""),
        Section("Data file formats", """
The format decides what can be stored, how large the file is, and what can read it.

| Format | Structure | Good at | Weak at |
| **CSV** | Structured, plain text | Universally readable, tiny, simple | No types, no nesting, breaks on commas in fields |
| **TSV** | Structured, plain text | As CSV, safer with commas | Same limitations otherwise |
| **JSON** | Semi-structured | Nesting, APIs, mixed types, human readable | Verbose, slow to parse at scale |
| **XML** | Semi-structured | Schemas, validation, long-lived documents | Very verbose |
| **XLSX** | Structured | Formulas, formatting, multiple sheets | Proprietary, size limits, easy to corrupt by hand |
| **SQL / database** | Structured | Relationships, integrity, concurrent access, querying | Needs a server and a schema |
| **Parquet** | Structured, columnar, binary | Compressed, fast on huge analytic queries | Not human readable, needs tooling |
| **TXT** | Unstructured | Anything | Nothing is guaranteed |
| **PDF** | Unstructured for data purposes | Fixed presentation | Extracting data from it is painful and error prone |

### Row stores and column stores

A **row-oriented** file or table keeps each record together, which suits writing one order at a time and reading whole records. A **column-oriented** format such as Parquet keeps each field together, which suits reading one column across ten million records. If the question is "what is the average order value this year", a columnar format reads one column instead of every field of every row, and that is why analytic warehouses are built that way.

### Choosing a format

- Sharing a small table with anyone: **CSV**
- An API response, or anything nested: **JSON**
- A document that must validate against a schema: **XML**
- A finished model with formulas for a human to use: **XLSX**
- Many related entities, many users, guaranteed integrity: **a database**
- Hundreds of millions of rows to analyse: **Parquet** in a data lake

!warn CSV is not a data type :: A CSV has no idea whether `0123` is a number or a product code, or whether `03/04/2026` is March or April. Every CSV import needs the types declared, and leading zeros and dates are where real analyses silently go wrong.
"""),
    ],
    keyterms=[
        ("Data", "Raw facts and figures with no context attached."),
        ("Information", "Data given context and structure so that it carries meaning."),
        ("Knowledge", "Information combined with experience and interpretation."),
        ("Quantitative data", "Numerical data that can be calculated with."),
        ("Qualitative data", "Descriptive, non-numerical data such as words, categories or images."),
        ("Discrete data", "Data that can take only particular values, usually whole numbers."),
        ("Continuous data", "Data that can take any value within a range."),
        ("Nominal data", "Named categories with no inherent order."),
        ("Ordinal data", "Ordered categories where the gaps between them are not equal."),
        ("Structured data", "Data that fits a fixed schema of rows and columns."),
        ("Semi-structured data", "Data with tags or markers but no fixed schema, such as JSON or XML."),
        ("Unstructured data", "Data with no predefined model, such as free text, images or video."),
        ("Metadata", "Data about data: its size, origin, structure, author or capture time."),
        ("Open data", "Data published for anyone to use, usually under a permissive licence."),
    ],
    grade="""
The marks at Level 3 are in **precision of vocabulary and consequence**. Not "JSON is good for APIs" but "JSON is used for API responses because it supports nesting, so a single response can carry an order and its line items together, which a flat CSV cannot represent without repeating the order header on every row."
""",
    mistakes=[
        "Using 'data' and 'information' interchangeably. The difference is context, and it is examined.",
        "Calling a spreadsheet unstructured. It has rows, columns and a schema, so it is structured.",
        "Averaging ordinal data, such as treating satisfaction ratings as numbers, without acknowledging the problem.",
        "Forgetting that CSV carries no type information, which is where leading zeros and dates break.",
        "Confusing metadata with the data itself.",
        "Assuming unstructured data is unusable. Most organisational data is unstructured.",
    ],
    quiz=[
        Q("Which of these is data rather than information?",
          ["37.2", "Patient A1402's temperature was 37.2 °C",
           "The patient's temperature is normal", "Review if it rises for three days"], 0,
          "A bare value with no context is data. Adding the patient, the unit and the date makes it information."),
        Q("A survey records satisfaction as poor, fair, good or excellent. What level of measurement is that?",
          ["Ordinal", "Nominal", "Interval", "Ratio"], 0,
          "The categories have an order, but the gaps between them are not equal, so it is ordinal."),
        Q("Which format is best suited to an API response containing nested data?",
          ["JSON", "CSV", "XLSX", "Parquet"], 0,
          "JSON supports nesting, so an order and its line items fit in one response."),
        Q("Height measured in centimetres is an example of:",
          ["Continuous ratio data", "Discrete nominal data",
           "Continuous ordinal data", "Discrete interval data"], 0,
          "It can take any value in a range and has a true zero, so it is continuous and ratio."),
        Q("Which of these is semi-structured data?",
          ["An XML document", "A relational database table",
           "A photograph", "A CSV file"], 0,
          "XML has tags and hierarchy but no fixed row and column schema."),
        Q("What is metadata?",
          ["Data about data, such as its size, origin or schema",
           "Data that has been anonymised", "The most important data in a set",
           "Data stored in the cloud"], 0,
          "It describes the data rather than being the data itself."),
        Q("Why is a columnar format such as Parquet faster for analytics?",
          ["A query can read one column without reading every field of every row",
           "It stores fewer records", "It is uncompressed",
           "It only works on small files"], 0,
          "Analytic queries touch few columns across many rows, which is exactly what columnar storage optimises."),
        Q("A product code 0123 is imported from a CSV and becomes 123. Why?",
          ["CSV carries no type information, so it was read as a number",
           "The file was corrupted", "CSV cannot store four characters",
           "The code was invalid"], 0,
          "Types have to be declared on import, and this is the classic failure."),
        Q("Which is an example of unstructured data?",
          ["A folder of customer support emails", "A sales table",
           "A CSV export", "A spreadsheet of orders"], 0,
          "Free text has no predefined data model, even though it is full of information."),
        Q("Data bought from a market research company is:",
          ["Secondary and external", "Primary and internal",
           "Primary and external", "Secondary and internal"], 0,
          "Somebody else collected it, for their own purpose, outside your organisation."),
    ],
    exam=[
        EQ("State **two** differences between structured and unstructured data.", 2,
           [MP("Structured data fits a fixed schema of rows and columns", ["schema", "rows and columns", "fixed", "table", "fields"]),
            MP("Unstructured data has no predefined model, with an example", ["no", "model", "free text", "images", "video", "audio", "documents"])],
           "Structured data fits a fixed schema of rows and columns, such as a database table, whereas unstructured data has no predefined data model at all, such as free text, images or video.",
           command="State"),
        EQ("Explain the difference between data, information and knowledge, using one example throughout.", 4,
           [MP("Data defined as raw facts without context", ["raw", "no context", "facts", "figures", "on its own"]),
            MP("Information defined as data given context", ["context", "meaning", "structure", "labels", "units"]),
            MP("Knowledge defined as information plus experience or interpretation", ["experience", "interpretation", "understanding", "judgement", "pattern"]),
            MP("A single example carried through all three", ["for example", "37.2", "temperature", "reading", "sales figure"])],
           "Data is a raw fact with no context attached: the value 37.2 on its own says nothing, because it could be a temperature, a price or a percentage. Information is that data given context and structure, so 'patient A1402's temperature was 37.2 degrees Celsius on 14 March' now means something, because it has a subject, a unit and a time. Knowledge is that information combined with experience and interpretation: a clinician knows that 37.2 is within the normal range for an adult, which is a judgement the database itself cannot hold. Each step adds something the previous one lacked, and the whole purpose of an analytics process is to move from the first to the third.",
           command="Explain"),
        EQ("A retailer exports its daily sales to a file that is read by a spreadsheet, a reporting tool and a Python script.\n\nJustify the use of CSV for this export, and identify **two** risks it introduces.", 6,
           [MP("CSV is readable by every tool without special software", ["every", "universal", "any tool", "plain text", "no software", "widely supported"]),
            MP("It is small and simple to produce", ["small", "simple", "lightweight", "easy to generate", "fast"]),
            MP("Risk: no type information", ["no types", "type", "leading zero", "dates", "treated as a number", "text or number"]),
            MP("The consequence of that risk", ["product code", "0123", "wrong date", "silently", "misread"]),
            MP("Risk: no nesting, or delimiter collisions", ["nesting", "flat", "comma in a field", "quoting", "escap", "repeat"]),
            MP("A mitigation is offered", ["schema", "data dictionary", "declare types", "quote", "TSV", "validate", "Parquet"])],
           "CSV is a reasonable choice here because all three consumers can read plain text without any shared library or licence: the spreadsheet opens it directly, the reporting tool imports it, and the Python script reads it in two lines. The files are small, trivial to generate from a database query and easy for a human to inspect when something looks wrong, which matters for a daily operational export. The first risk is that CSV carries no type information, so every consumer guesses: a product code of 0123 is read as the number 123, and a date written 03/04/2026 is March in one tool and April in another, and both failures are silent. The second risk is that the format is flat and delimited, so a product description containing a comma breaks the row alignment unless fields are properly quoted, and nested data such as an order with several line items has to be flattened by repeating the order header. Both risks are manageable: publish a data dictionary declaring each column's type and format, use ISO dates, quote all text fields, and move to Parquet or a database export if the volumes grow.",
           command="Justify"),
        EQ("Discuss the problems an organisation faces in using the unstructured data it already holds, such as emails, support calls and documents.", 8,
           [MP("Unstructured data has no schema to query", ["no schema", "cannot query", "no structure", "not in rows"]),
            MP("It must be processed before analysis", ["process", "extract", "transform", "text mining", "NLP", "transcri", "tag"]),
            MP("Volume is a problem", ["volume", "huge", "terabytes", "most of", "80%"]),
            MP("Storage and cost implications", ["storage", "cost", "data lake", "cloud", "expensive"]),
            MP("Quality and consistency problems", ["inconsistent", "spelling", "duplicate", "incomplete", "ambiguous", "quality"]),
            MP("Legal or privacy problems specific to this data", ["personal data", "GDPR", "consent", "purpose", "retention", "special category", "confidential"]),
            MP("A realistic approach is proposed", ["pipeline", "NLP", "classif", "metadata", "index", "sample", "prioritise", "start with"]),
            MP("A judgement weighing value against cost", ["worth", "value", "cost", "most organisations", "therefore", "only if"])],
           "The first problem is that unstructured data cannot be queried. A relational table can be aggregated with a single statement, whereas a folder of support emails has no fields, so there is nothing to group by and nothing to sum. Anything useful has to be created first, by extracting entities, classifying each message by topic and sentiment, transcribing recorded calls and attaching metadata, and all of that is a processing pipeline that has to be built, tuned and maintained rather than bought. The second problem is scale: unstructured content is the majority of what most organisations hold, and it is large per item, so storing it in a form that can be reprocessed means a data lake and the cloud costs that go with it. Quality is the third problem and the most underestimated. Free text is inconsistent by nature: the same product is spelled four ways, the same complaint is phrased differently by every customer, and sarcasm defeats sentiment analysis, so any measure derived from it carries error that is hard to quantify. Fourth, this data is legally the most dangerous the organisation holds. Support emails contain personal data the customer volunteered, sometimes including health information, which is special category data under the UK GDPR; it was collected to answer a query, not to train a model, so reusing it for analytics engages purpose limitation, and retention schedules are almost never applied to mailboxes. A workable approach is therefore narrow rather than total: pick one question worth answering, such as which product generates the most support contact, sample rather than process everything, classify that sample with a tested model, and keep a human check on the output. Judged overall, unstructured data is worth the effort only when a specific decision depends on it, because the cost of making it analysable is paid up front and in full, while the value is speculative until the first question has actually been answered.",
           command="Discuss"),
    ],
)

# ============================================================== F200 TA2

D_MANAGING = Topic(
    slug="managing-data",
    title="F200 TA2: Managing Data",
    spec="F200 TA2",
    icon="i-flow",
    minutes=30,
    blurb="The data lifecycle and the analytics pipeline, how data is gathered, stored and transformed, and what data quality actually means.",
    fact="Analysts consistently report spending the majority of their time finding, cleaning and reshaping data rather than analysing it. The modelling is the part that gets taught; the cleaning is the part that fills the week.",
    sections=[
        Section("The data lifecycle and the analytics pipeline", """
### The data lifecycle

Data has a life, and each stage has its own risks and its own legal duties.

| Stage | What happens | The risk here |
| **Create or capture** | Data is generated or collected | Collecting more than you need, or capturing it wrong |
| **Store** | It is written somewhere durable | Insecure storage, no backup, wrong location |
| **Use and process** | It is queried, analysed, shared | Using it for a purpose it was not collected for |
| **Share or publish** | It goes to another system or person | Disclosure, re-identification, loss in transit |
| **Archive** | It is moved to cheaper, colder storage | Forgetting it exists while remaining responsible for it |
| **Destroy** | It is securely deleted | Keeping it past its retention period |

### The analytics pipeline

| Step | What it produces |
| **1. Define the question** | A decision somebody will actually make differently |
| **2. Collect** | Raw data from systems, surveys, sensors, APIs, open sources |
| **3. Clean and prepare** | Data fit to analyse: typed, complete, consistent, deduplicated |
| **4. Transform** | Joined, aggregated, derived fields, the right grain |
| **5. Analyse** | Patterns, comparisons, correlations, models |
| **6. Visualise and communicate** | A chart and a sentence somebody can act on |
| **7. Act and monitor** | A decision, and a measurement of whether it worked |

!key Start at step one, not step two :: A pipeline built without a question produces a dashboard nobody opens. The first step is naming the decision that will be made differently depending on what the data says. If no decision changes, there is nothing to analyse.
"""),
        Section("Gathering and storing data", """
### Methods of gathering

| Method | Produces | Watch out for |
| **Operational systems** | Transactions, orders, logs, bookings | Captures what the business does, not what customers wanted |
| **Surveys and forms** | Direct answers at scale | Self report error, leading questions, low response rates |
| **Interviews and focus groups** | Reasons behind the numbers | Small samples, interviewer effects |
| **Observation and user testing** | What people actually do | Costly, small, people behave differently when watched |
| **Sensors and IoT** | High volume, high velocity readings | Drift, failure, gaps, enormous volume |
| **Web and app analytics** | Behaviour, funnels, devices | Consent requirements, blocking, bot traffic |
| **APIs** | Live data from another system | Rate limits, changes without notice, terms of use |
| **Open and purchased data** | Scale and context you cannot generate | Licence terms, age, different definitions |

### Where it is stored

| Store | What it is for |
| **Relational database (OLTP)** | Running the business: many small reads and writes, strict integrity |
| **Data warehouse (OLAP)** | Analysing the business: large reads over structured, modelled data |
| **Data lake** | Keeping everything, structured or not, in its raw form for later |
| **Data mart** | A subject-specific slice of a warehouse for one team |
| **NoSQL store** | Documents, key-values, graphs or wide columns, where a fixed schema does not fit |
| **Cloud object storage** | Cheap, durable storage of files at any scale |
| **Spreadsheet** | A model, a prototype or a small one-off. Not a database |

### Schema on write and schema on read

A warehouse enforces the structure when data is **written**, so everything in it is clean and consistent and anything that does not fit is rejected. A lake accepts data as it arrives and applies structure when it is **read**, so nothing is lost but nothing is guaranteed either. The modern pattern is both: a lake for raw retention, a warehouse for the modelled data people actually query.

!warn A spreadsheet is not a database :: No concurrency control, no referential integrity, no audit trail, a row limit, and one person's accidental sort destroys the whole thing. Spreadsheets are superb modelling tools and dangerous systems of record.
"""),
        Section("Transformation, data quality and assurance", """
### ETL and ELT

- **ETL** — Extract, Transform, Load. Clean and reshape the data on the way in, so only modelled data lands. Traditional warehouse practice.
- **ELT** — Extract, Load, Transform. Land the raw data first, transform it inside the warehouse. Cheaper compute makes this the common modern choice, and it keeps the raw data for re-processing.

### What cleaning actually involves

| Problem | What to do about it |
| **Missing values** | Decide per field: drop the row, impute a value, or keep it as explicitly unknown. Record which |
| **Duplicates** | Define what makes two records the same, then deduplicate on that key |
| **Inconsistent formats** | Standardise dates to ISO, phone numbers, capitalisation, units |
| **Inconsistent categories** | "UK", "U.K.", "United Kingdom", "GB" are one category spelled four ways |
| **Outliers** | Investigate before removing. An outlier is sometimes the most important record |
| **Wrong types** | Declare types on import rather than letting the tool guess |
| **Structural errors** | Trailing spaces, mojibake, merged cells, header rows inside the data |

### The dimensions of data quality

| Dimension | The question it answers |
| **Accuracy** | Does it match reality? |
| **Completeness** | Is anything missing that should be there? |
| **Consistency** | Do two systems agree? |
| **Timeliness** | Is it current enough for the decision? |
| **Validity** | Does it conform to the rules and the format? |
| **Uniqueness** | Is each real thing represented exactly once? |
| **Relevance** | Does it bear on the question being asked? |

### Validation and verification

- **Validation** is automated and checks that data is *reasonable*: a range check, a type check, a format check, a presence check, a lookup against a list, a check digit.
- **Verification** checks that data is *correct*: double entry, a read-back, a visual check against the source document.

Validation will happily accept a perfectly formatted wrong answer. Verification is the only thing that catches it, and it needs a human or a second source.

### Data assurance and governance

- A **data dictionary**: every field, its type, its format, its permitted values, its meaning
- **Ownership**: a named person accountable for each dataset
- An **audit trail**: who changed what, when
- **Lineage**: where each figure came from and what was done to it
- **Documented cleaning**: the decisions taken, so a result can be reproduced

!grade The sentence that earns the mark :: "Removing the 14 rows with a missing postcode would have biased the result, because those orders were all from one warehouse whose system does not capture postcodes, so they were kept and flagged instead." That is data quality reasoning, and it is what the longer questions reward.
"""),
    ],
    keyterms=[
        ("Data lifecycle", "The stages data passes through from creation to secure destruction."),
        ("Data pipeline", "The sequence of steps that takes raw data through to a decision."),
        ("ETL", "Extract, Transform, Load: data is cleaned and reshaped before it is loaded."),
        ("ELT", "Extract, Load, Transform: raw data is loaded first and transformed in place."),
        ("Data warehouse", "A store of structured, modelled data optimised for analysis."),
        ("Data lake", "A store holding raw data of any structure for later processing."),
        ("OLTP", "Online transaction processing: a system optimised for many small reads and writes."),
        ("OLAP", "Online analytical processing: a system optimised for large analytical queries."),
        ("Data cleaning", "Correcting or removing inaccurate, incomplete, duplicated or malformed data."),
        ("Validation", "An automated check that data is of the right type, format or range."),
        ("Verification", "A check that data is actually correct, usually against a second source."),
        ("Data dictionary", "Documentation defining every field, its type, format, permitted values and meaning."),
        ("Data lineage", "A record of where data came from and every transformation applied to it."),
        ("Outlier", "A value far from the rest of the distribution."),
    ],
    grade="""
Top answers treat cleaning as a set of **decisions with consequences**, not a checklist. Say what you did about the missing values, why that choice rather than the alternative, and what bias the alternative would have introduced. That is the difference between describing a process and understanding it.
""",
    mistakes=[
        "Confusing validation with verification. Validation checks plausibility; verification checks truth.",
        "Deleting outliers automatically. Investigate first, because the outlier is sometimes the finding.",
        "Dropping every row with a missing value without checking whether the missing rows share a cause.",
        "Confusing a data warehouse with a data lake, or either with a database used to run the business.",
        "Treating a spreadsheet as a system of record.",
        "Starting with the data rather than with the question the data is supposed to answer.",
    ],
    quiz=[
        Q("What does the T in ETL stand for, and when does it happen?",
          ["Transform, before the data is loaded", "Transfer, after loading",
           "Transform, after loading", "Transmit, during extraction"], 0,
          "ETL transforms on the way in; ELT loads first and transforms in place."),
        Q("Which is the best description of a data lake?",
          ["Raw data of any structure, kept for later processing",
           "Modelled, structured data optimised for queries",
           "A subject-specific slice of a warehouse",
           "A database used to run day to day operations"], 0,
          "A lake applies structure on read; a warehouse applies it on write."),
        Q("A form rejects a date of 31/02/2026. What kind of check is that?",
          ["Validation", "Verification", "Deduplication", "Imputation"], 0,
          "It is an automated check that the value is possible, which is validation."),
        Q("Double entry of a customer reference by two operators is an example of:",
          ["Verification", "Validation", "A range check", "Normalisation"], 0,
          "It checks the value is actually correct, not merely plausible."),
        Q("'UK', 'U.K.', 'United Kingdom' and 'GB' appear in one column. What problem is this?",
          ["Inconsistent categories", "Missing values",
           "Outliers", "Wrong data types"], 0,
          "One real category spelled four ways, which splits every grouping four ways."),
        Q("Why should an outlier be investigated before removal?",
          ["It may be the most important record in the set",
           "Removing data is never allowed", "Outliers are always errors",
           "It will reappear after cleaning"], 0,
          "A fraud, a fault or a record-breaking order all look like outliers."),
        Q("Which data quality dimension asks whether two systems agree?",
          ["Consistency", "Accuracy", "Validity", "Timeliness"], 0,
          "Consistency is about agreement between sources holding the same fact."),
        Q("What is a data dictionary for?",
          ["Defining every field's type, format, permitted values and meaning",
           "Translating data between languages",
           "Storing the data itself", "Listing the organisation's databases"], 0,
          "It is the documentation that makes a dataset usable by somebody who did not build it."),
        Q("Which system type suits many small reads and writes with strict integrity?",
          ["OLTP, a transactional database", "OLAP, a warehouse",
           "A data lake", "Object storage"], 0,
          "Running the business is transactional; analysing it is analytical."),
        Q("What should the first step of an analytics project be?",
          ["Defining the decision the analysis will inform",
           "Collecting as much data as possible",
           "Choosing a visualisation tool", "Cleaning the data"], 0,
          "Without a decision that could change, there is nothing to analyse."),
    ],
    exam=[
        EQ("Identify **three** stages of the data lifecycle.", 3,
           [MP("One valid stage", ["create", "capture", "collect", "store", "process", "use", "share", "archive", "destroy", "delete"]),
            MP("A second, different stage", ["store", "process", "share", "archive", "destroy", "use"]),
            MP("A third, different stage", ["archive", "destroy", "share", "process", "store"])],
           "Capture, storage, and secure destruction.",
           command="Identify"),
        EQ("Explain the difference between validation and verification, giving an example of each.", 4,
           [MP("Validation defined as an automated plausibility check", ["automatic", "plausible", "reasonable", "format", "range", "type", "rules"]),
            MP("A valid example of validation", ["range check", "format check", "presence check", "type check", "lookup", "check digit", "date"]),
            MP("Verification defined as a check that the data is actually correct", ["correct", "accurate", "matches", "against the source", "true"]),
            MP("A valid example of verification", ["double entry", "read back", "proof", "compare with", "visual check", "second source"])],
           "Validation is an automated check that a value is plausible: that it is the right type, within an acceptable range, in the correct format, present at all, or matches an entry in a permitted list. Rejecting a date of 31 February is validation. Verification checks that the value is actually correct rather than merely possible, which generally needs a human or a second source: entering a customer reference twice and comparing the two, or reading a figure back against the original document. The distinction matters because validation will happily accept a perfectly formatted wrong answer, and only verification catches that.",
           command="Explain"),
        EQ("A charity has merged two supporter databases. The combined file has 48,000 rows, some supporters appear twice, dates are in two different formats and 1,200 rows have no email address.\n\nDescribe the steps you would take to prepare this data for analysis.", 6,
           [MP("Profile the data before changing anything", ["profile", "examine", "look at", "count", "inspect", "summar"]),
            MP("Standardise the date formats", ["date", "ISO", "format", "standardise", "yyyy"]),
            MP("Define a key for identifying duplicates", ["key", "match", "same person", "name and postcode", "email", "identify duplicates"]),
            MP("Deduplicate, keeping the better record", ["dedup", "merge", "keep the most recent", "combine", "remove duplicate"]),
            MP("Handle the missing emails deliberately rather than deleting rows", ["flag", "keep", "unknown", "not delete", "investigate", "why missing"]),
            MP("Document the decisions, or validate the result", ["document", "record", "data dictionary", "audit", "lineage", "check the count", "reconcile"])],
           "I would profile the file before changing anything: row counts per source, the distinct values in each column, the pattern of the two date formats and a count of the blanks, so there is a baseline to reconcile against afterwards. Dates would be standardised to a single ISO format, converting each source separately rather than letting one tool guess, because the two formats are ambiguous for days of twelve or less. Deduplication needs a definition before it needs code: I would agree the matching key, probably email where present and surname plus postcode where not, then review a sample of the proposed matches before merging, keeping the most recently updated record for each field and preserving both source identifiers. The 1,200 missing emails would be flagged rather than deleted, and I would check whether they share a cause, because if they all come from one source then deleting them would quietly remove that source from every result. Finally I would document every decision in a data dictionary alongside a reconciliation of the final row count against the two originals, so that the figures can be explained and the process repeated.",
           command="Describe"),
        EQ("A company's monthly sales report disagrees with the figure produced by its finance team.\n\nDiscuss the data quality issues that could cause this, and how the company should prevent it recurring.", 8,
           [MP("Different definitions of the same measure", ["definition", "what counts as a sale", "gross", "net", "VAT", "returns", "different measure"]),
            MP("Timing or timeliness differences", ["timing", "cut off", "date", "when", "posted", "as at", "timezone"]),
            MP("Duplicates or missing records", ["duplicate", "missing", "incomplete", "double counted"]),
            MP("Different sources or systems", ["two systems", "different source", "spreadsheet", "export", "warehouse"]),
            MP("Manual handling introducing error", ["manual", "copy", "spreadsheet", "by hand", "sort", "paste"]),
            MP("A single source of truth is proposed", ["single source of truth", "one source", "warehouse", "agreed dataset"]),
            MP("Governance measures are proposed", ["data dictionary", "owner", "definition", "lineage", "audit", "automate", "reconcil"]),
            MP("A judgement about the root cause", ["most likely", "root cause", "usually", "therefore", "the real problem"])],
           "The most common cause is not an error at all but a difference in definition: the sales report may be counting gross order value including VAT at the point of order, while finance counts net revenue excluding VAT and only once the order has shipped and not been returned. Both numbers are correct and they measure different things. Timing is the next candidate: a month-end cut off taken at midnight in one timezone and at close of business in another will move orders between months, as will counting by order date in one system and posting date in the other. Beyond definition and timing come genuine quality problems: duplicated rows from a reimported export, missing records from a channel whose feed failed silently, and the two teams drawing from different systems, typically an operational database on one side and a warehouse or a hand-built spreadsheet on the other. Manual handling makes all of this worse, because every copy, paste and sort is an opportunity for a row to be lost without trace. Prevention is mostly governance rather than technology. The company should agree a single source of truth for sales and publish a data dictionary defining the measure precisely, including VAT treatment, returns, cancellations and the cut off rule. Each dataset needs a named owner, automated extraction rather than manual export, recorded lineage so any figure can be traced to its source, and a monthly reconciliation between the two reports that has to be explained rather than ignored. The root cause in cases like this is almost always definitional, which is why the fix is a written definition both teams have signed up to, not a more sophisticated report.",
           command="Discuss"),
    ],
)

# ============================================================== F200 TA3

D_PLATFORMS = Topic(
    slug="data-across-platforms",
    title="F200 TA3: Accessing Data Across Platforms",
    spec="F200 TA3",
    icon="i-network",
    minutes=28,
    blurb="APIs, interoperability, access control and the cloud: how data gets from one system to another, and who is allowed to see it.",
    fact="A public API is a promise. When a large platform changes or withdraws one, thousands of applications built on it break at the same moment, which is why serious integrations are versioned and monitored rather than simply used.",
    sections=[
        Section("APIs and moving data between systems", """
An **API**, an application programming interface, is a defined way for one system to ask another for data or ask it to do something, without either knowing how the other works inside.

### A REST API request, in order

1. The client sends a **request** to an **endpoint**, a URL such as `/api/v1/orders`
2. It uses an HTTP **method**: `GET` to read, `POST` to create, `PUT` or `PATCH` to update, `DELETE` to remove
3. It includes **parameters** to filter or page the data, and **headers** carrying the **API key** or token
4. The server **authenticates** the key, **authorises** the action, and runs the query
5. It returns a **status code** and a **response body**, usually JSON
6. The client **parses** the response and handles errors and paging

| Status | Meaning |
| `200` | OK |
| `201` | Created |
| `400` | Bad request: your parameters are wrong |
| `401` | Unauthenticated: no valid key |
| `403` | Forbidden: valid key, not allowed to do this |
| `404` | Not found |
| `429` | Too many requests: you have hit the rate limit |
| `500` | Server error: their fault, not yours |

### Why an organisation uses an API rather than a file

- **Live** rather than a snapshot that is stale the moment it is written
- **Only the data you asked for**, filtered server-side
- **Controlled**: keys can be scoped, logged, revoked and rate limited
- **Stable contract**: the provider can change their internals without breaking you
- **Auditable**: every request is attributable to a key

### What to plan for

- **Rate limits** and the `429` response, which means back off and retry later
- **Paging**: large results arrive in pages, and code that reads only the first page silently loses data
- **Versioning**: build against `/v1/`, and watch for deprecation notices
- **Authentication**: keys in a secrets store or environment variable, never in the code or the repository
- **Terms of use**: an API being technically open does not make the data free to republish

!key Authentication against authorisation :: Authentication is proving who you are. Authorisation is what you are then allowed to do. A `401` means the system does not know you; a `403` means it knows you and the answer is still no.
"""),
        Section("Interoperability and integration patterns", """
**Interoperability** is the ability of different systems to exchange data and use it meaningfully. It needs agreement at three levels, and failing any one of them breaks the exchange.

| Level | What has to be agreed | Failure looks like |
| **Technical** | The transport and format: HTTPS, JSON, CSV, SFTP | The file cannot be read at all |
| **Syntactic** | The structure: field names, nesting, encoding, date format | The file parses but fields land in the wrong place |
| **Semantic** | The meaning: what "customer" counts as, what "active" means | Everything imports cleanly and the numbers are wrong |

Semantic failures are the dangerous ones, because nothing errors.

### Patterns for getting data from A to B

| Pattern | How it works | Suits |
| **Manual export and import** | Somebody downloads a file and uploads it | One-off work only |
| **Scheduled batch** | A file or extract transferred on a timetable | Nightly reporting |
| **API pull** | Your system requests data when it needs it | Live lookups, moderate volume |
| **Webhook push** | Their system notifies yours when something changes | Near real time, low volume |
| **Streaming** | A continuous flow of events | Sensors, telemetry, fraud detection |
| **Direct database access** | One system queries another's database | Rarely wise: it couples you to their schema |

### Standards that make interoperability possible

Shared formats (JSON, XML, CSV), shared identifiers (ISO country codes, ISBN, UUIDs), shared schemas within a sector, shared character encoding (UTF-8), and shared time representation (ISO 8601 with a timezone). Every one of these exists because somebody's integration broke without it.
"""),
        Section("Access control, security and the cloud", """
### Controlling who sees what

| Control | What it does |
| **Authentication** | Establishes identity: password, passkey, certificate, token |
| **Multi-factor authentication** | Requires something else as well as the password |
| **Authorisation** | Decides what that identity may do |
| **Role-based access control** | Permissions attach to roles, and people are given roles |
| **Least privilege** | Everyone gets the minimum access their job needs, and no more |
| **Row and column level security** | Restricts which rows or which fields a user can see within one table |
| **Audit logging** | Records who accessed what, which is itself a control |
| **Separation of duties** | The person who requests a change is not the person who approves it |

### Protecting the data itself

- **Encryption in transit**: TLS, so an intercepted request is unreadable
- **Encryption at rest**: the stored file or disk is encrypted
- **Hashing**: passwords are hashed and salted, never stored or encrypted
- **Masking and redaction**: showing only the last four digits of a card
- **Pseudonymisation**: replacing identifiers with a key held separately. Still personal data
- **Anonymisation**: removing identifiers irreversibly. No longer personal data, and genuinely hard to achieve
- **Backup**: the 3-2-1 rule, three copies, two media, one off site, and a restore that has actually been tested

### Cloud and on-premise

| | Cloud | On-premise |
| **Cost shape** | Operating cost, pay for use | Capital cost up front |
| **Scaling** | Minutes, and down again | Buy, rack and configure |
| **Maintenance** | The provider patches the platform | Your team patches everything |
| **Resilience** | Multiple regions available by default | Whatever you build and pay for |
| **Control** | Constrained by the provider's options | Complete |
| **Data location** | Must be chosen and checked | Known by definition |
| **Risk** | Provider outage, lock-in, misconfiguration | Your own failures, and no one else to call |

**Hybrid** is the common reality: sensitive or regulated data on premise, elastic analytics workloads in the cloud.

!warn The most common cloud breach is not an attack :: It is a storage bucket left public by mistake. The platform's security was never the weak point; the configuration was. Which is why access review is a scheduled task, not a one-off.
"""),
    ],
    keyterms=[
        ("API", "A defined interface letting one system request data or actions from another."),
        ("Endpoint", "The specific URL an API request is sent to."),
        ("API key", "A credential identifying the caller of an API so access can be controlled and logged."),
        ("Rate limit", "A cap on how many API requests a caller may make in a period."),
        ("Interoperability", "The ability of different systems to exchange data and use it meaningfully."),
        ("Webhook", "A message sent by one system to another when an event occurs."),
        ("Authentication", "Establishing who a user or system is."),
        ("Authorisation", "Determining what an authenticated user or system is permitted to do."),
        ("Role-based access control", "Granting permissions to roles and assigning roles to people."),
        ("Least privilege", "Giving each user only the access their role requires."),
        ("Encryption in transit", "Protecting data while it moves across a network, usually with TLS."),
        ("Encryption at rest", "Protecting stored data so the files or disks are unreadable without a key."),
        ("Pseudonymisation", "Replacing identifiers with a separately held key; the data remains personal data."),
        ("Anonymisation", "Irreversibly removing identifying information so data is no longer personal data."),
    ],
    grade="""
Questions here are nearly always **applied**. Name the mechanism, then say what attack or failure it prevents and what it costs. "Role-based access control, so a new analyst inherits exactly the permissions of their role rather than being granted them individually, which means access can be audited by role and removed in one change when they leave."
""",
    mistakes=[
        "Treating authentication and authorisation as the same thing.",
        "Forgetting paging, so only the first page of an API response is ever processed.",
        "Putting API keys in source code or a public repository.",
        "Calling pseudonymised data anonymous. If it can be reversed with a key, it is still personal data.",
        "Describing the cloud as automatically more or less secure, rather than differently configured.",
        "Claiming a backup exists without ever having tested a restore.",
    ],
    quiz=[
        Q("An API returns status 403. What does that mean?",
          ["You are authenticated but not allowed to do this",
           "Your key is missing or invalid", "The endpoint does not exist",
           "You have made too many requests"], 0,
          "401 is unauthenticated, 403 is authenticated but forbidden, 429 is rate limited."),
        Q("Which HTTP method is used to read data from an API?",
          ["GET", "POST", "DELETE", "PATCH"], 0,
          "GET reads; POST creates; PATCH and PUT update; DELETE removes."),
        Q("What does a 429 response mean you should do?",
          ["Back off and retry later", "Change your API key",
           "Switch to a different endpoint", "Report a server fault"], 0,
          "You have hit the rate limit, so the correct behaviour is to wait and retry."),
        Q("Two systems exchange a file that imports cleanly, but the totals are wrong because each defines 'active customer' differently. What kind of interoperability has failed?",
          ["Semantic", "Technical", "Syntactic", "Physical"], 0,
          "The transport and structure worked; the meaning did not match."),
        Q("What is the principle of least privilege?",
          ["Each user gets only the access their role requires",
           "Administrators have no access to data",
           "Access is granted only in emergencies",
           "Everyone has read access by default"], 0,
          "It limits the damage any one compromised account can do."),
        Q("Which is true of pseudonymised data?",
          ["It is still personal data, because it can be reversed with the key",
           "It is anonymous and outside data protection law",
           "It cannot be analysed", "It has been encrypted at rest"], 0,
          "The UK GDPR treats pseudonymised data as personal data."),
        Q("How should passwords be stored?",
          ["Hashed and salted", "Encrypted with a reversible key",
           "In plain text with restricted access", "In a separate spreadsheet"], 0,
          "Hashing is one way, so a breach does not expose the passwords themselves."),
        Q("What does the 3-2-1 backup rule say?",
          ["Three copies, two media, one off site",
           "Three backups a day, two weekly, one monthly",
           "Three administrators, two sites, one key",
           "Three tests, two restores, one archive"], 0,
          "And a restore that has actually been tested, or it is not a backup."),
        Q("Which is the most common cause of cloud data exposure?",
          ["Misconfigured access permissions", "Weak provider encryption",
           "Physical theft of servers", "Network interception"], 0,
          "Public buckets and over-broad permissions cause far more incidents than attacks on the platform."),
        Q("Why would an organisation use an API rather than a nightly CSV export?",
          ["The data is live and only the records requested are transferred",
           "APIs are always cheaper", "CSV cannot be automated",
           "APIs need no authentication"], 0,
          "A snapshot is stale immediately; an API answers the question now, and access can be scoped and revoked."),
    ],
    exam=[
        EQ("State what is meant by an API.", 2,
           [MP("A defined interface between two systems", ["interface", "allows", "communicate", "request", "connect"]),
            MP("Without either needing to know the other's internal workings, or for data or functionality", ["without knowing", "internal", "data", "functionality", "exchange"])],
           "An API is a defined interface that lets one system request data or functionality from another, without either system needing to know how the other works internally.",
           command="State"),
        EQ("Explain the difference between authentication and authorisation in a data system.", 4,
           [MP("Authentication establishes identity", ["who", "identity", "prove", "login", "credentials"]),
            MP("An example of authentication", ["password", "passkey", "MFA", "token", "certificate", "key"]),
            MP("Authorisation determines what is permitted", ["allowed", "permission", "what they can do", "rights", "access"]),
            MP("An example, or why the distinction matters", ["role", "read only", "cannot delete", "403", "401", "least privilege"])],
           "Authentication establishes who a user or system is, using something they know, have or are: a password with a second factor, a passkey, a certificate or an API token. Authorisation then determines what that identity is permitted to do, which is usually expressed through roles, so an analyst can read the sales table but not delete it and cannot see the payroll table at all. The distinction matters because the two fail differently: an HTTP 401 means the system does not recognise you, while a 403 means it recognises you perfectly well and the answer is still no, and fixing one would not fix the other.",
           command="Explain"),
        EQ("A hospital wants to give its research team access to patient records for analysis.\n\nExplain **three** access control measures that should be applied, and why each is necessary.", 6,
           [MP("Least privilege or role-based access control", ["least privilege", "role", "RBAC", "minimum"]),
            MP("Why it is necessary here", ["only what they need", "limit", "sensitive", "not all records", "damage"]),
            MP("Pseudonymisation or masking of identifiers", ["pseudonym", "mask", "remove name", "de-identif", "ID instead"]),
            MP("Why it is necessary here", ["special category", "health data", "identify a patient", "not needed for research", "GDPR"]),
            MP("Audit logging, or row and column level security", ["audit", "log", "who accessed", "row level", "column level"]),
            MP("Why it is necessary here", ["accountab", "detect misuse", "investigate", "evidence", "only their cohort"])],
           "The team's access should be role based and set to least privilege: a research role granted read-only access to the specific dataset the approved study needs, rather than individual grants on the live clinical system. That matters because health records are special category data under the UK GDPR, the research purpose is narrower than clinical care, and a role can be audited and withdrawn in one change when the study ends. The data should be pseudonymised before it reaches them, with names, addresses and NHS numbers replaced by a study identifier and the linking key held separately by the clinical team, because researchers almost never need to know which individual a record belongs to and removing that need removes most of the risk. Finally every access should be logged and reviewed, with row level security limiting each researcher to their approved cohort, because logging is what makes misuse detectable and investigable rather than merely prohibited, and a hospital has to be able to evidence who looked at a record and why.",
           command="Explain"),
        EQ("A growing company is deciding whether to keep its data warehouse on its own servers or move it to a cloud provider.\n\nDiscuss the factors it should consider and recommend an approach.", 8,
           [MP("Cost shape is compared", ["capital", "up front", "operating", "pay for use", "subscription", "cost"]),
            MP("Scalability is compared", ["scale", "elastic", "minutes", "buy hardware", "peak", "grow"]),
            MP("Maintenance and staffing are addressed", ["patch", "maintain", "staff", "expertise", "managed", "IT team"]),
            MP("Resilience and backup are addressed", ["resilience", "backup", "disaster", "region", "availability", "outage"]),
            MP("Security and configuration risk are addressed", ["security", "misconfigur", "encryption", "access", "breach"]),
            MP("Legal or data location issues are addressed", ["GDPR", "data location", "residency", "transfer", "jurisdiction", "contract", "processor"]),
            MP("A clear recommendation is made", ["recommend", "should", "I would", "best"]),
            MP("The recommendation is justified against the drawbacks raised", ["because", "therefore", "addresses", "outweigh", "however"])],
           "The decision turns on five factors. Cost shape comes first: on premise is a capital purchase that has to be sized for the busiest hour of the year and then sits idle, while cloud is an operating cost that tracks use, which suits a company whose volumes are growing and unpredictable but which becomes expensive if a steady, heavy workload is left running continuously. Scalability follows from that: cloud capacity changes in minutes and can be reduced again, whereas on premise growth means specifying, buying, racking and configuring hardware weeks in advance. Maintenance matters more than it first appears, because a growing company rarely has staff to spare: a managed cloud warehouse removes patching, backup and hardware replacement from a small team, and that reclaimed time is a real saving rather than an accounting one. Resilience favours cloud too, since multi-region redundancy and tested restores are available as configuration rather than as a second data centre. Against all that sit two genuine risks. Security does not improve automatically; the dominant cause of cloud data exposure is misconfiguration, so the company would need enforced encryption, role-based access, least privilege and scheduled access reviews. Legally, it must know and control where data physically sits, put a processor contract with appropriate safeguards in place, and check whether any dataset is subject to restrictions on international transfer. My recommendation is a cloud warehouse with a hybrid exception: move the analytical warehouse to the cloud, where the elasticity and reduced maintenance burden genuinely fit a growing company, and keep any regulated or special category data on premise or in a specifically contracted region. That answers the two drawbacks directly, because the configuration risk is addressed by governance the company needs in any case, and the legal risk is addressed by not moving the data that creates it.",
           command="Discuss"),
    ],
)

# ============================================================== F200 TA4

D_LEGAL = Topic(
    slug="legal-considerations",
    title="F200 TA4: Legal Considerations",
    spec="F200 TA4",
    icon="i-scales",
    minutes=28,
    blurb="The UK GDPR and the Data Protection Act 2018 applied to real analytics work, plus the other legislation an analyst has to know by name.",
    fact="The UK GDPR gives people the right to ask what an organisation holds about them, and the organisation has one month to answer. A single such request has forced more data clean-ups than any internal policy ever has, because you cannot answer it if you do not know what you hold.",
    sections=[
        Section("The UK GDPR and the Data Protection Act 2018", """
The **Data Protection Act 2018** implements the **UK GDPR**. Together they govern the processing of **personal data**, which is any information relating to an identified or identifiable living person.

### Special category data

Data needing extra protection: racial or ethnic origin, political opinions, religious beliefs, trade union membership, genetic and biometric data, health, sex life and sexual orientation. Processing it needs a condition beyond the usual lawful basis, and in analytics it is the category that most often forces a project to be redesigned.

### The seven principles

| Principle | What it requires |
| **Lawfulness, fairness and transparency** | A lawful basis, no deception, and people told what you do |
| **Purpose limitation** | Collected for a stated purpose, not quietly reused for another |
| **Data minimisation** | Only what is adequate and necessary for that purpose |
| **Accuracy** | Kept correct and up to date, with errors corrected |
| **Storage limitation** | Kept no longer than necessary, with a retention schedule |
| **Integrity and confidentiality** | Kept secure against loss, damage and unauthorised access |
| **Accountability** | You can demonstrate compliance, not merely claim it |

### The six lawful bases

Consent, contract, legal obligation, vital interests, public task, and legitimate interests. **Consent** must be freely given, specific, informed and as easy to withdraw as to give; a pre-ticked box is not consent. Most analytics on existing customer data relies on **legitimate interests**, which requires a documented balancing test weighing the organisation's interest against the individual's rights.

### Individual rights

| Right | What it means in practice |
| **Access** | A subject access request, answered within one month |
| **Rectification** | Inaccurate data corrected |
| **Erasure** | The right to be forgotten, where no overriding reason to keep it applies |
| **Restriction** | Processing paused while a dispute is resolved |
| **Portability** | Their data provided in a structured, machine readable format |
| **Object** | Including an absolute right to object to direct marketing |
| **Automated decisions** | Not to be subject to a solely automated decision with legal or similarly significant effects, without safeguards |

### Accountability in practice

A record of processing activities, a privacy notice, a **Data Protection Impact Assessment** for high risk processing, a **Data Protection Officer** where required, processor contracts, staff training, and breach reporting to the **ICO** within 72 hours where there is a risk to individuals, plus notification to the individuals themselves where the risk is high.

!key Pseudonymised is not anonymous :: If the data can be linked back to a person using a key you hold, it is still personal data and the whole regime still applies. Only genuinely irreversible anonymisation falls outside it, and that is much harder than deleting the name column.
"""),
        Section("The other legislation by name", """
| Law | What it does | Why an analyst cares |
| **Computer Misuse Act 1990** | Makes unauthorised access to a computer system an offence, along with unauthorised modification and making or supplying tools for it | Accessing a dataset you were not granted access to is an offence even inside your own employer |
| **Freedom of Information Act 2000** | Gives a right of access to information held by public authorities | It is where a great deal of open public data comes from, and it is why public bodies must know what they hold |
| **Copyright, Designs and Patents Act 1988** | Protects original works, and gives database right over a database whose contents required substantial investment | Scraping or republishing somebody else's dataset is an infringement, licence or no licence to view it |
| **Equality Act 2010** | Prohibits discrimination and requires reasonable adjustments | A model that disadvantages a protected group can be unlawful discrimination, however it was trained |
| **Consumer Rights Act 2015** | Governs fairness in consumer contracts and digital content | Constrains what a terms-of-service click can be held to have agreed |
| **Privacy and Electronic Communications Regulations** | Covers cookies, tracking and electronic marketing | Consent is needed for non-essential cookies and most marketing email |

### Working with a data processor

If another organisation processes personal data on your behalf, a cloud provider or an analytics vendor, you remain the **controller** and stay accountable. That relationship needs a written contract specifying the purpose, the security measures, the use of sub-processors, assistance with individual rights, breach notification and what happens to the data at the end.

!warn The Computer Misuse Act applies to employees :: "I had the password" is not authorisation. Looking up a relative's record, or querying a database your role does not cover, is unauthorised access, and prosecutions of insiders are routine.
"""),
        Section("Ethics, retention and destruction", """
### Legal and ethical are not the same question

Something can be lawful and still be the wrong thing to do. The questions worth asking of any analysis:

- Would the people in this dataset be **surprised** to learn it was being done?
- Could the result **harm** an individual or a group, including by being wrong?
- Is the data being used for the purpose it was **given** for?
- Who is **accountable** if the output is acted on and turns out to be wrong?
- Would the organisation be comfortable **publishing** its method?

### Retention

Every dataset needs a documented retention period, derived from the purpose and from any legal minimum: accounting records have statutory retention, CCTV usually a few weeks, marketing contacts a defined period after last engagement. "We keep everything in case it is useful" is a breach of storage limitation, and it is also the single largest source of breach impact, because a breach exposes whatever you still hold.

### Secure destruction

- Deleting a file does not erase the data; the blocks persist until overwritten
- Durable deletion means secure erase, cryptographic erasure where the key is destroyed, or physical destruction of the medium
- Backups and archives have to be included, or the data is still there
- Destruction should be recorded, with what was destroyed, when and by whom

### Anonymisation for analysis

| Technique | What it does | Residual risk |
| **Removing direct identifiers** | Drops names, addresses, reference numbers | High: combinations still identify people |
| **Pseudonymisation** | Replaces identifiers with a key held separately | Reversible by design, so still personal data |
| **Aggregation** | Reports groups rather than individuals | Small groups can still disclose |
| **Generalisation** | Age bands instead of dates of birth | Reduces precision of the analysis |
| **Suppression** | Hides cells below a minimum count | Can be defeated by differencing two reports |
| **Noise or differential privacy** | Adds controlled randomness | Trades accuracy for protection, deliberately |

Re-identification is easier than it looks: a date of birth, a postcode and a gender identify most individuals in the UK population. Removing the name is not anonymisation.
"""),
    ],
    keyterms=[
        ("Personal data", "Any information relating to an identified or identifiable living person."),
        ("Special category data", "Sensitive personal data such as health, biometrics, religion or sexual orientation, needing extra protection."),
        ("Data controller", "The organisation that decides why and how personal data is processed."),
        ("Data processor", "An organisation that processes personal data on a controller's behalf."),
        ("Lawful basis", "One of six legal grounds that makes processing personal data lawful."),
        ("Purpose limitation", "The principle that data collected for one purpose is not reused for an incompatible one."),
        ("Data minimisation", "Collecting only the data that is necessary for the stated purpose."),
        ("Subject access request", "A person's request to see the personal data an organisation holds about them."),
        ("DPIA", "A Data Protection Impact Assessment, required before high risk processing."),
        ("ICO", "The Information Commissioner's Office, the UK data protection regulator."),
        ("Computer Misuse Act 1990", "The law making unauthorised access to computer systems an offence."),
        ("Database right", "Protection for a database whose contents required substantial investment to assemble."),
        ("Retention period", "The documented length of time a dataset is kept before secure destruction."),
        ("Re-identification", "Linking supposedly anonymous data back to the individuals it describes."),
    ],
    grade="""
Marks come from **applying a named law to the scenario and reaching a conclusion**. Identify the data, name the principle or Act, say whether the activity is lawful, and say what has to change. An answer that lists the seven principles without touching the scenario scores a fraction of one that applies two of them properly.
""",
    mistakes=[
        "Saying 'GDPR' without naming the UK GDPR and the Data Protection Act 2018.",
        "Treating consent as the only lawful basis. Most internal analytics relies on legitimate interests.",
        "Calling data anonymous when it is pseudonymised.",
        "Forgetting purpose limitation, which is the principle analytics projects breach most often.",
        "Confusing the controller with the processor. Using a cloud provider does not transfer accountability.",
        "Thinking a deleted file is erased, or that deletion covers the backups.",
    ],
    quiz=[
        Q("Which legislation implements the UK GDPR?",
          ["The Data Protection Act 2018", "The Computer Misuse Act 1990",
           "The Freedom of Information Act 2000", "The Equality Act 2010"], 0,
          "The 2018 Act is the UK statute that sits alongside and implements the UK GDPR."),
        Q("Within how long must a reportable personal data breach be notified to the ICO?",
          ["72 hours", "24 hours", "7 days", "One month"], 0,
          "Without undue delay and within 72 hours where there is a risk to individuals."),
        Q("A company collects email addresses for order confirmations and later uses them for marketing. Which principle is breached?",
          ["Purpose limitation", "Data minimisation",
           "Storage limitation", "Accuracy"], 0,
          "Data collected for one purpose cannot be reused for an incompatible one."),
        Q("Which of these is special category data?",
          ["A record of a customer's religion", "A customer's postcode",
           "An order history", "A phone number"], 0,
          "Religious belief is special category data and needs an additional condition."),
        Q("An employee uses their legitimate login to look up a neighbour's record out of curiosity. What law does this breach?",
          ["The Computer Misuse Act 1990", "The Equality Act 2010",
           "The Freedom of Information Act 2000", "No law, they had access"], 0,
          "Having a password is not authorisation for that access, which makes it an offence."),
        Q("Which right requires data to be provided in a structured, machine readable format?",
          ["The right to data portability", "The right of access",
           "The right to erasure", "The right to object"], 0,
          "Portability exists so a person can move their data to another provider."),
        Q("What must a Data Protection Impact Assessment be carried out for?",
          ["Processing that is likely to be high risk to individuals",
           "Every new database", "All marketing campaigns",
           "Any use of the cloud"], 0,
          "It is required where processing is likely to result in a high risk to people's rights."),
        Q("A hospital uses a cloud provider to store patient data. Who is accountable for compliance?",
          ["The hospital, as controller", "The cloud provider, as processor",
           "Both equally, in all respects", "The ICO"], 0,
          "The controller decides the purpose and remains accountable; the processor has its own narrower duties."),
        Q("Why is removing the name column not anonymisation?",
          ["A date of birth, postcode and gender together identify most people",
           "Names can be recovered from the file", "Anonymisation requires encryption",
           "It is anonymisation if the name is deleted"], 0,
          "Re-identification works through combinations of ordinary fields."),
        Q("'We keep everything in case it becomes useful' breaches which principle?",
          ["Storage limitation", "Lawfulness", "Accuracy", "Portability"], 0,
          "Data must be kept no longer than necessary, with a documented retention period."),
    ],
    exam=[
        EQ("State **three** of the data protection principles.", 3,
           [MP("One valid principle", ["lawful", "fair", "transparen", "purpose limitation", "minimis", "accura", "storage limitation", "integrity", "confidential", "accountab"]),
            MP("A second, different principle", ["purpose", "minimis", "accura", "storage", "security", "accountab", "lawful"]),
            MP("A third, different principle", ["accountab", "storage", "integrity", "accura", "minimis", "purpose"])],
           "Data minimisation, purpose limitation, and storage limitation.",
           command="State"),
        EQ("Explain the difference between a data controller and a data processor, using an example.", 4,
           [MP("The controller decides the purpose and means of processing", ["decides", "purpose", "why", "determines", "responsible for"]),
            MP("The processor acts on the controller's instructions", ["on behalf", "instructions", "for the controller", "only what"]),
            MP("A valid example of each", ["cloud", "payroll", "analytics provider", "company and", "hospital and"]),
            MP("Accountability remains with the controller", ["accountable", "remains", "still responsible", "contract", "does not transfer"])],
           "The controller is the organisation that decides why personal data is processed and how, and the processor is an organisation that processes it on the controller's behalf and only within its instructions. A retailer that stores its customer database with a cloud provider is the controller, and the cloud provider is the processor. The distinction matters because accountability does not transfer with the data: the retailer remains responsible for having a lawful basis, for answering subject access requests and for the security of the processing, and must have a written contract requiring the provider to apply appropriate security, use no further sub-processors without permission, and report any breach to it promptly.",
           command="Explain"),
        EQ("A fitness app collects users' step counts, heart rate and location. The company wants to sell aggregated insights to insurers.\n\nExplain the legal issues this raises and what the company must do.", 6,
           [MP("Health data is identified as special category data", ["special category", "health", "heart rate", "sensitive"]),
            MP("A condition or explicit consent is needed for it", ["explicit consent", "condition", "additional", "Article 9", "lawful basis"]),
            MP("Purpose limitation is engaged by the new use", ["purpose", "collected for", "new purpose", "not what it was collected for", "reuse"]),
            MP("Transparency: users must be told", ["privacy notice", "told", "inform", "transparen", "aware"]),
            MP("Aggregation does not automatically make it anonymous", ["re-identif", "small groups", "still personal", "not anonymous", "combination", "location"]),
            MP("A DPIA, or the right to object, or a clear conclusion", ["DPIA", "impact assessment", "object", "opt out", "high risk", "should not", "must obtain"])],
           "Heart rate is health information and therefore special category data under the UK GDPR, and location data combined with step counts is close behind it in sensitivity, so the company needs not only a lawful basis but an additional condition, which in a commercial context realistically means explicit consent. Selling insights to insurers is also a new purpose: the data was given so the app could show users their own activity, and purpose limitation means it cannot simply be repurposed, so the company must either obtain fresh, specific, freely given consent for the insurance use or abandon it. Whatever it does must be set out plainly in the privacy notice rather than buried in terms of service, because transparency is a principle in its own right and a consent the user did not understand is not consent. The company should also not assume that aggregation solves the problem: location traces are highly identifying, and an aggregate reported for a small group or compared between two reports can disclose an individual, so it would need a documented minimum group size and suppression rules. Because this is large scale processing of special category data for a purpose with potential significant effects on individuals, a Data Protection Impact Assessment is required before it begins, and users must be able to object and withdraw consent as easily as they gave it.",
           command="Explain"),
        EQ("A local council wants to combine data from its housing, council tax and school admissions systems to identify families who may need support.\n\nDiscuss the legal and ethical issues involved, and what safeguards the council should put in place.", 8,
           [MP("A lawful basis is identified, probably public task", ["public task", "lawful basis", "legal obligation", "statutory", "consent"]),
            MP("Purpose limitation across the three systems is addressed", ["purpose", "collected for", "different purpose", "combin", "reuse"]),
            MP("Data minimisation is applied", ["minimis", "only what", "necessary", "fewer fields", "proportionate"]),
            MP("Special category or children's data is recognised", ["children", "special category", "vulnerable", "sensitive", "health"]),
            MP("A DPIA is required and named", ["DPIA", "impact assessment"]),
            MP("An ethical issue beyond legality is raised", ["surpris", "trust", "stigma", "harm", "false positive", "wrongly", "chilling", "surveillance"]),
            MP("Technical and governance safeguards are proposed", ["access control", "least privilege", "pseudonym", "audit", "retention", "training", "named owner", "review"]),
            MP("A judgement about whether and how it should proceed", ["should proceed", "only if", "recommend", "therefore", "on balance"])],
           "The council is likely to have a lawful basis here, since safeguarding and support are part of its public task rather than something requiring consent, but a basis for processing each dataset separately is not automatically a basis for combining them. All three were collected for different statutory purposes, so purpose limitation has to be addressed explicitly: the council must be able to point to the function the combined processing serves and show that it is compatible with the original collection. Data minimisation then constrains the design, because the temptation is to join everything available when the actual question needs a small number of fields; a system built on three indicators is both more lawful and more likely to work than one built on forty. The data involved is among the most sensitive a council holds: school admissions concerns children, housing records can reveal health and disability, and the combination is capable of inferring special category information even where no such field is present, which brings additional conditions into play. Because this is large scale processing of sensitive data about vulnerable people, a Data Protection Impact Assessment is mandatory and should be completed before any system is built, not written up afterwards. Beyond legality there are ethical questions the law does not settle. Families would be surprised to learn that their rent account and their child's school application had been joined to score them, and that surprise matters, because a council depends on people reporting difficulties honestly. A false positive risks stigmatising a family, while a false negative gives false assurance, and the people affected have least power to challenge either. The council should therefore keep a human decision in the loop at all times rather than acting on a score. The safeguards follow: role-based access on least privilege so only the support team sees identified records while analysts work on pseudonymised extracts, full audit logging of every access, a documented retention period with automatic deletion, a named owner for the combined dataset, published information about what is being done and how to object, and a scheduled review of whether the system is producing better outcomes. On balance the council can proceed, but only with the DPIA completed first, the field list cut to the minimum that works, and a standing commitment that the output prompts a human conversation rather than triggering an automated consequence.",
           command="Discuss"),
    ],
)

# ============================================================== F200 TA5

D_ROLES = Topic(
    slug="roles-skills-and-attributes",
    title="F200 TA5: Job Roles, Skills and Attributes",
    spec="F200 TA5",
    icon="i-user",
    minutes=24,
    blurb="Who does what in a data team, the technical and personal skills each role needs, and how to communicate a finding to somebody who will not read the method.",
    fact="The most valuable skill in data analytics is not the one that gets advertised. An analysis nobody understands changes nothing, so the ability to explain a result in one sentence to a person who will never see the query is worth more than another modelling technique.",
    sections=[
        Section("The roles", """
| Role | Responsible for | Typical tools |
| **Data analyst** | Answering business questions from existing data: querying, analysing, reporting, visualising | SQL, spreadsheets, Power BI or Tableau, Python or R |
| **Data scientist** | Statistical modelling and prediction, experiment design, machine learning | Python or R, notebooks, ML libraries, SQL |
| **Data engineer** | Building and running the pipelines that deliver reliable data | SQL, Python, orchestration tools, cloud platforms |
| **Database administrator** | The databases themselves: performance, availability, backup, security | SQL, DBMS tooling, monitoring |
| **Data architect** | How data is modelled and how systems fit together across the organisation | Modelling tools, governance frameworks |
| **Business intelligence analyst** | Reporting and dashboards that the business runs on day to day | BI platforms, SQL, data modelling |
| **Data governance or protection officer** | Policy, compliance, quality standards, the data dictionary | Governance and cataloguing tools |
| **Information security analyst** | Protecting data against loss, breach and misuse | Security tooling, monitoring, audit |

### How the roles relate

The engineer makes the data available and trustworthy. The analyst uses it to answer a question that has been asked. The scientist tackles questions that need a model rather than a query. The administrator keeps the platform running. The architect decides how it all fits together, and the governance role decides what is allowed. In a small organisation one person does several of these, which is why the job titles overlap in adverts.

!key Analyst against scientist :: The analyst explains what happened and why, from data that exists. The scientist predicts what will happen, and often has to create the data to do it through an experiment. The dividing line in practice is whether the answer needs a model.
"""),
        Section("Technical skills", """
| Skill | Why it is needed |
| **SQL** | The common language of data. Almost every role needs it, and most interviews test it |
| **Spreadsheet modelling** | Lookups, pivot tables, named ranges, scenario modelling, and knowing when to stop using one |
| **Programming in Python or R** | Automation, reshaping data, statistics, modelling, anything repeated |
| **Data visualisation** | Choosing the right chart, and building a dashboard somebody will actually use |
| **Statistics** | Averages and spread, distributions, correlation, significance, and the limits of each |
| **Data modelling** | Tables, keys, relationships, normalisation, and designing a schema that will survive |
| **Data cleaning and wrangling** | The largest part of the actual job |
| **Cloud and pipeline tooling** | Where the data lives and how it moves |
| **Version control** | Keeping queries and scripts tracked, reviewable and reproducible |
| **Security and compliance awareness** | Enough to recognise when a request should not be fulfilled as asked |

### Statistics worth being precise about

- **Mean** is the arithmetic average, and a single extreme value drags it
- **Median** is the middle value, and it does not care about extremes
- **Mode** is the most common value, and it is the only average for nominal data
- **Range** is the crudest measure of spread; the **interquartile range** and the **standard deviation** are the useful ones
- **Correlation** means two things move together. It is not causation, and the exam will ask
- **Trend** is direction over time, and a short series can show a trend that is noise

Median household income and mean household income differ by thousands of pounds, and which one an organisation quotes tells you what it wants you to conclude.
"""),
        Section("Personal attributes and communicating results", """
### The attributes that are actually assessed

| Attribute | What it looks like in the job |
| **Attention to detail** | Noticing that a total is 1% out and chasing it rather than rounding it |
| **Logical reasoning** | Forming a hypothesis and testing it, rather than looking for a chart that agrees |
| **Curiosity** | Asking why the number moved, not just reporting that it did |
| **Scepticism** | Distrusting a result that is too convenient, including your own |
| **Communication** | Explaining a method to a technical colleague and a conclusion to a director |
| **Commercial awareness** | Knowing which questions are worth answering |
| **Ethical judgement** | Recognising when something lawful is still wrong |
| **Resilience and patience** | Most of the work is cleaning, and most hypotheses are wrong |
| **Teamwork** | Analysis is a relay: engineer, analyst, decision maker |
| **Time management** | A good answer on Tuesday beats a perfect one next month |

### Communicating to a non-technical audience

1. **Lead with the answer.** The conclusion first, the method afterwards, and the caveats with it rather than buried.
2. **One chart, one message.** If a chart needs a paragraph to interpret, it is the wrong chart.
3. **Use their units.** Pounds, customers, days. Not standard deviations.
4. **Quantify the uncertainty in plain words.** "Between about 4% and 7%" is honest; "4.83%" implies precision you do not have.
5. **Say what should change.** An analysis that recommends nothing is a report, not an analysis.
6. **Keep the method available, not in the way.** An appendix, a documented query, a reproducible notebook.

### Choosing a chart

| Chart | Shows | Do not use it for |
| **Bar** | Comparison between categories | Showing a trend over many points |
| **Line** | Change over time | Unordered categories |
| **Scatter** | Relationship between two numeric variables | Categorical data |
| **Histogram** | The distribution of one numeric variable | Comparing categories |
| **Box plot** | Spread, median and outliers across groups | A general audience, without explanation |
| **Stacked bar** | Composition within a total | Comparing the middle segments precisely |
| **Pie** | One part against a whole, with very few slices | More than about four categories, or any comparison |
| **Map** | Geographic pattern | Anything where geography is not the point |

!grade Say the number and the decision :: "Returns on the new line are running at 11% against 4% for the rest of the range, which is about £18,000 a month. The pattern is almost entirely one size, so the likely cause is sizing rather than quality, and the cheapest test is to update the size guide before changing the supplier." Finding, figure, cause, action. That is the shape of a top band answer.
"""),
    ],
    keyterms=[
        ("Data analyst", "A role answering business questions from existing data through querying, analysis and reporting."),
        ("Data scientist", "A role using statistical modelling and machine learning to predict and explain."),
        ("Data engineer", "A role building and maintaining the pipelines that deliver reliable data."),
        ("Database administrator", "A role responsible for a database's performance, availability, backup and security."),
        ("Data architect", "A role designing how data is modelled and how systems fit together."),
        ("SQL", "The standard language for querying and manipulating relational data."),
        ("Mean", "The arithmetic average, which is pulled by extreme values."),
        ("Median", "The middle value of an ordered set, which is unaffected by extremes."),
        ("Correlation", "A measure of how closely two variables move together, which does not establish cause."),
        ("Data visualisation", "Presenting data graphically so a pattern can be seen and acted on."),
        ("Data storytelling", "Communicating a finding, its evidence and its implication to a decision maker."),
    ],
    grade="""
Role questions are marked on **responsibility and boundary**, not on job titles. Say what the role is accountable for, what it hands to another role, and what it needs from them. Communication questions are marked on whether your answer would actually work on the person described.
""",
    mistakes=[
        "Describing a role by its tools rather than its responsibilities.",
        "Confusing the analyst with the scientist. The dividing line is whether a model is needed.",
        "Treating correlation as causation.",
        "Quoting a mean where the distribution is skewed, without mentioning the median.",
        "Using a pie chart to compare values, or with more than about four slices.",
        "Leading a report to a director with the method instead of the answer.",
    ],
    quiz=[
        Q("Who is responsible for building and maintaining data pipelines?",
          ["The data engineer", "The data analyst",
           "The data scientist", "The database administrator"], 0,
          "The engineer makes data available and reliable; the analyst then uses it."),
        Q("Which skill is needed in almost every data role?",
          ["SQL", "Reinforcement learning", "Graphic design", "Network administration"], 0,
          "SQL is the common language of querying data and is tested in most interviews."),
        Q("Sales figures include one enormous outlier order. Which average is most representative?",
          ["The median", "The mean", "The mode", "The range"], 0,
          "The median ignores extremes; the mean is dragged by them."),
        Q("Ice cream sales and drowning deaths both rise in summer. What does this show?",
          ["Correlation without causation", "That ice cream causes drowning",
           "A data quality error", "Reverse causation"], 0,
          "A third factor, hot weather, drives both. The exam asks this almost every year."),
        Q("Which chart is right for the relationship between advertising spend and sales?",
          ["A scatter plot", "A pie chart", "A stacked bar chart", "A histogram"], 0,
          "Two numeric variables plotted against each other is what a scatter plot is for."),
        Q("Which chart shows the distribution of a single numeric variable?",
          ["A histogram", "A line chart", "A pie chart", "A bar chart"], 0,
          "A histogram buckets values and shows how many fall in each bucket."),
        Q("What should a report to a non-technical director lead with?",
          ["The conclusion and what should change",
           "The data sources used", "The cleaning method",
           "The statistical technique"], 0,
          "Answer first, method available but not in the way."),
        Q("Which role decides how data is modelled across the whole organisation?",
          ["The data architect", "The data analyst",
           "The information security analyst", "The BI analyst"], 0,
          "Architecture is organisation-wide design rather than a single project."),
        Q("Why is scepticism listed as a professional attribute?",
          ["A convenient result is the one most likely to be wrong",
           "Analysts should distrust colleagues",
           "Data is usually falsified", "It speeds up analysis"], 0,
          "The result that confirms what everyone hoped is the one to check hardest."),
        Q("What is wrong with reporting a figure as 4.83%?",
          ["It implies precision the data does not support",
           "Percentages should be whole numbers",
           "Decimals are not allowed in reports",
           "Nothing, it is more accurate"], 0,
          "A range stated honestly is better than a decimal that pretends to certainty."),
    ],
    exam=[
        EQ("Identify **two** job roles in a data team and state the main responsibility of each.", 4,
           [MP("A genuine role is named", ["data analyst", "data scientist", "data engineer", "database administrator", "architect", "BI analyst", "governance"]),
            MP("Its main responsibility is stated", ["answers", "builds", "maintains", "models", "secures", "reports", "pipelines"]),
            MP("A second, different role is named", ["engineer", "scientist", "administrator", "analyst", "architect"]),
            MP("The second responsibility is stated", ["responsible for", "builds", "analyses", "maintains", "predicts"])],
           "A data engineer is responsible for building and maintaining the pipelines that extract, transform and load data so that it arrives reliably and on time. A data analyst is responsible for answering business questions from that data, through querying, analysis, visualisation and reporting to the people who make the decisions.",
           command="Identify"),
        EQ("Explain why correlation does not establish causation, using an example.", 3,
           [MP("Correlation means two variables move together", ["move together", "related", "both increase", "association"]),
            MP("A third factor, or reverse causation, may explain it", ["third factor", "confounding", "other cause", "coincidence", "reverse"]),
            MP("A valid example is given", ["ice cream", "weather", "example", "both caused by"])],
           "A correlation shows only that two variables move together, which can happen for several reasons other than one causing the other. A third factor may drive both: ice cream sales and drowning deaths rise and fall together across the year, but neither causes the other, because hot weather causes both more ice cream buying and more swimming. The relationship can also run the opposite way to the one assumed, or be coincidence in a small sample. Establishing cause needs a mechanism and ideally a controlled experiment, not a correlation coefficient.",
           command="Explain"),
        EQ("A data analyst has found that customer complaints rise sharply in the three days after each software release.\n\nDescribe how the analyst should communicate this to a non-technical management team.", 5,
           [MP("Lead with the finding, not the method", ["lead with", "conclusion first", "headline", "state the finding"]),
            MP("Quantify it in business terms", ["number", "how many", "percentage", "cost", "per release", "complaints per day"]),
            MP("Use one clear visual", ["chart", "line", "bar", "visual", "graph", "one chart"]),
            MP("Be honest about uncertainty or limitations", ["caveat", "uncertain", "may", "not proof", "limitation", "sample"]),
            MP("Recommend a specific action", ["recommend", "should", "next step", "test", "suggest"])],
           "The analyst should open with the finding in one sentence, not with how it was found: complaints run at roughly three times the normal rate for three days after every release, which is about 120 extra contacts per release. A single line chart of daily complaints with the release dates marked makes the pattern obvious without any explanation, and that should be the only chart in the room. The figures should be given in the management team's own units, complaints and support hours rather than standard deviations, and the uncertainty stated plainly: the pattern holds across the last eight releases, but it shows association rather than cause, and some of the rise may be users contacting support about a change rather than a defect. The analyst should then close with a specific recommendation, such as categorising the complaints from the next two releases to separate defects from confusion, because that distinguishes a testing problem from a communication one and costs nothing to find out. The method and the query should be available as an appendix for anyone who wants it, but not presented.",
           command="Describe"),
        EQ("Discuss the skills and personal attributes a data analyst needs, and explain which you consider most important.", 8,
           [MP("Technical skills are named specifically", ["SQL", "Python", "spreadsheet", "visualisation", "statistics", "modelling"]),
            MP("Data preparation is recognised as the bulk of the work", ["cleaning", "wrangling", "preparation", "most of the time", "messy"]),
            MP("Statistical judgement is addressed", ["statistics", "mean", "median", "correlation", "significance", "distribution", "sample"]),
            MP("Communication is addressed", ["communicat", "explain", "non-technical", "report", "storytelling", "audience"]),
            MP("Attention to detail is addressed", ["detail", "accurate", "checking", "notices"]),
            MP("Scepticism or ethical judgement is addressed", ["scepti", "question", "challenge", "ethical", "too good", "verify"]),
            MP("Commercial or business understanding is addressed", ["business", "commercial", "which questions", "context", "decision"]),
            MP("A clear judgement with justification", ["most important", "I consider", "because", "without this", "therefore"])],
           "The technical floor is well defined. An analyst needs SQL, because almost all organisational data sits behind it, together with enough spreadsheet modelling to build something a colleague can use and enough Python or R to automate anything done more than twice. They need visualisation skill, which is mostly the judgement to pick the right chart and resist the decorative one, and enough statistics to know that a mean is misleading on a skewed distribution, that a correlation is not a cause, and that a difference in a small sample may be nothing at all. Underneath those sits data preparation, which is the largest single part of the actual job: finding the data, understanding what each field really means, reconciling two systems that disagree and deciding what to do about missing values, all of which demands patience as much as technique. The personal attributes matter as much as the tools. Attention to detail is what makes an analyst chase a total that is one per cent out instead of rounding it, and that one per cent is quite often the finding. Scepticism is the discipline of distrusting the convenient result, including their own, and checking hardest when the answer is what everybody hoped for. Commercial awareness decides which questions are worth the week it takes to answer them, and ethical judgement decides which ones should not be answered at all. Weighing these, the most important is communication. Every other skill produces a result that exists only inside the analyst's head or their notebook, and a correct analysis that a decision maker does not understand changes nothing, while a clearly explained partial answer changes behaviour the same afternoon. Technical skills can be taught quickly and are increasingly assisted by tooling; the ability to turn a result into a sentence a director will act on, with its uncertainty stated honestly, is the part that makes the whole role worth funding.",
           command="Discuss"),
    ],
)

# ============================================================== F201 TA1

B_SCOPE = Topic(
    slug="the-scope-of-big-data",
    title="F201 TA1: The Scope of Managing Big Data",
    spec="F201 TA1",
    icon="i-cube",
    minutes=28,
    blurb="What makes data big, where it comes from, and the effect it has on organisations, individuals and whole sectors.",
    fact="A single modern jet engine generates more data on one flight than the entire airline industry produced in a year in the 1970s. Almost none of it is ever looked at by a human; it exists so that a model can notice a bearing starting to fail.",
    sections=[
        Section("What makes data big", """
Big data is not simply a large file. The usual definition is a set of characteristics, the **Vs**, and the point of them is that each one breaks a different conventional tool.

| Characteristic | What it means | What it breaks |
| **Volume** | Terabytes to petabytes, growing continuously | Single machine storage and processing |
| **Velocity** | Arriving continuously, needing a fast response | Batch processing on a nightly schedule |
| **Variety** | Structured, semi-structured and unstructured together | A fixed relational schema |
| **Veracity** | Uncertain accuracy, gaps, noise, duplicates, bias | The assumption that stored data is correct |
| **Value** | The business worth that has to be extracted | The assumption that collecting is the same as benefiting |

Variability and visualisation are sometimes added. The examinable point is that any one of these alone can make a dataset unmanageable with ordinary tools, which is the working definition of big data: **data that cannot be stored, processed or analysed with conventional single-machine methods**.

### Volume, in proportion

| Unit | Scale |
| Kilobyte | A short document |
| Megabyte | A photograph |
| Gigabyte | A film |
| Terabyte | A desktop hard drive |
| Petabyte | A thousand terabytes: a large organisation's data estate |
| Exabyte | A thousand petabytes: a global platform |

!key The definition that scores :: Not "a lot of data", but "data whose volume, velocity or variety makes it impossible to process with conventional tools on a single machine, so distributed storage and processing are required."
"""),
        Section("Where big data comes from", """
| Source | What it produces | Characteristic it stresses |
| **Transactional systems** | Every order, payment, booking, click to buy | Volume |
| **Web and app telemetry** | Page views, taps, scroll depth, session paths | Volume and velocity |
| **Social media** | Posts, reactions, comments, images, networks | Variety and veracity |
| **Sensors and IoT** | Temperature, vibration, location, energy use | Velocity and volume |
| **Machine and system logs** | Every request, error and state change | Volume |
| **Media** | Images, audio, video, CCTV | Volume and variety |
| **Mobile devices** | Location, movement, app use | Velocity and privacy risk |
| **Open data** | Census, weather, transport, health, geography | Value through combination |
| **Third party and purchased data** | Market, credit, demographic datasets | Veracity and licensing |

### Why combining sources is where the value is

Each source answers a narrow question. Joined, they answer a different kind of question entirely: weather data plus transaction data explains a sales dip; transport data plus footfall data decides where a shop goes; sensor data plus maintenance records predicts a failure before it happens. The combination is also where the privacy risk concentrates, because joining datasets is exactly what makes individuals re-identifiable.
"""),
        Section("The impacts of big data", """
### On organisations

| Impact | Detail |
| **Better decisions** | Evidence instead of instinct, and measurement of whether a change worked |
| **Personalisation** | Recommendations, pricing and content tailored per customer |
| **Operational efficiency** | Routing, stock, staffing and energy optimised against real demand |
| **Predictive maintenance** | Replacing a part before it fails rather than after |
| **New products** | Data itself becoming the product, sold as insight or as a service |
| **Risk and fraud detection** | Patterns across millions of transactions that no reviewer could see |
| **Cost** | Storage, compute, specialist staff and governance, all ongoing |
| **Skills shortage** | The scarce resource is people who can use it, not the data |
| **Risk concentration** | A single breach now exposes far more than it would have done |

### On individuals

The benefits are real: services that work better, prices that reflect demand, health research at a scale that was impossible, free products funded by advertising. So are the costs: surveillance as a default condition, profiling that affects credit and insurance, filter bubbles, price discrimination, and decisions made about a person by a system that cannot explain itself.

### On society and sectors

- **Healthcare** — population screening, drug discovery, outbreak detection
- **Transport** — live routing, congestion charging, autonomous vehicles
- **Retail** — demand forecasting, dynamic pricing, supply chains that react in hours
- **Finance** — credit scoring, fraud detection, algorithmic trading
- **Energy** — smart grids balancing supply and demand minute by minute
- **Public services** — targeting support, planning capacity, detecting fraud
- **Employment** — some roles automated away, others created, and a persistent shortage of the new ones

!warn Collecting is not the same as benefiting :: Most organisations store far more than they analyse. Value is a characteristic that has to be extracted deliberately, and the storage bill arrives whether or not anybody ever asks the data a question.
"""),
    ],
    keyterms=[
        ("Big data", "Data whose volume, velocity or variety prevents processing by conventional single-machine methods."),
        ("Volume", "The sheer quantity of data, typically terabytes to petabytes."),
        ("Velocity", "The speed at which data arrives and must be processed."),
        ("Variety", "The range of data types and structures held together."),
        ("Veracity", "The uncertainty, noise and bias present in the data."),
        ("Value", "The business worth that has to be deliberately extracted from data."),
        ("IoT", "The Internet of Things: networked sensors and devices generating continuous data."),
        ("Telemetry", "Automatically captured measurements of how a system or product is used."),
        ("Predictive maintenance", "Using sensor data to replace a component before it fails."),
        ("Personalisation", "Tailoring content, recommendations or pricing to an individual."),
        ("Petabyte", "A thousand terabytes, roughly a million gigabytes."),
    ],
    grade="""
Define big data by **what it breaks**, not by how large it is, and then tie each characteristic to a consequence. "High velocity means the data has to be processed as a stream, because by the time a nightly batch ran the fraudulent transaction would already have been settled" is a full mark sentence.
""",
    mistakes=[
        "Defining big data as 'a lot of data' with no reference to the limits of conventional processing.",
        "Naming the Vs without saying what each one causes.",
        "Confusing volume with velocity.",
        "Treating veracity as a minor issue. Big data is usually dirtier than small data, not cleaner.",
        "Assuming more data automatically means better decisions.",
        "Listing benefits to organisations and ignoring the effects on individuals.",
    ],
    quiz=[
        Q("Which characteristic of big data refers to the speed at which it arrives?",
          ["Velocity", "Volume", "Variety", "Veracity"], 0,
          "Velocity is about rate of arrival and the speed of response required."),
        Q("A dataset mixes database tables, social media text and CCTV footage. Which V is this?",
          ["Variety", "Volume", "Value", "Velocity"], 0,
          "Several structures and types held together is variety."),
        Q("Which V describes uncertainty about whether the data is accurate?",
          ["Veracity", "Variety", "Value", "Volume"], 0,
          "Veracity covers noise, gaps, duplicates and bias."),
        Q("What is the best definition of big data?",
          ["Data that cannot be processed with conventional single-machine methods",
           "Any dataset over one terabyte",
           "Data collected from the internet",
           "Data used for machine learning"], 0,
          "The definition is about exceeding conventional tools, not a fixed size."),
        Q("How many terabytes are in a petabyte?",
          ["About 1,000", "About 100", "About 10", "About 1,000,000"], 0,
          "A petabyte is a thousand terabytes, or roughly a million gigabytes."),
        Q("Which source most stresses velocity?",
          ["A network of vibration sensors reporting every second",
           "An annual census file", "A monthly accounts export",
           "An archive of scanned documents"], 0,
          "Continuous high frequency readings have to be handled as a stream."),
        Q("Why is combining datasets both valuable and risky?",
          ["It answers new questions, and it makes individuals re-identifiable",
           "It always reduces data quality",
           "It is prohibited by law",
           "It increases storage costs only"], 0,
          "Joining is where the insight is, and it is also how anonymity breaks."),
        Q("What does predictive maintenance use data to do?",
          ["Replace a component before it fails",
           "Repair a component faster after failure",
           "Reduce the cost of spare parts",
           "Schedule routine servicing by calendar"], 0,
          "Sensor patterns indicate wear before a failure occurs."),
        Q("Which is a genuine cost of a big data strategy?",
          ["Ongoing storage, compute, specialist staff and governance",
           "The purchase price of the data only",
           "A one-off software licence",
           "There are no significant ongoing costs"], 0,
          "All of those recur monthly whether or not any analysis is done."),
        Q("Why is 'value' listed as a characteristic rather than an outcome?",
          ["Because it has to be extracted deliberately and often is not",
           "Because data is always valuable",
           "Because value means file size",
           "Because only paid data has value"], 0,
          "Most organisations store far more than they ever analyse."),
    ],
    exam=[
        EQ("State **three** characteristics of big data.", 3,
           [MP("One valid characteristic", ["volume", "velocity", "variety", "veracity", "value"]),
            MP("A second, different characteristic", ["velocity", "variety", "veracity", "value", "volume"]),
            MP("A third, different characteristic", ["variety", "veracity", "value", "velocity", "volume"])],
           "Volume, velocity and variety.",
           command="State"),
        EQ("Explain why high velocity data requires a different approach from traditional batch processing.", 4,
           [MP("Velocity means data arrives continuously", ["continuous", "constantly", "real time", "stream", "as it happens"]),
            MP("Batch processing runs on a schedule, so results are late", ["overnight", "schedule", "delay", "too late", "once a day"]),
            MP("Stream processing handles each event as it arrives", ["stream", "event", "as it arrives", "immediately", "in flight"]),
            MP("A consequence or example where the delay matters", ["fraud", "settled", "already", "sensor", "failure", "alert", "outage"])],
           "High velocity means the data arrives continuously rather than as a file at a fixed time, so there is no natural point at which a complete set exists to be processed. Traditional batch processing runs on a schedule, typically overnight, which means every result is as old as the last run; for data arriving every second that delay is the whole problem rather than an inconvenience. Stream processing handles each event as it arrives, applying rules or a model in flight and acting within milliseconds. The difference matters wherever the value of the answer decays: a fraudulent card transaction has already been authorised and settled by the time a nightly batch notices it, and a vibration pattern indicating a bearing failure is useful before the bearing fails, not the next morning.",
           command="Explain"),
        EQ("A supermarket chain is using big data from loyalty cards, till transactions, weather feeds and its supply chain.\n\nExplain **three** benefits this could bring and **one** risk it creates.", 8,
           [MP("A benefit relating to demand forecasting or stock", ["forecast", "stock", "waste", "demand", "order", "supply"]),
            MP("It is explained with the mechanism", ["weather", "predict", "because", "combining", "sales rise"]),
            MP("A benefit relating to personalisation or marketing", ["personalis", "offer", "recommend", "target", "coupon", "loyalty"]),
            MP("It is explained with the mechanism", ["purchase history", "basket", "segment", "because"]),
            MP("A third benefit, such as pricing, layout or efficiency", ["pricing", "layout", "staffing", "range", "efficiency", "distribution"]),
            MP("It is explained with the mechanism", ["because", "allows", "data shows", "identif"]),
            MP("A genuine risk is identified", ["privacy", "re-identif", "breach", "trust", "surprise", "discriminat", "bias", "dependency"]),
            MP("The risk is explained and a mitigation or judgement offered", ["because", "could", "should", "mitigat", "transparen", "minimis", "therefore"])],
           "The first benefit is demand forecasting. Joining till data to weather feeds lets the chain predict, store by store, that a forecast of 24 degrees on a Friday raises barbecue and salad sales by a known proportion, so orders are placed before demand arrives rather than after; that cuts both empty shelves and waste on short-life products, which is where a supermarket's margin actually sits. The second is personalisation. Loyalty data shows what each household buys and how often, so offers can be targeted at products a customer already buys or is likely to switch to, which gives a far higher redemption rate than a uniform discount and costs less in lost margin. The third is operational: combining transaction data with supply chain data identifies which lines sell in which stores at which times, which informs range decisions, shelf layout and staffing, and lets distribution be planned against real rather than assumed demand. The risk that comes with all of this is privacy, and it is concentrated precisely where the value is. Individually, a weather feed and a basket are innocuous; joined to a loyalty card they produce a detailed and sensitive record of a household, capable of revealing pregnancy, illness, religious observance and financial difficulty as inferences the customer never disclosed. That creates both a legal exposure, since inferred health information is special category data and the processing must be transparent and minimised, and a trust exposure, because customers who feel watched stop using the card and the data disappears. The chain should therefore be explicit in its privacy notice about what it infers and why, hold the minimum it needs with a real retention period, keep identified data tightly access controlled, and avoid using inferences in ways a customer would find intrusive even where doing so would be lawful.",
           command="Explain"),
    ],
)

# ============================================================== F201 TA2

B_INFRA = Topic(
    slug="big-data-infrastructure",
    title="F201 TA2: The Infrastructure Challenges of Big Data",
    spec="F201 TA2",
    icon="i-memory",
    minutes=28,
    blurb="Storage, network and processing at a scale where one machine is not an option, and the trade-offs each choice forces.",
    fact="Moving a petabyte over a fast internet connection takes months. Cloud providers therefore sell a service where they post you a ruggedised storage appliance, you fill it and post it back, because a lorry has a higher effective bandwidth than a fibre link.",
    sections=[
        Section("Storage at scale", """
### Scaling up and scaling out

- **Scaling up**, vertically: a bigger machine. Simple, and it hits a ceiling that no budget can move.
- **Scaling out**, horizontally: more machines working together. No ceiling, but now everything is a distributed systems problem.

Big data is defined by having passed the point where scaling up works, so every storage option below is a way of scaling out.

### The options

| Store | How it works | Suits |
| **Distributed file system** | Files split into blocks, replicated across many machines | Huge files processed in parallel |
| **Object storage** | Files as objects with metadata, addressed by key, effectively unlimited | Cheap durable storage of anything, the usual basis of a data lake |
| **Data lake** | Raw data of any structure, schema applied on read | Keeping everything now, deciding later |
| **Data warehouse** | Structured, modelled, columnar, optimised for queries | The questions you already know you will ask |
| **Lakehouse** | A warehouse-style engine over lake storage | Both, which is why it is now the common design |
| **NoSQL document store** | Flexible JSON-like records, no fixed schema | Variety, rapidly changing structure |
| **Key-value store** | A key and a blob, extremely fast | Caching, sessions, lookups |
| **Column-family store** | Wide sparse rows across a cluster | Time series and very high write rates |
| **Graph database** | Nodes and relationships as first class things | Networks, fraud rings, recommendations |
| **Time series database** | Optimised for timestamped measurements | Sensors, telemetry, monitoring |

### Replication, partitioning and the consequence

Data is **partitioned**, or sharded, across machines so that work can run in parallel, and **replicated** so that a machine failing does not lose anything. Those two together buy scale and resilience, and they cost consistency: after a write, different replicas can briefly disagree. Many big data stores therefore offer **eventual consistency** rather than the immediate consistency a relational database guarantees, and the design question is whether the application can tolerate that. For a bank balance it cannot; for a view count it obviously can.

!key Store everything is a decision with a bill :: Object storage is cheap per gigabyte and not free, and retrieval, transfer and the compute to process it are charged separately. A data lake with no retention policy becomes a data swamp: expensive, undocumented, and unused.
"""),
        Section("Network and movement", """
Data has weight. Moving it is often the binding constraint rather than storing or processing it.

| Factor | Why it matters |
| **Bandwidth** | How much data can move per second. A petabyte over a gigabit link takes months |
| **Latency** | The delay before a response. Irreducible below the speed of light over distance |
| **Throughput** | What is actually achieved, which is always less than the bandwidth |
| **Egress cost** | Cloud providers charge to move data out, which is what makes lock-in real |
| **Congestion and contention** | Shared links slow under load, and backups compete with users |
| **Reliability** | A transfer that fails at 94% has to be resumable, or it is worthless |

### The principle that follows

**Move the computation to the data, not the data to the computation.** This is the single most important design idea in big data. Instead of pulling a petabyte to an analysis machine, the query is sent to the machines that already hold the blocks, each processes its own share locally, and only the small result comes back. Distributed processing frameworks exist to make that practical.

### Edge processing

Where velocity and bandwidth are both constrained, processing happens at the **edge**, on or near the device. A camera that detects motion locally and uploads only the clips that matter is moving kilobytes instead of a continuous stream, and it works when the connection does not.
"""),
        Section("Processing and computing power", """
### Distributed processing

The pattern underneath most big data processing has three steps: **split** the data across machines, **process** each part locally in parallel, **combine** the partial results. Map-reduce is the classic expression of it, and modern engines do the same thing in memory rather than via disk, which is why they are far faster.

| Approach | How it runs | Suits |
| **Batch** | A large volume processed on a schedule | Reporting, retraining, billing |
| **Micro-batch** | Small batches every few seconds | A compromise where near real time is enough |
| **Stream** | Each event handled as it arrives | Fraud, alerting, live dashboards, sensors |
| **Interactive query** | A human waiting for an answer | Exploration and dashboards |

### Compute

| Resource | What it is good for |
| **CPU** | General purpose logic, branching, coordination |
| **GPU** | Thousands of identical calculations at once, which is exactly what training a model is |
| **TPU and accelerators** | Purpose-built for machine learning workloads |
| **Memory** | Holding working data in RAM instead of reading from disk, the main source of modern speedups |
| **Cluster** | Many machines coordinated as one, which is how all of the above is scaled |

### Cloud elasticity and its economics

The cloud's real advantage for big data is **elasticity**: a cluster of two hundred machines for the forty minutes a job needs, then nothing. On premise, that peak capacity has to be bought and then sits idle. The matching risk is that elastic resources left running, or a badly written query that scans the entire lake, produce a bill nobody authorised, which is why cost monitoring is part of the architecture rather than an afterthought.

### Resilience

Replication across **availability zones**, automatic failover, retried and idempotent jobs, checkpointing so a failed job resumes rather than restarts, and backups that are tested. At this scale component failure is not an incident, it is the normal operating condition, so the system is designed to continue through it.

!grade The trade-off is the answer :: Every infrastructure question is a trade. Scale out buys capacity and costs consistency. Streaming buys immediacy and costs simplicity. The lake buys flexibility and costs governance. Naming the trade and then choosing, with a reason tied to the scenario, is what the top band looks like.
"""),
    ],
    keyterms=[
        ("Scaling up", "Increasing the capacity of a single machine."),
        ("Scaling out", "Adding more machines that work together as a cluster."),
        ("Distributed file system", "A system splitting files into blocks replicated across many machines."),
        ("Object storage", "Effectively unlimited storage of files as keyed objects with metadata."),
        ("Lakehouse", "An architecture applying warehouse-style querying directly to data lake storage."),
        ("Partitioning", "Splitting data across machines so it can be processed in parallel."),
        ("Replication", "Keeping copies of data on several machines so a failure loses nothing."),
        ("Eventual consistency", "A guarantee that replicas will agree in time, but may briefly disagree."),
        ("Latency", "The delay between a request and the start of a response."),
        ("Bandwidth", "The volume of data a connection can carry per second."),
        ("Egress cost", "A charge for moving data out of a cloud provider."),
        ("Edge processing", "Processing data on or near the device that generated it."),
        ("Batch processing", "Processing a large volume of data on a schedule."),
        ("Stream processing", "Processing each event as it arrives."),
        ("Elasticity", "The ability to add and remove computing capacity on demand."),
        ("GPU", "A processor with many cores suited to large numbers of identical calculations."),
    ],
    grade="""
Answers reach the top band by **quantifying** the constraint and then choosing. "A gigabit link moves about 10 terabytes a day at best, so a 400 terabyte migration is six weeks of continuous transfer; physical transfer or processing in place is the only realistic option" beats any amount of general discussion of bandwidth.
""",
    mistakes=[
        "Treating scaling out as simply 'more computers' without mentioning the consistency cost.",
        "Confusing bandwidth with latency. A fat link is not a fast one.",
        "Forgetting that moving data is usually the binding constraint, not storing it.",
        "Describing a data lake as a warehouse. One applies schema on read, the other on write.",
        "Assuming the cloud is automatically cheaper. Elasticity is cheaper; idle capacity and egress are not.",
        "Treating component failure as an exception rather than the normal condition at scale.",
    ],
    quiz=[
        Q("What does scaling out mean?",
          ["Adding more machines that work together",
           "Buying a more powerful single machine",
           "Compressing the data", "Moving to the cloud"], 0,
          "Horizontal scaling adds nodes; vertical scaling makes one node bigger."),
        Q("What is the main cost of replicating and partitioning data across a cluster?",
          ["Replicas can briefly disagree, so consistency is weakened",
           "Queries become impossible", "The data cannot be backed up",
           "Latency becomes zero"], 0,
          "Many big data stores offer eventual rather than immediate consistency."),
        Q("Which principle underlies distributed processing frameworks?",
          ["Move the computation to the data",
           "Move the data to the computation",
           "Store everything in memory",
           "Compress before processing"], 0,
          "Sending the query to the machines holding the blocks avoids moving the data at all."),
        Q("A data lake applies structure:",
          ["When the data is read", "When the data is written",
           "Never", "Only to structured sources"], 0,
          "Schema on read is what distinguishes a lake from a warehouse."),
        Q("Which workload type suits fraud detection on card transactions?",
          ["Stream processing", "Nightly batch processing",
           "Monthly batch processing", "Interactive query"], 0,
          "The transaction has to be assessed before it is authorised, not the next morning."),
        Q("Why are GPUs used to train machine learning models?",
          ["They perform thousands of identical calculations in parallel",
           "They have more storage", "They use less electricity",
           "They have faster single-core speed"], 0,
          "Training is overwhelmingly matrix arithmetic, which parallelises perfectly."),
        Q("What is egress cost?",
          ["A charge for moving data out of a cloud provider",
           "The cost of storing data", "The cost of a failed query",
           "The price of additional processing"], 0,
          "It is what makes cloud lock-in a financial reality rather than a technical one."),
        Q("What is edge processing?",
          ["Processing data on or near the device that produced it",
           "Processing at the edge of a data centre",
           "Processing only the newest data",
           "Processing in a separate region"], 0,
          "It saves bandwidth and works when the connection does not."),
        Q("Why is cloud elasticity valuable for big data?",
          ["Capacity can be rented for the duration of a job and then released",
           "Cloud storage is always free",
           "Cloud machines are faster than on premise",
           "It removes the need for governance"], 0,
          "On premise, peak capacity must be bought and then sits idle."),
        Q("At large scale, component failure should be treated as:",
          ["The normal operating condition, designed for",
           "A rare incident", "A supplier fault",
           "Something to prevent entirely"], 0,
          "With thousands of components, something is always failing, so jobs retry and data is replicated."),
    ],
    exam=[
        EQ("State the difference between scaling up and scaling out.", 2,
           [MP("Scaling up increases the capacity of one machine", ["one machine", "bigger", "more powerful", "vertical", "single"]),
            MP("Scaling out adds more machines working together", ["more machines", "cluster", "horizontal", "nodes", "additional servers"])],
           "Scaling up means increasing the capacity of a single machine, with more processors, memory or storage. Scaling out means adding more machines that work together as a cluster.",
           command="State"),
        EQ("Explain why a data lake is often chosen over a data warehouse for big data.", 4,
           [MP("A lake accepts any structure", ["any structure", "unstructured", "raw", "semi-structured", "all types"]),
            MP("Schema is applied on read rather than on write", ["schema on read", "on read", "later", "when queried", "not rejected"]),
            MP("It avoids losing data that does not fit a schema", ["nothing is lost", "rejected", "discard", "keep everything", "decide later"]),
            MP("A drawback is recognised", ["governance", "swamp", "no guarantee", "quality", "documentation", "catalogue"])],
           "A data lake accepts data in whatever structure it arrives in, including unstructured content such as images, audio and free text that a relational warehouse cannot hold at all. It applies structure when the data is read rather than when it is written, so nothing has to fit a schema at the point of arrival and nothing is rejected or reshaped before anyone knows what questions will be asked of it. That matters for big data because variety is one of its defining characteristics and the useful questions are often not known in advance. The cost is governance: because the lake guarantees nothing about quality, structure or meaning, an undocumented lake becomes a swamp that is expensive to store and that nobody trusts enough to use, so a catalogue, lineage and retention policy are not optional extras.",
           command="Explain"),
        EQ("A manufacturer has 4,000 sensors on its production line, each sending a reading every second. The site has a limited internet connection.\n\nExplain how the data should be collected and processed, and justify your choices.", 6,
           [MP("The data rate is quantified or recognised as high", ["per second", "4000", "millions", "volume", "rate", "high velocity"]),
            MP("Edge processing is proposed", ["edge", "locally", "on site", "on the device", "near"]),
            MP("Justified by bandwidth or connectivity", ["bandwidth", "limited connection", "upload", "cannot send", "works offline"]),
            MP("Aggregation or filtering at the edge is described", ["aggregate", "average", "only send", "threshold", "summar", "exceptions"]),
            MP("A suitable store is named for the retained data", ["time series", "data lake", "object storage", "cloud", "warehouse"]),
            MP("Stream processing for alerts, with a reason", ["stream", "alert", "real time", "before failure", "immediately", "threshold"])],
           "Four thousand sensors at one reading a second is 4,000 values every second, around 345 million a day, and a limited connection will not carry that continuously, so the design has to reduce the data before it leaves the site. Processing should therefore start at the edge: a local gateway ingests every reading, applies threshold rules immediately so an out of range vibration raises an alert on site within milliseconds, and aggregates the rest into, say, one-minute summaries holding the mean, minimum, maximum and standard deviation per sensor. That cuts the uploaded volume by roughly sixty times while keeping the statistical shape of the signal, and it means the line keeps being monitored when the connection drops, which a cloud-only design would not. Full resolution readings should be buffered locally for a short window and uploaded only around an event, because that is when per-second detail is actually needed for diagnosis. In the cloud the summaries belong in a time series store, which is built for timestamped measurements and compresses them far better than a relational table, with the raw event windows in object storage as a lake for later model training. Alerting should be stream processed rather than batched, because the entire value of the data is in acting before a component fails, and a nightly batch would discover the failure after it had already stopped the line.",
           command="Explain"),
        EQ("Discuss the infrastructure challenges an organisation faces when moving from a single-server database to a big data platform.", 8,
           [MP("Storage must be distributed rather than enlarged", ["distributed", "cluster", "scale out", "no longer fits", "partition"]),
            MP("Partitioning and replication are explained", ["partition", "shard", "replicat", "copies", "parallel"]),
            MP("The consistency trade-off is identified", ["consistency", "eventual", "disagree", "ACID", "immediate"]),
            MP("Network bandwidth or data movement is addressed", ["bandwidth", "move the data", "transfer", "egress", "latency"]),
            MP("Processing model change is addressed", ["batch", "stream", "parallel", "map", "distributed processing", "move the computation"]),
            MP("Cost and skills are addressed", ["cost", "bill", "staff", "skills", "expertise", "training"]),
            MP("Resilience and failure handling are addressed", ["failure", "resilien", "retry", "availability", "backup", "zone"]),
            MP("A judgement about the hardest challenge and why", ["hardest", "most difficult", "biggest", "overall", "therefore", "underestimated"])],
           "The first challenge is that the familiar answer stops working. A single server is improved by scaling up, and big data is by definition the point at which no affordable single machine is large enough, so storage has to become a cluster with the data partitioned across nodes for parallel processing and replicated so that a lost machine loses nothing. That immediately introduces a cost the organisation has not had to think about before: replicas can briefly disagree, so the immediate consistency a relational database guaranteed is replaced in many stores by eventual consistency, and every application has to be examined to see whether it can tolerate that. A balance cannot; a dashboard count can. The second challenge is movement. Data has weight, and at terabyte and petabyte scale the network becomes the binding constraint rather than storage: a migration that would take weeks of continuous transfer may need physical shipment, and cloud egress charges mean that moving data out later is a budget decision rather than a technical one. This is why the governing design principle inverts, from bringing data to the analysis to sending the computation to the machines that already hold the blocks. Third, the processing model changes. Queries become distributed jobs that split, process in parallel and combine, and workloads divide into batch for reporting and retraining and streaming for anything whose value decays within seconds, each needing different tooling and different thinking. Fourth, failure stops being an incident. With hundreds of components something is always broken, so jobs have to be retried, idempotent and checkpointed, and resilience has to be designed rather than hoped for. Finally there is cost and capability: elastic cloud capacity is genuinely cheaper than idle on premise hardware, but a runaway query that scans the whole lake produces a bill nobody approved, so cost monitoring belongs in the architecture, and the platform needs people who have run a distributed system before. Weighing these, the hardest challenge is not any of the technical ones; it is the skills and governance gap. Clusters can be rented in an afternoon, whereas the discipline to catalogue a lake, define ownership, control cost and reason correctly about consistency takes far longer to build, and it is the absence of that discipline, rather than any shortage of capacity, that turns most big data projects into expensive storage.",
           command="Discuss"),
    ],
)

# ============================================================== F201 TA3

B_ML = Topic(
    slug="machine-learning-and-ai",
    title="F201 TA3: Big Data with Machine Learning and AI",
    spec="F201 TA3",
    icon="i-brain",
    minutes=32,
    blurb="What machine learning actually is, the three kinds of learning, how a model is trained and tested, and how to tell whether it works.",
    fact="A model that predicts a rare disease by always answering 'no' can be 99% accurate and completely useless. That single observation is why accuracy is never reported alone, and it is the most reliable exam question in this topic area.",
    sections=[
        Section("AI, machine learning and deep learning", """
These three are often used as synonyms and are not.

| Term | What it means |
| **Artificial intelligence** | The broad field of making systems perform tasks that appear to need intelligence. Includes rule based systems with no learning at all |
| **Machine learning** | Systems that improve at a task by finding patterns in data rather than by being explicitly programmed with rules |
| **Deep learning** | Machine learning using neural networks with many layers, which is what made image, speech and language processing work |

They nest: deep learning is part of machine learning, which is part of AI.

### Why big data and machine learning arrived together

A learning algorithm needs examples, and its performance improves with the number of good ones. Two things made modern machine learning practical at the same moment: enough **data**, because systems began logging everything, and enough **compute**, because GPUs could do the arithmetic in parallel. Neither alone was sufficient, which is why techniques invented decades earlier only became useful recently.

### The traditional approach against the learned one

To detect spam with rules, a programmer writes conditions: these words, these senders, these patterns. Every new trick needs a new rule, written by a human, forever. With machine learning, the system is given a large set of messages already labelled spam or not spam, finds the features that distinguish them, and is retrained as the tricks change. The rules are no longer written; they are derived, which is both the power and the problem, because nobody chose them and they can be hard to inspect.

!key The definition that earns the mark :: "Machine learning is a system that learns patterns from data in order to make predictions or decisions, improving with more examples, rather than following rules written explicitly by a programmer."
"""),
        Section("The three kinds of learning, and the tasks", """
| Type | What it is given | What it learns | Examples |
| **Supervised** | Labelled examples: inputs with the right answer | To predict the label for new inputs | Spam detection, credit scoring, image classification, price prediction |
| **Unsupervised** | Unlabelled data | Structure that was not specified: groups, oddities, dimensions | Customer segmentation, anomaly detection, topic discovery |
| **Reinforcement** | An environment, actions and rewards | A policy of actions that maximises long run reward | Game playing, robotics, routing, energy control |

### The tasks within supervised learning

- **Classification** predicts a category: spam or not, which of ten digits, will churn or will not
- **Regression** predicts a number: a price, a demand, a time to failure

### And within unsupervised learning

- **Clustering** groups similar records, without being told the groups
- **Anomaly detection** finds records unlike the rest, which is how fraud and faults surface
- **Dimensionality reduction** compresses many variables into a few that carry most of the signal

### The vocabulary of a model

| Term | Meaning |
| **Feature** | An input variable the model uses |
| **Label** | The correct answer, in supervised learning |
| **Feature engineering** | Creating useful inputs from raw data, which often matters more than the algorithm |
| **Training set** | The data the model learns from, typically most of it |
| **Validation set** | Held back to tune the model and compare options |
| **Test set** | Held back, untouched, to estimate real performance once |
| **Overfitting** | Learning the training data including its noise, so performance collapses on new data |
| **Underfitting** | Too simple to capture the real pattern, so it is poor on everything |
| **Hyperparameter** | A setting chosen before training, such as depth or learning rate |

!warn Never evaluate on the training data :: A model tested on what it learned from will look excellent and tell you nothing. The test set has to be data the model has never seen, and it is used once, at the end. Testing repeatedly on it turns it into another training set.
"""),
        Section("Measuring whether a model works", """
### The confusion matrix

For a classifier, every prediction falls into one of four cells.

| | Predicted positive | Predicted negative |
| **Actually positive** | True positive (TP) | False negative (FN), a miss |
| **Actually negative** | False positive (FP), a false alarm | True negative (TN) |

### The measures that come out of it

| Measure | Formula | The question it answers |
| **Accuracy** | (TP + TN) / all | What proportion of predictions were right? |
| **Precision** | TP / (TP + FP) | When it says positive, how often is it right? |
| **Recall** | TP / (TP + FN) | Of the real positives, how many did it find? |
| **F1 score** | the harmonic mean of precision and recall | A single figure balancing the two |

### Why accuracy alone is misleading

Suppose 1 in 100 transactions is fraudulent. A model that predicts "not fraud" every single time is **99% accurate** and catches nothing at all. Its recall is zero. On an imbalanced problem, accuracy measures the imbalance rather than the model, which is why precision and recall are reported together.

### Precision against recall is a business decision

Tightening a model to raise precision lowers recall and vice versa. Which matters more depends entirely on the cost of each error:

- **Cancer screening**: a missed case is catastrophic, a false alarm means a further test. Favour **recall**.
- **Spam filtering**: a missed spam is an annoyance, a blocked job offer is serious. Favour **precision**.
- **Fraud blocking**: blocking a real customer's card loses them; missing a fraud costs money. The threshold is a commercial judgement, and it is usually set so a human reviews the uncertain middle.

For regression, the equivalent measures are **mean absolute error** and **root mean squared error**, in the units of the thing being predicted, which is why an error of "£38 per order" communicates better than any coefficient.

### Applications across industries

| Sector | Application |
| **Retail** | Recommendation, demand forecasting, dynamic pricing, churn prediction |
| **Finance** | Fraud detection, credit scoring, anti money laundering, trading |
| **Healthcare** | Image diagnosis, triage, drug discovery, readmission risk |
| **Manufacturing** | Predictive maintenance, visual quality inspection, yield optimisation |
| **Transport** | Routing, demand prediction, autonomous driving, maintenance |
| **Energy** | Load forecasting, grid balancing, fault prediction |
| **Agriculture** | Yield prediction, disease detection from imagery, irrigation control |
| **Public sector** | Demand planning, fraud detection, triage of casework |

!grade Name the measure and the cost of the error :: "Recall matters more here, because a missed fraudulent transaction is an unrecoverable loss while a false positive costs one customer service call, so the threshold should be set low and the borderline cases sent for human review." Measure, reason, and the operational consequence.
"""),
    ],
    keyterms=[
        ("Artificial intelligence", "The field of making systems perform tasks that appear to require intelligence."),
        ("Machine learning", "Systems that learn patterns from data rather than following explicitly programmed rules."),
        ("Deep learning", "Machine learning using neural networks with many layers."),
        ("Supervised learning", "Learning from labelled examples to predict labels for new data."),
        ("Unsupervised learning", "Finding structure in unlabelled data, such as clusters or anomalies."),
        ("Reinforcement learning", "Learning a policy of actions through rewards and penalties from an environment."),
        ("Classification", "Predicting which category something belongs to."),
        ("Regression", "Predicting a numerical value."),
        ("Clustering", "Grouping similar records without being told the groups in advance."),
        ("Feature", "An input variable used by a model."),
        ("Label", "The known correct answer attached to a training example."),
        ("Training data", "The data a model learns from."),
        ("Test data", "Held-back data, never seen in training, used to estimate real performance."),
        ("Overfitting", "Learning the training data including its noise, so performance on new data collapses."),
        ("Confusion matrix", "A table of true and false positives and negatives for a classifier."),
        ("Precision", "Of the cases predicted positive, the proportion that really are."),
        ("Recall", "Of the real positive cases, the proportion the model found."),
        ("Accuracy", "The proportion of all predictions that were correct."),
    ],
    grade="""
This topic area rewards **arithmetic and judgement together**. Be able to compute precision and recall from a confusion matrix, state what each means in the scenario's own terms, and then say which one the organisation should optimise and what that costs. An answer that defines the terms without applying them to the scenario stays in the lower bands.
""",
    mistakes=[
        "Using AI, machine learning and deep learning as synonyms.",
        "Quoting accuracy on an imbalanced problem without mentioning precision and recall.",
        "Evaluating a model on its training data.",
        "Confusing overfitting with underfitting.",
        "Describing clustering as supervised. Nobody provides the groups.",
        "Treating a model's output as fact rather than as a prediction with an error rate.",
    ],
    quiz=[
        Q("Which type of learning uses labelled training data?",
          ["Supervised", "Unsupervised", "Reinforcement", "Deep"], 0,
          "Labels are the defining feature of supervised learning."),
        Q("Grouping customers into segments without being told the segments is:",
          ["Unsupervised learning, specifically clustering",
           "Supervised classification", "Reinforcement learning",
           "Regression"], 0,
          "No labels are provided, so the structure is discovered rather than predicted."),
        Q("A model predicts a house price. What kind of task is that?",
          ["Regression", "Classification", "Clustering", "Anomaly detection"], 0,
          "The output is a number, which makes it regression."),
        Q("1 in 100 transactions is fraud. A model predicts 'not fraud' every time. What is its accuracy and recall?",
          ["99% accuracy, 0% recall", "99% accuracy, 99% recall",
           "1% accuracy, 0% recall", "50% accuracy, 50% recall"], 0,
          "It is right 99 times in 100 and finds none of the fraud, which is why accuracy alone is useless here."),
        Q("What is overfitting?",
          ["The model learns the training data's noise and fails on new data",
           "The model is too simple for the pattern",
           "The training set is too small",
           "The model runs too slowly"], 0,
          "It performs superbly on data it has seen and poorly on anything else."),
        Q("Precision answers which question?",
          ["When the model predicts positive, how often is it right?",
           "Of the real positives, how many were found?",
           "What proportion of all predictions were correct?",
           "How fast does the model run?"], 0,
          "Precision is TP divided by all predicted positives."),
        Q("For cancer screening, which measure should usually be favoured?",
          ["Recall, because a missed case is far more costly than a false alarm",
           "Precision, because false alarms are expensive",
           "Accuracy, because it summarises both",
           "Neither, speed matters most"], 0,
          "A missed case may be fatal; a false alarm means another test."),
        Q("Why must the test set be kept separate from training?",
          ["Otherwise the measured performance is meaningless",
           "To reduce training time", "To save storage",
           "Because the law requires it"], 0,
          "A model tested on what it memorised looks excellent and tells you nothing."),
        Q("Which is reinforcement learning?",
          ["A system learning to control heating by trial and reward",
           "Classifying emails from labelled examples",
           "Grouping products by similarity",
           "Predicting next month's sales"], 0,
          "Actions, an environment and a reward signal define reinforcement learning."),
        Q("Deep learning is best described as:",
          ["Machine learning using neural networks with many layers",
           "Any very large machine learning model",
           "A synonym for artificial intelligence",
           "Learning from very large datasets only"], 0,
          "The depth refers to the number of layers in the network."),
    ],
    exam=[
        EQ("State the difference between supervised and unsupervised learning.", 2,
           [MP("Supervised learning uses labelled data to predict a known target", ["labelled", "labels", "known answer", "target", "predict"]),
            MP("Unsupervised learning finds structure in unlabelled data", ["unlabelled", "no labels", "structure", "patterns", "groups", "clusters"])],
           "Supervised learning is trained on labelled examples, where each input has a known correct answer, and learns to predict that answer for new data. Unsupervised learning is given unlabelled data and finds structure within it, such as clusters of similar records or anomalies, without being told what to look for.",
           command="State"),
        EQ("A spam filter was tested on 1,000 emails. It correctly identified 180 spam emails, wrongly flagged 20 legitimate emails as spam, and missed 40 spam emails.\n\nCalculate its precision and recall, and explain which matters more for a spam filter.", 6,
           [MP("Precision is calculated as 180/200", ["180", "200", "90", "0.9"]),
            MP("Precision is stated as 90%", ["90%", "90 per cent", "0.9"]),
            MP("Recall is calculated as 180/220", ["220", "180", "81.8", "0.818"]),
            MP("Recall is stated as about 82%", ["82", "81.8", "0.82"]),
            MP("Precision is identified as more important for a spam filter", ["precision", "false positive", "legitimate email"]),
            MP("Justified by the cost of the error", ["important email", "job offer", "blocked", "lost", "worse than", "missed spam is only"])],
           "Precision is true positives divided by all predicted positives: 180 / (180 + 20) = 180 / 200 = 90%. Recall is true positives divided by all actual positives: 180 / (180 + 40) = 180 / 220 = 81.8%. For a spam filter, precision matters more. A false negative means one piece of spam reaches the inbox, which costs the user a moment's irritation and nothing else. A false positive means a legitimate email is hidden in a folder the user may never check, and if that email is a job offer, an invoice or a medical appointment the consequence is serious and the user is not even aware anything was lost. A spam filter is therefore tuned to be cautious about declaring spam, accepting a lower recall in exchange for very high precision.",
           command="Calculate"),
        EQ("Explain what overfitting is and describe **two** ways it can be reduced.", 5,
           [MP("Overfitting is learning the training data including its noise", ["noise", "memoris", "too closely", "specific to the training"]),
            MP("The consequence on unseen data", ["new data", "unseen", "poorly", "does not generalise", "test set"]),
            MP("One valid mitigation", ["more data", "simpler model", "regularis", "cross validation", "fewer features", "early stopping", "prune"]),
            MP("It is explained", ["because", "prevents", "reduces", "forces"]),
            MP("A second valid mitigation, explained", ["validation set", "cross validation", "more training data", "dropout", "simplify", "because"])],
           "Overfitting happens when a model learns the training data too closely, capturing not only the real pattern but also the noise and the accidents of that particular sample. The symptom is a model that performs almost perfectly on the data it was trained on and markedly worse on data it has never seen, because it has effectively memorised rather than generalised. One way to reduce it is to use a simpler model or fewer features, since a model with less capacity cannot fit the noise; a shallow decision tree, or a pruned one, is forced to find the broad pattern. A second is to train on more data, because noise does not repeat while the real pattern does, so additional examples dilute the accidental features. Alongside both, holding back a validation set and stopping training when validation performance stops improving detects overfitting as it begins rather than after the model is deployed.",
           command="Explain"),
        EQ("A hospital is considering a machine learning model to predict which patients are at risk of readmission within 30 days.\n\nDiscuss how such a model would be developed and evaluated, and the issues the hospital should consider before using it.", 8,
           [MP("Data and features are identified", ["features", "data", "age", "diagnosis", "previous admissions", "medication", "length of stay"]),
            MP("It is identified as supervised classification with labels from history", ["supervised", "labelled", "historic", "was readmitted", "classification"]),
            MP("Train, validation and test split is described", ["training", "test", "validation", "held back", "split", "unseen"]),
            MP("Appropriate evaluation measures are chosen", ["recall", "precision", "confusion matrix", "not accuracy", "imbalanced", "F1"]),
            MP("Recall is prioritised with a reason", ["recall", "missed", "false negative", "patient harm", "worse"]),
            MP("Bias in the training data is addressed", ["bias", "under-represent", "deprived", "ethnic", "historic inequal", "unfair"]),
            MP("Explainability and clinical oversight are addressed", ["explain", "black box", "clinician", "human", "decision support", "accountab"]),
            MP("Legal, ethical or monitoring issues with a judgement", ["special category", "GDPR", "DPIA", "consent", "monitor", "drift", "retrain", "therefore"])],
           "The task is supervised classification, and the labels already exist in the hospital's own history: for every past discharge it is known whether the patient was readmitted within thirty days. Features would come from the records the hospital already holds, such as age, primary and secondary diagnoses, length of stay, number of previous admissions, prescribed medication, and whether the patient lives alone, with feature engineering likely to matter more than the choice of algorithm. The data would be split into training, validation and test sets, and the split should be by time rather than at random, training on earlier years and testing on the most recent, because that is the only way to estimate how the model will behave on future patients rather than on contemporaries of its training data. Evaluation must not rest on accuracy. Readmission is a minority outcome, so a model predicting that nobody is readmitted would score well and be worthless; the hospital needs the confusion matrix and both precision and recall. Recall should be prioritised, because a missed high risk patient is a patient who comes back seriously unwell, while a false positive costs a follow-up phone call, so the threshold should be set to catch cases and the resulting workload planned for. Three issues then need settling before any use. The first is bias: if historic care was less effective for a deprived or minority group, the model learns that pattern as though it were clinical fact, so performance has to be measured separately for each group rather than only overall, and an unequal error rate treated as a defect. The second is explainability: a clinician cannot act on a score with no reason attached, and the hospital cannot defend a decision it cannot explain, so a model whose contributing factors can be surfaced is worth more here than a slightly more accurate opaque one. The third is legal and operational: this is special category health data, which means a Data Protection Impact Assessment, transparency with patients, and no solely automated decision with significant effects. Taken together, the model should be deployed as decision support that flags patients for a clinician to review, never as an automated discharge or intervention decision, with its performance and its error rates by group monitored continuously and the model retrained as practice and population change.",
           command="Discuss"),
    ],
)

# ============================================================== F201 TA4

B_ETHICS = Topic(
    slug="legal-and-ethical-issues",
    title="F201 TA4: Legal and Ethical Issues in Data Management",
    spec="F201 TA4",
    icon="i-shield",
    minutes=28,
    blurb="What changes legally and ethically when the dataset is enormous and a model is making the decisions: bias, transparency, profiling and accountability.",
    fact="A recruitment model trained on a decade of a company's own hiring decisions learned to downgrade applications that mentioned women's colleges. Nobody programmed that. It was in the historic data, and the model treated the past as a specification.",
    sections=[
        Section("Data protection at big data scale", """
The law is the same law as in F200. What changes is that big data practice pushes against the principles rather than fitting neatly inside them.

| Principle | Where big data strains it |
| **Purpose limitation** | The whole premise of a data lake is keeping data for purposes not yet identified |
| **Data minimisation** | Models improve with more features, which pulls directly against collecting less |
| **Storage limitation** | Training sets are kept to allow reproducibility and retraining |
| **Transparency** | It is hard to tell somebody what you will infer when you do not know yet |
| **Accuracy** | A prediction about a person is not a fact about them, yet it is stored like one |
| **Accountability** | A derived model is harder to audit than a query |

### Inference is processing

If a model infers that a customer is probably pregnant, has a health condition or holds a religious belief, the organisation is processing special category data even though nobody entered it and the customer never disclosed it. That the information is inferred rather than collected makes no difference to the duties attached to it, and this is the single point in this topic area most often missed.

### Automated decision making and profiling

Under the UK GDPR a person has the right not to be subject to a **solely automated decision** with legal or similarly significant effects, such as a credit refusal, an insurance price or a job rejection, unless a specific condition applies. Where such processing is permitted, the safeguards are meaningful human involvement, an explanation of the logic, and a route to contest the outcome. "The system decided" is not a defence.

### Consent at scale

Consent must be freely given, specific and informed, and withdrawable. None of that fits a model trained on everybody's data at once, because a specific consent cannot be given to an unspecified future inference, and withdrawal is almost impossible to honour once the data has been absorbed into a trained model. This is why serious organisations rely on a documented legitimate interests assessment, with a real balancing test, rather than on a consent they could not evidence.
"""),
        Section("Bias, fairness and transparency", """
### Where bias actually comes from

| Source | How it happens |
| **Historic bias** | The training data records past human decisions, including unfair ones |
| **Sampling bias** | A group is under-represented, so the model performs worse for them |
| **Measurement bias** | The chosen proxy is not the thing you care about: arrests are not crime, clicks are not interest |
| **Label bias** | The labels were applied by people with their own assumptions |
| **Aggregation bias** | One model applied to groups that genuinely behave differently |
| **Deployment bias** | A model used for a purpose or population it was never trained for |
| **Feedback loops** | The model's own output becomes tomorrow's training data and the bias compounds |

Removing the protected characteristic from the features does not remove the bias, because other fields act as proxies for it: postcode, school, first name, purchase history. A model can discriminate effectively without ever seeing the attribute, and under the Equality Act the outcome is what matters, not the intent or the feature list.

### Testing for it

Measure performance **per group**, not just overall. If recall is 88% for one group and 61% for another, the headline accuracy has concealed a system that works for some people and not others. Then decide what fairness means for this application, because the definitions conflict mathematically and you cannot have all of them at once: equal error rates, equal selection rates, or equal treatment of similar individuals.

### Transparency and explainability

- **Explainability**: can the factors behind an individual decision be stated?
- **Interpretability**: can a person understand how the model works overall?
- **The black box problem**: the most accurate models are often the least inspectable, which is a genuine trade-off, not a technical gap waiting to be closed
- **The right to an explanation**: where an automated decision significantly affects someone, they are entitled to meaningful information about the logic involved

!key Accuracy is not the only criterion :: A slightly less accurate model whose reasoning can be explained and audited is frequently the better choice, because a decision that cannot be explained cannot be defended, corrected or appealed.
"""),
        Section("Ownership, security and accountability", """
### Who owns data

- **Personal data** is not owned by the organisation holding it; the individual has rights over it regardless
- **Database right** protects a database that required substantial investment to assemble, which is what makes scraping someone else's dataset an infringement
- **Derived data** and models trained on other people's data raise ownership questions the law is still settling
- **Contracts** usually decide ownership of data generated by a product in use, and customers rarely read that clause
- **Open data licences** permit reuse on stated conditions, and those conditions are enforceable

### Security at scale

The impact of a breach scales with what you kept. The specific big data risks:

- **Concentration**: one lake holds what used to be in twenty systems, so one failure exposes everything
- **Re-identification**: datasets individually anonymous become identifying when joined
- **Misconfiguration**: the public storage bucket, which causes more exposure than any attack
- **Insider access**: analysts with broad access to the whole estate
- **Supply chain**: a compromised vendor or library reaching your pipeline
- **Model attacks**: extracting training data from a model, or poisoning the training set to change its behaviour

### Surveillance, autonomy and manipulation

- **Workplace monitoring**: keystrokes, location, productivity scores, and the question of proportionality
- **Behavioural advertising**: profiles built across sites and apps, mostly invisible to the person profiled
- **Dark patterns**: interfaces designed so that the privacy-protecting choice is the hard one
- **Price discrimination**: different prices for different people, from inferred willingness to pay
- **Filter bubbles**: optimisation for engagement narrowing what a person is shown
- **Chilling effects**: people behaving differently because they believe they are observed

### Accountability

Somebody has to be answerable. In practice that means: a named owner for each model and dataset; a documented impact assessment before deployment; a human in the loop for consequential decisions; monitoring for drift and for unequal outcomes; an appeal route for the person affected; and an audit trail showing what the model did and on what data.

!grade The structure that scores on an ethics question :: Identify the specific harm and who bears it. Name the law or principle engaged. Weigh the benefit honestly rather than dismissing it. Reach a conclusion with a safeguard attached. A balanced answer that decides outscores a one-sided one every time.
"""),
    ],
    keyterms=[
        ("Inferred data", "Information a model derives about a person, which is personal data even though it was never disclosed."),
        ("Profiling", "Automated processing to evaluate or predict aspects of a person's behaviour or characteristics."),
        ("Automated decision making", "A decision made by a system without meaningful human involvement."),
        ("Algorithmic bias", "Systematic unfairness in a model's outputs, usually inherited from its training data."),
        ("Proxy variable", "A field that stands in for a protected characteristic, such as postcode for ethnicity."),
        ("Explainability", "The ability to state the factors behind an individual automated decision."),
        ("Black box model", "A model whose internal reasoning cannot practically be inspected."),
        ("Re-identification", "Linking anonymised data back to individuals, often by joining datasets."),
        ("Database right", "Protection for a database whose contents required substantial investment to assemble."),
        ("Dark pattern", "An interface designed to steer users away from the choice that protects them."),
        ("Data poisoning", "Deliberately corrupting training data so a model behaves as the attacker intends."),
        ("Model drift", "The decline in a model's performance as the world it was trained on changes."),
    ],
    grade="""
Top band answers are **balanced and decisive**. State the benefit, state the harm, name the law or principle, then conclude with a safeguard. Answers that only condemn, or only enthuse, stay in the middle bands however much detail they contain.
""",
    mistakes=[
        "Thinking inferred information escapes data protection law. Inference is processing.",
        "Claiming that removing the protected characteristic removes the bias. Proxies remain.",
        "Reporting only overall accuracy, which hides unequal performance between groups.",
        "Treating 'the algorithm decided' as an explanation or a defence.",
        "Assuming aggregated data is automatically anonymous.",
        "Writing a one-sided answer. The marks are for weighing both sides and concluding.",
    ],
    quiz=[
        Q("A model infers that a customer is probably pregnant. What is that data?",
          ["Special category personal data", "Anonymous statistical data",
           "The company's own intellectual property only",
           "Not personal data, because it was inferred"], 0,
          "Inference is processing, and health information is special category data however it arose."),
        Q("Why does removing ethnicity from the features not remove racial bias?",
          ["Other fields such as postcode act as proxies for it",
           "Models always discriminate", "The field is still stored elsewhere",
           "It does remove the bias"], 0,
          "Proxy variables let a model reproduce the pattern without ever seeing the attribute."),
        Q("Under the UK GDPR, a person has the right not to be subject to:",
          ["A solely automated decision with significant effects, without safeguards",
           "Any automated processing at all",
           "Having their data stored in the cloud",
           "Being included in a training set"], 0,
          "Where such processing is allowed, there must be human involvement, an explanation and a route to contest it."),
        Q("A recruitment model trained on past hiring decisions downgrades certain applicants. What is this?",
          ["Historic bias learned from the training data",
           "A programming error", "Sampling bias",
           "Data poisoning"], 0,
          "The model treated past human decisions as a specification for the future."),
        Q("What is the black box problem?",
          ["The most accurate models are often the least inspectable",
           "Models cannot store their training data",
           "Encrypted models cannot be audited",
           "Models fail without warning"], 0,
          "It is a genuine trade-off between accuracy and explainability."),
        Q("Why should model performance be measured per group?",
          ["Overall accuracy can hide a model that works for some people and not others",
           "To reduce training time", "The law requires equal accuracy",
           "To increase the sample size"], 0,
          "An 88% recall for one group and 61% for another averages to something that looks acceptable."),
        Q("What is data poisoning?",
          ["Corrupting training data so the model behaves as the attacker wants",
           "Deleting a training set", "Overfitting a model",
           "Introducing noise for privacy"], 0,
          "It attacks the model through its inputs rather than through its code."),
        Q("What is a dark pattern?",
          ["An interface that steers users away from the privacy-protecting choice",
           "A hidden data processing activity", "An unexplainable model",
           "A security vulnerability"], 0,
          "Accept-all in one tap and refuse in six is the classic example."),
        Q("What is model drift?",
          ["Performance declining as the world the model was trained on changes",
           "A model gradually using more memory",
           "The model's predictions becoming more confident",
           "Training data being lost over time"], 0,
          "It is why deployed models need monitoring and retraining rather than being finished."),
        Q("Which is the strongest argument for a slightly less accurate but explainable model?",
          ["A decision that cannot be explained cannot be defended or appealed",
           "Explainable models are always faster",
           "Accuracy does not matter",
           "The law bans complex models"], 0,
          "Accountability needs an explanation, and the affected person needs a route to challenge it."),
    ],
    exam=[
        EQ("State **two** sources of bias in a machine learning model.", 2,
           [MP("One valid source", ["historic", "training data", "sampling", "under-represent", "label", "measurement", "proxy"]),
            MP("A second, different source", ["sampling", "label", "measurement", "deployment", "feedback", "historic"])],
           "Historic bias, where the training data records past unfair human decisions, and sampling bias, where a group is under-represented in the training data.",
           command="State"),
        EQ("Explain why data inferred by a model about an individual is still subject to data protection law.", 4,
           [MP("Inferred information relates to an identifiable person", ["relates to", "about a person", "identifiable", "individual"]),
            MP("It therefore meets the definition of personal data", ["personal data", "definition", "counts as"]),
            MP("Inferring it is itself processing", ["processing", "generating", "creating data", "deriving"]),
            MP("A consequence, such as special category duties or rights applying", ["special category", "health", "rights", "access", "accuracy", "must be told", "transparen"])],
           "Personal data is any information relating to an identified or identifiable living person, and that definition does not depend on how the information arose. A model's inference that a particular customer is likely to be pregnant, in financial difficulty or of a given religious belief relates directly to that individual, so it is personal data in exactly the way a declared field would be. Generating the inference is itself processing, which needs a lawful basis and must be transparent. The consequences are substantial: where the inference concerns health, religion or sexual orientation it is special category data requiring an additional condition, the individual can request access to it and dispute its accuracy, and because a prediction is not a fact the organisation must be careful not to present it as one.",
           command="Explain"),
        EQ("An insurer plans to use social media activity and shopping data to set premiums.\n\nDiscuss the legal and ethical problems with this, and what safeguards would be needed.", 8,
           [MP("Purpose limitation and the original collection purpose are addressed", ["purpose", "not collected for", "reuse", "incompatible"]),
            MP("Transparency is addressed", ["told", "privacy notice", "aware", "transparen", "hidden"]),
            MP("Special category data by inference is addressed", ["special category", "health", "religion", "infer", "sensitive"]),
            MP("Automated decision making rights are addressed", ["automated", "significant effect", "human", "contest", "explanation"]),
            MP("Discrimination or proxy variables are addressed", ["discriminat", "proxy", "postcode", "Equality Act", "protected", "unfair"]),
            MP("Accuracy and the harm of a wrong inference are addressed", ["accuracy", "wrong", "incorrect", "cannot challenge", "false"]),
            MP("Specific safeguards are proposed", ["DPIA", "human review", "appeal", "explain", "audit", "per group", "minimis"]),
            MP("A judgement weighing the insurer's interest against the harm", ["legitimate", "risk pricing", "however", "on balance", "should not", "only if"])],
           "The insurer has a genuine interest here, since pricing risk accurately is what insurance is, and a model that prices more precisely can lower premiums for lower-risk customers. But the proposal has serious problems. The data was not collected for this: posts and purchases were made for social and commercial purposes, and reusing them to price insurance is a different and incompatible purpose, which engages purpose limitation and means the insurer cannot simply help itself to data that happens to be accessible. Transparency compounds it, because customers would have no realistic idea that their shopping history was affecting their premium, and a privacy notice that technically mentions it does not make the processing fair. The inferences themselves are the legal centre of the problem: shopping and social data are highly revealing, and a model will infer pregnancy, mental health, alcohol consumption and religious observance whether or not it is asked to, which means the insurer would be processing special category data and needs a specific condition for doing so. Because the outcome, a price or a refusal, has a significant effect on the individual, the rules on solely automated decision making apply, so there must be meaningful human involvement, an explanation of the logic and a route to contest the result. Discrimination is the ethical core. Removing protected characteristics from the model does not help, because postcode, store, brand and vocabulary are proxies, and under the Equality Act it is the outcome that matters: a model that prices higher for an ethnic group or a disabled customer is unlawful however innocent the feature list looks. Accuracy makes it worse rather than better, because a wrong inference, a gift bought for someone else, a parody account, produces a real financial penalty the customer cannot see, understand or appeal. The safeguards would have to be substantial: a Data Protection Impact Assessment before anything is built; the feature set cut to data the customer knowingly provided for insurance purposes; explicit exclusion of inferred special category data; testing of error and pricing rates per protected group with unequal outcomes treated as a defect; human review and a published appeal route for every adverse decision; and an audit trail allowing any individual price to be reconstructed and explained. On balance, the social media element should not proceed at all, because the purpose mismatch and the unavoidable inference of sensitive characteristics cannot be safeguarded away, while a narrow use of data the customer supplies for the policy itself can be defended provided the safeguards above are real rather than documentary.",
           command="Discuss"),
    ],
)

# ============================================================== F201 TA5

B_ENV = Topic(
    slug="environment-and-society",
    title="F201 TA5: Environment and Society",
    spec="F201 TA5",
    icon="i-gauge",
    minutes=26,
    blurb="What all this computing costs the planet, what green computing can actually do about it, and how big data is changing work and society.",
    fact="Training one large AI model can use as much electricity as a few hundred UK homes use in a year, and the data centre housing it may evaporate millions of litres of water doing it. Both figures are now reported, which is itself a recent change.",
    sections=[
        Section("The environmental cost", """
### Where the energy goes

| Source | Detail |
| **Servers** | Continuous power, whether busy or idle. An idle server still draws a large fraction of its peak |
| **Cooling** | Historically as much energy as the computing itself; modern designs have cut this sharply |
| **Storage** | Keeping data costs power continuously, for years, whether or not it is read |
| **Networking** | Moving data between regions and to users |
| **Model training** | Weeks of thousands of GPUs, repeated every time a model is retrained |
| **Inference** | Each individual query is small, and multiplied by billions it exceeds the training cost |

### Power usage effectiveness

**PUE** is total facility power divided by the power delivered to the computing equipment. A PUE of 2.0 means half the electricity is spent on cooling and overheads; the best modern facilities run close to 1.1. It is the standard measure, and it is examinable.

### Water and materials

Evaporative cooling consumes fresh water, which matters where data centres sit in water-stressed regions. Hardware manufacture needs mined metals including rare earths, with their own extraction impact, and a three to five year replacement cycle produces **e-waste** containing both valuable and hazardous materials. Only a minority of global e-waste is formally recycled.

### Carbon, and why location matters

The same workload produces very different emissions depending on the grid it runs on. A job run where the grid is coal-heavy can emit several times what it would on a grid dominated by wind, hydro or nuclear, which is why the location and the timing of a workload are now genuine environmental decisions rather than purely technical ones.

!warn Storing everything has a carbon cost, not just a bill :: A data lake nobody queries still draws power every second of every year. Deleting data that serves no purpose is both a data protection duty under storage limitation and the simplest environmental saving available.
"""),
        Section("Green computing", """
### What actually reduces the impact

| Measure | How it helps |
| **Virtualisation and consolidation** | Many workloads on fewer physical machines, so fewer idle servers |
| **Elastic scaling** | Capacity released when the job finishes rather than running all night |
| **Efficient hardware** | Newer processors and accelerators do far more work per watt |
| **Renewable supply** | Buying or generating clean power, ideally matched hour by hour rather than annually |
| **Carbon aware scheduling** | Running flexible batch jobs when and where the grid is cleanest |
| **Better cooling** | Free air cooling, liquid cooling, warm-water loops, cold climates |
| **Heat reuse** | Waste heat piped to district heating or swimming pools |
| **Efficient code and queries** | A query scanning one column instead of a whole table costs a fraction of the energy |
| **Model efficiency** | Smaller models, pruning, quantisation, reusing a pretrained model rather than training from scratch |
| **Data retention** | Deleting what has no purpose, and archiving cold data to lower-power storage |
| **Hardware lifecycle** | Longer refresh cycles, repair, resale, certified recycling |

### The analyst's own contribution

- Do not re-run the query every five minutes if the data updates daily
- Filter and aggregate at the source rather than pulling everything and discarding most of it
- Partition tables so a query touches the partitions it needs
- Cache results that many people request
- Delete intermediate datasets when the pipeline is finished
- Reuse a pretrained model rather than training one from nothing

### Rebound effects, honestly

Efficiency does not automatically reduce total consumption, because cheaper computing gets used more. Data centre efficiency has improved dramatically while total data centre energy use has continued to rise, since the work has grown faster than the efficiency. An honest answer acknowledges this rather than presenting efficiency as a solution on its own.
"""),
        Section("Society, work and culture", """
### Employment

| Effect | Detail |
| **Automation of routine work** | Data entry, basic reporting, first-line support, routine document review |
| **New roles** | Data engineers, analysts, scientists, ML engineers, governance and AI ethics roles |
| **Changed roles** | Most jobs gain a data component rather than disappearing: clinicians, farmers, marketers, mechanics |
| **Polarisation** | Growth at both ends of the skill range and hollowing in the middle |
| **Skills gap** | Persistent shortage of people able to do the new work, and a retraining problem for those displaced |
| **Monitoring at work** | Productivity measured continuously, which changes the experience of work itself |

### Society and culture

- **Personalisation and filter bubbles**: recommendation optimised for engagement narrows what people see, and the effect is strongest on contested topics
- **Misinformation**: synthetic text, images and video are cheap to produce and hard to detect, which shifts the burden to verification
- **The digital divide**: benefits accrue to people and regions with connectivity, devices and skills; those without fall further behind, and public services moving online deepens it
- **Public health and research**: population-scale data has produced genuine advances in outbreak detection, screening and treatment
- **Smart cities**: transport, energy and waste optimised against real demand, alongside the surveillance that comes with it
- **Trust**: a visible breach or a visibly unfair algorithm damages trust across the whole sector, not just the organisation responsible
- **Attention and wellbeing**: systems optimised to maximise time spent have measurable effects on sleep and mental health, particularly for younger users

### A balanced position

Big data is not a force with a single direction. The same capability that detects an outbreak early also enables surveillance; the same recommendation engine that helps somebody find work also narrows what they see. The examinable skill is weighing a specific application rather than judging the technology as a whole, and strong answers do exactly that: name the benefit, name the cost, say who carries each, and conclude with what would have to be true for it to be worth doing.

!grade What a top band answer looks like here :: It quantifies something, names a measure such as PUE or a retention period, acknowledges a rebound effect or a trade-off, and reaches a clear conclusion that somebody could act on. Lists of advantages and disadvantages with no judgement stay in the middle bands.
"""),
    ],
    keyterms=[
        ("PUE", "Power usage effectiveness: total facility power divided by power used by the computing equipment."),
        ("Green computing", "Designing and operating computing to reduce its environmental impact."),
        ("Carbon aware scheduling", "Running flexible workloads when or where the electricity grid is cleanest."),
        ("E-waste", "Discarded electronic equipment, containing both valuable and hazardous materials."),
        ("Virtualisation", "Running several logical machines on one physical machine to reduce idle hardware."),
        ("Heat reuse", "Capturing waste heat from a data centre for another purpose such as district heating."),
        ("Rebound effect", "The tendency for efficiency gains to be offset by increased use."),
        ("Digital divide", "The gap between those with access to technology, connectivity and skills and those without."),
        ("Filter bubble", "The narrowing of what a person sees caused by personalisation optimised for engagement."),
        ("Model inference", "Using a trained model to make a prediction, whose cumulative energy cost can exceed training."),
    ],
    grade="""
Quantify, name a measure, and decide. "Their PUE is 1.6, so 60% overhead on top of the computing load; moving the flexible nightly jobs to a region with a cleaner grid and raising the inlet temperature would cut both, though the saving will be partly offset as the freed capacity gets used."
""",
    mistakes=[
        "Treating the environmental cost as only the electricity for the servers, and ignoring cooling, storage, water and manufacture.",
        "Assuming model training dominates. At scale, inference across billions of queries usually exceeds it.",
        "Presenting efficiency as a complete solution without acknowledging the rebound effect.",
        "Saying 'data is stored in the cloud so there is no environmental impact'.",
        "Writing only about job losses. Most roles change rather than disappear.",
        "Giving a list of advantages and disadvantages with no judgement at the end.",
    ],
    quiz=[
        Q("What does PUE measure?",
          ["Total facility power divided by power used by the computing equipment",
           "The proportion of renewable energy used",
           "Power used per query",
           "The efficiency of a processor"], 0,
          "A PUE of 2.0 means half the electricity goes on cooling and overheads."),
        Q("Which is usually the larger lifetime energy cost for a widely used AI model?",
          ["Inference, because of the number of queries",
           "Training, because it takes weeks",
           "Storage of the training data",
           "Network transfer"], 0,
          "Each query is small, but billions of them exceed the one-off training cost."),
        Q("What is carbon aware scheduling?",
          ["Running flexible jobs when or where the grid is cleanest",
           "Measuring a data centre's total emissions",
           "Buying carbon offsets for computing",
           "Shutting servers down overnight"], 0,
          "The same workload emits very differently depending on the grid powering it."),
        Q("Why does deleting unused data help the environment?",
          ["Stored data consumes power continuously whether or not it is read",
           "Deletion releases stored carbon",
           "It reduces network traffic only",
           "It does not; storage is free"], 0,
          "It is also a data protection duty under storage limitation."),
        Q("What is the rebound effect?",
          ["Efficiency gains are offset because cheaper computing gets used more",
           "Servers drawing more power after cooling",
           "Data growing back after deletion",
           "Models degrading over time"], 0,
          "Data centre efficiency has improved while total energy use has still risen."),
        Q("Which cooling approach reduces energy use?",
          ["Free air cooling in a cool climate", "Lower inlet temperatures",
           "More refrigeration units", "Running servers at full load constantly"], 0,
          "Using outside air avoids running refrigeration at all for much of the year."),
        Q("What is the digital divide?",
          ["The gap between those with access to technology and skills and those without",
           "The split between cloud and on-premise systems",
           "The difference between analogue and digital data",
           "The gap between data scientists and analysts"], 0,
          "It widens as essential services move online."),
        Q("Which best describes the effect of big data on employment?",
          ["Most roles change and gain a data component, while some routine roles are automated",
           "Nearly all jobs are replaced",
           "Employment is unaffected",
           "Only technology jobs are affected"], 0,
          "Routine work is automated, new specialist roles appear, and most existing roles change."),
        Q("Why is e-waste a particular concern for data centres?",
          ["Hardware is replaced every few years and contains hazardous materials",
           "Servers cannot be recycled at all",
           "Data centres produce more waste than households",
           "Hardware contains no valuable materials"], 0,
          "Short refresh cycles produce a continuous stream, and only a minority is formally recycled."),
        Q("Which would most reduce the energy cost of a daily report?",
          ["Querying only the partitions and columns it needs",
           "Running it every five minutes to keep it fresh",
           "Exporting the whole table and filtering locally",
           "Storing a copy in every region"], 0,
          "Scanning less data uses proportionately less energy, and the other options all increase it."),
    ],
    exam=[
        EQ("State **two** ways a data centre can reduce its energy consumption.", 2,
           [MP("One valid measure", ["cooling", "free air", "liquid", "virtualis", "consolidat", "efficient hardware", "renewable", "heat reuse", "scheduling"]),
            MP("A second, different valid measure", ["virtualis", "renewable", "heat reuse", "efficient", "cooling", "shut down", "schedul"])],
           "Using free air cooling rather than refrigeration where the climate allows it, and virtualising workloads so that fewer physical servers run, reducing the number sitting idle.",
           command="State"),
        EQ("Explain why the location of a data centre affects the carbon emissions of the work it does.", 4,
           [MP("Emissions depend on how the local electricity is generated", ["grid", "generated", "coal", "renewable", "mix", "electricity source"]),
            MP("The same workload can emit several times as much on a dirtier grid", ["same workload", "several times", "more", "differen", "varies"]),
            MP("Climate affects the cooling energy required", ["climate", "cool", "temperature", "free air", "hot country"]),
            MP("A consequence, such as carbon aware placement or scheduling", ["locate", "schedule", "move the workload", "choose a region", "flexible jobs"])],
           "The emissions from a computing workload come almost entirely from the electricity it consumes, and the carbon intensity of electricity varies enormously by grid: a kilowatt hour on a coal-dominated grid can carry several times the emissions of the same kilowatt hour on a grid dominated by wind, hydro or nuclear. The identical job therefore has a very different footprint depending only on where it runs. Location also changes how much electricity is needed in the first place, because a facility in a cool climate can use outside air for much of the year while one in a hot climate runs refrigeration continuously, and cooling has historically been a large share of total consumption. The practical consequence is that placement and timing become environmental decisions: flexible batch work and model training can be scheduled into regions and hours when the grid is cleanest, without changing the work itself.",
           command="Explain"),
        EQ("Discuss the environmental impact of big data and machine learning, and evaluate what organisations can realistically do to reduce it.", 8,
           [MP("Energy use of servers and cooling is addressed", ["electricity", "power", "cooling", "servers", "idle"]),
            MP("A measure such as PUE is named and used", ["PUE", "power usage effectiveness", "1.1", "overhead"]),
            MP("Storage's continuous cost is addressed", ["storage", "continuous", "kept", "never read", "retention"]),
            MP("Training and inference are distinguished", ["training", "inference", "queries", "retrain", "GPU"]),
            MP("Water, materials or e-waste are addressed", ["water", "e-waste", "rare earth", "mining", "hardware", "recycl"]),
            MP("Realistic mitigations are proposed", ["virtualis", "elastic", "renewable", "carbon aware", "efficient", "delete", "smaller model", "pretrained"]),
            MP("The rebound effect or a limitation is acknowledged", ["rebound", "offset", "still rising", "demand grows", "however", "not enough"]),
            MP("A clear evaluative judgement", ["most effective", "biggest", "therefore", "on balance", "realistically"])],
           "The impact is larger and broader than the electricity bill suggests. Servers draw power continuously and an idle machine still consumes a substantial share of its peak, while cooling adds an overhead measured by power usage effectiveness: a facility at a PUE of 1.8 spends eighty per cent as much again on cooling and losses as it does on computing, where the best modern designs run near 1.1. Storage is the cost organisations most often overlook, because data kept for years draws power every second whether or not a single query ever reads it, which makes a neglected data lake a continuing environmental liability as well as a compliance one. In machine learning the headline figure is training, which can occupy thousands of accelerators for weeks and is repeated at every retrain, but for any widely used model the cumulative energy of inference across billions of individual queries exceeds it. Beyond energy there is water, since evaporative cooling consumes fresh water in regions that may be water stressed, and materials, since a three to five year hardware cycle depends on mined metals and produces a continuous stream of e-waste of which only a minority is formally recycled. What organisations can realistically do divides into the effective and the cosmetic. The genuinely effective measures are consolidating workloads through virtualisation so fewer machines idle, using elastic capacity that is released when a job finishes rather than running overnight, scheduling flexible batch work and training into regions and hours when the grid is cleanest, enforcing retention policies so unused data is deleted and cold data moved to lower-power storage, writing queries that scan partitions and columns rather than whole tables, and reusing or fine-tuning a pretrained model instead of training from scratch. Procuring renewable supply matters, though matching it hour by hour is far stronger than an annual accounting claim, and extending hardware life with repair and certified recycling addresses the materials side that energy measures ignore. The limitation has to be stated honestly: efficiency alone has not reduced total consumption, because data centre efficiency has improved markedly while total data centre energy use has continued to rise, as cheaper computing simply gets used more. Judged overall, the measures with the largest certain effect are the unglamorous ones, deleting data that serves no purpose, not running what does not need to run, and sizing models and queries to the question, because they reduce the work itself rather than making the same growing workload marginally cheaper to perform.",
           command="Discuss"),
    ],
)

# ================================================================== COURSE

COURSE = Course(
    slug="data-analytics",
    seo="OCR Data Analytics F200 F201 F202",
    title="Data Analytics",
    short="Data Analytics",
    stage="KS5",
    board="OCR",
    code="H019/H119",
    goal="Distinction star",
    icon="i-chart",
    accent="var(--teal)",
    blurb="OCR Cambridge Advanced National in IT: Data Analytics. Both exam units covered topic area by topic area, F200 Fundamentals of data analytics and F201 Big data and machine learning, plus the mandatory coursework unit F202 Spreadsheet data modelling, with quizzes, graphs, interactive models, exam-style questions and a guide to the set assignment.",
    intro="",
    units=[
        Unit("f200", "F200: Fundamentals of Data Analytics",
             "Externally assessed: 1 hour 15 minutes, 60 marks, 75 guided learning hours. Understanding data, managing data, platforms and access, the law, and the roles.",
             [D_UNDERSTANDING, D_MANAGING, D_PLATFORMS, D_LEGAL, D_ROLES],
             icon="i-database", term="Exam unit"),
        Unit("f201", "F201: Big Data and Machine Learning",
             "Externally assessed: 1 hour 30 minutes, 60 marks, 70 guided learning hours. The scope of big data, its infrastructure, machine learning and AI, ethics, and the environment.",
             [B_SCOPE, B_INFRA, B_ML, B_ETHICS, B_ENV],
             icon="i-brain", term="Exam unit"),
        Unit("f202", "F202: Spreadsheet Data Modelling",
             "Coursework, 75 guided learning hours: an OCR-set assignment, marked by your teacher and moderated by OCR. The principles of modelling, planning, creating, testing and delivering, evaluating, and a guide to the assignment itself.",
             F202_TOPICS, icon="i-table", term="Coursework"),
    ],
)
