"""This module models an open-position instruction."""
from construct import Struct, Int64ul, Int64sl, Flag, PaddedString, Int64ub, Bytes, Padding
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from sdk.instructions.core import InstructionCore
from sdk.layouts import (
    Int128ul, Int128sl, POSITION_DIRECTION_LAYOUT, MANAGE_POSITION_OPTIONAL_ACCOUNTS_LAYOUT, Int8ul,
    INSTRUCTION_NAME_LAYOUT
)
from sdk.constants import (
    DEFAULT_MANAGE_POSITION_OPTIONAL_ACCOUNTS, ManagePositionOptionalAccounts, Number, QUOTE_PRECISION,
    MARK_PRICE_PRECISION
)
from sdk.utils import position_direction

class OpenPositionInstruction(InstructionCore):
    """Object to model an open-position instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'direction' / POSITION_DIRECTION_LAYOUT,
        'quote_asset_amount' / Int128ul,
        'market_index' / Int64ul,
        'limit_price' / Int128ul,
        'optional_accounts' / MANAGE_POSITION_OPTIONAL_ACCOUNTS_LAYOUT
    )

    def __init__(
            self, direction: int, quote_asset_amount: int, market_index: int, limit_price: int,
            optional_accounts: ManagePositionOptionalAccounts = DEFAULT_MANAGE_POSITION_OPTIONAL_ACCOUNTS
    ) -> None:
        self.name = 'open_position'
        self.direction = direction
        self.quote_asset_amount = quote_asset_amount
        self.market_index = market_index
        self.limit_price = limit_price
        self.optional_accounts = optional_accounts

    @classmethod
    def from_user_precision(
            cls, direction: int, quote_asset_amount: Number, market_index: int, limit_price: Number,
            optional_accounts: ManagePositionOptionalAccounts = DEFAULT_MANAGE_POSITION_OPTIONAL_ACCOUNTS
    ):
        """Handle precision."""
        instruction_object = cls(
            direction=direction,
            quote_asset_amount=round(quote_asset_amount * QUOTE_PRECISION),
            market_index=market_index,
            limit_price=round(limit_price * MARK_PRICE_PRECISION)
        )
        return instruction_object

    def get_instruction(
            self, state: PublicKey, user: PublicKey, authority: PublicKey, markets: PublicKey,
            user_positions: PublicKey, trade_history: PublicKey, funding_payment_history: PublicKey,
            funding_rate_history: PublicKey, oracle: PublicKey, program_id: PublicKey
    ) -> TransactionInstruction:
        """Returns a TransactionInstruction object."""
        bytes_data = self.build()
        account_keys = [
            AccountMeta(
                pubkey=state,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=user,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=authority,
                is_writable=False,
                is_signer=True
            ),
            AccountMeta(
                pubkey=markets,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=user_positions,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=trade_history,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=funding_payment_history,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=funding_rate_history,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=oracle,
                is_writable=False,
                is_signer=False
            )
        ]
        transaction_instruction = TransactionInstruction(
            keys=account_keys,
            program_id=program_id,
            data=bytes_data
        )
        return transaction_instruction