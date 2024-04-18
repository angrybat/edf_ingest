from src.client import get_account_number, get_authorization_tokens
from src.constants import ENV_FILE_PATH, GET_ACCOUNT_NUMBER_QUERY_FILE_PATH
from src.cursors import ReadingsCursor
from src.factories import get_settings

settings = get_settings(ENV_FILE_PATH)
authorization_tokens = get_authorization_tokens(
    settings.url, settings.email_address, settings.password
)
account_number = get_account_number(
    settings.url, authorization_tokens.jwt, GET_ACCOUNT_NUMBER_QUERY_FILE_PATH
)
cursor = ReadingsCursor(settings, account_number, authorization_tokens)

gas_readings = []
electricity_readings = []
while cursor.next_page():
    gas_readings += cursor.gas_readings
    electricity_readings += cursor.electricity_readings
gas_readings += cursor.gas_readings
electricity_readings += cursor.electricity_readings

print(gas_readings)
print(electricity_readings)
