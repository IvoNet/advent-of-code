def shoelace_theorem(coords: list[tuple[int, int]]) -> int:
    """
    Calculate the area of a polygon using the Shoelace Theorem.
    https://en.wikipedia.org/wiki/Shoelace_formula

    Parameters:
    - coords: List of (row, column) pairs representing the vertices.

    Returns:
    - Area of the polygon.

    Note:
        see y2023/day_18.py for an example usage
    """

    # Ensure the polygon is closed
    if coords[0] != coords[-1]:
        coords.append(coords[0])

    n = len(coords)

    # Calculate the area using the Shoelace Theorem
    area = 0.0
    for i in range(n - 1):
        left_r, left_c = coords[i]
        right_r, right_c = coords[i + 1]
        area += left_r * right_c - right_r * left_c
    area = abs(area) // 2
    return int(area)


def shoelace(path: list[tuple[int, int]]) -> int:
    """
    same as shoelace_theorem but witt solved differently
    """
    return sum((y1 + y2) * (x2 - x1) for ((x1, y1), (x2, y2)) in zip(path, path[1:])) // 2


def picks_theorem(area, boundary_points):
    """
    Calculate the number of interior points of a simple lattice polygon using Pick's Theorem.
    https://en.wikipedia.org/wiki/Pick%27s_theorem
    I changed this one to give the interior points instead of the area as I can get the area
    from the shoelace theorem, and I am missing the interior points.

    Parameters:
    - area: Area of the polygon.
    - boundary_points: Number of lattice points on the boundary.

    Returns:
    - Number of interior points.

    Note:
        see y2023/day_18.py for an example usage
    """
    interior_points = area + 1 - boundary_points // 2
    return interior_points


def is_point_inside_polygon(x, y, polygon):
    """
    Check if a point (x, y) is inside a polygon.
    https://en.wikipedia.org/wiki/Point_in_polygon

    Parameters:
    - x: x-coordinate of the point.
    - y: y-coordinate of the point.
    - polygon: List of (x, y) coordinates representing the vertices of the polygon.

    Returns:
    - True if the point is inside the polygon, False otherwise.
    """
    n = len(polygon)
    inside = False

    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[(i + 1) % n]

        # Check if the point is on the boundary
        if y == yi and (x == xi or x == xj):
            return True

        # Check if the ray intersects with the edge
        if (yi < y and yj >= y) or (yj < y and yi >= y):
            if xi + (y - yi) / (yj - yi) * (xj - xi) < x:
                inside = not inside

    return inside
