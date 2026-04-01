import json
import os
from fun.init import w3
from fun.commonFun import check_method_id_start_with_arr, before_method_id_start_with, get_init_item
from abiJson.dir import current_dir

from fun.constants import ETH, WETH, INCH_WETH

paraSwapRouter = "0x6A000F20005980200259B80c5102003040001068"
file = os.path.join(current_dir, 'paraSwapRouterAbi.json')
with open(file, 'r') as f:
    paraSwapRouterAbiJson = json.load(f)
paraSwapRouterAbi = w3.eth.contract(address=paraSwapRouter, abi=paraSwapRouterAbiJson)

paraSwapRouter_swapExactAmountIn_id = "0xe3ead59e"
paraSwapRouter_swapExactAmountInOnUniswapV2_id = "0xe8bb3b6c"
paraSwapRouter_swapExactAmountInOnUniswapV3_id = "0x876a02f6"
paraSwapRouter_swapExactAmountOut_id = "0x7f457675"
paraSwapRouter_swapExactAmountOutOnUniswapV2_id = "0xa76f4eb6"
paraSwapRouter_swapExactAmountOutOnUniswapV3_id = "0x5e94e28d"
paraSwapRouter_swapOnAugustusRFQTryBatchFill_id = "0xda35bb0d"
paraSwapRouter_uniswapV3SwapCallback_id = "0xfa461e33"


paraSwapRouter_swap_id_list = [
    paraSwapRouter_swapExactAmountIn_id,
    paraSwapRouter_swapExactAmountInOnUniswapV2_id,
    paraSwapRouter_swapExactAmountInOnUniswapV3_id,
    paraSwapRouter_swapExactAmountOut_id,
    paraSwapRouter_swapExactAmountOutOnUniswapV2_id,
    paraSwapRouter_swapExactAmountOutOnUniswapV3_id,
    paraSwapRouter_swapOnAugustusRFQTryBatchFill_id,
    paraSwapRouter_uniswapV3SwapCallback_id,
]


def paraSwapRouter_decode_input(input_data):
    swap_info_arr = []
    item = get_init_item()
    if check_method_id_start_with_arr(input_data, paraSwapRouter_swap_id_list):
        decode_input = paraSwapRouterAbi.decode_function_input(input_data)
        item["part_name"] = "paraSwapRouter_swap"
        item["amount_in"] = decode_input[1]["swapData"]["fromAmount"]
        item["amount_out_min"] = decode_input[1]["swapData"]["toAmount"]
        srcToken = WETH if decode_input[1]["swapData"]["srcToken"] in [ETH, INCH_WETH] else decode_input[1]["swapData"]["srcToken"]
        dstToken = WETH if decode_input[1]["swapData"]["destToken"] in [ETH, INCH_WETH] else decode_input[1]["swapData"]["destToken"]
        item["path"] = [srcToken, dstToken]
        swap_info_arr.append(item)
    return swap_info_arr


