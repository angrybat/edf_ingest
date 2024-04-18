from pathlib import Path

QUERIES_FOLDER = Path("src/queries")
GET_READINGS_QUERY_FILE_PATH = QUERIES_FOLDER / "get_readings.graphql"
GET_ACCOUNT_NUMBER_QUERY_FILE_PATH = QUERIES_FOLDER / "get_account_number.graphql"
GET_JWT_QUERY_FILE_PATH = QUERIES_FOLDER / "get_jwt.graphql"
ENV_FILE_PATH = Path("env.json")
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
