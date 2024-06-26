from datetime import datetime, timezone

from src.models import ReadingFrequencyType

JWT = "ThisIsAJwt"
REFRESH_TOKEN = "ThisIsARefreshToken"
EMAIL_ADDRESS = "email@address.com"
PASSWORD = "password"
ACCOUNT_NUMBER = "account_number"
URL = "http://localhost:8008"
START_AT = datetime(2024, 4, 1)
END_AT = datetime(2024, 4, 20)
EXPIRES_AT = datetime(2024, 4, 1, 1, tzinfo=timezone.utc)
REFRESH_EXPIRES_IN = datetime(2024, 4, 1, 1, 5, 0, tzinfo=timezone.utc)
FIRST = 42
CURSOR = "thisIsTheCursor"
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
