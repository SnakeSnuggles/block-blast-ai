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
            if game.is_valid_move(piece, pos):
                score = simulate_move(temp_board, game, piece, pos)
                if score > best_score:
                    best_score = score
                    best_move = pos
                    best_piece = piece_index

    if best_move:
        game.check_blocks_eh(game.current_blocks[best_piece], best_move)
        if len(game.current_blocks) <= 0:
            game.give_blocks()

def simulate_move(board, game, block, pos):

    poses = game.parser_for_blocks(block,pos)
    for peice_pos in poses:
        x,y = peice_pos
        board[(pos[0] + x, pos[1] + y)] = True

    temp_score = fake_clear_rows_and_columns(game, board)
    return temp_score

def fake_clear_rows_and_columns(game, temp_board):
    """Simulate the row and column clearing without modifying the real board."""
    rows_to_clear = [row for row in range(game.size) if sum(temp_board[(row, block)] for block in range(game.size)) >= game.size]
    cols_to_clear = [col for col in range(game.size) if sum(temp_board[(block, col)] for block in range(game.size)) >= game.size]
    return len(rows_to_clear) * game.size + len(cols_to_clear) * game.size
