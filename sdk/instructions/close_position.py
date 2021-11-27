from construct import Struct, Int64ul, Int64sl, Flag
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from drift.instructions.core import InstructionCore
from drift.layouts import Int128ul, Int128sl, POSITION_DIRECTION_LAYOUT


class ClosePositionInstruction(InstructionCore):
    layout = Struct(
        'market_index' / Int64ul,
    )

    def __init__(self, market_index: int) -> None:
        self.market_index = market_index

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