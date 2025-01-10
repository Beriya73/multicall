import json

with open('abis/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open('abis/multicall_abi.json') as file:
    MULTICALL_ABI = json.load(file)

with open('abis/all_chains_data.json') as file:
    ALL_CHAINS_DATA = json.load(file)

MULTICALL_ADDRESSES = {'Ethereum Mainnet':'0xcA11bde05977b3631167028862bE2a173976CA11',
                       'BNB Smart Chain Mainnet':'0xcA11bde05977b3631167028862bE2a173976CA11',
                       'zkSync Mainnet':'0xF9cda624FBC7e059355ce98a31693d299FACd963',
                       'Arbitrum One':'0xcA11bde05977b3631167028862bE2a173976CA11',
                       }

TOKENS_PER_CHAIN = {
    'Arbitrum One': {
        "ETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        "USDC.e":'0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8',
        "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        'ARB':'0x912CE59144191C1204E64559FE8253a0e49E6548',
    },
    'BNB Smart Chain Mainnet': {
        'BNB': '0x3E14602186DD9dE538F729547B3918D24c823546',
        "ETH": "0x2170Ed0880ac9A755fd29B2688956BD959F933F8",
        'BSC-USD':'0x55d398326f99059fF775485246999027B3197955',
        'XRP':'0x1D2F0da169ceB9fC7B3144628dB156f3F6c60dBE',
        'WBNB':'0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
    },
    'Ethereum Mainnet': {
        "ETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        'USDT':'0xdAC17F958D2ee523a2206206994597C13D831ec7',
        'BNB':'0xB8c77482e45F1F44dE1745F52C74426C631bDD52',
        'USDC':'0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
        'stETH':'0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84'
    },
    'zkSync Mainnet': {
        "ETH": "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        "WETH": "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        "USDT": "0x493257fD37EDB34451f62EDf8D2a0C418852bA4C",
        "USDC.e": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
        "USDC": "0x1d17CBcF0D6D143135aE902365D2E5e2A16538D4"
    }
}
