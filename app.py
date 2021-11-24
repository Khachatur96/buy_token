from web3 import Web3
from csv import reader
import config
from utils import swap_tokens_for_tokens, approve, buy_token
import pandas as pd
import asyncio



def read_csv(file_name):
    with open(file_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        # result = pd.DataFrame(csv_reader)[1:]
        result = pd.DataFrame(csv_reader, columns=['id', 'coin_pair', 'swap_pair', 'date_added', 'price_defference', 'dex_1', 'dex_2'])
        return result[1:]


async def swap_token():
    if config.eth_bal < 1:
        print("You have not enough funds ")

    else:
        prices_result = read_csv('result_Binance.csv')
        for index, row in prices_result.iterrows():
            if float(row['price_defference']) > 0:
                token_allowance = config.COIN_CONTRACTS[row['coin_pair'].split('-')[0]].functions.allowance(config.wallet_address, config.SWAPS_ADDRESSES[row['swap_pair'].split('-')[0]]).call() / 10**18
                token_balance = config.COIN_CONTRACTS[row['coin_pair'].split('-')[0]].functions.balanceOf(config.wallet_address).call() / 10**18
                print(config.COIN_CONTRACTS[row['coin_pair'].split('-')[0]].functions.decimals().call())

                if token_balance < 1 :
                    func_1 = asyncio.create_task(buy_token(config.COINS[row['coin_pair'].split('-')[0]],
                                                           config.CONTRACTS[row['swap_pair'].split('-')[0]],
                                                           config.nonce))
                    await  func_1
                    if token_allowance < 1:
                        func_2 = asyncio.create_task(approve(config.COIN_CONTRACTS[row['coin_pair'].split('-')[0]],
                                                             config.SWAPS_ADDRESSES[row['swap_pair'].split('-')[0]],
                                                             config.nonce + 1))
                        await func_2
                        func_3 = asyncio.create_task(swap_tokens_for_tokens(config.CONTRACTS[row['swap_pair'].split('-')[0]],
                                                                            config.COINS[row['coin_pair'].split('-')[0]],
                                                                            config.COINS[row['coin_pair'].split('-')[1]],config.nonce + 1))
                        await func_3
                    else:
                        func_3 = asyncio.create_task(
                            swap_tokens_for_tokens(config.CONTRACTS[row['swap_pair'].split('-')[0]],
                                                   config.COINS[row['coin_pair'].split('-')[0]],
                                                   config.COINS[row['coin_pair'].split('-')[1]], config.nonce))
                        await func_3
                else:
                    print('////////////')

                    if token_allowance < 1:
                        func_2 = asyncio.create_task(approve(config.COIN_CONTRACTS[row['coin_pair'].split('-')[0]],
                                                             config.SWAPS_ADDRESSES[row['swap_pair'].split('-')[0]],
                                                             config.nonce))
                        await func_2
                        func_3 = asyncio.create_task(
                            swap_tokens_for_tokens(config.CONTRACTS[row['swap_pair'].split('-')[0]],
                                                   config.COINS[row['coin_pair'].split('-')[0]],
                                                   config.COINS[row['coin_pair'].split('-')[1]], config.nonce + 1))
                        await func_3
                    else:
                        print('else')
                        func_3 = asyncio.create_task(
                            swap_tokens_for_tokens(config.CONTRACTS[row['swap_pair'].split('-')[0]],
                                                   config.COINS[row['coin_pair'].split('-')[0]],
                                                   config.COINS[row['coin_pair'].split('-')[1]], config.nonce ))
                        await func_3


asyncio.run(swap_token())




