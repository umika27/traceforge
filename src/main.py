import pygame
import time

from astar import astar, count_turns

# CONFIGURATION


CELL_SIZE = 15

GRID_WIDTH = 50
GRID_HEIGHT = 40

BOARD_WIDTH = GRID_WIDTH * CELL_SIZE
BOARD_HEIGHT = GRID_HEIGHT * CELL_SIZE

WINDOW_HEIGHT = BOARD_HEIGHT + 110

FPS = 60

# COLORS
BACKGROUND = (25, 25, 25)
GRID_COLOR = (55, 55, 55)

OBSTACLE_COLOR = (100, 100, 100)

START_COLOR = (50, 200, 80)
END_COLOR = (220, 60, 60)

PATH_COLOR = (50, 150, 255)
VISITED_COLOR = (70, 70, 120)

TEXT_COLOR = (240, 240, 240)
PANEL_COLOR = (20, 20, 20)

# INITIALIZE PYGAME
pygame.init()

screen = pygame.display.set_mode(
    (BOARD_WIDTH, WINDOW_HEIGHT)
)

pygame.display.set_caption(
    "TraceForge - PCB Auto-Router"
)

clock = pygame.time.Clock()

font = pygame.font.SysFont(
    "Arial",
    18
)

title_font = pygame.font.SysFont(
    "Arial",
    22,
    bold=True
)


# PCB GRID

grid = [
    [0 for _ in range(GRID_WIDTH)]
    for _ in range(GRID_HEIGHT)
]



# START AND END PADS

start = (3, 3)

end = (45, 35)



# ADD OBSTACLE


def add_obstacle(x1, y1, x2, y2):

    for y in range(y1, y2 + 1):

        for x in range(x1, x2 + 1):

            if (
                0 <= x < GRID_WIDTH
                and
                0 <= y < GRID_HEIGHT
            ):

                grid[y][x] = 1


# CREATE SAMPLE PCB COMPONENTS

def create_sample_board():

    # Component 1
    add_obstacle(
        12, 8,
        25, 13
    )

    # Component 2
    add_obstacle(
        30, 5,
        40, 10
    )

    # Component 3
    add_obstacle(
        18, 20,
        30, 26
    )

    # Component 4
    add_obstacle(
        35, 22,
        44, 29
    )



# RESET BOARD

def reset_board():

    global grid

    grid = [
        [0 for _ in range(GRID_WIDTH)]
        for _ in range(GRID_HEIGHT)
    ]

    create_sample_board()


# DRAW PCB GRID


def draw_board():

    for y in range(GRID_HEIGHT):

        for x in range(GRID_WIDTH):

            rect = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            # Empty PCB area

            pygame.draw.rect(
                screen,
                BACKGROUND,
                rect
            )

            # Component / obstacle

            if grid[y][x] == 1:

                pygame.draw.rect(
                    screen,
                    OBSTACLE_COLOR,
                    rect
                )

            # Grid lines

            pygame.draw.rect(
                screen,
                GRID_COLOR,
                rect,
                1
            )


# DRAW SINGLE CELL

def draw_cell(
    position,
    color
):

    x, y = position

    rect = pygame.Rect(
        x * CELL_SIZE + 2,
        y * CELL_SIZE + 2,
        CELL_SIZE - 4,
        CELL_SIZE - 4
    )

    pygame.draw.rect(
        screen,
        color,
        rect
    )

# DRAW ROUTE

def draw_path(path):

    if not path:
        return

    for node in path:

        if node != start and node != end:

            draw_cell(
                node,
                PATH_COLOR
            )

# DRAW SEARCHED NODES

def draw_visited(visited):

    for node in visited:

        if node != start and node != end:

            draw_cell(
                node,
                VISITED_COLOR
            )



# DRAW START / END

def draw_pads():

    draw_cell(
        start,
        START_COLOR
    )

    draw_cell(
        end,
        END_COLOR
    )


# DRAW TEXT


def draw_text(
    text,
    x,
    y,
    font_object=font
):

    text_surface = font_object.render(
        text,
        True,
        TEXT_COLOR
    )

    screen.blit(
        text_surface,
        (x, y)
    )


# DRAW INFORMATION PANEL

def draw_panel(
    path,
    visited,
    routing_time
):

    panel_y = BOARD_HEIGHT

    pygame.draw.rect(
        screen,
        PANEL_COLOR,
        (
            0,
            panel_y,
            BOARD_WIDTH,
            WINDOW_HEIGHT - BOARD_HEIGHT
        )
    )

    # Title

    draw_text(
        "TraceForge - PCB Auto-Router",
        10,
        panel_y + 8,
        title_font
    )

    # Controls

    draw_text(
        "SPACE: Route    R: Reset    ESC: Exit",
        10,
        panel_y + 38
    )

    # Status

    if path:

        path_length = len(path) - 1

        turns = count_turns(path)

        draw_text(
            "STATUS: ROUTE FOUND ✓",
            320,
            panel_y + 8
        )

        draw_text(
            f"Path Length: {path_length} cells",
            320,
            panel_y + 35
        )

        draw_text(
            f"Turns: {turns}",
            320,
            panel_y + 62
        )

        draw_text(
            f"Nodes Explored: {len(visited)}",
            500,
            panel_y + 35
        )

        draw_text(
            f"Time: {routing_time * 1000:.3f} ms",
            500,
            panel_y + 62
        )

    else:

        draw_text(
            "STATUS: READY TO ROUTE",
            320,
            panel_y + 8
        )

        draw_text(
            "Press SPACE to run A*",
            320,
            panel_y + 35
        )


# 
# ROUTE PCB

def route_pcb():

    print("Starting A* routing...")

    start_time = time.perf_counter()

    path, visited = astar(
        grid,
        start,
        end
    )

    routing_time = (
        time.perf_counter()
        - start_time
    )

    if path:

        print()
        print("========== ROUTING RESULT ==========")

        print(
            f"Status: SUCCESS"
        )

        print(
            f"Path length: {len(path) - 1} cells"
        )

        print(
            f"Turns: {count_turns(path)}"
        )

        print(
            f"Nodes explored: {len(visited)}"
        )

        print(
            f"Routing time: {routing_time * 1000:.3f} ms"
        )

        print(
            "===================================="
        )

    else:

        print()
        print("========== ROUTING RESULT ==========")

        print(
            "Status: NO ROUTE FOUND"
        )

        print(
            f"Nodes explored: {len(visited)}"
        )

        print(
            "===================================="
        )

    return path, visited, routing_time


# 
# MAIN LOOP

def main():

    create_sample_board()

    running = True

    path = None

    visited = []

    routing_time = 0

    while running:

        # EVENTS

        for event in pygame.event.get():

            # Close window

            if event.type == pygame.QUIT:

                running = False

            # Keyboard

            if event.type == pygame.KEYDOWN:

                # Exit

                if event.key == pygame.K_ESCAPE:

                    running = False

                # Route

                elif event.key == pygame.K_SPACE:

                    (
                        path,
                        visited,
                        routing_time
                    ) = route_pcb()

                # Reset

                elif event.key == pygame.K_r:

                    reset_board()

                    path = None

                    visited = []

                    routing_time = 0

        # DRAW

        screen.fill(
            BACKGROUND
        )

        # PCB

        draw_board()

        # A* explored nodes

        draw_visited(
            visited
        )

        # Final route

        draw_path(
            path
        )

        # Pads

        draw_pads()

        # Information panel

        draw_panel(
            path,
            visited,
            routing_time
        )

        # UPDATE
         

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
# PROGRAM ENTRY POINT
if __name__ == "__main__":

    main()