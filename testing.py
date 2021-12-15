"""Testing the drift client."""
import asyncio
from os import environ
from sdk.client import DriftClient
from sdk.constants import SERUM_ENDPOINT


async def main():
	"""Test function."""
	drift_client = await DriftClient.create(
		private_key=environ['SOLANA_WALLET_PRIVATE_KEY'],
		endpoint=SERUM_ENDPOINT
	)
	market = await drift_client.get_market(
		symbol='BNB-PERP'
	)
	print(market)

	await drift_client.close()

if __name__ == '__main__':
	asyncio.run(main())
