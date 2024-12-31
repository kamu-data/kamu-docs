---
Title: Python Scripts & Notebooks
description: Connecting Python applications to Kamu.
categories: []
aliases: []
---

This guide explains how to connect to Kamu from Python scripts, applications, and Notebook environments like Jupyter.

## Official Client Library
The easiest way to get started is the official [`kamu`](https://github.com/kamu-data/kamu-client-python) Python library available on [PyPi](https://pypi.org/project/kamu/).

Insall:
```sh
pip install kamu
```

Connect and query data via SQL:
```python
import kamu

# Create connection
con = kamu.connect("grpc+tls://node.demo.kamu.dev:50050")

# Returns a Pandas dataframe
con.query("selec 1 as value")
```

Take a look at the [library documentation](https://github.com/kamu-data/kamu-client-python) for examples of authenticating, using different engines, and connecting to local workspaces.


## Jupyter Notebooks
The official [`kamu`](https://github.com/kamu-data/kamu-client-python) Python library offers a few optional Jupyter integrations that you can install as:

```sh
pip install[jupyter-autoviz,jupyter-sql]
```

Import the extension at the beginning of your notebook:

```python
%load_ext kamu
```

Create a connection:
```python
import kamu
con = kamu.connect("grpc+tls://node.demo.kamu.dev:50050")
```

You can now use `%%sql` cell magic:
```sql
%%sql
select 1 as value
```

This extension is pre-installed in the integrated notebook environment you can run via `kamu notebook` command line command.

See [Exploring Data]({{<ref "explore#jupyter-notebooks">}}) section for a tutorial on using notebooks.

For more information on extensions see the [library documentation](https://github.com/kamu-data/kamu-client-python).


## Alternative Options

### SQL Using ADBC
Kamu is based on the [ADBC](https://arrow.apache.org/docs/format/ADBC.html) client API standard and the [Flight SQL](https://arrow.apache.org/docs/format/FlightSql.html) protocol, so any library that can work with those should be able to connect.

Example using the official ADBC library and Pandas:
```python
import adbc_driver_manager
import adbc_driver_flightsql.dbapi
import pandas

con = adbc_driver_flightsql.dbapi.connect(
    "grpc+tls://node.demo.kamu.dev:50050",
    db_kwargs={
        # Anonymous users have to authenticate using basic auth so they could be assigned a session token
        adbc_driver_manager.DatabaseOptions.USERNAME.value: "anonymous",
        adbc_driver_manager.DatabaseOptions.PASSWORD.value: "anonymous",
        # Registered users can provide a bearer token directy
        # adbc_driver_flightsql.DatabaseOptions.AUTHORIZATION_HEADER.value: "Bearer <token>",
    },
    autocommit=True,
)

with con:
    # Pandas natively supports ADBC connections!
    df = pandas.read_sql("select 1 as value", con)
    print(df)
```

### SQL Using SQLAlchemy
[SQLAlchemy](https://www.sqlalchemy.org/) is a popular ORM library for Python that you can use to access data in Kamu in a same way as dozens of other data sources. It is row-oriented, so may be less efficient than using ADBC client for certain use cases. To use it you'll need to install [flightsql-dbapi](https://github.com/influxdata/flightsql-dbapi) package.

Example:
```python
import flightsql.sqlalchemy
import sqlalchemy
import pandas as pd

# Secure remote connection
engine = sqlalchemy.create_engine(
    # Anonymous users have to authenticate using basic auth so they could be assigned a session token
    "datafusion+flightsql://anonymous:anonymous@node.demo.kamu.dev:50050"
    # Registered users can provide a bearer token directy
    # "datafusion+flightsql://node.demo.kamu.dev:50050?token=kamu-token"
)

with engine.connect() as con:
    df = pd.read_sql(sql="select 1 as value", con=con.connection)
    print(df)
```


### SQL Using DBAPI2
DBAPI2 (aka [PEP-249](https://peps.python.org/pep-0249/)) is a standard DB access API in Python, but its row-oriented access to data may be less efficient than using ADBC client. To use it you'll need to install [flightsql-dbapi](https://github.com/influxdata/flightsql-dbapi) package.

Example:
```python
from flightsql import connect, FlightSQLClient
import pandas

# Secure remote connection
client = FlightSQLClient(
    host="node.demo.kamu.dev",
    port=50050,
    # Anonymous users have to authenticate using basic auth so they could be assigned a session token
    user="anonymous",
    password="anonymous",
    # Registered users can provide a bearer token
    # token="<kamu-token>",
)

df = pandas.read_sql("select 1 as value", con)
print(df)
```
