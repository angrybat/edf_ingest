from datetime import datetime

from src.models import ReadingFrequencyType

JWT = "ThisIsAJwt"
ACCOUNT_NUMBER = "account_number"
URL = "http://localhost:8008"
START_AT = datetime(2024, 4, 1)
END_AT = datetime(2024, 4, 14)
FIRST = 42
GAS_READING_FREQUENCY = ReadingFrequencyType.DAY_INTERVAL
ELECTRICITY_READING_FREQUENCY = ReadingFrequencyType.MONTH_INTERVAL
QUERY_STRING = """
{
  hero {
    name
    # Queries can have comments!
    friends {
      name
    }
  }
}
"""
