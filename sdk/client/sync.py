import base58
import json
from typing import List, Literal
from construct import Int8ul

from solana.publickey import PublicKey
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.types import RPCResponse

from sdk.constants import *
from sdk.state.all import *
from sdk.calls.sync import *
from sdk.sends.sync import *
from sdk.utils import get_user_account_address, position_direction, get_collateral_account_address


class DriftClient:

    def __init__(self, connector: Client, endpoint: str, commitment: Literal['processed', 'confirmed', 'finalized'],
                 wallet: Keypair, user_account: PublicKey, user_positions: PublicKey,
                 user_collateral_account: PublicKey) -> None:
        self.connector = connector
        self.endpoint = endpoint
        self.commitment = commitment
        self.wallet = wallet
        self.user_account = user_account
        self.user_positions = user_positions
        self.user_collateral_account = user_collateral_account

    @classmethod
    def create(cls, private_key: str or List[int], endpoint: str = MAINNET_ENDPOINT,
               commitment: str = 'confirmed'):
        if type(private_key) == str:
            private_key_bytes = base58.b58decode(private_key.encode('utf-8'))
        elif type(private_key) == list:
            private_key_bytes = Int8ul[64].build(private_key)
        else:
            raise Exception('Invalid private key.')

        wallet_keypair = Keypair.from_secret_key(
            secret_key=private_key_bytes
        )
        connector = Client(
            endpoint=endpoint,
            commitment=commitment
        )
        user_account_address = get_user_account_address(
            authority=wallet_keypair.public_key
        )
        user_account = call_user_account(
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

    def get_clearing_house(self) -> ClearingHouseState:
        clearing_house = call_clearing_house(
            client=self.connector,
            address=CLEARING_HOUSE_ADDRESSES.state
        )
        return clearing_house

    def get_user_account(self) -> UserAccount:
        user_account = call_user_account(
            client=self.connector,
            address=self.user_account
        )
        return user_account

    def get_positions(self) -> UserPositions:
        user_positions = call_positions_account(
            client=self.connector,
            address=self.user_positions
        )
        return user_positions

    def get_market(self) -> DriftMarket:
        pass

    def open_position(self, market: str, direction: Literal['long', 'short'], quote_amount: int) -> RPCResponse:
        if market in MARKET_NAME_TO_INDEX:
            market_index = MARKET_NAME_TO_INDEX.index(market)
        else:
            raise Exception(f'Invalid market. Current supported markets are: \n{MARKET_NAME_TO_INDEX}')
        int_direction = position_direction(
            direction=direction
        )
        open_position_response = send_open_position(
            client=self.connector,
            wallet=self.wallet,
            user_positions=self.user_positions,
            quote_asset_amount=quote_amount,
            market_index=market_index,
            direction=int_direction,
            limit_price=0
        )
        return open_position_response

    def deposit_collateral(self, quote_amount: int) -> RPCResponse:
        deposit_collateral_response = send_deposit_collateral(
            client=self.connector,
            wallet=self.wallet,
            user_positions=self.user_positions,
            amount=quote_amount,
            user_collateral_account=self.user_collateral_account
        )
        return deposit_collateral_response

    def to_dict(self) -> dict:
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