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
print("Str queries:")
print(str_queries.get_profile_by_id)
# SELECT * FROM profile WHERE id = $1;
print(str_queries.get_profile_by_username)
# SELECT * FROM profile WHERE username = $1;

examples_path = Path(__file__).parent
sql_path = examples_path / "sql"
file_path = sql_path / "user.sql"


class FileQueries(Queries):
    get_user_by_id: str
    get_user_by_username: str


file_queries = FileQueries().from_file(file_path)
print("File queries:")
print(file_queries.__dict__)


class DirQueries(Queries):
    get_user_by_id: str
    get_user_by_username: str
    get_game_by_id: str
    get_games_by_score: str


class MergedQueries(StrQueries, FileQueries):
    pass


dir_queries = DirQueries().from_dir(sql_path)
print("Dir queries:")
print(dir_queries.__dict__)

merged = MergedQueries().merge(*[str_queries, file_queries])
# or
merged = MergedQueries().merge(str_queries, file_queries)
print("Merged queries:")
print(merged.__dict__)
