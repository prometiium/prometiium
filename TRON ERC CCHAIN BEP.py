import requests
import time
import json
from web3 import Web3
from typing import Tuple, List
from tronpy import Tron
from tronpy.providers import HTTPProvider

# ===== Configuration =====
ETHERSCAN_API_KEY = "ZF9B4Q343IZDVA51EYFTR5F5JZ9INSKNGI"
BSC_RPC = "https://bsc-dataseed.binance.org/"
CCHAIN_RPC = "https://api.avax.network/ext/bc/C/rpc"
TRONGRID_API_KEY = "7779ab56-6159-4832-bee5-0aad6a2c8c7b" 

ADDRESSES = [
    "TN3t8tMENquQzQ2ZUrkFURvACtpKbYa94V",
    "0xD3C3Ad850347A43b0c99ad3C144Bfe58fad5aCcB",
    "0x13271ADF8C9753547b98501B684ad892B33Dc0b7",
]

# ===== Verified Token Lists =====
AVAX_TOKENS = [
    ("AVAX", None, 18),  # Native token
    ("USDT", "0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7", 6),
    ("USDC", "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E", 6),
    ("PNG", "0x60781C2586D68229fde47564546784ab3fACA982", 18),
    ("GAU", "0xca8ebfb8e1460aaac7c272cb9053b3d42412aac2", 18),
    ("ICPX", "0xd78d3D08053130A3b4466e15D8fc2a61a3DeE47d", 6),
    ("JOE", "0x6e84a6216ea6dacc71ee8e6b0a5b7322eebc0fdd", 18),
    ("OILX", "0xd5CcFDfbc0eFF28EbE310b9b28b627Cfc39EaBc7", 6),
    ("XAGX", "0x2C472e913635c85143369aDc9962bbB56Efc446A", 6),
]

ERC20_TOKENS = [
    ("ETH", None, 18),  # Native token
    ("USDT", "0xdac17f958d2ee523a2206206994597c13d831ec7", 6),
    ("FLOKI", "0x43f11c02439e2736800433b4594994bd43cd066d", 9),
    ("FTT", "0x50d1c9771902476076ecfc8b2a83ad6b9355a4c9", 18),
    ("ILV", "0x767fe9edc9e0df98e07454847909b5e959d7ca0e", 18),
    ("MKR", "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2", 18),
    ("LDO", "0x5a98fcbea516cf06857215779fd812ca3bef1b32", 18)
]

BSC_TOKENS = [
    ("BNB", None, 18),  # Native token
    ("USDT", "0x55d398326f99059ff775485246999027b3197955", 18),
    ("PIT", "0xa57ac35ce91ee92caefaa8dc04140c8e232c2e50", 9),
    ("CAKE", "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82", 18),
    ("ETH", "0x2170ed0880ac9a755fd29b2688956bd959f933f8", 18),
    ("CEEK", "0xe0f94ac5462997d2bc57287ac3a3ae4c31345d66", 18),
    ("ATOM", "0x0EB3a705fc54725037CC9e008bdede697F62F335", 18)
]

TRC20_TOKENS = [
    ("TRX", None, 6),  # Native token
    ("USDT", "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t", 6),
    ("USDC", "TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8", 6),
    ("BTT", "TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4", 18),
    ("JST", "TCFLL5dx5ZJdKnWuesXxi1VPwjLVmWZZy9", 18),
    ("SUN", "TSSMHYeV2uE9qYH95DqyoCuNCzEL1NvU3S", 18),
    ("WIN", "TLa2f6VPqDgRE67v1736s7bJ8Ray5wYjU7", 6)
]

# ===== Core Functions =====
def get_avax_balance(w3: Web3, address: str, contract: str, decimals: int) -> float:
    try:
        if contract is None:  # AVAX native
            balance = w3.eth.get_balance(Web3.to_checksum_address(address))
            return balance / (10 ** 18)
        
        token_abi = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]'
        token = w3.eth.contract(
            address=Web3.to_checksum_address(contract),
            abi=token_abi
        )
        balance = token.functions.balanceOf(Web3.to_checksum_address(address)).call()
        return balance / (10 ** decimals)
    except Exception as e:
        print(f"  ❌ Error fetching {contract[:10] if contract else 'AVAX'}...: {str(e)[:100]}")
        return 0.0

def get_eth_balance(address: str) -> float:
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return int(data["result"]) / 1e18 if data.get("status") == "1" else 0.0
    except Exception as e:
        print(f"  ❌ ETH Error: {str(e)[:100]}")
        return 0.0

def get_erc20_balance(address: str, contract: str, decimals: int) -> float:
    if contract is None:  # ETH native
        return get_eth_balance(address)
    
    url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={contract}&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return int(data["result"]) / (10 ** decimals) if data.get("status") == "1" else 0.0
    except Exception as e:
        print(f"  ❌ ERC20 Error {contract[:10]}...: {str(e)[:100]}")
        return 0.0

def get_bsc_balance(w3: Web3, address: str, contract: str, decimals: int) -> float:
    try:
        if contract is None:  # BNB native
            balance = w3.eth.get_balance(Web3.to_checksum_address(address))
            return balance / (10 ** 18)
        
        token_abi = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]'
        token = w3.eth.contract(
            address=Web3.to_checksum_address(contract),
            abi=token_abi
        )
        balance = token.functions.balanceOf(Web3.to_checksum_address(address)).call()
        return balance / (10 ** decimals)
    except Exception as e:
        print(f"  ❌ BSC Error {contract[:10] if contract else 'BNB'}...: {str(e)[:100]}")
        return 0.0

def get_trx_balance(client: Tron, address: str) -> float:
    """Get native TRX balance"""
    try:
        if not client.is_address(address):
            print(f"  ❌ Invalid TRON address: {address}")
            return 0.0
            
        # Fonksiyon zaten TRX cinsinden döndürüyor, bölme yapmaya gerek yok
        balance = client.get_account_balance(address)
        return float(balance)  # Direkt float'a çevir
    except Exception as e:
        if "Account not found" in str(e):
            return 0.0
        print(f"  ❌ TRX Error: {str(e)[:100]}")
        return 0.0

def get_trc20_balance(client: Tron, address: str, contract: str, decimals: int) -> float:
    """Get TRC20 token balance"""
    try:
        if contract is None:  # TRX native
            return get_trx_balance(client, address)
            
        contract_obj = client.get_contract(contract)
        balance = contract_obj.functions.balanceOf(address)
        return float(balance) / (10 ** decimals)  # Sadece tokenlar için decimals kullan
    except Exception as e:
        print(f"  ❌ TRC20 Error {contract[:10] if contract else 'TRX'}...: {str(e)[:100]}")
        return 0.0

# ===== Main Execution =====
def main():
    print("🔍 Starting Multi-Chain Portfolio Scan")
    print(f"📋 Addresses to check: {', '.join([addr[:6]+'...'+addr[-4:] for addr in ADDRESSES])}\n")
    
    # Initialize Web3 connections
    avax_w3 = Web3(Web3.HTTPProvider(CCHAIN_RPC))
    bsc_w3 = Web3(Web3.HTTPProvider(BSC_RPC))
    
    if not avax_w3.is_connected():
        print("❌ Failed to connect to Avalanche RPC")
        return
    if not bsc_w3.is_connected():
        print("❌ Failed to connect to BSC RPC")
        return

    # Initialize Tron client
    tron_client = Tron(HTTPProvider(api_key=TRONGRID_API_KEY))

    # Initialize totals
    totals = {
        'avax': {token[0]: 0.0 for token in AVAX_TOKENS},
        'eth': {token[0]: 0.0 for token in ERC20_TOKENS},
        'bsc': {token[0]: 0.0 for token in BSC_TOKENS},
        'tron': {token[0]: 0.0 for token in TRC20_TOKENS}
    }

    for address in ADDRESSES:
        print(f"\n🔷 Scanning full address: {address}")
        start_time = time.time()
        
        # Determine chain by address format
        is_tron = address.startswith('T') and len(address) == 34
        
        # AVAX C-Chain (skip TRON addresses)
        if not is_tron:
            print("\n  🌋 Avalanche:")
            for symbol, contract, decimals in AVAX_TOKENS:
                bal = get_avax_balance(avax_w3, address, contract, decimals)
                if bal > 0:
                    print(f"    {symbol}: {bal:.6f}")
                    totals['avax'][symbol] += bal

            # Ethereum
            print("\n  🔷 Ethereum:")
            for symbol, contract, decimals in ERC20_TOKENS:
                bal = get_erc20_balance(address, contract, decimals)
                if bal > 0:
                    print(f"    {symbol}: {bal:.6f}")
                    totals['eth'][symbol] += bal

            # BSC
            print("\n  🍌 Binance Smart Chain:")
            for symbol, contract, decimals in BSC_TOKENS:
                bal = get_bsc_balance(bsc_w3, address, contract, decimals)
                if bal > 0:
                    print(f"    {symbol}: {bal:.6f}")
                    totals['bsc'][symbol] += bal
        else:
            # TRON
            print("\n  🌐 TRON:")
            for symbol, contract, decimals in TRC20_TOKENS:
                bal = get_trc20_balance(tron_client, address, contract, decimals)
                if bal > 0:
                    print(f"    {symbol}: {bal:.6f}")
                    totals['tron'][symbol] += bal

        print(f"\n  ⏱️ Scan completed in {time.time() - start_time:.2f}s")
        time.sleep(1)  # Rate limiting

    # Display totals
    print("\n" + "="*50)
    print("TOTAL BALANCES ACROSS ALL ADDRESSES")
    print("="*50)
    
    # AVAX Totals
    print("\n🌋 Avalanche Totals:")
    for token, amount in totals['avax'].items():
        if amount > 0:
            print(f"  {token}: {amount:.6f}")
    
    # Ethereum Totals
    print("\n🔷 Ethereum Totals:")
    for token, amount in totals['eth'].items():
        if amount > 0:
            print(f"  {token}: {amount:.6f}")
    
    # BSC Totals
    print("\n🍌 Binance Smart Chain Totals:")
    for token, amount in totals['bsc'].items():
        if amount > 0:
            print(f"  {token}: {amount:.6f}")
    
    # TRON Totals
    print("\n🌐 TRON Totals:")
    for token, amount in totals['tron'].items():
        if amount > 0:
            print(f"  {token}: {amount:.6f}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Script stopped by user")
    except Exception as e:
        print(f"\n❌ Critical error: {str(e)}")
    finally:
        input("\nPress Enter to exit...")