import json
import os.path
from fun.commonFun import get_init_item
from fun.constants import WETH, ETH
from fun.init import w3

from abiJson.dir import current_dir


transitSwapRouterV4 = "0xb45A2DDA996C32E93B8c47098E90Ed0E7ab18E39"
transitSwapRouterV4_swap_id = "0xc10bea5c"
file = os.path.join(current_dir, "TransitSwapRouterV4Abi.json")
with open(file, 'r') as f:
    transitSwapRouterV4AbiJson = json.load(f)
transitSwapRouterV4Abi = w3.eth.contract(address=transitSwapRouterV4, abi=transitSwapRouterV4AbiJson)


def transit_swap_router_v4_decode_input(input_data):
    swap_info_arr = []
    item = get_init_item()
    if input_data.startswith(transitSwapRouterV4_swap_id):
        decode_input = transitSwapRouterV4Abi.decode_function_input(input_data)
        item["part_name"] = "transitSwapRouterV4_swap"
        item["amount_in"] = decode_input[1]["desc"]["amount"]
        item["amount_out_min"] = decode_input[1]["desc"]["minReturnAmount"]
        srcToken = decode_input[1]["desc"]["srcToken"] if decode_input[1]["desc"]["srcToken"] != ETH else WETH
        dstToken = decode_input[1]["desc"]["dstToken"] if decode_input[1]["desc"]["dstToken"] != ETH else WETH
        item["path"] = [srcToken, dstToken]
        swap_info_arr.append(item)
    return swap_info_arr
