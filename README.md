# Advanced-Programming-and-Optimization-Algorithms
Solutions to programming assignments 



ASSIGNMENT 1 

Part 1: ("lp assignment 1, vocareum version")

Solve the following program:

   min 122x + 143y
subject to: x ≥ -10 y ≤ 10 3x + 2y ≤ 10 12x + 14y ≥ -12.5 2x + 3y ≥ 3 5x - 6y ≥-100 Required output example:

Optimal solution: x = 0.1 y = -2.3 Objective value: 100.1214 Tight constraints: 1 2 4 So, your program should find the optimal solution, determine its objective value, and identify the tight constraints. 





Part 2: ("lp assignment 2, vocareum version")

Find an optimal mixed strategy of the following game: Both players choose independently a single integer from 1 to 6. Then, the numbers are compared:
If they are equal, there is a draw If they differ by 1, the player who played the smaller number gets 2EUR from the other player If they differ by ≥2, the player who played the larger number gets 1EUR from the other player Note that the game is symmetric and the same strategy is optimal for both players. Required output example:

x1: 0.2 x2: 0.1 x3: 0.2 x4: 0.1 x5: 0.2 x6: 0.2





Part 3: ("lp assignment 3, vocareum version")

On some imaginary island, there are 69 companies and there are bilateral contracts between them. The monarch of the island would like to inspect validity of each of these contracts during a single large event. The monarch requires two representatives to represent each contract relationship (they can be both from the same party of the contract or each from a different one). This is of course satisfied by each company sending a single representative, which would require involvement of 69 representatives in total. However, the companies want to find a solution which minimizes the total number of representatives who need to attend the event.

Input file hw1-03.txt contains information about the contracts. Each line corresponds to a single contract and contains identifiers (1-69) of both involved parties separated by a space.

Example output:

representatives from company 1: 1.0 representatives from company 2: 2.0 representatives from company 3: 1.0 ... representatives from company 69: 1.0 Total number of representatives involved: 58 Important: It is not possible to send an arbitrary fraction of a representative. However, it is enough to solve the LP relaxation since it already gives an integral solution. Reasons for this will be explained later in the class.







ASSIGNMENT 2
Consider a set of pictures from 360° camera mounted inside a merry-go-round. They were taken at night and only one seat is visible which emits light – the seat in the shape of a jelly fish. We know that the merry-go-round rotates clockwise and that all the pictures were taken during a single cycle of merry-go-round. Given that the first picture is P1, your task is to sort the rest in the chronological order. Assume that the move of jelly fish is monotonous in horizontal direction, i.e., it always moves in clockwise direction, never backwards.

Input files: text files, each of them with 10 rows and 80 columns representing the brightness level in the given parts of the picture. Jelly fish can be recognized by high brightness (value 1 to 9) on a black background (value 0).

00000000000000000000000000000000000000000000000000000000000000000000000000000000 00000000000000000000000000000000000000000000000000000000000000000000000000000000 00000000000000000000000000000000000000000000000000000000000000000000000000000000 00000000000000000000000000000000000000000000000000000000000000000000000000000000 00000000000000000000000000000000000000000000000000000000000000000000000000000000 00000000000000000000000000000000000005950000000000000000000000000000000000000000 00000000000000000000000000000000000009990000000000000000000000000000000000000000 00000000000000000000000000000000000005950000000000000000000000000000000000000000 00000000000000000000000000000000000003930000000000000000000000000000000000000000 00000000000000000000000000000000000000000000000000000000000000000000000000000000
Directions

In order to capture the movement of the jelly fish between two pictures, use Earth-mover distance, also known as Wasserstein distance. It can be formulated as a min-cost flow problem on a certain network. Use NetworkX package (https://networkx.org) to perform the optimization required to find this flow.
About Earth-mover distance: Consider two distributions over a discrete set of points P: μ in [0,1]^P and λ in [0,1]^P. Since both are distributions and sum of μ(p) over all points in P is 1 (and the same holds for λ), there is surely a way to transform μ into λ: we denote fp,q the probability mass transfered from point p to q for each pair of points p,q from P, in order to transform μ into λ:

For each p in P: μ(p) = Σq fp,q and for each q in P: λ(q) = Σp fp,q.

Note that fp,p denotes the probability mass which remains at the same place. Let d(p,q) denote the distance between p and q. Then, the cost of the transformation f is

Σp,q d(p,q) fp,q

The earth-mover distance of μ and λ is then the cost of the cheapest transformation between μ and λ.

Technical instructions:

Your code should implement function sort_files() which returns ordered list of the pictures, something like this:

['P1.txt', 'P2.txt', 'P3.txt', 'P10.txt', 'P4.txt', 'P13.txt', 'P14.txt', 'P9.txt', 'P15.txt', 'P7.txt', 'P12.txt', 'P11.txt', 'P5.txt', 'P6.txt', 'P8.txt'] You should also define and use function comp_dist(file1, file2) which returns the Earth-mover distance between file1 and file2. I may want to access it during the grading process, especially if your output is not completely correct.
Make sure your code never breaks down. If you know that it cannot handle e.g. P10.txt, skip this file and don't include it in the output. This way, you will not get a full score, but you will still get points for the partial solution.

Before submission, always try your code in vocareum using "Run" button. Incorrect output format, syntax and indentation errors, etc will result into 0 points.

Firstly we define a function which given two files calculated the EMD distance between them. We create a graph with a sink node 's' and a tank node 't' with an additional 'jolly edge' which solves some rounding problems which will would have emerged later
