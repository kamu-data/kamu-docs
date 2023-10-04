---
Title: Generic Python Clients
description: Connecting Python applications to Kamu.
weight: 10040
categories: []
aliases:
---

This guide explains how to connect Python application and scripts to Kamu.

## SQL API: Using ADBC
***Coming soon!***


## SQL API: Using SQLAlchemy and FlightSQL
[SQLAlchemy](https://www.sqlalchemy.org/) is a popular ORM library for Python that you can use to access data in Kamu in a same way as dozens of other data sources. It is row-oriented, so may be less efficient than using ADBC client for certain use cases. To use it you'll need to install [flightsql-dbapi](https://github.com/influxdata/flightsql-dbapi) package.

Example:
```python
import flightsql.sqlalchemy
from sqlalchemy import func, select
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData, Table

engine = create_engine("datafusion+flightsql://kamu:kamu@localhost:50050?insecure=True")
runs = Table("co.alphavantage.tickers.daily.spy", MetaData(bind=engine), autoload=True)
count = select([func.count("*")], from_obj=runs).scalar()
print([(r.name, r.type) for r in runs.columns])
```


## SQL API: Using DBAPI2 and FlightSQL
DBAPI2 (aka [PEP-249](https://peps.python.org/pep-0249/)) is a standard DB access API in Python, but its row-oriented access to data may be less efficient than using ADBC client. To use it you'll need to install [flightsql-dbapi](https://github.com/influxdata/flightsql-dbapi) package.

Example:
```python
from flightsql import connect, FlightSQLClient

client = FlightSQLClient(host='localhost', port=50050, user='kamu', password='kamu', insecure=True)
conn = connect(client)
cursor = conn.cursor()
cursor.execute('select * from "co.alphavantage.tickers.daily.spy" limit 10')
print([r for r in cursor])
```


## SQL API: Using JPype DBAPI2 and JDBC
{{<warning>}}
This method involves running Java process under the hood and in most cases is NOT recommended  - prefer using more efficient connectors listed above.
{{</warning>}}

You can connect to Kamu from Python via JDBC protocol using [Jpype](https://jpype.readthedocs.io/en/latest/) library.

Example:
```python
import jpype
import jpype.dbapi2
import os

jpype.startJVM(
    "--add-opens=java.base/java.nio=ALL-UNNAMED",
    # Include JDBC connector JAR on the class path
    classpath=os.path.join(os.getcwd(), "./flight-sql-jdbc-driver-13.0.0.jar")
)

conn = jpype.dbapi2.connect(
    "jdbc:arrow-flight-sql://127.0.0.1:50050?useEncryption=false", 
    driver_args={
        'user': 'kamu', 
        'password': 'kamu',
    }
)

cursor = conn.cursor()
res = cursor.execute("show tables").fetchall()

print(res)

cursor.close()
conn.close()
```
