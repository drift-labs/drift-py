import base64
import json
import asyncio

from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
from sdk.state.all import *
from sdk.constants import *


async def load_account_bytes(client: AsyncClient, address: PublicKey) -> bytes:
    resp = await client.get_account_info(pubkey=address)
    if ('result' not in resp) or ('value' not in resp['result']):
        raise Exception('Cannot load bytes.')
    data = resp['result']['value']['data'][0]
    bytes_data = base64.decodebytes(data.encode('ascii'))
    return bytes_data


async def get_clearing_house(client: AsyncClient, address: PublicKey) -> ClearingHouseState:
    """Get the Drift protocol clearing house state.
    :param client: Solana client object.
    :param address: The public address of the Drift protocol clearing house state."""
    bytes_data = await load_account_bytes(
        client=client,
        address=address
    )
    clearing_house = ClearingHouseState.parse(bytes_data=bytes_data)
    return clearing_house


async def get_markets(client: AsyncClient, address: PublicKey) -> DriftMarkets:
    """Get the Drift protocol markets information.
    :param client: Solana client object.
    :param address: The public address of the Drift protocol markets."""
    bytes_data = await load_account_bytes(
        client=client,
        address=address
    )
    markets = DriftMarkets.parse(bytes_data=bytes_data)
    return markets


async def get_user_account(client: AsyncClient, address: PublicKey) -> UserAccount:
    """Get a Drift protocol user account.
    :param client: Solana client object.
    :param address: The public address of the user account."""
    bytes_data = await load_account_bytes(
        client=client,
        address=address
    )
    user_account = UserAccount.parse(bytes_data=bytes_data)
    return user_account


async def get_positions_account(client: AsyncClient, address: PublicKey) -> UserPositions:
    """Get a Drift protocol positions account.
    :param client: Solana client object.
    :param address: The public address of the positions account."""
    bytes_data = await load_account_bytes(
        client=client,
        address=address
    )
    positions_account = UserPositions.parse(bytes_data=bytes_data)
    return positions_account


async def get_curve_history_buffer(client: AsyncClient, address: PublicKey) -> CurveHistory:
    bytes_data = await load_account_bytes(
        client=client,
        address=address
    )
    curve_history = CurveHistory.parse(bytes_data=bytes_data)
    return curve_history


async def get_deposit_history_buffer(client: AsyncClient, address: PublicKey) -> DepositHistory:
    bytes_data = await load_account_bytes(
        client=client,
        address=address
    )
    deposit_history = DepositHistory.parse(bytes_data=bytes_data)
    return deposit_history


async def get_funding_payment_history_buffer(client: AsyncClient, address: PublicKey) -> FundingPaymentHistory:
    bytes_data = await load_account_bytes(
        client=client,
        address=address
    )
    funding_payment_history = FundingPaymentHistory.parse(bytes_data=bytes_data)
    return funding_payment_history


async def get_funding_rate_history_buffer(client: AsyncClient, address: PublicKey) -> FundingRateHistory:
    bytes_data = await load_account_bytes(
        client=client,
        address=address
    )
    funding_rate_history = FundingRateHistory.parse(bytes_data=bytes_data)
    return funding_rate_history


async def get_liquidation_history_buffer(client: AsyncClient, address: PublicKey) -> LiquidationHistory:
    bytes_data = await load_account_bytes(
        client=client,
        address=address
    )
    liquidation_history = LiquidationHistory.parse(bytes_data=bytes_data)
    return liquidation_history


async def get_trade_history_buffer(client: AsyncClient, address: PublicKey) -> TradeHistory:
    bytes_data = await load_account_bytes(
        client=client,
        address=address
    )
    trade_history = TradeHistory.parse(bytes_data=bytes_data)
    return trade_history