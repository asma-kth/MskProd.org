"""Original practice papers for the OCR Data Analytics examined units.

Three for F200 and three for F201. Each is written to the shape of the real
assessment, 60 marks sampled across all five topic areas of its unit, with the
command words and mark tariffs the papers use and a resource figure on the
questions that need one. They are not past papers: OCR's are their copyright.

F200 allows 1 hour 15 minutes for 60 marks and F201 1 hour 30 minutes for the
same, which is roughly a mark a minute with reading time, and the papers here
are timed on the same basis.
"""
from mskbuild.models import EQ, MP, Paper

ACC = "var(--teal)"


# ============================================================== F200 PAPER A

F200_A = Paper(
    slug="f200-paper-a",
    title="Data Analytics F200 Paper A: Fundamentals of Data Analytics",
    course="Data Analytics",
    board="OCR",
    code="F200 style",
    minutes=75,
    marks=0,
    accent=ACC,
    blurb="A full length original paper sampling all five topic areas of F200: understanding data, managing data, platforms and access, the law, and the roles. Built around a veterinary group merging its practices onto one system.",
    calculator="A calculator may be used.",
    questions=[
        EQ("State what is meant by **information**, and how it differs from data.", 3, [
            MP("Data is raw facts or figures with no context", ["raw", "no context", "facts", "figures", "on its own"]),
            MP("Information is data given context, structure or meaning", ["context", "meaning", "structure", "labels", "units"]),
            MP("A valid example showing the difference", ["example", "37", "15", "temperature", "becomes", "for instance"]),
        ], "Data is raw facts or figures carrying no context, so the value 14.2 on its own means nothing at all. Information is that data given context and structure so that it means something: 'patient 4412 weighed 14.2 kg on 3 March' identifies the subject, the unit and the time, and can now be acted on.",
           command="State"),

        EQ("Give **two** examples of unstructured data a veterinary practice would hold.", 2, [
            MP("One valid example of unstructured data", ["photograph", "x-ray", "image", "scan", "free text", "notes", "email", "voicemail", "video"]),
            MP("A second, different valid example", ["email", "notes", "image", "scan", "recording", "letter", "document"]),
        ], "X-ray and scan images, and the free text clinical notes typed by a vet during a consultation.",
           command="Give"),

        EQ("The practice has merged the membership files of its three sites.\n\nIdentify **four** data quality problems visible in the extract.", 4, [
            MP("Duplicate records for the same person", ["duplicate", "same person", "twice", "rows 1 and 2", "repeated"]),
            MP("Inconsistent date formats", ["date", "format", "dd/mm", "2025-08-07", "11/9/25", "inconsistent"]),
            MP("Missing values", ["missing", "blank", "empty", "no email", "no name", "not supplied"]),
            MP("Inconsistent capitalisation, or an implausible value", ["capital", "lower case", "case", "4500", "postcode", "spaces", "implausible", "outlier", "invalid email"]),
        ], "Rows 1 and 2 are the same member entered twice, differing only in capitalisation, so an exact string match would not detect the duplicate. The joined dates appear in at least three formats, 07/08/2025, 2025-08-07 and 11/9/25, and the third is ambiguous about which number is the month. Several fields are empty: row 3 has no fee, row 4 no email, row 5 no name, and row 5's email field contains the words 'not supplied' rather than being properly null. Finally there are invalid values: a fee of 4500.00 where every other row is 45.00, a postcode written with spaces between every character, and an email address with no domain.",
           command="Identify",
           figure="!diagram exam-extract-members"),

        EQ("Explain **two** automated checks that would have prevented some of these problems at the point of entry.", 4, [
            MP("A format or pattern check on a field", ["format check", "pattern", "regular expression", "mask", "postcode", "email format"]),
            MP("Why it would have prevented the problem", ["reject", "would not accept", "forced", "at entry", "before it is stored"]),
            MP("A range, presence or lookup check", ["range check", "presence check", "lookup", "required field", "list", "type check"]),
            MP("Why it would have prevented the problem", ["blank", "4500", "outside", "cannot be left", "must be chosen"]),
        ], "A format check on the email and postcode fields, applied as the form is submitted, would have rejected 's.mihai@ex' for having no domain and 'N E 3 2 R L' for not matching the pattern of a UK postcode, so neither could ever have reached the file. A range check on the fee field, set to the band the practice actually charges, would have refused 4500.00 and prompted the operator to correct it, and a presence check on name and email would have made those fields impossible to leave blank, which also removes the need for somebody to type 'not supplied' into a field meant to hold an address.",
           command="Explain"),

        EQ("The diagram shows the practice's analytics pipeline with two stages missing.\n\nName stage 3 and stage 6, and state what each one produces.", 4, [
            MP("Stage 3 is cleaning or preparing the data", ["clean", "prepare", "preparation", "wrangl"]),
            MP("It produces data that is typed, complete, consistent and deduplicated", ["typed", "consistent", "deduplicat", "usable", "accurate", "fit to analyse"]),
            MP("Stage 6 is visualising or communicating", ["visualis", "visualiz", "communicat", "present", "report"]),
            MP("It produces a chart and a conclusion somebody can act on", ["chart", "dashboard", "report", "conclusion", "one sentence", "act on"]),
        ], "Stage 3 is cleaning and preparing, which produces data that is correctly typed, complete, internally consistent and free of duplicates, so that it can be analysed without the result depending on an accident of entry. Stage 6 is visualising and communicating, which produces a chart and a conclusion a decision maker can act on, since an analysis that stays inside the analyst's notebook changes nothing.",
           command="Name",
           figure="!diagram exam-pipeline-gaps"),

        EQ("Describe the difference between a data warehouse and a data lake.", 4, [
            MP("A warehouse holds structured, modelled data", ["structured", "modelled", "schema", "tables", "clean"]),
            MP("Its schema is enforced when data is written", ["on write", "when written", "rejected", "must fit"]),
            MP("A lake holds raw data of any structure", ["raw", "any structure", "unstructured", "as it arrived"]),
            MP("Its schema is applied when the data is read", ["on read", "when read", "later", "nothing is rejected"]),
        ], "A data warehouse holds structured, modelled data that has already been cleaned and shaped, and it enforces its schema when data is written, so anything that does not fit is rejected and everything inside it is consistent and queryable. A data lake holds data in whatever form it arrived in, structured or not, and applies a schema only when the data is read, so nothing is ever rejected and nothing is guaranteed either. The warehouse answers the questions you already knew you would ask; the lake keeps the material for the questions you have not thought of yet.",
           command="Describe"),

        EQ("The practice's booking system is read through an API by a reporting tool.\n\nExplain what has gone wrong in the way the reporting tool is using this API.", 6, [
            MP("429 means the rate limit has been exceeded", ["429", "rate limit", "too many requests"]),
            MP("The correct response is to wait and retry", ["wait", "retry", "back off", "Retry-After", "60 seconds"]),
            MP("The second response returns only 100 of the records requested", ["100", "not 500", "fewer", "only part"]),
            MP("Because the response is paged", ["page", "paging", "pagination", "next"]),
            MP("The client stops after the first page, so data is silently lost", ["stops", "first page", "ignores", "silently", "missing", "incomplete"]),
            MP("It should follow the next link until there are no more pages", ["follow", "next link", "loop", "until", "repeat"]),
        ], "Two faults are visible. The first call returns 429 Too Many Requests, which means the tool has exceeded the endpoint's rate limit; the correct behaviour is to pause for the period given in the Retry-After header, here 60 seconds, and try again, rather than hammering the endpoint or treating the call as failed. The second fault is more serious because it is silent. The request asked for a limit of 500, but the response contains 100 items and a 'next' field pointing at page 2, which means the API has paged the result. The note says the client reads the orders array and stops, so it is processing the first hundred records and discarding the rest without any error being raised. Every report built on it is quietly incomplete. The tool must loop, following the next link and appending each page until no next link is returned.",
           command="Explain",
           figure="!diagram exam-api-exchange"),

        EQ("State **three** of the data protection principles.", 3, [
            MP("One valid principle", ["lawful", "fair", "transparen", "purpose limitation", "minimis", "accura", "storage limitation", "integrity", "confidential", "accountab"]),
            MP("A second, different principle", ["purpose", "minimis", "accura", "storage", "security", "accountab", "lawful"]),
            MP("A third, different principle", ["accountab", "storage", "integrity", "accura", "minimis", "purpose"]),
        ], "Purpose limitation, data minimisation, and storage limitation.",
           command="State"),

        EQ("The practice stores its records with a cloud provider.\n\nExplain why the practice is the data controller and the provider is the data processor.", 4, [
            MP("The controller decides why and how data is processed", ["decides", "why", "purpose", "means", "determines"]),
            MP("The practice makes those decisions here", ["the practice", "it decides", "chooses", "its own records"]),
            MP("The processor acts only on the controller's instructions", ["instructions", "on behalf", "only what", "does not decide"]),
            MP("Accountability stays with the controller", ["accountable", "remains", "still responsible", "does not transfer", "contract"]),
        ], "The controller is whoever decides why personal data is processed and how, and here that is the practice: it decides to keep client and animal records, what to record and for how long. The provider only stores and serves that data on the practice's instructions and has no say in the purpose, which makes it the processor. The distinction matters because accountability does not move with the data: the practice still needs a lawful basis, still has to answer subject access requests and is still answerable to the ICO for the security of the processing, so it must have a written contract obliging the provider to apply appropriate security, use no further sub-processors without permission and report any breach to it promptly.",
           command="Explain"),

        EQ("The table shows the current access permissions at the practice.\n\nIdentify **three** problems with these permissions and state how each should be fixed.", 6, [
            MP("A former employee still has an active account", ["former", "ex-employee", "left", "still active", "leaver"]),
            MP("The account should be disabled as part of a leaver process", ["disable", "revoke", "remove", "offboard", "leaver process"]),
            MP("Roles have access they do not need, breaching least privilege", ["least privilege", "do not need", "too much", "payroll", "intern", "export all"]),
            MP("Permissions should be cut to what the role requires", ["minimum", "only what", "restrict", "remove", "role based"]),
            MP("Almost every role can export all data or delete records", ["export", "delete", "everyone", "every role", "all data"]),
            MP("Those rights should be separated and logged or approved", ["separate", "approval", "log", "audit", "two people", "restrict to"]),
        ], "First, a former employee's account is still active with full rights, which means somebody no longer employed can read and delete everything; the fix is a leaver process that disables the account on the last working day, with a scheduled review to catch any that are missed. Second, least privilege is not being applied: a marketing assistant and a temporary intern can export all data, and a developer and analyst can read payroll, none of which their work requires; each role's permissions should be cut back to the minimum the job needs and granted through the role rather than to the individual. Third, almost every role can delete records and export the entire dataset, so one compromised account could remove or exfiltrate the practice's data; export and deletion should be separated from ordinary access, restricted to named roles, require approval, and be written to an audit log that somebody actually reviews.",
           command="Identify",
           figure="!diagram exam-access-matrix"),

        EQ("Describe the responsibilities of a **data engineer** and a **data analyst**.", 4, [
            MP("The engineer builds and maintains the pipelines", ["pipeline", "build", "ingest", "ETL", "infrastructure", "moves data"]),
            MP("So that data arrives reliably, on time and in a usable form", ["reliable", "on time", "available", "usable", "trustworthy"]),
            MP("The analyst answers business questions from that data", ["questions", "analys", "report", "insight", "queries"]),
            MP("Through querying, analysis, visualisation and communication", ["SQL", "query", "visualis", "report", "communicat", "dashboard"]),
        ], "A data engineer is responsible for building and maintaining the pipelines that extract data from the source systems, transform it and load it somewhere it can be queried, so that the data arrives reliably, on schedule and in a usable shape. A data analyst is responsible for answering the practice's questions from that data, which means querying it, analysing it, choosing how to present it and explaining the result to the people who will act on it. The engineer makes the data trustworthy; the analyst makes it useful.",
           command="Describe"),

        EQ("The chart shows the practice's online bookings over a year.\n\nDescribe what the chart shows, and explain **one** caution you would give before acting on it.", 6, [
            MP("Identifies the overall pattern", ["rises", "peak", "seasonal", "varies", "higher in"]),
            MP("Quotes specific figures from the chart", ["418", "142", "302", "December", "January", "thousand"]),
            MP("Identifies December as the maximum and January as the minimum", ["December", "highest", "January", "lowest", "minimum", "maximum"]),
            MP("A valid caution about the data", ["one year", "single year", "no comparison", "does not say why", "correlation", "cause", "what changed", "promotion"]),
            MP("The caution is explained", ["because", "cannot tell", "may be", "would need", "another year"]),
            MP("A sensible next step", ["compare", "previous year", "investigate", "ask", "segment", "check"]),
        ], "Bookings move seasonally within a broad range. They climb through spring and summer from 182 thousand in April to a summer peak of 302 thousand in August, fall back in the autumn, then spike sharply to 418 thousand in December, which is by some distance the highest month. January is the lowest at 142 thousand, less than a third of the December figure, and the following two months recover only slowly. The caution is that this is a single year with nothing to compare it against, so it is impossible to tell whether the December spike is the normal seasonal pattern or a one-off caused by something specific such as a promotion, a competitor closing or a change to the booking system. The chart also says nothing about why any of it happened. Before acting I would put at least two further years alongside it and check what the practice actually did in December, because a plan built on a pattern that occurred once is a plan built on an accident.",
           command="Describe",
           figure="!diagram exam-chart-monthly"),

        EQ("The veterinary group is merging three practices onto one system and wants to use the combined data to plan staffing and stock.\n\nDiscuss how the group should prepare, store and govern this data, and explain the risks of getting it wrong.", 10, [
            MP("Profiling and reconciliation before anything is changed", ["profile", "examine", "count", "reconcile", "baseline", "before"]),
            MP("Cleaning decisions: duplicates, formats, missing values", ["duplicate", "format", "missing", "standardise", "merge", "deduplicate"]),
            MP("Agreed definitions across the three practices", ["definition", "same thing", "what counts as", "consistent", "data dictionary"]),
            MP("A suitable store, with a reason", ["warehouse", "database", "lake", "cloud", "because", "queries", "structured"]),
            MP("Access control and security", ["access", "role", "least privilege", "encryption", "audit", "permission"]),
            MP("Legal obligations, named", ["Data Protection Act", "UK GDPR", "lawful basis", "purpose", "retention", "ICO"]),
            MP("Governance: ownership, documentation, lineage", ["owner", "data dictionary", "documentation", "lineage", "quality", "responsible"]),
            MP("A risk of poor preparation is explained", ["wrong", "double count", "staffing", "stock", "decision", "misleading", "overstat"]),
            MP("A risk relating to the law or to trust is explained", ["breach", "fine", "ICO", "clients", "trust", "confidential", "records"]),
            MP("A judgement about what matters most and why", ["most important", "first", "overall", "therefore", "greatest risk"]),
        ], "The first task is to understand the three datasets before changing any of them: row counts per practice, the distinct values in each field, the formats dates and postcodes arrive in, and the volume of blanks. That produces a baseline the merged file can be reconciled against, which is the only way to prove afterwards that nothing was lost. Cleaning then has to be a set of recorded decisions rather than a button. Duplicates need a defined matching key, probably surname plus postcode plus animal, with a sample of proposed matches reviewed before anything is merged; dates need standardising to one format; and missing values have to be kept and flagged rather than deleted, because if the blanks come disproportionately from one practice then dropping those rows quietly removes that practice from every result. Underneath the technical work sits the harder problem, which is definitional: if one site counts a consultation when it is booked and another when it is paid for, the merged figures are wrong in a way no cleaning will reveal, so the group needs agreed written definitions before it merges anything. For storage, a single relational database or small warehouse is the right shape here, because the data is structured, the questions, appointments per day per site and stock used per procedure, are known in advance, and a modelled store gives consistent answers to everyone. Access must be role based and on least privilege, with clinical records restricted to clinical staff, data encrypted at rest and in transit, and access logged, since this data includes client contact details and payment history. The group is the controller under the Data Protection Act 2018 and the UK GDPR, so it needs a lawful basis, a privacy notice that reflects the merged use, a retention schedule and a process for subject access requests, and it must not quietly repurpose clinical data for marketing. Governance means a named owner for the combined dataset, a data dictionary defining every field, recorded lineage so any figure can be traced back, and a regular quality check. Getting it wrong has two kinds of consequence. The operational one is that staffing and stock decisions are made from numbers that are wrong: duplicates inflate demand, so the group hires for patients who do not exist and orders stock it does not need. The legal and reputational one is more serious, because a merge is exactly when records get exposed to people who should not see them, and a breach of client and clinical data would have to be reported to the ICO and would damage the trust the practice depends on. Of everything above, the agreed definitions matter most, because a cleaning error is visible and fixable while a definitional mismatch produces confident, precise figures that are simply untrue.",
           command="Discuss"),
    ],
)


# ============================================================== F200 PAPER B

F200_B = Paper(
    slug="f200-paper-b",
    title="Data Analytics F200 Paper B: Fundamentals of Data Analytics",
    course="Data Analytics",
    board="OCR",
    code="F200 style",
    minutes=75,
    marks=0,
    accent=ACC,
    blurb="A second full length F200 paper, built around a city council bringing together data from its waste, housing and leisure services to plan where to invest.",
    calculator="A calculator may be used.",
    questions=[
        EQ("State the difference between **quantitative** and **qualitative** data, giving one example of each.", 3, [
            MP("Quantitative is numerical and can be calculated with", ["numerical", "numbers", "counts", "measure", "calculate"]),
            MP("Qualitative is descriptive: words, categories or opinions", ["words", "opinions", "descriptive", "categories", "reasons"]),
            MP("A valid example of each", ["example", "number of", "how many", "comments", "interview", "rating"]),
        ], "Quantitative data is numerical and can be calculated with, such as the number of missed bin collections per week. Qualitative data is descriptive rather than numerical, such as residents' written comments explaining why they were dissatisfied with the service.",
           command="State"),

        EQ("Identify **two** sources of secondary data the council could use.", 2, [
            MP("One valid secondary source", ["census", "ONS", "open data", "published", "report", "government", "other council", "ofcom"]),
            MP("A second, different valid source", ["weather", "transport", "health", "published", "statistics", "survey results", "index of deprivation"]),
        ], "Census and Office for National Statistics population data, and published government open data such as the index of multiple deprivation.",
           command="Identify"),

        EQ("The extract comes from the council's leisure centre bookings export.\n\nIdentify **four** data quality problems in it.", 4, [
            MP("A duplicate row", ["duplicate", "twice", "repeated", "A1001", "same order"]),
            MP("Inconsistent country values", ["UK", "U.K.", "GB", "country", "inconsistent", "same category"]),
            MP("Inconsistent formats in totals or dates", ["currency", "symbol", "space", "format", "date", "03/01", "ambiguous"]),
            MP("A missing value or an implausible value", ["missing", "blank", "customer", "0.00", "zero", "empty"]),
        ], "A1001 appears twice, identically, so any total will double count it. The country column holds one real category written five ways: UK, U.K., United Kingdom, GB and uk, which would split every grouping five ways. The totals are formatted inconsistently, some with a currency symbol, one without and one with a space after it, so a naive import will read them as text rather than numbers; the dates are similarly inconsistent, and 03/01/2026 is ambiguous about whether it is January or March. Finally there are suspect values: a total of 0.00 on a completed order and a blank customer reference on A1004.",
           command="Identify",
           figure="!diagram exam-extract-orders"),

        EQ("Explain how the duplicate should be handled, and why deleting every row with a blank field would be the wrong approach.", 4, [
            MP("Define a matching key before deduplicating", ["key", "match", "define", "which fields", "identify"]),
            MP("Keep one record, merging the better values", ["keep", "merge", "one record", "most complete", "most recent"]),
            MP("Deleting blanks removes rows that may share a cause", ["cause", "one source", "systematic", "not random", "same system"]),
            MP("Which biases the result rather than cleaning it", ["bias", "skew", "misleading", "removes a group", "unrepresentative"]),
        ], "Deduplication needs a definition before it needs code: the council should decide what makes two rows the same, here the order reference together with the date and total, review a sample of the proposed matches, then keep one record, merging in the most complete value for each field and preserving both source identifiers. Deleting every row with a blank field is the wrong approach because missing values are rarely random. If the blank customer references all come from one leisure centre whose till does not capture them, deleting those rows removes that centre from the analysis entirely, and the resulting report says that site is quiet when in fact it was excluded. Blanks should be kept and explicitly flagged as unknown, and the pattern of where they occur investigated, because that pattern is often itself the finding.",
           command="Explain"),

        EQ("The council wants a single count of active customers across its two systems.\n\nExplain why simply joining these tables would produce a wrong figure.", 6, [
            MP("The identifiers are formatted differently", ["204", "C-204", "prefix", "format", "identifier", "will not match"]),
            MP("So a direct join matches nothing, or matches wrongly", ["no match", "fails", "zero", "wrong", "will not join"]),
            MP("Each system holds customers the other does not", ["455", "C-902", "only in", "missing", "not present"]),
            MP("'Active' is defined differently in the two systems", ["definition", "active", "different", "12 months", "closed"]),
            MP("So the same customer can be active in one and not the other", ["Olawale", "lapsed", "TRUE", "disagree", "both", "contradict"]),
            MP("The definitions must be agreed before any join", ["agree", "define", "decide", "which definition", "data dictionary"]),
        ], "Three things break it. The identifiers do not match: sales holds 204 while support holds C-204, so a direct join on those columns returns nothing at all, and the keys have to be normalised before anything else happens. The two tables also contain different people: Mihai, 455, appears only in sales and Hargreaves, C-902, only in support, so the answer depends on whether the council wants customers in both systems, in either, or in one specific system, and that is a decision somebody has to make rather than a technical detail. The most dangerous problem is the definitional one. Sales treats a customer as active if they have ordered in the last twelve months, while support treats them as active unless their account has been closed, so Olawale is lapsed in one system and TRUE in the other without either being wrong. Joining them produces a precise number that answers no question. The council has to agree a single written definition of 'active', apply it to both sources, and record it in a data dictionary before counting anything.",
           command="Explain",
           figure="!diagram exam-two-tables"),

        EQ("Describe **four** dimensions of data quality.", 4, [
            MP("Accuracy: does it match reality", ["accuracy", "correct", "matches reality", "true"]),
            MP("Completeness: is anything missing", ["complete", "missing", "gaps", "all present"]),
            MP("Consistency: do sources agree", ["consistent", "agree", "same", "contradict"]),
            MP("Timeliness, validity or uniqueness, described", ["timeliness", "up to date", "current", "valid", "format", "unique", "duplicate", "relevance"]),
        ], "Accuracy is whether a value matches reality, so a recorded address is accurate if the resident actually lives there. Completeness is whether anything that should be present is missing, such as records with no postcode. Consistency is whether two systems holding the same fact agree with each other. Timeliness is whether the data is current enough for the decision being made, since a six month old occupancy figure cannot support a decision about next week.",
           command="Describe"),

        EQ("Explain the difference between **ETL** and **ELT**.", 4, [
            MP("ETL transforms the data before loading it", ["transform", "before", "on the way in", "then load"]),
            MP("So only modelled data reaches the store", ["only", "modelled", "clean", "nothing raw"]),
            MP("ELT loads the raw data first and transforms it in place", ["load first", "raw", "in the warehouse", "afterwards"]),
            MP("So the raw data stays available to be reprocessed", ["reprocess", "rerun", "keep the raw", "redo", "available"]),
        ], "In ETL the data is extracted, transformed to clean and reshape it, and only then loaded, so nothing but modelled data ever reaches the warehouse and storage stays small. The cost is that any field discarded on the way in has to be fetched again from the source if it later turns out to be needed. In ELT the data is extracted, loaded raw, and transformed inside the warehouse using its own compute, so the original remains available and a transformation can simply be rerun when a definition changes. That costs more storage and processing, which is why cheap cloud storage is the reason ELT has become the common choice.",
           command="Explain"),

        EQ("The chart shows the mean response time of two servers hosting the council's website.\n\nDescribe what the chart shows and suggest what should be investigated next.", 6, [
            MP("Describes server B as broadly flat", ["B", "flat", "stable", "steady", "little change"]),
            MP("Quotes figures for server B", ["40", "52", "around 50", "ms"]),
            MP("Describes server A as rising sharply", ["A", "rises", "increases", "climbs", "worse"]),
            MP("Quotes figures for server A", ["42", "168", "four times", "168 ms"]),
            MP("Identifies when the divergence begins", ["from 12", "midday", "hour 12", "halfway", "after"]),
            MP("A sensible next step", ["investigate", "load", "memory", "leak", "restart", "logs", "same traffic", "compare", "monitor"]),
        ], "Both servers start the day at about the same point, around 40 to 42 milliseconds, and server B stays there: it drifts gently from 40 to 52 milliseconds over the twelve hours, which is effectively flat. Server A tracks it until about midday and then diverges sharply, climbing from roughly 52 milliseconds to 168 by the end of the period, four times its morning figure and more than three times server B at the same moment. Since both serve the same site, the cause is specific to server A rather than to demand. The next step is to check whether the two are genuinely receiving the same share of traffic, and then to look at server A's own resources over the same hours, because a steady rise through the day that does not recover is the signature of something accumulating, such as a memory leak, an unreleased connection pool or a log file filling the disk. Restarting it and watching whether the curve starts again from 40 would confirm that quickly.",
           command="Describe",
           figure="!diagram exam-chart-response"),

        EQ("State **three** rights an individual has over their personal data.", 3, [
            MP("One valid right", ["access", "rectification", "erasure", "restriction", "portability", "object", "automated"]),
            MP("A second, different right", ["erasure", "rectification", "portability", "object", "access", "restriction"]),
            MP("A third, different right", ["object", "portability", "restriction", "automated", "erasure", "access"]),
        ], "The right of access, the right to rectification, and the right to erasure.",
           command="State"),

        EQ("Explain what a **Data Protection Impact Assessment** is and when one must be carried out.", 4, [
            MP("A documented assessment of the risk to individuals", ["assessment", "risk", "individuals", "document", "evaluate"]),
            MP("Carried out before the processing begins", ["before", "in advance", "at the start", "prior"]),
            MP("Required where processing is likely to be high risk", ["high risk", "likely", "significant", "required"]),
            MP("An example of such processing", ["large scale", "special category", "children", "vulnerable", "profiling", "automated", "combining", "monitoring"]),
        ], "A Data Protection Impact Assessment is a documented exercise that identifies what personal data a proposed activity will process, why, what could go wrong for the people in it, and what will be done to reduce that risk. It has to be carried out before the processing starts, not written up afterwards, because its purpose is to change the design. One is legally required wherever processing is likely to result in a high risk to individuals, which includes large scale processing of special category data, systematic monitoring of a public area, profiling with significant effects, and combining datasets collected for different purposes, all of which a council joining service records would be doing.",
           command="Explain"),

        EQ("Explain the difference between **authentication** and **authorisation**.", 4, [
            MP("Authentication establishes identity", ["who", "identity", "prove", "credentials"]),
            MP("An example of authentication", ["password", "MFA", "passkey", "token", "certificate", "biometric"]),
            MP("Authorisation decides what is permitted", ["permitted", "allowed", "what they can do", "rights"]),
            MP("An example, or why the distinction matters", ["role", "read only", "cannot delete", "401", "403", "least privilege"]),
        ], "Authentication establishes who somebody is, using something they know, have or are, such as a password with a second factor or a certificate. Authorisation then decides what that identity is allowed to do, usually through a role, so an officer in waste services can read waste records but not housing ones and cannot delete anything. The two fail differently and have to be fixed differently: an HTTP 401 means the system does not recognise you at all, while a 403 means it recognises you perfectly well and is refusing anyway.",
           command="Explain"),

        EQ("A committee of councillors, none of whom work in IT, will decide whether to fund the project.\n\nDescribe how the analyst should present the findings to them.", 6, [
            MP("Lead with the conclusion, not the method", ["conclusion first", "lead with", "headline", "answer first"]),
            MP("Use the committee's own units", ["pounds", "residents", "weeks", "their terms", "plain", "no jargon"]),
            MP("One chart carrying one message", ["one chart", "single", "simple", "clear", "no clutter"]),
            MP("State uncertainty honestly and in words", ["uncertain", "between", "roughly", "caveat", "limitation", "not precise"]),
            MP("Make a specific recommendation", ["recommend", "should", "next step", "decision"]),
            MP("Keep the method available but not in the way", ["appendix", "available", "on request", "technical note", "not in the presentation"]),
        ], "The analyst should open with the conclusion rather than the method, because the committee is deciding, not reviewing: one sentence saying what the data shows and what it implies for the decision. Everything after that should be in the committee's own units, residents affected, weeks of delay and pounds, rather than percentages of a sample or statistical terms. There should be one chart, carrying one message, large enough to read from the back of the room; if a chart needs a paragraph to interpret, it is the wrong chart. Uncertainty should be stated in plain words rather than hidden or faked, 'somewhere between four and seven thousand households' rather than '5,412', because a figure that implies precision the data cannot support destroys trust the moment somebody tests it. The presentation should end with a specific recommendation and what it would cost, since an analysis that recommends nothing leaves the committee exactly where it started. The method, the sources and the assumptions belong in a written appendix, available to anyone who asks and in front of nobody who does not.",
           command="Describe",
           figure=""),

        EQ("The council wants to join its waste, housing and leisure data to identify households that may need support.\n\nDiscuss the legal and ethical issues this raises, and what safeguards the council should put in place.", 10, [
            MP("A lawful basis is identified", ["public task", "lawful basis", "legal obligation", "statutory", "consent"]),
            MP("Purpose limitation across the three sources is addressed", ["purpose", "collected for", "different purpose", "combining", "compatible"]),
            MP("Data minimisation is applied", ["minimis", "only what", "necessary", "fewer fields", "proportionate"]),
            MP("Sensitive or inferred data is recognised", ["special category", "infer", "health", "financial", "vulnerable", "sensitive"]),
            MP("A DPIA is named as required", ["DPIA", "impact assessment"]),
            MP("Transparency with residents", ["privacy notice", "told", "aware", "transparen", "publish"]),
            MP("An ethical concern beyond legality", ["surpris", "trust", "stigma", "surveillance", "chilling", "wrongly", "false positive"]),
            MP("Technical safeguards proposed", ["access control", "least privilege", "pseudonym", "encrypt", "audit", "retention"]),
            MP("Human involvement rather than automated action", ["human", "not automated", "review", "officer decides", "in the loop"]),
            MP("A judgement about whether and how to proceed", ["should proceed", "only if", "on balance", "recommend", "therefore"]),
        ], "A council is likely to have a lawful basis for this without consent, because supporting vulnerable residents falls within its public task, but a basis for each dataset separately is not automatically a basis for combining them. Waste, housing and leisure records were collected under different statutory functions, so purpose limitation requires the council to show that the new use is compatible with the original collection and to be able to point to the specific function it serves. Data minimisation then constrains the design: the instinct is to join everything available, but a model built on three or four indicators is both more lawful and more likely to work than one built on forty, and every extra field widens the exposure if the dataset leaks. The sensitivity of the result matters more than the sensitivity of the inputs. None of these sources is a health record, yet joined they infer health, disability, financial difficulty and household composition, and inference is processing, so the council would be handling special category data whether or not any field is labelled that way. Because this is large scale processing of sensitive inferences about vulnerable people, a Data Protection Impact Assessment is mandatory and must be completed before anything is built. Residents must also be told, in a published privacy notice written to be read rather than to be compliant, what is being combined and why, with a route to object. Beyond the law there is a question the law does not settle. Residents would be surprised to learn that their bin collections and their gym attendance had been joined to score their household, and that surprise matters for a council, which depends on people reporting difficulties honestly; a service that feels like surveillance gets told less. A false positive risks stigmatising a family and a false negative gives false assurance, and the people affected have the least power to challenge either. The safeguards follow from that. Analysts should work on pseudonymised extracts with the linking key held separately, and only the support team should see identified records, under role based access on least privilege with every access logged. The combined dataset needs a named owner, a documented retention period with automatic deletion, and a scheduled review of whether it is actually producing better outcomes rather than just more flags. Most importantly the output must prompt a human conversation rather than trigger an automated consequence, because a solely automated decision with a significant effect on someone engages their right to human involvement and an explanation. On balance the council can proceed, but only with the impact assessment completed first, the field list cut to the minimum that works, and a standing commitment that an officer, not a score, decides what happens to a household.",
           command="Discuss"),
    ],
)


# ============================================================== F200 PAPER C

F200_C = Paper(
    slug="f200-paper-c",
    title="Data Analytics F200 Paper C: Fundamentals of Data Analytics",
    course="Data Analytics",
    board="OCR",
    code="F200 style",
    minutes=75,
    marks=0,
    accent=ACC,
    blurb="A third full length F200 paper, set in a manufacturer running production line sensors alongside its order and maintenance systems.",
    calculator="A calculator may be used.",
    questions=[
        EQ("State what is meant by **metadata**, and give one example.", 2, [
            MP("Data about data: information describing the data itself", ["about data", "describes", "data about", "not the data itself"]),
            MP("A valid example", ["file size", "date created", "author", "schema", "column types", "resolution", "timestamp", "format"]),
        ], "Metadata is data about data: information describing a dataset rather than the content of it. The capture time, the sensor that produced a reading and the data type of a column are all metadata.",
           command="State"),

        EQ("Give **two** advantages of a columnar file format such as Parquet for analytics.", 2, [
            MP("A query reads only the columns it needs", ["only the columns", "one column", "does not read every field", "fewer columns"]),
            MP("Better compression, or faster aggregation over many rows", ["compress", "smaller", "faster", "aggregate", "millions of rows"]),
        ], "A query can read only the columns it actually uses rather than every field of every row, and storing like values together compresses far better, so the same analysis moves a fraction of the data.",
           command="Give"),

        EQ("The extract comes from the production line sensor log.\n\nIdentify **four** data quality problems in it.", 4, [
            MP("An impossible or sentinel value", ["-999", "minus 999", "impossible", "sentinel", "temperature"]),
            MP("A value outside a plausible range", ["410", "humidity", "out of range", "impossible", "over 100"]),
            MP("A duplicate reading", ["duplicate", "repeated", "same timestamp", "twice", "08:00:04"]),
            MP("Missing readings, a gap in the sequence, or inconsistent casing", ["missing", "blank", "offline", "gap", "08:00:05", "OK", "capital", "case"]),
        ], "The temperature of minus 999 for T-01 is a sentinel value standing in for a failed reading, not a measurement, and averaging it would wreck the result. The humidity of 410 per cent for T-03 is outside the possible range for the field and is likely a misplaced decimal point. T-02 appears twice at 08:00:04 with identical values, which is a duplicate that would double count. Beyond those, the status field holds both 'OK' and 'ok', which splits a two-value field into three; T-04 has blank readings with a status of offline; and the second 08:00:05 is missing from the sequence entirely, so a reading has been lost rather than recorded as absent.",
           command="Identify",
           figure="!diagram exam-extract-sensors"),

        EQ("Explain why an outlier should be investigated before it is removed.", 3, [
            MP("An outlier may be a genuine and important value", ["genuine", "real", "important", "not an error", "valid"]),
            MP("An example of such a case", ["fault", "fraud", "failure", "record", "best", "worst", "breakdown"]),
            MP("Removing it silently hides the finding", ["hides", "loses", "miss", "removes the finding", "exactly what"]),
        ], "An outlier is not the same thing as an error. A reading far from the rest may be a genuine measurement of something unusual, and in a sensor log on a production line that unusual thing is very often the fault the monitoring exists to catch: a bearing starting to fail, a blockage, a sudden temperature spike. Deleting outliers automatically therefore removes exactly the records the analysis was installed to find, and does so silently. The correct order is to investigate first, establish whether the value is impossible, implausible or merely rare, and only then decide whether to exclude it, recording the decision either way.",
           command="Explain"),

        EQ("Describe **two** methods of gathering primary data about how operators use the line monitoring software.", 4, [
            MP("One valid primary method named", ["observation", "interview", "survey", "questionnaire", "focus group", "user testing", "shadowing"]),
            MP("How it would be carried out here", ["watch", "ask", "record", "operators", "shift", "task"]),
            MP("A second, different method named", ["interview", "survey", "observation", "testing", "focus group"]),
            MP("How it would be carried out, or what it adds", ["why", "reasons", "numbers", "compare", "scale", "open questions"]),
        ], "Observation: sit with operators during a shift and record what they actually do with the software, where they hesitate, what they write down on paper instead and which screens they never open. This finds problems nobody would report, because people adapt to bad software and stop noticing. A structured questionnaire issued to every operator across all three shifts: closed questions so the answers can be counted and compared between shifts, with a small number of open questions to catch anything the designer did not think to ask. The observation explains why; the questionnaire establishes how widespread it is.",
           command="Describe"),

        EQ("Explain **two** reasons the manufacturer should read its maintenance data through an API rather than receiving a nightly CSV export.", 4, [
            MP("The data is live rather than a snapshot", ["live", "current", "up to date", "real time", "immediately"]),
            MP("Why that matters here", ["fault", "before", "react", "stale", "overnight", "too late"]),
            MP("Access can be scoped, logged and revoked", ["scoped", "key", "logged", "revoked", "controlled", "audit"]),
            MP("Or: only the records needed are transferred", ["only", "filter", "server side", "less data", "parameters"]),
        ], "An API returns the current state rather than a snapshot that is already stale by the time anyone reads it, which matters on a production line because a maintenance flag raised at 09:00 is useful at 09:05 and worthless the following morning. It also gives control that a file drop cannot: each consumer holds its own key, the requests are attributable and logged, access can be scoped to particular endpoints and revoked in one action, and the query can be filtered server side so only the records needed cross the network rather than the whole table every night.",
           command="Explain"),

        EQ("Describe the **three** levels at which two systems must agree for data to be exchanged successfully.", 6, [
            MP("Technical: the transport and format", ["technical", "transport", "protocol", "format", "HTTPS", "file type"]),
            MP("What failure looks like at that level", ["cannot read", "cannot open", "fails", "no connection"]),
            MP("Syntactic: the structure and field names", ["syntactic", "structure", "field names", "schema", "encoding", "order"]),
            MP("What failure looks like at that level", ["wrong column", "parses but", "fields land", "misaligned", "garbled"]),
            MP("Semantic: the meaning of the values", ["semantic", "meaning", "definition", "what counts as"]),
            MP("Why semantic failure is the dangerous one", ["no error", "silently", "numbers are wrong", "nothing fails", "looks fine"]),
        ], "Technically, the two systems must agree how the data physically moves and in what container: the protocol, the file format, the encoding. If they do not agree here the exchange simply fails, loudly, and somebody fixes it. Syntactically, they must agree the structure: the field names, their order, whether records nest, how dates are written. A failure here produces a file that parses but whose values land in the wrong places, which is usually visible on inspection. Semantically, they must agree what the values mean: whether 'completed' includes cancelled jobs, whether a maintenance hour counts the travel time, whether a shift is dated by its start or its end. This is the dangerous level, because nothing errors. The transfer succeeds, the import succeeds, the report runs, and the numbers are wrong in a way that only shows up when somebody notices two systems disagreeing months later.",
           command="Describe"),

        EQ("The scatter plot shows weekly sales of one product against its price over thirty weeks.\n\nDescribe the relationship shown, and comment on the point that sits apart from the rest.", 6, [
            MP("Identifies a negative relationship", ["negative", "inverse", "as price rises", "falls", "downward"]),
            MP("Quotes figures from the plot", ["150", "190", "20", "50", "units", "pounds"]),
            MP("Describes the strength as fairly strong, with a caveat", ["strong", "fairly", "clear", "band", "scatter", "not perfect"]),
            MP("Identifies the odd point correctly", ["one point", "outlier", "16", "176", "apart", "away from"]),
            MP("Offers a plausible explanation for it", ["promotion", "error", "stock", "competitor", "data entry", "special", "event", "mis-recorded"]),
            MP("Says what should be done before using the data", ["investigate", "check", "do not delete", "find out", "verify", "flag"]),
        ], "There is a clear negative relationship: weeks with a low price show high sales, around 150 to 190 units, and weeks with a high price show low sales, around 20 to 50, with the points forming a fairly tight band running from the upper left to the lower right. The relationship is strong enough to be useful but it is a band rather than a line, so price plainly does not explain everything about a given week. One point sits well away from that band, at a price near 16 pounds with sales of about 176 units, which is roughly what the product sells at its cheapest. That single week is worth more attention than the other twenty nine put together, because it is either an error or the most interesting thing in the dataset: a mis-keyed price, a week when the product was promoted or featured, a competitor out of stock, or a bulk order from one customer. It should be investigated rather than deleted, and if it turns out to be a genuine week the explanation for it may be more commercially valuable than the price relationship itself.",
           command="Describe",
           figure="!diagram exam-scatter-describe"),

        EQ("State **one** measure that protects data in transit and **one** that protects data at rest.", 2, [
            MP("In transit: TLS or encryption of the connection", ["TLS", "HTTPS", "SSL", "encrypt", "in transit", "VPN"]),
            MP("At rest: disk or file encryption", ["at rest", "disk encryption", "encrypted storage", "encrypt the file", "full disk"]),
        ], "In transit, TLS, so an intercepted request cannot be read. At rest, encryption of the stored volume or file, so a stolen disk or a copied backup is useless without the key.",
           command="State"),

        EQ("Explain the difference between **pseudonymisation** and **anonymisation**.", 4, [
            MP("Pseudonymisation replaces identifiers with a key", ["replace", "identifier", "key", "reference", "token", "ID"]),
            MP("It is reversible, so the data is still personal data", ["reversible", "can be linked back", "still personal data", "GDPR applies"]),
            MP("Anonymisation removes identifiability irreversibly", ["irreversib", "cannot be linked", "permanent", "no longer identifiable"]),
            MP("So it falls outside data protection law, and is hard to achieve", ["outside", "no longer applies", "hard", "difficult", "re-identif"]),
        ], "Pseudonymisation replaces direct identifiers with a reference, with the key linking them held separately. It reduces risk, but it is reversible by design, so the data remains personal data and the whole of the UK GDPR continues to apply to it. Anonymisation removes identifiability permanently, so the data is no longer personal data and the regime no longer applies. The catch is that genuine anonymisation is much harder than deleting the name column, because combinations of ordinary fields identify people: a date of birth, a postcode and a sex pick out most of the UK population, so real anonymisation means generalising, aggregating, suppressing small groups or adding noise, and accepting the loss of precision that comes with it.",
           command="Explain"),

        EQ("Identify **three** personal attributes a data analyst needs, and explain why each matters.", 6, [
            MP("Attention to detail", ["detail", "accurate", "careful", "notices", "checking"]),
            MP("Why it matters", ["one per cent", "small error", "wrong figure", "chase", "finding"]),
            MP("Communication", ["communicat", "explain", "present", "non-technical", "audience"]),
            MP("Why it matters", ["decision", "acted on", "understood", "useless if", "nobody understands"]),
            MP("Scepticism, curiosity or ethical judgement", ["scepti", "question", "curious", "why", "ethical", "challenge"]),
            MP("Why it matters", ["too convenient", "check", "wrong", "assumption", "should not", "bias"]),
        ], "Attention to detail, because the analyst who notices that a total is one per cent out and chases it is very often the one who finds the duplicate feed behind it, while the one who rounds it reports a wrong number with confidence. Communication, because every other skill produces a result that exists only inside a notebook: a correct analysis a manager does not understand changes nothing, and a clearly explained partial answer changes behaviour the same afternoon. Scepticism, because the result most likely to be wrong is the one everybody hoped for, and an analyst who checks hardest when the answer is convenient is the one whose figures survive being questioned in a meeting.",
           command="Identify"),

        EQ("Describe what a **data dictionary** contains and why one is needed.", 3, [
            MP("Every field, with its type and format", ["field", "column", "type", "format", "permitted values"]),
            MP("And its meaning or definition", ["meaning", "definition", "what it represents", "description"]),
            MP("So the dataset can be used correctly by somebody who did not build it", ["somebody else", "did not build", "understand", "consistent", "reuse", "avoid misuse"]),
        ], "A data dictionary lists every field in a dataset with its data type, its format, its permitted values or range, whether it can be null, and crucially what it actually means: not just that 'status' is a three character code but what each code represents and when it changes. It is needed because a dataset is unusable, and worse, misusable, by anybody who did not build it. Without one, two analysts quietly interpret the same column differently and produce two defensible answers to the same question.",
           command="Describe"),

        EQ("The time taken to repair a machine is recorded for every breakdown. Most repairs take between one and three hours, but a small number take more than two days.\n\nExplain which average the manufacturer should report, and why.", 4, [
            MP("Identifies the distribution as skewed", ["skew", "long tail", "not symmetrical", "few very large"]),
            MP("The mean is pulled by the long repairs", ["mean", "pulled", "dragged", "inflated", "higher", "affected by extremes"]),
            MP("The median is unaffected by them", ["median", "middle", "not affected", "unaffected", "ignores extremes"]),
            MP("Recommends the median, or reports both with a reason", ["median", "report both", "typical", "honest", "represent"]),
        ], "The distribution is right skewed: most repairs cluster between one and three hours with a long thin tail of multi-day jobs. The mean is calculated from every value, so those few very long repairs drag it well above what a typical repair actually takes, and quoting it would make the line look slower than it is on an ordinary day. The median is the middle value and is unaffected by how extreme the tail gets, so it describes the typical repair honestly. The manufacturer should report the median as the headline figure, and report the long repairs separately as what they are, a small number of serious events worth managing in their own right, rather than letting them distort the everyday number.",
           command="Explain"),

        EQ("The manufacturer wants to bring sensor, order and maintenance data together to reduce unplanned downtime.\n\nDiscuss how it should design this, covering how the data would be gathered, stored, prepared and governed.", 10, [
            MP("The question is defined before the data is collected", ["question", "decision", "what will change", "purpose", "start with"]),
            MP("Sensor data's volume and velocity are addressed", ["velocity", "volume", "per second", "stream", "rate", "huge"]),
            MP("Edge processing or aggregation is proposed", ["edge", "aggregate", "summar", "locally", "threshold", "only send"]),
            MP("A suitable store is chosen with a reason", ["time series", "warehouse", "lake", "object storage", "because", "cloud"]),
            MP("Joining the three sources requires shared keys and definitions", ["key", "join", "machine id", "definition", "timestamp", "align"]),
            MP("Data quality handling is described", ["sentinel", "-999", "outlier", "duplicate", "missing", "clean", "validate"]),
            MP("Governance: ownership, dictionary, lineage, retention", ["owner", "dictionary", "lineage", "retention", "documented", "quality"]),
            MP("Security or access control", ["access", "role", "least privilege", "encrypt", "audit"]),
            MP("How success would be measured", ["measure", "downtime", "before and after", "baseline", "monitor", "evaluate"]),
            MP("A judgement about the hardest part and why", ["hardest", "most difficult", "underestimated", "therefore", "overall"]),
        ], "The design should start from the decision rather than the data: the question is which machine to take off line and when, so the output has to be an alert with enough lead time for maintenance to act, and everything upstream is judged against that. Sensor data is the hard part of the collection. A line with hundreds of sensors sampling every second produces hundreds of millions of readings a day, which is a volume and velocity problem rather than a storage one, so processing should begin at the edge: a gateway on site applies threshold rules immediately, so an out of range vibration raises an alert within milliseconds and keeps working when the connection drops, and aggregates the rest into one minute summaries holding the mean, minimum, maximum and spread per sensor. Full resolution readings are buffered locally and uploaded only around an event, which is when per second detail is actually needed. For storage, the summaries belong in a time series database, which is built for timestamped measurements and compresses them far better than a relational table, with the raw event windows in object storage for later model training, while orders and maintenance records sit in the warehouse where they already are. Bringing the three together needs two things that are easy to overlook: a shared machine identifier used consistently by all three systems, and agreement on how timestamps are recorded, because a maintenance record dated by the day of the visit cannot be aligned to sensor data recorded in UTC to the second without an explicit rule. Preparation has to deal with what the sensor log actually contains. Sentinel values such as minus 999 must be converted to explicit nulls rather than averaged, impossible values such as a humidity of 410 rejected by a range check at ingest, duplicate readings at identical timestamps deduplicated, and gaps in the sequence recorded as gaps rather than silently closed up, because a missing reading may itself indicate the fault. Governance is what keeps this usable in two years' time: a named owner for the combined dataset, a data dictionary defining every field including the units and the aggregation applied, recorded lineage so any alert can be traced back to the readings behind it, a retention policy covering how long full resolution data is kept, and role based access with least privilege, since this data reveals production volumes and would be commercially damaging if it leaked. Finally the system has to be evaluated honestly: the manufacturer should record unplanned downtime for a period before deployment and compare it afterwards, because the only measure that matters is whether downtime fell. The hardest part of all this will not be the sensors or the storage; it is aligning the three systems' identifiers and definitions, because that work is unglamorous, invisible when done and produces confidently wrong answers when skipped.",
           command="Discuss"),
    ],
)


# ============================================================== F201 PAPER A

F201_A = Paper(
    slug="f201-paper-a",
    title="Data Analytics F201 Paper A: Big Data and Machine Learning",
    course="Data Analytics",
    board="OCR",
    code="F201 style",
    minutes=90,
    marks=0,
    accent="var(--purple)",
    blurb="A full length original paper sampling all five topic areas of F201, built around a logistics company instrumenting its fleet and warehouses with sensors.",
    calculator="A calculator may be used.",
    questions=[
        EQ("State **three** characteristics of big data.", 3, [
            MP("One valid characteristic", ["volume", "velocity", "variety", "veracity", "value"]),
            MP("A second, different characteristic", ["velocity", "variety", "veracity", "value", "volume"]),
            MP("A third, different characteristic", ["variety", "veracity", "value", "velocity", "volume"]),
        ], "Volume, velocity and variety.",
           command="State"),

        EQ("The company's vehicles each report location, fuel and engine data every second.\n\nExplain why this data cannot be handled by the overnight batch process the company uses for its orders.", 4, [
            MP("The data arrives continuously rather than as a daily file", ["continuous", "every second", "constantly", "stream", "no end point"]),
            MP("A batch process runs on a schedule, so results are as old as the last run", ["overnight", "schedule", "once a day", "delay", "stale", "hours old"]),
            MP("The value of the data decays quickly", ["too late", "already", "no use", "by the time", "decay", "immediate"]),
            MP("An example specific to this scenario", ["breakdown", "accident", "route", "fault", "driver", "divert", "fuel", "temperature"]),
        ], "Vehicle telemetry arrives continuously rather than as a file that is complete at a known moment, so there is no natural point at which a batch could run over a finished set. A batch process scheduled overnight means every answer is as old as the last run, and for this data that is the whole problem rather than an inconvenience: an engine fault pattern, a refrigeration unit losing temperature or a vehicle leaving its route are all worth knowing within seconds and worth nothing the following morning. The company needs stream processing, where each event is assessed as it arrives and an alert is raised while somebody can still act on it.",
           command="Explain"),

        EQ("Explain the difference between **scaling up** and **scaling out**, and state one cost of scaling out.", 4, [
            MP("Scaling up means a more powerful single machine", ["one machine", "bigger", "more powerful", "vertical"]),
            MP("Scaling out means more machines working together", ["more machines", "cluster", "nodes", "horizontal"]),
            MP("Scaling up has a hard ceiling", ["ceiling", "limit", "largest", "cannot", "runs out"]),
            MP("A genuine cost of scaling out", ["consistency", "eventual", "complexity", "coordination", "network", "replicas disagree", "harder"]),
        ], "Scaling up means replacing a machine with a more powerful one: more processors, more memory, more storage in the same box. Scaling out means adding more machines that work together as a cluster, with the data partitioned across them. Scaling up is simpler and it stops, because there is a largest machine available and no budget moves that ceiling, which is precisely where big data begins. The cost of scaling out is consistency: with data replicated across nodes, different replicas can briefly disagree after a write, so many distributed stores offer only eventual consistency, and every application has to be examined to see whether it can tolerate that. A vehicle's live position can; a fuel card balance cannot.",
           command="Explain"),

        EQ("The chart shows the total data the company holds.\n\nDescribe the trend, estimate the figure for 2027, and give **one** caution about that estimate.", 5, [
            MP("Identifies the growth as accelerating rather than steady", ["accelerat", "exponential", "doubling", "faster", "not linear", "steepen"]),
            MP("Quotes figures from the chart", ["12", "310", "141", "terabytes", "2021", "2026"]),
            MP("Notes the roughly doubling pattern", ["double", "doubling", "twice", "x2", "roughly double"]),
            MP("Gives an estimate consistent with that pattern", ["600", "620", "650", "700", "around 600", "double"]),
            MP("A valid caution about extrapolating", ["cannot continue", "assume", "capacity", "may slow", "extrapolat", "no reason", "limit", "budget"]),
        ], "The growth is accelerating rather than steady: the total roughly doubles each year, from 12 terabytes in 2021 to 19, 34, 68, 141 and 310, so the annual increase itself is growing, which on a linear axis gives the characteristic upward curve shown. Continuing that pattern gives an estimate of roughly 600 to 650 terabytes for 2027. The caution is that this is an extrapolation of a pattern with no stated cause: it assumes the same doubling continues, and growth of this kind usually stops for an ordinary reason, a retention policy, a budget ceiling, a change to what is logged, or simply the end of whatever rollout drove it. The estimate is useful for planning capacity headroom, not as a forecast to commit money against.",
           command="Describe",
           figure="!diagram exam-chart-growth"),

        EQ("Explain what is meant by **moving the computation to the data**, and why it matters at this scale.", 4, [
            MP("The query is sent to the machines holding the data", ["sent to", "query goes", "where the data is", "each node", "locally"]),
            MP("Each node processes its own partition in parallel", ["parallel", "own part", "partition", "block", "share"]),
            MP("Only the small results are returned and combined", ["results", "combine", "small", "aggregate", "partial"]),
            MP("Because moving the data itself would be the bottleneck", ["bandwidth", "too slow", "weeks", "network", "cannot move", "bottleneck"]),
        ], "Instead of pulling a dataset to a machine that will analyse it, the query itself is sent to the machines that already hold the partitions, each one processes its own share locally and in parallel, and only the small partial results travel back to be combined. It matters at this scale because data has weight: moving hundreds of terabytes across a network takes days or weeks, so the transfer, rather than the processing, becomes the limit. Sending a query that is a few kilobytes and receiving a result that is a few kilobytes avoids that entirely, which is the organising idea behind every distributed processing framework.",
           command="Explain"),

        EQ("The company plotted its customers by how often they order and how much they spend, and the groups shown emerged without being specified in advance.\n\nName the technique and the type of learning it is, and describe what the plot shows.", 5, [
            MP("Names the technique as clustering", ["cluster", "k-means", "segmentation"]),
            MP("Identifies it as unsupervised learning", ["unsupervised", "no labels", "unlabelled"]),
            MP("Explains why it is unsupervised", ["no labels", "not told", "discovered", "not specified", "no right answer"]),
            MP("Describes the three groups", ["three", "groups", "low", "high", "frequent", "basket"]),
            MP("Characterises at least one group usefully", ["occasional", "loyal", "high value", "bulk", "small frequent", "infrequent"]),
        ], "The technique is clustering, and it is unsupervised learning, because no labels were supplied: nobody told the algorithm which customers belonged in which group, so the structure was discovered in the data rather than predicted against a known answer. The plot shows three clearly separated groups. One has few visits and a low average basket, which is the occasional small customer. One has many visits but still a low to moderate basket, which is the frequent top-up customer. One has a moderate number of visits with a high basket value, which is the smaller group that is probably worth the most per customer. The separation between them is wide enough that the groups are not an artefact of where the boundaries were drawn.",
           command="Name",
           figure="!diagram exam-cluster-plot"),

        EQ("The table shows the results of the company's fraud detection model.\n\nCalculate the **precision** and the **recall**. Show your working.", 4, [
            MP("Precision substitution: 96 / (96 + 304)", ["96", "400", "304", "96/400"]),
            MP("Precision stated as 24%", ["24", "0.24", "24%"]),
            MP("Recall substitution: 96 / (96 + 24)", ["120", "96/120", "24"]),
            MP("Recall stated as 80%", ["80", "0.8", "80%"]),
        ], "Precision is true positives divided by everything predicted positive: 96 / (96 + 304) = 96 / 400 = 0.24, which is 24%. Recall is true positives divided by everything that actually was positive: 96 / (96 + 24) = 96 / 120 = 0.80, which is 80%.",
           command="Calculate",
           figure="!diagram exam-conf-fraud"),

        EQ("Using your answers, explain what these two figures tell the company about its fraud model.", 4, [
            MP("Recall of 80% means most fraud is caught", ["80", "most", "four in five", "catches", "finds"]),
            MP("But one fifth is still missed", ["24", "missed", "one fifth", "20%", "gets through"]),
            MP("Precision of 24% means most alerts are false alarms", ["24", "three quarters", "most", "false alarm", "304", "wrong"]),
            MP("The operational consequence of that", ["review", "workload", "investigat", "customers", "blocked", "cost", "ignore the alerts"]),
        ], "A recall of 80% means the model finds four fifths of the genuine fraud, which is substantial, though the 24 cases it missed are real losses and the company should know what they have in common. The precision of 24% is the figure that shapes how the model can actually be used: of every hundred transactions it flags, roughly seventy six are perfectly genuine, so the 400 alerts contain 304 false alarms. If each alert blocks a card, the company annoys three honest customers for every fraud it stops; if each is reviewed by a person instead, that is 400 reviews to find 96 cases. Neither is fatal, but it means the model belongs in a review queue rather than wired directly to an automatic block, and raising precision should be the next piece of work.",
           command="Explain"),

        EQ("The chart shows the error of a model on its training data and on held-back validation data during training.\n\nIdentify what is happening and state **two** things that could be done about it.", 6, [
            MP("Identifies overfitting", ["overfit", "memoris", "learning the noise"]),
            MP("Supports it from the chart: training error keeps falling", ["training", "falls", "keeps", "0.04", "down to"]),
            MP("While validation error turns and rises", ["validation", "rises", "turns", "increases", "0.28", "0.53"]),
            MP("Identifies roughly where it begins", ["epoch 6", "sixth", "around 6", "halfway", "0.28"]),
            MP("One valid remedy", ["early stopping", "stop", "simpler model", "fewer features", "regularis", "more data", "prune", "dropout"]),
            MP("A second, different valid remedy", ["more data", "simpler", "regularis", "cross validation", "early stopping", "fewer"]),
        ], "The model is overfitting. The training error falls continuously across all twelve epochs, from 0.62 down to 0.04, which looks like steady improvement. The validation error tells a different story: it falls to a minimum of about 0.28 at around epoch six and then turns and climbs steadily to 0.53, worse than it was at epoch three. From that turning point the model is no longer learning the pattern, it is learning the particular noise of the training set, and its performance on anything it has not seen is getting worse while its apparent performance improves. Two remedies: use early stopping, halting training at the epoch where validation error bottomed out and keeping that version rather than the final one; and reduce the model's capacity or train on more data, since a simpler model has less room to fit noise and more examples dilute it.",
           command="Identify",
           figure="!diagram exam-training-curves"),

        EQ("State **two** sources of bias in a machine learning model.", 2, [
            MP("One valid source", ["historic", "training data", "sampling", "under-represent", "label", "measurement", "proxy", "deployment"]),
            MP("A second, different source", ["sampling", "label", "measurement", "deployment", "feedback", "historic"]),
        ], "Historic bias, where the training data records past unfair human decisions, and sampling bias, where a group is under-represented in the training data.",
           command="State"),

        EQ("The company removes the driver's age and nationality from its model's inputs.\n\nExplain why this does not guarantee that the model is free from bias.", 4, [
            MP("Other fields act as proxies for the removed attribute", ["proxy", "stand in", "correlated", "related", "indirectly"]),
            MP("A plausible example of a proxy here", ["postcode", "depot", "years of service", "licence", "shift", "route", "name", "language"]),
            MP("So the model can still produce unequal outcomes", ["still", "discriminat", "unequal", "same effect", "outcome"]),
            MP("The outcome is what the law judges, not the feature list", ["Equality Act", "outcome", "effect", "not intent", "unlawful", "measured"]),
        ], "Removing a protected characteristic removes the label, not the information. Other fields in the data correlate with it: a postcode, a depot, years of service, which licence categories somebody holds or what shifts they work can all stand in for age or nationality closely enough for the model to reproduce the same pattern without ever seeing the attribute. The result is a model that discriminates in effect while appearing neutral on inspection, and under the Equality Act 2010 it is the outcome that matters rather than the intent or the feature list. The only way to know is to measure: compare the model's error and selection rates for each group separately, and treat a gap between them as a defect rather than as a statistic.",
           command="Explain"),

        EQ("The table compares the company's two data centres.\n\nCalculate the PUE of each site, and identify **two** changes Site A could make.", 5, [
            MP("Site A substitution: 2400 / 1500", ["2400", "1500", "2400/1500"]),
            MP("Site A PUE stated as 1.6", ["1.6", "1.60"]),
            MP("Site B PUE stated as 1.1", ["1.1", "1.10", "1980", "1800"]),
            MP("One valid change", ["raise the inlet temperature", "temperature", "cooling", "free air", "renewable", "consolidat", "virtualis", "idle"]),
            MP("A second, different valid change", ["idle", "310", "decommission", "refresh", "renewable", "hardware", "longer life", "consolidate"]),
        ], "PUE is total facility power divided by the power delivered to the IT equipment. Site A: 2,400 / 1,500 = 1.6, so 60% is spent on cooling and losses on top of the computing itself. Site B: 1,980 / 1,800 = 1.1, which is close to best practice. Two changes for Site A: raise the inlet temperature towards Site B's 27 degrees, since modern equipment is rated for it and cooling to 18 degrees is where most of that 60% overhead is going; and deal with the 310 idle servers out of 900, by consolidating those workloads through virtualisation and decommissioning the hardware, which removes power drawn for no work at all. Beyond those two, moving from a 20% to a higher renewable share would cut emissions without cutting consumption, and extending the three year refresh cycle would reduce the embodied carbon and e-waste.",
           command="Calculate",
           figure="!diagram exam-energy-figures"),

        EQ("The company plans to expand its sensor programme to every vehicle and warehouse, and to use the data to predict breakdowns.\n\nDiscuss the infrastructure and ethical issues this raises, and what the company should do about them.", 10, [
            MP("The volume and velocity of the expanded data is quantified or characterised", ["volume", "velocity", "per second", "millions", "terabytes", "rate"]),
            MP("Edge processing or aggregation is proposed", ["edge", "locally", "aggregate", "only send", "threshold", "summar"]),
            MP("Network bandwidth or connectivity is addressed", ["bandwidth", "mobile", "connection", "coverage", "upload", "data allowance"]),
            MP("A storage approach is named with a reason", ["time series", "lake", "object storage", "warehouse", "cloud", "because"]),
            MP("Processing model: streaming for alerts, batch for training", ["stream", "real time", "batch", "retrain", "both"]),
            MP("An ethical issue about monitoring drivers is raised", ["driver", "monitor", "surveillance", "privacy", "watched", "performance", "personal data"]),
            MP("It is developed, not just named", ["because", "feel", "trust", "proportionate", "consulted", "used against"]),
            MP("Model limitations are addressed", ["false positive", "false negative", "accuracy", "drift", "retrain", "not perfect"]),
            MP("Specific safeguards or governance are proposed", ["policy", "transparent", "told", "DPIA", "access", "retention", "human", "consult", "limit"]),
            MP("A judgement about what matters most and why", ["most important", "biggest", "overall", "therefore", "hardest"]),
        ], "The infrastructure problem is one of rate rather than size. Every vehicle reporting each second produces a continuous stream that no overnight batch can serve, and the volumes compound quickly: the growth chart already shows the company's holdings doubling annually before this expansion. The design should therefore push work to the edge. A unit in each vehicle and warehouse applies threshold rules locally, so a fault raises an alert within milliseconds and keeps doing so when the vehicle is out of coverage, and aggregates the rest into minute level summaries with the mean, minimum, maximum and spread. Full resolution data is buffered and uploaded only around an event, which cuts the transmitted volume by a large factor and matters particularly for vehicles on mobile data, where bandwidth is both limited and metered. Centrally, the summaries belong in a time series store built for timestamped measurements, with the raw event windows in object storage as a lake for model training; alerts run as stream processing because their value decays in seconds, while model retraining runs as batch because it does not. Capacity planning should assume the growth continues, and a retention policy should be written at the start rather than after the bill arrives, since storing everything forever is both an expense and, under storage limitation, a compliance problem. The ethical issues are at least as significant and are easier to get wrong. Telemetry that monitors a vehicle also monitors the person driving it: speed, braking, breaks taken, time at each stop. That is personal data about an identifiable employee, so the company needs a lawful basis, a clear policy saying exactly what is collected and what it will and will not be used for, and it should consult drivers rather than announce it. The difference between a system that predicts a failing alternator and one that scores drivers is a decision about how the same data is used, and if drivers believe it is the second they will work to the measure rather than to the job. Model limitations need stating honestly too: a breakdown predictor will raise false alarms, which cost a wasted inspection, and miss failures, which cost a roadside recovery, so the threshold is a commercial judgement and the output should prompt a maintenance decision rather than automatically take a vehicle off the road. Performance will also drift as the fleet ages and vehicles are replaced, so it must be monitored and the model retrained. Of all of this, the governance of driver data is what the company should get right first. The technical problems are well understood and have standard answers; the trust of the people being measured is the part that cannot be bought back once it is lost, and a workforce that resents the system will find ways to defeat it long before the engineering becomes the limiting factor.",
           command="Discuss"),
    ],
)


# ============================================================== F201 PAPER B

F201_B = Paper(
    slug="f201-paper-b",
    title="Data Analytics F201 Paper B: Big Data and Machine Learning",
    course="Data Analytics",
    board="OCR",
    code="F201 style",
    minutes=90,
    marks=0,
    accent="var(--purple)",
    blurb="A second full length F201 paper, set in an NHS trust considering a model that predicts which patients are at risk of readmission.",
    calculator="A calculator may be used.",
    questions=[
        EQ("Define **machine learning**.", 2, [
            MP("A system that learns patterns from data", ["learns", "patterns", "from data", "examples"]),
            MP("Rather than following rules written explicitly by a programmer", ["rules", "programmed", "explicit", "not told", "without being programmed"]),
        ], "Machine learning is a system that learns patterns from data in order to make predictions or decisions, improving as it is given more examples, rather than following rules written explicitly by a programmer.",
           command="Define"),

        EQ("State the difference between **supervised** and **unsupervised** learning.", 2, [
            MP("Supervised uses labelled data to predict a known target", ["labelled", "labels", "known answer", "target"]),
            MP("Unsupervised finds structure in unlabelled data", ["unlabelled", "no labels", "structure", "groups", "clusters"]),
        ], "Supervised learning is trained on labelled examples, where each input comes with the correct answer, and learns to predict that answer for new data. Unsupervised learning is given unlabelled data and finds structure within it, such as clusters or anomalies, without being told what to look for.",
           command="State"),

        EQ("The table shows the model's results on a held-back set of 4,000 patients.\n\nCalculate the **accuracy**, **precision** and **recall**. Show your working.", 5, [
            MP("Accuracy substitution: (152 + 3342) / 4000", ["3494", "152", "3342", "4000"]),
            MP("Accuracy stated as about 87%", ["87", "87.4", "0.87"]),
            MP("Precision substitution: 152 / 620", ["620", "152/620", "468"]),
            MP("Precision stated as about 25%", ["24.5", "25", "0.245"]),
            MP("Recall stated as 80%", ["190", "152/190", "80", "0.8"]),
        ], "Accuracy is (TP + TN) / all = (152 + 3342) / 4000 = 3494 / 4000 = 0.874, about 87%. Precision is TP / (TP + FP) = 152 / (152 + 468) = 152 / 620 = 0.245, about 25%. Recall is TP / (TP + FN) = 152 / (152 + 38) = 152 / 190 = 0.80, exactly 80%.",
           command="Calculate",
           figure="!diagram exam-conf-disease"),

        EQ("Explain why the accuracy figure you calculated is a misleading measure of this model.", 4, [
            MP("The classes are heavily imbalanced", ["imbalanc", "rare", "few", "190 out of 4000", "5%", "most are negative"]),
            MP("Predicting negative for everyone would score highly", ["predict negative", "say no", "everyone", "95", "without finding"]),
            MP("Such a model would find nothing at all", ["nothing", "zero recall", "no cases", "useless"]),
            MP("So precision and recall must be reported as well", ["precision", "recall", "together", "instead", "as well"]),
        ], "Only 190 of the 4,000 patients actually have the condition, so the classes are heavily imbalanced. A model that simply predicted negative for every patient would be right 3,810 times out of 4,000, an accuracy of about 95%, which is higher than the real model achieves, while finding not a single case. On an imbalanced problem accuracy largely measures the imbalance rather than the model, which is why it should never be quoted alone: precision and recall separate the two things that matter here, how much of the condition the model finds and how often its positive calls are right.",
           command="Explain"),

        EQ("Explain the purpose of a **test set**, and why it should be used only once.", 4, [
            MP("Held back and never used in training", ["held back", "unseen", "not used", "separate"]),
            MP("To estimate performance on new data", ["estimate", "real", "new data", "unseen", "generalise"]),
            MP("Repeated use leaks information into the model", ["leak", "tuned to", "becomes training", "information", "chosen because"]),
            MP("So the estimate stops being honest", ["optimistic", "no longer", "meaningless", "overstate", "biased"]),
        ], "A test set is data held back from training entirely, used at the very end to estimate how the model will perform on cases it has never seen. It should be used once because every time a decision is made on the basis of the test score, which model to keep, which setting to use, information from the test set leaks into those choices. After a few rounds the model has effectively been tuned to that particular sample, and the score it produces measures how well it fits the test set rather than how it will behave on new patients. Tuning belongs on a separate validation set, which can be consulted as often as needed.",
           command="Explain"),

        EQ("Describe **three** sources of big data a hospital trust holds, and state which characteristic of big data each one most stresses.", 6, [
            MP("One valid source named", ["imaging", "scans", "x-ray", "monitor", "vital signs", "records", "notes", "pathology", "genomic", "sensors"]),
            MP("The characteristic it stresses", ["volume", "velocity", "variety", "veracity"]),
            MP("A second, different source", ["monitor", "notes", "records", "imaging", "wearable", "appointment", "pathology"]),
            MP("The characteristic it stresses", ["velocity", "volume", "variety", "veracity"]),
            MP("A third, different source", ["notes", "wearable", "sensor", "records", "imaging", "research"]),
            MP("The characteristic it stresses", ["variety", "veracity", "volume", "velocity"]),
        ], "Medical imaging, where a single CT or MRI study is hundreds of megabytes and a trust produces thousands a week, which stresses volume above all. Bedside monitoring, where every patient on a ward streams heart rate, oxygen saturation and blood pressure continuously, which stresses velocity because the value of a deteriorating trend is in acting on it now. Free text clinical notes and letters, which stress variety and veracity together: they hold a great deal of the clinically useful information and none of it is structured, abbreviations and spellings vary by author, and the same condition is described five ways.",
           command="Describe"),

        EQ("Explain what **overfitting** is, and describe **two** ways of reducing it.", 5, [
            MP("Learning the training data including its noise", ["noise", "too closely", "memoris", "particular sample"]),
            MP("Performs well on training data and poorly on new data", ["training", "new data", "unseen", "poorly", "does not generalise"]),
            MP("One valid remedy", ["more data", "simpler", "fewer features", "regularis", "early stopping", "prune", "cross validation"]),
            MP("It is explained", ["because", "less capacity", "dilute", "prevents", "stops"]),
            MP("A second valid remedy, explained", ["validation", "early stopping", "simpler", "more data", "because"]),
        ], "Overfitting is when a model learns its training data too closely, capturing not only the real pattern but the noise and accidents of that particular sample. The symptom is a model that performs almost perfectly on data it has seen and markedly worse on anything new, because it has memorised rather than generalised. One remedy is to reduce the model's capacity, using fewer features or a simpler, pruned model, because a model with less room to fit cannot fit the noise. A second is to train on more data, since noise does not repeat while the real pattern does, so additional examples dilute the accidents. Alongside both, holding back a validation set and stopping training when validation error stops improving detects the problem as it starts rather than after deployment.",
           command="Explain"),

        EQ("Explain **one** infrastructure challenge of storing and analysing the trust's medical imaging.", 4, [
            MP("The volume is very large per study", ["hundreds of megabytes", "gigabytes", "large", "huge", "per scan"]),
            MP("Which exceeds single machine storage over time", ["cannot fit", "one machine", "petabytes", "distributed", "scale out"]),
            MP("Moving the data is slow", ["bandwidth", "transfer", "slow", "network", "move"]),
            MP("A proposed response", ["distributed", "object storage", "process where it is stored", "GPU", "tiered", "archive", "cloud"]),
        ], "Imaging is the trust's volume problem: a single study runs to hundreds of megabytes, a busy trust produces thousands a week, and the retention periods for clinical images are measured in decades, so the archive grows into petabytes and long ago passed what a single machine can hold. That forces distributed, replicated object storage, and it makes moving the data the binding constraint rather than storing it, because transferring a petabyte over any ordinary link takes weeks. The practical response is to keep the images in one place and send the processing to them, running analysis on machines in the same facility, with GPU capacity alongside the storage, and to tier older studies onto cheaper, slower media rather than keeping everything on the fastest tier.",
           command="Explain"),

        EQ("State **three** legal issues with training a model on patient records.", 3, [
            MP("Health data is special category data", ["special category", "health", "sensitive", "Article 9"]),
            MP("A lawful basis and an additional condition are needed", ["lawful basis", "condition", "consent", "public task", "research"]),
            MP("Transparency, purpose limitation, a DPIA or patient rights", ["purpose", "told", "transparen", "DPIA", "rights", "object", "retention"]),
        ], "Patient records are special category data, so processing needs an additional condition as well as a lawful basis. The records were collected to provide care rather than to train a model, which engages purpose limitation. And because this is large scale processing of special category data, a Data Protection Impact Assessment is required before it begins.",
           command="State"),

        EQ("Explain the safeguards required where a decision about a patient would be made solely by an automated system.", 4, [
            MP("Individuals have a right not to be subject to such a decision", ["right", "not to be subject", "solely automated", "significant effect"]),
            MP("Where it is permitted, meaningful human involvement is required", ["human", "involvement", "review", "not just rubber stamp", "in the loop"]),
            MP("An explanation of the logic must be available", ["explanation", "logic", "reasons", "how it decided", "explainab"]),
            MP("And a route to contest the outcome", ["contest", "challenge", "appeal", "object", "dispute"]),
        ], "Under the UK GDPR a person has the right not to be subject to a decision based solely on automated processing where it produces legal or similarly significant effects, and a decision about someone's clinical care plainly qualifies. Where such processing is permitted at all, three safeguards apply. There must be meaningful human involvement, which means a clinician who genuinely reviews the case and can reach a different conclusion, not one who signs off a queue of scores. The patient must be able to obtain an explanation of the logic involved, which in practice rules out a model whose contributing factors cannot be surfaced. And there must be a route to contest the outcome and have it reconsidered. In a hospital this points firmly towards using the model as decision support that flags patients for review, never as a system that allocates or withholds care by itself.",
           command="Explain"),

        EQ("The table shows the current access permissions in the trust's analytics system.\n\nIdentify **three** problems and state the fix for each.", 6, [
            MP("A former employee's account is still active", ["former", "left", "still active", "leaver", "ex-employee"]),
            MP("It should be disabled through a leaver process", ["disable", "revoke", "remove", "offboard", "leaver"]),
            MP("Least privilege is not applied", ["least privilege", "do not need", "too much", "intern", "payroll", "excessive"]),
            MP("Permissions should be reduced to what the role needs", ["minimum", "restrict", "only", "reduce", "role based"]),
            MP("Export or delete rights are too widely held", ["export", "delete", "every role", "all data", "everyone"]),
            MP("They should be restricted, approved and logged", ["restrict", "approval", "audit", "log", "separate", "named"]),
        ], "First, an account belonging to a former employee is still active with full rights, which in a trust means someone no longer employed can read and delete patient data; the fix is an enforced leaver process that disables accounts on the last working day, backed by a quarterly review of all active accounts against the staff list. Second, least privilege is not being applied: an intern and a marketing assistant can export all data, and developers and analysts can read payroll, none of which those roles require. Permissions should be granted through roles, each cut to the minimum the job needs, with any exception time limited and justified. Third, almost every role can delete records and export the entire dataset, so a single compromised account could exfiltrate or destroy the trust's data. Export and deletion should be separated from ordinary read access, limited to named roles, require a second person's approval, and be written to an audit log that is actually reviewed rather than merely retained.",
           command="Identify",
           figure="!diagram exam-access-matrix"),

        EQ("Explain **two** environmental costs of training and running machine learning models.", 5, [
            MP("Training consumes large amounts of electricity", ["electricity", "energy", "power", "weeks", "GPU", "accelerator"]),
            MP("Development, and retraining, repeats that cost", ["retrain", "repeated", "many runs", "experiments", "every time"]),
            MP("Inference at scale can exceed the training cost", ["inference", "queries", "each use", "billions", "cumulative"]),
            MP("Cooling, water or hardware manufacture is addressed", ["cooling", "water", "e-waste", "hardware", "mining", "manufacture"]),
            MP("A mitigation is offered", ["smaller model", "pretrained", "fine tune", "carbon aware", "renewable", "efficient", "delete"]),
        ], "The first is the electricity of training. A substantial model occupies many accelerators continuously for days or weeks, and that cost is not paid once: the published run is preceded by many failed experiments and followed by retraining each time the data or the task shifts. The second is inference, which is counter-intuitive because a single prediction is tiny; multiplied across every patient scored every day for years, the cumulative energy of running a model routinely exceeds the energy of training it. Behind both sit costs that do not appear on the electricity bill: cooling, which can add a large fraction again depending on the facility's efficiency, fresh water consumed by evaporative cooling, and the mined metals and e-waste of a hardware refresh cycle measured in a few years. The mitigations are mostly about doing less work: fine-tune a pretrained model rather than training from scratch, choose the smallest model that answers the question, schedule flexible training when and where the grid is cleanest, and delete the intermediate datasets a training run leaves behind.",
           command="Explain"),

        EQ("The trust is deciding whether to deploy the readmission model.\n\nDiscuss the arguments for and against deployment, and recommend what the trust should do.", 10, [
            MP("A genuine benefit is identified", ["earlier", "target", "support", "prevent", "resources", "fewer readmissions", "patients"]),
            MP("It is quantified or tied to the figures", ["80", "recall", "152", "four fifths", "finds"]),
            MP("The precision problem is applied to the decision", ["25", "precision", "false positive", "468", "three quarters", "workload"]),
            MP("The operational cost of false positives is described", ["workload", "staff", "calls", "capacity", "resources", "unnecessary"]),
            MP("The cost of false negatives is described", ["missed", "38", "harm", "readmitted", "false assurance"]),
            MP("Bias and unequal performance are addressed", ["bias", "group", "deprived", "ethnic", "measure separately", "unequal"]),
            MP("Explainability and clinical acceptance are addressed", ["explain", "clinician", "black box", "trust", "accountab", "reason"]),
            MP("Legal requirements are named", ["DPIA", "GDPR", "special category", "automated", "human", "transparen"]),
            MP("A clear recommendation is made", ["recommend", "should", "deploy", "do not deploy", "pilot"]),
            MP("The recommendation is justified against the objections raised", ["because", "therefore", "addresses", "on balance", "provided"]),
        ], "The case for deployment is real. A recall of 80% means the model identifies four fifths of the patients who go on to be readmitted within thirty days, and a readmission is both a poor outcome for the patient and an expensive one for the trust. If that list lets a discharge team make a follow-up call, arrange a district nurse visit or check that medication has actually been collected, even a modest reduction in readmissions pays for the work several times over, and it targets scarce follow-up capacity at the patients most likely to need it rather than spreading it evenly. The case against is largely about the other three quarters. With precision at 25%, the model flags 620 patients to find 152, so 468 people are followed up who were never going to be readmitted. That is not harmless: it consumes the same scarce staff time the model is supposed to target, and if the follow-up is intrusive it is an intervention in the lives of people who did not need one. The 38 missed cases matter too, and more subtly, because a list of flagged patients invites staff to treat the unflagged ones as safe, which is a false assurance the model never offered. Two further objections are more serious than the arithmetic. If the trust's historic care was less effective for a deprived or minority group, the model has learned that as though it were clinical fact, so performance must be measured separately for each group and an unequal error rate treated as a defect rather than a footnote. And clinicians cannot act on a score with no reason attached, nor can the trust defend a decision it cannot explain, so a model whose contributing factors can be surfaced is worth more here than a marginally more accurate opaque one. Legally the trust needs a Data Protection Impact Assessment before deployment, an additional condition for processing special category data, transparency with patients, and no solely automated decision with significant effects. My recommendation is to deploy, but as decision support in a limited pilot rather than across the trust, and only once four conditions are met: the impact assessment is complete, error rates have been measured and found comparable across patient groups, the model's main contributing factors are shown alongside each score, and a clinician makes every decision that follows. The pilot should run on one or two wards with readmission rates measured against a comparable ward that does not use it, because the only question that actually matters is whether patients are readmitted less, and that is not answered by the model's accuracy at all.",
           command="Discuss"),
    ],
)


# ============================================================== F201 PAPER C

F201_C = Paper(
    slug="f201-paper-c",
    title="Data Analytics F201 Paper C: Big Data and Machine Learning",
    course="Data Analytics",
    board="OCR",
    code="F201 style",
    minutes=90,
    marks=0,
    accent="var(--purple)",
    blurb="A third full length F201 paper, set around a streaming platform that recommends content, predicts which subscribers will cancel, and reports on its own energy use.",
    calculator="A calculator may be used.",
    questions=[
        EQ("State what is meant by **veracity**, and give one example of poor veracity in a platform's data.", 3, [
            MP("Veracity is the uncertainty or trustworthiness of the data", ["uncertain", "accuracy", "trust", "reliab", "quality", "noise"]),
            MP("Covering noise, gaps, duplicates or bias", ["noise", "gaps", "missing", "duplicate", "bias", "error"]),
            MP("A valid example", ["bot", "shared account", "left playing", "autoplay", "fake", "accidental", "background", "VPN"]),
        ], "Veracity is how far the data can be trusted: how much noise, error, duplication and bias it contains. On a streaming platform a clear example is a title left playing to an empty room, or on a shared household account where one profile is used by three people, both of which are recorded as a genuine view by a single person and are not.",
           command="State"),

        EQ("Give **two** examples of unstructured data the platform holds.", 2, [
            MP("One valid example", ["video", "audio", "subtitle", "artwork", "image", "review", "comment", "thumbnail"]),
            MP("A second, different valid example", ["review", "comment", "support", "audio", "image", "transcript"]),
        ], "The video and audio files themselves, and the free text of subscriber reviews and support messages.",
           command="Give"),

        EQ("Explain the difference between **batch** and **stream** processing, giving an example of each on this platform.", 4, [
            MP("Batch processes a large volume on a schedule", ["schedule", "overnight", "large volume", "periodically", "all at once"]),
            MP("A valid batch example", ["retrain", "monthly report", "billing", "overnight", "royalt", "encode"]),
            MP("Stream processes each event as it arrives", ["as it arrives", "each event", "immediately", "continuous", "real time"]),
            MP("A valid stream example", ["buffering", "live", "play event", "fraud", "concurrent", "recommend now", "alert"]),
        ], "Batch processing handles a large volume of accumulated data on a schedule, which suits work whose answer is not needed immediately: retraining the recommendation model overnight, or calculating the month's royalty payments. Stream processing handles each event as it arrives, which suits work whose value decays within seconds: detecting that playback quality has collapsed in one region and rerouting traffic, or spotting that one account is streaming from six countries at once. The distinction is not about volume but about how quickly the answer stops being useful.",
           command="Explain"),

        EQ("The chart shows the data the platform holds.\n\nDescribe the trend and explain **one** infrastructure consequence of it.", 5, [
            MP("Identifies accelerating growth", ["accelerat", "doubling", "exponential", "faster", "not linear"]),
            MP("Quotes figures from the chart", ["12", "310", "141", "terabytes"]),
            MP("A consequence for storage", ["storage", "distributed", "scale out", "cluster", "cannot fit", "one machine"]),
            MP("Or a consequence for cost, backup or movement", ["cost", "bill", "backup", "transfer", "bandwidth", "egress", "migration"]),
            MP("The consequence is explained rather than stated", ["because", "means", "so the", "would take", "no longer"]),
        ], "The growth is accelerating, not steady: the total roughly doubles each year, from 12 terabytes in 2021 to 19, 34, 68, 141 and 310 in 2026, so each year adds more than all previous years combined did a short time ago. The consequence is that planning cannot be done by scaling up. A single machine large enough for last year is not large enough for next year, so the platform must scale out onto a cluster with the data partitioned and replicated, and accept the consistency trade that comes with it. The second consequence is that migration becomes impractical: moving 300 terabytes between providers over any ordinary link takes weeks and, in the cloud, incurs egress charges that turn an architectural decision into a financial one. Choices made now are harder to reverse each year.",
           command="Describe",
           figure="!diagram exam-chart-growth"),

        EQ("Explain what **eventual consistency** means and give one example where it is acceptable on this platform and one where it is not.", 4, [
            MP("Replicas may briefly disagree after a write", ["replicas", "disagree", "briefly", "not immediately", "lag"]),
            MP("But will converge given time", ["converge", "eventually", "catch up", "agree in time"]),
            MP("An acceptable example", ["view count", "watch list", "recommendation", "rating", "trending", "profile picture"]),
            MP("An unacceptable example, with a reason", ["payment", "subscription", "billing", "cancel", "parental", "access", "because"]),
        ], "Eventual consistency means that after a write, different replicas of the data may briefly disagree, and the guarantee is only that they will converge in time rather than that every reader sees the change immediately. On this platform it is perfectly acceptable for a view count or a trending list: if one region shows a figure a few seconds behind another, nothing is harmed and the alternative, coordinating every replica before acknowledging a play, would make the service slower for everyone. It is not acceptable for the subscription and billing state. If a cancellation reaches one replica and not another, the subscriber is charged after cancelling or keeps access after their final payment, and for parental controls the consequence is worse: a restriction set by a parent must take effect everywhere at once, not shortly.",
           command="Explain"),

        EQ("The table shows how the platform's churn model performed on 2,000 subscribers.\n\nCalculate the **precision** and **recall**, and state which the platform should favour and why.", 6, [
            MP("Precision substitution: 210 / 300", ["210", "300", "90", "210/300"]),
            MP("Precision stated as 70%", ["70", "0.7", "70%"]),
            MP("Recall substitution: 210 / 350", ["350", "140", "210/350"]),
            MP("Recall stated as 60%", ["60", "0.6", "60%"]),
            MP("States which to favour", ["recall", "precision", "favour", "prioritis"]),
            MP("Justifies it with the cost of the error", ["lost subscriber", "cheap", "offer", "discount", "cost of", "annoy", "margin", "worth"]),
        ], "Precision is TP / (TP + FP) = 210 / (210 + 90) = 210 / 300 = 0.70, which is 70%. Recall is TP / (TP + FN) = 210 / (210 + 140) = 210 / 350 = 0.60, which is 60%. The platform should favour recall. A false negative is a subscriber who leaves without ever being offered anything, and the lifetime value of a lost subscriber is large. A false positive is a subscriber who was staying anyway and receives a retention offer, which costs only the margin on that offer and is not unwelcome. Since the cost of missing a leaver is far higher than the cost of a wasted discount, the threshold should be loosened to catch more of the 140 currently missed, accepting that precision will fall as a result.",
           command="Calculate",
           figure="!diagram exam-conf-churn"),

        EQ("Describe **reinforcement learning** and give an example of how this platform could use it.", 4, [
            MP("An agent takes actions in an environment", ["agent", "actions", "environment", "choices"]),
            MP("It receives rewards or penalties for the outcome", ["reward", "penalty", "feedback", "score", "signal"]),
            MP("It learns a policy maximising long run reward", ["policy", "long run", "maximise", "over time", "strategy"]),
            MP("A plausible example on this platform", ["artwork", "thumbnail", "ordering", "which row", "bitrate", "autoplay", "next episode", "test"]),
        ], "In reinforcement learning a system takes actions in an environment and receives a reward or penalty depending on what happens, then adjusts its policy to maximise reward over the long run rather than at each individual step. There is no labelled dataset: the data is generated by acting. The platform could use it to choose which artwork to show for a title, trying variants and learning from whether each viewer went on to watch, or to set streaming bitrate dynamically, where the reward balances picture quality against the penalty of a buffering event. Both suit reinforcement learning because the right answer is not known in advance and the consequences arrive after the decision.",
           command="Describe"),

        EQ("Explain how a recommendation system optimised for engagement can create a **filter bubble**.", 4, [
            MP("It recommends more of what the viewer already engaged with", ["similar", "more of", "same", "already watched", "past behaviour"]),
            MP("Which narrows the range of what is shown", ["narrow", "less variety", "reinforces", "fewer", "restricted"]),
            MP("Its own output becomes the next training signal", ["feedback", "loop", "own output", "reinforces", "compounds", "self"]),
            MP("A consequence for the viewer or society", ["unaware", "cannot discover", "polaris", "assume", "limited", "misses", "entrenched"]),
        ], "A system trained to maximise engagement learns to recommend whatever is most like the things the viewer already watched to the end, because that is what the reward signal rewards. Each round narrows the range offered, and because the viewer can only engage with what they are shown, the system's own output becomes the evidence for its next recommendation. That feedback loop compounds: a mild early preference becomes the whole of what the platform shows. The effect on the viewer is that the catalogue appears to be much smaller and much more uniform than it is, and they have no way of knowing what was filtered out. On contested subjects the same mechanism narrows what people believe is being said, which is why engagement optimisation is treated as a societal issue and not only a product one.",
           command="Explain"),

        EQ("State **four** measures that reduce the environmental impact of a data centre.", 4, [
            MP("A measure relating to cooling", ["free air", "liquid cooling", "inlet temperature", "cooling", "heat reuse"]),
            MP("A measure relating to utilisation", ["virtualis", "consolidat", "idle", "elastic", "shut down", "right size"]),
            MP("A measure relating to supply", ["renewable", "carbon aware", "grid", "clean power", "timing", "location"]),
            MP("A measure relating to hardware or data", ["efficient hardware", "refresh", "lifecycle", "recycl", "delete", "retention", "archive"]),
        ], "Free air or liquid cooling rather than refrigeration, which attacks the largest overhead in most facilities. Virtualisation and consolidation so that fewer physical servers run and fewer sit idle. Buying or generating renewable power, and scheduling flexible workloads for when and where the grid is cleanest. Deleting data that serves no purpose and extending the hardware refresh cycle with repair and certified recycling.",
           command="State"),

        EQ("The table compares two of the platform's data centres running the same workload.\n\nCalculate the PUE of Site A, and explain **two** reasons Site B's figure is lower.", 6, [
            MP("Substitution: 2400 / 1500", ["2400", "1500", "2400/1500"]),
            MP("Site A PUE stated as 1.6", ["1.6", "1.60"]),
            MP("Interprets what that means", ["60%", "overhead", "on top of", "cooling and losses"]),
            MP("Site B's higher inlet temperature means less cooling energy", ["27", "temperature", "cooling", "less refrigeration", "warmer"]),
            MP("Site B has far fewer idle servers", ["idle", "40", "310", "utilis", "consolidat"]),
            MP("A further valid reason, or the overall comparison", ["1.1", "renewable", "newer", "efficient", "refresh", "compared"]),
        ], "PUE is total facility power divided by the power delivered to the IT equipment, so Site A is 2,400 / 1,500 = 1.6. That means 60 per cent again is spent on cooling and distribution losses on top of the computing itself. Site B is 1,980 / 1,800 = 1.1, close to current best practice. Two reasons for the difference. Site B runs at a mean inlet temperature of 27 degrees against Site A's 18, and cooling to the lower figure requires mechanical refrigeration for most of the year, which is where the bulk of Site A's overhead goes, whereas at 27 degrees much of the cooling can be done with outside air. Site B also has 40 idle servers out of 900 against Site A's 310, so Site A is drawing power for more than a third of its fleet doing no work at all, which inflates its IT load and the cooling needed to remove that load's heat. Site B's longer hardware refresh cycle and far higher renewable share do not affect PUE directly but reduce its embodied carbon and emissions substantially.",
           command="Calculate",
           figure="!diagram exam-energy-figures"),

        EQ("Explain what is meant by the **rebound effect** in computing.", 4, [
            MP("Efficiency gains reduce the cost of a unit of computing", ["cheaper", "less energy per", "more efficient", "cost falls"]),
            MP("So more computing is done", ["more", "increases", "used more", "grows", "demand"]),
            MP("Total consumption does not fall as expected", ["total", "overall", "does not fall", "still rises", "offset"]),
            MP("A real example of it", ["data centre", "energy use has risen", "PUE improved", "models got bigger", "streaming quality"]),
        ], "The rebound effect is the tendency for an efficiency gain to be partly or wholly cancelled out by increased use, because the gain makes the activity cheaper. In computing it is well documented: data centre efficiency has improved markedly over the last fifteen years, with typical PUE falling from near 2.0 towards 1.1, and total data centre energy consumption has nevertheless kept rising, because cheaper computing is used for more things. The same pattern appears inside a product: more efficient video codecs were spent on higher resolutions rather than on lower bandwidth. The practical lesson is that efficiency alone is not a strategy, because it reduces the cost per unit of work rather than the amount of work; reducing the work itself, by deleting what is not needed and not running what need not run, is the part that actually shows up in the total.",
           command="Explain"),

        EQ("Explain **two** ways in which a platform of this scale affects society.", 4, [
            MP("One valid effect named", ["filter bubble", "attention", "wellbeing", "employment", "culture", "misinformation", "digital divide", "local industry", "data collection"]),
            MP("It is explained with a mechanism", ["because", "optimis", "algorithm", "autoplay", "replaces", "shifts"]),
            MP("A second, different effect", ["employment", "culture", "surveillance", "divide", "wellbeing", "misinformation", "local"]),
            MP("It is explained with a mechanism", ["because", "means", "leads to", "requires", "shifts"]),
        ], "The first is its effect on attention and wellbeing. Systems that maximise time spent learn the techniques that do so, autoplay, countdowns, episode-length pacing, and the measurable consequences, particularly for younger viewers, are later bedtimes and shorter sleep; the platform is not trying to produce that outcome, which is precisely the problem, because the optimisation target produces it without anyone choosing it. The second is cultural and economic. At this scale the platform's commissioning decisions shape what gets made: data about what is finished and what is abandoned feeds back into which programmes are funded, which favours formats that perform well on the metrics it collects and disadvantages work that is slow, regional or minority-language. That is a genuine shift in who decides what a culture produces, and it is made by an optimisation process rather than by an editor anyone can name.",
           command="Explain"),

        EQ("The platform's board has proposed increasing how strongly the recommendation system optimises for time spent watching.\n\nDiscuss the arguments for and against this, and recommend what the board should do.", 10, [
            MP("A commercial argument in favour", ["revenue", "retention", "subscription", "engagement", "churn", "value", "advertis"]),
            MP("A viewer-facing argument in favour", ["discover", "relevant", "useful", "finds", "satisfaction", "less searching"]),
            MP("The filter bubble or narrowing effect against", ["filter bubble", "narrow", "same", "less variety", "range"]),
            MP("The wellbeing or attention concern against", ["wellbeing", "sleep", "attention", "young", "excessive", "time spent"]),
            MP("A feedback loop or measurement problem is identified", ["feedback", "loop", "own output", "proxy", "time spent is not", "measure"]),
            MP("Bias, fairness or cultural effects are addressed", ["bias", "culture", "minority", "regional", "what gets made", "unequal"]),
            MP("Legal or regulatory exposure is addressed", ["regulat", "online safety", "age", "children", "GDPR", "profiling", "transparen"]),
            MP("An alternative objective is proposed", ["satisfaction", "long term", "completion", "subscriber value", "different metric", "diversity", "measure instead"]),
            MP("A clear recommendation is made", ["recommend", "should not", "should", "instead", "I would"]),
            MP("The recommendation is justified against the arguments raised", ["because", "therefore", "addresses", "on balance", "outweigh"]),
        ], "The commercial argument is straightforward and genuine. Time spent correlates with retention, retention is what a subscription business is, and a recommendation system that surfaces something a subscriber actually wants saves them the irritation of searching a catalogue of thousands of titles. For most viewers most of the time, better recommendations are a better product, and the board is not wrong to want them. The arguments against are about what happens when that particular measure is pushed hard. Optimising for time spent narrows what is shown, because the safest way to keep someone watching is to offer more of what they already finished, and since they can only engage with what they are offered, the system's own output becomes the evidence for its next decision. That feedback loop compounds quietly: the catalogue appears to shrink, discovery stops, and nobody can see what was filtered out. The wellbeing question is sharper still, because the techniques that raise time spent, autoplay, countdowns, cliffhanger pacing, work by making stopping harder rather than by making watching better, and the measurable effects on sleep, particularly for younger viewers, are well established. There is a cultural cost too, since commissioning follows the metrics, and work that is slow, regional or in a minority language performs poorly on time spent regardless of its value. And there is regulatory exposure: profiling that shapes what children see attracts specific obligations, and a platform that cannot explain why it showed what it showed is in a weak position when asked. Underneath all of these is a measurement problem the board should name explicitly. Time spent is a proxy for value, and it is a poor one: a subscriber who watched four hours and regretted it, and one who watched forty minutes and cancelled nothing, look identical to the metric, and only one of them renews. My recommendation is that the board should not increase the weight on time spent. It should instead change what is optimised: use long-run subscriber value, measured by renewal and by direct satisfaction responses, as the objective, keep a deliberate proportion of recommendations outside the viewer's established pattern to preserve discovery, cap the autoplay mechanisms that work by removing a decision rather than informing one, and apply stricter defaults to profiles registered to under-18s. That answers the commercial case, because renewal is what actually produces revenue, while removing the mechanism that generates the wellbeing, cultural and regulatory risks. Raising the weight on time spent would buy a measurable short-term gain against a metric the board has already acknowledged is not the thing it cares about.",
           command="Discuss"),
    ],
)

ALL_DA_PAPERS = [F200_A, F200_B, F200_C, F201_A, F201_B, F201_C]
