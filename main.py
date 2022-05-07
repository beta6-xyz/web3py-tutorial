from web3 import Web3
from abi import ERC20
import asyncio
import os

infura_url = os.environ["INFURA_URL"]

w3 = Web3(
    Web3.WebsocketProvider(
        infura_url
    )
)


def print_eth_balance(address: str) -> None:
    address = w3.toChecksumAddress(address)
    balance = w3.eth.get_balance(address)
    print(Web3.fromWei(balance, "ether"))


def print_erc20_info(contract_addr: str, address: str) -> None:
    address = w3.toChecksumAddress(address)
    contract_addr = w3.toChecksumAddress(contract_addr)    
    contract = w3.eth.contract(contract_addr, abi=ERC20)

    name = contract.functions.name().call()
    symbol = contract.functions.symbol().call()
    raw_balance = contract.functions.balanceOf(address).call()
    DECIMALS = 10 ** contract.functions.decimals().call()
    balance = raw_balance / DECIMALS

    print(f"Name: {name}, Symbol: {symbol}, Balance of {address}: {balance}")


async def log_loop():
    APE_contract_addr = "0x4d224452801ACEd8B2F0aebE155379bb5D594381"
    contract = w3.eth.contract(APE_contract_addr, abi=ERC20)    
    event_filter = contract.events.Transfer.createFilter(fromBlock="latest")    
    DECIMALS = 10 ** contract.functions.decimals().call()    

    while True:
        for event in event_filter.get_new_entries():
            from_address = event.args["from"]
            to_address = event.args["to"]
            value = event.args["value"]
            value /= DECIMALS

            print(f"{from_address} transfer {value} APE token to {to_address}")

        await asyncio.sleep(1)


def main():
    print_eth_balance("0xbe0eb53f46cd790cd13851d5eff43d12404d33e8")
    print_erc20_info("0x4d224452801ACEd8B2F0aebE155379bb5D594381", "0x6cC5F688a315f3dC28A7781717a9A798a59fDA7b")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(log_loop())
    finally:
        loop.close()


if __name__ == "__main__":
    main()
