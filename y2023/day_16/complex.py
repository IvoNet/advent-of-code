#!/usr/bin/env python3
#  -*- coding: utf-8 -*-


def navigate_through_grid():
    # Starting point
    current_position = 0 + 0j  # Complex number representing (0,0)

    # Define movements using imaginary numbers
    move_right = 1  # Move one unit to the right
    move_up = 1j  # Move one unit up
    move_left = -1  # Move one unit to the left
    move_down = -1j  # Move one unit down

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


# Call the function to see the navigation
navigate_through_grid()
