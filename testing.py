from os import environ
from sdk.client.sync import DriftClient

# instantiate a client with a private key for your Solana wallet
drift_client = DriftClient.create(
    private_key=environ['SOLANA_WALLET_PRIVATE_KEY'],
)

print('client:')
print(drift_client, '\n')

user_account = drift_client.call_user_account(,

print('user account:')
print(user_account)