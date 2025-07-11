import requests
import sys

def get_sol_balance(address):
    """
    Retrieve SOL balance for a single Solana address.
    
    Args:
        address (str): Solana wallet address
    
    Returns:
        float: Balance in SOL
    """
    # Solana JSON-RPC endpoint
    url = "https://api.mainnet-beta.solana.com"
    
    # JSON-RPC request payload
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [address]
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Check for errors in response
        if 'error' in data:
            print(f"Error for {address}: {data['error']['message']}")
            return 0.0
            
        # Extract balance in lamports
        lamports = data['result']['value']
        
        # Convert from lamports to SOL (1 SOL = 1,000,000,000 lamports)
        balance = lamports / 10**9
        
        print(f"{address} balance: {balance:.9f} SOL")
        return balance
            
    except requests.exceptions.RequestException as e:
        print(f"Network error for {address}: {str(e)}")
        return 0.0
    except KeyError:
        print(f"Invalid response format for {address}")
        return 0.0

def get_total_sol_balance(addresses):
    """
    Retrieve total SOL balance for a list of addresses.
    
    Args:
        addresses (list): List of Solana addresses
    
    Returns:
        float: Total balance in SOL
    """
    if not addresses:
        return 0.0
        
    total_balance = 0
    
    print("\nChecking SOL balances:")
    for address in addresses:
        balance = get_sol_balance(address)
        total_balance += balance
    
    return total_balance

# Example usage
if __name__ == "__main__":
    # Replace with your actual Solana addresses
    sol_addresses = [
"8o1AwgNcWJoozZ3kkTXE5hY6njrQafR6edCEFSaR4RBo",
"EfHraskgbJVyk2Rz7C5GnV57zHcaMPAyiurKmnc26vFJ",
"2YBnRHRp9YdCJhsJVMETB39G6guazTYx52MTcBrDJLTU",
"9exe2bM8j6rH4nBUHqwnKhZwPDKdDNdK7eRpbAc5w9nd",
"E2MZopHkhuKqiJB18eBoRKwfpS87Z421MEREopmzit98",
"2VrwjLn8JX1CSyDfhKoSyxm7pzHb5cQBhpcV9ns8zhmJ",
"4NCZCHhHMQZQeAohHgvJGxHw4eSLC4Y4Cpo2rWtUutWF",
"9GmNWnKQwAXhjVXW62dciYLZRn9iFKoBvNtw6gcZca25",
"CzCBz16JWyvbnih7ATZ68seFeEviogcw6dLSuiuN21Yt",
"62vVRTeBTMfdWAP4488JgNkpHgxLYoVvXTzzC8D7jqTt",
"7KwjkNniZV8Podu7UypccfLfoUAP2MjUjSPZBNd9EaHP",
"6TiAzQAkSeSZwqB6LUaSHGtsxcu1T1uMVYoz5i21zhfR",
"AMFXFCL4VDKQx3Ncd8kBoJARNEbKT8da2XDYCYpMDzVB",
"GWXGvhzEknyxmfVsHNhoD3FFjb6Sc6Pnx9qWB959ZJQs",
"BpmD5aqDxPcQooki2P8ykSEhNPjkzZuETua12jKcvXDT",
"GLqegWeT6fAfTebUrBdyBnpz74JZDCRNdNGnP1SnTmKe",
    ]
    
    print("Starting SOL balance check...\n")
    
    try:
        total_sol = get_total_sol_balance(sol_addresses)
        
        print(f"\nTotal SOL Balance: {total_sol:.9f}")
        print("\nBalance check completed successfully!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)

input("Press Enter to exit...")
