"""This object is built for providing the correct move ways for pieces."""

import move_recordings


class GameBoard():

    def __init__(self):
        # the board of the whole game: sp represents silver piece, gp
        # represents gold pieces, gK represents king/flag, -- represents blank
        # space

        self.board = [

            ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', 'sp', 'sp', 'sp', 'sp', 'sp', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', 'sp', '--', '--', 'gp', 'gp', 'gp', '--', '--', 'sp', '--'],
            ['--', 'sp', '--', 'gp', '--', '--', '--', 'gp', '--', 'sp', '--'],
            ['--', 'sp', '--', 'gp', '--', 'gK', '--', 'gp', '--', 'sp', '--'],
            ['--', 'sp', '--', 'gp', '--', '--', '--', 'gp', '--', 'sp', '--'],
            ['--', 'sp', '--', '--', 'gp', 'gp', 'gp', '--', '--', 'sp', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', 'sp', 'sp', 'sp', 'sp', 'sp', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],

        ]
        self.gold_move = True  # Decide which team to move now
        self.move_log = []  # Record the moves
        self.gold_king_location = (5, 5)  # The initialize location of king
        self.check_mate = False  # WINS FLAG
        self.stale_mate = False  # NO ONE WINS
        self.move_twice = 0  # Change to adjust if someone can move two pieces in one round
        self.turn_team = 0  # Change to another team to move
        self.piece_captured = []  # Capture pieces
        self.gold_piece = 12  # The amount of the gold team
        self.silver_piece = 20  # The amount of the silver team
        self.king = 1  # The amount of the King
        self.result = ' '
        self.game_continue = True
        self.process = []
        self.running = True
        self.index_to_col = (
            ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"])
        self.index_to_row = (
            ["11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1"])

    # All moves without considering checks

    def valid_moves(self):

        moves, capture = [], []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[0])):
                start = self.board[r][c][0]
                if (start == 'g' and self.gold_move) or (
                        start == 's' and not self.gold_move):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        if self.move_twice == 1:
                            last_piece = self.move_log[-1]
                            if r != last_piece.end_row or c != last_piece.end_col:
                                # print('2')
                                self.rules_for_pieces_moves(r, c, moves)

                        else:
                            # print('----')
                            self.rules_for_pieces_moves(r, c, moves)
                            # print('11111')

                            self.rules_for_pieces_capture(r, c, capture)
                            # print('wwwww')

                    elif piece == 'K' and self.move_twice == 0:
                        self.rules_for_pieces_moves(r, c, moves)
                        self.rules_for_pieces_capture(r, c, capture)

        return moves, capture

    def rules_for_pieces_moves(self, r, c, moves):
        before = len(moves)
        # up, left, down, right
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            for i in range(1, 11):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 11 and 0 <= end_col < 11:  # on board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':  # empty space valid
                        moves.append(
                            move_recordings.MyMoveRecording(
                                (r, c), (end_row, end_col), self.board))
                    else:
                        break
                else:  # off board
                    break
        return len(moves) - before

    # Get all the pawn captures for the pawn located at row, col and add these
    # moves to the list

    def rules_for_pieces_capture(self, r, c, capture):
        enemy_color = 's' if self.gold_move else 'g'
        directions_oblique = ((-1, -1), (-1, 1), (1, -1), (1, 1))

        for d in directions_oblique:
            for i in range(1, 11):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 11 and 0 <= end_col < 11:  # on board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':  # empty space valid
                        break
                    elif end_piece[0] == enemy_color:  # enemy piece valid
                        capture.append(
                            move_recordings.MyMoveRecording(
                                (r, c), (end_row, end_col), self.board))
                        # print(self.board)
                        break
                    else:
                        break
                else:
                    break

    # Turn the team

    def turn(self):
        self.gold_move = not self.gold_move
        self.turn_team += 1
        self.move_twice = 0

    def calculate_pieces(self, move):
        if move.piece_capture != "--":
            self.move_twice = 2
            self.piece_captured.append(move.piece_capture)
            if move.piece_capture == 'gK':
                self.king = 0
            elif move.piece_capture[0] == 'g':
                self.gold_piece -= 1
            else:
                self.silver_piece -= 1
        elif move.piece_move[1] == "K":
            self.move_twice = 2
        else:
            self.move_twice += 1

    # retrieve the last move。

    def retrieve_move(self):
        if len(self.move_log) != 0:  # make sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_move
            self.board[move.end_row][move.end_col] = move.piece_capture
            self.gold_move = not self.gold_move  # switch turns back
            if move.piece_move[1] == 'K':
                self.move_twice = 0
                self.gold_move = not self.gold_move
                self.gold_king_location = (move.start_row, move.start_col)

            elif self.move_twice == 0:
                self.gold_move = not self.gold_move  # the turn back to the user
                self.turn_team -= 1
                self.move_twice = 1
            elif self.move_twice == 1:
                self.move_twice = 0

    def moves(self, move):
        self.board[move.start_row][move.start_col] = '--'
        turn = 'gold' if self.gold_move else 'silver'
        row_board = move.end_row
        col_board = move.end_col
        if move.piece_move == 'gK':
            self.gold_king_location = (row_board, col_board)
            if (row_board == 0 or row_board == 10) or (
                    col_board == 10 or col_board == 0):
                self.result = 'Gold Team wins the game!'
                self.game_continue = False
        if self.running:
            if move.piece_capture == '--':
                self.process.append(
                    turn + ':   ' + move.piece_move + ' ' + move.get_notations())
                if move.piece_move == 'gK':
                    if (move.end_col == 10 or move.end_col == 0) or (
                            move.end_row == 0 or move.end_row == 10):
                        self.result = "Gold Team wins the game!"
                        self.game_continue = False
            else:
                self.process.append(
                    turn +
                    " captured " +
                    move.piece_capture +
                    ":   " +
                    move.piece_move +
                    " " +
                    move.get_notations())
        self.calculate_pieces(move)

        if self.silver_piece == 0:
            self.game_continue = False
            self.result = "Gold Team wins the game!"
        if self.king == 0:
            self.game_continue = False
            self.result = "Silver Team wins the game!"

        self.board[move.end_row][move.end_col] = move.piece_move
        self.move_log.append(move)
        if self.move_twice == 2:
            self.turn()

    # # move the piece, not capture
    #
    # def makeMove(self, move):
    #     self.board[move.startRow][move.startCol] = '--'
    #     self.board[move.endRow][move.endCol] = move.pieceMoved
    #     self.moveLog.append(move)  # log the move so we can undo it later
    #
    #     if move.pieceMoved[1] == 'K':
    #         self.moveTwice += 1
    #     self.moveTwice += 1
    #     if self.moveTwice == 2:
    #         self.goldToMove = not self.goldToMove
    #         self.turnTeam += 1
    #         self.moveTwice = 0
    #
    #     if move.pieceMoved[1] == 'K':
    #         self.goldKingLocation = (move.endRow, move.endCol)
    #         print(self.goldKingLocation)
    #         # return self.goldKingLocation
    #
    # # capture piece,not move
    #
    # def makeCapture(self, move):
    #     self.board[move.startRow][move.startCol] = "--"
    #     self.pieceCaptured.append(self.board[move.endRow][move.endCol])
    #     self.board[move.endRow][move.endCol] = move.pieceMoved
    #     self.moveLog.append(move)
    #
    #     self.goldToMove = not self.goldToMove
    #     self.turnTeam += 1
    #     self.moveTwice = 0

    # Determine if the current player is in check

    # def inCheck(self):
    #     if self.goldToMove:
    #         return self.squareUnderAttack(self.silverNothingLocation[0], self.silverNothingLocation[1])
    #     else:
    # return self.squareUnderAttack(self.goldKingLocation[0],
    # self.goldKingLocation[1])

    # Determine if the enemy can attack the square r, c

    # def squareUnderAttack(self, r, c):
    #     self. goldToMove = not self.goldToMove  # switch to oppoent's turn
    #     oppMoves = self.getAllPossibleMoves()
    #     self.goldToMove = not self.goldToMove  # switch turns back
    #     for move in oppMoves:
    #         if move.endRow == r and move.endCol == c:  # square is under attack
    #             return True
    #     return False
