import asyncio

from typing import List

from solana.rpc.async_api import AsyncClient
from solana.transaction import TransactionInstruction, Transaction
from solana.rpc.types import TxOpts, RPCResponse
from solana.publickey import PublicKey
from solana.keypair import Keypair

from sdk.constants import *
from sdk.instructions.all import *
from sdk.utils import get_user_account_address


async def sign_and_send_transaction_instructions(client: AsyncClient, keypair: Keypair,
                                                 transaction_instructions: List[TransactionInstruction]) -> RPCResponse:
    signers = [keypair]
    transaction = Transaction(
        fee_payer=keypair.public_key
    )
    transaction.add(*transaction_instructions)
    transaction_options = TxOpts(
        preflight_commitment='single'
    )
    response = await client.send_transaction(
        txn=transaction,
        *signers,
        opts=transaction_options
    )
    return response


async def close_position(client: AsyncClient, wallet: Keypair, market_index: int,
                         user_positions: PublicKey) -> RPCResponse:
    instruction_object = ClosePositionInstruction(
        market_index=market_index
    )
    user = get_user_account_address(authority=wallet.public_key)
    transaction_instruction = instruction_object.get_instruction(
        state=CLEARING_HOUSE_ADDRESSES.state,
        user=user,
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
        transaction_instructions=transaction_instruction
    )
    return rpc_response


async def delete_user(client: AsyncClient, wallet: Keypair, user_positions: PublicKey) -> RPCResponse:
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
        transaction_instructions=transaction_instruction
    )
    return rpc_response


async def deposit_collateral(client: AsyncClient, wallet: Keypair, amount: int, user_collateral_account: PublicKey,
                             user_positions: PublicKey) -> RPCResponse:
    instruction_object = DepositCollateralInstruction(
        amount=amount
    )
    user = get_user_account_address(
        authority=wallet.public_key
    )
    transaction_instruction = instruction_object.get_instruction(
        state=CLEARING_HOUSE_ADDRESSES.state,
        user=user,
        authority=wallet,
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
        transaction_instructions=transaction_instruction
    )
    return rpc_response


async def liquidate(client: Client, wallet: Keypair, liquidator: PublicKey, user_positions: PublicKey) -> RPCResponse:
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
        transaction_instructions=transaction_instruction
    )
    return rpc_response


async def open_position(client: Client, wallet: Keypair, direction, quote_asset_amount: int, market_index: int,
                        limit_price: int, user_positions: PublicKey) -> RPCResponse:
    instruction_object = OpenPositionInstruction(
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
        oracle=CURRENT_MARKETS[market_index].mainnet_pyth_oracle
    )
    rpc_response = await sign_and_send_transaction_instructions(
        client=client,
        keypair=wallet,
        transaction_instructions=transaction_instruction
    )
    return rpc_response


async def settle_funding_payment(client: Client, wallet: Keypair, user_positions: PublicKey) -> RPCResponse:
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
        transaction_instructions=transaction_instruction
    )
    return rpc_response


async def withdraw_collateral(client: Client, wallet: Keypair, amount: int, user_positions: PublicKey,
                              user_collateral_account: PublicKey) -> RPCResponse:
    instruction_object = WithdrawCollateralInstruction(
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
        transaction_instructions=transaction_instruction
    )
    return rpc_response