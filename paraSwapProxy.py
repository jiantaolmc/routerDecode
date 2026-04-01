import json
import os
from fun.init import w3
from fun.commonFun import check_method_id_start_with_arr, before_method_id_start_with, get_init_item
from abiJson.dir import current_dir

from fun.constants import ETH, WETH, INCH_WETH

paraSwapProxy = "0xDEF171Fe48CF0115B1d80b88dc8eAB59176FEe57"
file = os.path.join(current_dir, 'paraSwapProxyAbi.json')
with open(file, 'r') as f:
    paraSwapProxyAbiJson = json.load(f)
paraSwapProxyAbi = w3.eth.contract(address=paraSwapProxy, abi=paraSwapProxyAbiJson)

paraSwapProxy_swapOnUniswapV2Fork_id = "0x0b86a4c1"
paraSwapProxy_multiSwap_id = "0xa94e78ef"


paraSwapProxy_id_list = [
    paraSwapProxy_swapOnUniswapV2Fork_id,
    paraSwapProxy_multiSwap_id,
]


def paraSwapProxy_decode_input(input_data):
    swap_info_arr = []
    item = get_init_item()
    if check_method_id_start_with_arr(input_data, [paraSwapProxy_swapOnUniswapV2Fork_id]):
        decode_input = paraSwapProxyAbi.decode_function_input(input_data)
        item["part_name"] = "paraSwapProxy"
        item["amount_in"] = decode_input[1]["amountIn"]
        item["amount_out_min"] = decode_input[1]["amountOutMin"]
        srcToken = WETH if decode_input[1]["tokenIn"] in [ETH, INCH_WETH] else decode_input[1]["tokenIn"]
        dstToken = WETH if decode_input[1]["weth"] in [ETH, INCH_WETH] else decode_input[1]["weth"]
        item["path"] = [srcToken, dstToken]
        swap_info_arr.append(item)
    elif check_method_id_start_with_arr(input_data, [paraSwapProxy_multiSwap_id]):
        decode_input = paraSwapProxyAbi.decode_function_input(input_data)
        item["part_name"] = "paraSwapProxy"
        item["amount_in"] = decode_input[1]["data"]["fromAmount"]
        item["amount_out_min"] = decode_input[1]["data"]["toAmount"]
        srcToken = WETH if decode_input[1]["data"]["fromToken"] in [ETH, INCH_WETH] else decode_input[1]["data"]["fromToken"]
        dstToken = WETH if decode_input[1]["data"]["path"][0]["to"] in [ETH, INCH_WETH] else decode_input[1]["data"]["path"][0]["to"]
        item["path"] = [srcToken, dstToken]
        swap_info_arr.append(item)
    return swap_info_arr


