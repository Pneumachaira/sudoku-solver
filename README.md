# sudoku-solver
A relatively simple program that solves Sudoku puzzles.
On December 29, 2019, a friend and I made a bet to see who could make a better Sudoku Solver in two weeks.
Currently, using the techniques listed on https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php the program can look for Sole Candidates and Unique Candidates.
After no further numbers can be discerned, the program finds one of the most influential cells and inputs a guess number. Afterwards, it returns to the Sole Candidates and Unique Candidates. If the puzzle cannot be completed with the guess number, the pre-guess list is recalled and a new guess number is put in.
We are using https://sudoku.game/ to generate puzzles of varying difficulty. Currently the program can solve all levels of Sudoku.
