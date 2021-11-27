from construct import Struct, Int8ul, Int64ul, Int64sl, Flag
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from drift.instructions.core import InstructionCore
from drift.layouts import Int128ul, Int128sl


class DeleteUserInstruction(InstructionCore):
    layout = Struct()

    def __init__(self):
        pass

    def get_instruction(self, user: PublicKey, user_positions: PublicKey, authority: PublicKey,
                        program_id: PublicKey) -> TransactionInstruction:
        bytes_data = self.build()
        account_keys = [
            AccountMeta(
                pubkey=user,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=user_positions,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=authority,
                is_writable=False,
                is_signer=True
            )
        ]
        transaction_instruction = TransactionInstruction(
            keys=account_keys,
            program_id=program_id,
            data=bytes_data
        )
        return transaction_instruction