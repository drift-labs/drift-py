from construct import Struct, Int64ul, Int64sl, Flag, PaddedString, Int64ub, Bytes, Padding
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from sdk.instructions.core import InstructionCore
from sdk.layouts import Int128ul, Int128sl, POSITION_DIRECTION_LAYOUT, MANAGE_POSITION_OPTIONAL_ACCOUNTS_LAYOUT, Int8ul
from sdk.constants import DEFAULT_MANAGE_POSITION_OPTIONAL_ACCOUNTS, ManagePositionOptionalAccounts


class OpenPositionInstruction(InstructionCore):
    layout = Struct(
        Padding(8),
        'tag' / Int64ul,
        'direction' / POSITION_DIRECTION_LAYOUT,
        'quote_asset_amount' / Int128ul,
        'market_index' / Int64ul,
        'limit_price' / Int128ul,
        'optional_accounts' / MANAGE_POSITION_OPTIONAL_ACCOUNTS_LAYOUT
    )

    def __init__(self, tag: int, direction: int, quote_asset_amount: int, market_index: int, limit_price: int,
                 optional_accounts: ManagePositionOptionalAccounts = DEFAULT_MANAGE_POSITION_OPTIONAL_ACCOUNTS) -> None:
        self.tag = tag
        self.direction = direction
        self.quote_asset_amount = quote_asset_amount
        self.market_index = market_index
        self.limit_price = limit_price
        self.optional_accounts = optional_accounts

    def get_instruction(self, state: PublicKey, user: PublicKey, authority: PublicKey, markets: PublicKey,
                        user_positions: PublicKey, trade_history: PublicKey, funding_payment_history: PublicKey,
                        funding_rate_history: PublicKey, oracle: PublicKey,
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
                pubkey=markets,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=user_positions,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=trade_history,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=funding_payment_history,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=funding_rate_history,
                is_writable=True,
                is_signer=False
            ),
            AccountMeta(
                pubkey=oracle,
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