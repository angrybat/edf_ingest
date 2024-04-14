from src.client import get_account_name
from src.constants import ACCOUNT_NAME_QUERY_FILE_PATH, ENV_FILE_PATH
from src.cursors import ReadingsCursor
from src.factories import get_settings

settings = get_settings(ENV_FILE_PATH)
account_number = get_account_name(
    settings.url, settings.jwt, ACCOUNT_NAME_QUERY_FILE_PATH
)
cursor = ReadingsCursor(settings, account_number)

gas_readings = []
electricity_readings = []
while cursor.next_page():
    gas_readings += cursor.gas_readings
    electricity_readings += cursor.electricity_readings
gas_readings += cursor.gas_readings
electricity_readings += cursor.electricity_readings

print(gas_readings)
print(electricity_readings)
