import pygame
import time

from astar import astar, count_turns


# ============================================================
# TRACEFORGE
# Interactive PCB Auto-Router
# Milestone 2
# ============================================================


# ============================================================
# CONFIGURATION
# ============================================================

CELL_SIZE = 15

GRID_WIDTH = 50
GRID_HEIGHT = 40

BOARD_WIDTH = GRID_WIDTH * CELL_SIZE
BOARD_HEIGHT = GRID_HEIGHT * CELL_SIZE

PANEL_HEIGHT = 150

WINDOW_WIDTH = BOARD_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT + PANEL_HEIGHT

FPS = 60


# ============================================================
# COLORS
# ============================================================

BACKGROUND = (25, 25, 25)

GRID_COLOR = (55, 55, 55)

OBSTACLE_COLOR = (105, 105, 105)

START_COLOR = (50, 210, 80)

END_COLOR = (230, 60, 60)

PATH_COLOR = (40, 150, 255)

VISITED_COLOR = (65, 65, 120)

PANEL_COLOR = (18, 18, 18)

TEXT_COLOR = (240, 240, 240)

SECONDARY_TEXT = (170, 170, 170)

HIGHLIGHT_COLOR = (255, 200, 70)


# ============================================================
# INITIALIZE PYGAME
# ============================================================

pygame.init()

screen = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)

pygame.display.set_caption(
    "TraceForge - PCB Auto-Router"
)

clock = pygame.time.Clock()


# ============================================================
# FONTS
# ============================================================

font = pygame.font.SysFont(
    "Arial",
    17
)

small_font = pygame.font.SysFont(
    "Arial",
    14
)

title_font = pygame.font.SysFont(
    "Arial",
    22,
    bold=True
)


# ============================================================
# PCB GRID
# ============================================================

grid = [
    [0 for _ in range(GRID_WIDTH)]
    for _ in range(GRID_HEIGHT)
]


# ============================================================
# START / END PADS
# ============================================================

start = (3, 3)

end = (45, 35)


# ============================================================
# APPLICATION STATE
# ============================================================

# Current editing mode:
#
# "obstacle"
# "start"
# "end"
# "erase"

mode = "obstacle"

path = None

visited = []

routing_time = 0

mouse_down = False


# ============================================================
# ADD RECTANGULAR OBSTACLE
# ============================================================

def add_obstacle(x1, y1, x2, y2):

    for y in range(y1, y2 + 1):

        for x in range(x1, x2 + 1):

            if (
                0 <= x < GRID_WIDTH
                and 0 <= y < GRID_HEIGHT
            ):

                # Don't place obstacles on pads

                if (x, y) != start and (x, y) != end:

                    grid[y][x] = 1


# ============================================================
# CREATE INITIAL DEMO BOARD
# ============================================================

def create_sample_board():

    add_obstacle(
        12, 8,
        25, 13
    )

    add_obstacle(
        30, 5,
        40, 10
    )

    add_obstacle(
        18, 20,
        30, 26
    )

    add_obstacle(
        35, 22,
        44, 29
    )


# ============================================================
# RESET BOARD
# ============================================================

def reset_board():

    global grid
    global start
    global end
    global path
    global visited
    global routing_time
    global mode

    grid = [
        [0 for _ in range(GRID_WIDTH)]
        for _ in range(GRID_HEIGHT)
    ]

    start = (3, 3)

    end = (45, 35)

    create_sample_board()

    path = None

    visited = []

    routing_time = 0

    mode = "obstacle"


# ============================================================
# CLEAR ROUTE
# ============================================================

def clear_route():

    global path
    global visited
    global routing_time

    path = None

    visited = []

    routing_time = 0


# ============================================================
# CONVERT MOUSE POSITION TO GRID CELL
# ============================================================

def mouse_to_grid(position):

    mouse_x, mouse_y = position

    if mouse_y >= BOARD_HEIGHT:

        return None

    grid_x = mouse_x // CELL_SIZE

    grid_y = mouse_y // CELL_SIZE

    if (
        0 <= grid_x < GRID_WIDTH
        and
        0 <= grid_y < GRID_HEIGHT
    ):

        return (grid_x, grid_y)

    return None


# ============================================================
# EDIT PCB
# ============================================================

def edit_cell(cell):

    global start
    global end

    if cell is None:

        return

    x, y = cell

    # --------------------------------------------------------
    # OBSTACLE MODE
    # --------------------------------------------------------

    if mode == "obstacle":

        # Don't overwrite pads

        if cell != start and cell != end:

            grid[y][x] = 1

            clear_route()

    # --------------------------------------------------------
    # ERASE MODE
    # --------------------------------------------------------

    elif mode == "erase":

        grid[y][x] = 0

        clear_route()

    # --------------------------------------------------------
    # START MODE
    # --------------------------------------------------------

    elif mode == "start":

        # Start cannot be placed inside obstacle

        if grid[y][x] == 0:

            # Don't place start on end

            if cell != end:

                start = cell

                clear_route()

    # --------------------------------------------------------
    # END MODE
    # --------------------------------------------------------

    elif mode == "end":

        if grid[y][x] == 0:

            if cell != start:

                end = cell

                clear_route()


# ============================================================
# DRAW PCB
# ============================================================

def draw_board():

    for y in range(GRID_HEIGHT):

        for x in range(GRID_WIDTH):

            rect = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            # PCB background

            pygame.draw.rect(
                screen,
                BACKGROUND,
                rect
            )

            # Component / keep-out area

            if grid[y][x] == 1:

                pygame.draw.rect(
                    screen,
                    OBSTACLE_COLOR,
                    rect
                )

            # Grid

            pygame.draw.rect(
                screen,
                GRID_COLOR,
                rect,
                1
            )


# ============================================================
# DRAW CELL
# ============================================================

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


# ============================================================
# DRAW ROUTE
# ============================================================

def draw_path():

    if not path:

        return

    for node in path:

        if node != start and node != end:

            draw_cell(
                node,
                PATH_COLOR
            )


# ============================================================
# DRAW A* SEARCH
# ============================================================

def draw_visited():

    for node in visited:

        if (
            node != start
            and node != end
            and not (
                path and node in path
            )
        ):

            draw_cell(
                node,
                VISITED_COLOR
            )


# ============================================================
# DRAW PADS
# ============================================================

def draw_pads():

    draw_cell(
        start,
        START_COLOR
    )

    draw_cell(
        end,
        END_COLOR
    )


# ============================================================
# DRAW TEXT
# ============================================================

def draw_text(
    text,
    x,
    y,
    font_object=font,
    color=TEXT_COLOR
):

    surface = font_object.render(
        text,
        True,
        color
    )

    screen.blit(
        surface,
        (x, y)
    )


# ============================================================
# DRAW INFORMATION PANEL
# ============================================================

def draw_panel():

    panel_y = BOARD_HEIGHT

    pygame.draw.rect(
        screen,
        PANEL_COLOR,
        (
            0,
            panel_y,
            WINDOW_WIDTH,
            PANEL_HEIGHT
        )
    )

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    draw_text(
        "TRACEFORGE",
        15,
        panel_y + 10,
        title_font
    )

    draw_text(
        "PCB Auto-Routing & Optimization Engine",
        150,
        panel_y + 14,
        small_font,
        SECONDARY_TEXT
    )

    # --------------------------------------------------------
    # MODE
    # --------------------------------------------------------

    draw_text(
        f"MODE: {mode.upper()}",
        15,
        panel_y + 48,
        font,
        HIGHLIGHT_COLOR
    )

    # --------------------------------------------------------
    # CONTROLS
    # --------------------------------------------------------

    draw_text(
        "Left Click: Edit    Right Click: Erase",
        180,
        panel_y + 48
    )

    draw_text(
        "S + Click: Start    E + Click: End",
        180,
        panel_y + 72
    )

    draw_text(
        "SPACE: Route    R: Reset    ESC: Exit",
        180,
        panel_y + 96
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if path:

        path_length = len(path) - 1

        turns = count_turns(path)

        draw_text(
            "STATUS: ROUTE FOUND ✓",
            15,
            panel_y + 76,
            font,
            START_COLOR
        )

        draw_text(
            f"Length: {path_length} cells",
            15,
            panel_y + 103,
            small_font
        )

        draw_text(
            f"Turns: {turns}",
            15,
            panel_y + 125,
            small_font
        )

        draw_text(
            f"Nodes: {len(visited)}",
            370,
            panel_y + 103,
            small_font
        )

        draw_text(
            f"Time: {routing_time * 1000:.3f} ms",
            370,
            panel_y + 125,
            small_font
        )

    else:

        draw_text(
            "STATUS: READY",
            15,
            panel_y + 76,
            font,
            SECONDARY_TEXT
        )


# ============================================================
# RUN A*
# ============================================================

def route_pcb():

    global path
    global visited
    global routing_time

    print()
    print("======================================")
    print("        TRACEFORGE A* ROUTER")
    print("======================================")

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

        path_length = len(path) - 1

        turns = count_turns(path)

        print("Status          : SUCCESS")

        print(
            f"Path length     : {path_length} cells"
        )

        print(
            f"Turns           : {turns}"
        )

        print(
            f"Nodes explored  : {len(visited)}"
        )

        print(
            f"Routing time    : {routing_time * 1000:.3f} ms"
        )

    else:

        print("Status          : NO ROUTE FOUND")

        print(
            f"Nodes explored  : {len(visited)}"
        )

    print("======================================")


# ============================================================
# HANDLE KEYBOARD
# ============================================================

def handle_key(event):

    global mode

    if event.key == pygame.K_ESCAPE:

        return False

    # --------------------------------------------------------
    # ROUTE
    # --------------------------------------------------------

    if event.key == pygame.K_SPACE:

        route_pcb()

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    elif event.key == pygame.K_r:

        reset_board()

    # --------------------------------------------------------
    # OBSTACLE MODE
    # --------------------------------------------------------

    elif event.key == pygame.K_o:

        mode = "obstacle"

    # --------------------------------------------------------
    # ERASE MODE
    # --------------------------------------------------------

    elif event.key == pygame.K_x:

        mode = "erase"

    # --------------------------------------------------------
    # START MODE
    # --------------------------------------------------------

    elif event.key == pygame.K_s:

        mode = "start"

    # --------------------------------------------------------
    # END MODE
    # --------------------------------------------------------

    elif event.key == pygame.K_e:

        mode = "end"

    return True


# ============================================================
# MAIN LOOP
# ============================================================

def main():

    global mouse_down

    reset_board()

    running = True

    while running:

        # ====================================================
        # EVENTS
        # ====================================================

        for event in pygame.event.get():

            # ------------------------------------------------
            # WINDOW CLOSE
            # ------------------------------------------------

            if event.type == pygame.QUIT:

                running = False

            # ------------------------------------------------
            # KEYBOARD
            # ------------------------------------------------

            elif event.type == pygame.KEYDOWN:

                running = handle_key(event)

            # ------------------------------------------------
            # MOUSE DOWN
            # ------------------------------------------------

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    mouse_down = True

                    cell = mouse_to_grid(
                        event.pos
                    )

                    edit_cell(cell)

                elif event.button == 3:

                    # Right click = erase

                    cell = mouse_to_grid(
                        event.pos
                    )

                    if cell:

                        x, y = cell

                        grid[y][x] = 0

                        clear_route()

            # ------------------------------------------------
            # MOUSE UP
            # ------------------------------------------------

            elif event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1:

                    mouse_down = False

        # ====================================================
        # MOUSE DRAG
        # ====================================================

        if mouse_down:

            mouse_buttons = pygame.mouse.get_pressed()

            mouse_position = pygame.mouse.get_pos()

            cell = mouse_to_grid(
                mouse_position
            )

            # Left button held

            if mouse_buttons[0]:

                edit_cell(cell)

            # Right button held

            elif mouse_buttons[2]:

                if cell:

                    x, y = cell

                    grid[y][x] = 0

                    clear_route()

        # ====================================================
        # DRAW
        # ====================================================

        screen.fill(
            BACKGROUND
        )

        draw_board()

        draw_visited()

        draw_path()

        draw_pads()

        draw_panel()

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()