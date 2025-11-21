from pydantic import BaseModel


class Wallet(BaseModel):
    """Pydantic model for a wallet."""
    id: int
    address: str
    expected_quantity: float
    currency: str
    
class WalletCreate(BaseModel):
    """Pydantic model for creating a wallet."""
    address: str
    expected_quantity: float
    currency: str

class WalletUpdate(BaseModel):
    """Pydantic model for updating a wallet."""
    expected_quantity: float