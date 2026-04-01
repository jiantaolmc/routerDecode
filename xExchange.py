import json
import os
from fun.init import w3
from fun.commonFun import check_method_id_start_with_arr, before_method_id_start_with, get_init_item
from abiJson.dir import current_dir

from fun.constants import ETH, WETH, INCH_WETH

xExchangeRouter = "0xDef1C0ded9bec7F1a1670819833240f027b25EfF"
file = os.path.join(current_dir, '0xExchangeAbi.json')
with open(file, 'r') as f:
    xExchangeRouterAbiJson = json.load(f)
xExchangeAbi = w3.eth.contract(address=xExchangeRouter, abi=xExchangeRouterAbiJson)

xExchange_sellToUniswap_id = "0xd9627aa4"
xExchange_multiplexMultiHopSellTokenForToken_id = "0x0f3b31b2"
xExchange_0x44A6999Ec971cfCA458AFf25A808F272f6d492A2_id = "0x415565b0"


xExchange_id_list = [
    xExchange_sellToUniswap_id,
    xExchange_multiplexMultiHopSellTokenForToken_id,
]


def xExchange_decode_input(input_data):
    swap_info_arr = []
    item = get_init_item()
    if check_method_id_start_with_arr(input_data, xExchange_id_list):
        decode_input = xExchangeAbi.decode_function_input(input_data)
        item["part_name"] = "xExchange"
        item["amount_in"] = decode_input[1]["sellAmount"]
        item["amount_out_min"] = decode_input[1]["minBuyAmount"]
        srcToken = WETH if decode_input[1]["tokens"][0] in [ETH, INCH_WETH] else decode_input[1]["tokens"][0]
        dstToken = WETH if decode_input[1]["tokens"][1] in [ETH, INCH_WETH] else decode_input[1]["tokens"][1]
        item["path"] = [srcToken, dstToken]
        swap_info_arr.append(item)
    elif check_method_id_start_with_arr(input_data, [xExchange_0x44A6999Ec971cfCA458AFf25A808F272f6d492A2_id]):
        decode_input = xExchangeAbi.decode_function_input(input_data)
        item["part_name"] = "xExchange"
        item["amount_in"] = decode_input[1]["inputTokenAmount"]
        item["amount_out_min"] = decode_input[1]["minOutputTokenAmount"]
        srcToken = WETH if decode_input[1]["inputToken"] in [ETH, INCH_WETH] else decode_input[1]["inputToken"]
        dstToken = WETH if decode_input[1]["outputToken"] in [ETH, INCH_WETH] else decode_input[1]["outputToken"]
        item["path"] = [srcToken, dstToken]
        swap_info_arr.append(item)
    return swap_info_arr


