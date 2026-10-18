#!/usr/bin/env python3
"""
Read float32 Big-Endian holding/input registers from DeviceLab DL-ENV10 Datalogger over Modbus TCP.
Product Page: https://devicelab.vn/san-pham/dl-env10/
Solution Page: https://devicelab.vn/datalogger-quan-trac-moi-truong-tt10/
"""

import socket
import struct

DL_ENV10_IP = "192.168.1.100"
MODBUS_PORT = 502
UNIT_ID = 1

def build_read_input_registers(unit_id: int, start_addr: int, count: int, tx_id: int = 1) -> bytes:
    # MBAP Header (7 bytes) + Function Code 0x04 (Read Input Registers) + Start Addr + Quantity
    pdu = struct.pack(">BHH", 0x04, start_addr, count)
    mbap = struct.pack(">HHHB", tx_id, 0, len(pdu) + 1, unit_id)
    return mbap + pdu

def parse_float32_abcd(high_word: int, low_word: int) -> float:
    raw = struct.pack(">HH", high_word, low_word)
    return struct.unpack(">f", raw)[0]

def poll_dl_env10():
    # Read 10 Input Registers starting at 30001 (offset 0x0000): pH, COD, TSS, NH4+, Temp
    req = build_read_input_registers(UNIT_ID, start_addr=0, count=10)
    with socket.create_connection((DL_ENV10_IP, MODBUS_PORT), timeout=3.0) as sock:
        sock.sendall(req)
        resp = sock.recv(256)

    byte_count = resp[8]
    regs = struct.unpack(f">{byte_count // 2}H", resp[9:9 + byte_count])

    telemetry = {
        "pH": round(parse_float32_abcd(regs[0], regs[1]), 2),
        "COD_mg_L": round(parse_float32_abcd(regs[2], regs[3]), 2),
        "TSS_mg_L": round(parse_float32_abcd(regs[4], regs[5]), 2),
        "NH4_mg_L": round(parse_float32_abcd(regs[6], regs[7]), 2),
        "Temp_oC": round(parse_float32_abcd(regs[8], regs[9]), 2),
    }
    print("DL-ENV10 Modbus TCP Telemetry:", telemetry)

if __name__ == "__main__":
    poll_dl_env10()
