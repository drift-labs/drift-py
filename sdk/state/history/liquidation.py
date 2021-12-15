"""This module models a liquidation-history buffer account."""
from construct import Int64sl, Struct, Container, Flag, Padding, Int64ul
from typing import List
from solana.publickey import PublicKey
from sdk.layouts import Int128ul, Int128sl, PUBLIC_KEY_LAYOUT
from sdk.state.core import ElementCore
from sdk.state.history.core import HistoryCore


class LiquidationRecord(ElementCore):
    """Object to model a single liquidation record."""
    layout = Struct(
        'ts' / Int64sl,
        'record_id' / Int128ul,
        'user_authority' / PUBLIC_KEY_LAYOUT,
        'user' / PUBLIC_KEY_LAYOUT,
        'partial' / Flag,
        'base_asset_value' / Int128ul,
        'base_asset_value_closed' / Int128ul,
        'liquidation_fee' / Int128ul,
        'fee_to_liquidator' / Int128ul,
        'fee_to_insurance_fund' / Int128ul,
        'liquidator' / PUBLIC_KEY_LAYOUT,
        'total_collateral' / Int128ul,
        'collateral' / Int128ul,
        'unrealized_pnl' / Int128sl,
        'margin_ratio' / Int128ul
    )

    def __init__(
            self, ts: int, record_id: int, user_authority: PublicKey, user: PublicKey, partial: bool,
            base_asset_value: int, base_asset_value_closed: int, liquidation_fee: int,
            fee_to_liquidator: int, fee_to_insurance_fund: int, liquidator: PublicKey, total_collateral: int,
            collateral: int, unrealized_pnl: int, margin_ratio: int
    ) -> None:
        self.ts = ts
        self.record_id = record_id
        self.user_authority = user_authority
        self.user = user
        self.partial = partial
        self.base_asset_value = base_asset_value
        self.base_asset_value_closed = base_asset_value_closed
        self.liquidation_fee = liquidation_fee
        self.fee_to_liquidator = fee_to_liquidator
        self.fee_to_insurance_fund = fee_to_insurance_fund
        self.liquidator = liquidator
        self.total_collateral = total_collateral
        self.collateral = collateral
        self.unrealized_pnl = unrealized_pnl
        self.margin_ratio = margin_ratio

    @classmethod
    def from_container(cls, container: Container):
        """Create a liquidation-record from a container."""
        liquidation_record = cls(
            ts=container.ts,
            record_id=container.record_id,
            user_authority=PublicKey(container.user_authority),
            user=PublicKey(contianer.user),
            partial=container.partial,
            base_asset_value=container.base_asset_value,
            base_asset_value_closed=container.base_asset_value_closed,
            liquidation_fee=container.liquidation_fee,
            fee_to_liquidator=container.fee_to_liquidator,
            fee_to_insurance_fund=container.fee_to_insurance_fund,
            liquidator=PublicKey(container.liquidator),
            total_collateral=container.total_collateral,
            collateral=container.collateral,
            unrealized_pnl=container.unrealized_pnl,
            margin_ratio=container.margin_ratio
        )
        return liquidation_record

    def to_dict(self) -> dict:
        """For pretty printing."""
        my_dict = {
            'ts': self.ts,
            'record_id': self.record_id,
            'user_authority': self.user_authority.__str__(),
            'user': self.user.__str__(),
            'partial': self.partial,
            'base_asset_value': self.base_asset_value,
            'base_asset_value_closed': self.base_asset_value_closed,
            'liquidation_fee': self.liquidation_fee,
            'fee_to_liquidator': self.fee_to_liquidator,
            'fee_to_insurance_fund': self.fee_to_insurance_fund,
            'liquidator': self.liquidator.__str__(),
            'total_collateral': self.total_collateral,
            'unrealized_pnl': self.unrealized_pnl,
            'margin_ratio': self.margin_ratio
        }
        return my_dict


class LiquidationHistory(HistoryCore):
    """Object to model a liquidation-history buffer account."""
    layout = Struct(
        Padding(8),
        'head' / Int64ul,
        'records' / LiquidationRecord.layout[1024]
    )

    def __init__(self, head: int, records: List[LiquidationRecord]) -> None:
        self.head = head
        self.records = records

    @classmethod
    def from_container(cls, container: Container):
        """Create a liquidation-history account from a container."""
        history = cls(
            head=container.head,
            records=[LiquidationRecord.from_container(c) for c in container.records]
        )
        return history
