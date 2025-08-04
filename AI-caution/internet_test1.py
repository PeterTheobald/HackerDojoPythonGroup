import argparse
import logging
import time
import requests
import yaml

CONFIG_FILE = 'internet_test.yaml'
LOG_FILE = 'internet_test.log'

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)

def run_test(url, num_tests, debug=False):
    logger = logging.getLogger()
    logger.info(f"Starting test: {num_tests} requests to {url}")
    start = time.time()
    for i in range(num_tests):
        if debug:
            logger.debug(f"Request {i+1}/{num_tests} to {url}")
        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except Exception as e:
            logger.error(f"Request {i+1} failed: {e}")
    duration = time.time() - start
    logger.info(f"Test completed in {duration:.2f} seconds.")
    return duration

def main():
    parser = argparse.ArgumentParser(description='Internet test script')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.DEBUG if args.debug else logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )
    logger = logging.getLogger()

    config = load_config()
    url = config['test_url']
    num_tests = config['num_tests']
    logger.info(f"Loaded config: url={url}, num_tests={num_tests}")
    run_test(url, num_tests, args.debug)

if __name__ == '__main__':
    main()
