import json
import os
from fun.init import w3
from abiJson.dir import current_dir
from fun.commonFun import check_method_id_start_with_arr, before_method_id_start_with, get_init_item, \
    merge_swap_info_arr

################################uniswapV3Router############################################

uniswapV3Router = "0xE592427A0AEce92De3Edee1F18E0157C05861564"
uniswapV3Router_multicall_id = "0xac9650d8"
uniswapV3Router_exactInput_id = "0xc04b8d59"
uniswapV3Router_exactInputSingle_id = "0x414bf389"
uniswapV3Router_exactOutput_id = "0xf28c0498"
uniswapV3Router_exactOutputSingle_id = "0xdb3e2198"
uniswapV3Router_sweepToken_id = "0xdf2ab5bb"
uniswapV3Router_sweepTokenWithFee_id = "0xe0e189a0"

uniswapV3Router_swap_id_list = [
    uniswapV3Router_exactInput_id,
    uniswapV3Router_exactInputSingle_id,
    uniswapV3Router_exactOutput_id,
    uniswapV3Router_exactOutputSingle_id,
]
file = os.path.join(current_dir, "UniswapV3RouterAbi.json")
with open(file, 'r') as f:
    uniswapV3RouterAbiJson = json.load(f)
uniswapV3RouterAbi = w3.eth.contract(address=uniswapV3Router, abi=uniswapV3RouterAbiJson)
############################################################################

################################uniswapV3Router2############################################
uniswapV3Router2 = "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45"
file = os.path.join(current_dir, "UniswapV3Router2Abi.json")
with open(file, 'r') as f:
    uniswapV3Router2AbiJson = json.load(f)
uniswapV3Router2Abi = w3.eth.contract(address=uniswapV3Router2, abi=uniswapV3Router2AbiJson)

uniswapV3Router2_multicall_id_1 = "0x5ae401dc"
uniswapV3Router2_multicall_id_2 = "0xac9650d8"
uniswapV3Router2_multicall_id_3 = "0x1f0464d1"
uniswapV3Router2_exactInput_id = "0xb858183f"
uniswapV3Router2_exactInputSingle_id = "0x04e45aaf"
uniswapV3Router2_exactOutput_id = "0x09b81346"
uniswapV3Router2_exactOutputSingle_id = "0x5023b4df"
uniswapV3Router2_swapExactTokensForTokens_id = "0x472b43f3"
uniswapV3Router2_swapTokensForExactTokens_id = "0x42712a67"

uniswapV3Router2_multicall_id_list = [
    uniswapV3Router2_multicall_id_1,
    uniswapV3Router2_multicall_id_2,
    uniswapV3Router2_multicall_id_3
]
uniswapV3Router2_swap_id_list = [
    uniswapV3Router2_exactInput_id,
    uniswapV3Router2_exactInputSingle_id,
    uniswapV3Router2_exactOutput_id,
    uniswapV3Router2_exactOutputSingle_id,
    uniswapV3Router2_swapExactTokensForTokens_id,
    uniswapV3Router2_swapTokensForExactTokens_id,
]


############################################################################

def uniswap_v3_router_decode_input(input_data):
    swap_info_arr = []
    if check_method_id_start_with_arr(input_data, uniswapV3Router2_multicall_id_list+[uniswapV3Router_multicall_id]):
        if input_data.startswith(uniswapV3Router_multicall_id):  # uniswapV3Router_multicall
            decode_input = uniswapV3RouterAbi.decode_function_input(input_data)
        elif check_method_id_start_with_arr(input_data,
                                            uniswapV3Router2_multicall_id_list):  # uniswapV3Router2_multicall_id
            decode_input = uniswapV3Router2Abi.decode_function_input(input_data)
        args_inputs = decode_input[1]["data"]
        for args_input in args_inputs:
            if check_method_id_start_with_arr(args_input, uniswapV3Router2_swap_id_list + uniswapV3Router_swap_id_list):
                swap_info = uniswap_v3_decode_part_input(args_input)
                swap_info_arr.append(swap_info)
    else:
        if check_method_id_start_with_arr(input_data, uniswapV3Router2_swap_id_list + uniswapV3Router_swap_id_list):
            swap_info = uniswap_v3_decode_part_input(input_data)
            swap_info_arr.append(swap_info)
    if len(swap_info_arr) > 1:
        swap_info_arr = merge_swap_info_arr(swap_info_arr)
    return swap_info_arr





def uniswap_v3_decode_part_input(part_input):
    item = get_init_item()
    ####################################uniswapV3Router##########################
    if check_method_id_start_with_arr(part_input, uniswapV3Router_swap_id_list):  # uniswapV3Router
        decode_input = uniswapV3RouterAbi.decode_function_input(part_input)
        part_input = before_method_id_start_with(part_input)
        if part_input.startswith(
                uniswapV3Router_exactInput_id):  # {'params': (path, recipient, deadline, amountIn, amountOutMinimum)}
            item["part_name"] = "uniswapV3Router_exactInput"
            item["amount_in"] = decode_input[1]["params"]["amountIn"]
            item["amount_out_min"] = decode_input[1]["params"]["amountOutMinimum"]
            path_str = decode_input[1]["params"]["path"].hex()
            token_num = (len(path_str) + 6) // 46
            for i in range(token_num):
                value = path_str[i * 46:i * 46 + 40]
                item["path"].append("0x" + value)
        elif part_input.startswith(
                uniswapV3Router_exactOutput_id):  # {'params': (path, recipient, deadline, amountOut, amountInMaximum)}
            item["part_name"] = "uniswapV3Router_exactOutput"
            item["swap_type"] = 1
            item["amount_in_max"] = decode_input[1]["params"]["amountInMaximum"]
            item["amount_out"] = decode_input[1]["params"]["amountOut"]
            path_str = decode_input[1]["params"]["path"].hex()
            token_num = (len(path_str) + 6) // 46
            for i in range(token_num):
                value = path_str[i * 46:i * 46 + 40]
                item["path"].append("0x" + value)
        elif part_input.startswith(
                uniswapV3Router_exactInputSingle_id):  # {'params': (tokenIn, tokenOut, fee, recipient, deadline, amountIn, amountOutMinimum, sqrtPriceLimitX96)}
            item["part_name"] = "uniswapV3Router_exactInputSingle"
            item["amount_in"] = decode_input[1]["params"]["amountIn"]
            item["amount_out_min"] = decode_input[1]["params"]["amountOutMinimum"]
            item["path"] = [decode_input[1]["params"]["tokenIn"], decode_input[1]["params"]["tokenOut"]]
        elif part_input.startswith(
                uniswapV3Router_exactOutputSingle_id):  # {'params': (tokenIn, tokenOut, fee, recipient,deadline, amountOut, amountInMaximum, sqrtPriceLimitX96)}
            item["part_name"] = "uniswapV3Router_exactOutputSingle"
            item["swap_type"] = 1
            item["amount_in_max"] = decode_input[1]["params"]["amountInMaximum"]
            item["amount_out"] = decode_input[1]["params"]["amountOut"]
            item["path"] = [decode_input[1]["params"]["tokenIn"], decode_input[1]["params"]["tokenOut"]]
    ####################################uniswapV3Router2##########################
    elif check_method_id_start_with_arr(part_input,
                                        uniswapV3Router2_swap_id_list):  # uniswapV3Router2
        decode_input = uniswapV3Router2Abi.decode_function_input(part_input)
        part_input = before_method_id_start_with(part_input)
        if part_input.startswith(uniswapV3Router2_swapExactTokensForTokens_id):  # {amountIn, amountOutMin, path, to}
            item["part_name"] = "uniswapV3Router2_swapExactTokensForTokens"
            item["router_version"] = "v2"
            item["amount_in"] = decode_input[1]["amountIn"]
            item["amount_out_min"] = decode_input[1]["amountOutMin"]
            item["path"] = decode_input[1]["path"]
        elif part_input.startswith(uniswapV3Router2_swapTokensForExactTokens_id):  # {amountOut, amountInMax, path, to}
            item["part_name"] = "uniswapV3Router2_swapTokensForExactTokens"
            item["swap_type"] = 1
            item["router_version"] = "v2"
            item["amount_in_max"] = decode_input[1]["amountInMax"]
            item["amount_out"] = decode_input[1]["amountOut"]
            item["path"] = decode_input[1]["path"]
        elif part_input.startswith(
                uniswapV3Router2_exactInput_id):  # {'params': (path, recipient, amountIn, amountOutMinimum)}
            item["part_name"] = "uniswapV3Router2_exactInput"
            item["amount_in"] = decode_input[1]["params"]["amountIn"]
            item["amount_out_min"] = decode_input[1]["params"]["amountOutMinimum"]
            path_str = decode_input[1]["params"]["path"].hex()
            token_num = (len(path_str) + 6) // 46
            for i in range(token_num):
                value = path_str[i * 46:i * 46 + 40]
                item["path"].append("0x" + value)
        elif part_input.startswith(
                uniswapV3Router2_exactOutput_id):  # {'params': (path, recipient, amountOut, amountInMaximum)}
            item["part_name"] = "uniswapV3Router2_exactOutput"
            item["swap_type"] = 1
            item["amount_in_max"] = decode_input[1]["params"]["amountInMaximum"]
            item["amount_out"] = decode_input[1]["params"]["amountOut"]
            path_str = decode_input[1]["params"]["path"].hex()
            token_num = (len(path_str) + 6) // 46
            for i in range(token_num):
                value = path_str[i * 46:i * 46 + 40]
                item["path"].append("0x" + value)
        elif part_input.startswith(
                uniswapV3Router2_exactInputSingle_id):  # {'params': (tokenIn, tokenOut, fee, recipient, amountIn, amountOutMinimum, sqrtPriceLimitX96)}
            item["part_name"] = "uniswapV3Router2_exactInputSingle"
            item["amount_in"] = decode_input[1]["params"]["amountIn"]
            item["amount_out_min"] = decode_input[1]["params"]["amountOutMinimum"]
            item["path"] = [decode_input[1]["params"]["tokenIn"], decode_input[1]["params"]["tokenOut"]]
        elif part_input.startswith(
                uniswapV3Router2_exactOutputSingle_id):  # {'params': (tokenIn, tokenOut, fee, recipient, amountOut, amountInMaximum, sqrtPriceLimitX96)}
            item["part_name"] = "uniswapV3Router2_exactOutputSingle"
            item["swap_type"] = 1
            item["amount_in_max"] = decode_input[1]["params"]["amountInMaximum"]
            item["amount_out"] = decode_input[1]["params"]["amountOut"]
            item["path"] = [decode_input[1]["params"]["tokenIn"], decode_input[1]["params"]["tokenOut"]]
    return item
