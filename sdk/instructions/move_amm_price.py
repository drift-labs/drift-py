"""This module models a move-amm-price instruction."""
from construct import Struct, Int64ul, Int64sl, Flag
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from sdk.instructions.core import InstructionCore
from sdk.layouts import Int128ul, Int128sl, INSTRUCTION_NAME_LAYOUT


class MoveAmmPriceInstruction(InstructionCore):
    """Object to model a move-amm-price instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'base_asset_reserve' / Int128ul,
        'quote_asset_reserve' / Int128ul,
        'market_index' / Int64ul
    )

    def __init__(
            self, base_asset_reserve: int, quote_asset_reserve: int, market_index: int
    ) -> None:
        self.name = 'move_amm_price'
        self.base_asset_reserve = base_asset_reserve
        self.quote_asset_reserve = quote_asset_reserve
        self.market_index = market_index

    def get_instruction(
            self, state: PublicKey, admin: PublicKey, markets: PublicKey, program_id: PublicKey
    ) -> TransactionInstruction:
        """Returns a TransactionInstruction object."""
        bytes_data = self.build()
        account_keys = [
            AccountMeta(
                pubkey=state,
                is_writable=False,
                is_signer=False
            ),
            AccountMeta(
                pubkey=admin,
                is_writable=False,
                is_signer=True
            ),
            AccountMeta(
                pubkey=markets,
                is_writable=True,
                is_signer=False
            )
        ]
        transaction_instruction = TransactionInstruction(
            keys=account_keys,
            program_id=program_id,
            data=bytes_data
        )
        return transaction_instruction
