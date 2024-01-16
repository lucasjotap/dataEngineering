import logging
import requests

from typing import Any
from backoff import on_exception, constant
from ratelimit import limits, RateLimitExcepetion

class SoulWhisper:
	logging.getLogger().setLevel(logging.INFO)

	@on_exception(constant,
				  requests.exception.HTTPError,
				  max_tries=3,
		          interval=10)
	@limits(calls=20, period=60)
	@on_exception(constant, RateLimitExcepetion, interval=60, max_treis=3)
	def get_daily_summary(self, coin, year, month, day) -> dict:

		ENDPOINT: str = f"https://www.mercadobitcoint.net/api/{coin}/day-summary/{year}/{month}/{day}"

		logging.info(f"Fetching data from API with: {ENDPOINT}")

		reponse = requests.get(ENDPOINT)
		reponse.raise_for_status()

		return reponse.json()

if __name__ == "__main__":
	soul_whisper_object: Any = SoulWhisper()
	result = soul_whisper_object.get_daily_summary()
	print(result)