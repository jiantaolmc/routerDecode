import json
import os.path
from fun.commonFun import get_init_item
from fun.constants import WETH
from fun.init import w3

from abiJson.dir import current_dir

cowSwapEthFlowRouter = "0x40A50cf069e992AA4536211B23F286eF88752187"
cowSwapEthFlowRouter_createOrder_id = "0x322bba21"
file = os.path.join(current_dir, "CowSwapEthFlowAbi.json")
with open(file, 'r') as f:
    cowSwapEthFlowAbiJson = json.load(f)
cowSwapEthFlowAbi = w3.eth.contract(address=cowSwapEthFlowRouter, abi=cowSwapEthFlowAbiJson)


def cow_swap_eth_flow_router_decode_input(input_data):  # 这个是单纯挂单用eth买进其它token的
    swap_info_arr = []
    item = get_init_item()
    if input_data.startswith(cowSwapEthFlowRouter_createOrder_id):
        decode_input = cowSwapEthFlowAbi.decode_function_input(input_data)
        item["part_name"] = "cowSwapEthFlowRouter_createOrder"
        item["amount_in"] = decode_input[1]["order"]["sellAmount"]+decode_input[1]["order"]["feeAmount"]
        item["amount_out_min"] = decode_input[1]["order"]["buyAmount"]
        item["path"] = [WETH, decode_input[1]["order"]["buyToken"]]
        swap_info_arr.append(item)
    return swap_info_arr