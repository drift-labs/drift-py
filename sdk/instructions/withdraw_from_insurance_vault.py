"""This module models a withdraw-from-insurance-vault instruction."""
from construct import Struct, Int64ul, Int64sl, Flag
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from sdk.instructions.core import InstructionCore
from sdk.layouts import Int128ul, Int128sl, INSTRUCTION_NAME_LAYOUT


class WithdrawFromInsuranceVaultInstruction(InstructionCore):
    """Object to model a withdraw-from-insurance-vault instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'amount' / Int64ul
    )

    def __init__(self, amount: int) -> None:
        self.name = 'withdraw_from_insurance_vault'
        self.amount = amount

    def get_instruction(
            self, state: PublicKey, admin: PublicKey, insurance_vault: PublicKey, insurance_vault_authority: PublicKey,
            recipient: PublicKey, token_program: PublicKey, program_id: PublicKey
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
                pubkey=insurance_vault,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=insurance_vault_authority,
                is_writable=False,
                is_signer=False
            ),
            AccountMeta(
                pubkey=recipient,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=token_program,
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
