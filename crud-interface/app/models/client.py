from pydantic import BaseModel

class OAuth2Client(BaseModel):
    client_id: str
    client_secret: str
    description: str = "Default client for testing"

# Default client credentials for testing
DEFAULT_CLIENT = OAuth2Client(
    client_id="test_client",
    client_secret="test_secret",
    description="Test client for local development"
) 