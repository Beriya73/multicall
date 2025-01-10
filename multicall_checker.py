import asyncio
import logging
from web3 import AsyncWeb3, AsyncHTTPProvider
from functions import get_valid_private_keys, get_blockchain_data, get_chain
from config import *

PRIVATE_KEYS_FILE = '.env'
PROXY = ''

# Настройка логирования
file_log = logging.FileHandler('multicall.log', encoding='utf-8')
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out),
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

class MulticallChecker:

    def __init__(self, proxy):
        try:
            # Получение приватных ключей из файла
            self.private_keys = get_valid_private_keys(PRIVATE_KEYS_FILE)
            # Настройка параметров запроса
            self.request_kwargs = {'proxy': f'http://{proxy}'}
            # Получение данных о блокчейне
            self.chain_name = get_chain()
            self.chain_data = get_blockchain_data(self.chain_name)
            self.rpc = self.chain_data.get('rpc')[0]

            # Инициализация клиента Web3
            self.w3 = AsyncWeb3(AsyncHTTPProvider(self.rpc, request_kwargs=self.request_kwargs))
        except Exception as er:
            logging.error(f"Ошибка при инициализации клиента! {er}")
            exit(1)

    async def check_balance(self):
        try:
            # Получение контрактов для текущей цепи
            chain_contracts = TOKENS_PER_CHAIN.get(self.chain_name)
            # Инициализация контракта Multicall
            multicall_contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(MULTICALL_ADDRESSES[self.chain_name]),
                abi=MULTICALL_ABI
            )

            for private_key in self.private_keys:
                token_calls = []
                wallet_address = self.w3.to_checksum_address(
                    self.w3.eth.account.from_key(private_key).address)
                print('\n',"*"*60, sep='')
                print(f'Баланс {wallet_address}:')

                # Подготовка вызовов для токенов
                token_calls.extend(await self.prepare_token_calls(wallet_address, chain_contracts))
                # Выполнение мультиколла
                result_multicall = await multicall_contract.functions.aggregate3(token_calls).call()
                # Декодирование данных мультиколла
                self.decode_data_multicall(result_multicall)
        except Exception as e:
            logging.error(f"Ошибка при проверке баланса: {e}")

    async def prepare_token_calls(self, wallet_address, chain_contracts):
        token_calls = []
        try:
            for token in chain_contracts:
                token_address = self.w3.to_checksum_address(chain_contracts.get(token))
                if token != self.chain_data['nativeCurrency']['symbol']:
                    token_contract = self.w3.eth.contract(
                        address=token_address,
                        abi=ERC20_ABI)
                    token_calls.extend(await self.prepare_erc20_calls(token_contract, wallet_address))
                else:
                    await self.print_native_currency_balance(wallet_address)
        except Exception as e:
            logging.error(f"Ошибка при подготовке вызовов токенов: {e}")
        return token_calls

    async def prepare_erc20_calls(self, token_contract, wallet_address):
        token_calls = []
        try:
            token_name = token_contract.encode_abi('name')
            token_calls.append([token_contract.address, False, token_name])

            token_decimals = token_contract.encode_abi('decimals')
            token_calls.append([token_contract.address, False, token_decimals])

            balance = token_contract.encode_abi('balanceOf', args=([wallet_address]))
            token_calls.append([token_contract.address, False, balance])
        except Exception as e:
            logging.error(f"Ошибка при подготовке вызовов ERC20: {e}")
        return token_calls

    async def print_native_currency_balance(self, wallet_address):
        try:
            balance = await self.w3.eth.get_balance(wallet_address)
            name = self.chain_data.get('nativeCurrency').get('symbol')
            decimals = self.chain_data.get('nativeCurrency').get('decimals')
            print(f'Токен  {name}:{balance / 10 ** decimals:.6f}')
        except Exception as e:
            logging.error(f"Ошибка при получении баланса нативной валюты: {e}")

    def decode_data_multicall(self, result_multicall):
        try:
            for name, decimals, balance in zip(result_multicall[0::3], result_multicall[1::3], result_multicall[2::3]):

                if name[0]:
                    name = self.w3.to_text(primitive=name[1])
                    name = ''.join(filter(str.isprintable, name))
                else:
                    logging.error("Произошла ошибка при получении имени токена!")

                if decimals[0]:
                    decimals = self.w3.to_int(decimals[1])
                else:
                    logging.error("Произошла ошибка при получении decimals!")

                if balance[0]:
                    balance = self.w3.to_int(balance[1])
                    print(f'Токен {name}: {balance / 10 ** decimals}')
                else:
                    logging.error("Произошла ошибка при получении balance!")

            print("*" * 60)
        except Exception as e:
            logging.error(f"Ошибка при декодировании данных мультиколла: {e}")

async def main():
    try:
        mlt_bal = MulticallChecker(PROXY)
        await mlt_bal.check_balance()
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")

if __name__ == "__main__":
    asyncio.run(main())
