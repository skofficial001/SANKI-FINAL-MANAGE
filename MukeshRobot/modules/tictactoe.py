import random
from telegram import Update
from telegram.ext import CallbackContext
from MukeshRobot import pbot as mukesh

# Define the Tic-Tac-Toe class
class TicTacToe:
    def __init__(self):
        self.board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.current_player = "X"

    def display_board(self):
        board_str = "\n".join([
            " ".join(self.board[i:i + 3]) for i in range(0, 9, 3)
        ])
        return f"```\n{board_str}\n```"

    def make_move(self, position):
        if self.board[position - 1] == str(position):
            self.board[position - 1] = self.current_player
            return True
        return False

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for combo in winning_combinations:
            if (
                self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]
                and self.board[combo[0]] != str(combo[0] + 1)
            ):
                return True
        return False

    def is_board_full(self):
        return all(cell == "X" or cell == "O" for cell in self.board)


# Define a dictionary to keep track of games in different chats
tic_tac_toe_games = {}


# Command handler for starting a new Tic-Tac-Toe game
def start_tic_tac_toe(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in tic_tac_toe_games:
        tic_tac_toe_games[chat_id] = TicTacToe()
        update.message.reply_text(
            "Tic-Tac-Toe game started!\n" + tic_tac_toe_games[chat_id].display_board()
        )
    else:
        update.message.reply_text("A game is already in progress. Finish it before starting a new one.")


# Command handler for making a move in Tic-Tac-Toe
def make_move(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id in tic_tac_toe_games:
        game = tic_tac_toe_games[chat_id]
        player = update.message.from_user.username

        if player == game.current_player:
            try:
                move = int(context.args[0])
                if 1 <= move <= 9:
                    if game.make_move(move):
                        update.message.reply_text(game.display_board())
                        if game.check_winner():
                            update.message.reply_text(f"{player} wins! Game over.")
                            del tic_tac_toe_games[chat_id]
                        elif game.is_board_full():
                            update.message.reply_text("It's a tie! Game over.")
                            del tic_tac_toe_games[chat_id]
                        else:
                            game.switch_player()
                    else:
                        update.message.reply_text("Invalid move. Try again.")
                else:
                    update.message.reply_text("Invalid move. Please choose a number between 1 and 9.")
            except (ValueError, IndexError):
                update.message.reply_text("Invalid input. Please provide a number between 1 and 9.")
        else:
            update.message.reply_text("It's not your turn. Wait for the other player.")
    else:
        update.message.reply_text("No Tic-Tac-Toe game in progress. Start a new game with /start_tic_tac_toe.")


# Add command handlers to the dispatcher
dispatcher.add_handler(CommandHandler("start_tic_tac_toe", start_tic_tac_toe))
dispatcher.add_handler(CommandHandler("make_move", make_move, pass_args=True))

# You can add more features or customize the code as needed.
