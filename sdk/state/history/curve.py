from construct import Int64ul, Struct, Container, Padding
from typing import List
from drift.layouts import Int128ul, Int128sl
from drift.state.core import ElementCore
from drift.state.history.core import HistoryCore


class CurveRecord(ElementCore):
    layout = Struct(
        'ts' / Int64ul,
        'record_id' / Int128ul,
        'market_index' / Int64ul,
        'peg_multiplier_before' / Int128ul,
        'base_asset_reserve_before' / Int128ul,
        'quote_asset_reserve_before' / Int128ul,
        'sqrt_k_before' / Int128ul,
        'peg_multiplier_after' / Int128ul,
        'base_asset_reserve_after' / Int128ul,
        'quote_asset_reserve_after' / Int128ul,
        'sqrt_k_after' / Int128ul,
        'base_asset_amount_long' / Int128ul,
        'base_asset_amount_short' / Int128ul,
        'base_asset_amount' / Int128ul,
        'open_interest' / Int128ul,
        'total_fee' / Int128ul,
        'total_fee_minus_distributions' / Int128ul,
        'adjustment_cost' / Int128sl
    )

    def __init__(self, ts: int, record_id: int, market_index: int, peg_multiplier_before: int,
                 base_asset_reserve_before: int, quote_asset_reserve_before: int, sqrt_k_before: int,
                 peg_multiplier_after: int, base_asset_reserve_after: int, quote_asset_reserve_after: int,
                 sqrt_k_after: int, base_asset_amount_long: int, base_asset_amount_short: int, base_asset_amount: int,
                 open_interest: int, total_fee: int, total_fee_minus_distributions: int, adjustment_cost: int) -> None:
        self.ts = ts
        self.record_id = record_id
        self.market_index = market_index
        self.peg_multiplier_before = peg_multiplier_before
        self.base_asset_reserve_before = base_asset_reserve_before
        self.quote_asset_reserve_before = quote_asset_reserve_before
        self.sqrt_k_before = sqrt_k_before
        self.peg_multiplier_after = peg_multiplier_after
        self.base_asset_reserve_after = base_asset_reserve_after
        self.quote_asset_reserve_after = quote_asset_reserve_after
        self.sqrt_k_after = sqrt_k_after
        self.base_asset_amount_long = base_asset_amount_long
        self.base_asset_amount_short = base_asset_amount_short
        self.base_asset_amount = base_asset_amount
        self.open_interest = open_interest
        self.total_fee = total_fee
        self.total_fee_minus_distributions = total_fee_minus_distributions
        self.adjustment_cost = adjustment_cost

    @classmethod
    def from_container(cls, container: Container):
        curve_record = cls(
            ts=container.ts,
            record_id=container.record_id,
            market_index=container.market_index,
            peg_multiplier_before=container.peg_multiplier_before,
            base_asset_reserve_before=container.base_asset_reserve_before,
            quote_asset_reserve_before=container.quote_asset_reserve_before,
            sqrt_k_before=container.sqrt_k_before,
            peg_multiplier_after=container.peg_multiplier_after,
            base_asset_reserve_after=container.base_asset_reserve_after,
            quote_asset_reserve_after=container.quote_asset_reserve_after,
            sqrt_k_after=container.sqrt_k_after,
            base_asset_amount_long=container.base_asset_amount_long,
            base_asset_amount_short=container.base_asset_amount_short,
            base_asset_amount=container.base_asset_amount,
            open_interest=container.open_interest,
            total_fee=container.total_fee,
            total_fee_minus_distributions=container.total_fee_minus_distributions,
            adjustment_cost=container.adjustment_cost
        )
        return curve_record


    def to_dict(self) -> dict:
        my_dict = {
            'ts': self.ts,
            'record_id': self.record_id,
            'market_index': self.market_index,
            'peg_multiplier_before': self.peg_multiplier_before,
            'base_asset_reserve_before': self.base_asset_reserve_before,
            'quote_asset_reserve_before': self.quote_asset_reserve_before,
            'sqrt_k_before': self.sqrt_k_before,
            'peg_multiplier_after': self.peg_multiplier_after,
            'base_asset_reserve_after': self.base_asset_reserve_after,
            'quote_asset_reserve_after': self.quote_asset_reserve_after,
            'sqrt_k_after': self.sqrt_k_after,
            'base_asset_amount_long': self.base_asset_amount_long,
            'base_asset_amount_short': self.base_asset_amount_short,
            'base_asset_amount': self.base_asset_amount,
            'open_interest': self.open_interest,
            'total_fee': self.total_fee,
            'total_fee_minus_distributions': self.total_fee_minus_distributions,
            'adjustment_cost': self.adjustment_cost
        }
        return my_dict


class CurveHistory(HistoryCore):
    layout = Struct(
        Padding(8),
        'head' / Int64ul,
        'records' / CurveRecord.layout[1024]
    )

    def __init__(self, head: int, records: List[CurveRecord]) -> None:
        self.head = head
        self.records = records

    @classmethod
    def from_container(cls, container: Container):
        history = cls(
            head=container.head,
            records=[CurveRecord.from_container(c) for c in container.records]
        )
        return history