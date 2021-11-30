from construct import Struct, Int64ul, Int64sl, Flag
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from sdk.instructions.core import InstructionCore
from sdk.layouts import Int128ul, Int128sl


class DepositCollateralInstruction(InstructionCore):
    layout = Struct(
        'amount' / Int64ul
    )

    def __init__(self, amount: int) -> None:
        self.amount = amount

    def get_instruction(self, state: PublicKey, user: PublicKey, authority: PublicKey, collateral_vault: PublicKey,
                        user_collateral_account: PublicKey, token_program: PublicKey, markets: PublicKey,
                        user_positions: PublicKey, funding_payment_history: PublicKey, deposit_history: PublicKey,
                        program_id: PublicKey) -> TransactionInstruction:
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
                pubkey=collateral_vault,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=user_collateral_account,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=token_program,
                is_writable=False,
                is_signer=False
            ),
            AccountMeta(
                pubkey=markets,
                is_writable=False,
                is_signer=False
            ),
            AccountMeta(
                pubkey=user_positions,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=funding_payment_history,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=deposit_history,
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