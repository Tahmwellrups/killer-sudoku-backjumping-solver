
# ✏️ Killer Sudoku Solver (Backjumping Algorithm)
### Implemented using Pygame with UI

![image](https://github.com/Tahmwellrups/killer-sudoku-backjumping-solver/assets/130148168/7b3fd76b-e64b-41e9-8fc0-0cc3ce657cb0)

Killer Sudoku is a combination of both Sudoku and Kakuro (Cross Sums) puzzles. Typically it takes the form of a 9x9 grid, but for this project, I used 4x4 grid. 
It also has "cages" to add twist to the traditional Sudoku, it has the sum of the numbers included in that cage. 

The game works by clicking squares that will be included in the cage, and the user will input the sum of the cage.

![image](https://github.com/Tahmwellrups/killer-sudoku-backjumping-solver/assets/130148168/33a2354a-7269-4481-b49a-aeb530e80419)
![image](https://github.com/Tahmwellrups/killer-sudoku-backjumping-solver/assets/130148168/d777df9c-87a5-44b1-9348-f7ee38ec51a5)

If the whole board is completed with cages, the board will be solved using Backjumping algorithm by clicking the "SOLVE" button. 

![image](https://github.com/Tahmwellrups/killer-sudoku-backjumping-solver/assets/130148168/23b26b45-1d15-4e64-85bd-e23dbf555919)

In this algorithm, when a dead end is encountered while solving the board, instead of backtracking all the way to the root of the search tree, 
the algorithm identifies the most recent decision point that caused the conflict using the find_empty_cell() function and jumps back directly to that point, 
filling it with value until it satisfies the conditions.

