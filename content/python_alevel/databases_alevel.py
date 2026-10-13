"""A Level Python: relational databases, normalisation, SQL and transactions."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="relational-databases-and-sql",
    title="Relational Databases, Normalisation and SQL",
    spec="A Level 11",
    icon="i-database",
    minutes=65,
    blurb="Why a flat file goes wrong, normalisation to third normal form worked through on real data, then joins, grouping and constraints in SQL that runs, and transactions with ACID, with a failed transfer rolled back in front of you.",
    fact="The relational model was published in 1970 by Edgar Codd, an IBM researcher, in a paper of just thirteen pages. IBM was slow to build it, because it already sold a profitable older database, and the first commercial relational database came from a small start up that became Oracle.",
    sections=[
        Section("Flat files, keys and relationships", r"""
A **flat file** keeps everything in one table. It is easy to start with and goes wrong in a predictable way: facts get **repeated**.

| OrderID | Customer | City | Product | Price | Quantity |
| 1 | Asha Khan | Leeds | Keyboard | 25.00 | 1 |
| 1 | Asha Khan | Leeds | Mouse | 12.50 | 2 |
| 2 | Ben Ali | York | Keyboard | 25.00 | 3 |
| 3 | Asha Khan | Leeds | Monitor | 120.00 | 1 |

Asha's city is stored three times and the price of a keyboard twice. Every repeat is a chance for the copies to **disagree**:

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Orders (OrderID INTEGER, Customer TEXT, City TEXT, Product TEXT, Price REAL, Quantity INTEGER)")
db.executemany("INSERT INTO Orders VALUES (?, ?, ?, ?, ?, ?)", [
    (1, "Asha Khan", "Leeds", "Keyboard", 25.0, 1),
    (1, "Asha Khan", "Leeds", "Mouse", 12.5, 2),
    (2, "Ben Ali", "York", "Keyboard", 25.0, 3),
    (3, "Asha Khan", "Leeds", "Monitor", 120.0, 1),
])

# Asha moves to Bradford, but the update only reaches one of her three rows
db.execute("UPDATE Orders SET City = 'Bradford' WHERE OrderID = 1 AND Product = 'Keyboard'")

for row in db.execute("SELECT DISTINCT Customer, City FROM Orders ORDER BY Customer, City"):
    print(row)
```

The database now says that Asha lives in Bradford **and** in Leeds. Three kinds of fault come from the repetition:

| Anomaly | What goes wrong | Example |
| **Update** | Changing a fact in some places and not others | Asha's city |
| **Insertion** | You cannot record a fact without an unrelated one | A new product cannot be added until somebody orders it |
| **Deletion** | Deleting one fact destroys another | Deleting order 3 removes the only record of the monitor and its price |

### The relational answer

A **relational database** splits the data into several tables, each about **one thing**, and links them with keys.

| Term | Meaning |
| **Entity** | A thing the database holds facts about, such as a customer |
| **Attribute** | One fact about an entity, which is a column |
| **Record** (tuple) | One entity's row |
| **Primary key** | Attribute(s) whose value is **unique** for each record |
| **Composite key** | A primary key made from **two or more** attributes together |
| **Foreign key** | An attribute holding the **primary key of another table**, which makes the link |
| **Secondary key** | An attribute indexed for searching, though not unique |
| **Referential integrity** | Every foreign key value matches a primary key that really exists |

### Relationships between entities

!diagram py-er-diagram

A **one to many** relationship, one customer has many orders, is made with a foreign key on the **many** side. A **many to many** relationship, an order contains many products and a product is on many orders, cannot be held directly. It is split by a **link table** that has a foreign key to each side, `OrderLine`, whose primary key is the pair together.
"""),
        Section("Normalisation", r"""
**Normalisation** is the process of organising the tables to remove the repetition, and with it the three anomalies. It goes in stages, each one a **normal form**, and each includes the one before.

!diagram py-normalisation

| Form | The rule | What is removed |
| **1NF** | Every cell holds **one value**, there are no repeating groups, and there is a primary key | Lists inside a cell, repeated columns such as Product1, Product2 |
| **2NF** | In 1NF, and every non key attribute depends on the **whole** key | **Partial dependencies**: facts about only part of a composite key |
| **3NF** | In 2NF, and no non key attribute depends on **another non key attribute** | **Transitive dependencies**: a fact about a fact |

A phrase that holds all three: every attribute depends on **the key, the whole key, and nothing but the key**.

### Worked example

The flat table above has no repeating groups, once the primary key is the pair `OrderID` and `Product`, so it is in **1NF**. Now work out what each attribute really depends on.

- `Quantity` depends on **both** parts of the key: how many of *this product* on *this order*.
- `Price` depends only on `Product`. That is a **partial dependency**.
- `Customer` and `City` depend only on `OrderID`. That is another.

**To reach 2NF**, move those out into tables of their own. Now the order's facts and the product's facts are each held once.

- `City` depends on `Customer`, and `Customer` depends on `OrderID`. A fact about a fact is a **transitive dependency**.

**To reach 3NF**, give the customer a table of their own, and let the order refer to it with a foreign key. The finished design is four tables:

| Table | Columns | Key |
| `Customer` | CustomerID, Name, City | CustomerID |
| `Product` | ProductID, Name, Price | ProductID |
| `CustomerOrder` | OrderID, CustomerID | OrderID, with CustomerID as a foreign key |
| `OrderLine` | OrderID, ProductID, Quantity | OrderID and ProductID together, both foreign keys |

Asha's city is stored once. Changing it is one update, and every order sees it.

### Building it in SQL

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys = ON")
db.executescript('''
CREATE TABLE Customer (CustomerID INTEGER PRIMARY KEY, Name TEXT NOT NULL, City TEXT);
CREATE TABLE Product (ProductID INTEGER PRIMARY KEY, Name TEXT NOT NULL, Price REAL CHECK (Price > 0));
CREATE TABLE CustomerOrder (
    OrderID INTEGER PRIMARY KEY,
    CustomerID INTEGER NOT NULL REFERENCES Customer(CustomerID));
CREATE TABLE OrderLine (
    OrderID INTEGER REFERENCES CustomerOrder(OrderID),
    ProductID INTEGER REFERENCES Product(ProductID),
    Quantity INTEGER NOT NULL,
    PRIMARY KEY (OrderID, ProductID));
''')

db.executemany("INSERT INTO Customer VALUES (?, ?, ?)", [(1, "Asha Khan", "Leeds"), (2, "Ben Ali", "York")])
db.executemany("INSERT INTO Product VALUES (?, ?, ?)", [(1, "Keyboard", 25.0), (2, "Mouse", 12.5), (3, "Monitor", 120.0)])
db.executemany("INSERT INTO CustomerOrder VALUES (?, ?)", [(1, 1), (2, 2), (3, 1)])
db.executemany("INSERT INTO OrderLine VALUES (?, ?, ?)", [(1, 1, 1), (1, 2, 2), (2, 1, 3), (3, 3, 1)])

db.execute("UPDATE Customer SET City = 'Bradford' WHERE CustomerID = 1")      # one change
for row in db.execute("SELECT CustomerID, Name, City FROM Customer"):
    print(row)

# referential integrity: an order for a customer that does not exist is refused
try:
    db.execute("INSERT INTO CustomerOrder VALUES (4, 99)")
except sqlite3.IntegrityError as error:
    print("refused:", error)

# a CHECK constraint refuses a price that makes no sense
try:
    db.execute("INSERT INTO Product VALUES (4, 'Faulty', -5)")
except sqlite3.IntegrityError as error:
    print("refused a negative price:", type(error).__name__)
```

The **constraints** do the work that the programmer would otherwise have to remember: `PRIMARY KEY` and `NOT NULL` for entity integrity, `REFERENCES` for **referential integrity**, and `CHECK` for **domain** rules.
"""),
        Section("SQL at A Level: joins, grouping and aggregates", r"""
With the data in separate tables, a query puts it back together with a **JOIN**. `JOIN ... ON` pairs rows of two tables where the key matches.

The queries below all run against the four table design. The setup is repeated so that the program runs on its own.

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript('''
CREATE TABLE Customer (CustomerID INTEGER PRIMARY KEY, Name TEXT, City TEXT);
CREATE TABLE Product (ProductID INTEGER PRIMARY KEY, Name TEXT, Price REAL);
CREATE TABLE CustomerOrder (OrderID INTEGER PRIMARY KEY, CustomerID INTEGER);
CREATE TABLE OrderLine (OrderID INTEGER, ProductID INTEGER, Quantity INTEGER);
INSERT INTO Customer VALUES (1, 'Asha Khan', 'Leeds'), (2, 'Ben Ali', 'York');
INSERT INTO Product VALUES (1, 'Keyboard', 25.0), (2, 'Mouse', 12.5), (3, 'Monitor', 120.0);
INSERT INTO CustomerOrder VALUES (1, 1), (2, 2), (3, 1);
INSERT INTO OrderLine VALUES (1, 1, 1), (1, 2, 2), (2, 1, 3), (3, 3, 1);
''')

def run(sql):
    print(" ".join(sql.split()))
    for row in db.execute(sql):
        print("    ", row)

run('''SELECT Customer.Name, Product.Name, OrderLine.Quantity
       FROM OrderLine
       JOIN CustomerOrder ON OrderLine.OrderID = CustomerOrder.OrderID
       JOIN Customer ON CustomerOrder.CustomerID = Customer.CustomerID
       JOIN Product ON OrderLine.ProductID = Product.ProductID
       WHERE Customer.City = 'Leeds'
       ORDER BY Product.Name''')

run('''SELECT CustomerOrder.OrderID, SUM(Product.Price * OrderLine.Quantity) AS Total
       FROM CustomerOrder
       JOIN OrderLine ON CustomerOrder.OrderID = OrderLine.OrderID
       JOIN Product ON OrderLine.ProductID = Product.ProductID
       GROUP BY CustomerOrder.OrderID''')

run('''SELECT Customer.Name, SUM(Product.Price * OrderLine.Quantity)
       FROM Customer
       JOIN CustomerOrder ON Customer.CustomerID = CustomerOrder.CustomerID
       JOIN OrderLine ON CustomerOrder.OrderID = OrderLine.OrderID
       JOIN Product ON OrderLine.ProductID = Product.ProductID
       GROUP BY Customer.CustomerID
       HAVING SUM(Product.Price * OrderLine.Quantity) > 100''')

run("SELECT COUNT(*), AVG(Price), MIN(Price), MAX(Price) FROM Product")
run("SELECT Name FROM Product WHERE Price BETWEEN 10 AND 30 AND Name LIKE '%o%'")
run("SELECT Name FROM Customer WHERE CustomerID IN (SELECT CustomerID FROM CustomerOrder WHERE OrderID = 2)")
```

| Clause | Does |
| `JOIN ... ON a = b` | Combines rows from two tables where the keys match |
| `GROUP BY` | Collapses rows that share a value into one row per group |
| `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` | **Aggregate functions**: one answer per group |
| `HAVING` | Filters **groups**, after the aggregates are worked out |
| `WHERE` | Filters **rows**, before grouping |
| `BETWEEN`, `IN`, `LIKE` | Range, a list of values, and a pattern |
| A `SELECT` inside another | A **subquery** |

!key WHERE before the groups, HAVING after them :: `WHERE Price > 20` removes products before anything is totalled. `HAVING SUM(...) > 100` removes customers after their totals are worked out, which a WHERE cannot do because the totals do not exist yet.

### Changing data safely

```pseudo
UPDATE Product SET Price = Price * 1.1 WHERE Name = 'Keyboard'
DELETE FROM OrderLine WHERE OrderID = 3
INSERT INTO Product (ProductID, Name, Price) VALUES (4, 'Webcam', 39.99)
```

Always use **parameters**, never joined text, when a value comes from a user. You saw this at GCSE as a defence against SQL injection, and it is still the rule: `db.execute("SELECT ... WHERE Name = ?", (name,))`.
"""),
        Section("Transactions and ACID", r"""
Moving £30 from one account to another takes two updates: take it from one, add it to the other. If the program stops between the two, £30 has disappeared. A **transaction** is a group of operations treated as **one unit**, that either all happen or none do.

The four properties a database guarantees are **ACID**:

| Property | Means | In the transfer |
| **A**tomicity | All of the transaction, or none of it | Both updates happen, or neither does |
| **C**onsistency | The database goes from one valid state to another | The money in the system is the same before and after |
| **I**solation | Transactions running at once do not interfere | Another transfer cannot see the half done one |
| **D**urability | Once committed, the change survives a crash | A power cut after the commit does not lose it |

`commit()` makes the transaction permanent. `rollback()` undoes everything since it began.

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Account (ID INTEGER PRIMARY KEY, Owner TEXT, Balance REAL CHECK (Balance >= 0))")
db.executemany("INSERT INTO Account VALUES (?, ?, ?)", [(1, "Asha", 100.0), (2, "Ben", 50.0)])
db.commit()

def balances():
    return [row[0] for row in db.execute("SELECT Balance FROM Account ORDER BY ID")]

def transfer(source, target, amount):
    try:
        db.execute("UPDATE Account SET Balance = Balance + ? WHERE ID = ?", (amount, target))
        db.execute("UPDATE Account SET Balance = Balance - ? WHERE ID = ?", (amount, source))
        db.commit()
        return "committed"
    except sqlite3.IntegrityError:
        db.rollback()
        return "rolled back"

print(transfer(1, 2, 30), balances())
print(transfer(1, 2, 500), balances())
```

In the second transfer, the first statement, **crediting Ben with £500, succeeded**. The second statement, taking £500 from Asha, was refused by the `CHECK`, because she only has £70. Without a transaction Ben would now hold £550 that came from nowhere. The rollback undid the credit, and the balances are as they were.

### Concurrency and locking

When two users change the same record at once, one change can overwrite the other. The database prevents it with **record locking**: the first transaction to touch a record locks it, and others wait. Two transactions each waiting for a lock that the other holds are in **deadlock**, and the database resolves it by rolling one back.

### Indexes

An **index** is a separate sorted structure on a column, usually a tree, which lets the database find rows by that column without reading the whole table. It makes reads **faster** and writes **slower**, because every insert must update the index, and it costs storage. Primary keys are indexed automatically, and you add an index to a column you search often.

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Person (ID INTEGER PRIMARY KEY, Surname TEXT)")
db.executemany("INSERT INTO Person (Surname) VALUES (?)", [("Khan",), ("Ali",), ("Smith",), ("Khan",)])
db.execute("CREATE INDEX idx_surname ON Person (Surname)")
print(db.execute("SELECT COUNT(*) FROM Person WHERE Surname = 'Khan'").fetchone()[0])
```
"""),
    ],
    keyterms=[
        ("Flat file", "A database held as a single table, which tends to repeat data."),
        ("Relational database", "A database of several tables, each about one entity, linked by keys."),
        ("Primary key", "An attribute, or set of attributes, whose value is unique for every record in a table."),
        ("Foreign key", "An attribute in one table that holds the primary key of a record in another table."),
        ("Referential integrity", "The rule that every foreign key value must match an existing primary key value."),
        ("Normalisation", "Organising the tables of a database to remove repeated data and the anomalies it causes."),
        ("Partial dependency", "An attribute that depends on only part of a composite primary key."),
        ("Transitive dependency", "A non key attribute that depends on another non key attribute rather than directly on the key."),
        ("Transaction", "A group of database operations that is treated as a single unit."),
        ("ACID", "The four properties of a reliable transaction: atomicity, consistency, isolation and durability."),
        ("Index", "A data structure on a column that lets the database find records quickly without reading the whole table."),
    ],
    grade="""
Database questions are about structure first and syntax second, so get the design right before writing a query.

+ Name the key of every table, and mark each foreign key and what it refers to
+ For normalisation, say which rule each change satisfies, and which dependency was removed
+ Join tables on matching keys, and put the aggregate condition in HAVING, not in WHERE
+ Define each part of ACID in a sentence, and tie it to the example in the question
+ Describe an index as a trade: faster searching, slower writing and more storage
""",
    mistakes=[
        "Putting a condition on an aggregate, such as SUM(...) > 100, in a WHERE clause.",
        "Describing normalisation as making a database smaller, instead of removing repeated data and anomalies.",
        "Forgetting the foreign key that links two tables, so the design cannot be joined.",
        "Mixing up a partial dependency, on part of a composite key, with a transitive one, through another attribute.",
        "Saying atomicity means a transaction is fast, when it means all or nothing.",
    ],
    quiz=[
        Q("What is the main problem with storing all the data in a single flat file?",
          ["The same facts are repeated, which can lead to inconsistent data",
           "The file cannot be backed up while the program is running",
           "The data can only be read by one person at a time",
           "The file cannot store more than one type of data"], 0,
          "Repeated data can be changed in one place and not another, which leaves the copies disagreeing."),
        Q("What is a foreign key?",
          ["An attribute that holds the primary key of a record in another table", "An attribute that is unique in its own table",
           "An attribute that holds a password for the database", "An attribute that can be left empty in every record"], 0,
          "It is what links one table to another, such as CustomerID in the order table."),
        Q("What does first normal form require?",
          ["Every cell holds a single value, with no repeating groups, and there is a primary key",
           "Every non key attribute depends on the whole of the primary key",
           "No non key attribute depends on another non key attribute",
           "Every table is linked to at least two other tables"], 0,
          "1NF is the basic tidiness: atomic values, no repeated columns, and a key."),
        Q("What does second normal form remove?",
          ["Partial dependencies on part of a composite key", "Repeating groups of columns",
           "Transitive dependencies between non key attributes", "Foreign keys that refer to other tables"], 0,
          "If an attribute depends on only part of the key, it belongs in a table of its own."),
        Q("What does third normal form remove?",
          ["Transitive dependencies between non key attributes", "Partial dependencies on a composite key",
           "Records that have no foreign key", "Columns that hold numbers"], 0,
          "An attribute should depend on the key itself and not on another attribute that depends on the key."),
        Q("Which clause filters the groups produced by GROUP BY, after aggregates are calculated?",
          ["HAVING", "WHERE", "ORDER BY", "JOIN"], 0,
          "WHERE removes individual rows before grouping, so it cannot use a total that has not been calculated yet."),
        Q("What is the purpose of a JOIN in SQL?",
          ["To combine rows from two tables where their key values match", "To copy a table into a second database",
           "To add a new column to a table", "To delete rows that are not used"], 0,
          "A join is how the data that normalisation split apart is put back together for a query."),
        Q("What does atomicity mean for a database transaction?",
          ["All of its operations happen, or none of them do", "It runs faster than any other operation",
           "It can only affect a single table", "It cannot be undone once it has started"], 0,
          "If any part fails, the whole transaction is rolled back and the database is left as it was."),
        Q("What does referential integrity ensure?",
          ["Every foreign key value matches an existing primary key", "Every primary key is a whole number",
           "Every table has at least ten records", "Every column has a different data type"], 0,
          "It stops an order being recorded for a customer who does not exist."),
        Q("What is the effect of adding an index to a column?",
          ["Searches on that column are faster, but writes are slower and more storage is used",
           "Searches on that column are slower, but writes are faster and less storage is used",
           "The column can no longer contain duplicate values", "The column is removed from the table"], 0,
          "The index is an extra structure that must be kept up to date every time a record changes."),
    ],
    exam=[
        EQ("State three problems that can occur when data is stored in a flat file database.", 3, [
            MP("Data is duplicated, which wastes storage space", ["duplicated", "repeated", "redundant", "redundancy", "wastes", "storage"]),
            MP("The same data may be stored differently in different places, so it is inconsistent", ["inconsistent", "inconsistency", "differently", "disagree", "different places"]),
            MP("A change to a repeated item must be made in many places, which is slow or may be missed", ["many places", "every record", "update", "missed", "each occurrence", "slow"]),
            MP("It is difficult to add or remove data without affecting other data", ["anomal", "delete", "insert", "without affecting", "lost"]),
        ], "Data is repeated in many records, which wastes storage space. The repeated data can become inconsistent, if an item is changed in one record but not in the others. A change to repeated data has to be made in every place it appears, which is slow and easy to get wrong. Deleting a record can also lose other facts that were held only in that record.",
           command="State"),
        EQ("The table shows the data held by a small online shop in a single table. The primary key is the pair OrderID and ProductID. Normalise the data to third normal form. State the name, attributes and primary key of each table that you create.", 6, [
            MP("A Customer table with CustomerID as the primary key, holding the name and address", ["customer", "customerid", "customername", "address"]),
            MP("A Product table with ProductID as the primary key, holding the name and price", ["product", "productid", "productname", "price"]),
            MP("An Order table with OrderID as the primary key, holding the date", ["order table", "orderid", "orderdate", "date"]),
            MP("The Order table has CustomerID as a foreign key to the Customer table", ["customerid", "foreign key", "link", "refers"]),
            MP("An OrderLine table, which links orders and products, with Quantity", ["orderline", "order line", "quantity", "link table"]),
            MP("OrderLine has a composite primary key of OrderID and ProductID, which are both foreign keys", ["composite", "orderid and productid", "both foreign keys", "together"]),
        ], "Customer details depend only on the customer, so they go in a Customer table: CustomerID (primary key), CustomerName, Address. Product details depend only on the product: Product table with ProductID (primary key), ProductName, Price. Order details depend only on the order: Order table with OrderID (primary key), OrderDate and CustomerID, which is a foreign key to the Customer table. The quantity depends on both the order and the product, so an OrderLine table holds OrderID, ProductID and Quantity, and its primary key is the pair OrderID and ProductID together, each of which is also a foreign key.",
           command="Normalise",
           figure="""| OrderID | ProductID | OrderDate | CustomerID | CustomerName | Address | ProductName | Price | Quantity |
| 101 | P1 | 03/05 | C7 | A. Khan | 4 High St | Keyboard | 25.00 | 1 |
| 101 | P2 | 03/05 | C7 | A. Khan | 4 High St | Mouse | 12.50 | 2 |
| 102 | P1 | 04/05 | C9 | B. Ali | 9 Mill Rd | Keyboard | 25.00 | 3 |"""),
        EQ("A database has the tables Customer(CustomerID, Name, City) and CustomerOrder(OrderID, CustomerID, Total). Write an SQL query that displays the Name of each customer and the sum of the Total of all their orders, but only for customers whose orders add up to more than 100.", 4, [
            MP("SELECT the name and SUM of the Total", ["select name", "sum(total)", "sum(", "select"]),
            MP("FROM the two tables, joined ON the matching CustomerID", ["join", "customerid = ", "on", "from customer"]),
            MP("GROUP BY the customer", ["group by"]),
            MP("HAVING SUM(Total) > 100, not WHERE", ["having", "> 100", ">100"]),
        ], r"""```text
SELECT Customer.Name, SUM(CustomerOrder.Total)
FROM Customer
JOIN CustomerOrder ON Customer.CustomerID = CustomerOrder.CustomerID
GROUP BY Customer.CustomerID
HAVING SUM(CustomerOrder.Total) > 100
```

The two tables are joined on the matching CustomerID, the orders are grouped by customer so that SUM gives one total for each, and HAVING keeps only those groups whose total is over 100. WHERE could not be used because the total does not exist until after the grouping.""",
           command="Write"),
        EQ("Explain what is meant by referential integrity, and give an example of how it protects a database.", 3, [
            MP("Every foreign key value must match the primary key of an existing record in the table it refers to", ["match", "exists", "existing", "refers to", "primary key"]),
            MP("The database refuses an action that would break this rule", ["refuse", "prevent", "stops", "rejected", "not allowed", "cannot"]),
            MP("For example, an order cannot be added for a customer who does not exist, or a customer cannot be deleted while they still have orders", ["example", "order", "customer", "does not exist", "still has"]),
        ], "Referential integrity means that every foreign key value must match the primary key of a record that really exists in the table it refers to. The database refuses any action that would break the rule. For example, it will not allow an order to be recorded for a customer number that is not in the Customer table, and it will not allow a customer to be deleted while orders that refer to them still exist, so there are never orders left pointing at nothing.",
           command="Explain"),
        EQ("A bank transfer takes money from one account and adds it to another using two SQL updates. Explain how using a transaction protects the data if the system fails after the first update, with reference to atomicity and durability.", 4, [
            MP("A transaction treats both updates as a single unit", ["single unit", "one unit", "together", "group", "both updates"]),
            MP("Atomicity means all of the updates happen or none do", ["all or nothing", "all of", "none", "atomic", "neither"]),
            MP("After a failure the first update is rolled back, so no money is lost", ["rolled back", "rollback", "undone", "reversed", "no money is lost"]),
            MP("Durability means that once the transaction is committed, the changes are permanent even if the system then fails", ["durab", "permanent", "committed", "survive", "even if", "crash"]),
        ], "A transaction treats the two updates as a single unit. Atomicity means that either both updates are carried out or neither is, so if the system fails after the first update the transaction is rolled back and the first update is undone, which means no money is lost or created. Durability means that once the transaction has been committed the changes are permanent, and they will still be there even if the system fails immediately afterwards.",
           command="Explain"),
    ],
)
