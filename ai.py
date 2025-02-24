def ai_play(game):
    if not game.current_blocks:
        return
    
    temp_board = {k: v.state for k, v in game.board.items()}

    best_score = -float("inf")
    best_move = None
    best_piece = None

    empty_spots = [pos for pos in game.board if not game.board[pos].state]

    for piece_index, piece in enumerate(game.current_blocks):
        for pos in empty_spots:
            if game.is_valid_move(piece, pos):
                temp_board_copy = temp_board.copy()  # Ensure fresh board for each move
                score, _ = simulate_move(temp_board_copy, game, piece, pos)
                edging_score = get_edge_priority(game, pos, piece, game.size)
                hole_penalty = calculate_hole_penalty(temp_board_copy)
                final_score = score + edging_score - hole_penalty

                if final_score > best_score:
                    best_score = final_score
                    best_move = pos
                    best_piece = piece_index

                    print("edge score:", edging_score)
                    print("hole no no:", hole_penalty)
                    print("score:", score)
                    print("final_score:", final_score)

    # If no move was found, just pick any valid one
    if best_move is None:
        for piece_index, piece in enumerate(game.current_blocks):
            for pos in empty_spots:
                if game.is_valid_move(piece, pos):
                    best_move = pos
                    best_piece = piece_index
                    break
            if best_move:
                break

    # Make the best move
    if best_move:
        game.check_blocks_eh(game.current_blocks[best_piece], best_move)

    # If no blocks are left, get new ones
    if not game.current_blocks:
        game.give_blocks()
def get_edge_priority(game, pos, block, board_size):
    x, y = pos
    posses = game.parser_for_blocks(block,pos)
    blocks_on_edge = 0

    for x,y in posses:
        relitive_x = pos[0]
        relitive_y = pos[1]
        x += relitive_x 
        y += relitive_y 
        if x == 0 or x == board_size:
            blocks_on_edge += 1
        if y == 0 or y == board_size:
            blocks_on_edge += 1
    return blocks_on_edge 
def calculate_hole_penalty(board):
    penalty = 0
    surroundings = [(0,1), (1,0), (0,-1), (-1,0)]

    for x, y in board:
        if not board[(x, y)]:  # If the space is empty
            surrounding_filled = sum(
                1 for dx, dy in surroundings 
                if (x + dx, y + dy) not in board or board.get((x + dx, y + dy), False)
            )

            if surrounding_filled >= 3:  # Change to 3 if 2 was unintentional
                penalty += 1
                
    return penalty
def simulate_move(board, game, block, pos):
    temp_board = board.copy()  # Always start with a fresh copy

    poses = game.parser_for_blocks(block, pos)
    for piece_pos in poses:
        x, y = piece_pos
        temp_board[(pos[0] + x, pos[1] + y)] = True  # Place block on temp board

    temp_score = fake_clear_rows_and_columns(game, temp_board)
    return temp_score, temp_board

def fake_clear_rows_and_columns(game, temp_board):
    size = game.size

    rows_to_clear = [row for row in range(size) if sum(temp_board.get((row, col), False) for col in range(size)) >= size]
    cols_to_clear = [col for col in range(size) if sum(temp_board.get((row, col), False) for row in range(size)) >= size]

    return len(rows_to_clear) * size + len(cols_to_clear) * size
