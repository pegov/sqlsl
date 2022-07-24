# sqlsl - SQL simple loader

Load sql queries from directories, files or strings.

Queries are loaded as simple strings.

## Installation
```
pip install sqlsl
```

Or if you use [poetry](https://python-poetry.org/):
```
poetry add sqlsl
```

## Format
```sql
-- name: <name1>
<query1>;

-- name: <name2>
<query2>;
```

**"name"** will be used as an attribute of a python object.

**;** - delimiter (subject to change).

A `LoaderException` will be raised on a duplicate name.

Example:
```sql
-- name: get_profile_by_id
SELECT
  *
FROM
  profile
WHERE
  id = $1;

-- name: get_profile_by_username
SELECT
  *
FROM
  profile
WHERE
  username = $1;
```

**IMPORTANT!!!**

Queries without names will be ignored.

In the following *example.sql* `INSERT` query is ignored
because **;** is the delimiter, so `INSERT` query has no **name**.


*example.sql*
```sql
-- name: get_four_and_insert
SELECT 4;
INSERT INTO profile(username) VALUES ('username1');

-- name: get_five
SELECT 5;
```

*db.py*
```python
print(queries.get_four_and_insert)
# SELECT 4;
```


## Usage

See **examples** folder

Load from **string**:

```python
from pathlib import Path

from sqlsl import Queries


# type hints
class StrQueries(Queries):
    get_profile_by_id: str
    get_profile_by_username: str


sql = """
-- name: get_profile_by_id
SELECT * FROM profile WHERE id = $1;

-- name: get_profile_by_username
SELECT * FROM profile WHERE username = $1;
"""

str_queries = StrQueries().from_str(sql)
print(str_queries.get_profile_by_id)
# SELECT * FROM profile WHERE id = $1;
print(str_queries.get_profile_by_username)
# SELECT * FROM profile WHERE username = $1;

```

Load from **file**:

*sql/user.sql*
```sql
-- name: get_user_by_id
SELECT
  id,
  username
FROM
  auth_user
WHERE
  id = $1;

-- name: get_user_by_username
SELECT
  id,
  username
FROM
  auth_user
WHERE
  username = $1;

```

```python
from pathlib import Path

from sqlsl import Queries

examples_path = Path(__file__).parent
sql_path = examples_path / "sql"
file_path = sql_path / "user.sql"


class FileQueries(Queries):
    get_user_by_id: str
    get_user_by_username: str


file_queries = FileQueries().from_file(file_path)
```

Load from **dir**:


```python
from pathlib import Path

from sqlsl import Queries

examples_path = Path(__file__).parent
sql_path = examples_path / "sql"

class DirQueries(Queries):
    get_user_by_id: str
    get_user_by_username: str
    get_game_by_id: str
    get_games_by_score: str


# load all *.sql files from dir
dir_queries = DirQueries().from_dir(sql_path)
```

Merge queries:

```python
# type hinting
class MergedQueries(StrQueries, FileQueries):
    pass

merged = MergedQueries().merge(*[str_queries, file_queries])
# or
merged = MergedQueries().merge(str_queries, file_queries)
```

## TODO

- [ ] make `-- name:` the delimiter (allow the example from **IMPORTANT!!!**).
- [ ] tests
