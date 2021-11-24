from web3 import Web3
import time
import config


web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))

async def buy_token(coin,contract, nonce):
    pancakeswap2_txn = contract.functions.swapExactETHForTokens(
        10000, [config.weth, coin],
        config.wallet_address,
        (int(time.time()) + 1000000)
    ).buildTransaction({
        'from': config.wallet_address,
        'value': web3.toWei('0.01', 'ether'),
        'gas': 250000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config.private_key)
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(web3.toHex(tx_token))

async def approve(token, spender_address, nonce):

    tx = token.functions.approve(spender_address, 10000000000).buildTransaction({
        'from': config.wallet_address,
        'nonce': nonce
    })

    signed_tx = web3.eth.account.signTransaction(tx, config.private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    print(web3.toHex(tx_hash))



async def swap_tokens_for_tokens(contract,coin_1, coin_2, nonce):
    tokens_for_tokens = contract.functions.swapExactTokensForTokens(
        100000000000, 0, [coin_1, coin_2],
        config.wallet_address,
        (int(time.time()) + 100000)
    ).buildTransaction({
        'from': config.wallet_address,
        'value': web3.toWei('0.01', 'ether'),  # This is the Token(BNB) amount you want to Swap from
        'gas': 25000000,
        'gasPrice': web3.toWei('40', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = web3.eth.account.sign_transaction(tokens_for_tokens, private_key=config.private_key)
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print(web3.toHex(tx_token))
