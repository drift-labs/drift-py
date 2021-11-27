from construct import Struct, Int8ul, Flag
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from drift.instructions.core import InstructionCore

class InitializeHistoryInstruction(InstructionCore):
    layout = Struct()

    def get_instruction(self, admin: PublicKey, state: PublicKey, funding_payment_history: PublicKey,
                        trade_history: PublicKey, liquidation_history: PublicKey, deposit_history: PublicKey,
                        funding_rate_history: PublicKey, curve_history: PublicKey,
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
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=funding_payment_history,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=trade_history,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=liquidation_history,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=deposit_history,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=funding_rate_history,
                is_writable=True,
                is_signer=False
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

