"""This module models an initialize instruction."""
from construct import Struct, Int8ul, Flag
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from sdk.instructions.core import InstructionCore
from sdk.layouts import INSTRUCTION_NAME_LAYOUT


class InitializeInstruction(InstructionCore):
    """Object to model an initialize instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'clearing_house_nonce' / Int8ul,
        'collateral_vault_nonce' / Int8ul,
        'insurance_vault_nonce' / Int8ul,
        'admin_controls_prices' / Flag
    )

    def __init__(
            self, clearing_house_nonce: int, collateral_vault_nonce: int, insurance_vault_nonce: int,
            admin_controls_prices: int
    ) -> None:
        self.name = 'initialize'
        self.clearing_house_nonce = clearing_house_nonce
        self.collateral_vault_nonce = collateral_vault_nonce
        self.insurance_vault_nonce = insurance_vault_nonce
        self.admin_controls_prices = admin_controls_prices

    def get_instruction(
            self, admin: PublicKey, state: PublicKey, collateral_mint: PublicKey, collateral_vault: PublicKey,
            collateral_vault_authority: PublicKey, insurance_vault: PublicKey, insurance_vault_authority: PublicKey,
            markets: PublicKey, rent: PublicKey, system_program: PublicKey, token_program: PublicKey,
            program_id: PublicKey
    ) -> TransactionInstruction:
        """Returns a TransactionInstruction object."""
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
                is_signer=True
            ),
            AccountMeta(
                pubkey=collateral_mint,
                is_writable=True,
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
                pubkey=markets,
                is_writable=True,
                is_signer=False
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