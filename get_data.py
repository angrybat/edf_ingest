from src.constants import ENV_FILE_PATH
from src.cursors import ReadingsCursor
from src.factories import get_settings

settings = get_settings(ENV_FILE_PATH)
cursor = ReadingsCursor(settings)

gas_readings = []
electricity_readings = []
while cursor.next_page():
    gas_readings += cursor.gas_readings
    electricity_readings += cursor.electricity_readings
gas_readings += cursor.gas_readings
electricity_readings += cursor.electricity_readings

print(gas_readings)
print(electricity_readings)
