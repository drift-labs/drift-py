from construct import Struct, Int8ul, Int64ul, Int64sl, Flag
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from drift.instructions.core import InstructionCore
from drift.layouts import Int128ul, Int128sl


class InitializeUserInstruction(InstructionCore):
    layout = Struct(
        'user_nonce' / Int8ul
    )

    def __init__(self, user_nonce: int) -> None:
        self.user_nonce = user_nonce

    def get_instruction(self, user: PublicKey, state: PublicKey, user_positions: PublicKey, authority: PublicKey,
                        rent: PublicKey, system_program: PublicKey, program_id: PublicKey) -> TransactionInstruction:
        bytes_data = self.build()
        account_keys = [
            AccountMeta(
                pubkey=user,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=state,
                is_writable=False,
                is_signer=False
            ),
            AccountMeta(
                pubkey=user_positions,
                is_writable=True,
                is_signer=True
            ),
            AccountMeta(
                pubkey=authority,
                is_writable=False,
                is_signer=True
            ),
            AccountMeta(
                pubkey=rent,
                is_writable=False,
                is_signer=False
            ),
            AccountMeta(
                pubkey=system_program,
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