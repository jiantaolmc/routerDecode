import json
import os
from fun.init import w3

#############################1inch###############################################
from fun.inchFun import get_inch_path_by_pool, get_inch_path_by_pools_from_int
from fun.commonFun import check_method_id_start_with_arr, before_method_id_start_with, get_init_item
from fun.constants import WETH, INCH_WETH
from abiJson.dir import current_dir

from fun.constants import ETH

inchV4Router = "0x1111111254fb6c44bAC0beD2854e76F90643097d"
file = os.path.join(current_dir, 'inchV4RouterAbi.json')
with open(file, 'r') as f:
    inchV4RouterAbiJson = json.load(f)
inchV4RouterAbi = w3.eth.contract(address=inchV4Router, abi=inchV4RouterAbiJson)

inchV4Router_swap_id = "0x7c025200"
inchV4Router_unoswap_id = "0x2e95b6c8"
inchV4Router_unoswapWithPermit_id = "0xa1251d75"
inchV4Router_uniswapV3Swap_id = "0xe449022e"
inchV4Router_uniswapV3SwapTo_id = "0xbc80f1a8"
inchV4Router_uniswapV3SwapToWithPermit_id = "0x2521b930"

inchV4Router_swap_id_list = [
    inchV4Router_swap_id,
    inchV4Router_unoswap_id,
    inchV4Router_unoswapWithPermit_id,
    inchV4Router_uniswapV3Swap_id,
    inchV4Router_uniswapV3SwapTo_id,
    inchV4Router_uniswapV3SwapToWithPermit_id,
]
inchV4Router_unoswap_id_list = [
    inchV4Router_unoswap_id,
    inchV4Router_unoswapWithPermit_id,
]
inchV4Router_uniswapV3_id_list = [
    inchV4Router_uniswapV3Swap_id,
    inchV4Router_uniswapV3SwapTo_id,
    inchV4Router_uniswapV3SwapToWithPermit_id,
]


def inch_v4_router_decode_input(input_data):
    swap_info_arr = []
    if check_method_id_start_with_arr(input_data, inchV4Router_swap_id_list):
        swap_info = inch_v4_decode_part_input(input_data)
        swap_info_arr.append(swap_info)
    return swap_info_arr


def inch_v4_decode_part_input(part_input):
    item = get_init_item()
    if check_method_id_start_with_arr(part_input, inchV4Router_swap_id_list):
        decode_input = inchV4RouterAbi.decode_function_input(part_input)
        part_input = before_method_id_start_with(part_input)
        if part_input.startswith(
                inchV4Router_swap_id):  # {'executor', {'desc': {'srcToken', 'dstToken', 'srcReceiver', 'dstReceiver', 'amount', 'minReturnAmount', 'flag'}}, 'permit', 'data'}
            item["part_name"] = "inchV4Router_swap"
            item["router_version"] = "v2"
            item["amount_in"] = decode_input[1]["desc"]["amount"]
            item["amount_out_min"] = decode_input[1]["desc"]["minReturnAmount"]
            src = decode_input[1]["desc"]["srcToken"]
            dst = decode_input[1]["desc"]["dstToken"]
            item["path"] = [src, dst]
        elif check_method_id_start_with_arr(part_input, inchV4Router_unoswap_id_list):
            if part_input.startswith(inchV4Router_unoswap_id):  # {'srcToken', 'amount', 'minRetrun', 'pools[]'}
                item["part_name"] = "inchV4Router_unoswap"
            elif part_input.startswith(inchV4Router_unoswapWithPermit_id):  # { 'srcToken', 'amount', 'minRetrun', 'pools[]', 'permit'}
                item["part_name"] = "inchV4Router_unoswapWithPermit"
            item["router_version"] = "v2"
            item["amount_in"] = decode_input[1]["amount"]
            item["amount_out_min"] = decode_input[1]["minReturn"]
            src = decode_input[1]["srcToken"].lower()
            pools = decode_input[1]["pools"]
            # bytes to string
            pool_address = "0x" + pools[len(pools) - 1].hex()
            path_last = get_inch_path_by_pool(pool_address)
            item["path"] = [src, path_last[1]]
        elif check_method_id_start_with_arr(part_input, inchV4Router_uniswapV3_id_list):  # 和v5合集一样
            if part_input.startswith(inchV4Router_uniswapV3Swap_id):  # {'amount', 'minRetrun', 'pools[]'}
                item["part_name"] = "inchV4Router_uniswapV3Swap"
            elif part_input.startswith(
                    inchV4Router_uniswapV3SwapTo_id):  # {'srcToken', 'amount', 'minRetrun', 'pools[]'}
                item["part_name"] = "inchV4Router_uniswapV3SwapTo"
            elif part_input.startswith(
                    inchV4Router_uniswapV3SwapToWithPermit_id):  # {'srcToken', 'amount', 'minRetrun', 'pools[]', 'permit'}
                item["part_name"] = "inch45Router_uniswapV3SwapToWithPermit"
            item["router_version"] = "v3"
            item["amount_in"] = decode_input[1]["amount"]
            item["amount_out_min"] = decode_input[1]["minReturn"]
            path_temp = get_inch_path_by_pools_from_int(decode_input[1]["pools"])
            item["path"] = path_temp
    item["path"][0] = WETH if item["path"][0].lower() in [INCH_WETH.lower(), ETH] else item["path"][0]
    item["path"][1] = WETH if item["path"][1].lower() in [INCH_WETH.lower(), ETH] else item["path"][1]
    return item
