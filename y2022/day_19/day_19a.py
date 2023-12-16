#!/usr/bin/python3
import sys
from collections import deque

infile = sys.argv[1] if len(sys.argv) > 1 else '/Users/ivonet/dev/puzzle/advent-of-code/2022/day_19/day_19.input'
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]


def solve(ore_cost,
          clay_cost,
          obsidian_cost_ore,
          obsidian_cost_clay,
          geode_cost_ore,
          geode_cost_clay, T):
    best = 0
    # state is (ore, clay, obsidian, geodes, r1, r2, r3, r4, time)
    S = (0, 0, 0, 0, 1, 0, 0, 0, T)
    Q = deque([S])
    SEEN = set()
    while Q:
        state = Q.popleft()
        # print(state)
        ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot, t = state

        best = max(best, geode)
        if t == 0:
            continue

        core = max([ore_cost,
                    clay_cost,
                    obsidian_cost_ore,
                    geode_cost_ore])
        if ore_robot >= core:
            ore_robot = core
        if clay_robot >= obsidian_cost_clay:
            clay_robot = obsidian_cost_clay
        if obsidian_robot >= geode_cost_clay:
            obsidian_robot = geode_cost_clay
        if ore >= t * core - ore_robot * (t - 1):
            ore = t * core - ore_robot * (t - 1)
        if clay >= t * obsidian_cost_clay - clay_robot * (t - 1):
            clay = t * obsidian_cost_clay - clay_robot * (t - 1)
        if obsidian >= t * geode_cost_clay - obsidian_robot * (t - 1):
            obsidian = t * geode_cost_clay - obsidian_robot * (t - 1)

        state = (ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot, t)

        if state in SEEN:
            continue
        SEEN.add(state)

        if len(SEEN) % 1000000 == 0:
            print(t, best, len(SEEN))
        assert ore >= 0 and clay >= 0 and obsidian >= 0 and geode >= 0, state
        Q.append((ore + ore_robot,
                  clay + clay_robot,
                  obsidian + obsidian_robot,
                  geode + geode_robot,
                  ore_robot,
                  clay_robot,
                  obsidian_robot,
                  geode_robot,
                  t - 1))
        if ore >= ore_cost:  # buy ore
            Q.append((ore - ore_cost + ore_robot,
                      clay + clay_robot,
                      obsidian + obsidian_robot,
                      geode + geode_robot,
                      ore_robot + 1,
                      clay_robot,
                      obsidian_robot,
                      geode_robot,
                      t - 1))
        if ore >= clay_cost:
            Q.append((ore - clay_cost + ore_robot,
                      clay + clay_robot,
                      obsidian + obsidian_robot,
                      geode + geode_robot,
                      ore_robot,
                      clay_robot + 1,
                      obsidian_robot,
                      geode_robot,
                      t - 1))
        if ore >= obsidian_cost_ore and clay >= obsidian_cost_clay:
            Q.append((ore - obsidian_cost_ore + ore_robot,
                      clay - obsidian_cost_clay + clay_robot,
                      obsidian + obsidian_robot,
                      geode + geode_robot,
                      ore_robot,
                      clay_robot,
                      obsidian_robot + 1,
                      geode_robot,
                      t - 1))
        if ore >= geode_cost_ore and obsidian >= geode_cost_clay:
            Q.append((ore - geode_cost_ore + ore_robot,
                      clay + clay_robot,
                      obsidian - geode_cost_clay + obsidian_robot,
                      geode + geode_robot,
                      ore_robot,
                      clay_robot,
                      obsidian_robot,
                      geode_robot + 1,
                      t - 1))
    return best


if __name__ == '__main__':
    p1 = 0
    p2 = 1
    for i, line in enumerate(lines):
        words = line.split()
        id_ = int(words[1][:-1])
        ore_cost = int(words[6])
        clay_cost = int(words[12])
        obsidian_cost_ore, obsidian_cost_clay = int(words[18]), int(words[21])
        geode_cost_ore, geode_cost_clay = int(words[27]), int(words[30])
        s1 = solve(ore_cost,
                   clay_cost,
                   obsidian_cost_ore,
                   obsidian_cost_clay,
                   geode_cost_ore,
                   geode_cost_clay,
                   24)
        p1 += id_ * s1
        if i < 3:
            s2 = solve(ore_cost, clay_cost, obsidian_cost_ore, obsidian_cost_clay, geode_cost_ore, geode_cost_clay, 32)
            p2 *= s2
    print(p1)
    print(p2)
