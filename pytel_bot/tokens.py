import os


def get_tokens():
    if "PYTEL_TELEGRAM" not in os.environ:
        exit("Error: Required Telegram token...\nExit...")
    if "PYTEL_CONSUMER_KEY" not in os.environ:
        exit("Error: Required Twitter Consumer Key...\nExit...")
    if "PYTEL_CONSUMER_SECRET" not in os.environ:
        exit("Error: Required Twitter Consumer Secret...\nExit...")
    if "PYTEL_ACCESS_TOKEN" not in os.environ:
        exit("Error: Required Twitter Access Token...\nExit...")
    if "PYTEL_ACCES_TOKEN_SECRET" not in os.environ:
        exit("Error: Required Twitter Access Token Secret... \nExit...")
    if 'API_KEY' not in os.environ:
        exit("Error: Required LastFM API key... \nExit...")
    if 'SHARED_SECRET' not in os.environ:
        exit("Error: Required LastFM Shared Secret token... \nExit...")
    return {
        "telegram": os.environ["PYTEL_TELEGRAM"],
        "consumer_key": os.environ["PYTEL_CONSUMER_KEY"],
        "consumer_secret": os.environ["PYTEL_CONSUMER_SECRET"],
        "access_token": os.environ["PYTEL_ACCESS_TOKEN"],
        "access_token_secret": os.environ["PYTEL_ACCES_TOKEN_SECRET"],
        "api_key": os.environ["API_KEY"],
        "shared_secret": os.environ["SHARED_SECRET"]
    }
