from construct import Struct, Int8ul, Int64ul, Int64sl, Flag
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from sdk.instructions.core import InstructionCore
from sdk.layouts import Int128ul, Int128sl, PUBLIC_KEY_LAYOUT
from sdk.state.clearing_house import FeeStructure, OracleGuardRails, ORACLE_SOURCE_LAYOUT


class UpdateFundingRateInstruction(InstructionCore):
    layout = Struct(
        'market_index' / Int64ul
    )

    def __init__(self, market_index: int) -> None:
        """Initialize object to update the funding rate of a given market.
        :param market_index: The index of the market to be updated."""
        self.market_index = market_index

    def get_instruction(self, state: PublicKey, markets: PublicKey, oracle: PublicKey,
                        funding_rate_history: PublicKey, program_id: PublicKey) -> TransactionInstruction:
        """Generate the required transaction instructions to update the funding rate.
        :param state: The public address of the clearing house state.
        :param markets: The public address of the clearing house markets.
        :param oracle: The public address of the oracle relating to the market to be updated.
        :param funding_rate_history: The public address of the clearing house funding rate history buffer.
        :param program_id: The public address of the clearing house program id."""
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
                pubkey=funding_rate_history,
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


class UpdateKInstruction(InstructionCore):
    layout = Struct(
        'sqrt_k' / Int128ul,
        'market_index' / Int64ul
    )

    def __init__(self, sqrt_k: int, market_index: int) -> None:
        self.sqrt_k = sqrt_k
        self.market_index = market_index

    def get_instruction(self, admin: PublicKey, state: PublicKey, markets: PublicKey, curve_history: PublicKey,
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
                is_writable=False,
                is_signer=False
            ),
            AccountMeta(
                pubkey=markets,
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


class UpdateParameterInstructionCore(InstructionCore):

    def get_instruction(self, admin: PublicKey, state: PublicKey, program_id: PublicKey) -> TransactionInstruction:
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
            )
        ]
        transaction_instruction = TransactionInstruction(
            keys=account_keys,
            program_id=program_id,
            data=bytes_data
        )
        return transaction_instruction


class UpdateMarginRatioInstruction(UpdateParameterInstructionCore):
    layout = Struct(
        'margin_ratio_initial' / Int128ul,
        'margin_ratio_partial' / Int128ul,
        'margin_ratio_maintenance' / Int128ul
    )

    def __init__(self, margin_ratio_initial: int, margin_ratio_partial: int, margin_ratio_maintenance: int) -> None:
        self.margin_ratio_initial = margin_ratio_initial
        self.margin_ratio_partial = margin_ratio_partial
        self.margin_ratio_maintenance = margin_ratio_maintenance


class UpdateFractionInstructionCore(UpdateParameterInstructionCore):
    layout = Struct(
        'numerator' / Int128ul,
        'denominator' / Int128ul
    )

    def __init__(self, numerator: int, denominator: int):
        self.numerator = numerator
        self.denominator = denominator


class UpdatePartialLiquidationClosePercentageInstruction(UpdateFractionInstructionCore):
    pass


class UpdatePartialLiquidationPenaltyPercentageInstruction(UpdateFractionInstructionCore):
    pass


class UpdateFullLiquidationPenaltyPercentageInstruction(UpdateFractionInstructionCore):
    pass


class UpdateDenominatorInstructionCore(UpdateParameterInstructionCore):
    layout = Struct(
        'denominator' / Int64ul
    )

    def __init__(self, denominator: int) -> None:
        self.denominator = denominator


class UpdatePartialLiquidationLiquidatorShareDenominatorInstruction(UpdateDenominatorInstructionCore):
    pass


class UpdateFullLiquidationLiquidatorShareDenominatorInstruction(UpdateDenominatorInstructionCore):
    pass


class UpdateFeeInstruction(UpdateParameterInstructionCore):
    layout = Struct(
        'fees' / FeeStructure.layout
    )

    def __init__(self, fees: FeeStructure) -> None:
        self.fees = fees


class UpdateOracleGuardRailsInstruction(UpdateParameterInstructionCore):
    layout = Struct(
        'oracle_guard_rails' / OracleGuardRails.layout
    )

    def __init__(self, oracle_guard_rails: OracleGuardRails) -> None:
        self.oracle_guard_rails = oracle_guard_rails


class UpdateMarketOracleInstruction(InstructionCore):
    layout = Struct(
        'market_index' / Int64ul,
        'oracle' / PUBLIC_KEY_LAYOUT,
        'oracle_source' / ORACLE_SOURCE_LAYOUT
    )

    def __init__(self, market_index: int, oracle: PublicKey, oracle_source: int) -> None:
        self.market_index = market_index
        self.oracle = oracle
        self.oracle_source = oracle_source

    def get_instruction(self, admin: PublicKey, state: PublicKey, markets: PublicKey,
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
                is_writable=False,
                is_signer=False
            ),
            AccountMeta(
                pubkey=markets,
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


class UpdateMarketMinimumTradeSizeInstruction(InstructionCore):
    layout = Struct(
        'market_index' / Int64ul,
        'minimum_trade_size' / Int128ul
    )

    def __init__(self, market_index: int, minimum_trade_size: int) -> None:
        self.market_index = market_index
        self.minimum_trade_size = minimum_trade_size

    def get_instruction(self, admin: PublicKey, state: PublicKey, markets: PublicKey,
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
                is_writable=False,
                is_signer=False
            ),
            AccountMeta(
                pubkey=markets,
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


class UpdateAdminInstruction(UpdateParameterInstructionCore):
    layout = Struct(
        'admin' / PUBLIC_KEY_LAYOUT
    )

    def __init__(self, admin: PublicKey) -> None:
        self.admin = admin


class UpdateWhiteListMintInstruction(UpdateParameterInstructionCore):
    layout = Struct(
        'white_list_mint' / PUBLIC_KEY_LAYOUT
    )

    def __init__(self, white_list_mint: PublicKey) -> None:
        self.white_list_mint = white_list_mint


class UpdateDiscountMintInstruction(UpdateParameterInstructionCore):
    layout = Struct(
        'discount_mint' / PUBLIC_KEY_LAYOUT
    )

    def __init__(self, discount_mint: PublicKey) -> None:
        self.discount_mint = discount_mint


class UpdateMaxDepositInstruction(UpdateParameterInstructionCore):
    layout = Struct(
        'max_deposit' / Int128ul
    )

    def __init__(self, max_deposit: int) -> None:
        self.max_deposit = max_deposit


class UpdateExchangePausedInstruction(UpdateParameterInstructionCore):
    layout = Struct(
        'exchange_paused' / Flag
    )

    def __init__(self, exchange_paused: bool) -> None:
        self.exchange_paused = exchange_paused


class DisableAdminControlsPricesInstruction(UpdateParameterInstructionCore):
    layout = Struct()

    def __init__(self) -> None:
        pass


class UpdateFundingPausedInstruction(UpdateParameterInstructionCore):
    layout = Struct(
        'funding_paused' / Flag
    )

    def __init__(self, funding_paused: bool) -> None:
        self.funding_paused = funding_paused