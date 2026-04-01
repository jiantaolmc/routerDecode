import json
import os
from fun.init import w3
from fun.inchFun import get_inch_path_by_pool, get_inch_path_by_pools_from_int
from fun.commonFun import check_method_id_start_with_arr, before_method_id_start_with, get_init_item
from abiJson.dir import current_dir

from fun.constants import WETH, INCH_WETH

from fun.constants import ETH

inchV5Router = "0x1111111254EEB25477B68fb85Ed929f73A960582"
file = os.path.join(current_dir, 'inchV5RouterAbi.json')
with open(file, 'r') as f:
    inchV5RouterAbiJson = json.load(f)
inchV5RouterAbi = w3.eth.contract(address=inchV5Router, abi=inchV5RouterAbiJson)

inchV5Router_swap_id = "0x12aa3caf"
inchV5Router_uniswapV3Swap_id = "0xe449022e"
inchV5Router_uniswapV3SwapTo_id = "0xbc80f1a8"
inchV5Router_uniswapV3SwapToWithPermit_id = "0x2521b930"
inchV5Router_unoswap_id = "0x0502b1c5"
inchV5Router_unoswapTo_id = "0xf78dc253"
inchV5Router_unoswapToWithPermit_id = "0x3c15fd91"

inchV5Router_swap_id_list = [
    inchV5Router_swap_id,
    inchV5Router_uniswapV3Swap_id,
    inchV5Router_uniswapV3SwapTo_id,
    inchV5Router_uniswapV3SwapToWithPermit_id,
    inchV5Router_unoswap_id,
    inchV5Router_unoswapTo_id,
    inchV5Router_unoswapToWithPermit_id,
]
inchV5Router_unoswap_id_list = [
    inchV5Router_unoswap_id,
    inchV5Router_unoswapTo_id,
    inchV5Router_unoswapToWithPermit_id,
]
inchV5Router_uniswapV3_id_list = [
    inchV5Router_uniswapV3Swap_id,
    inchV5Router_uniswapV3SwapTo_id,
    inchV5Router_uniswapV3SwapToWithPermit_id,
]


def inch_v5_router_decode_input(input_data):
    swap_info_arr = []
    if check_method_id_start_with_arr(input_data, inchV5Router_swap_id_list):
        swap_info = inch_v5_decode_part_input(input_data)
        swap_info_arr.append(swap_info)
    return swap_info_arr


def inch_v5_decode_part_input(part_input):
    item = get_init_item()
    ####################################inchV5Router##########################
    if check_method_id_start_with_arr(part_input, inchV5Router_swap_id_list):
        decode_input = inchV5RouterAbi.decode_function_input(part_input)
        part_input = before_method_id_start_with(part_input)
        if part_input.startswith(inchV5Router_swap_id):  # {'executor', {'desc': {'srcToken', 'dstToken', 'srcReceiver', 'dstReceiver', 'amount', 'minReturnAmount', 'flag'}}, 'permit', 'data'}
            item["part_name"] = "inchV5Router_swap"
            item["router_version"] = "v2"
            item["amount_in"] = decode_input[1]["desc"]["amount"]
            item["amount_out_min"] = decode_input[1]["desc"]["minReturnAmount"]
            src =decode_input[1]["desc"]["srcToken"]
            dst = decode_input[1]["desc"]["dstToken"]
            item["path"] = [src, dst]
        elif check_method_id_start_with_arr(part_input, inchV5Router_unoswap_id_list):
            if part_input.startswith(inchV5Router_unoswap_id):  # {'srcToken', 'amount', 'minRetrun', 'pools[]'}
                item["part_name"] = "inchV5Router_unoswap"
            elif part_input.startswith(inchV5Router_unoswapTo_id):  # {'recipient', 'srcToken', 'amount', 'minRetrun', 'pools[]'}
                item["part_name"] = "inchV5Router_unoswapTo"
            elif part_input.startswith(inchV5Router_unoswapToWithPermit_id):  # {'recipient', 'srcToken', 'amount', 'minRetrun', 'pools[]', 'permit'}
                item["part_name"] = "inchV5Router_unoswapToWithPermit"
            item["router_version"] = "v2"
            item["amount_in"] = decode_input[1]["amount"]
            item["amount_out_min"] = decode_input[1]["minReturn"]
            src = decode_input[1]["srcToken"].lower()
            pools = decode_input[1]["pools"]
            path_last = get_inch_path_by_pool(hex(pools[len(pools) - 1]))
            item["path"] = [src, path_last[1]]
        elif check_method_id_start_with_arr(part_input, inchV5Router_uniswapV3_id_list):
            if part_input.startswith(inchV5Router_uniswapV3Swap_id):  # {'amount', 'minRetrun', 'pools[]'}
                item["part_name"] = "inchV5Router_uniswapV3Swap"
            elif part_input.startswith(inchV5Router_uniswapV3SwapTo_id):  # {'srcToken', 'amount', 'minRetrun', 'pools[]'}
                item["part_name"] = "inchV5Router_uniswapV3SwapTo"
            elif part_input.startswith(inchV5Router_uniswapV3SwapToWithPermit_id):  # {'srcToken', 'amount', 'minRetrun', 'pools[]', 'permit'}
                item["part_name"] = "inchV5Router_uniswapV3SwapToWithPermit"
            item["router_version"] = "v3"
            item["amount_in"] = decode_input[1]["amount"]
            item["amount_out_min"] = decode_input[1]["minReturn"]
            path_temp = get_inch_path_by_pools_from_int(decode_input[1]["pools"])
            item["path"] = path_temp
    ####################################inchV5Router##########################
    item["path"][0] = WETH if item["path"][0].lower() in [INCH_WETH.lower(), ETH] else item["path"][0]
    item["path"][1] = WETH if item["path"][1].lower() in [INCH_WETH.lower(), ETH] else item["path"][1]
    return item
