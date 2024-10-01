import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up window
window_size = 512  # 512x512 window for a 128x128 grid (4x scaling)
grid_size = 128
cell_size = window_size // grid_size
screen = pygame.display.set_mode((window_size, window_size), pygame.SRCALPHA)
pygame.display.set_caption("Simple Pixel Drawer")

# Colors
WHITE = (255, 255, 255)
colors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128),
    "cyan": (0, 255, 255),
    "orange": (255, 165, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
}

selected_color = WHITE  # Default drawing color
line_thickness = 2  # Default thickness for drawing
eraser_mode = False  # Eraser mode toggle
fill_mode = False  # Fill mode toggle

# Grid setup (transparent canvas)
TRANSPARENT = (0, 0, 0, 0)  # Fully transparent color
canvas = [[TRANSPARENT for _ in range(grid_size)] for _ in range(grid_size)]

# Function to draw the grid and pixels
def draw_grid():
    for row in range(grid_size):
        for col in range(grid_size):
            pygame.draw.rect(screen, canvas[row][col], (col * cell_size, row * cell_size, cell_size, cell_size))

# Function to save the drawing to a PNG file
def save_drawing_png():
    drawing_surface = pygame.Surface((grid_size, grid_size), pygame.SRCALPHA)
    for row in range(grid_size):
        for col in range(grid_size):
            drawing_surface.set_at((col, row), canvas[row][col])
    pygame.image.save(drawing_surface, "drawing.png")
    print("Drawing saved as 'drawing.png' with a transparent background!")

# Function to save the drawing to an SVG file
def save_drawing_svg():
    with open("drawing.svg", "w") as svg_file:
        svg_file.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{grid_size}" height="{grid_size}">\n')
        for row in range(grid_size):
            for col in range(grid_size):
                color = canvas[row][col]
                if color != TRANSPARENT:
                    hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                    svg_file.write(f'<rect x="{col}" y="{row}" width="1" height="1" fill="{hex_color}" />\n')
        svg_file.write('</svg>\n')
    print("Drawing saved as 'drawing.svg'!")

# Function to fill cells on the grid based on the line drawn
def fill_line_on_grid(start_pos, end_pos, color, thickness):
    start_x, start_y = start_pos[0] // cell_size, start_pos[1] // cell_size
    end_x, end_y = end_pos[0] // cell_size, end_pos[1] // cell_size
    pygame.draw.line(screen, color, start_pos, end_pos, thickness)
    
    # Drawing lines in between grid cells to account for thickness
    for i in range(thickness):
        for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
            for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
                if 0 <= x < grid_size and 0 <= y < grid_size:
                    canvas[y][x] = color

# Flood fill algorithm
def flood_fill(x, y, target_color, replacement_color):
    if target_color == replacement_color:
        return

    # If the clicked pixel is already the target color, we don't need to fill
    if canvas[y][x] != target_color:
        return

    # BFS or DFS flood fill algorithm using a queue (BFS for simplicity)
    queue = [(x, y)]
    while queue:
        cx, cy = queue.pop()

        if canvas[cy][cx] == target_color:
            canvas[cy][cx] = replacement_color

            # Add neighbors (up, down, left, right) if they are within bounds
            if cx > 0: queue.append((cx - 1, cy))  # Left
            if cx < grid_size - 1: queue.append((cx + 1, cy))  # Right
            if cy > 0: queue.append((cx, cy - 1))  # Up
            if cy < grid_size - 1: queue.append((cx, cy + 1))  # Down

# Main loop
running = True
drawing = False
last_pos = None

while running:
    screen.fill(TRANSPARENT)  # Fill with transparency
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Change color
            if event.key == pygame.K_1:
                selected_color = colors["red"]
            elif event.key == pygame.K_2:
                selected_color = colors["green"]
            elif event.key == pygame.K_3:
                selected_color = colors["blue"]
            elif event.key == pygame.K_4:
                selected_color = colors["yellow"]
            elif event.key == pygame.K_5:
                selected_color = colors["purple"]
            elif event.key == pygame.K_6:
                selected_color = colors["cyan"]
            elif event.key == pygame.K_7:
                selected_color = colors["orange"]
            elif event.key == pygame.K_8:
                selected_color = colors["white"]
            elif event.key == pygame.K_0:
                selected_color = colors["black"]
            # Toggle eraser mode
            elif event.key == pygame.K_e:
                eraser_mode = not eraser_mode
                print("Eraser mode:", "On" if eraser_mode else "Off")
            # Toggle fill mode
            elif event.key == pygame.K_f:
                fill_mode = not fill_mode
                print("Fill mode:", "On" if fill_mode else "Off")
            # Save as PNG
            elif event.key == pygame.K_s:
                save_drawing_png()
            # Save as SVG
            elif event.key == pygame.K_v:
                save_drawing_svg()
            # Change line thickness
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                line_thickness += 1
                print(f"Line thickness: {line_thickness}")
            elif event.key == pygame.K_MINUS and line_thickness > 1:
                line_thickness -= 1
                print(f"Line thickness: {line_thickness}")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if fill_mode:
                # Get the clicked pixel position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = mouse_x // cell_size
                grid_y = mouse_y // cell_size
                target_color = canvas[grid_y][grid_x]
                flood_fill(grid_x, grid_y, target_color, selected_color)
            else:
                drawing = True
                last_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.MOUSEMOTION and drawing:
            current_pos = pygame.mouse.get_pos()
            if eraser_mode:
                fill_line_on_grid(last_pos, current_pos, TRANSPARENT, line_thickness)
            else:
                fill_line_on_grid(last_pos, current_pos, selected_color, line_thickness)
            last_pos = current_pos  # Update last position to current

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
