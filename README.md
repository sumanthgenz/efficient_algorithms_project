# efficient algorithms & intractable problems project

Input:  A list of nodes N (length of list vary from 10, 20, 50), pairwise positive happiness reward H and negative stress S between all pairs of nodes and a total negative stress budget S_max. 

Constraints: Assign edges between nodes such that each node must belong to exactly one clique. There must be between [1, |N|] cliques. If num_cliques > 1, then the cliques must be edge-disjoint and unconnected. The sum of pairwise S (stresses) among nodes in any clique C must not exceed S_max / num_cliques.

Goal: Optimize the assignment of edges and formation of cliques such that the sum of pairwise H among all nodes is maximized.

Complexity: NP-Hard

Specifications: https://cs170.org/assets/pdf/project_spec.pdf

Approach: 

We opt to use an ensemble algorithm consisting of two experts, and choosing the maximum-scoring assignment among the two experts. 

Expert 1:
The first expert is a greedy, randomized algorithm that employs local-search and exploration from simulated annealing. At the start, all nodes are unconnected (there are |N| cliques, each consisting only of one node). During each iteration, the algorithm evaluates all valid 1-changes (where any two cliques are merged without violating any constraints) and the associated H-scores with each 1-change. Next, among the top-5 H-scores, we randomly choose amongst the 1-changes that produces one of these scores (note since 1-changes need not produce unique H-scores, we are choosing amongst at least 5 possible 1-changes during each iteration). Having choosen the 1-change, we perform the specified merge. There is then a check which will move around individual nodes from the newly merged clique to any of the other cliques, based on whether there is an overall reduction in S-scores for the configuration of all cliques. Each iteration is repeated for a fixed number of steps until convergence. The algorithm itself is repeated for a fixed number of steps to motivate exploration of the solution space by taking advantage o the randomized nature of the algorithm.

Expert 2:
The second expert consists of a mapping function f, followed by expectation maximization (EM) in the form of k-means clustering algorithm. Given pairwise H and S values between nodes, for a given pair of distinct nodes N(i) and N(j), a mapping function f(i, j) will produce a pairwise distance D(ij) based on H(ij) and S(ij). After repeating this process for all distinct pairs of nodes in N, we can arbitrary choose one node as an anchor (the zero vector in a p-dimensional Euclidian space R, for p=3), and plot the remaining points in this space using pairwise distances. Having now assigned a unique coordinate in R for each node in N, we now use vanilla k-means clustering, iterating over k values from range [1, |N|], to explore all possible clique sizes. 
