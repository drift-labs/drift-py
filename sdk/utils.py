"""General utility."""
from typing import Literal, Optional
from solana.publickey import PublicKey
from solana.rpc.api import Client
from sdk.constants import *


def get_user_account_address(authority: PublicKey) -> PublicKey:
    """Get a user-account address from a personal wallet-address."""
    user_account_address = PublicKey.find_program_address(
        seeds=[
            'user'.encode('utf-8'),
            authority.__bytes__()
        ],
        program_id=CLEARING_HOUSE_ADDRESSES.program
    )[0]
    return user_account_address


def get_clearing_house_state_address() -> PublicKey:
    """Get the Drift clearing-house address."""
    clearing_house_state_address_tuple = PublicKey.find_program_address(
        seeds=[
            'clearing_house'.encode('utf-8')
        ],
        program_id=CLEARING_HOUSE_ADDRESSES.program
    )
    clearing_house_state_address = clearing_house_state_address_tuple[0]
    return clearing_house_state_address


def position_direction(direction: Literal['long', 'short']) -> int:
    """Get an integer from a position direction."""
    position_direction_to_int = {
        'long': 0,
        'short': 1
    }
    int_direction = position_direction_to_int[direction]
    return int_direction


def find_associated_token_address(authority: PublicKey, token_mint_address: PublicKey) -> PublicKey:
    """Get an associated token address."""
    associated_token_address = PublicKey.find_program_address(
        seeds=[
            authority.__bytes__(),
            TOKEN_PROGRAM_ID.__bytes__(),
            token_mint_address.__bytes__()
        ],
        program_id=ASSOCIATED_TOKEN_PROGRAM_ID
    )[0]
    return associated_token_address


def get_collateral_account_address(authority: PublicKey) -> PublicKey:
    """Get collateral account address."""
    collateral_account_address = find_associated_token_address(
        authority=authority,
        token_mint_address=USDC_MINT
    )
    return collateral_account_address


def get_market_index(symbol: str) -> Optional[int]:
    """Get the index of a market from it's symbol."""
    market_index = MARKET_SYMBOL_TO_INDEX.get(symbol)
    if market_index is not None:
        return market_index
    else:
        raise Exception('Invalid market symbol.')



