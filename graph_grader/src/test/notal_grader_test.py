from graph_grader.src.grader.notal_grader import notal_grader

src_answers = [
    """
PROGRAM demo_1
KAMUS
    sum, i, n: integer

    function pangkat(a, n: integer) -> integer

ALGORITMA
    input(n)
    i <- 1
    sum <- 0

    repeat
        sum <- sum + pangkat(2, i)
        i <- i + 1
    until (i = n)

    output(sum)

function pangkat(a, n: integer) -> integer

KAMUS LOKAL
    res, i: integer

ALGORITMA
    res <- 1
    repeat n times
        res <- res * a
    -> res

""",
    """
PROGRAM demo_1

KAMUS
    sum, n: integer

    function pangkat(a, n: integer) -> integer

ALGORITMA
    input(n)
    sum <- pangkat(2, n + 1) - 1
    output(sum)

function pangkat(a, n: integer) -> integer

KAMUS LOKAL
    res, i: integer

ALGORITMA
    res <- 1
    repeat n times
        res <- res * a
    -> res
"""
]

src = """
PROGRAM demo_1

KAMUS
    sum, n: integer

    function pangkat(a, n: integer) -> integer

ALGORITMA
    input(n)
    sum <- pangkat(2, n + 1) - 1
    output(sum)

function pangkat(a, n: integer) -> integer

KAMUS LOKAL
    res, i: integer

ALGORITMA
    res <- 1
    repeat n times
        res <- res * a
    -> res

"""

if __name__ == "__main__":
    score = notal_grader(src_answers, src)
    print(score)

