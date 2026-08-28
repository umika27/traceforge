import heapq


# HEURISTIC

def heuristic(a, b):
    """
    Manhattan distance between two grid cells.

    a = (x, y)
    b = (x, y)

    Used by A* to estimate the remaining distance
    from the current node to the destination.
    """

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# GET VALID NEIGHBORS


def get_neighbors(grid, node):
    """
    Return all valid neighboring cells.

    PCB routing currently allows movement in four directions:

        UP
        DOWN
        LEFT
        RIGHT

    Diagonal movement is not allowed.
    """

    x, y = node

    possible_neighbors = [

        (x + 1, y),   # RIGHT
        (x - 1, y),   # LEFT
        (x, y + 1),   # DOWN
        (x, y - 1)    # UP

    ]

    neighbors = []

    height = len(grid)
    width = len(grid[0])

    for nx, ny in possible_neighbors:

        # Check whether the cell is inside the PCB

        if (
            0 <= nx < width
            and
            0 <= ny < height
        ):

            # 0 = available
            # 1 = obstacle

            if grid[ny][nx] == 0:

                neighbors.append((nx, ny))

    return neighbors


# RECONSTRUCT PATH
def reconstruct_path(came_from, current):

    #Reconstruct the final route by following parent nodes backwards from the destination.
    path = [current]

    while current in came_from:

        current = came_from[current]

        path.append(current)

    # We reconstructed the path backwards,
    # so reverse it.

    path.reverse()

    return path


# A* PATHFINDING

def astar(grid, start, goal):
    """
    A* pathfinding algorithm.

    Parameters
    ----------
    grid:
        2D PCB grid.

        0 = free
        1 = obstacle

    start:
        Starting pad (x, y)

    goal:
        Destination pad (x, y)

    Returns
    -------
    path:
        List of cells representing the route.

    visited:
        List of cells explored by A*.
    """

    
    # Priority Queue

    open_set = []

    # The first value is the priority.
    # Start has f-score = 0 initially.

    heapq.heappush(
        open_set,
        (0, start)
    )

    
    # Cost from start to each node
    

    g_score = {

        start: 0

    }

    # Parent of each node

    came_from = {}

    # Nodes explored by the algorithm
    

    visited = []

    # MAIN A* LOOP

    while open_set:

        # Get node with lowest priority

        _, current = heapq.heappop(
            open_set
        )

        # Record that we explored this node

        visited.append(
            current
        )

        # GOAL CHECK

        if current == goal:

            path = reconstruct_path(
                came_from,
                current
            )

            return path, visited

        
        # EXPLORE NEIGHBORS
        

        for neighbor in get_neighbors(
            grid,
            current
        ):

            movement_cost = 1

            tentative_g_score = (
                g_score[current]
                +
                movement_cost
            )

            
            # Is this a better route?

            if (
                neighbor not in g_score
                or
                tentative_g_score
                <
                g_score[neighbor]
            ):

                # Store parent

                came_from[neighbor] = current

                # Store new cost

                g_score[neighbor] = (
                    tentative_g_score
                )

                # ------------------------------------------------
                # A* COST
                #
                # f(n) = g(n) + h(n)
                # ------------------------------------------------

                h_score = heuristic(
                    neighbor,
                    goal
                )

                f_score = (
                    tentative_g_score
                    +
                    h_score
                )

                # Add node to priority queue

                heapq.heappush(
                    open_set,
                    (
                        f_score,
                        neighbor
                    )
                )

    # NO PATH FOUND
    

    return None, visited


# COUNT TURNS


def count_turns(path):
    """
    Count the number of 90-degree turns in a route.
    """

    if not path or len(path) < 3:

        return 0

    turns = 0

    for i in range(
        1,
        len(path) - 1
    ):

        previous = path[i - 1]

        current = path[i]

        next_node = path[i + 1]

        # Direction of first movement

        direction_1 = (
            current[0] - previous[0],
            current[1] - previous[1]
        )

        # Direction of second movement

        direction_2 = (
            next_node[0] - current[0],
            next_node[1] - current[1]
        )

        # If direction changes,we have a turn

        if direction_1 != direction_2:

            turns += 1

    return turns