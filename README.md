# efficient algorithms & intractable problems project

Input:  A list of nodes N (length of list vary from 10, 20, 50), pairwise positive happiness reward H and negative stress S between all pairs of nodes and a total negative stress budget S_max. 

Constraints: Assign edges between nodes such that each node must belong to exactly one clique. There must be between [1, |N|] cliques. If num_cliques > 1, then the cliques must be edge-disjoint and unconnected. The sum of pairwise S (stresses) among nodes in any clique C must not exceed S_max / num_cliques.

Goal: Optimize the assignment of edges and formation of cliques such that the sum of pairwise H among all nodes is maximized.

Complexity: NP-Hard

Specifications: https://cs170.org/assets/pdf/project_spec.pdf

Input Generation Approach:
After trying to generate random inputs but struggling to find a "good" or "optimal" output for it, we tried creating inputs by hand by constraining budgets carefully (for example nodes 0-4 and 5-9 cannot mix, and further 0-1 cannot mix with 2-3) such that we can backtrack from our intended optimal solution to a full input set. While this helped guarantee we had a true optimal, since the our first-iteration solver (Expert 1 in the section below), was able to get the optimal solution. Then we realized we could generate inputs somewhat randomly by creating random clusters with N-points (where N = #nodes or students on input graph G) such that nodes points in the same cluster Euclidian Space correspond to cliques on G (room assignments). This mapping is calculated as a function of pairwise Euclidian Distances between points, which is then decomposed into pairwise Happiness and Stress matrices between the nodes. This was a fast process, and our large input proved to be moderately challenging for other solvers. We considered the hints suggested on piazza, which involved the difficult inputs for independent set, but ran out of time to try it.

Solver Approach: 
We opt to use an ensemble algorithm consisting of two experts, and choosing the maximum-scoring assignment among the two experts (we attempted an unsuccessful third expert as well).

Expert 1:
The first expert is a greedy, randomized algorithm that employs local-search and exploration from simulated annealing. At the start, all nodes are unconnected (there are |N| cliques, each consisting only of one node). During each iteration, the algorithm evaluates all valid 1-changes (where any two cliques are merged without violating any constraints) and the associated H-scores with each 1-change. Next, among the top-5 H-scores, we randomly choose amongst the 1-changes that produces one of these scores (note since 1-changes need not produce unique H-scores, we are choosing amongst at least 5 possible 1-changes during each iteration). Having chosen the 1-change, we perform the specified merge. There is then a check which will move around individual nodes from the newly merged clique to any of the other cliques, based on whether there is an overall reduction in S-scores for the configuration of all cliques (rooms). Each iteration is repeated for a fixed number of steps until convergence. The algorithm itself is repeated for a fixed number of steps to motivate exploration of the solution space by taking advantage o the randomized nature of the algorithm.

Expert 2:
The second expert uses 170 Starter Code. Whereas the first approach starts with all nodes disconnected from each other and greedily merges rooms under budget constraints to maximize happiness (bottom-up), this approach starts with a fully disconnected graph and removes nodes and their adjacent vertices form the graph under budget constraints to greedily form cliques that maximize happiness (top-down). Another key difference from Expert 1 is that Expert 2 deals with 1-changes on the order of each node (student) being moved, rather than cliques (rooms) being merged. Similar to Expert 1, the algorithm uses randomization between topK moves, has modes to consider initially illegal modes, and runs the algorithm several times, and returns maximum valid score and room assignment across all rollouts.

Sub- Expert 3:
We considered a third expert using k-means clustering algorithm. First we convert pairwise H and S values between nodes to Euclidian distance D matrix and using QR decomposition on a function of the distance matrix [1] [2], and plot the remaining points using this. Having now assigned a unique coordinate in R for each node in N, we now use vanilla k-means clustering, iterating over k values from range [1, |N|], to explore all possible clique sizes. A bare-bones implementation of this approach [4] did not work as the ordering of the points was not the same as the order of the nodes of G (students). Additionally, we plotted all inputs from peers in R^2 [3] and saw that the inputs generally do not form well-formed clusters.

Reflection on Solver:
Overall, we are decently happy with our ensemble solver. Both expert 1 and expert 2 have done very well on a good portion of the inputs, and we think that greedy + randomization is a powerful combination, that allows us to reliably hit optimal or rank1 solutions given enough rollouts. Since expert 1 is bottom-up and room-focused, and expert 2 is top-down and student-focused, we saw that the two complemented each other and were able to achieve optimality on different sets of inputs. Additionally, the time to run inputs by size-type, has successfully been <8 hours. Thus, we are happy that this ensemble greedy randomized approach approximates optimal solutions to this problem.

Considered Approaches:
Given enough time, we would've tried several other approaches, namely reduction to other problem types. In particular, we considered multiple-knapsacks (each room is a knapsack, H and S -> W and W) and independent set (cliques or rooms as sets). We considered a google package as inspiration [5], but did not have time to begin implementing.

Resources:
All input generation and solvers were run locally at all times (never used instructional machines). Python packages such as numpy, random, sklearn (for clustering), matplotlib (for cluster visualization), multiprocessing and networkx were used to save on implementation time, boost computation speed and improve code clarity.

Team:
We are grateful to have done this as a team. All of us brought unique ideas and approaches to all aspects of the project, which created diversity in our inputs and solver. At (many) times, this project was difficult and tested our patience, but venting and working through these tough moments as a team was key. 

Sources Cited:
[1] https://math.stackexchange.com/questions/156161/finding-the-coordinates-of-points-from-distance-matrix
[2] https://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.linalg.qr.html
[3] https://matplotlib.org/3.1.1/gallery/mplot3d/scatter3d.html
[4] https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
[5] https://developers.google.com/optimization/bin/multiple_knapsack



