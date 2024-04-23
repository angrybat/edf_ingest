from src.constants import ENV_FILE_PATH
from src.main import get_readings_cursor

cursor = get_readings_cursor(ENV_FILE_PATH)

gas_readings = []
electricity_readings = []
while cursor.next_page():
    gas_readings += cursor.gas_readings
    electricity_readings += cursor.electricity_readings
gas_readings += cursor.gas_readings
electricity_readings += cursor.electricity_readings

print(gas_readings)
print(electricity_readings)
