import itertools
import random
from copy import deepcopy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        if self.count == len(self.cells):
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def neighbours(self, cell):
        """
    !   Helper function:
        Returns cells in a set which are 1 block away from the "cell" passed variable
        """

        ret_val = set()

        # Loop through each cell
        for row in range(self.height):
            for col in range(self.width):

                # Get cells of one in each direction, but not self
                # [-1, -1][-1, 0][-1, 1]
                # [ 0, -1][ 0, 0][ 0, 1]
                # [ 1, -1][ 1, 0][ 1, 1]
                if abs(cell[0] - row) <= 1 and abs(cell[1] - col) <= 1 and (row, col) != cell:
                    ret_val.add((row, col))

        return ret_val

    def check(self):
        """
    !   Helper function:
        Checks knowledge, adds additional mines and safes when found
        """

        copy_knowledge = deepcopy(self.knowledge)
        for sentence in copy_knowledge:

            # Assign mines and safes known by the sentence
            mines = sentence.known_mines()
            safes = sentence.known_safes()

            # When any mines mark them and run self
            if mines:
                for mine in mines:
                    self.mark_mine(mine)
                    self.check()

            # When any safes mark them and run self
            if safes:
                for safe in safes:
                    self.mark_safe(safe)
                    self.check()

    def inference(self, a_sentence, b_sentence):
        """
    !   Helper function:
        Update knowledge based on inference
        """

        # Check if A is subset of B
        if a_sentence.cells.issubset(b_sentence.cells):

            # Create new sentence
            n_cells = b_sentence.cells - a_sentence.cells
            n_count = b_sentence.count - a_sentence.count
            n_sentence = Sentence(n_cells, n_count)

            # Assign mines and safes known by the new sentence
            mines = n_sentence.known_mines()
            safes = n_sentence.known_safes()

            # When any mines just mark them
            if mines:
                for mine in mines:
                    self.mark_mine(mine)

            # When any safes just mark them
            if safes:
                for safe in safes:
                    self.mark_safe(safe)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1. mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2. mark the cell as safe
        self.mark_safe(cell)

        # 3. add a new sentence to the AI's knowledge base,
        #   based on the value of `cell` and `count`
        cells = set()
        copy_count = deepcopy(count)
        neighbours = self.neighbours(cell)
        for v_cell in neighbours:
            if v_cell in self.mines:
                copy_count -= 1
            if v_cell not in self.mines | self.safes:
                cells.add(v_cell)

        n_sentence = Sentence(cells, copy_count)

        if len(n_sentence.cells) > 0:
            self.knowledge.append(n_sentence)

        # 4. mark any additional cells as safe or as mines,
        #   if it can be concluded based on the AI's knowledge base
        self.check()

        # 5. add any new sentences to the AI's knowledge base,
        #   if they can be inferred from existing knowledge
        for a_sentence in self.knowledge:
            for b_sentence in self.knowledge:
                self.inference(a_sentence, b_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # For not made moves from the safe one, return first
        for move in self.safes - self.moves_made:

            # When using move from known as safe, no need to check if it's a mine
            return move

        # No move found
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # Return None when no possible safe move exist
        if (len(self.moves_made) + len(self.mines)) >= (self.width * self.height):
            return None

        # Loop till find possible move, the more cells used the slower the code,
        # but random move should happen most likely at the start of the game.
        while True:

            # Get random row and column
            row = random.randrange(self.height)
            col = random.randrange(self.width)

            # When cell isn't a mine, and the move still exists
            if (row, col) not in self.moves_made | self.mines:
                return row, col
