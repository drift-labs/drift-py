from construct import Struct, Int64ul, Int64sl, Flag
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from drift.instructions.core import InstructionCore
from drift.layouts import Int128ul, Int128sl


class WithdrawFeesInstruction(InstructionCore):
    layout = Struct(
        'market_index' / Int64ul,
        'amount' / Int64ul
    )

    def __init__(self, market_index: int, amount: int) -> None:
        self.market_index = market_index
        self.amount = amount

    def get_instruction(self, state: PublicKey, admin: PublicKey, collateral_vault: PublicKey,
                        collateral_vault_authority: PublicKey, markets: PublicKey, recipient: PublicKey,
                        token_program: PublicKey, program_id: PublicKey) -> TransactionInstruction:
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
                pubkey=collateral_vault,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=collateral_vault_authority,
                is_writable=False,
                is_signer=False
            ),
            AccountMeta(
                pubkey=markets,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=recipient,
                is_writable=False,
                is_signer=True
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