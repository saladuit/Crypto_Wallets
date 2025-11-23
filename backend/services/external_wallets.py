"""Mocked external wallets service.

This module simulates fetching wallets from an external API by returning
a hard-coded list of wallets. Each wallet is represented as a dict with
`id`, `address`, `quantity`, and `currency` keys.
"""

from typing import List, Dict


def get_external_wallets() -> List[Dict]:
    """Return a hard-coded list of three external wallets.

    The data simulates the shape returned by an external API and is
    intentionally simple for frontend integration and testing.
    """
    return [
        {
            "id": 1,
            "address": "0xExternalAddr1",
            "quantity": 10.0,
            "currency": "ETH",
        },
        {
            "id": 2,
            "address": "0xExternalAddr2",
            "quantity": 5.5,
            "currency": "BTC",
        },
        {
            "id": 3,
            "address": "0xExternalAddr3",
            "quantity": 0.0,
            "currency": "USDT",
        },
    ]
