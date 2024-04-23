from src.constants import ENV_FILE_PATH
from src.main import get_readings, get_readings_cursor

cursor = get_readings_cursor(ENV_FILE_PATH)
readings = get_readings(cursor)

print(readings.gas)
print(readings.electricity)
