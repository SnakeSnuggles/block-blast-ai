def ai_play(game):
    if len(game.current_blocks) == 0:
        return
    temp_board = {k: v.state for k, v in game.board.items()}

    best_score = -float("inf")
    best_move = None
    best_piece = None

    empty_spots = [pos for pos in game.board if not game.board[pos].state]

    for piece_index, piece in enumerate(game.current_blocks):
        for pos in empty_spots:  # Only check empty spaces
            if is_valid_move(game, piece, pos):
                score = simulate_move(temp_board, game, piece, pos)
                if score > best_score:
                    best_score = score
                    best_move = pos
                    best_piece = piece_index

    if best_move:
        game.check_blocks_eh(game.current_blocks[best_piece], best_move)
        game.current_blocks.pop(best_piece)
        if len(game.current_blocks) <= 0:
            game.give_blocks()


def is_valid_move(game, block, pos):
    lines = block.split("o")
    x, y = pos
    for line_index, line in enumerate(lines):
        for char_index, char in enumerate(line):
            if (x + char_index, y + line_index) not in game.board:
                return False
            if game.board[(x + char_index, y + line_index)].state:
                return False
    return True

def simulate_move(board, game, block, pos):
    """Simulate placing a block and score the move."""

    lines = block.split("o")
    for line_index, line in enumerate(lines):
        for char_index, char in enumerate(line):
            board[(pos[0] + char_index, pos[1] + line_index)] = True

    temp_score = fake_clear_rows_and_columns(game, board)
    return temp_score

def fake_clear_rows_and_columns(game, temp_board):
    """Simulate the row and column clearing without modifying the real board."""
    rows_to_clear = [row for row in range(game.size) if sum(temp_board[(row, block)] for block in range(game.size)) >= game.size]
    cols_to_clear = [col for col in range(game.size) if sum(temp_board[(block, col)] for block in range(game.size)) >= game.size]
    return len(rows_to_clear) * game.size + len(cols_to_clear) * game.size
