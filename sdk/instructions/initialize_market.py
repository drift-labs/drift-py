from construct import Struct, Int64ul, Int64sl, Flag
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from drift.instructions.core import InstructionCore
from drift.layouts import Int128ul, Int128sl

class InitializeMarketInstruction(InstructionCore):
    layout = Struct(
        'market_index' / Int64ul,
        'amm_base_asset_amount' / Int128ul,
        'amm_quote_asset_amount' / Int128ul,
        'amm_periodicity' / Int64sl,
        'amm_peg_multiplier' / Int128ul
    )

    def __init__(self, market_index: int, amm_base_asset_amount: int, amm_quote_asset_amount: int,
                 amm_periodicity: int, amm_peg_multiplier: int) -> None:
        self.market_index = market_index
        self.amm_base_asset_amount = amm_base_asset_amount
        self.amm_quote_asset_amount = amm_quote_asset_amount
        self.amm_periodicity = amm_periodicity
        self.amm_peg_multiplier = amm_peg_multiplier

    def get_instruction(self, admin: PublicKey, state: PublicKey, markets: PublicKey, oracle: PublicKey,
                        program_id: PublicKey) -> TransactionInstruction:
        bytes_data = self.build()
        account_keys = [
            AccountMeta(
                pubkey=admin,
                is_writable=False,
                is_signer=True
            ),
            AccountMeta(
                pubkey=state,
                is_writable=False,
                is_signer=False
            ),
            AccountMeta(
                pubkey=markets,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=oracle,
                is_signer=False,
                is_writable=False
            )
        ]
        transaction_instruction = TransactionInstruction(
            keys=account_keys,
            program_id=program_id,
            data=bytes_data
        )
        return transaction_instruction