class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'

    # -------------------------
    # Display Board
    # -------------------------
    def print_board(self):
        for i in range(0, 9, 3):
            print(" | ".join(self.board[i:i+3]))
            if i < 6:
                print("---------")

    # -------------------------
    # Check Winner
    # -------------------------
    def is_winner(self, player):
        # rows
        for i in range(0, 9, 3):
            if all(self.board[i+j] == player for j in range(3)):
                return True

        # columns
        for i in range(3):
            if all(self.board[i+3*j] == player for j in range(3)):
                return True

        # diagonals
        if all(self.board[i] == player for i in [0, 4, 8]):
            return True
        if all(self.board[i] == player for i in [2, 4, 6]):
            return True

        return False

    # -------------------------
    # Check Board Status
    # -------------------------
    def is_full(self):
        return ' ' not in self.board

    def is_game_over(self):
        return self.is_winner('X') or self.is_winner('O') or self.is_full()

    def get_available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    # -------------------------
    # Move Handling
    # -------------------------
    def make_move(self, move):
        self.board[move] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def undo_move(self, move):
        self.board[move] = ' '
        self.current_player = 'O' if self.current_player == 'X' else 'X'


# =================================
# Minimax Algorithm
# =================================
def minimax(board, maximizing):
    if board.is_winner('X'):
        return -1
    if board.is_winner('O'):
        return 1
    if board.is_full():
        return 0

    if maximizing:
        max_eval = float('-inf')
        for move in board.get_available_moves():
            board.make_move(move)
            eval_score = minimax(board, False)
            board.undo_move(move)
            max_eval = max(max_eval, eval_score)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.get_available_moves():
            board.make_move(move)
            eval_score = minimax(board, True)
            board.undo_move(move)
            min_eval = min(min_eval, eval_score)
        return min_eval


# =================================
# Find Best AI Move
# =================================
def get_best_move(board):
    best_move = None
    best_eval = float('-inf')

    for move in board.get_available_moves():
        board.make_move(move)
        eval_score = minimax(board, False)
        board.undo_move(move)

        if eval_score > best_eval:
            best_eval = eval_score
            best_move = move

    return best_move


# =================================
# Play the Game
# =================================
def play_game():
    game = TicTacToe()

    while not game.is_game_over():
        game.print_board()

        if game.current_player == 'X':
            try:
                move = int(input("Enter your move (0-8): "))
            except ValueError:
                print("Invalid input! Enter a number.")
                continue

            if move not in game.get_available_moves():
                print("Invalid move! Try again.")
                continue

            game.make_move(move)

        else:
            print("\nAI (O) is thinking...")
            move = get_best_move(game)
            print(f"AI plays: {move}")
            game.make_move(move)

    # Final board
    game.print_board()

    if game.is_winner('X'):
        print("You win!")
    elif game.is_winner('O'):
        print("AI wins!")
    else:
        print("It's a draw!")


# Run the game
if __name__ == "__main__":
    play_game()