""""This object is built for adding the AI functions for the game."""

import time
from copy import deepcopy
import random
import move_recordings


class AI():

    def __init__(self, max_depth, IDS):
        self.value = 0
        self.time_consumed = 0
        self.max_depth = max_depth
        self.terminal_nodes = 0
        self.table = [[[random.randint(1, 2 ** 64 - 1) for king in range(3)]
                       for gold_piece in range(11)] for silver_piece in range(11)]
        self.IDS = IDS
        self.TT = dict({})
        self.ids_timeout = 5

    def evaluation_function(self, board, gold_move):
        capture = 0
        evaluation = 0
        row_king_location, col_king_location = board.gold_king_location
        if board.king == 0:
            self.value = -129 if gold_move else -139
        evaluation += self.value
        if row_king_location == 0 or row_king_location == 10 or col_king_location == 0 or col_king_location == 10:
            evaluation += 59

        piece_blocked = [0, 0, 0, 0]
        for i in range(11 - col_king_location - 1):
            if board.board[row_king_location][col_king_location + i + 1] != '--':
                piece_blocked[0] += 1
        for i in range(col_king_location):
            if board.board[row_king_location][col_king_location - i - 1] != '--':
                piece_blocked[1] += 1
        for i in range(row_king_location):
            if board.board[row_king_location - i - 1][col_king_location] != '--':
                piece_blocked[2] += 1
        for i in range(11 - row_king_location - 1):
            if board.board[row_king_location + i + 1][col_king_location] != '--':
                piece_blocked[3] += 1
        directions = (
                      (row_king_location - 1, col_king_location - 1), (row_king_location - 1, col_king_location + 1),
                      (row_king_location + 1, col_king_location - 1), (row_king_location + 1, col_king_location + 1)
        )

        for direction in directions:
            if 0 <= direction[0] <= 10 and 0 <= direction[1] <= 10:
                if board.board[direction[0]][direction[1]] == "sp":
                    capture += 1
        if not gold_move:
            if capture > 0:
                evaluation = 199
            elif int(min(piece_blocked)) != 0:
                king_capture = {0: 0, 1: 139, 2: 139, 3: 139, 4: 139}
                evaluation = king_capture[capture]
            else:
                evaluation = -139
        else:
            if int(min(piece_blocked)) == 0:
                evaluation = 139

            elif capture == 0:
                king_go_to_board = {0: 139, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
                evaluation = king_go_to_board[int(min(piece_blocked))]
            else:
                evaluation = -139
        evaluation += 11 * board.gold_piece + 9 * board.king - 7 * board.silver_piece

        return evaluation

    def check_transposition_table(self, hash):
        result = self.TT.get(hash)
        if result is not None:
            return result
        return -1

    def zobrist_hash(self, board):

        board = board.board
        hash = 0
        for r in range(len(board)):
            for c in range(len(board[0])):
                piece = board[r][c]
                if piece != "--":
                    # XOR according to position
                    hash ^= self.table[r][c][move_recordings.piece_index(
                        piece)]
        return hash

    def store(self, hash, cache):
        self.TT[hash] = cache

    def minimax_function_with_alpha_beta(
            self,
            max_depth,
            board,
            game_continue,
            gold_move,
            alpha,
            beta):
        hash = self.zobrist_hash(board)
        alpha_initial, beta_initial = alpha, beta
        self.terminal_nodes += 1
        best_value = float('-inf') if gold_move else float('inf')
        best_move = ""
        moves, captures = board.valid_moves()
        result = self.check_transposition_table(hash)
        if result != -1:
            if result[0] >= max_depth:
                if result[3] == "continue":
                    return result[1], result[2]
                elif result[3] == "high":
                    alpha = max(alpha, result[1])
                elif result[3] == "low":
                    beta = min(beta, result[1])
                if alpha >= beta:
                    return result[1], result[2]
        if max_depth == 0 or not game_continue:
            return self.evaluation_function(board, board.gold_move), ""
        for move in captures:
            moves.append(move)

        for move in moves:
            new_board = move_recordings.update_board(move, board)
            tree_child, action_child = self.minimax_function_with_alpha_beta(
                max_depth - 1, new_board, new_board.game_continue, new_board.gold_move, alpha, beta)
            if gold_move and best_value < tree_child:
                best_value = tree_child
                best_move = move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            elif (not gold_move) and best_value > tree_child:
                best_value = tree_child
                best_move = move
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        if best_value <= alpha_initial:
            flag = "low"
        elif best_value >= beta_initial:
            flag = "high"
        else:
            flag = "continue"

        hash = self.zobrist_hash(board)
        cache = (max_depth, best_value, best_move, flag)
        self.store(hash, cache)
        return best_value, best_move

    def minimax_function_with_alpha_beta_and_ids(
            self,
            max_depth,
            board,
            game_continue,
            gold_move,
            alpha,
            beta):
        start_time = time.time()
        hash = self.zobrist_hash(board)
        alpha_initial, beta_initial = alpha, beta
        self.terminal_nodes += 1
        result = self.check_transposition_table(hash)
        if result != -1:
            if result[0] >= max_depth:
                if result[3] == "continue":
                    return result[1], result[2]
                elif result[3] == "high":
                    alpha = max(alpha, result[1])
                elif result[3] == "low":
                    beta = min(beta, result[1])
                if alpha >= beta:
                    return result[1], result[2]
        if max_depth == 0 or not game_continue or self.ids_timeout < 0:
            return self.evaluation_function(board, board.gold_move), ""

        moves, captures = board.valid_moves()
        for move in captures:
            moves.append(move)

        best_value = float('-inf') if gold_move else float('inf')
        best_move = ""

        for move in moves:
            new_board = move_recordings.update_board(move, board)
            tree_child, action_child = self.minimax_function_with_alpha_beta_and_ids(
                max_depth - 1, new_board, new_board.game_continue, new_board.gold_move, alpha, beta)

            if gold_move and best_value < tree_child:
                best_value = tree_child
                best_move = move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            elif (not gold_move) and best_value > tree_child:
                best_value = tree_child
                best_move = move
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        if best_value <= alpha_initial:
            flag = "low"
        elif best_value >= beta_initial:
            flag = "high"
        else:
            flag = "continue"
        end_time = time.time()
        time_spent = end_time - start_time
        self.ids_timeout -= time_spent
        hash = self.zobrist_hash(board)
        cache = (max_depth, best_value, best_move, flag)
        self.store(hash, cache)
        return best_value, best_move

    def ids(self, board):
        best_value = float("-inf") if board.gold_move else float("inf")
        best_move = ""
        total_times = 20
        current_depth = 1
        while True:
            start_time = time.time()
            self.ids_timeout = 10
            score, move = self.minimax_function_with_alpha_beta_and_ids(
                current_depth, board, board.game_continue, board.gold_move, float('-inf'), float('inf'))
            end_time = time.time()
            time_spent = end_time - start_time
            total_times -= time_spent
            if board.gold_move:
                if score > best_value:
                    best_value = score
                    best_move = move
            else:
                if score < best_value:
                    best_value = score
                    best_move = move
            current_depth += 1
            if current_depth > self.max_depth:
                break
            if total_times < 0:
                break
        return best_value, best_move

    def ai_move(self, board):
        start_time = time.time()
        self.terminal_nodes = 0
        # print("AI is thinking!")
        new_board = deepcopy(board)
        if self.IDS:
            score, move = self.ids(new_board)
            # print('111')
        else:
            score, move = self.minimax_function_with_alpha_beta(
                self.max_depth, new_board, new_board.game_continue, new_board.gold_move, float('-inf'), float('inf'))
        time_consumed = time.time() - start_time
        self.time_consumed += time_consumed
        self.time_consumed = round(self.time_consumed, 2)
        if move != '':
            board.moves(move)
