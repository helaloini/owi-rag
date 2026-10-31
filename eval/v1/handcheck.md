# Hand check of 20 LLM-judge verdicts

For each item, read the cited passage and tick whether it supports the sentence.
Sampled with `random.seed(0)` from the cited sentences in `faithfulness.json`.

## 1. How does the ANALYZE command help the SQLite query planner?

**Sentence:** The ANALYZE command gathers statistics about tables and indices, which the query optimizer uses to make better query planning choices [240-0].

**Judge:** supported

**Cited `240-0`** (https://www.sqlite.org/lang_analyze.html)

> The ANALYZE command gathers statistics about tables and indices and stores the collected information in internal tables of the database where the query optimizer can access the information and use it to help make better query planning choices. If no arguments are given, the main database and all attached databases are analyzed. If a schema name is given as the argument, then all tables and indices in that one database are analyzed. If the argument is a table name, then only that table and the indices associated with that table are analyzed. If the argument is an index name, then only that one index is analyzed. The use of ANALYZE is never required. However, if an application makes complex queries that have many possible query plans, the query planner will be better able to pick the best plan if ANALYZE has been run. This can result in significant performance improvements for some queries. Two recommended approaches for when and how to run ANALYZE are described in the next subsections, in order of preference. The PRAGMA optimize command will automatically run ANALYZE when needed. Suggested use: Applications with short-lived database connections should run "PRAGMA optimize;" once, just prior to closing each database connection. Applications that use long-lived database connections should run "PRAGMA optimize=0x10002;" when the connection is first opened, and then

**You:** - [x] supported  - [ ] not supported

---

## 2. What does ON CONFLICT DO UPDATE do in a SQLite upsert?

**Sentence:** Specifically, if a conflict occurs, the specified columns are updated instead of inserting a new row. [376-4] [376-1] [376-2]

**Judge:** supported

**Cited `376-4`** (https://www.sqlite.org/lang_upsert.html)

> just "WHERE true". Ambiguous use of ON: INSERT INTO t1 SELECT * FROM t2 ON CONFLICT(x) DO UPDATE SET y=excluded.y; Ambiguity resolved using a WHERE clause: INSERT INTO t1 SELECT * FROM t2 WHERE true ON CONFLICT(x) DO UPDATE SET y=excluded.y; UPSERT does not currently work for virtual tables. The conflict resolution algorithm for the update operation of the DO UPDATE clause is always ABORT. In other words, the behavior is as if the DO UPDATE clause were actually written as "DO UPDATE OR ABORT". If the DO UPDATE clause encounters any constraint violation, the entire INSERT statement rolls back and halts. This is true even if the DO UPDATE clause is contained within an INSERT statement or a trigger that specifies some other conflict resolution algorithm. UPSERT syntax was added to SQLite with version 3.24.0 (2018-06-04). The original implementation closely followed the PostgreSQL syntax in that it only permitted a single ON CONFLICT clause and it required a conflict target for on DO UPDATE. The syntax was generalized to permit multiple ON CONFLICT clauses and to allow DO UPDATE resolution without a conflict target in SQLite version 3.35.0 (2021-03-12). This page was last updated on 2024-04-11 23:26:09Z

**Cited `376-1`** (https://www.sqlite.org/lang_upsert.html)

> not captured by prior ON CONFLICT clauses. Only a single ON CONFLICT clause, specifically the first ON CONFLICT clause with a matching conflict target, may run for each row of the INSERT. When an ON CONFLICT clause fires, all subsequent ON CONFLICT clauses are bypassed for that one row. In the case of a multi-row insert, the upsert decision is made separately for each row of the insert. The UPSERT processing happens only for uniqueness constraints. A "uniqueness constraint" is an explicit UNIQUE or PRIMARY KEY constraint within the CREATE TABLE statement, or a unique index. UPSERT does not intervene for failed NOT NULL, CHECK, or foreign key constraints or for constraints that are implemented using triggers. Column names in the expressions of a DO UPDATE refer to the original unchanged value of the column, before the attempted INSERT. To use the value that would have been inserted had the constraint not failed, add the special "excluded." table qualifier to the column name. Some examples will help illustrate how UPSERT works: CREATE TABLE vocabulary(word TEXT PRIMARY KEY, count INT DEFAULT 1); INSERT INTO vocabulary(word) VALUES('jovial') ON CONFLICT(word) DO UPDATE SET count=count+1; The upsert above inserts the new vocabulary word "jovial" if that word is not already in the dictionary, or if it is already in the dictionary, it increments the

**Cited `376-2`** (https://www.sqlite.org/lang_upsert.html)

> 1); INSERT INTO vocabulary(word) VALUES('jovial') ON CONFLICT(word) DO UPDATE SET count=count+1; The upsert above inserts the new vocabulary word "jovial" if that word is not already in the dictionary, or if it is already in the dictionary, it increments the counter. The "count+1" expression could also be written as "vocabulary.count". PostgreSQL requires the second form, but SQLite accepts either. CREATE TABLE phonebook(name TEXT PRIMARY KEY, phonenumber TEXT); INSERT INTO phonebook(name,phonenumber) VALUES('Alice','704-555-1212') ON CONFLICT(name) DO UPDATE SET phonenumber=excluded.phonenumber; In the second example, the expression in the DO UPDATE clause is of the form "excluded.phonenumber". The "excluded." prefix causes the "phonenumber" to refer to the value for phonenumber that would have been inserted had there been no conflict. Hence, the effect of the upsert is to insert a phonenumber of Alice if none exists, or to overwrite any prior phonenumber for Alice with the new one. Note that the DO UPDATE clause acts only on the single row that experienced the constraint error during INSERT. It is not necessary to include a WHERE clause that restricts the action to that one row. The only use for the WHERE clause at the end of the DO UPDATE is to optionally change the DO UPDATE into a no-op depending on the original and/or new values. For example: CREATE TABLE phonebook2( name TEXT PRIMARY KEY,

**You:** - [x] supported  - [ ] not supported

---

## 3. What is the purpose of the __init__.py files in a Python package directory?

**Sentence:** They can also execute initialization code for the package or set the __all__ variable. [6-15]

**Judge:** supported

**Cited `6-15`** (https://docs.python.org/3/tutorial/modules.html)

> for the last must be a package; the last item can be a module or a package but can’t be a class or function or variable defined in the previous item. 6.4.1. Importing * From a Package¶ Now what happens when the user writes from sound.effects import *? Ideally, one would hope that this somehow goes out to the filesystem, finds which submodules are present in the package, and imports them all. This could take a long time and importing sub-modules might have unwanted side-effects that should only happen when the sub-module is explicitly imported. The only solution is for the package author to provide an explicit index of the package. The import statement uses the following convention: if a package’s __init__.py code defines a list named __all__, it is taken to be the list of module names that should be imported when from package import * is encountered. It is up to the package author to keep this list up-to-date when a new version of the package is released. Package authors may also decide not to support it, if they don’t see a use for importing * from their package. For example, the file sound/effects/__init__.py could contain the following code: __all__ = ["echo", "surround", "reverse"] This would mean that from sound.effects import * would import the three named submodules

**You:** - [ ] supported  - [x] not supported

---

## 4. How does type affinity work in SQLite for a column declared INTEGER?

**Sentence:** If not, the original data type is preserved. [102-6]

**Judge:** NOT supported

**Cited `102-6`** (https://www.sqlite.org/datatype3.html)

> that it forces integer values into floating point representation. (As an internal optimization, small floating point values with no fractional component and stored in columns with REAL affinity are written to disk as integers in order to take up less space and are automatically converted back into floating point as the value is read out. This optimization is completely invisible at the SQL level and can only be detected by examining the raw bits of the database file.) A column with affinity BLOB does not prefer one storage class over another and no attempt is made to coerce data from one storage class into another. For tables not declared as STRICT, the affinity of a column is determined by the declared type of the column, according to the following rules in the order shown: If the declared type contains the string "INT" then it is assigned INTEGER affinity. If the declared type of the column contains any of the strings "CHAR", "CLOB", or "TEXT" then that column has TEXT affinity. Notice that the type VARCHAR contains the string "CHAR" and is thus assigned TEXT affinity. If the declared type for a column contains the string "BLOB" or if no type is specified then the column has affinity BLOB. If the declared type for a column contains any of the strings

**You:** - [ ] supported  - [x] not supported

---

## 5. What does EXPLAIN QUERY PLAN show?

**Sentence:** It shows how the query is evaluated, including the use of indices and the order of operations. [241-4]

**Judge:** supported

**Cited `241-4`** (https://www.sqlite.org/eqp.html)

> EXPLAIN QUERY PLAN, one SCAN or SEARCH record is output for each nested loop. For example: sqlite> EXPLAIN QUERY PLAN SELECT t1.*, t2.* FROM t1, t2 WHERE t1.a=1 AND t1.b>2; QUERY PLAN |--SEARCH t1 USING INDEX i2 (a=? AND b>?) `--SCAN t2 The order of the entries indicates the nesting order. In this case, the scan of table t1 using index i2 is the outer loop (since it appears first) and the full-table scan of table t2 is the inner loop (since it appears last). In the following example, the positions of t1 and t2 in the FROM clause of the SELECT are reversed. The query strategy remains the same. The output from EXPLAIN QUERY PLAN shows how the query is actually evaluated, not how it is specified in the SQL statement. sqlite> EXPLAIN QUERY PLAN SELECT t1.*, t2.* FROM t2, t1 WHERE t1.a=1 AND t1.b>2; QUERY PLAN |--SEARCH t1 USING INDEX i2 (a=? AND b>?) `--SCAN t2 If the WHERE clause of a query contains an OR expression, then SQLite might use the "OR by union" strategy (also known as the OR optimization). In this case there will be a single top-level record for the search, with two sub-records, one for each index: sqlite> CREATE INDEX i3 ON t1(b); sqlite> EXPLAIN QUERY PLAN SELECT * FROM t1 WHERE a=1

**You:** - [x] supported  - [ ] not supported

---

## 6. What are the RESERVED and PENDING lock states in SQLite?

**Sentence:** Only one can be active, allowing multiple shared locks. [53-3]

**Judge:** NOT supported

**Cited `53-3`** (https://www.sqlite.org/lockingv3.html)

> locks are active. | | RESERVED | A RESERVED lock means that the process is planning on writing to the database file at some point in the future but that it is currently just reading from the file. Only a single RESERVED lock may be active at one time, though multiple SHARED locks can coexist with a single RESERVED lock. RESERVED differs from PENDING in that new SHARED locks can be acquired while there is a RESERVED lock. | | PENDING | A PENDING lock means that the process holding the lock wants to write to the database as soon as possible and is just waiting on all current SHARED locks to clear so that it can get an EXCLUSIVE lock. No new SHARED locks are permitted against the database if a PENDING lock is active, though existing SHARED locks are allowed to continue. | | EXCLUSIVE | An EXCLUSIVE lock is needed in order to write to the database file. Only one EXCLUSIVE lock is allowed on the file and no other locks of any kind are allowed to coexist with an EXCLUSIVE lock. In order to maximize concurrency, SQLite works to minimize the amount of time that EXCLUSIVE locks are held. | The operating system interface layer understands and tracks all five locking states described above. The pager

**You:** - [x] supported  - [ ] not supported

---

## 7. How does the ANALYZE command help the SQLite query planner?

**Sentence:** Running ANALYZE helps the query planner choose more efficient query plans by providing it with up-to-date information on the data distribution [240-5].

**Judge:** supported

**Cited `240-5`** (https://www.sqlite.org/lang_analyze.html)

> to as "statistics tables". The content of the statistics tables can be queried using SELECT and can be changed using the DELETE, INSERT, and UPDATE commands. The DROP TABLE command works on statistics tables as of SQLite version 3.7.9. (2011-11-01) The ALTER TABLE command does not work on statistics tables. Appropriate care should be used when changing the content of the statistics tables as invalid content can cause SQLite to select inefficient query plans. Generally speaking, one should not modify the content of the statistics tables by any mechanism other than invoking the ANALYZE command. See "Manual Control Of Query Plans Using SQLITE_STAT Tables" for further information. Statistics gathered by ANALYZE are not updated as the content of the database changes. If the content of the database changes significantly, or if the database schema changes, then one should consider rerunning the ANALYZE command in order to update the statistics. The query planner loads the content of the statistics tables into memory when the schema is read. Hence, when an application changes the statistics tables directly, SQLite will not immediately notice the changes. An application can force the query planner to reread the statistics tables by running ANALYZE sqlite_schema. The PRAGMA optimize command will automatically run ANALYZE on individual tables on an as-needed basis. The recommended practice is for applications to

**You:** - [ ] supported  - [x] not supported

---

## 8. What does the bm25 function do in FTS5?

**Sentence:** The bm25 function in FTS5 returns a real value indicating how well the current row matches the full-text query [66-42].

**Judge:** supported

**Cited `66-42`** (https://www.sqlite.org/fts5.html)

> '</b>') FROM ft WHERE ft MATCH 'fts5' The built-in auxiliary functions provided as part of FTS5 are described in the following section. Applications may also implement custom auxiliary functions in C. FTS5 provides three built-in auxiliary functions: The built-in auxiliary function bm25() returns a real value indicating how well the current row matches the full-text query. The better the match, the numerically smaller the value returned. A query such as the following may be used to return matches in order from best to worst match: SELECT * FROM ft WHERE ft MATCH ? ORDER BY bm25(ft) In order to calculate a documents score, the full-text query is separated into its component phrases. The bm25 score for document D and query Q is then calculated as follows: In the above, nPhrase is the number of phrases in the query. |D| is the number of tokens in the current document, and avgdl is the average number of tokens in all documents within the FTS5 table. k1 and b are both constants, hard-coded at 1.2 and 0.75 respectively. The "-1" term at the start of the formula is not found in most implementations of the BM25 algorithm. Without it, a better match is assigned a numerically higher BM25 score. Since the default sorting order is "ascending", this means that appending "ORDER BY bm25(ft)"

**You:** - [x] supported  - [ ] not supported

---

## 9. How does SQLite achieve atomic commit with a rollback journal?

**Sentence:** This mechanism allows SQLite to recover from crashes and power failures, maintaining the integrity of the database. [30-7]

**Judge:** supported

**Cited `30-7`** (https://www.sqlite.org/tempfiles.html)

> that created the database connection) with a randomized suffix. The super-journal file contains the names of all of the various attached auxiliary databases that were changed during the transaction. The multi-database transaction commits when the super-journal file is deleted. See the documentation titled Atomic Commit In SQLite for additional detail. Without the super-journal, the transaction commit on a multi-database transaction would be atomic for each database individually, but it would not be atomic across all databases. In other words, if the commit were interrupted in the middle by a crash or power loss, then the changes to one of the databases might complete while the changes to another database might roll back. The super-journal causes all changes in all databases to either rollback or commit together. The super-journal file is only created for COMMIT operations that involve multiple database files where at least two of the databases meet all of the following requirements: This means that SQLite transactions are not atomic across multiple database files on a power-loss when the database files have synchronous turned off or when they are using journal modes of OFF, MEMORY, or WAL. For synchronous OFF and for journal_modes OFF and MEMORY, database will usually corrupt if a transaction commit is interrupted by a power loss. For WAL mode, individual database files are updated atomically

**You:** - [ ] supported  - [x] not supported

---

## 10. What is the difference between VIRTUAL and STORED generated columns in SQLite?

**Sentence:** STORED columns take up space in the database file, whereas VIRTUAL columns use more CPU cycles when being read [38-1].

**Judge:** supported

**Cited `38-1`** (https://www.sqlite.org/gencol.html)

> t1( a INTEGER PRIMARY KEY, b INT, c TEXT, d INT AS (a*abs(b)), e TEXT AS (substr(c,b,b+1)) STORED ); Generated columns can be either VIRTUAL or STORED. The value of a VIRTUAL column is computed when read, whereas the value of a STORED column is computed when the row is written. STORED columns take up space in the database file, whereas VIRTUAL columns use more CPU cycles when being read. From the point of view of SQL, STORED and VIRTUAL columns are almost the same. Queries against either class of generated column produce the same results. The only functional difference is that one cannot add new STORED columns using the ALTER TABLE ADD COLUMN command. Only VIRTUAL columns can be added using ALTER TABLE. Generated columns can have a datatype. SQLite attempts to transform the result of the generating expression into that datatype using the same affinity rules as for ordinary columns. Generated columns may have NOT NULL, CHECK, and UNIQUE constraints, and foreign key constraints, just like ordinary columns. Generated columns can participate in indexes, just like ordinary columns. An index that uses STORED generated columns is just an ordinary index, but an index that uses one or more VIRTUAL generated columns is an expression index. The expression of a generated column can refer to any of the other

**You:** - [x] supported  - [ ] not supported

---

## 11. What values can the journal_mode pragma take?

**Sentence:** The journal_mode pragma can take several values including DELETE, TRUNCATE, PERSIST, MEMORY, WAL, and OFF [32-27].

**Judge:** supported

**Cited `32-27`** (https://www.sqlite.org/pragma.html)

> PRAGMA quick_check command which does most of the checking of PRAGMA integrity_check but runs much faster. PRAGMA schema.journal_mode; PRAGMA schema.journal_mode = DELETE | TRUNCATE | PERSIST | MEMORY | WAL | OFF This pragma queries or sets the journal mode for databases associated with the current database connection. The first form of this pragma queries the current journaling mode for database. When database is omitted, the "main" database is queried. The second form changes the journaling mode for "database" or for all attached databases if "database" is omitted. The new journal mode is returned. If the journal mode could not be changed, the original journal mode is returned. The DELETE journaling mode is the default. In the DELETE mode, the rollback journal is deleted at the conclusion of each transaction. Indeed, the delete operation is the action that causes the transaction to commit. (See the document titled Atomic Commit In SQLite for additional detail.) The TRUNCATE journaling mode commits transactions by truncating the rollback journal to zero-length instead of deleting it. On many systems, truncating a file is much faster than deleting the file since the containing directory does not need to be changed. The PERSIST journaling mode prevents the rollback journal from being deleted at the end of each transaction. Instead, the header of the journal is overwritten with

**You:** - [x] supported  - [ ] not supported

---

## 12. What are STRICT tables in SQLite?

**Sentence:** STRICT tables in SQLite are a feature introduced in version 3.37.0 that enforces rigid type rules, requiring every column to specify a datatype. [27-0] [27-3]

**Judge:** supported

**Cited `27-0`** (https://www.sqlite.org/stricttables.html)

> SQLite strives to be flexible regarding the datatype of the content that it stores. For example, if a table column has a type of "INTEGER", then SQLite tries to convert anything inserted into that column into an integer. So an attempt to insert the string '123' results in an integer 123 being inserted. But if the content cannot be losslessly converted into an integer, for example if the input is 'xyz', then the original string is inserted instead. See the Datatypes In SQLite document for additional information. Some developers appreciate the freedom that SQLite's flexible typing rules provide and use that freedom to advantage. But other developers are aghast at SQLite's flagrant rule-breaking and prefer the traditional rigid type system found in all other SQL database engines and in the SQL standard. For this latter group, SQLite supports a strict typing mode, as of version 3.37.0 (2021-11-27), that is enabled separately for each table. In a CREATE TABLE statement, if the "STRICT" table-option keyword is added to the end, after the closing ")", then strict typing rules apply to that table. The STRICT keyword causes the following differences: Every column definition must specify a datatype for that column. The freedom to specify a column without a datatype is removed. The datatype must be one of the following: No other datatype

**Cited `27-3`** (https://www.sqlite.org/stricttables.html)

> this advanced capability. The behavior of ANY is slightly different in a STRICT table versus an ordinary non-strict table. In a STRICT table, a column of type ANY always preserves the data exactly as it is received. For an ordinary non-strict table, a column of type ANY will attempt to convert strings that look like numbers into a numeric value, and if successful will store the numeric value rather than the original string. For example: | STRICT | ordinary non-strict | |---|---| | CREATE TABLE t1(a ANY) STRICT; INSERT INTO t1 VALUES('000123'); SELECT typeof(a), quote(a) FROM t1; -- result: text '000123' | CREATE TABLE t1(a ANY); INSERT INTO t1 VALUES('000123'); SELECT typeof(a), quote(a) FROM t1; -- result: integer 123 | The STRICT keyword at the end of a CREATE TABLE statement is only recognized by SQLite version 3.37.0 (2021-11-27) and later. If you try to open a database containing the STRICT keyword in an earlier version of SQLite, it will not recognize the keyword and will report an error (except as noted below). But apart from the extra STRICT keyword, the underlying file format of the database is identical. Thus, in general, a database file that contains one or more STRICT tables can only be read and written by SQLite version 3.37.0 or later. However, a database created by SQLite

**You:** - [x] supported  - [ ] not supported

---

## 13. What does EXPLAIN QUERY PLAN show?

**Sentence:** EXPLAIN QUERY PLAN provides a high-level description of the query execution strategy used by SQLite. [241-4]

**Judge:** supported

**Cited `241-4`** (https://www.sqlite.org/eqp.html)

> EXPLAIN QUERY PLAN, one SCAN or SEARCH record is output for each nested loop. For example: sqlite> EXPLAIN QUERY PLAN SELECT t1.*, t2.* FROM t1, t2 WHERE t1.a=1 AND t1.b>2; QUERY PLAN |--SEARCH t1 USING INDEX i2 (a=? AND b>?) `--SCAN t2 The order of the entries indicates the nesting order. In this case, the scan of table t1 using index i2 is the outer loop (since it appears first) and the full-table scan of table t2 is the inner loop (since it appears last). In the following example, the positions of t1 and t2 in the FROM clause of the SELECT are reversed. The query strategy remains the same. The output from EXPLAIN QUERY PLAN shows how the query is actually evaluated, not how it is specified in the SQL statement. sqlite> EXPLAIN QUERY PLAN SELECT t1.*, t2.* FROM t2, t1 WHERE t1.a=1 AND t1.b>2; QUERY PLAN |--SEARCH t1 USING INDEX i2 (a=? AND b>?) `--SCAN t2 If the WHERE clause of a query contains an OR expression, then SQLite might use the "OR by union" strategy (also known as the OR optimization). In this case there will be a single top-level record for the search, with two sub-records, one for each index: sqlite> CREATE INDEX i3 ON t1(b); sqlite> EXPLAIN QUERY PLAN SELECT * FROM t1 WHERE a=1

**You:** - [x] supported  - [ ] not supported

---

## 14. What does the del statement do to a list?

**Sentence:** The del statement can be used to remove items from a list given their index, rather than their value. [8-10]

**Judge:** supported

**Cited `8-10`** (https://docs.python.org/3/tutorial/datastructures.html)

> 'cat', {'spam': 'eggs'}] >>> [*element for element in x] [1, 2, 3, 'c', 'a', 't', 'spam'] But if the objects in x are not iterable, this expression would again raise an exception. 5.2. The del statement¶ There is a way to remove an item from a list given its index instead of its value: the del statement. This differs from the pop() method which returns a value. The del statement can also be used to remove slices from a list or clear the entire list (which we did earlier by assignment of an empty list to the slice). For example: >>> a = [-1, 1, 66.25, 333, 333, 1234.5] >>> del a[0] >>> a [1, 66.25, 333, 333, 1234.5] >>> del a[2:4] >>> a [1, 66.25, 1234.5] >>> del a[:] >>> a [] del can also be used to delete entire variables: >>> del a Referencing the name a hereafter is an error (at least until another value is assigned to it). We’ll find other uses for del later. 5.3. Tuples and Sequences¶ We saw that lists and strings have many common properties, such as indexing and slicing operations. They are two examples of sequence data types (see Sequence Types — list, tuple, range). Since Python is an evolving language, other sequence data types may be added. There is also

**You:** - [x] supported  - [ ] not supported

---

## 15. How do you create a full-text search table with FTS5?

**Sentence:** For example: `CREATE VIRTUAL TABLE email USING fts5(sender, title, body)`. [66-0]

**Judge:** supported

**Cited `66-0`** (https://www.sqlite.org/fts5.html)

> FTS5 is an SQLite virtual table module that provides full-text search functionality to database applications. In their most elementary form, full-text search engines allow the user to efficiently search a large collection of documents for the subset that contain one or more instances of a search term. The search functionality provided to world wide web users by Google is, among other things, a full-text search engine, as it allows users to search for all documents on the web that contain, for example, the term "fts5". To use FTS5, the user creates an FTS5 virtual table with one or more columns. For example: CREATE VIRTUAL TABLE email USING fts5(sender, title, body); It is an error to add types, constraints or PRIMARY KEY declarations to a CREATE VIRTUAL TABLE statement used to create an FTS5 table. Once created, an FTS5 table may be populated using INSERT, UPDATE or DELETE statements like any other table. Like any other table with no PRIMARY KEY declaration, an FTS5 table has an implicit INTEGER PRIMARY KEY field named rowid. Not shown in the example above is that there are also various options that may be provided to FTS5 as part of the CREATE VIRTUAL TABLE statement to configure various aspects of the new table. These may be used to modify the way in which the FTS5

**You:** - [x] supported  - [ ] not supported

---

## 16. Where does sys.argv come from and what does it contain?

**Sentence:** sys.argv comes from the command line arguments passed to the Python script. [4-1] [7-2]

**Judge:** supported

**Cited `4-1`** (https://docs.python.org/3/tutorial/stdlib.html)

> 'quote.py'] 10.3. Command-line arguments¶ Common utility scripts often need to process command-line arguments. These arguments are stored in the sys module’s argv attribute as a list. For instance, let’s take the following demo.py file: # File demo.py import sys print(sys.argv) Here is the output from running python demo.py one two three at the command line: ['demo.py', 'one', 'two', 'three'] The argparse module provides a more sophisticated mechanism to process command-line arguments. The following script extracts one or more filenames and an optional number of lines to be displayed: import argparse parser = argparse.ArgumentParser( prog='top', description='Show top lines from each file') parser.add_argument('filenames', nargs='+') parser.add_argument('-l', '--lines', type=int, default=10) args = parser.parse_args() print(args) When run at the command line with python top.py --lines=5 alpha.txt beta.txt, the script sets args.lines to 5 and args.filenames to ['alpha.txt', 'beta.txt']. 10.4. Error output redirection and program termination¶ The sys module also has attributes for stdin, stdout, and stderr. The latter is useful for emitting warnings and error messages to make them visible even when stdout has been redirected: >>> sys.stderr.write('Warning, log file not found starting a new one\n') Warning, log file not found starting a new one The most direct way to terminate a script is to use sys.exit(). 10.5. String pattern matching¶ The re module provides regular expression tools for advanced string processing. For complex matching

**Cited `7-2`** (https://docs.python.org/3/tutorial/interpreter.html)

> also useful as scripts. These can be invoked using python -m module [arg] ..., which executes the source file for module as if you had spelled out its full name on the command line. When a script file is used, it is sometimes useful to be able to run the script and enter interactive mode afterwards. This can be done by passing -i before the script. All command line options are described in Command line and environment. 2.1.1. Argument Passing¶ When known to the interpreter, the script name and additional arguments thereafter are turned into a list of strings and assigned to the argv variable in the sys module. You can access this list by executing import sys. The length of the list is at least one; when no script and no arguments are given, sys.argv[0] is an empty string. When the script name is given as '-' (meaning standard input), sys.argv[0] is set to '-'. When -c command is used, sys.argv[0] is set to '-c'. When -m module is used, sys.argv[0] is set to the full name of the located module. Options found after -c command or -m module are not consumed by the Python interpreter’s option processing but left in sys.argv for the command or module to handle. 2.1.2. Interactive Mode¶ When commands are read from a tty,

**You:** - [x] supported  - [ ] not supported

---

## 17. What does the AUTOINCREMENT keyword change about rowid selection in SQLite?

**Sentence:** The AUTOINCREMENT keyword changes the ROWID selection algorithm to prevent the reuse of ROWIDs over the lifetime of the database, ensuring that automatically chosen ROWIDs are increasing but not necessarily sequential. [90-0] [90-5]

**Judge:** supported

**Cited `90-0`** (https://www.sqlite.org/autoinc.html)

> The AUTOINCREMENT keyword imposes extra CPU, memory, disk space, and disk I/O overhead and should be avoided if not strictly needed. It is usually not needed. In SQLite, a column with type INTEGER PRIMARY KEY is an alias for the ROWID (except in WITHOUT ROWID tables) which is always a 64-bit signed integer. On an INSERT, if the ROWID or INTEGER PRIMARY KEY column is not explicitly given a value, then it will be filled automatically with an unused integer, usually one more than the largest ROWID currently in use. This is true regardless of whether or not the AUTOINCREMENT keyword is used. If the AUTOINCREMENT keyword appears after INTEGER PRIMARY KEY, that changes the automatic ROWID assignment algorithm to prevent the reuse of ROWIDs over the lifetime of the database. In other words, the purpose of AUTOINCREMENT is to prevent the reuse of ROWIDs from previously deleted rows. In SQLite, table rows normally have a 64-bit signed integer ROWID which is unique among all rows in the same table. (WITHOUT ROWID tables are the exception.) You can access the ROWID of an SQLite table using one of the special column names ROWID, _ROWID_, or OID. Except if you declare an ordinary table column to use one of those special names, then the use of that name will refer to

**Cited `90-5`** (https://www.sqlite.org/autoinc.html)

> inserted and thus causes INSERTs to run a little slower. Note that "monotonically increasing" does not imply that the ROWID always increases by exactly one. One is the usual increment. However, if an insert fails due to (for example) a uniqueness constraint, the ROWID of the failed insertion attempt might not be reused on subsequent inserts, resulting in gaps in the ROWID sequence. AUTOINCREMENT guarantees that automatically chosen ROWIDs will be increasing but not that they will be sequential. Because AUTOINCREMENT keyword changes the behavior of the ROWID selection algorithm, AUTOINCREMENT is not allowed on WITHOUT ROWID tables or on any table column other than INTEGER PRIMARY KEY. Any attempt to use AUTOINCREMENT on a WITHOUT ROWID table or on a column other than the INTEGER PRIMARY KEY column results in an error. This page was last updated on 2024-02-22 16:13:38Z

**You:** - [x] supported  - [ ] not supported

---

## 18. What is the maximum size of a SQLite database file?

**Sentence:** The maximum size of a SQLite database file is theoretically 4294967294 pages, with each page being up to 65536 bytes, which translates to approximately 281 terabytes. [71-11]

**Judge:** supported

**Cited `71-11`** (https://www.sqlite.org/limits.html)

> (18446744073709551616 or about 1.8e+19). This limit is unreachable since the maximum database size of 281 terabytes will be reached first. A 281 terabytes database can hold no more than approximately 2e+13 rows, and then only if there are no indices and if each row contains very little data. Maximum Database Size Every database consists of one or more "pages". Within a single database, every page is the same size, but different databases can have page sizes that are powers of two between 512 and 65536, inclusive. The maximum size of a database file is 4294967294 pages. At the maximum page size of 65536 bytes, this translates into a maximum database size of approximately 2.8e+14 bytes (281 terabytes, or 256 tebibytes, or 281474 gigabytes, or 262143 gibibytes). This particular upper bound is untested since the developers do not have access to hardware capable of reaching this limit. However, tests do verify that SQLite behaves correctly and sanely when a database reaches the maximum file size of the underlying filesystem (which is usually much less than the maximum theoretical database size) and when a database is unable to grow due to disk space exhaustion. Maximum Number Of Tables In A Schema Each table and index requires at least one page in the database file. Thus the maximum number of pages in a

**You:** - [x] supported  - [ ] not supported

---

## 19. What is a covering index in the SQLite query optimizer?

**Sentence:** This makes queries more efficient by reducing the number of disk accesses. [415-18] [119-29]

**Judge:** supported

**Cited `415-18`** (https://www.sqlite.org/queryplanner.html)

> mostly from the estimated time, and so this case could go either way depending on the table size and what WHERE clause constraints were available, and so forth. But generally speaking, the indexed sort would probably be chosen, if for no other reason, because it does not need to accumulate the entire result set in temporary storage before sorting and thus uses much less temporary storage. If a covering index can be used for a query, then the multiple rowid lookups can be avoided and the cost of the query drops dramatically. With a covering index, SQLite can simply walk the index from one end to the other and deliver the output in time proportional to N and without having to allocate a large buffer to hold the result set. The previous discussion has treated searching and sorting as separate topics. But in practice, it is often the case that one wants to search and sort at the same time. Fortunately, it is possible to do this using a single index. Suppose we want to find the prices of all kinds of oranges sorted in order of the state where they are grown. The query is this: | SELECT price FROM fruitforsale WHERE fruit='Orange' ORDER BY state | The query contains both a search restriction in the WHERE clause and

**Cited `119-29`** (https://www.sqlite.org/optoverview.html)

> the usual procedure is to do a binary search on the index to find the index entry, then extract the rowid from the index and use that rowid to do a binary search on the original table. Thus a typical indexed lookup involves two binary searches. If, however, all columns that were to be fetched from the table are already available in the index itself, SQLite will use the values contained in the index and will never look up the original table row. This saves one binary search for each row and can make many queries run twice as fast. When an index contains all of the data needed for a query and when the original table never needs to be consulted, we call that index a "covering index". SQLite attempts to use an index to satisfy the ORDER BY clause of a query when possible. When faced with the choice of using an index to satisfy WHERE clause constraints or satisfying an ORDER BY clause, SQLite does the same cost analysis described above and chooses the index that it believes will result in the fastest answer. SQLite will also attempt to use indexes to help satisfy GROUP BY clauses and the DISTINCT keyword. If the nested loops of the join can be arranged such that rows that are equivalent

**You:** - [ ] supported  - [x] not supported

---

## 20. What is memory-mapped I/O in SQLite and how is it enabled?

**Sentence:** It is enabled by setting the `mmap_size` to a large value using the `PRAGMA mmap_size` statement, typically 256MB or more, depending on the available address space. [128-2]

**Judge:** supported

**Cited `128-2`** (https://www.sqlite.org/mmap.html)

> it will (incorrectly) report database corruption due to the unused space at the end. Or if a version of SQLite prior to 3.7.0 writes to the database while it still has unused space at the end, it may make that unused space inaccessible and unavailable for reuse until after the next VACUUM. Because of the potential disadvantages, memory-mapped I/O is disabled by default. To activate memory-mapped I/O, use the mmap_size pragma and set the mmap_size to some large number, usually 256MB or larger, depending on how much address space your application can spare. The rest is automatic. The PRAGMA mmap_size statement will be a silent no-op on systems that do not support memory-mapped I/O. To read a page of database content using the legacy xRead() method, SQLite first allocates a page-size chunk of heap memory then invokes the xRead() method which causes the database page content to be copied into the newly allocated heap memory. This involves (at a minimum) a copy of the entire page. But if SQLite wants to access a page of the database file and memory mapped I/O is enabled, it first calls the xFetch() method. The xFetch() method asks the operating system to return a pointer to the requested page, if possible. If the requested page has been or can be mapped into the application

**You:** - [x] supported  - [ ] not supported

---
