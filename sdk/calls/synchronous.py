import base64
import json

from solana.rpc.api import Client
from solana.publickey import PublicKey
from sdk.state.all import *
from sdk.constants import *


def load_account_bytes(client: Client, address: PublicKey) -> bytes:
    resp = client.get_account_info(pubkey=address)
    if ('result' not in resp) or ('value' not in resp['result']):
        raise Exception('Cannot load bytes.')
    data = resp['result']['value']['data'][0]
    bytes_data = base64.decodebytes(data.encode('ascii'))
    return bytes_data


def call_clearing_house(client: Client, address: PublicKey) -> ClearingHouseState:
    """Get the Drift protocol clearing house state.
    :param client: Solana client object.
    :param address: The public address of the Drift protocol clearing house state."""
    bytes_data = load_account_bytes(
        client=client,
        address=address
    )
    clearing_house = ClearingHouseState.parse(bytes_data=bytes_data)
    return clearing_house


def call_markets(client: Client, address: PublicKey) -> DriftMarkets:
    """Get the Drift protocol markets information.
    :param client: Solana client object.
    :param address: The public address of the Drift protocol markets."""
    bytes_data = load_account_bytes(
        client=client,
        address=address
    )
    markets = DriftMarkets.parse(bytes_data=bytes_data)
    return markets


def call_user_account(client: Client, address: PublicKey) -> UserAccount:
    """Get a Drift protocol user account.
    :param client: Solana client object.
    :param address: The public address of the user account."""
    bytes_data = load_account_bytes(
        client=client,
        address=address
    )
    user_account = UserAccount.parse(bytes_data=bytes_data)
    return user_account


def call_positions_account(client: Client, address: PublicKey) -> UserPositions:
    """Get a Drift protocol positions account.
    :param client: Solana client object.
    :param address: The public address of the positions account."""
    bytes_data = load_account_bytes(
        client=client,
        address=address
    )
    positions_account = UserPositions.parse(bytes_data=bytes_data)
    return positions_account


def call_curve_history_buffer(client: Client, address: PublicKey) -> CurveHistory:
    bytes_data = load_account_bytes(
        client=client,
        address=address
    )
    curve_history = CurveHistory.parse(bytes_data=bytes_data)
    return curve_history


def call_deposit_history_buffer(client: Client, address: PublicKey) -> DepositHistory:
    bytes_data = load_account_bytes(
        client=client,
        address=address
    )
    deposit_history = DepositHistory.parse(bytes_data=bytes_data)
    return deposit_history


def get_funding_payment_history_buffer(client: Client, address: PublicKey) -> FundingPaymentHistory:
    bytes_data = load_account_bytes(
        client=client,
        address=address
    )
    funding_payment_history = FundingPaymentHistory.parse(bytes_data=bytes_data)
    return funding_payment_history


def get_funding_rate_history_buffer(client: Client, address: PublicKey) -> FundingRateHistory:
    bytes_data = load_account_bytes(
        client=client,
        address=address
    )
    funding_rate_history = FundingRateHistory.parse(bytes_data=bytes_data)
    return funding_rate_history


def get_liquidation_history_buffer(client: Client, address: PublicKey) -> LiquidationHistory:
    bytes_data = load_account_bytes(
        client=client,
        address=address
    )
    liquidation_history = LiquidationHistory.parse(bytes_data=bytes_data)
    return liquidation_history


def get_trade_history_buffer(client: Client, address: PublicKey) -> TradeHistory:
    bytes_data = load_account_bytes(
        client=client,
        address=address
    )
    trade_history = TradeHistory.parse(bytes_data=bytes_data)
    return trade_history