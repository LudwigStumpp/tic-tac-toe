from .helpers import *

class WrongConfigurationException(Exception):
    pass

class CantMakeMoveException(Exception):
    pass

class CantEvaluateException(Exception):
    pass

class Board:
    def __init__(self, num_rows, num_cols, num_winning, stone_p1, stone_p2, field_preset = None):
        # check if winnable
        if (num_winning > num_rows) and (num_winning > num_cols):
            raise WrongConfigurationException('num_winning must be equal to one of either num_rows or num_cols')

        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_winning = num_winning

        # check if stones other string values than ""
        if self.is_empty(stone_p1) or self.is_empty(stone_p2):
            raise WrongConfigurationException('stones must have other values than " "')

        self.stone_p1 = stone_p1
        self.stone_p2 = stone_p2
        
        # check if preset field has correct dimensions + values
        if field_preset:
            rows = len(field_preset)
            cols = len(field_preset[0])

            # check if size aligns
            if not ((rows == self.num_rows) or (cols == self.num_cols)):
                raise WrongConfigurationException('preset field must have same dimensions as specified with num_rows and num_cols')

            # check if values meet stones
            unique_values = unique_2d(field_preset)
            for value in unique_values:
                if not self.is_valid_stone(value):
                    raise WrongConfigurationException('preset field must have same stones as specified with stone_p1 and stone_p2 or " " for empty')

            # all correct
            self.field = field_preset
        else:
            # intialize empty field
            self.field = [[' ' for x in range(self.num_rows)] for y in range(self.num_cols)]

    def is_empty(self, value):
        if value == ' ':
            return True
        
        return False

    def is_valid_stone(self, value):
        if not self.is_empty(value) and ((value != self.stone_p1) and (value != self.stone_p2)):
            return False
        return True

    def show_board(self):
        rows = len(self.field)
        cols = len(self.field[0])

        for r in range(rows):
            for c in range(cols):
                print('|', end = '')
                print(self.field[r][c], end = '')
            print('|')

    def get_free_moves(self):
        free_moves = []

        rows = len(self.field)
        cols = len(self.field[0])

        for r in range(rows):
            for c in range(cols):
                value = self.field[r][c]
                if self.is_empty(value):
                    free_moves.append(r * cols + c + 1)

        return free_moves

    def set_move(self, value, position):
        if not self.is_valid_stone(value):
            raise CantMakeMoveException(f'stones must have either {self.stone_p1}, {self.stone_p2} or " "')

        free_moves = self.get_free_moves()
        if position not in free_moves:
            raise CantMakeMoveException(f'position {position} not in free places {free_moves}')

        (row, col) = self.get_row_col_from_position(position)

        self.field[row][col] = value

    def get_row_col_from_position(self, position):
        row = int((position - 1) / self.num_cols)
        col = (position - 1) % self.num_cols 

        return row, col

    def is_win(self, stone):
        if stone != self.stone_p1 and stone != self.stone_p2:
            raise CantEvaluateException(f'stones must have either {self.stone_p1}, {self.stone_p2}')

        rows = len(self.field)
        cols = len(self.field[0])

        for r in range(rows):
            for c in range(cols):
                value = self.field[r][c]
                if value == stone:

                    # left, top, right, bottom, top-left, top-right, bottom-right, bottom-left
                    check_ver_list = [0, -1, 0, 1, -1, -1, 1, 1]
                    check_hor_list = [-1, 0, 1, 0, -1, 1, 1, -1]

                    for i in range(len(check_ver_list)):
                        row_current = r
                        col_current = c

                        check_ver = check_ver_list[i]
                        check_hor = check_hor_list[i]
                    
                        for line in range(self.num_winning - 1):
                            row_current = row_current + check_ver
                            col_current = col_current + check_hor

                            if row_current >= rows or col_current >= cols:
                                break

                            value_current = self.field[row_current][col_current]
                            if value_current != stone:
                                break

                            if (line + 1) == (self.num_winning - 1):
                                return True
                    
                    return False


                    



