
import warnings
from urllib3.exceptions import NotOpenSSLWarning

warnings.filterwarnings("ignore", category=NotOpenSSLWarning) # You don't need the first three lines if you have OpenSSL installed

import time
import sys
import requests
import argparse
import logging

# creating a log file
logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--url')
	parser.add_argument('--timeout', type=int, default=10)
	parser.add_argument('--retries', type=int, default=3)
	parser.add_argument('--sleep', type=int, default=3)
	args = parser.parse_args()

	url = args.url
	timeout_s = args.timeout
	max_tries = args.retries
	sleep_duration_s = args.sleep

	status_code = None
	result = 'NOK'

	for attempt in range(1, max_tries + 1):
		start_time = time.perf_counter()

		try:
			response = requests.get(url, timeout=timeout_s)
			end_time = time.perf_counter()
			time_ms = (end_time - start_time) * 1000
			response_time = f"{time_ms:.2f}"
			status_code = response.status_code

			if status_code == 200:
				result = 'OK'
				logging.info(f"Attempt {attempt}: Response Code: {status_code}, Result: {result}, Response Time: {response_time} ms")
				break
			else:
				result = 'NOK'
				logging.warning(f"Attempt {attempt}: Non-200 Response Code: {status_code}, retrying after {sleep_duration_s} seconds")

			

		except requests.exceptions.RequestException as error:
			end_time = time.perf_counter()
			time_ms = (end_time - start_time) * 1000
			response_time = f"{time_ms:.2f}"

			logging.warning(f"Attempt {attempt} failed: {error}, retrying after {sleep_duration_s} seconds")

			if attempt < max_tries:
				time.sleep(sleep_duration_s)
			else:
				logging.error(f"All attempts failed: {error}")

	print(f"Response code: {status_code if status_code else 'None'}")
	print(f"Result: { result }")
	print(f'Response time: { response_time } ms')


	if result == 'OK':
		sys.exit(0)
	elif status_code is not None:
		sys.exit(2)
	else:
		sys.exit(1)

if __name__ == '__main__':
	main()
