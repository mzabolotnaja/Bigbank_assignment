import time
import sys
import requests
import argparse


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

	start_time = time.perf_counter()

	for attempt in range(1, max_tries + 1):
		try:
			response = requests.get(url, timeout=timeout_s)
			end_time = time.perf_counter()
			time_ms = (end_time - start_time) * 1000
			response_time = f"{time_ms:.2f}"
			status_code = response.status_code
			result = 'OK' if status_code == 200 else 'NOK'

			break

		except requests.exceptions.RequestException as error:
			end_time = time.perf_counter()
			time_ms = (end_time - start_time) * 1000
			response_time = f"{time_ms:.2f}"
			if attempt < max_tries:
				print(f"Attempt {attempt} failed, trying again..")
				time.sleep(sleep_duration_s)
			else:
				print('All attempts failed')
				print(error)

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
