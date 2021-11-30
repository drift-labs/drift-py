from typing import List
from construct import Struct, Padding, Int8ul, Flag, Int64ul, Int64sl, Container, GreedyRange
from solana.publickey import PublicKey
from sdk.layouts import PUBLIC_KEY_LAYOUT, Int128ul, Int128sl
from sdk.state.core import ElementCore
from sdk.constants import *


class DriftAmm(ElementCore):
    layout = Struct(
        'oracle' / PUBLIC_KEY_LAYOUT,
        'oracle_source' / Int8ul,
        'base_asset_reserve' / Int128ul,
        'quote_asset_reserve' / Int128ul,
        'cumulative_repeg_rebate_long' / Int128ul,
        'cumulative_repeg_rebate_short' / Int128ul,
        'cumulative_funding_rate_long' / Int128sl,
        'cumulative_funding_rate_short' / Int128sl,
        'last_funding_rate' / Int128sl,
        'last_funding_rate_ts' / Int64sl,
        'funding_period' / Int64sl,
        'last_oracle_mark_spread_twap' / Int128sl,
        'last_mark_price_twap' / Int128ul,
        'last_mark_price_twap_ts' / Int64sl,
        'sqrt_k' / Int128ul,
        'peg_multiplier' / Int128ul,
        'total_fee' / Int128ul,
        'total_fee_minus_distributions' / Int128ul,
        'total_fee_withdrawn' / Int128ul,
        'minimum_trade_size' / Int128ul,
        Padding(80)
    )

    def __init__(self, oracle: PublicKey, oracle_source: str, base_asset_reserve: int, quote_asset_reserve: int,
                 cumulative_repeg_rebate_long: int, cumulative_repeg_rebate_short: int,
                 cumulative_funding_rate_long: int, cumulative_funding_rate_short: int, last_funding_rate: int,
                 last_funding_rate_ts: int, funding_period: int, last_oracle_mark_spread_twap: int,
                 last_mark_price_twap: int, last_mark_price_twap_ts: int, sqrt_k: int, peg_multiplier: int,
                 total_fee: int, total_fee_minus_distributions: int, total_fee_withdrawn: int,
                 minimum_trade_size: int) -> None:
        self.oracle = oracle
        self.oracle_source = oracle_source
        self.base_asset_reserve = base_asset_reserve
        self.quote_asset_reserve = quote_asset_reserve
        self.cumulative_repeg_rebate_long = cumulative_repeg_rebate_long
        self.cumulative_repeg_rebate_short = cumulative_repeg_rebate_short
        self.cumulative_funding_rate_long = cumulative_funding_rate_long
        self.cumulative_funding_rate_short = cumulative_funding_rate_short
        self.last_funding_rate = last_funding_rate
        self.last_funding_rate_ts = last_funding_rate_ts
        self.funding_period = funding_period
        self.last_oracle_mark_spread_twap = last_oracle_mark_spread_twap
        self.last_mark_price_twap = last_mark_price_twap
        self.last_mark_price_twap_ts = last_mark_price_twap_ts
        self.sqrt_k = sqrt_k
        self.peg_multiplier = peg_multiplier
        self.total_fee = total_fee
        self.total_fee_minus_distributions = total_fee_minus_distributions
        self.total_fee_withdrawn = total_fee_withdrawn
        self.minimum_trade_size = minimum_trade_size

    @classmethod
    def from_container(cls, container: Container):
        amm = cls(
            oracle=PublicKey(container.oracle),
            oracle_source=ORACLE_INDEX_TO_SOURCE[container.oracle_source],
            base_asset_reserve=container.base_asset_reserve,
            quote_asset_reserve=container.quote_asset_reserve,
            cumulative_repeg_rebate_long=container.cumulative_repeg_rebate_long,
            cumulative_repeg_rebate_short=container.cumulative_repeg_rebate_short,
            cumulative_funding_rate_long=container.cumulative_funding_rate_long,
            cumulative_funding_rate_short=container.cumulative_funding_rate_short,
            last_funding_rate=container.last_funding_rate,
            last_funding_rate_ts=container.last_funding_rate_ts,
            funding_period=container.funding_period,
            last_oracle_mark_spread_twap=container.last_oracle_mark_spread_twap,
            last_mark_price_twap=container.last_mark_price_twap,
            last_mark_price_twap_ts=container.last_mark_price_twap_ts,
            sqrt_k=container.sqrt_k,
            peg_multiplier=container.peg_multiplier,
            total_fee=container.total_fee,
            total_fee_minus_distributions=container.total_fee_minus_distributions,
            total_fee_withdrawn=container.total_fee_withdrawn,
            minimum_trade_size=container.minimum_trade_size
        )
        return amm

    def to_dict(self) -> dict:
        my_dict = {
            'oracle': self.oracle.__str__(),
            'oracle_source': self.oracle_source,
            'base_asset_reserve': self.base_asset_reserve,
            'quote_asset_reserve': self.quote_asset_reserve,
            'cumulative_repeg_rebate_long': self.cumulative_repeg_rebate_long,
            'cumulative_repeg_rebate_short': self.cumulative_repeg_rebate_short,
            'cumulative_funding_rate_long': self.cumulative_funding_rate_long,
            'cumulative_funding_rate_short': self.cumulative_funding_rate_short,
            'last_funding_rate': self.last_funding_rate,
            'last_funding_rate_ts': self.last_funding_rate_ts,
            'funding_period': self.funding_period,
            'last_oracle-mark_spread_twap': self.last_oracle_mark_spread_twap,
            'last_mark_price_twap': self.last_mark_price_twap,
            'last_mark_price_twap_ts': self.last_mark_price_twap_ts,
            'sqrt_k': self.sqrt_k,
            'peg_multiplier': self.peg_multiplier,
            'total_fee': self.total_fee,
            'total_fee_minus_distributions': self.total_fee_minus_distributions,
            'total_fee_withdrawn': self.total_fee_withdrawn,
            'minimum_trade_size': self.minimum_trade_size
        }
        return my_dict

    def get_mark_price(self) -> float:
        unpegged_price = self.quote_asset_reserve / self.base_asset_reserve
        pegged_price = unpegged_price * self.peg_multiplier
        mark_price = pegged_price * PRICE_TO_PEG_PRECISION_RATIO / MARK_PRICE_PRECISION
        return mark_price


class DriftMarket(ElementCore):
    layout = Struct(
        'initialized' / Flag,
        'base_asset_amount_long' / Int128sl,
        'base_asset_amount_short' / Int128sl,
        'base_asset_amount' / Int128sl,
        'open_interest' / Int128ul,
        'amm' / DriftAmm.layout,
        Padding(80)
    )

    def __init__(self, initialized: bool, base_asset_amount_long: int, base_asset_amount_short: int,
                 base_asset_amount: int, open_interest: int, amm: DriftAmm) -> None:
        self.initialized = initialized
        self.base_asset_amount_long = base_asset_amount_long
        self.base_asset_amount_short = base_asset_amount_short
        self.base_asset_amount = base_asset_amount
        self.open_interest = open_interest
        self.amm = amm

    @classmethod
    def from_container(cls, container: Container):
        drift_market = cls(
            initialized=container.initialized,
            base_asset_amount_long=container.base_asset_amount_long,
            base_asset_amount_short=container.base_asset_amount_short,
            base_asset_amount=container.base_asset_amount,
            open_interest=container.open_interest,
            amm=DriftAmm.from_container(container=container.amm)
        )
        return drift_market

    def to_dict(self) -> dict:
        my_dict = {
            'initialized': self.initialized,
            'base_asset_amount_long': self.base_asset_amount_long,
            'base_asset_amount_short': self.base_asset_amount_short,
            'base_asset_amount': self.base_asset_amount,
            'open_interest': self.open_interest,
            'amm': self.amm.to_dict()
        }
        return my_dict


class DriftMarkets(ElementCore):
    layout = Struct(
        Padding(8),
        'markets' / DriftMarket.layout[NUMBER_OF_CURRENT_MARKETS]
    )

    def __init__(self, markets: List[DriftMarket]) -> None:
        self.markets = markets

    @classmethod
    def from_container(cls, container: Container):
        drift_markets = cls(
            markets=[DriftMarket.from_container(dm) for dm in container.markets]
        )
        return drift_markets

    def to_dict(self) -> dict:
        my_dict = [market.to_dict() for market in self.markets]
        return my_dict

