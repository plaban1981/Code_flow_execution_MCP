"""
Cryptocurrency Tool Wrapper

Type-safe wrapper for cryptocurrency price MCP tool
"""
from typing import Union
import asyncio

from ..models.crypto import GetCryptocurrencyPriceInput, GetCryptocurrencyPriceResponse
from ..client import call_mcp_tool


async def get_cryptocurrency_price(input_data: Union[GetCryptocurrencyPriceInput, dict]) -> GetCryptocurrencyPriceResponse:
    """
    Gets the price of a cryptocurrency

    Args:
        input_data: Input parameters containing crypto symbol

    Returns:
        Cryptocurrency price information
    """
    if isinstance(input_data, dict):
        input_data = GetCryptocurrencyPriceInput(**input_data)

    result = await call_mcp_tool(
        'crypto_service__get_cryptocurrency_price',
        input_data.model_dump(exclude_none=True)
    )

    # Extract fields excluding crypto and raw_data which we set explicitly
    response_fields = {}
    if isinstance(result, dict):
        response_fields = {k: v for k, v in result.items() if k in GetCryptocurrencyPriceResponse.model_fields and k not in ['crypto', 'raw_data']}

    return GetCryptocurrencyPriceResponse(
        crypto=input_data.crypto,
        raw_data=result if isinstance(result, dict) else {"response": result},
        **response_fields
    )


def get_cryptocurrency_price_sync(input_data: Union[GetCryptocurrencyPriceInput, dict]) -> GetCryptocurrencyPriceResponse:
    """Synchronous version of get_cryptocurrency_price"""
    return asyncio.run(get_cryptocurrency_price(input_data))
