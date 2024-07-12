import pygame
import time
import mindrove
from mindrove.data_filter import DataFilter, FilterTypes, AggOperations
from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds, MindRoveError

# Initialyze EMG armband 
board_shim = None
try:
    BoardShim.enable_dev_board_logger()
    params = MindRoveInputParams()
    board_id = BoardIds.MINDROVE_WIFI_BOARD.value
    board_shim = BoardShim(board_id, params)
    board_shim.prepare_session()
    board_shim.start_stream(450000)

    sampling_rate = board_shim.get_sampling_rate(board_id)
    counter_idx = board_shim.get_package_num_channel(board_id)
    trigger_idx = board_shim.get_other_channels(board_id)[0]
    n_package = 0
    print("Device ready")
except MindRoveError:
    print(MindRoveError)



# Colors for plotting
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Screen size and data point limit
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAX_DATA_POINTS = 1000  # Adjust this value to control the graph width

# Initialize Pygame
pygame.init()

# Check if there's a joystick connected
if not pygame.joystick.get_count():
    print("Error: No joystick detected.")
    quit()

# Get the first joystick (modify the index for other connected controllers)
joystick = pygame.joystick.Joystick(0)

# Get the name of the joystick
joystick_name = joystick.get_name()
print(f"Connected joystick: {joystick_name}")



# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(f"Joystick Signals ({joystick_name})")

# Font for labels and values
font = pygame.font.SysFont(None, 14)

# Define signal labels and colors
signal_labels = ["X-Axis", "Y-Axis", "Button 1", "Button 2"]
signal_colors = [RED, GREEN, BLUE, YELLOW]

# Initialize lists to store data points for each signal
signals = [[], [], [], []]


margin = 20
old_x = margin
old_y = margin
# Main loop
running = True
clock = pygame.time.Clock()  # Used for recording time
while running:
    for event in pygame.event.get():
        # Quit on window close event
        if event.type == pygame.QUIT:
            running = False

    # Read joystick values
    x_axis = joystick.get_axis(0)  # Left thumbstick horizontal (-1 to 1)
    y_axis = joystick.get_axis(1)  # Left thumbstick vertical (-1 to 1)
    button_1_pressed = joystick.get_button(0)
    button_2_pressed = joystick.get_button(1)

    # Update signal data points
    signals[0].append(x_axis)
    signals[1].append(-y_axis)
    signals[2].append(button_1_pressed)
    signals[3].append(button_2_pressed)

    # Limit the number of data points for each signal
    for i in range(len(signals)):
        if len(signals[i]) > MAX_DATA_POINTS:
            signals[i].pop(0)

    # Clear the screen
    screen.fill(BLACK)

    # Draw the layout
    
    
    plot_width = (SCREEN_WIDTH - 2 * margin) // 1
    plot_height = (SCREEN_HEIGHT - margin - font.get_linesize()) // 4

    for i in range(4):
        # Draw subplot frames and labels
        x = margin #+ (plot_width)
        y = margin +((i)*(plot_height))
        pygame.draw.rect(screen, WHITE, (x, y, plot_width, plot_height), 1)
        label_text = font.render(signal_labels[i], True, WHITE)
        screen.blit(label_text, (x + 5, y + 5))
        #label_text = font.render(signal_labels[i], True, WHITE)
        #screen.blit(label_text, (x + 5, y + plot_height - label_text.get_height() - 5))

    # Draw data plots for each signal
    for i, signal in enumerate(signals):
        x = margin #+  (plot_width)
        y = margin + (i) * (plot_height) 
        old_x=x
        old_y=y+ (plot_height//2)
        for j, data_point in enumerate(signal):
            scaled_x = int(j * (plot_width - 2) / (MAX_DATA_POINTS - 1) + x + 1)
            scaled_y = int(-data_point * (plot_height - 2) / 2 + y + plot_height // 2)
            pygame.draw.line(screen, signal_colors[i], (old_x, old_y),(scaled_x, scaled_y), 1)
            old_x=scaled_x
            old_y=scaled_y
        

    # Update the display
    pygame.display.flip()

    # Limit loop framerate (optional)
    clock.tick(500)  # Update at most 60 times per second

# Quit Pygame
pygame.quit()
