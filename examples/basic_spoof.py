from orb.config import OrbConfig
from orb.scraper.utils import spoof_request

if __name__ == "__main__":
    config = OrbConfig.from_env()
    response = spoof_request("https://example.com", config=config)
    print(response.status_code)
