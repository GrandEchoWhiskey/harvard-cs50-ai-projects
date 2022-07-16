import sys

from crossword import *

from copy import deepcopy


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # Copy domains, better to work on copy in loops
        domains_cpy = deepcopy(self.domains)

        # Go through variables in the copy
        for var in domains_cpy:

            # Assign length variable
            length = var.length

            # Go through words
            for word in domains_cpy[var]:

                # When word is inconsistent remove from orginal
                if len(word) != length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # Create some variables for overlap, copy of domains, and a boolean if revision was made
        x_overlap, y_overlap = self.crossword.overlaps[x, y]
        revision = False
        domains_cpy = deepcopy(self.domains)

        # If exist
        if x_overlap:

            # Go through x words
            for x_word in domains_cpy[x]:

                # Variable if x word letter at x overlap matched y word letter at y overlap
                matched = False

                # Go through y words
                for y_word in domains_cpy[y]:

                    # When x word letter at x overlap is same as y word at y overlap, set matched true and break
                    if x_word[x_overlap] == y_word[y_overlap]:
                        matched = True
                        break

                # When matched check next
                if matched:
                    continue

                # Else remove word and set revision to true
                self.domains[x].remove(x_word)
                revision = True

        # Return revision boolean
        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # Create a queue
        queue = list()

        # If no arcs add sets of 2 vars to list
        if not arcs:

            for var1 in self.domains:

                for var2 in self.crossword.neighbors(var1):

                    # When overlaping add set to list
                    if self.crossword.overlaps[var1, var2] is not None:
                        queue.append((var1, var2))

        # Skip when queue is empty
        while len(queue):

            # Take vars from queue list
            var1, var2 = queue.pop(0)

            # Revise
            if self.revise(var1, var2):

                # When found empty domain -> return false
                if len(self.domains[var1]) == 0:
                    return False

                # Append neighbors to queue
                for neighbor in self.crossword.neighbors(var1):

                    if neighbor != var2:
                        queue.append((neighbor, var1))

        # Arcs provided or no domain ends empty
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # Seek in domains if something is not in assignment -> return false, other way true
        for var in self.domains:

            if var not in assignment:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Unpack assignment values into list
        words = [*assignment.values()]

        # Length checks
        if len(words) != len(set(words)):
            return False

        for var in assignment:

            if var.length != len(assignment[var]):
                return False

        # Overlap check
        for var in assignment:

            for neighbor in self.crossword.neighbors(var):

                if neighbor in assignment:

                    var1, var2 = self.crossword.overlaps[var, neighbor]

                    if assignment[var][var1] != assignment[neighbor][var2]:
                        return False

        # Is consistent
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Create new word dictionary and a list of neighbors
        word_dict = dict()
        neighbors = self.crossword.neighbors(var)

        for word in self.domains[var]:

            eliminated = 0

            for neighbor in neighbors:

                # Skip when neighbor already in assigment
                if neighbor in assignment:
                    continue

                x_overlap, y_overlap = self.crossword.overlaps[var, neighbor]

                for neighbor_word in self.domains[neighbor]:

                    if word[x_overlap] != neighbor_word[y_overlap]:
                        eliminated += 1

            word_dict[word] = eliminated

        # Sort pairs by value
        # Set sort key to second item in pairs, so that the value is the soring key
        # lambda defining inline function
        sort_key = lambda item: item[1]
        sorted_set_list = sorted(word_dict.items(), key=sort_key)
        sorted_dict = {k: v for k, v in sorted_set_list}

        # Return unpacked dict as list
        return [*sorted_dict]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Create dictionary
        choice = dict()

        # Go through vars in domain
        for var in self.domains:

            # When var not in assignment assign value to choice[var]
            if var not in assignment:
                choice[var] = self.domains[var]

        # Create sorted value list, set key to the length of value in dictionary
        sort_key = lambda item:len(item[1])
        sorted_set_list = sorted(choice.items(), key=sort_key)
        sorted_list = [key for key, val in sorted_set_list]

        # Return shortest values key
        return sorted_list[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # When equal length return assignment
        if len(assignment) == len(self.domains):
            return assignment

        # Assign unassingned variable
        variable = self.select_unassigned_variable(assignment)

        for value in self.domains[variable]:

            # Create a assignment copy
            assignment_copy = assignment.copy()
            assignment_copy[variable] = value

            # When copy is consistent
            if self.consistent(assignment_copy):

                # Call self function on the new copy
                result = self.backtrack(assignment_copy)

                # When backtrack was successful -> return result
                if result is not None:
                    return result

        # Unsuccessful
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
