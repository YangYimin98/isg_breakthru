"""This object is built for recording the moves."""


from copy import deepcopy


def piece_index(piece):
    if piece == "sp":
        return 0
    elif piece == "gp":
        return 1

    elif piece == 'gK':
        return 2


def update_board(move, board):
    next_state = deepcopy(board)
    next_state.running = False
    next_state.moves(move)
    return next_state


class MyMoveRecording():

    def __init__(self, click_to_start, click_to_end, board):
        self.index_to_row = {
            '1': 10,
            '2': 9,
            '3': 8,
            '4': 7,
            '5': 6,
            '6': 5,
            '7': 4,
            '8': 3,
            '9': 2,
            '10': 1,
            '11': 0}
        self.index_to_col = {v: k for k, v in self.index_to_row.items()}

        self.moves_in_col = {
            'a': 0,
            'b': 1,
            'c': 2,
            'd': 3,
            'e': 4,
            'f': 5,
            'g': 6,
            'h': 7,
            'i': 8,
            'j': 9,
            'k': 10}
        self.col_In_Moves = {v: k for k, v in self.moves_in_col.items()}
        self.start_row = click_to_start[0]
        self.start_col = click_to_start[1]
        self.end_row = click_to_end[0]
        self.end_col = click_to_end[1]
        self.piece_move = board[self.start_row][self.start_col]
        self.piece_capture = board[self.end_row][self.end_col]
        self.move_recording = self.start_row * 10000 + self.start_col * \
            1000 + self.end_row * 100 + self.end_col * 10

    def __eq__(self, other):
        if isinstance(other, MyMoveRecording):
            return self.move_recording == other.move_recording
        return False

    def get_notations(self):
        return self.record_notations(self.start_row, self.start_col) + \
            self.record_notations(self.end_row, self.end_col)

    def record_notations(self, row, col):
        return self.col_In_Moves[col] + self.index_to_col[row]
