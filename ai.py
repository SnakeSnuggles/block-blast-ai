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
                cluster_bonus = calculate_cluster_bonus(temp_board_copy, game.parser_for_blocks(piece, pos))
                group_reward = get_grouping_bonus(game,pos,piece)
                final_score = score + edging_score + group_reward * 1.5 + hole_penalty + cluster_bonus 

                if final_score > best_score:
                    best_score = final_score
                    best_move = pos
                    best_piece = piece_index


                    print("--------------")
                    print("edge score:", edging_score)
                    print("hole no no:", hole_penalty)
                    print("group reward:", group_reward)
                    print("score:", score)
                    print("vvvvvvvvvvvv")
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
    posses = game.parser_for_blocks(block, pos)
    edge_contact_score = 0

    for x, y in posses:
        if x == 0 or x == board_size - 1:  # Left or right edge
            edge_contact_score += 2  # Favor stronger edge contact
        if y == 0 or y == board_size - 1:  # Top or bottom edge
            edge_contact_score += 2  # Favor stronger edge contact

    return edge_contact_score
def future_move_reward(game, board):
    remaining_moves = 0
    for piece in game.current_blocks:
        for pos in board:
            if not board[pos] and game.is_valid_move(piece, pos):
                remaining_moves += 1
    
    return remaining_moves
def calculate_cluster_bonus(board, piece_positions):
    bonus = 0
    surroundings = [(0,1), (1,0), (0,-1), (-1,0)]

    for x, y in piece_positions:
        adjacent_blocks = sum(
            (x + dx, y + dy) in board and board[x + dx, y + dy]
            for dx, dy in surroundings
        )
        bonus += adjacent_blocks  # More adjacent blocks = higher bonus

    return bonus
def calculate_hole_penalty(board):
    penalty = 0
    surroundings = [(0,1), (1,0), (0,-1), (-1,0)]

    for (x, y), filled in board.items():
        if not filled:  # If the space is empty
            surrounding_filled = sum(
                (x + dx, y + dy) in board and board[x + dx, y + dy]
                for dx, dy in surroundings
            )

            if surrounding_filled == 3:  
                penalty += 1  
            elif surrounding_filled == 4:  
                penalty += 3  # Extra penalty for fully enclosed holes

    return -penalty
def get_grouping_bonus(game, pos, block):
    posses = game.parser_for_blocks(block, pos)
    surroundings = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    grouping_bonus = 0

    for x, y in posses:
        for dx, dy in surroundings:
            neighbor = (x + dx, y + dy)
            if neighbor in game.board and game.board[neighbor].state:  # If touching a filled block
                grouping_bonus += 2  # Give bonus points for clustering

    return grouping_bonus
def simulate_move(board, game, block, pos):
    temp_board = board.copy()  # Always start with a fresh copy

    poses = game.parser_for_blocks(block, pos)
    for piece_pos in poses:
        x, y = piece_pos
        temp_board[(pos[0] + x, pos[1] + y)] = True  # Place block on temp board

    temp_score = fake_clear_rows_and_columns(game, temp_board)
    return temp_score, temp_board

def fake_clear_rows_and_columns(game, temp_board):
    size = game.size - 1

    rows_to_clear = [row for row in range(size) if sum(temp_board.get((row, col), False) for col in range(size)) >= size]
    cols_to_clear = [col for col in range(size) if sum(temp_board.get((row, col), False) for row in range(size)) >= size]

    return (len(rows_to_clear) + len(cols_to_clear)) * size
