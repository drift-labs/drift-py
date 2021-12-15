"""Asynchronous client to interact with the Drift protocol."""
import base58
import json
import asyncio
from typing import List, Literal, Optional
from construct import Int8ul

from solana.publickey import PublicKey
from solana.keypair import Keypair
from solana.rpc.async_api import AsyncClient as SolanaClient, Commitment
from solana.rpc.types import RPCResponse

from sdk.constants import *
from sdk.state.all import *
from sdk.calls.asynchronous import *
from sdk.sends.asynchronous import *
from sdk.utils import (
    get_user_account_address, position_direction, get_collateral_account_address, get_market_index
)


class DriftClient:
    """Asynchronous client to interact with the drift protocol."""

    def __init__(
            self, connector: Optional[SolanaClient], endpoint: Optional[str], commitment: Optional[Commitment],
            wallet: Optional[Keypair], user_account: Optional[PublicKey], user_positions: Optional[PublicKey],
            user_collateral_account: Optional[PublicKey]
    ) -> None:
        self.connector = connector
        self.endpoint = endpoint
        self.commitment = Commitment(commitment)
        self.wallet = wallet
        self.user_account = user_account
        self.user_positions = user_positions
        self.user_collateral_account = user_collateral_account

    @classmethod
    async def create(
            cls, private_key: str or List[int], endpoint: str = MAINNET_ENDPOINT,
            commitment: Commitment = CONFIRMED
    ):
        """Instantiate a Drift-client from a private key.

        :param private_key: The private key of the wallet, either as a string (e.g., Phantom) or a list of 8-bit
        integers (e.g., Solflare).
        :param endpoint: The http endpoint of the rpc node to which instructions are to be sent.
        :param commitment: The Solana-commitment object specifying the validity of state, see Solana docs for
        more info."""
        if type(private_key) == str:
            private_key_bytes = base58.b58decode(private_key.encode('utf-8'))
        elif type(private_key) == list:
            private_key_bytes = Int8ul[64].build(private_key)
        else:
            raise Exception('Invalid private key.')

        wallet_keypair = Keypair.from_secret_key(
            secret_key=private_key_bytes
        )
        connector = SolanaClient(
            endpoint=endpoint,
            commitment=commitment
        )
        user_account_address = get_user_account_address(
            authority=wallet_keypair.public_key
        )
        user_account = await call_user_account(
            client=connector,
            address=user_account_address
        )
        user_positions_address = user_account.positions_account
        user_collateral_account_address = get_collateral_account_address(
            authority=wallet_keypair.public_key
        )
        drift_client = cls(
            connector=connector,
            endpoint=endpoint,
            commitment=commitment,
            wallet=wallet_keypair,
            user_account=user_account_address,
            user_positions=user_positions_address,
            user_collateral_account=user_collateral_account_address
        )
        return drift_client

    async def close(self) -> None:
        """Close connections."""
        await self.connector.close()

    """GET ACCOUNTS"""

    async def get_clearing_house(self) -> ClearingHouseState:
        """Get the current state of the ClearingHouse."""
        clearing_house = await call_clearing_house(
            client=self.connector,
            address=CLEARING_HOUSE_ADDRESSES.state
        )
        return clearing_house

    async def get_user_account(self) -> UserAccount:
        """Get your user-account."""
        user_account = await call_user_account(
            client=self.connector,
            address=self.user_account
        )
        return user_account

    async def get_positions(self) -> UserPositions:
        """Get your positions."""
        user_positions = await call_positions_account(
            client=self.connector,
            address=self.user_positions
        )
        return user_positions

    async def get_all_markets(self) -> DriftMarkets:
        """Get all markets."""
        drift_markets = await call_markets(
            client=self.connector,
            address=CLEARING_HOUSE_ADDRESSES.markets
        )
        return drift_markets

    async def get_market(self, symbol: str) -> DriftMarket:
        """Get a single market."""
        market_index = get_market_index(
            symbol=symbol
        )
        all_markets = await self.get_all_markets()
        drift_market = all_markets.markets[market_index]
        return drift_market

    """SEND INSTRUCTIONS"""

    async def open_position(
            self, market: str, direction: Literal['long', 'short'], quote_amount: int
    ) -> RPCResponse:
        """Open a position."""
        if market in MARKET_NAME_TO_INDEX:
            market_index = MARKET_NAME_TO_INDEX.index(market)
        else:
            raise Exception(f'Invalid market. Current supported markets are: \n{MARKET_NAME_TO_INDEX}')
        int_direction = position_direction(
            direction=direction
        )
        open_position_response = await send_open_position(
            client=self.connector,
            wallet=self.wallet,
            user_positions=self.user_positions,
            quote_asset_amount=quote_amount,
            market_index=market_index,
            direction=int_direction,
            limit_price=0,
            commitment=self.commitment
        )
        return open_position_response

    async def close_position(
            self, market: str
    ) -> RPCResponse:
        """Completely close a position.

        :param market: The market in which the position is held."""
        if market in MARKET_NAME_TO_INDEX:
            market_index = MARKET_NAME_TO_INDEX.index(market)
        else:
            raise Exception(f'Invalid market. Current supported markets are: \n{MARKET_NAME_TO_INDEX}')
        close_position_response = await send_close_position(
            client=self.connector,
            wallet=self.wallet,
            market_index=market_index,
            user_positions=self.user_positions,
            commitment=self.commitment
        )
        return close_position_response

    async def deposit_collateral(
            self, amount: Number
    ) -> RPCResponse:
        """Deposit collateral."""
        deposit_collateral_response = await send_deposit_collateral(
            client=self.connector,
            wallet=self.wallet,
            user_positions=self.user_positions,
            amount=amount,
            user_collateral_account=self.user_collateral_account,
            commitment=self.commitment
        )
        return deposit_collateral_response

    async def withdraw_collateral(
            self, amount: Number
    ) -> RPCResponse:
        """Withdraw collateral."""
        withdraw_collateral_response = await send_withdraw_collateral(
            client=self.connector,
            wallet=self.wallet,
            user_positions=self.user_positions,
            amount=amount,
            user_collateral_account=self.user_collateral_account,
            commitment=self.commitment
        )
        return withdraw_collateral_response

    def to_dict(self) -> dict:
        """For pretty printing."""
        my_dict = {
            'connector': {
                'endpoint': self.endpoint,
                'commitment': self.commitment
            },
            'wallet_address': self.wallet.public_key.__str__(),
            'user_account_address': self.user_account.__str__(),
            'user_positions_address': self.user_positions.__str__(),
            'user_collateral_account': self.user_collateral_account.__str__()
        }
        return my_dict

    def __str__(self):
        my_dict = self.to_dict()
        return json.dumps(my_dict, sort_keys=False, indent=4)
