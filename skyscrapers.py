def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.
    """
    input_lines = []

    with open(path, "r", encoding="utf-8") as file:

        for line in file:
            line = line.strip("\n")
            input_lines.append(line)

    return input_lines


def left_to_right_check(input_line: str, pivot: int):
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible
    looking to the right, False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412435*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    input_line = input_line[:-1]

    max_dif = -1
    counter = 0

    input_line = input_line[1:]

    idx = int(input_line.index(min(input_line)))
    if idx == 0:
        counter = 1
    for i in range(len(input_line)):
        if max_dif < int(input_line[i]) - int(input_line[idx]) and\
                int(input_line[i]) - int(input_line[idx]) != 0:
            max_dif = int(input_line[i]) - int(input_line[idx])
            counter += 1

    if counter != pivot:
        return False

    return True


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', '*?????*',\
    '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', '*35214*',\
    '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', '*35214*',\
    '*41532*', '*2*1***'])
    False
    """
    for idx in range(len(board)):
        for idx2 in range(len(board[idx])):
            if board[idx][idx2] == "?":
                return False

    return True


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', '*35214*',\
    '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', '*35214*',\
    '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', '*35214*',\
    '*41532*', '*2*1***'])
    False
    """
    for idx in range(1, len(board) - 1):

        if board[idx][0] == "*":
            row_lst = []
            for idx2 in range(1, len(board[idx]) - 1):
                row_lst.append(board[idx][idx2])
            if len(row_lst) != len(set(row_lst)):
                return False

        elif board[idx][-1] == "*":
            row_lst = []
            board[idx] = board[idx][::-1]
            for idx2 in range(1, len(board[idx]) - 1):
                row_lst.append(board[idx][idx2])
            if len(row_lst) != len(set(row_lst)):
                return False

        elif board[idx][0] == "*" and board[idx][-1] == "*":
            row_lst = []
            for idx2 in range(1, len(board[idx] - 1)):
                row_lst.append(board[idx][idx2])
            if len(row_lst) != len(set(row_lst)):
                return False

    return True


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', '*35214*',\
    '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', '*35214*',\
    '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', '*35214*',\
    '*41532*', '*2*1***'])
    False
    """

    for i in range(1, len(board) - 1):
        if board[i][0] == "*" and board[i][-1].isdigit():
            row = left_to_right_check(board[i][::-1], int(board[i][::-1][0]))

            if not row:
                return False

        elif board[i][-1] == "*" and board[i][0].isdigit():
            row = left_to_right_check(board[i], int(board[i][0]))

            if not row:
                return False

    return True


def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height) and
    visibility (top-bottom and vice versa).
    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*',\
    '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*',\
    '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*',\
    '*41532*', '*2*1***'])
    False
    """
    for i in range(1, len(board)-1):
        column_lst = []
        for j in range(1, len(board[i]) - 1):
            column_lst.append(board[j][i])
            if len(column_lst) != len(set(column_lst)):
                return False

    first_row = 0
    last_row = len(board) - 1

    for i in range(len(board)):
        idx = board[first_row][i]
        if idx.isdigit():
            input_line = ""

            for k in range(0, len(board)-1):
                input_line += board[k][i]

            input_line = input_line + "*"

            row = left_to_right_check(input_line, int(input_line[0]))

            if not row:
                return False

    for i in range(len(board)):
        idx = board[last_row][i]

        if idx.isdigit():

            input_line = ""

            for k in range(1, len(board)):
                input_line += board[k][i]

            input_line = input_line[::-1]
            input_line = input_line + "*"

            row = left_to_right_check(input_line, int(input_line[0]))

            if not row:
                return False

    return True


def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.
    """
    board = read_input(input_path)

    unchecked_skyscrapers = check_not_finished_board(board)

    horizontal_check = check_horizontal_visibility(board)

    column_check = check_columns(board)

    uniq_check = check_uniqueness_in_rows(board)

    if unchecked_skyscrapers and horizontal_check and column_check and\
            uniq_check:
        return True

    return False


if __name__ == "__main__":
    print(check_skyscrapers("check.txt"))
