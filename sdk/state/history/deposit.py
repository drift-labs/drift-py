"""This module models a deposit-history buffer account."""
from construct import Int8ul, Int64ul, Int64sl, Struct, Container, Padding
from typing import List
from solana.publickey import PublicKey
from sdk.layouts import Int128ul, PUBLIC_KEY_LAYOUT
from sdk.state.core import ElementCore
from sdk.state.history.core import HistoryCore


class DepositRecord(ElementCore):
    """Object to model a single deposit-record."""
    layout = Struct(
        'ts' / Int64sl,
        'record_id' / Int128ul,
        'user_authority' / PUBLIC_KEY_LAYOUT,
        'user' / PUBLIC_KEY_LAYOUT,
        'direction' / Int8ul,
        'collateral_before' / Int128ul,
        'cumulative_deposits_before' / Int128ul,
        'amount' / Int64ul
    )

    def __init__(
            self, ts: int, record_id: int, user_authority: PublicKey, user: PublicKey, direction: int,
            collateral_before: int, cumulative_deposits_before: int
    ) -> None:
        self.ts = ts
        self.record_id = record_id
        self.user_authority = user_authority
        self.user = user
        self.direction = direction
        self.collateral_before = collateral_before
        self.cumulative_deposits_before = cumulative_deposits_before

    @classmethod
    def from_container(cls, container: Container):
        """Create a curve-record from a container."""
        deposit_record = cls(
            ts=container.ts,
            record_id=container.record_id,
            user_authority=container.user_authority,
            user=container.user,
            direction=container.direction,
            collateral_before=container.collateral_before,
            cumulative_deposits_before=container.cumulative_deposits_before
        )
        return deposit_record

    def to_dict(self) -> dict:
        """For pretty printing."""
        my_dict = {
            'ts': self.ts,
            'record_id': self.record_id,
            'user_authority': self.user_authority.__str__(),
            'user': self.user.__str__(),
            'direction': self.direction,
            'collateral_before': self.collateral_before,
            'cumulative_deposits_before': self.cumulative_deposits_before
        }
        return my_dict


class DepositHistory(HistoryCore):
    """Object to model a deposit-history buffer account."""
    layout = Struct(
        Padding(8),
        'head' / Int64ul,
        'records' / DepositRecord.layout[1024]
    )

    def __init__(self, head: int, records: List[DepositRecord]) -> None:
        self.head = head
        self.records = records

    @classmethod
    def from_container(cls, container: Container):
        """Create a curve-history account from a container."""
        history = cls(
            head=container.head,
            records=[DepositRecord.from_container(c) for c in container.records]
        )
        return history