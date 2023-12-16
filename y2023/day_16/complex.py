#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

# Define movements using imaginary numbers
move_right = 1j  # Move one unit to the right
move_up = -1  # Move one unit up
move_left = -1j  # Move one unit to the left
move_down = 1  # Move one unit down


def navigate_through_grid():
    # Starting point
    current_position = 0 + 0j  # Complex number representing (0,0)

    # List of movements to navigate through the grid
    movements = [move_right, move_up, move_left, move_down]

    # Navigate through the grid
    for movement in movements:
        current_position += movement
        print(f"Moved to 1: {int(current_position.real), int(current_position.imag)} - {current_position}")

    for movement in movements:
        current_position -= movement
        print(f"Moved to 2: {int(current_position.real), int(current_position.imag)} - {current_position}")

    for movement in movements:
        nd = current_position.real * movement
        print(f"Moved to 3: {int(nd.real), int(nd.imag)} - {current_position}")

    start = 0 + 0j
    start_direction = -1 - 0j
    for i in range(10):
        start += start_direction
        print(f"Moved to 4: {int(start.real), int(start.imag)} - {start}")

    grid = [list(row) for row in ["....", "....", "....", "...."]]
    pos = 0 + 0j
    for direction in [move_right, move_down, move_left, move_up]:
        for i in range(len(grid) - 1):
            print(f"Moved to 5: {int(pos.real), int(pos.imag)} - {pos}")
            grid[int(pos.imag)][int(pos.real)] = "#"
            pos += direction
    print("\n".join("".join(row) for row in grid))

    def turn_left(direction):
        return direction * move_left

    def turn_right(direction):
        return direction * move_right

    direction = move_right
    pos = 0 + 0j
    for i in range(10):
        print(f"Moved to 6: {int(pos.real), int(pos.imag)} - {pos}")
        pos += direction
        direction = turn_left(direction)


def moving():
    # /
    current_direction = move_up  # Moving up en find ing / should go right
    current_direction *= -1j
    assert current_direction == move_right
    current_direction = move_down  # Moving up en find ing / should go right
    current_direction *= -1j
    assert current_direction == move_left
    current_direction = move_right  # Moving up en find ing / should go right
    current_direction *= 1j
    assert current_direction == move_up
    current_direction = move_left  # Moving up en find ing / should go right
    current_direction *= 1j
    assert current_direction == move_down

    # \
    current_direction = move_up  # Moving up en find ing / should go right
    current_direction *= 1j
    assert current_direction == move_left
    current_direction = move_down  # Moving up en find ing / should go right
    current_direction *= 1j
    assert current_direction == move_right
    current_direction = move_right  # Moving up en find ing / should go right
    current_direction *= -1j
    assert current_direction == move_down
    current_direction = move_left  # Moving up en find ing / should go right
    current_direction *= -1j
    assert current_direction == move_up


# Call the function to see the navigation
# navigate_through_grid()

moving()
