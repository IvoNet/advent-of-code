#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"

import sys
import unittest
from dataclasses import dataclass, field
from pathlib import Path

from ivonet.calc import base_x_to_10, prod
from ivonet.files import read_data
from ivonet.iter import ints, chunkify

sys.dont_write_bytecode = True

TRANSLATE = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

FUNC = {
    0: "sum({}), ",
    1: "prod({}), ",
    2: "min({}), ",
    3: "max({}), ",
    4: "{},",
    5: "(1 if ({} > {}) else 0), ",
    6: "(1 if ({} < {}) else 0), ",
    7: "(1 if ({} = {}) else 0), ",
}


def visualize(pl: list[Packet]) -> str:
    ret = ""
    for packet in pl:
        if packet.type_id == 0:
            ret += FUNC[packet.type_id].format(visualize(packet.children))
        elif packet.type_id == 1:
            ret += FUNC[packet.type_id].format(visualize(packet.children))
        elif packet.type_id == 2:
            ret += FUNC[packet.type_id].format(visualize(packet.children))
        elif packet.type_id == 3:
            ret += FUNC[packet.type_id].format(visualize(packet.children))
        elif packet.type_id == 4:
            ret += FUNC[packet.type_id].format(packet.value)
        elif packet.type_id == 5:
            ret += FUNC[packet.type_id].format(visualize([packet.children[0]]), visualize([packet.children[1]]))
        elif packet.type_id == 6:
            ret += FUNC[packet.type_id].format(visualize([packet.children[0]]), visualize([packet.children[1]]))
        elif packet.type_id == 7:
            ret += FUNC[packet.type_id].format(visualize([packet.children[0]]), visualize([packet.children[1]]))
        else:
            raise ValueError(f"Unknown type_id: {packet.type_id}")

    if ret.endswith(", "):
        return ret[:-2]
    return ret


def hex_2_bin(s: str) -> str:
    return "".join(TRANSLATE[x] for x in s)


def b2d(s):
    return base_x_to_10(s, base=2)


def literal_value(s: str):
    values = [x for x in chunkify(s, 5) if len(x) == 5]
    b = "".join([x[1:] for x in values])
    return b2d(b)


@dataclass
class Packet:
    version: int
    type_id: int
    value: int = 0
    children: list[Packet] = field(default_factory=list)


class BITS(object):
    """
        packet := packet + packet |
                  header(6) + literal_value |
                  header + operator_packet
        header(6) := version(3) + type_id(3)
        version := number
        type_id := literal_value(=4) | operator_value(!=4)
        operator_packet := length_type_id(1) + sub_packets_amount(11) + sub_packets |
                           length_type_id(1) + total_length_sub_packets(15) + sub_packets
        length_type_id(1) := 0 -> 15 bits -> b2d representing the total length of the sub_packets (NOT LITERAL just binary)
                             1 -> 11 bits -> b2d value representing the total nr of sub_package
        sub_package := header + literal_value |
                       header +

        so in the end:
        - Packet := version + type_id + [ value* | Packet]

    """

    def __init__(self, hex: str) -> None:
        self.hex = hex
        self.binary = hex_2_bin(self.hex)

    @staticmethod
    def take(data: str, size: int) -> tuple[str, str]:
        return data[:size], data[size:]

    def consume_version(self, data) -> tuple[int, str]:
        version, data = self.take(data, 3)
        return b2d(version), data

    def consume_type_id(self, data) -> tuple[int, str]:
        v, d = self.take(data, 3)
        return b2d(v), d

    def consume_literal(self, data) -> tuple[int, str]:
        val = ""
        more = "1"
        while more == "1":
            more, data = self.take(data, 1)
            b4, data = self.take(data, 4)
            val += b4
        return b2d(val), data

    def consume_lti(self, data) -> tuple[str, str]:
        return self.take(data, 1)

    def consume_sub_package_count(self, data: str) -> tuple[int, str]:
        v, d = self.take(data, 11)
        return b2d(v), d

    def consume_total_length_in_bits(self, data) -> tuple[int, str]:
        v, d = self.take(data, 15)
        return b2d(v), d

    def parse(self, data: str) -> tuple[Packet, str]:
        version, data = self.consume_version(data)
        type_id, data = self.consume_type_id(data)
        packet = Packet(version, type_id)
        if type_id == 4:  # Literal value
            packet.value, data = self.consume_literal(data)
        else:  # Operator packet
            lti, data = self.consume_lti(data)
            if lti == "0":
                sub_bits, data = self.consume_total_length_in_bits(data)
                sub_data, data = self.take(data, sub_bits)
                while sub_data:
                    sub_package, sub_data = self.parse(sub_data)
                    packet.children.append(sub_package)
            else:
                sub_package_count, data = self.consume_sub_package_count(data)
                for _ in range(sub_package_count):
                    sub_package, data = self.parse(data)
                    packet.children.append(sub_package)
        return packet, data

    def go(self):
        return self.parse(self.binary)


def print_operators():
    print("sum:", BITS("C200B40A82").go()[0].type_id)
    print("prod:", BITS("04005AC33890").go()[0].type_id)
    print("min:", BITS("880086C3E88112").go()[0].type_id)
    print("max:", BITS("CE00C43D881120").go()[0].type_id)
    print("lt:", BITS("D8005AC2A8F0").go()[0].type_id)  # 1 of true else 0?
    print("gt:", BITS("F600BC2D8F").go()[0].type_id)
    print("ne:", BITS("9C005AC2F8F0").go()[0].type_id)  # equal test false
    print("eq:", BITS("9C0141080250320F1802104A08").go()[0].type_id)  # equal test true


def calculate(packet: Packet) -> int:
    if packet.type_id == 0:
        return sum([calculate(c) for c in packet.children])
    elif packet.type_id == 1:
        return prod([calculate(c) for c in packet.children])
    elif packet.type_id == 2:
        return min([calculate(c) for c in packet.children])
    elif packet.type_id == 3:
        return max([calculate(c) for c in packet.children])
    elif packet.type_id == 4:
        return packet.value
    elif packet.type_id == 5:
        return 1 if calculate(packet.children[0]) > calculate(packet.children[1]) else 0
    elif packet.type_id == 6:
        return 1 if calculate(packet.children[0]) < calculate(packet.children[1]) else 0
    elif packet.type_id == 7:
        return 1 if calculate(packet.children[0]) == calculate(packet.children[1]) else 0
    else:
        raise ValueError(f"Unknown type_id: {packet.type_id}")


def sum_versions(ps: list[Packet]) -> int:
    return sum([sum_versions(p.children) + p.version for p in ps])


def part_1(source):
    bits = BITS(source)
    packet, data = bits.go()
    assert all(c == "0" for c in data)
    return sum_versions([packet])


def part_2(source):
    bits = BITS(source)
    packet, data = bits.go()
    assert all(c == "0" for c in data)
    result = calculate(packet)
    print("\n\n")
    print(visualize([packet]), " = ", result)
    return result


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        day = str(ints(Path(__file__).name)[0])
        self.source = read_data(f"day_{day.zfill(2)}.input")
        self.test_source = read_data("""D2FE28""")
        self.test_source_a = read_data("""8A004A801A8002F478""")  # 16
        self.test_source_b = read_data("""620080001611562C8802118E34""")  # 12
        self.test_source_c = read_data("""C0015000016115A2E0802F182340""")  # 23
        self.test_source_d = read_data("""A0016C880162017C3686B18A3D4780""")  # 31

    def test_example_data_part_1(self):
        self.assertEqual(6, part_1(self.test_source))

    def test_example_data_part_1_a(self):
        self.assertEqual(16, part_1(self.test_source_a))

    def test_example_data_part_1_b(self):
        self.assertEqual(12, part_1(self.test_source_b))

    def test_example_data_part_1_c(self):
        self.assertEqual(23, part_1(self.test_source_c))

    def test_example_data_part_1_d(self):
        self.assertEqual(31, part_1(self.test_source_d))

    def test_part_1(self):
        self.assertEqual(969, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(2021, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(124921618408, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
