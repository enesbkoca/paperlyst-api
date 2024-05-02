import logging
from service import DoiFetcherService

def main():
    doi_fetcher_service = DoiFetcherService()
    doi_fetcher_service.consume_messages()

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()