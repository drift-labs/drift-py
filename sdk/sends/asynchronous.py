"""Asynchronous functions to send instructions to the blockchain, to be executed by the Drift protocol."""
import asyncio
from typing import List

from solana.rpc.async_api import AsyncClient as SolanaClient, Commitment
from solana.transaction import TransactionInstruction, Transaction
from solana.rpc.types import TxOpts, RPCResponse
from solana.publickey import PublicKey
from solana.keypair import Keypair

from sdk.constants import *
from sdk.instructions.all import *
from sdk.utils import get_user_account_address


async def sign_and_send_transaction_instructions(
        client: SolanaClient,
        keypair: Keypair,
        commitment: Commitment,
        transaction_instructions: List[TransactionInstruction]
) -> RPCResponse:
    """Sign a transaction instruction and send it."""
    signers = [keypair]
    transaction = Transaction()
    transaction.fee_payer = keypair.public_key
    transaction.add(*transaction_instructions)
    response = await client.send_transaction(
        transaction,
        *signers,
        opts=TxOpts(
            preflight_commitment=commitment
        )
    )
    return response


async def send_initialize(
        client: SolanaClient, wallet: Keypair, commitment: Commitment, clearing_house_nonce: int,
        collateral_vault_nonce: int, insurance_vault_nonce: int, admin_controls_prices: int, admin: PublicKey
) -> RPCResponse:
    """Send an initialize instruction."""
    instruction_object = InitializeInstruction(
        clearing_house_nonce=clearing_house_nonce,
        collateral_vault_nonce=collateral_vault_nonce,
        insurance_vault_nonce=insurance_vault_nonce,
        admin_controls_prices=admin_controls_prices
    )
    transaction_instruction = instruction_object.get_instruction(
        admin=admin
    )
    rpc_response = await sign_and_send_transaction_instructions(
        client=client,
        keypair=wallet,
        transaction_instructions=[transaction_instruction],
        commitment=commitment
    )
    return rpc_response


async def send_close_position(
        client: SolanaClient, commitment: Commitment, wallet: Keypair, market_index: int, user_positions: PublicKey
) -> RPCResponse:
    """Send a close-position instruction."""
    instruction_object = ClosePositionInstruction(
        market_index=market_index
    )
    user = get_user_account_address(authority=wallet.public_key)
    transaction_instruction = instruction_object.get_instruction(
        state=CLEARING_HOUSE_ADDRESSES.state,
        user=user,
        authority=wallet.public_key,
        markets=CLEARING_HOUSE_ADDRESSES.markets,
        user_positions=user_positions,
        trade_history=CLEARING_HOUSE_ADDRESSES.history.trade,
        funding_payment_history=CLEARING_HOUSE_ADDRESSES.history.funding_payment,
        funding_rate_history=CLEARING_HOUSE_ADDRESSES.history.funding_rate,
        oracle=CURRENT_MARKETS[market_index].mainnet_pyth_oracle,
        program_id=CLEARING_HOUSE_ADDRESSES.program
    )
    rpc_response = await sign_and_send_transaction_instructions(
        client=client,
        keypair=wallet,
        transaction_instructions=[transaction_instruction],
        commitment=commitment
    )
    return rpc_response


async def send_delete_user(
        client: SolanaClient, commitment: Commitment, wallet: Keypair, user_positions: PublicKey
) -> RPCResponse:
    """Send a delete-user instruction."""
    instruction_object = DeleteUserInstruction()
    user = get_user_account_address(
        authority=wallet.public_key
    )
    transaction_instruction = instruction_object.get_instruction(
        user=user,
        user_positions=user_positions,
        authority=wallet.public_key,
        program_id=CLEARING_HOUSE_ADDRESSES.program
    )
    rpc_response = await sign_and_send_transaction_instructions(
        client=client,
        keypair=wallet,
        transaction_instructions=[transaction_instruction],
        commitment=commitment
    )
    return rpc_response


async def send_deposit_collateral(
        client: SolanaClient, commitment: Commitment, wallet: Keypair, amount: int, user_collateral_account: PublicKey,
        user_positions: PublicKey
) -> RPCResponse:
    """Send a deposit-collateral instruction."""
    instruction_object = DepositCollateralInstruction.from_user_precision(
        amount=amount
    )
    user = get_user_account_address(
        authority=wallet.public_key
    )
    transaction_instruction = instruction_object.get_instruction(
        state=CLEARING_HOUSE_ADDRESSES.state,
        user=user,
        authority=wallet.public_key,
        collateral_vault=CLEARING_HOUSE_ADDRESSES.collateral_vault,
        user_collateral_account=user_collateral_account,
        token_program=TOKEN_PROGRAM_ID,
        markets=CLEARING_HOUSE_ADDRESSES.markets,
        user_positions=user_positions,
        funding_payment_history=CLEARING_HOUSE_ADDRESSES.history.funding_payment,
        deposit_history=CLEARING_HOUSE_ADDRESSES.history.deposit,
        program_id=CLEARING_HOUSE_ADDRESSES.program
    )
    rpc_response = await sign_and_send_transaction_instructions(
        client=client,
        keypair=wallet,
        transaction_instructions=[transaction_instruction],
        commitment=commitment
    )
    return rpc_response


async def send_liquidate(
        client: SolanaClient, commitment: Commitment, wallet: Keypair, liquidator: PublicKey, user_positions: PublicKey
) -> RPCResponse:
    """Send a liquidate instruction."""
    instruction_object = LiquidateInstruction()
    user = get_user_account_address(
        authority=wallet.public_key
    )
    transaction_instruction = instruction_object.get_instruction(
        state=CLEARING_HOUSE_ADDRESSES.state,
        authority=wallet.public_key,
        liquidator=PublicKey,
        user=user,
        collateral_vault=CLEARING_HOUSE_ADDRESSES.collateral_vault,
        collateral_vault_authority=CLEARING_HOUSE_ADDRESSES.collateral_vault_authority,
        insurance_vault=CLEARING_HOUSE_ADDRESSES.insurance_vault,
        insurance_vault_authority=CLEARING_HOUSE_ADDRESSES.insurance_vault_authority,
        token_program=TOKEN_PROGRAM_ID,
        markets=CLEARING_HOUSE_ADDRESSES.markets,
        user_positions=user_positions,
        trade_history=CLEARING_HOUSE_ADDRESSES.history.trade,
        funding_payment_history=CLEARING_HOUSE_ADDRESSES.history.funding_payment,
        program_id=CLEARING_HOUSE_ADDRESSES.program
    )
    rpc_response = await sign_and_send_transaction_instructions(
        client=client,
        keypair=wallet,
        transaction_instructions=[transaction_instruction],
        commitment=commitment
    )
    return rpc_response


async def send_open_position(
        client: SolanaClient, commitment: Commitment, wallet: Keypair, direction: int, quote_asset_amount: int,
        market_index: int, limit_price: int, user_positions: PublicKey
) -> RPCResponse:
    """Send an open-position instruction."""
    instruction_object = OpenPositionInstruction.from_user_precision(
        direction=direction,
        quote_asset_amount=quote_asset_amount,
        market_index=market_index,
        limit_price=limit_price
    )
    user = get_user_account_address(
        authority=wallet.public_key
    )
    transaction_instruction = instruction_object.get_instruction(
        state=CLEARING_HOUSE_ADDRESSES.state,
        user=user,
        authority=wallet.public_key,
        markets=CLEARING_HOUSE_ADDRESSES.markets,
        user_positions=user_positions,
        trade_history=CLEARING_HOUSE_ADDRESSES.history.trade,
        funding_payment_history=CLEARING_HOUSE_ADDRESSES.history.funding_payment,
        funding_rate_history=CLEARING_HOUSE_ADDRESSES.history.funding_rate,
        oracle=CURRENT_MARKETS[market_index].mainnet_pyth_oracle,
        program_id=CLEARING_HOUSE_ADDRESSES.program
    )
    rpc_response = await sign_and_send_transaction_instructions(
        client=client,
        keypair=wallet,
        transaction_instructions=[transaction_instruction],
        commitment=commitment
    )
    return rpc_response


async def send_settle_funding_payment(
        client: SolanaClient, commitment: Commitment, wallet: Keypair, user_positions: PublicKey
) -> RPCResponse:
    """Send a settle-funding-payment instruction."""
    instruction_object = SettleFundingPaymentInstruction()
    user = get_user_account_address(
        authority=wallet.public_key
    )
    transaction_instruction = instruction_object.get_instruction(
        state=CLEARING_HOUSE_ADDRESSES.state,
        user=user,
        markets=CLEARING_HOUSE_ADDRESSES.markets,
        user_positions=user_positions,
        funding_payment_history=CLEARING_HOUSE_ADDRESSES.history.funding_payment,
        program_id=CLEARING_HOUSE_ADDRESSES.program
    )
    rpc_response = await sign_and_send_transaction_instructions(
        client=client,
        keypair=wallet,
        transaction_instructions=[transaction_instruction],
        commitment=commitment
    )
    return rpc_response


async def send_withdraw_collateral(
        client: SolanaClient, commitment: Commitment, wallet: Keypair, amount: int, user_positions: PublicKey,
        user_collateral_account: PublicKey
) -> RPCResponse:
    """Send a withdraw-collateral instruction."""
    instruction_object = WithdrawCollateralInstruction.from_user_precision(
        amount=amount
    )
    user = get_user_account_address(
        authority=wallet.public_key
    )
    transaction_instruction = instruction_object.get_instruction(
        state=CLEARING_HOUSE_ADDRESSES.state,
        user=user,
        authority=wallet.public_key,
        collateral_vault=CLEARING_HOUSE_ADDRESSES.collateral_vault,
        collateral_vault_authority=CLEARING_HOUSE_ADDRESSES.collateral_vault_authority,
        insurance_vault=CLEARING_HOUSE_ADDRESSES.insurance_vault,
        insurance_vault_authority=CLEARING_HOUSE_ADDRESSES.insurance_vault_authority,
        user_collateral_account=user_collateral_account,
        token_program=TOKEN_PROGRAM_ID,
        markets=CLEARING_HOUSE_ADDRESSES.markets,
        user_positions=user_positions,
        funding_payment_history=CLEARING_HOUSE_ADDRESSES.history.funding_payment,
        deposit_history=CLEARING_HOUSE_ADDRESSES.history.deposit,
        program_id=CLEARING_HOUSE_ADDRESSES.program
    )
    rpc_response = await sign_and_send_transaction_instructions(
        client=client,
        keypair=wallet,
        transaction_instructions=[transaction_instruction],
        commitment=commitment
    )
    return rpc_response
