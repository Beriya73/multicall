

from ecdsa import SigningKey, VerifyingKey, SECP256k1
import logging
from config import ALL_CHAINS_DATA, MULTICALL_ADDRESSES


# Настройка логирования
file_log = logging.FileHandler('functions.log', encoding='utf-8')
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out),
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

# Выбираем сеть
def get_chain():
    [print(items[0],items[1]) for items in enumerate(MULTICALL_ADDRESSES,1)]
    listing=(list(MULTICALL_ADDRESSES))
    while True:
        try:
            selected_network= int(input("Выберите сеть: "))
            if 1 <= selected_network <= len(listing):
                selected_network = selected_network - 1
                chain_name = listing[selected_network]
                logging.info(f"Вы выбрали сеть {chain_name}")
                return chain_name
        except:
            logging.warning("Попробуйте еще раз...")



# Получаем список приватных ключей из файла
def get_valid_private_keys(file_path)-> list:
    def check_private_key(private_key_hex):

        try:
            private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
            public_key = private_key.get_verifying_key()
            message = b"Hello, Blockchain!"
            signature = private_key.sign(message)
            return public_key.verify(signature, message)
        except Exception:
            logging.warning(f"{private_key_hex} - не валидный")
            return False

    try:
        with open(file_path, "r") as file:
            private_keys = file.readlines()
    except Exception as er:
        logging.error((f"Файл {file_path} не найден"))
        exit(1)

    valid_keys = [key.strip() for key in private_keys if check_private_key(key.strip())]
    if not valid_keys:
        logging.error(f"В файле {file_path} нет валидных private key!")
    return valid_keys

# Получаем данные о сети из файла по входному имени
def get_blockchain_data(name: str) -> dict:
    for chain in ALL_CHAINS_DATA:
        if chain["name"] == name:
            filtered_data = {}
            # Фильтрация RPC URLs
            filtered_rpc = [url for url in chain.get("rpc", []) if
                            "${INFURA_API_KEY}" not in url and not url.startswith("wss:") and
                            "${ALCHEMY_API_KEY}" not in url]
            chain["rpc"] = filtered_rpc
            # Фильтрация Explorers URLs
            filtered_explorers = [explorer["url"] for explorer in chain.get("explorers", []) if
                                  not explorer["url"].startswith("wss:")]
            chain["explorers"] = filtered_explorers
            return chain
if __name__ == '__main__':

    # file_private_keys = '.env'
    # valid_keys = get_valid_private_keys(file_private_keys)
    # print(f"Валидные приватные ключи: {valid_keys}")

    #print(get_blockchain_data("Ethereum Mainnet"))
    get_chain()


