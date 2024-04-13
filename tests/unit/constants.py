URL = "http://localhost:8008"
JWT = "ThisIsAJwt"
ACCOUNT_NUMBER = "account_number"
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
