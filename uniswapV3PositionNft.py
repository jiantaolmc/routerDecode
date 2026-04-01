import os
import json

from fun.init import w3
from abiJson.dir import current_dir

from fun.constants import UniSwapV3PositionNft

file = os.path.join(current_dir, 'UniswapV3PositionAbi.json')
with open(file, 'r') as f:
    uniswapV3PositionNftAbiJson = json.load(f)
uniswapV2Router02Abi = w3.eth.contract(address=UniSwapV3PositionNft, abi=uniswapV3PositionNftAbiJson)



def uniswap_v3_position_nft_raw_decode(input_data, id):
    if input_data.startswith("0xac9650d8"): # multicall
        decode_input = uniswapV2Router02Abi.decode_function_input(input_data)
        for item in decode_input[1]["data"]:
            input = "0x"+item.hex()
            if input.startswith(id):
                return uniswapV2Router02Abi.decode_function_input(input)
    elif input_data.startswith(id):
        return uniswapV2Router02Abi.decode_function_input(input_data)

