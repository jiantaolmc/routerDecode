import json
import os
from fun.init import w3
from fun.commonFun import check_method_id_start_with_arr, before_method_id_start_with, get_init_item
from abiJson.dir import current_dir

from fun.constants import WETH, INCH_WETH

from fun.constants import ETH

kyberSwapRouterV2 = "0x6131B5fae19EA4f9D964eAc0408E4408b66337b5"
file = os.path.join(current_dir, 'kyberSwapRouterV2Abi.json')
with open(file, 'r') as f:
    kyberSwapRouterV2AbiJson = json.load(f)
kyberSwapRouterV2Abi = w3.eth.contract(address=kyberSwapRouterV2, abi=kyberSwapRouterV2AbiJson)

kyberSwapRouterV2_swap_id = "0xe21fd0e9"
kyberSwapRouterV2_swapGeneric_id = "0x59e50fed"
kyberSwapRouterV2_swapSimpleMode_id = "0x8af033fb"

kyberSwapRouterV2_swap_id_list = [
    kyberSwapRouterV2_swap_id,
    kyberSwapRouterV2_swapGeneric_id,
    kyberSwapRouterV2_swapSimpleMode_id,
]




def kyberSwapRouterV2_decode_input(input_data):
    swap_info_arr = []
    if check_method_id_start_with_arr(input_data, kyberSwapRouterV2_swap_id_list):
        swap_info = kyberSwapRouterV2_part_input(input_data)
        swap_info_arr.append(swap_info)
    return swap_info_arr


def kyberSwapRouterV2_part_input(part_input):
    item = get_init_item()
    if check_method_id_start_with_arr(part_input, kyberSwapRouterV2_swap_id_list):
        decode_input = kyberSwapRouterV2Abi.decode_function_input(part_input)
        part_input = before_method_id_start_with(part_input)
        if part_input.startswith(kyberSwapRouterV2_swap_id) or part_input.startswith(kyberSwapRouterV2_swapGeneric_id):
            item["part_name"] = "kyberSwapRouterV2_swap"
            item["router_version"] = "v2"
            item["amount_in"] = decode_input[1]["execution"]["desc"]["amount"]
            item["amount_out_min"] = decode_input[1]["execution"]["desc"]["minReturnAmount"]
            src = WETH if decode_input[1]["execution"]["desc"]["srcToken"].lower() in [INCH_WETH.lower(), ETH] else decode_input[1]["execution"]["desc"]["srcToken"].lower()
            dst = WETH if decode_input[1]["execution"]["desc"]["dstToken"].lower() in [INCH_WETH.lower(), ETH] else decode_input[1]["execution"]["desc"]["dstToken"].lower()
            item["path"] = [src, dst]
        elif part_input.startswith(kyberSwapRouterV2_swapSimpleMode_id):
            item["part_name"] = "kyberSwapRouterV2_swapSimpleMode"
            item["router_version"] = "v2"
            item["amount_in"] = decode_input[1]["desc"]["amount"]
            item["amount_out_min"] = decode_input[1]["desc"]["minReturnAmount"]
            src = WETH if decode_input[1]["desc"]["srcToken"].lower() in [INCH_WETH.lower(), ETH] else decode_input[1]["desc"]["srcToken"].lower()
            dst = WETH if decode_input[1]["desc"]["dstToken"].lower() in [INCH_WETH.lower(), ETH] else decode_input[1]["desc"]["dstToken"].lower()
            item["path"] = [src, dst]

    return item
