"""Constants relating to the drift-protocol."""
from typing import NamedTuple, Union

from solana.rpc.types import TxOpts
from solana.publickey import PublicKey

from solana.rpc.api import Commitment


Number = Union[int, float]


class HistoryAddresses(NamedTuple):
    """History addresses."""
    curve: PublicKey
    deposit: PublicKey
    funding_payment: PublicKey
    funding_rate: PublicKey
    liquidation: PublicKey
    trade: PublicKey


class ClearingHouseAddresses(NamedTuple):
    """Clearing-house addresses."""
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
    """Market basics."""
    name: str
    base_asset_symbol: str
    market_index: int
    devnet_pyth_oracle: PublicKey
    mainnet_pyth_oracle: PublicKey


class ManagePositionOptionalAccounts(NamedTuple):
    """Manage-positional-optional-accounts."""
    discount_token: bool
    referrer: bool


CURRENT_MARKETS = [
    MarketBasics(
        name='SOL-PERP',
        base_asset_symbol='SOL',
        market_index=0,
        devnet_pyth_oracle=PublicKey('J83w4HKfqxwcq3BEMMkPFSppX3gqekLyLJBexebFVkix'),
        mainnet_pyth_oracle=PublicKey('H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG')
    ),
    MarketBasics(
        name='BTC-PERP',
        base_asset_symbol='BTC',
        market_index=1,
        devnet_pyth_oracle=PublicKey('HovQMDrbAgAYPCmHVSrezcSmkMtXSSUsLDFANExrZh2J'),
        mainnet_pyth_oracle=PublicKey('GVXRSBjFk6e6J3NbVPXohDJetcTjaeeuykUpbQF8UoMU')
    ),
    MarketBasics(
        name='ETH-PERP',
        base_asset_symbol='ETH',
        market_index=2,
        devnet_pyth_oracle=PublicKey('EdVCmQ9FSPcVe5YySXDPCRmc8aDQLKJ9xvYBMZPie1Vw'),
        mainnet_pyth_oracle=PublicKey('JBu1AL4obBcCMqKBBxhpWCNUt136ijcuMZLFvTP7iWdB')
    ),
    MarketBasics(
        name='LUNA-PERP',
        base_asset_symbol='LUNA',
        market_index=3,
        devnet_pyth_oracle=PublicKey('8PugCXTAHLM9kfLSQWe2njE5pzAgUdpPk3Nx5zSm7BD3'),
        mainnet_pyth_oracle=PublicKey('5bmWuR1dgP4avtGYMNKLuxumZTVKGgoN2BCMXWDNL9nY')
    ),
    MarketBasics(
        name='AVAX-PERP',
        base_asset_symbol='AVAX',
        market_index=4,
        devnet_pyth_oracle=PublicKey('FVb5h1VmHPfVb1RfqZckchq18GxRv4iKt8T4eVTQAqdz'),
        mainnet_pyth_oracle=PublicKey('Ax9ujW5B9oqcv59N8m6f1BpTBq2rGeGaBcpKjC5UYsXU')
    ),
    MarketBasics(
        name='BNB-PERP',
        base_asset_symbol='BNB',
        market_index=5,
        devnet_pyth_oracle=PublicKey('GwzBgrXb4PG59zjce24SF2b9JXbLEjJJTBkmytuEZj1b'),
        mainnet_pyth_oracle=PublicKey('4CkQJBxhU8EZ2UjhigbtdaPbpTe6mqf811fipYBFbSYN')
    )
]

NUMBER_OF_CURRENT_MARKETS = len(CURRENT_MARKETS)
MARKET_INDEX_TO_SYMBOL = [market.name for market in CURRENT_MARKETS]
MARKET_SYMBOL_TO_INDEX = {symbol: index for (index, symbol) in enumerate(MARKET_INDEX_TO_SYMBOL)}
print(MARKET_SYMBOL_TO_INDEX)

USDC_MINT = PublicKey('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v')

CLEARING_HOUSE_ADDRESSES = ClearingHouseAddresses(
    admin=PublicKey('4eRo4naR84BadrPAuJ2WazMvLKvo9iCr2RGrF9NwAgP8'),
    state=PublicKey('FExhvPycCCwYnZGeDsVtLhpEQ3yEkVY2k1HuPyfLj91L'),
    program=PublicKey('dammHkt7jmytvbS3nHTxQNEcP59aE57nxwV21YdqEDN'),
    markets=PublicKey('773hq3SbGPKVj93TXi5qV5CREuhxobywfALjS3XVHhLH'),
    collateral_mint=USDC_MINT,
    collateral_vault=PublicKey('6W9yiHDCW9EpropkFV8R3rPiL8LVWUHSiys3YeW6AT6S'),
    collateral_vault_authority=PublicKey('CU4eFxpyCGNDEXN27Jonn7RfgwBt3cnp7TcTrJF6EW9Q'),
    insurance_vault=PublicKey('Bzjkrm1bFwVXUaV9HTnwxFrPtNso7dnwPQamhqSxtuhZ'),
    insurance_vault_authority=PublicKey('DboRdMqoF1UMKgsqj5F6EN3pUJFDr3phTkA4zkzMAq4B'),
    history=HistoryAddresses(
        curve=PublicKey('2tjmvkzxJsrfRLiaxFfKt6FXG1vFhsBZ1wBM3jY3t8mR'),
        deposit=PublicKey('C7rF2Qy2rnDGQLRijBRRArJyaeuQcFi81BXDrUCQ45ya'),
        funding_payment=PublicKey('895iPhzwT2tBufLnRpYtBG3gif1HDDUfpH2AqbS5joo4'),
        funding_rate=PublicKey('BWiJLMbmrwfqHVpcPJa8715XamNyNYamDDKQVQMnduEC'),
        liquidation=PublicKey('CSFaaf8yVoTx6NcXUKtNPYAewv76CH2jATqSVRBvUWKM'),
        trade=PublicKey('FCuCXEoQppoaCYdttA7rK3HNQfYkTNEGpwuBESzYcENp')
    ),
    discount_mint=PublicKey('EGfR6MbHk3P5kksmWjZG8sxY3GNnK7TBvCLYXEoNvB7G'),
    white_list_mint=PublicKey('EGeMJgLaAHkBQ1UaLEBhzscfFsPqWgyaw9Lc4gMav186')
)

MAINNET_ENDPOINT = 'https://api.mainnet-beta.solana.com'
SERUM_ENDPOINT = 'https://solana-api.projectserum.com'


class TradeSide(NamedTuple):
    none: int
    sell: int
    buy: int


TRADE_SIDE = TradeSide(
    none=0,
    buy=1,
    sell=2
)


class InstructionTag(NamedTuple):
    """Instructino tag."""
    initialize: int
    initialize_history: int
    initialize_market: int
    deposit_collateral: int
    withdraw_collateral: int
    open_position: int


INSTRUCTION_TAG = InstructionTag(
    initialize=0,
    initialize_history=1,
    initialize_market=2,
    deposit_collateral=3,
    withdraw_collateral=4,
    open_position=5
)


MAX_LEVERAGE = 5
FULL_LIQUIDATION_RATIO = 500
PARTIAL_LIQUIDATION_RATIO = 625

QUOTE_PRECISION = 1e6
MARK_PRICE_PRECISION = 1e10
FUNDING_PAYMENT_PRECISION = 1e4
PEG_PRECISION = 1e3
AMM_RESERVE_PRECISION = 1e13
MARGIN_PRECISION = 1e4

PRICE_TO_PEG_PRECISION_RATIO = int(MARK_PRICE_PRECISION / PEG_PRECISION)
PRICE_TO_PEG_QUOTE_PRECISION_RATIO = int(MARK_PRICE_PRECISION / QUOTE_PRECISION)
AMM_TO_QUOTE_PRECISION_RATIO = int(AMM_RESERVE_PRECISION / QUOTE_PRECISION)
PRICE_TO_QUOTE_PRECISION_RATIO = int(MARK_PRICE_PRECISION / QUOTE_PRECISION)
QUOTE_TO_BASE_AMT_FUNDING_PRECISION = \
    int(AMM_RESERVE_PRECISION * MARK_PRICE_PRECISION * FUNDING_PAYMENT_PRECISION) / QUOTE_PRECISION

SHARE_OF_FEES_ALLOCATED_TO_CLEARING_HOUSE_NUMERATOR = 1
SHARE_OF_FEES_ALLOCATED_TO_CLEARING_HOUSE_DENOMINATOR = 2
UPDATE_K_ALLOWED_PRICE_RANGE_CHANGE = int(MARK_PRICE_PRECISION / 10)


DEFAULT_FEE_NUMERATOR = 10
DEFAULT_FEE_DENOMINATOR = 10000

DEFAULT_DISCOUNT_TOKEN_FIRST_TIER_MINIMUM_BALANCE = 1e12
DEFAULT_DISCOUNT_TOKEN_FIRST_TIER_DISCOUNT_NUMERATOR = 20
DEFAULT_DISCOUNT_TOKEN_FIRST_TIER_DISCOUNT_DENOMINATOR = 100

DEFAULT_DISCOUNT_TOKEN_SECOND_TIER_MINIMUM_BALANCE = 1e11
DEFAULT_DISCOUNT_TOKEN_SECOND_TIER_DISCOUNT_NUMERATOR = 15
DEFAULT_DISCOUNT_TOKEN_SECOND_TIER_DISCOUNT_DENOMINATOR = 100

DEFAULT_DISCOUNT_TOKEN_THIRD_TIER_MINIMUM_BALANCE = 1e10
DEFAULT_DISCOUNT_TOKEN_THIRD_TIER_DISCOUNT_NUMERATOR = 10
DEFAULT_DISCOUNT_TOKEN_THIRD_TIER_DISCOUNT_DENOMINATOR = 100

DEFAULT_DISCOUNT_TOKEN_FOURTH_TIER_MINIMUM_BALANCE = 1e9
DEFAULT_DISCOUNT_TOKEN_FOURTH_TIER_DISCOUNT_NUMERATOR = 5
DEFAULT_DISCOUNT_TOKEN_FOURTH_TIER_DISCOUNT_DENOMINATOR = 100

DEFAULT_REFERRER_REWARD_NUMERATOR = 5
DEFAULT_REFERRER_REWARD_DENOMINATOR = 100

DEFAULT_REFEREE_DISCOUNT_NUMERATOR = 5
DEFAULT_REFEREE_DISCOUNT_DENOMINATOR = 100

ORACLE_INDEX_TO_SOURCE = {
    0: 'Pyth',
    1: 'SwitchBoard'
}

TOKEN_PROGRAM_ID = PublicKey('TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA')
ASSOCIATED_TOKEN_PROGRAM_ID = PublicKey('ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL')

DEFAULT_MANAGE_POSITION_OPTIONAL_ACCOUNTS = ManagePositionOptionalAccounts(
    discount_token=False,
    referrer=False
)

# commitments
PROCESSED = Commitment('processed')
CONFIRMED = Commitment('confirmed')
FINALIZED = Commitment('finalized')

