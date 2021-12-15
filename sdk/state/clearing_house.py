"""This module models the Drift clearing house."""
import json

from abc import ABC, abstractmethod
from construct import Container, Struct, Int8ul, Int64ul, Int64sl, Flag, Padding

from solana.publickey import PublicKey
from sdk.layouts import PUBLIC_KEY_LAYOUT, Int128ul, Int128sl, ORACLE_SOURCE_LAYOUT
from sdk.constants import ORACLE_INDEX_TO_SOURCE
from sdk.state.core import ElementCore


class Fraction(ElementCore):
    """Object to model a fraction."""
    layout = Struct(
        'numerator' / Int128ul,
        'denominator' / Int128ul
    )

    def __init__(self, numerator: int, denominator: int) -> None:
        self.numerator = numerator
        self.denominator = denominator

    @classmethod
    def from_container(cls, container: Container):
        """Create a fraction from a container."""
        fraction = cls(
            numerator=container.numerator,
            denominator=container.denominator
        )
        return fraction

    def to_float(self):
        """Get the value of the fraction."""
        return float(self.numerator / self.denominator)

    def to_dict(self) -> dict:
        """For pretty printing."""
        my_dict = {
            'numerator': self.numerator,
            'denominator': self.denominator
        }
        return my_dict


class DiscountTokenTier(ElementCore):
    """Object to model a discount-token-tier."""
    layout = Struct(
        'minimum_balance' / Int64ul,
        'discount' / Fraction.layout
    )

    def __init__(self, minimum_balance: int, discount: Fraction) -> None:
        self.minimum_balance = minimum_balance
        self.discount = discount

    @classmethod
    def from_container(cls, container: Container):
        """Create a discount-token-tier from a container."""
        discount_token_tier = cls(
            minimum_balance=container.minimum_balance,
            discount=Fraction.from_container(container=container.discount)
        )
        return discount_token_tier

    def to_dict(self) -> dict:
        """For pretty printing."""
        my_dict = {
            'minimum_balance': self.minimum_balance,
            'discount': self.discount.to_dict()
        }
        return my_dict


class DiscountTokenTiers(ElementCore):
    """Object to model multiple discount-token-tiers."""
    layout = Struct(
        'first_tier' / DiscountTokenTier.layout,
        'second_tier' / DiscountTokenTier.layout,
        'third_tier' / DiscountTokenTier.layout,
        'fourth_tier' / DiscountTokenTier.layout
    )

    def __init__(self, first_tier: DiscountTokenTier, second_tier: DiscountTokenTier, third_tier: DiscountTokenTier,
                 fourth_tier: DiscountTokenTier) -> None:
        self.first_tier = first_tier
        self.second_tier = second_tier
        self.third_tier = third_tier
        self.fourth_tier = fourth_tier

    @classmethod
    def from_container(cls, container: Container):
        """Create multiple discount-token-tiers from a container."""
        discount_token_tiers = cls(
            first_tier=DiscountTokenTier.from_container(container=container.first_tier),
            second_tier=DiscountTokenTier.from_container(container=container.second_tier),
            third_tier=DiscountTokenTier.from_container(container=container.third_tier),
            fourth_tier=DiscountTokenTier.from_container(container=container.fourth_tier)
        )
        return discount_token_tiers

    def to_dict(self) -> dict:
        """For pretty printing."""
        my_dict = {
            'first_tier': self.first_tier.to_dict(),
            'second_tier': self.second_tier.to_dict(),
            'third_tier': self.third_tier.to_dict(),
            'fourth_tier': self.fourth_tier.to_dict()
        }
        return my_dict


class ReferralDiscount(ElementCore):
    """Object to model a referral-discount."""
    layout = Struct(
        'referrer_reward' / Fraction.layout,
        'referee_discount' / Fraction.layout
    )

    def __init__(self, referrer_reward: Fraction, referee_discount: Fraction) -> None:
        self.referrer_reward = referrer_reward
        self.referee_discount = referee_discount

    @classmethod
    def from_container(cls, container: Container):
        """Create a referral-discount from a container."""
        referral_discount = cls(
            referrer_reward=Fraction.from_container(container=container.referrer_reward),
            referee_discount=Fraction.from_container(container=container.referee_discount)
        )
        return referral_discount

    def to_dict(self) -> dict:
        """For pretty-printing."""
        my_dict = {
            'referrer_reward': self.referrer_reward.to_dict(),
            'referee_discount': self.referee_discount.to_dict()
        }
        return my_dict


class FeeStructure(ElementCore):
    """Object to model Drift fee-structure."""
    layout = Struct(
        'fee' / Fraction.layout,
        'discount_token_tiers' / DiscountTokenTiers.layout,
        'referral_discount' / ReferralDiscount.layout
    )

    def __init__(
            self, fee: Fraction, discount_token_tiers: DiscountTokenTiers, referral_discount: ReferralDiscount
    ) -> None:
        self.fee = fee
        self.discount_token_tiers = discount_token_tiers
        self.referral_discount = referral_discount

    @classmethod
    def from_container(cls, container: Container):
        """Create a fee-structure from a container."""
        fee_structure = cls(
            fee=Fraction.from_container(container=container.fee),
            discount_token_tiers=DiscountTokenTiers.from_container(container=container.discount_token_tiers),
            referral_discount=ReferralDiscount.from_container(container=container.referral_discount)
        )
        return fee_structure

    def to_dict(self) -> dict:
        """For pretty printing."""
        my_dict = {
            'fee': self.fee.to_dict(),
            'discount_token_tiers': self.discount_token_tiers.to_dict(),
            'referral_discount': self.referral_discount.to_dict()
        }
        return my_dict

class OracleValidity(ElementCore):
    """Object to model oracle-validity."""
    layout = Struct(
        'slots_before_stale' / Int64sl,
        'confidence_interval_max_size' / Int128ul,
        'too_volatile_ratio' / Int128sl
    )

    def __init__(self, slots_before_stale: int, confidence_interval_max_size: int, too_volatile_ratio: int) -> None:
        self.slots_before_stale = slots_before_stale
        self.confidence_interval_max_size = confidence_interval_max_size
        self.too_volatile_ratio = too_volatile_ratio

    @classmethod
    def from_container(cls, container: Container):
        """Create an oracle-validity object from a container."""
        oracle_validity = cls(
            slots_before_stale=container.slots_before_stale,
            confidence_interval_max_size=container.confidence_interval_max_size,
            too_volatile_ratio=container.too_volatile_ratio
        )
        return oracle_validity

    def to_dict(self) -> dict:
        """For pretty printing."""
        my_dict = {
            'slots_before_stale': self.slots_before_stale,
            'confidence_interval_max_size': self.confidence_interval_max_size,
            'too_volatile_ratio': self.too_volatile_ratio
        }
        return my_dict


class OracleGuardRails(ElementCore):
    """Object to model oracle-guard-rails."""
    layout = Struct(
        'price_divergence' / Fraction.layout,
        'validity' / OracleValidity.layout,
        'use_for_liquidation' / Flag
    )

    def __init__(self, price_divergence: Fraction, validity: OracleValidity, use_for_liquidation: bool) -> None:
        self.price_divergence = price_divergence
        self.validity = validity
        self.use_for_liquidation = use_for_liquidation

    @classmethod
    def from_container(cls, container: Container):
        """Create oracle-guard-rails from a container."""
        oracle_guard_rails = cls(
            price_divergence=Fraction.from_container(container=container.price_divergence),
            validity=OracleValidity.from_container(container=container.validity),
            use_for_liquidation=container.use_for_liquidation
        )
        return oracle_guard_rails

    def to_dict(self) -> dict:
        """For pretty printing."""
        my_dict = {
            'price_divergence': self.price_divergence.to_dict(),
            'validity': self.validity.to_dict(),
            'use_for_liquidation': self.use_for_liquidation
        }
        return my_dict


class ClearingHouseState(ElementCore):
    """Object to model the drift clearing-house."""
    layout = Struct(
        Padding(8),
        'admin' / PUBLIC_KEY_LAYOUT,
        'exchange_paused' / Flag,
        'funding_paused' / Flag,
        'admin_controls_prices' / Flag,
        'collateral_mint' / PUBLIC_KEY_LAYOUT,
        'collateral_vault' / PUBLIC_KEY_LAYOUT,
        'collateral_vault_authority' / PUBLIC_KEY_LAYOUT,
        'collateral_vault_nonce' / Int8ul,
        'deposit_history' / PUBLIC_KEY_LAYOUT,
        'trade_history' / PUBLIC_KEY_LAYOUT,
        'funding_payment_history' / PUBLIC_KEY_LAYOUT,
        'funding_rate_history' / PUBLIC_KEY_LAYOUT,
        'liquidation_history' / PUBLIC_KEY_LAYOUT,
        'curve_history' / PUBLIC_KEY_LAYOUT,
        'insurance_vault' / PUBLIC_KEY_LAYOUT,
        'insurance_vault_authority' / PUBLIC_KEY_LAYOUT,
        'insurance_vault_nonce' / Int8ul,
        'markets' / PUBLIC_KEY_LAYOUT,
        'margin_ratio_initial' / Int128ul,
        'margin_ratio_maintenance' / Int128ul,
        'margin_ratio_partial' / Int128ul,
        'partial_liquidation_close_percentage' / Fraction.layout,
        'partial_liquidation_penalty_percentage' / Fraction.layout,
        'full_liquidation_penalty_percentage' / Fraction.layout,
        'partial_liquidation_liquidator_share_denominator' / Int64ul,
        'full_liquidation_liquidator_share_denominator' / Int64ul,
        'fee_structure' / FeeStructure.layout,
        'white_list_mint' / PUBLIC_KEY_LAYOUT,
        'discount_mint' / PUBLIC_KEY_LAYOUT,
        'oracle_guard_rails' / OracleGuardRails.layout,
        'max_deposit' / Int128ul,
        Padding(128)
    )

    def __init__(
            self, admin: PublicKey, exchange_paused: bool, funding_paused: bool, admin_controls_prices: bool,
            collateral_mint: PublicKey, collateral_vault: PublicKey, collateral_vault_authority: PublicKey,
            collateral_vault_nonce: int, deposit_history: PublicKey, trade_history: PublicKey,
            funding_payment_history: PublicKey, funding_rate_history: PublicKey, liquidation_history: PublicKey,
            curve_history: PublicKey, insurance_vault: PublicKey, insurance_vault_authority: PublicKey,
            insurance_vault_nonce: PublicKey, markets: PublicKey, margin_ratio_initial: int,
            margin_ratio_maintenance: int, margin_ratio_partial: int, partial_liquidation_close_percentage: Fraction,
            partial_liquidation_penalty_percentage: Fraction, full_liquidation_penalty_percentage: Fraction,
            partial_liquidation_liquidator_share_denominator: int, full_liquidation_liquidator_share_denominator: int,
            fee_structure: FeeStructure, white_list_mint: PublicKey, discount_mint: PublicKey,
            oracle_guard_rails: OracleGuardRails, max_deposit: int
    ) -> None:
        self.admin = admin
        self.exchange_paused = exchange_paused
        self.funding_paused = funding_paused
        self.admin_controls_prices = admin_controls_prices
        self.collateral_mint = collateral_mint
        self.collateral_vault = collateral_vault
        self.collateral_vault_authority = collateral_vault_authority
        self.collateral_vault_nonce = collateral_vault_nonce
        self.deposit_history = deposit_history
        self.trade_history = trade_history
        self.funding_payment_history = funding_payment_history
        self.funding_rate_history = funding_rate_history
        self.liquidation_history = liquidation_history
        self.curve_history = curve_history
        self.insurance_vault = insurance_vault
        self.insurance_vault_authority = insurance_vault_authority
        self.insurance_vault_nonce = insurance_vault_nonce
        self.markets = markets
        self.margin_ratio_initial = margin_ratio_initial
        self.margin_ratio_maintenance = margin_ratio_maintenance
        self.margin_ratio_partial = margin_ratio_partial
        self.partial_liquidation_close_percentage = partial_liquidation_close_percentage
        self.partial_liquidation_penalty_percentage = partial_liquidation_penalty_percentage
        self.full_liquidation_penalty_percentage = full_liquidation_penalty_percentage
        self.partial_liquidation_liquidator_share_denominator = partial_liquidation_liquidator_share_denominator
        self.full_liquidation_liquidator_share_denominator = full_liquidation_liquidator_share_denominator
        self.fee_structure = fee_structure
        self.white_list_mint = white_list_mint
        self.discount_mint = discount_mint
        self.oracle_guard_rails = oracle_guard_rails
        self.max_deposit = max_deposit

    @classmethod
    def from_container(cls, container: Container):
        """Create a clearing-house from a container."""
        clearing_house = cls(
            admin=container.admin,
            exchange_paused=container.exchange_paused,
            funding_paused=container.funding_paused,
            admin_controls_prices=container.admin_controls_prices,
            collateral_mint=container.collateral_mint,
            collateral_vault=container.collateral_vault,
            collateral_vault_authority=container.collateral_vault_authority,
            collateral_vault_nonce=container.collateral_vault_nonce,
            deposit_history=container.deposit_history,
            trade_history=container.trade_history,
            funding_payment_history=container.funding_payment_history,
            funding_rate_history=container.funding_rate_history,
            liquidation_history=container.liquidation_history,
            curve_history=container.curve_history,
            insurance_vault=container.insurance_vault,
            insurance_vault_authority=container.insurance_vault_authority,
            insurance_vault_nonce=container.insurance_vault_nonce,
            markets=container.markets,
            margin_ratio_initial=container.margin_ratio_initial,
            margin_ratio_maintenance=container.margin_ratio_maintenance,
            margin_ratio_partial=container.margin_ratio_partial,
            partial_liquidation_close_percentage=Fraction.from_container(
                container=container.partial_liquidation_close_percentage
            ),
            partial_liquidation_penalty_percentage=Fraction.from_container(
                container=container.partial_liquidation_penalty_percentage
            ),
            full_liquidation_penalty_percentage=Fraction.from_container(
                container=container.full_liquidation_penalty_percentage
            ),
            partial_liquidation_liquidator_share_denominator=container.partial_liquidation_liquidator_share_denominator,
            full_liquidation_liquidator_share_denominator=container.full_liquidation_liquidator_share_denominator,
            fee_structure=FeeStructure.from_container(container=container.fee_structure),
            white_list_mint=container.white_list_mint,
            discount_mint=container.discount_mint,
            oracle_guard_rails=OracleGuardRails.from_container(container=container.oracle_guard_rails),
            max_deposit=container.max_deposit
        )
        return clearing_house

    def to_dict(self) -> dict:
        """For pretty printing."""
        my_dict = {
            'admin': self.admin.__str__(),
            'exchange_paused': self.exchange_paused,
            'funding_paused': self.funding_paused,
            'admin_controls_prices': self.admin_controls_prices,
            'collateral_mint': self.collateral_mint.__str__(),
            'collateral_vault': self.collateral_vault.__str__(),
            'collateral_vault_authority': self.collateral_vault_authority.__str__(),
            'collateral_vault_nonce': self.collateral_vault_nonce,
            'deposit_history': self.deposit_history.__str__(),
            'trade_history': self.trade_history.__str__(),
            'funding_payment_history': self.funding_payment_history.__str__(),
            'funding_rate_history': self.funding_rate_history.__str__(),
            'liquidation_history': self.liquidation_history.__str__(),
            'curve_history': self.curve_history.__str__(),
            'insurance_vault': self.insurance_vault.__str__(),
            'insurance_vault_authority': self.insurance_vault_authority.__str__(),
            'insurance_vault_nonce': self.insurance_vault_nonce,
            'markets': self.markets.__str__(),
            'margin_ratio_initial': self.margin_ratio_initial,
            'margin_ratio_maintenance': self.margin_ratio_maintenance,
            'margin_ratio_partial': self.margin_ratio_partial,
            'partial_liquidation_close_percentage': self.partial_liquidation_close_percentage.to_dict(),
            'partial_liquidation_penalty_percentage': self.partial_liquidation_penalty_percentage.to_dict(),
            'full_liquidation_penalty_percentage': self.full_liquidation_penalty_percentage.to_dict(),
            'partial_liquidation_liquidator_share_denominator': self.partial_liquidation_liquidator_share_denominator,
            'full_liquidation_liquidator_share_denominator': self.full_liquidation_liquidator_share_denominator,
            'fee_structure': self.fee_structure.to_dict(),
            'white_list_mint': self.white_list_mint.__str__(),
            'discount_mint': self.discount_mint.__str__(),
            'oracle_guard_rails': self.oracle_guard_rails.to_dict(),
            'max_deposit': self.max_deposit
        }
        return my_dict
