import json
import os

from eth_abi import abi

from fun.init import w3
from abiJson.dir import current_dir

################################universalRouter############################################
from fun.commonFun import check_method_id_start_with_arr, merge_swap_info_arr

universalRouter = "0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD"
file = os.path.join(current_dir, 'UniversalRouterAbi.json')
with open(file, 'r') as f:
    universalRouterAbiJson = json.load(f)
universalRouterAbi = w3.eth.contract(address=universalRouter, abi=universalRouterAbiJson)

# https://docs.uniswap.org/contracts/universal-router/technical-reference
universalRouter_execute_id1 = "0x24856bc3"
universalRouter_execute_id2 = "0x3593564c"
universalRouter_v3SwapExactIn_id = "0x00"
universalRouter_v3SwapExactOut_id = "0x01"
universalRouter_v2SwapExactIn_id = "0x08"
universalRouter_v2SwapExactOut_id = "0x09"

universalRouter_swap_id_list = [
    universalRouter_v3SwapExactIn_id,
    universalRouter_v3SwapExactOut_id,
    universalRouter_v2SwapExactIn_id,
    universalRouter_v2SwapExactOut_id,
]

universalRouter_v2SwapExactIn_data_type = ["address", "uint256", "uint256", "address[]", "bool"]
universalRouter_v2SwapExactOut_data_type = ["address", "uint256", "uint256", "address[]", "bool"]
universalRouter_v3SwapExactIn_data_type = ["address", "uint256", "uint256", "bytes", "bool"]
universalRouter_v3SwapExactOut_data_type = ["address", "uint256", "uint256", "bytes", "bool"]
############################################################################

def universal_router_decode_input(input_data):
    swap_info_arr = []
    if input_data.startswith(universalRouter_execute_id1) or input_data.startswith(universalRouter_execute_id2):
        decode_input = universalRouterAbi.decode_function_input(input_data)
        part_commands = decode_input[1]["commands"].hex()
        token_num = (len(part_commands)) // 2
        part_command_arr = []
        for i in range(token_num):
            value = part_commands[i * 2:i * 2 + 2]
            part_command_arr.append("0x" + value)
        part_inputs = decode_input[1]["inputs"]
        if len(part_inputs) == len(part_command_arr):
            for i in range(len(part_inputs)):
                if check_method_id_start_with_arr(part_command_arr[i], universalRouter_swap_id_list):
                    swap_info = decode_universal_router_part_input(part_inputs[i], part_command_arr[i])
                    swap_info_arr.append(swap_info)
    if len(swap_info_arr) > 1:
        swap_info_arr = handle_swap_info_arr(swap_info_arr)
    if len(swap_info_arr) > 1:
        swap_info_arr = merge_swap_info_arr(swap_info_arr)
    return swap_info_arr


# v2 v3路由合并
def handle_swap_info_arr(swap_info_arr):
    merge_num = 57896044618658097711785492504343953926634992332820282019728792003956564819968
    new_arr = []
    for i in range(0, len(swap_info_arr)):
        item = swap_info_arr[i]
        if i > 0:
            if item["path"][0] == new_arr[-1]["path"][len(new_arr[-1]["path"]) - 1] and new_arr:
                new_arr[-1]["amount_in"] += item["amount_in"] if item["amount_in"] != merge_num else 0
                new_arr[-1]["amount_in_max"] += item["amount_in_max"] if item["amount_in_max"] != merge_num else 0
                new_arr[-1]["amount_out"] += item["amount_out"] if item["amount_out"] != merge_num else 0
                new_arr[-1]["amount_out_min"] += item["amount_out_min"] if item["amount_out_min"] != merge_num else 0
                new_arr[-1]["path"].append(item["path"][len(item["path"]) - 1])
            else:
                new_arr.append(item)
        else:
            new_arr.append(item)
    return new_arr


def decode_universal_router_part_input(input_byte, command):
    # swapType 交易类型 0：用精确数量代币买入 1：获得精确数量代币
    item = {"router_version": "v3", "swap_type": 0, "part_name": "", "amount_in": 0, "amount_in_max": 0,
            "amount_out": 0,
            "amount_out_min": 0, "path": []}
    if command == universalRouter_v2SwapExactIn_id:  # address recipient; uint256 amountIn; uint256 amountOutMin; address[]  path; bool input_from_msg_sender
        decode_input = abi.decode(universalRouter_v2SwapExactIn_data_type, input_byte)
        item["part_name"] = "universalRouter_v2SwapExactIn"
        item["router_version"] = "v2"
        item["amount_in"] = decode_input[1]
        item["amount_out_min"] = decode_input[2]
        item["path"] = list(decode_input[3])
    elif command == universalRouter_v2SwapExactOut_id:  # address recipient; uint256 amountOut; uint256 amountInMax; address[]  path; bool input_from_msg_sender
        decode_input = abi.decode(universalRouter_v2SwapExactOut_data_type, input_byte)
        item["part_name"] = "universalRouter_v2SwapExactOut"
        item["router_version"] = "v2"
        item["swap_type"] = 1
        item["amount_in_max"] = decode_input[2]
        item["amount_out"] = decode_input[1]
        item["path"] = list(decode_input[3])
    elif command == universalRouter_v3SwapExactIn_id:  # address recipient; uint256 amountIn; uint256 amountOutMin; bytes[]  path; bool input_from_msg_sender
        decode_input = abi.decode(universalRouter_v3SwapExactIn_data_type, input_byte)
        item["part_name"] = "universalRouter_v3SwapExactIn"
        item["amount_in"] = decode_input[1]
        item["amount_out_min"] = decode_input[2]
        path_str = decode_input[3].hex()
        token_num = (len(path_str) + 6) // 46
        for i in range(token_num):
            value = path_str[i * 46:i * 46 + 40]
            item["path"].append("0x" + value)
    elif command == universalRouter_v3SwapExactOut_id:  # address recipient; uint256 amountOut; uint256 amountInMax; bytes[]  path; bool input_from_msg_sender
        decode_input = abi.decode(universalRouter_v3SwapExactOut_data_type, input_byte)
        item["part_name"] = "universalRouter_v3SwapExactOut"
        item["swap_type"] = 1
        item["amount_in_max"] = decode_input[2]
        item["amount_out"] = decode_input[1]
        path_str = decode_input[3].hex()
        token_num = (len(path_str) + 6) // 46
        for i in range(token_num):
            value = path_str[i * 46:i * 46 + 40]
            item["path"].append("0x" + value)
    return item
