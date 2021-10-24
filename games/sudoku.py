# Based on a tutorial from freeCodeCamp.org
# This doesn't truly solve the sudoku, but rather, 
# determines if at least one possible solution exits.

# Finds the next -1 square
def find_next_empty(puzzle):
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c
    return None, None


# Determines whether this guess is valid
def is_valid(puzzle, guess, row, col):

    row_vals = puzzle[row]
    if guess in row_vals:
        return False

    col_vals = []
    for i in range(9):
        col_vals.append(puzzle[i][col])
    # Or- col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    row_start = (row // 3) * 3
    col_start = (col // 3) * 3

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False

    return True


def solve_sudoku(puzzle):
    # Step 1: Choose somewhere to make a guess
    row, col = find_next_empty(puzzle)

    # Step 1.1: Make sure the guess is valid
    if row is None:
        return True

    # Step 2: If there's an empty square, make a guess
    for guess in range(1, 10):
        # Step 3: Check if this guess is valid
        if is_valid(puzzle, guess, row, col):
            # Step 3.1: If the guess is valid, guess this spot!
            puzzle[row][col] = guess
            # Step 4: Keep calling until we get to the end
            if solve_sudoku(puzzle):
                return True

        # Step 5: If the guess isn't valid, or if the guess doesn't solve the puzzle, backtrack
        puzzle[row][col] = -1

    # Step 6: If none of the numbers work that we try, then this puzzle is impossible
    return False
