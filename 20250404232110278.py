import random
import tkinter as tk
from tkinter import messagebox
# Removed PIL import

# --- Image related code removed ---

def roll_die():
    """Simulates rolling a single six-sided die."""
    return random.randint(1, 6)

# --- Global Game State ---
current_player = 1
player_scores = {1: 0, 2: 0} # Direct cumulative score
player_rolls = {1: [], 2: []} # Store individual rolls for history
player_stopped = {1: False, 2: False} # Tracks if player chose to stop
game_over = False
current_round = 1 # Add round counter

# --- GUI Elements ---
window = None
lbl_player_turn = None
lbl_round = None # Label for round number
# lbl_current_sum is removed as score is cumulative per player now
lbl_p1_score = None
lbl_p2_score = None
txt_p1_history = None # Text widget for P1 roll history
txt_p2_history = None # Text widget for P2 roll history
lbl_dice_display = None # Label to show dice image or number
# Separate buttons for each player
btn_p1_roll = None
btn_p1_stop = None
btn_p2_roll = None
btn_p2_stop = None
btn_new_game = None

def update_display():
    """Updates all the labels and button states in the GUI."""
    lbl_round.config(text=f"第 {current_round} 轮") # Update round display
    if game_over:
         lbl_player_turn.config(text="游戏结束!")
    else:
         lbl_player_turn.config(text=f"玩家 {current_player} 回合")
    # lbl_current_sum is removed

    # Display scores directly
    lbl_p1_score.config(text=f"玩家 1 总分: {player_scores[1]}") # Clarify 'Total Score'
    lbl_p2_score.config(text=f"玩家 2 总分: {player_scores[2]}") # Clarify 'Total Score'

    # Update history displays (though primarily updated on roll/reset)
    # This ensures they are cleared/updated correctly on game state changes if needed
    update_history_display(1)
    update_history_display(2)


    if game_over:
        btn_p1_roll.config(state=tk.DISABLED) # Disable all game buttons on game over
        btn_p1_stop.config(state=tk.DISABLED)
        btn_p2_roll.config(state=tk.DISABLED)
        btn_p2_stop.config(state=tk.DISABLED)
        btn_new_game.config(state=tk.NORMAL) # Enable New Game button
    else:
        btn_new_game.config(state=tk.DISABLED) # Disable New Game button during play

        # Player 1 buttons state
        if current_player == 1 and not player_stopped[1]:
            btn_p1_roll.config(state=tk.NORMAL)
            # Can always stop, even with 0 score in this version
            btn_p1_stop.config(state=tk.NORMAL)
        else:
            btn_p1_roll.config(state=tk.DISABLED)
            btn_p1_stop.config(state=tk.DISABLED)

        # Player 2 buttons state
        if current_player == 2 and not player_stopped[2]:
            btn_p2_roll.config(state=tk.NORMAL)
            btn_p2_stop.config(state=tk.NORMAL)
        else:
            btn_p2_roll.config(state=tk.DISABLED)
            btn_p2_stop.config(state=tk.DISABLED)


def display_dice(roll_value):
    """Updates the dice display label with the rolled number."""
    # Only display text
    lbl_dice_display.config(image="", text=str(roll_value), font=("Arial", 30))

def update_history_display(player_num):
    """Updates the text widget for the specified player's roll history."""
    history_widget = txt_p1_history if player_num == 1 else txt_p2_history
    history_widget.config(state=tk.NORMAL) # Enable writing
    history_widget.delete('1.0', tk.END) # Clear existing content
    history_text = " ".join(map(str, player_rolls[player_num]))
    history_widget.insert(tk.END, history_text)
    history_widget.config(state=tk.DISABLED) # Disable editing


def switch_player_and_check_end():
    """Switches player, skips stopped players, and checks for game end."""
    global current_player, game_over, current_round

    # Check for game end condition first
    if player_stopped[1] and player_stopped[2]:
        end_game()
        return

    # Switch player
    prev_player = current_player
    current_player = 3 - current_player
    # Increment round if switching back to player 1
    if prev_player == 2 and current_player == 1:
        current_round += 1

    # If the new player has already stopped, switch back/check end again
    if player_stopped[current_player]:
         # Check again if the *other* player also stopped in the meantime
         if player_stopped[1] and player_stopped[2]:
              end_game()
              return
         else:
              # The other player hasn't stopped, switch back to them
              current_player = 3 - current_player

    # If after checks, both are stopped, end game
    if player_stopped[1] and player_stopped[2]:
         end_game()
    else:
         update_display() # Update GUI for the active player


def roll_action():
    """Handles the Roll button click for the current player."""
    global game_over
    player = current_player # Capture current player before potential switch
    if game_over or player_stopped[player]: return

    roll = roll_die()
    display_dice(roll)
    player_rolls[player].append(roll) # Add roll to history list
    update_history_display(player) # Update the history display
    new_sum = player_scores[player] + roll

    if new_sum > 10:
        messagebox.showinfo("爆了!", f"玩家 {player} 掷出 {roll}. 总和 {new_sum} > 10. 爆了! 得分为 0.")
        player_scores[player] = 0 # Reset score for bust
        # Keep rolls in history even if busted
        player_stopped[player] = True # Bust forces stop
        switch_player_and_check_end()
    else:
        player_scores[player] = new_sum # Update cumulative score
        # Turn automatically switches after a successful roll
        switch_player_and_check_end()


def stop_action():
    """Handles the Stop button click for the current player."""
    global game_over
    player = current_player # Capture current player
    if game_over or player_stopped[player]: return

    messagebox.showinfo("停止", f"玩家 {player} 停止掷骰子，得分 {player_scores[player]}.")
    player_stopped[player] = True
    switch_player_and_check_end()


def end_game():
    """Determines the winner and updates the display for game over."""
    global game_over
    if game_over: return # Prevent running multiple times if called again

    game_over = True
    p1s = player_scores[1]
    p2s = player_scores[2]

    # Determine winner
    winner_message = ""
    if p1s > p2s:
        winner_message = "玩家 1 获胜!"
    elif p2s > p1s:
        winner_message = "玩家 2 获胜!"
    else:
        winner_message = "平局!"

    messagebox.showinfo("游戏结束", f"最终得分:\n玩家 1: {p1s}\n玩家 2: {p2s}\n\n{winner_message}")

    # Removed duplicate messagebox call
    update_display() # Update display to show final state (disabled buttons, etc.)


def start_new_game():
    """Resets the game state for a new game."""
    global current_player, player_scores, player_rolls, player_stopped, game_over, current_round
    current_player = 1
    player_scores = {1: 0, 2: 0} # Reset scores to 0
    player_rolls = {1: [], 2: []} # Clear roll history lists
    player_stopped = {1: False, 2: False} # Reset stopped status
    current_round = 1 # Reset round counter
    game_over = False
    lbl_dice_display.config(image="", text="") # Clear dice display
    update_display() # Update GUI to initial state (will also clear history displays)


def create_gui():
    """Creates the main game window and widgets."""
    global window, lbl_player_turn, lbl_round, lbl_p1_score, lbl_p2_score, lbl_dice_display
    global txt_p1_history, txt_p2_history # Add history text widgets
    global btn_p1_roll, btn_p1_stop, btn_p2_roll, btn_p2_stop, btn_new_game

    window = tk.Tk()
    # Removed load_dice_images() call

    window.title("掷骰子游戏") # Translated title
    # Remove fixed geometry, let it size naturally or be resized
    # window.geometry("400x470")
    window.resizable(True, True) # Allow resizing

    # --- Copyright Footer Frame (Packed first to reserve space at bottom) ---
    footer_frame = tk.Frame(window)
    footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 2))
    footer_label = tk.Label(footer_frame, text="© 刘展均数智实验室 (https://blog.snas.club)", font=("Arial", 8), fg="grey")
    footer_label.pack() # Pack label inside footer frame

    # --- Main content frame (to pack above the footer) ---
    main_frame = tk.Frame(window)
    main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)


    # --- Score and Turn Info --- (Pack inside main_frame)
    info_frame = tk.Frame(main_frame) # Changed parent to main_frame
    info_frame.pack(pady=5)

    lbl_round = tk.Label(info_frame, text="第 1 轮", font=("Arial", 12)) # Add round label
    lbl_round.pack()

    lbl_player_turn = tk.Label(info_frame, text="玩家 1 回合", font=("Arial", 14))
    lbl_player_turn.pack()

    # lbl_current_sum removed

    score_frame = tk.Frame(main_frame) # Changed parent to main_frame
    score_frame.pack(pady=5)

    lbl_p1_score = tk.Label(score_frame, text="玩家 1 总分: 0", font=("Arial", 12), width=15, anchor="w")
    lbl_p1_score.pack(side=tk.LEFT, padx=10)

    lbl_p2_score = tk.Label(score_frame, text="玩家 2 总分: 0", font=("Arial", 12), width=15, anchor="w")
    lbl_p2_score.pack(side=tk.LEFT, padx=10)

    # --- History Display --- (Pack inside main_frame)
    history_frame = tk.Frame(main_frame) # Changed parent to main_frame
    history_frame.pack(pady=5, fill=tk.X, padx=10)

    tk.Label(history_frame, text="玩家 1 掷骰记录:", font=("Arial", 10)).pack(anchor="w")
    txt_p1_history = tk.Text(history_frame, height=2, width=40, state=tk.DISABLED, font=("Arial", 10), wrap=tk.WORD)
    txt_p1_history.pack(fill=tk.X)

    tk.Label(history_frame, text="玩家 2 掷骰记录:", font=("Arial", 10)).pack(anchor="w", pady=(5,0))
    txt_p2_history = tk.Text(history_frame, height=2, width=40, state=tk.DISABLED, font=("Arial", 10), wrap=tk.WORD)
    txt_p2_history.pack(fill=tk.X)


    # --- Dice Display --- (Pack inside main_frame)
    lbl_dice_display = tk.Label(main_frame, text="", font=("Arial", 30), width=4, height=2, relief="groove") # Changed parent
    lbl_dice_display.pack(pady=10)

    # --- Player 1 Buttons --- (Pack inside main_frame)
    p1_button_frame = tk.Frame(main_frame) # Changed parent
    p1_button_frame.pack(pady=2)
    tk.Label(p1_button_frame, text="玩家 1:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    btn_p1_roll = tk.Button(p1_button_frame, text="掷骰子", command=roll_action, width=8, height=1) # Roll
    btn_p1_roll.pack(side=tk.LEFT, padx=5)
    btn_p1_stop = tk.Button(p1_button_frame, text="停止", command=stop_action, width=8, height=1) # Stop
    btn_p1_stop.pack(side=tk.LEFT, padx=5)

    # --- Player 2 Buttons --- (Pack inside main_frame)
    p2_button_frame = tk.Frame(main_frame) # Changed parent
    p2_button_frame.pack(pady=2)
    tk.Label(p2_button_frame, text="玩家 2:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    btn_p2_roll = tk.Button(p2_button_frame, text="掷骰子", command=roll_action, width=8, height=1) # Roll
    btn_p2_roll.pack(side=tk.LEFT, padx=5)
    btn_p2_stop = tk.Button(p2_button_frame, text="停止", command=stop_action, width=8, height=1) # Stop
    btn_p2_stop.pack(side=tk.LEFT, padx=5)


    # --- New Game Button --- (Pack inside main_frame, adjust padding)
    btn_new_game = tk.Button(main_frame, text="新游戏", command=start_new_game, width=15, font=("Arial", 10)) # Added font size for consistency
    btn_new_game.pack(pady=10) # Increased vertical padding


    start_new_game() # Initialize game state
    window.mainloop()


if __name__ == "__main__":
    create_gui()
