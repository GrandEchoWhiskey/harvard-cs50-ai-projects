from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(

    # Can be Knight or Knave but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    # A can be Knight or Knave but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # B can be Knight or Kanve but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))

)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(

    # A can be Knight or Knave but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # B can be Knight or Kanve but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # A same as B
    Implication(AKnight, Or(
        And(AKnight, BKnight),
        And(AKnave, BKnave)
    )),

    # A not same as B
    Implication(AKnave, Not(Or(
        And(AKnight, BKnight),
        And(AKnave, BKnave)
    ))),

    # B different as A
    Implication(BKnight, Or(
        And(AKnight, BKnave),
        And(AKnave, BKnight)
    )),

    # B not different as A
    Implication(BKnave, Not(Or(
        And(AKnight, BKnave),
        And(AKnave, BKnight)
    )))

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    # A can be Knight or Knave but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # B can be Knight or Kanve but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # C can be Knight or Kanve but not both
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Or(

        # "I am a knight."
        And(
            Implication(AKnight, AKnight),
            Implication(AKnave, Not(AKnight))
        ),

        # "I am a knave."
        And(
            Implication(AKnight, AKnave),
            Implication(AKnave, Not(AKnave))
        )

    ),

    # Cant say both
    Not(And(

        # "I am a knight."
        And(
            Implication(AKnight, AKnight),
            Implication(AKnave, Not(AKnight))
        ),

        # "I am a knave."
        And(
            Implication(AKnight, AKnave),
            Implication(AKnave, Not(AKnave))
        )

    )),


    # B says "A said 'I am a knave'."
    Implication(BKnight, And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave))
    )),

    Implication(BKnave, Not(And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave))
    ))),

    # B says "C is a knave."
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # C says "A is a knight."
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
