#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Ivo Woltring"
__copyright__ = "Copyright (c) 2022 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
If a part of the code is not part of the post it is probably 
code I found reusable and I may have moved it to my 'ivonet' library.
you can find that here: https://github.com/IvoNet/advent-of-code/tree/master/ivonet
"""

import os
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

import sys

from ivonet.collection import Queue
from ivonet.files import read_rows
from ivonet.iter import ints

sys.dont_write_bytecode = True

DEBUG = True


# noinspection DuplicatedCode
def _(*args, end="\n", sep=" "):
    if DEBUG:
        print(sep.join(str(x) for x in args), end=end)


@dataclass(frozen=True, order=True)
class Cost:
    ore: int
    clay: int


class OreRobot(Cost):
    pass


class ClayRobot(Cost):
    pass


class ObsidianRobot(Cost):
    pass


class GeodeRobot(Cost):
    pass


class Blueprint(NamedTuple):
    name: int
    ore_robot: OreRobot
    clay_robot: ClayRobot
    obsidian_robot: ObsidianRobot
    geode_robot: GeodeRobot


class Factory:

    def __init__(self, source, minutes=24) -> None:
        self.time_left = minutes
        self.source = source
        self.blueprint: dict[int, Blueprint] = {}
        for line in source:
            cost = ints(line)
            identifier = cost[0]
            ore = OreRobot(cost[1], 0)
            clay = ClayRobot(cost[2], 0)
            obsidian = ObsidianRobot(cost[3], cost[4])
            geode = GeodeRobot(cost[5], cost[6])
            self.blueprint[identifier] = Blueprint(identifier, ore, clay, obsidian, geode)

    def run_blueprint(self, blueprint, time_left=24):
        queue = Queue()
        #  ore, clay, obsidian, geodes,  ore_robot, clay_robot, obsidian_robot, geode_robot, time)
        #   0,    1,       2,       3,          4,          5,          6,            7,       8
        queue.push((0, 0, 0, 0, 1, 0, 0, 0, time_left))
        explored = set()
        best_quality = 0
        while not queue.empty:
            state_machine = queue.pop()

            ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot, time_left = state_machine

            best_quality = max(best_quality, geode)

            if time_left <= 0:
                continue

            core = max(blueprint.ore_robot.ore,
                       blueprint.clay_robot.ore,
                       blueprint.obsidian_robot.ore,
                       blueprint.geode_robot.ore)
            if ore_robot >= core:
                ore_robot = core
            if clay_robot >= blueprint.obsidian_robot.clay:
                clay_robot = blueprint.obsidian_robot.clay
            if obsidian_robot >= blueprint.geode_robot.clay:
                obsidian_robot = blueprint.geode_robot.clay
            ore_robot_gain = time_left * core - ore_robot * (time_left - 1)
            if ore >= ore_robot_gain:
                ore = ore_robot_gain
            clay_robot_gain = time_left * blueprint.obsidian_robot.clay - clay_robot * (time_left - 1)
            if clay >= clay_robot_gain:
                clay = clay_robot_gain
            obsidian_robot_gain = time_left * blueprint.geode_robot.clay - obsidian_robot * (time_left - 1)
            if obsidian >= obsidian_robot_gain:
                obsidian = obsidian_robot_gain

            state_machine = (ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot, time_left)

            if state_machine in explored:
                continue
            explored.add(state_machine)

            queue.push((ore + ore_robot,
                        clay + clay_robot,
                        obsidian + obsidian_robot,
                        geode + geode_robot,
                        ore_robot + 1,
                        clay_robot,
                        obsidian_robot,
                        geode_robot,
                        time_left - 1))
            if ore >= blueprint.ore_robot.ore:
                queue.push((ore - blueprint.ore_robot.ore + ore_robot,
                            clay + clay_robot,
                            obsidian + obsidian_robot,
                            geode + geode_robot,
                            ore_robot + 1,
                            clay_robot,
                            obsidian_robot,
                            geode_robot,
                            time_left - 1))
            if ore >= blueprint.clay_robot.ore:
                queue.push((ore - blueprint.clay_robot.ore + ore_robot,
                            clay + clay_robot,
                            obsidian + obsidian_robot,
                            geode + geode_robot,
                            ore_robot,
                            clay_robot + 1,
                            obsidian_robot,
                            geode_robot,
                            time_left - 1))
            if ore >= blueprint.obsidian_robot.ore and clay >= blueprint.obsidian_robot.clay:
                queue.push((ore - blueprint.obsidian_robot.ore + ore_robot,
                            clay - blueprint.obsidian_robot.clay + clay_robot,
                            obsidian + obsidian_robot,
                            geode + geode_robot,
                            ore_robot,
                            clay_robot,
                            obsidian_robot + 1,
                            geode_robot,
                            time_left - 1))
            if ore >= blueprint.geode_robot.ore and clay >= blueprint.geode_robot.clay:
                queue.push((ore - blueprint.geode_robot.ore + ore_robot,
                            clay + clay_robot,
                            obsidian - blueprint.geode_robot.clay + obsidian_robot,
                            geode + geode_robot,
                            ore_robot,
                            clay_robot,
                            obsidian_robot,
                            geode_robot + 1,
                            time_left - 1))

        return best_quality

    def run(self):
        quality = 0
        for name, blueprint in self.blueprint.items():
            q = self.run_blueprint(blueprint)
            quality += name * q
            _(name, q, quality)
        return quality


def part_1(source, minutes=24):
    factory = Factory(source, minutes).run()
    return factory


def part_2(source):
    return None


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        if DEBUG:
            print()
        day = str(ints(Path(__file__).name)[0])
        self.source = read_rows(f"{os.path.dirname(__file__)}/day_{day.zfill(2)}.input")
        self.test_source = read_rows("""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""")

    def test_example_data_part_1(self):
        self.assertEqual(33, part_1(self.test_source))

    def test_part_1(self):
        self.assertEqual(1834, part_1(self.source))

    def test_example_data_part_2(self):
        self.assertEqual(None, part_2(self.test_source))

    def test_part_2(self):
        self.assertEqual(2240, part_2(self.source))


if __name__ == '__main__':
    unittest.main()
