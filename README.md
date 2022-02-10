# Drift-py

**DEPRECATED** please see https://github.com/drift-labs/driftpy

A python software developer kit for interacting with the [Drift Protocol](https://www.drift.trade/). The package can
also be used for research purposes to simulate transactions and events on the protocol, battle-testing it in 
unique scenarios.

## Setup

recommend using [`virtualenv`](https://formulae.brew.sh/formula/virtualenv)

```sh
virtualenv venv # creates a virtualenv called "venv"
source venv/bin/activate # uses the virtualenv
pip install -r requirements.txt
```
## General Usage
### Instantiating a Client

```py
from os import environ
from sdk.client import DriftClient

# instantiate a client with a private key for your Solana wallet
drift_client = DriftClient.create(
	private_key=environ['SOLANA_WALLET_PRIVATE_KEY'],
	endpoint='https://api.mainnet-beta.solana.com'
)
```
### Reading Protocol Data

```python
market = drift_client.call_market(,
print(market)
```
