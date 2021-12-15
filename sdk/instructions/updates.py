"""This module models update instructions."""
from construct import Struct, Int8ul, Int64ul, Int64sl, Flag
from solana.transaction import TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from sdk.instructions.core import InstructionCore
from sdk.layouts import Int128ul, Int128sl, PUBLIC_KEY_LAYOUT, INSTRUCTION_NAME_LAYOUT
from sdk.state.clearing_house import FeeStructure, OracleGuardRails, ORACLE_SOURCE_LAYOUT


class UpdateFundingRateInstruction(InstructionCore):
    """Object to model an update-funding-rate instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'market_index' / Int64ul
    )

    def __init__(self, market_index: int) -> None:
        self.name = 'update_funding_rate'
        self.market_index = market_index

    def get_instruction(
            self, state: PublicKey, markets: PublicKey, oracle: PublicKey, funding_rate_history: PublicKey,
            program_id: PublicKey
    ) -> TransactionInstruction:
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
    """Object to model an update-k instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'sqrt_k' / Int128ul,
        'market_index' / Int64ul
    )

    def __init__(self, sqrt_k: int, market_index: int) -> None:
        self.name = 'update_k'
        self.sqrt_k = sqrt_k
        self.market_index = market_index

    def get_instruction(
            self, admin: PublicKey, state: PublicKey, markets: PublicKey, curve_history: PublicKey,
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
    """Core functionality for instructions which update parameters."""

    def get_instruction(
            self, admin: PublicKey, state: PublicKey, program_id: PublicKey
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
    """Object to model an update-margin-ratio instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'margin_ratio_initial' / Int128ul,
        'margin_ratio_partial' / Int128ul,
        'margin_ratio_maintenance' / Int128ul
    )

    def __init__(
            self, margin_ratio_initial: int, margin_ratio_partial: int, margin_ratio_maintenance: int
    ) -> None:
        self.name = 'update_margin_ratio'
        self.margin_ratio_initial = margin_ratio_initial
        self.margin_ratio_partial = margin_ratio_partial
        self.margin_ratio_maintenance = margin_ratio_maintenance


class UpdateFractionInstructionCore(UpdateParameterInstructionCore):
    """Core functionality for instructions which update a fraction-variable."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'numerator' / Int128ul,
        'denominator' / Int128ul
    )

    def __init__(self, numerator: int, denominator: int) -> None:
        self.numerator = numerator
        self.denominator = denominator


class UpdatePartialLiquidationClosePercentageInstruction(UpdateFractionInstructionCore):
    """Object to model an update-partial-liquidation-close-percentage instruction."""
    def __init__(self, numerator: int, denominator: int) -> None:
        self.name = 'update_partial_liquidation_close_percentage'
        super().__init__(
            numerator=numerator,
            denominator=denominator
        )



class UpdatePartialLiquidationPenaltyPercentageInstruction(UpdateFractionInstructionCore):
    """Object to model an update-partial-liquidation-penalty-percentage instruction."""
    def __init__(self, numerator: int, denominator: int) -> None:
        self.name = 'update_partial_liquidation_penalty_percentage'
        super().__init__(
            numerator=numerator,
            denominator=denominator
        )


class UpdateFullLiquidationPenaltyPercentageInstruction(UpdateFractionInstructionCore):
    """Object to model an update-full-liquidation-penalty-percentage instruction."""
    def __init__(self, numerator: int, denominator: int) -> None:
        self.name = 'update_full_liquidation_penalty_percentage'
        super().__init__(
            numerator=numerator,
            denominator=denominator
        )


class UpdateDenominatorInstructionCore(UpdateParameterInstructionCore):
    """Core functionality for instructions which update a denominator."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'denominator' / Int64ul
    )

    def __init__(self, denominator: int) -> None:
        self.denominator = denominator


class UpdatePartialLiquidationLiquidatorShareDenominatorInstruction(UpdateDenominatorInstructionCore):
    """Object to model an update-partial-liquidation-liquidator-share-denominator instruction."""
    def __init__(self, denominator: int) -> None:
        self.name = 'update_partial_liquidation_liquidator_share_denominator'
        super().__init__(
            denominator=denominator
        )


class UpdateFullLiquidationLiquidatorShareDenominatorInstruction(UpdateDenominatorInstructionCore):
    """Object to model an update-full-liquidation-liquidator-share-denominator instruction."""
    def __init__(self, denominator: int) -> None:
        self.name = 'update_full_liquidation_liquidator_share_denominator'
        super().__init__(
            denominator=denominator
        )


class UpdateFeeInstruction(UpdateParameterInstructionCore):
    """Object to model an update-fee instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'fees' / FeeStructure.layout
    )

    def __init__(self, fees: FeeStructure) -> None:
        self.name = 'update_fee'
        self.fees = fees


class UpdateOracleGuardRailsInstruction(UpdateParameterInstructionCore):
    """Object to model an update-oracle-guard-rails instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'oracle_guard_rails' / OracleGuardRails.layout
    )

    def __init__(self, oracle_guard_rails: OracleGuardRails) -> None:
        self.name = 'update_oracle_guard_rails'
        self.oracle_guard_rails = oracle_guard_rails


class UpdateMarketOracleInstruction(InstructionCore):
    """Object to model an update-market-oracle instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'market_index' / Int64ul,
        'oracle' / PUBLIC_KEY_LAYOUT,
        'oracle_source' / ORACLE_SOURCE_LAYOUT
    )

    def __init__(
            self, market_index: int, oracle: PublicKey, oracle_source: int
    ) -> None:
        self.name = 'update_market_oracle_instruction'
        self.market_index = market_index
        self.oracle = oracle
        self.oracle_source = oracle_source

    def get_instruction(
            self, admin: PublicKey, state: PublicKey, markets: PublicKey, program_id: PublicKey
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
    """Object to model an update-market-minimum-trade-size instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'market_index' / Int64ul,
        'minimum_trade_size' / Int128ul
    )

    def __init__(self, market_index: int, minimum_trade_size: int) -> None:
        self.name = 'update_market_minimum_trade_size_instruction'
        self.market_index = market_index
        self.minimum_trade_size = minimum_trade_size

    def get_instruction(self, admin: PublicKey, state: PublicKey, markets: PublicKey,
                        program_id: PublicKey) -> TransactionInstruction:
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
    """Object to model an update-admin instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'admin' / PUBLIC_KEY_LAYOUT
    )

    def __init__(self, admin: PublicKey) -> None:
        self.name = 'update_admin'
        self.admin = admin


class UpdateWhiteListMintInstruction(UpdateParameterInstructionCore):
    """Object to model an update-white-list-mint instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'white_list_mint' / PUBLIC_KEY_LAYOUT
    )

    def __init__(self, white_list_mint: PublicKey) -> None:
        self.name = 'update_white_list_mint'
        self.white_list_mint = white_list_mint


class UpdateDiscountMintInstruction(UpdateParameterInstructionCore):
    """Object to model an update-discount-mint instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'discount_mint' / PUBLIC_KEY_LAYOUT
    )

    def __init__(self, discount_mint: PublicKey) -> None:
        self.discount_mint = discount_mint


class UpdateMaxDepositInstruction(UpdateParameterInstructionCore):
    """Object to model an update-max-deposit instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'max_deposit' / Int128ul
    )

    def __init__(self, max_deposit: int) -> None:
        self.name = 'update_max_deposit_instruction'
        self.max_deposit = max_deposit


class UpdateExchangePausedInstruction(UpdateParameterInstructionCore):
    """Object to model an update-exchange-paused instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'exchange_paused' / Flag
    )

    def __init__(self, exchange_paused: bool) -> None:
        self.name = 'update_exchange_paused'
        self.exchange_paused = exchange_paused


class DisableAdminControlsPricesInstruction(UpdateParameterInstructionCore):
    """Object to model a disable-admin-controls-prices instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT
    )

    def __init__(self) -> None:
        self.name = 'disable_admin_controls_prices'


class UpdateFundingPausedInstruction(UpdateParameterInstructionCore):
    """Object to model an update-funding-paused instruction."""
    layout = Struct(
        'name' / INSTRUCTION_NAME_LAYOUT,
        'funding_paused' / Flag
    )

    def __init__(self, funding_paused: bool) -> None:
        self.name = 'update_funding_paused'
        self.funding_paused = funding_paused
