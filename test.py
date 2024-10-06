from explainer import Analysis

src='''def BFS(board: chess.Board, goal_position: chess.Square):
    """
    This function implements the breath first search algorithm
    
    Parameters:
    - board: the chess board that the knight is moving upon
    
    Returns:
    A list containing the visited tile values in the order they were visited with starting tile
    always being the first tile and the goal tile always being the last tile
    """
    visited_nodes_in_order = []

    # YOUR CODE HERE
    seen_nodes = set()
    seen_nodes.add(chess.A1)
    queue = []
    queue.append(chess.A1)

    while queue:
        curr_pos = queue.pop(0)
        visited_nodes_in_order.append(curr_pos)
        
        board.set_piece_at(curr_pos, chess.Piece(chess.KNIGHT, chess.WHITE))
        # print("*****")  
        # print(board)
        if goal_reached(board, goal_position):
            break

        legal_moves = [move.to_square for move in board.legal_moves]
        
        for move in legal_moves:
            if move not in seen_nodes:
                seen_nodes.add(move)
                queue.append(move)

        board.remove_piece_at(curr_pos)
        # print(queue)
    return visited_nodes_in_order'''
explainer = Analysis() 
feedback = explainer.get_feedback('bfs', src)
print(feedback)