from construct import Struct, Int64ul, Int64sl, Flag
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from drift.instructions.core import InstructionCore
from drift.layouts import Int128ul, Int128sl


class RepegAmmCurveInstruction(InstructionCore):
    layout = Struct(
        'new_peg_candidate' / Int128ul,
        'market_index' / Int64ul
    )

    def __init__(self, new_peg_candidate: int, market_index: int) -> None:
        self.new_peg_candidate = new_peg_candidate
        self.market_index = market_index

    def get_instruction(self, state: PublicKey, markets: PublicKey, oracle: PublicKey, admin: PublicKey,
                        curve_history: PublicKey, program_id: PublicKey) -> TransactionInstruction:
        bytes_data = self.build()
        account_keys = [
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
                is_writable=False,
                is_signer=False
            ),
            AccountMeta(
                pubkey=admin,
                is_writable=False,
                is_signer=True
            ),
            AccountMeta(
                pubkey=curve_history,
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