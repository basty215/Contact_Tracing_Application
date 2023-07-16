import random
import tkinter as tk

# Player class
class Player:
    def __init__(self, name, color):
        self.name = name
        self.row = 0
        self.column = 0
        self.score = 0
        self.movements = []
        self.color = color

# Function to handle a player's turn
def play_turn(player, direction):
    old_row, old_column = player.row, player.column
    move_player(player, direction)
    if player.row == old_row and player.column == old_column:
        print(f"{player.name} did not move.")
    else:
        player.movements.append((player.row, player.column))  # Track the movement
        print(f"{player.name} moved to position ({player.row}, {player.column})")
        check_player_contact(player)
        update_gui(player)

# Function to move the player in the specified direction
def move_player(player, direction):
    new_row, new_column = player.row, player.column
    if direction == "up":
        new_row -= 1
    elif direction == "down":
        new_row += 1
    elif direction == "left":
        new_column -= 1
    elif direction == "right":
        new_column += 1

    # Check if the new position is within the board boundaries
    if is_valid_move(new_row, new_column):
        player.row = new_row
        player.column = new_column

# Function to check if the move is valid within the board boundaries
def is_valid_move(row, column):
    return 0 <= row < board_rows and 0 <= column < board_columns

# Function to check if a player has been in contact with another player
def check_player_contact(player):
    for other_player in players:
        if other_player != player and other_player.row == player.row and other_player.column == player.column:
            print(f"Alert! {player.name} has been in contact with {other_player.name}!")
            # Perform any desired actions when players come in contact

# Function to update GUI with player positions
def update_gui(player):
    canvas.delete(player.name)
    row, column = player.row, player.column
    x1 = column * 50 + 5
    y1 = row * 50 + 5
    x2 = (column + 1) * 50 - 5
    y2 = (row + 1) * 50 - 5
    canvas.create_oval(x1, y1, x2, y2, fill=player.color, tags=(player.name, "player"))

# Function to handle GUI button click
def handle_click(player, direction):
    global turn
    if player == players[turn]:
        play_turn(player, direction)
        if player.row == board_rows - 1 and player.column == board_columns - 1:
            print(f"{player.name} wins!")
            print(f"{player.name}'s movements: {player.movements}")
            window.destroy()
        else:

            turn = (turn + 1) % len(players)
            update_button_visibility()

# Function to update button visibility based on the current turn
def update_button_visibility():
    for i, button_frame in enumerate(button_frames):
        if i == turn:
            button_frame.pack()
        else:
            button_frame.pack_forget()

# Get the size of the board
board_rows = int(input("Enter the number of rows for the board: "))
board_columns = int(input("Enter the number of columns for the board: "))

# Create players
players = []
num_players = int(input("Enter the number of players: "))
colors = ["red", "blue", "green", "orange", "purple", "yellow"]  # Define color options
for i in range(num_players):
    name = input(f"Enter name for Player {i+1}: ")
    color = colors[i % len(colors)]  # Assign colors cyclically
    players.append(Player(name, color))

# GUI setup
window = tk.Tk()
window.title("Board Game")

canvas = tk.Canvas(window, width=board_columns * 50, height=board_rows * 50)
canvas.pack()

# Create board cells
for row in range(board_rows):
    for column in range(board_columns):
        x1 = column * 50
        y1 = row * 50
        x2 = (column + 1) * 50
        y2 = (row + 1) * 50
        canvas.create_rectangle(x1, y1, x2, y2, fill="white")

# Set initial player positions on the GUI
for player in players:
    update_gui(player)

# Create button frames for each player
button_frames = []
for player in players:
    frame = tk.Frame(window)
    button_frames.append(frame)

# Button setup
turn = 0
directions = ["up", "down", "left", "right"]
for direction in directions:
    for i, player in enumerate(players):
        button_frame = button_frames[i]
        button = tk.Button(button_frame, text=f"{player.name} {direction.title()}", command=lambda p=player, d=direction: handle_click(p, d))
        button.pack(side="left")

# Initially show buttons for the first player
update_button_visibility()

window.mainloop()
