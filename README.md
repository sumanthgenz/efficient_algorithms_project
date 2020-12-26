# efficient algorithms project

Input:  A list of nodes N (length of list vary from 10, 20, 50), pairwise positive happiness reward H and negative stress S between all pairs of nodes and a total negative stress budget S_max. 

Constraints: Assign edges between nodes such that each node must belong to exactly one clique. There must be between [1, |N|] cliques. If num_cliques > 1, then the cliques must be edge-disjoint and unconnected. The sum of pairwise S (stresses) among nodes in any clique C must not exceed S_max / num_cliques.

Goal: Optimize the assignment of edges and formation of cliques such that the sum of pairwise H among all nodes is maximized.

Complexity: NP-Hard


