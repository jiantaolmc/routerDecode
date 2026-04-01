import os
import json

from fun.init import w3
from abiJson.dir import current_dir
from fun.constants import UniswapV2Router02
from fun.commonFun import get_init_item, check_method_id_start_with_arr, before_method_id_start_with


file = os.path.join(current_dir, 'UniswapV2Router02Abi.json')
with open(file, 'r') as f:
    uniswapV2Router02AbiJson = json.load(f)
uniswapV2Router02Abi = w3.eth.contract(address=UniswapV2Router02, abi=uniswapV2Router02AbiJson)

UniswapV2Router02_swapETHForExactTokens_id = "0xfb3bdb41"
UniswapV2Router02_swapExactETHForTokens_id = "0x7ff36ab5"
UniswapV2Router02_swapExactETHForTokensSupportingFeeOnTransferTokens_id = "0xb6f9de95"
UniswapV2Router02_swapExactTokensForETH_id = "0x18cbafe5"
UniswapV2Router02_swapExactTokensForETHSupportingFeeOnTransferTokens_id = "0x791ac947"
UniswapV2Router02_swapExactTokensForTokens_id = "0x38ed1739"
UniswapV2Router02_swapExactTokensForTokensSupportingFeeOnTransferTokens_id = "0x5c11d795"
UniswapV2Router02_swapTokensForExactETH_id = "0x4a25d94a"
UniswapV2Router02_swapTokensForExactTokens_id = "0x8803dbee"

UniswapV2Router02_swap_id_list = [
    UniswapV2Router02_swapETHForExactTokens_id,
    UniswapV2Router02_swapExactETHForTokens_id,
    UniswapV2Router02_swapExactETHForTokensSupportingFeeOnTransferTokens_id,
    UniswapV2Router02_swapExactTokensForETH_id,
    UniswapV2Router02_swapExactTokensForETHSupportingFeeOnTransferTokens_id,
    UniswapV2Router02_swapExactTokensForTokens_id,
    UniswapV2Router02_swapExactTokensForTokensSupportingFeeOnTransferTokens_id,
    UniswapV2Router02_swapTokensForExactETH_id,
    UniswapV2Router02_swapTokensForExactTokens_id,
]

def uniswap_v2_router02_raw_decode(input_data):
    decode_input = uniswapV2Router02Abi.decode_function_input(input_data)
    # print(decode_input)
    return decode_input


def uniswap_v2_router02_decode_input(input_data, value):
    swap_info_arr = []
    if check_method_id_start_with_arr(input_data, UniswapV2Router02_swap_id_list):
        swap_info = uniswap_v2_router02_decode_part_input(input_data, value)
        swap_info_arr.append(swap_info)
    return swap_info_arr


def uniswap_v2_router02_decode_part_input(part_input, value):
    item = get_init_item()
    item["router_version"] = "v2"
    decode_input = uniswapV2Router02Abi.decode_function_input(part_input)
    part_input = before_method_id_start_with(part_input)
    if part_input.startswith(
            UniswapV2Router02_swapETHForExactTokens_id):
        item["part_name"] = "UniswapV2Router02_swapETHForExactTokens"
        item["amount_in"] = value
        item["amount_out_min"] = decode_input[1]["amountOut"]
        item["path"] = decode_input[1]["path"]
    elif part_input.startswith(
            UniswapV2Router02_swapExactETHForTokens_id):
        item["part_name"] = "UniswapV2Router02_swapExactETHForTokens"
        item["amount_in"] = value
        item["amount_out_min"] = decode_input[1]["amountOutMin"]
        item["path"] = decode_input[1]["path"]
    elif part_input.startswith(
            UniswapV2Router02_swapExactETHForTokensSupportingFeeOnTransferTokens_id):
        item["part_name"] = "UniswapV2Router02_swapExactETHForTokensSupportingFeeOnTransferTokens"
        item["amount_in"] = value
        item["amount_out_min"] = decode_input[1]["amountOutMin"]
        item["path"] = decode_input[1]["path"]
    elif part_input.startswith(
            UniswapV2Router02_swapExactTokensForETH_id):
        item["part_name"] = "UniswapV2Router02_swapExactTokensForETH"
        item["amount_in"] = decode_input[1]["amountIn"]
        item["amount_out_min"] = decode_input[1]["amountOutMin"]
        item["path"] = decode_input[1]["path"]
    elif part_input.startswith(
            UniswapV2Router02_swapExactTokensForETHSupportingFeeOnTransferTokens_id):
        item["part_name"] = "UniswapV2Router02_swapExactTokensForETHSupportingFeeOnTransferTokens"
        item["amount_in"] = decode_input[1]["amountIn"]
        item["amount_out_min"] = decode_input[1]["amountOutMin"]
        item["path"] = decode_input[1]["path"]
    elif part_input.startswith(
            UniswapV2Router02_swapExactTokensForTokens_id):
        item["part_name"] = "UniswapV2Router02_swapExactTokensForTokens"
        item["amount_in"] = decode_input[1]["amountIn"]
        item["amount_out_min"] = decode_input[1]["amountOutMin"]
        item["path"] = decode_input[1]["path"]
    elif part_input.startswith(
            UniswapV2Router02_swapExactTokensForTokensSupportingFeeOnTransferTokens_id):
        item["part_name"] = "UniswapV2Router02_swapExactTokensForTokensSupportingFeeOnTransferTokens"
        item["amount_in"] = decode_input[1]["amountIn"]
        item["amount_out_min"] = decode_input[1]["amountOutMin"]
        item["path"] = decode_input[1]["path"]
    elif part_input.startswith(
            UniswapV2Router02_swapTokensForExactETH_id):
        item["part_name"] = "UniswapV2Router02_swapTokensForExactETH"
        item["amount_in"] = decode_input[1]["amountInMax"]
        item["amount_out_min"] = decode_input[1]["amountOut"]
        item["path"] = decode_input[1]["path"]
    elif part_input.startswith(
            UniswapV2Router02_swapTokensForExactTokens_id):
        item["part_name"] = "UniswapV2Router02_swapTokensForExactTokens"
        item["amount_in"] = decode_input[1]["amountInMax"]
        item["amount_out_min"] = decode_input[1]["amountOut"]
        item["path"] = decode_input[1]["path"]
    return item
