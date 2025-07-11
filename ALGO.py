import requests
import sys

def get_algo_balance(address):
    """
    Retrieve ALGO balance for a single address using AlgoNode API.
    
    Args:
        address (str): Algorand address
    
    Returns:
        float: Balance in ALGO
    """
    url = f"https://mainnet-api.algonode.cloud/v2/accounts/{address}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Convert from microAlgos to ALGO (1 ALGO = 1,000,000 microAlgos)
        micro_algos = data.get('amount', 0)
        balance = micro_algos / 10**6
        
        print(f"{address} balance: {balance:.6f} ALGO")
        return balance
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching balance for {address}: {str(e)}")
        return 0.0
    except KeyError:
        print(f"Invalid response format for {address}")
        return 0.0

def get_total_algo_balance(addresses):
    """
    Retrieve total ALGO balance for a list of addresses.
    
    Args:
        addresses (list): List of Algorand addresses
    
    Returns:
        float: Total balance in ALGO
    """
    if not addresses:
        return 0.0
        
    total_balance = 0
    
    print("\nChecking ALGO balances:")
    for address in addresses:
        balance = get_algo_balance(address)
        total_balance += balance
    
    return total_balance

# Example usage
if __name__ == "__main__":
    # Replace with your actual Algorand addresses
    algo_addresses = [
"R5POM57UREJ7OKDVT3TQJJ2DXTQDCCJUZGB4DYPOBNJCZTDZKGYREXTTHI",
"2AGVAPVS7BAVSXUJHC5B4ILIUW25E4SFCWDYQOBEPZLDT5X6QN5DELYWTA",
"4U7HCPVHVAFZHMFLBH6ZPHHG6332JAUREL7VYEIVZUN3U5Q5NZIOXLW2B4",
"INMOXCSQEKTOG5RLM2FTJOENNLMR7VUBWH23I67NEDQJ6HQEUKDFUCWIS4",
"D5CK3YWIEYDUTOHU2XKACOF5UUMLA2CLQ6OIQMYCBZ3DYEFYHQRVHGUCCE",
"JU555AXLCUC3WSQWYP3Q4DIBTTKB7JB4N5PLDR4LK7GYAGLN2DE6W5RH2M",
"HDGFCEMKUZJUKWV63X64QDBE7TXV7V5OI6LQAGH4JELJAGI55G4A",
"LQDNQE3I5C3E3QJYHJWQZ3OPFO6AIMD3F7CKYQ3MOTCDQISFS5TA",
"7YZTYPX73SOLABDE7V27MKGU2IZOL2GWP443AHQTO2O2ODWPOZDWH4SEBY",
"7MD42UXGBLLCJD2N3TUQA2N5KCHBS362YRK4ABRJR75RVAVG5LJCPO77WE",
"H6V2ONQOPRDPZBZM3SXZ3U73VOCKO66KFJTWDJWY32VJQUU6QRVECQ54A4",
"7C7TKT7QSITKJ6DASG6ZKTUMCW5BW257XY3VBSH6NE5FJ7XEERB2AGSARI",
"VASSKNZRW2XATRND764IVW5HLIC37UKV4LMABTVNT2AX6GRKTR2O22XTHE",
"TGBWWZMTM7UVUUTLFUX2FT6J46JNIPFEZ3ESOVAU6F5VSEPQQQ6YM24VEQ",
"TKL7Q47Y4VQVYU7A3VR2TKHVCKDDBW5CETPDCHAI5HEICBN4JFAA4VOTE4",
"UT5PCDL7JC24IRZ3CLLUG2KFZCB6Y6J54NFYKNDWNLZBPDOI444QX6NKMA",
"MLZQEAJVKPRZAYOOGSRI4E34CN2JXIK3YNCLCTINNCLWW4OIANZ6RN7DCI",
"5ST2VJ7IPAHXEVD46QAPEWNDQ6TISVXYT7HGUGIVBQSP65WVVLUDYQQ66E",
"MLDMS5L4DKDZYMODWCGTZ3TXHDYZ53IK6RAPZCP5ZIQWF6YPRQOQJPQEJI",
"2ME4ZYT7COT4GMTB4DLKK3ZHZBGYIUMOBKHKIPMNSV4QFEFWVEDMMEV4LU",
"PIANWSHP4RDMB6CO63XKNML6ECQHHCD4TKJ3BLDWHA2V6WVSOZJOAD4EE4",
"CJVPSYZEVVCMTPAYQM4O6HTFRUJ2RKZWILLK7K36KR2QWBFB5FHT6XTH7E",
"DZG32GDZJ7GKW73ACN7RANMD3HYL2H7A2RP2BZTN25U46U4IRUDUQNN3GQ",
"OFUTCBUL5YUSDSWCMIT7XUG6BT4TZJVLB65CNGMPZ475KB3PEQJQPD6ZCE",
"6GBDG7ZJNG5YTEECLGMZCLIC2VODV74XDRVU3P5RLYJWKZX74AR3OVBQRA",
    ]
    
    print("Starting ALGO balance check...\n")
    
    try:
        total_algo = get_total_algo_balance(algo_addresses)
        
        print(f"\nTotal ALGO Balance: {total_algo:.6f}")
        print("\nBalance check completed successfully!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)

input("Press Enter to exit...")