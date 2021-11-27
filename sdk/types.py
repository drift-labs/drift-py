from typing import NamedTuple
from solana.publickey import PublicKey


class TradeSide(NamedTuple):
    none: int
    sell: int
    buy: int


class HistoryAddresses(NamedTuple):
    curve: PublicKey
    deposit: PublicKey
    funding_payment: PublicKey
    funding_rate: PublicKey
    liquidation: PublicKey
    trade: PublicKey


class ClearingHouseAddresses(NamedTuple):
    admin: PublicKey
    state: PublicKey
    program: PublicKey
    markets: PublicKey
    collateral_mint: PublicKey
    collateral_vault: PublicKey
    collateral_vault_authority: PublicKey
    insurance_vault: PublicKey
    insurance_vault_authority: PublicKey
    history: HistoryAddresses
    white_list_mint: PublicKey
    discount_mint: PublicKey


class MarketBasics(NamedTuple):
    name: str
    base_asset_symbol: str
    market_index: int
    devnet_pyth_oracle: PublicKey
    mainnet_pyth_oracle: PublicKey


class ManagePositionOptionalAccounts(NamedTuple):
    discount_token: bool
    referrer: bool