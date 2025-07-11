import requests
import time
import sys

# Your BlockCypher API token
API_TOKEN = "d4645d23f3784b288604d366b914a88b"

def get_address_balance(address, coin_symbol):
    """
    Retrieve balance for a single cryptocurrency address with API token.
    
    Args:
        address (str): Cryptocurrency address
        coin_symbol (str): 'btc', 'ltc', or 'doge'
    
    Returns:
        float: Balance in main units (BTC, LTC, or DOGE)
    """
    url = f"https://api.blockcypher.com/v1/{coin_symbol}/main/addrs/{address}"
    params = {'token': API_TOKEN}
    
    max_retries = 3
    retry_delay = 1  # Initial delay in seconds
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            
            # Handle rate limiting (429) specifically
            if response.status_code == 429:
                # Get Retry-After header or use default
                retry_after = int(response.headers.get('Retry-After', 3))
                print(f"Rate limited. Retrying in {retry_after} seconds... (Attempt {attempt+1}/{max_retries})")
                time.sleep(retry_after)
                continue
                
            response.raise_for_status()
            data = response.json()
            
            if 'final_balance' in data:
                balance = data['final_balance'] / 10**8
                print(f"{address} balance: {balance:.8f} {coin_symbol.upper()}")
                return balance
            elif 'error' in data:
                print(f"Error for {address} ({coin_symbol.upper()}): {data['error']}")
                return 0.0
            else:
                print(f"No balance found for {address} ({coin_symbol.upper()})")
                return 0.0
                
        except requests.exceptions.RequestException as e:
            print(f"Network error for {address} ({coin_symbol.upper()}): {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds... ({attempt+1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 1.5  # Exponential backoff
            else:
                print(f"Failed to get balance for {address} after {max_retries} attempts")
                return 0.0
                
    return 0.0

def get_coin_balance(addresses, coin_symbol):
    """
    Retrieve total balance for a list of addresses in a specific cryptocurrency.
    
    Args:
        addresses (list): List of cryptocurrency addresses
        coin_symbol (str): 'btc', 'ltc', or 'doge'
    
    Returns:
        float: Total balance in main units (BTC, LTC, or DOGE)
    """
    if not addresses:
        return 0.0
        
    total_balance = 0
    
    print(f"\nChecking {coin_symbol.upper()} balances:")
    for i, address in enumerate(addresses):
        # Add small delay between requests (0.2 seconds = 5 requests/second)
        if i > 0:
            time.sleep(0.2)
            
        balance = get_address_balance(address, coin_symbol)
        total_balance += balance
    
    return total_balance

# Example usage
if __name__ == "__main__":
    # Replace with your actual addresses
    btc_addresses = [
    "bc1qa8z45j9hvuhfwd8qmu53f3g0ws6q4vyrevw7j9",
    "bc1q86unvjpv0rrytvqereuq00hr9c6l84a74fx534",
    "bc1qg64736kfrc0ypgz6200c0tfnemwdvd8653axxa",
    "36VMKgAofcX8RGKPoME8rh8wcooVnVe8zU",
    "3QEQfH32wEfrcWJM6NidmVC4MnLREzufzs",
    "bc1qrepd2k8svmgl7770a74c8y47jerdxtqp8tvgd3",
    "bc1qnsqzzxs6pjpxqge3g2nxxv0qsrp9dse5fx062s",
    "3CRpkqnnmYqRQn6yavXZxxbTs2m5vhfiTF",
    "bc1q3a0xxx78njk4autp3x0hj57nmtfw4t6wflwznp",
    ]
    
    ltc_addresses = [
    "ltc1qjznz24qse3t5avv8g4k3qfn7lkx9ecs8pl9qlv",
    "ltc1qjeshkxces4vpzleesy60aq4aecnmnkgj5lh7tf",
    "ltc1qucepjjx0lnzvw65zg8dnl0crftjeggnh4p36tp",
    "ltc1qxy2t00wgj52jgt8lkl7ul088u6zsmecufwf6qa",
    "MRR2dfd8in2qvLZg2AjD4ph5nE7dU7BdTU",
    "ltc1q57gd34vgczr9txgfc6erk870txrtp8qya3h7wc",
    "MLa7esUBQGCctDDLWD9tJZVXgxLQ32Uijo",
    "ltc1qv9nk68uctktygwkgylh3mupfn8pajdt0mx8wlq",
    "ltc1ql3tv4rau8dpsw97czhms9cacafqxlcyasgxqgu",
    "ltc1qff7twweky2qwezq2sa7d2d82k2dfc5jqxv0a93",
    "ltc1q7g5yefwcwuag9d52d2dczfv857vaf9zclqhcx9",
    "ltc1qma4shep4px57pvg8dkrefvujf25fglt4d4hxst",
    ]
    
    doge_addresses = [
    "D67wgem1UPyYFZyMLNNY5Fs97e6TDHcjFL",
    "D6KEnZKetQKArUWxyPUrSfZPC5ZUY5Z2z1",
    "D8hJf2hGogy4URyXhfc5CU5b8rvffKmXFt",
    "DAehf1NBvLE4tZ55XgkZijLJxgwSo6Ks8P",
    "DFNiGSAXm5M42bL8RvYURdPNK2Gb1tLgiY",
    "DM5EVnBLQzZvSCWXErWMgntdF5G6X9XeXT",
    "DRqGxLmW9nsNt23C9TCPXKL4avqSsStGMB",
    "DTH48gZPMGes5VrqwV3Katc9oWz4hU5JJE",
    "DAyoyubDZYvziRn1twFtfb3ZSfgghnsP8z",
    "DC2PYUSWRCb9gjq3Siz7kanZ5H9aQbykmx",
    "DQERJscohfevQFhfcsGg5jHzFN4NWMQQ5Q",
    "D7oHgmgeZmnG7bTysnUWiHLK2R9CmySYB3",
    "DB7UdL7TgWcnnuvKzvB7HgkrhNxYEQVqW8",
    "DHGsmZ3kZx4de6jwnZnTCj9SACHQ9e9MQ1",
    "DDUi235sstedgBL9s9zDkNNJp1kR5gFRoH",
    "DQz2TrajjjVXaZgkwXKHnSsRjcFKCkgHiL",
    "DLzRo3Aem1m8QVDag11ZkmZb1c5Zgps1mN",
    "DFTCLBQkC8MF8vkt6EuaAeaVpzPqh6bL2E",
    "DHifmgZYN3rY13abj6KPFTsE93YAMtPVoH",
    "DCebtwwq3ucA5pEEpRb82HZQsEjvrzD3L3",
    "D7QR3pGcuvTCBggMt2btZbAz4egev71piW",
    "DEkCNtkFyYN1392vpkz8wpou7gFdRR95Pa",
    "DRMMmUPKoqyajrjckXkVRUqUNq1ccYPD2G",
    "DQ2hhV8LvhrH7FTEEvxxP6J5psWq4kPxhy",
    "DMvrtq3TaScP2E8tGjtPSpbAJbqrzhw8wS",
    "D67HvqSupKdMTSHmciFp9DWwpuLfehDLtg",
    "DCYtvP63ysARAPdSL63HDDsvv3WZHqR9qN",
    "D6L7LrTFy8GMqpT7tfVk61NLF6MXPJcdBU",
    "D93c4bBV5jrqinF2SH7p2AYntdZSeHRD76",
    "DRbC7T4ACQ6tctgM63DkMCDAdnHQEBFG9X",
    "DKSpkDozX6Txikts3o8nzcRSmiQXsToXbo",
    "D6HU7Fjg4J8pwzAJzrBMkJUajXHfZEzEZP",
    ]
    
    
    print("Starting balance check with API token...\n")
    
    try:
        # Process each cryptocurrency
        btc_total = get_coin_balance(btc_addresses, "btc")
        ltc_total = get_coin_balance(ltc_addresses, "ltc")
        doge_total = get_coin_balance(doge_addresses, "doge")
        
        print("\nTotal Balances:")
        print(f"BTC Total: {btc_total:.8f}")
        print(f"LTC Total: {ltc_total:.8f}")
        print(f"DOGE Total: {doge_total:.8f}")
        
        print("\nBalance check completed successfully!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)

input("Press Enter to exit...")