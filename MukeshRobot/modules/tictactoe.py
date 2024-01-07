from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
from MukeshRobot import pbot as mukesh

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the Tic-Tac-Toe class
class TicTacToe:
    def __init__(self):
        self.board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.current_player = "X"
        self.winner = None

    def display_board(self):
        board_str = "\n".join([
            " ".join(self.board[i:i + 3]) for i in range(0, 9, 3)
        ])
        return f"```\n{board_str}\n```"

    def make_move(self, position):
        if self.board[position - 1] == str(position) and not self.winner:
            self.board[position - 1] = self.current_player
            if self.check_winner():
                self.winner = self.current_player
            elif all(cell == "X" or cell == "O" for cell in self.board):
                self.winner = "Tie"
            else:
                self.switch_player()
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

# Dictionary to keep track of games in different chats
tic_tac_toe_games = {}

# Command handler for starting a new Tic-Tac-Toe game
def start_tic_tac_toe(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in tic_tac_toe_games:
        tic_tac_toe_games[chat_id] = TicTacToe()
        message = (
            "Tic-Tac-Toe game started!\n" +
            tic_tac_toe_games[chat_id].display_board() +
            f"\n\n{tic_tac_toe_games[chat_id].current_player}'s turn."
        )
        update.message.reply_text(message, reply_markup=create_keyboard())
    else:
        update.message.reply_text("A game is already in progress. Finish it before starting a new one.")

# Command handler for handling player moves
def make_move(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user = update.message.from_user.username
    if chat_id in tic_tac_toe_games and tic_tac_toe_games[chat_id].current_player == user:
        try:
            move = int(update.message.text)
            if 1 <= move <= 9:
                if tic_tac_toe_games[chat_id].make_move(move):
                    message = (
                        tic_tac_toe_games[chat_id].display_board() +
                        f"\n\n{tic_tac_toe_games[chat_id].current_player}'s turn."
                    )
                    update.message.reply_text(message, reply_markup=create_keyboard())
                    if tic_tac_toe_games[chat_id].winner:
                        end_game(update, chat_id)
                else:
                    update.message.reply_text("Invalid move. Try again.")
            else:
                update.message.reply_text("Invalid move. Please choose a number between 1 and 9.")
        except ValueError:
            update.message.reply_text("Invalid input. Please provide a number between 1 and 9.")
    else:
        update.message.reply_text("It's not your turn. Wait for the other player.")

# Inline keyboard handler for handling button clicks
def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    user = query.from_user.username

    if chat_id in tic_tac_toe_games and tic_tac_toe_games[chat_id].current_player == user:
        try:
            move = int(query.data)
            if 1 <= move <= 9:
                if tic_tac_toe_games[chat_id].make_move(move):
                    message = (
                        tic_tac_toe_games[chat_id].display_board() +
                        f"\n\n{tic_tac_toe_games[chat_id].current_player}'s turn."
                    )
                    query.edit_message_text(message, reply_markup=create_keyboard())
                    if tic_tac_toe_games[chat_id].winner:
                        end_game(update, chat_id)
                else:
                    query.answer("Invalid move. Try again.")
            else:
                query.answer("Invalid move. Please choose a number between 1 and 9.")
        except ValueError:
            query.answer("Invalid input. Please provide a number between 1 and 9.")
    else:
        query.answer("It's not your turn. Wait for the other player.")

# Function to create the inline keyboard
def create_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data='1'),
            InlineKeyboardButton("2", callback_data='2'),
            InlineKeyboardButton("3", callback_data='3'),
        ],
        [
            InlineKeyboardButton("4", callback_data='4'),
            InlineKeyboardButton("5", callback_data='5'),
            InlineKeyboardButton("6", callback_data='6'),
        ],
        [
            InlineKeyboardButton("7", callback_data='7'),
            InlineKeyboardButton("8", callback_data='8'),
            InlineKeyboardButton("9", callback_data='9'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

# Function to end the game and display the result
def end_game(update: Update, chat_id: int):
    game = tic_tac_toe_games[chat_id]
    if game.winner == "Tie":
        message = "It's a tie! Game over."
    else:
        message = f"{game.winner} wins! Game over."

    del tic_tac_toe_games[chat_id]
    update.message.reply_text(
        game.display_board() + f"\n\n{message}\n\nUse /start_tic_tac_toe to play again."
    )

# Add command handlers and inline keyboard handler to the dispatcher
dispatcher.add_handler(CommandHandler("start_tic_tac_toe", start_tic_tac_toe))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, make_move))
dispatcher.add_handler(C
