import networkx as nx
from parse import *
from utils import *
import sys
from os.path import basename, normpath
import glob
import random
import numpy as np
import multiprocessing
from joblib import Parallel, delayed
from tqdm import tqdm

def solve(G, s, greed=True, max_step=50):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """

    def convergence(room_queue, s):
        
        #of the last steps stored in queue, output max-scoring, valid room_assignment 
        max_score, max_D, max_K = 0, 0, 0
        for r in room_q:
            D = {}
            for i in range(len(r)):
                D[str(i)] = r[i]
            D = convert_dictionary(D)
            score = calculate_happiness(D, G)
            if is_valid_solution(D, G, s, len(r)) and calculate_happiness(D, G) > max_score:
                max_score = score
                max_D = D
                max_K = len(r)
        if not max_D or not max_K:
            return {}, G.number_of_nodes()
        return max_D, max_K

    n = G.number_of_nodes()
    rooms = [list(range(0,n))]
    n_rooms = 1
    done = False
    steps = 0
    topK =  7

    room_q = []

    while steps < max_step:

        #define outside nested loops to save memory allocation
        best_moves = []
        old_from_room, old_to_room = None, None
        new_from_room, new_to_room = None, None

        # random.shuffle(rooms)

        #iterate over shuffled rooms, and find the first room that is invalid stress
        invalid_rooms = [(calculate_stress_for_room(r, G) > (s/n_rooms)) for r in rooms]

        if any(invalid_rooms):
            from_idx = invalid_rooms.index(True)
            old_from_room = rooms[from_idx]
        
            for student_idx in range(len(old_from_room)):
                new_from_room = old_from_room[:student_idx] + old_from_room[student_idx + 1:]

                # calculate the amount of stress we reduced, which we want to optimize alongisde happiness
                dec_S =  calculate_stress_for_room(old_from_room, G) - calculate_stress_for_room(new_from_room, G)        
            
                #see if its possible to move the optimal student to an existing room besides the one they just got removed form
                for to_idx in range(len(rooms)):
                    if from_idx != to_idx:
                        old_to_room = rooms[to_idx]
                        new_to_room = old_to_room + [old_from_room[student_idx]]

                        #stress added by moving student to the destination to_room
                        # dec_S = calculate_stress_for_room(old_to_room, G) - calculate_stress_for_room(new_to_room, G)        

                        #calculate the happiness of moving the student given by student_idx to old_to_room (the result is new_to_room)
                        inc_H = calculate_happiness_for_room(new_to_room, G) - calculate_happiness_for_room(old_to_room, G)

                        #check whether the stress in new_to_room is valid
                        if (calculate_stress_for_room(new_to_room, G) <= (s/(n_rooms))):
                            best_moves.append((dec_S + inc_H, from_idx, to_idx, student_idx))
                    else:
                        best_moves.append((dec_S, from_idx, 101, student_idx))

            #each move is tuple (happiness, from_room_idx, to_room_idx, student_from_room_idx)           
            best_moves = sorted(best_moves, key=lambda x: -x[0])
            # moves = best_moves[0]
            move = random.choice(best_moves[:topK])


            #if no possible move to existing room, place student alone in a new room
            if move[2] == 101:
                rooms.append([rooms[move[1]][move[3]]])
                rooms[move[1]] = rooms[move[1]][:move[3]] + rooms[move[1]][move[3]+1:]
                n_rooms += 1

            else:
                rooms[move[2]].append(rooms[move[1]][move[3]])
                rooms[move[1]] = rooms[move[1]][:move[3]] + rooms[move[1]][move[3]+1:]

                # print('')
                # print('FIXER')
                # print(steps)
                # # print(move)
                # print(rooms)
                # print(s/n_rooms)
                # print([calculate_stress_for_room(r, G) for r in rooms])

            room_q.append(rooms)

        else:
            for from_idx in range(len(rooms)):
                for student_idx in range(len(rooms[from_idx])):
                    for to_idx in range(len(rooms)):
                        if from_idx != to_idx:
                            old_from_room = rooms[from_idx]
                            old_to_room = rooms[to_idx]
                            new_from_room = old_from_room[:student_idx] + old_from_room[student_idx + 1:]
                            new_to_room = old_to_room + [old_from_room[student_idx]]

                            dec_H = calculate_happiness_for_room(new_from_room, G) + calculate_happiness_for_room(old_from_room, G)
                            inc_H = calculate_happiness_for_room(new_to_room, G) + calculate_happiness_for_room(old_to_room, G)

                            # all rooms in old rooms are valid in stress
                            # removing student from old_from_room decreases stress
                            # so, only check new_to_room stress validity

                            if greed:
                                if (calculate_stress_for_room(new_to_room, G) >= (s/n_rooms)):
                                    best_moves.append((dec_H + inc_H, from_idx, to_idx, student_idx))

                            if not greed:
                                if (calculate_stress_for_room(new_to_room, G) <= (s/n_rooms)):
                                    best_moves.append((dec_H + inc_H, from_idx, to_idx, student_idx))

            # if we are out of moves, the algorithm has converged and score can no longer legally improve
            if not len(best_moves):
                # done = True
                pass
            else:
                best_moves = sorted(best_moves, key=lambda x: -x[0])
                # move = best_moves[0]
                move = random.choice(best_moves[:topK])

                rooms[move[2]].append(rooms[move[1]][move[3]])
                rooms[move[1]] = rooms[move[1]][:move[3]] + rooms[move[1]][move[3]+1:]

                # print('')
                # print('ASSIGNER')
                # print(steps)
                # # print(move)
                # print(rooms)
                # print(s/n_rooms)
                # print([calculate_stress_for_room(r, G) for r in rooms])

            room_q.append(rooms)
                
        steps += 1

    #todo
    #randomly choose between top5 best moves with 70% probability, top10 with 20% probability, bottom 10 with 10% probability  

    # room_queue = [[[2, 3, 11, 16, 20, 23, 25, 27, 49], [41, 34, 10, 7, 35, 12], [36, 37, 15, 14, 39], [19, 46, 42, 44, 38], [40, 6, 33, 29, 31, 9, 8], [43, 45, 17], [47, 5], [13, 24, 1, 26, 30, 28], [22, 0, 4, 48, 21, 18, 32]]]
    return convergence(room_q[-20:], s)

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

def solo_main(path):
    G, s = read_input_file(path)



    D, k = solve(G, s, greed=False, max_step=50)
    assert is_valid_solution(D, G, s, k)

    Dg, kg = solve(G, s, greed=True, max_step=60)
    assert is_valid_solution(Dg, G, s, kg)
    careful = calculate_happiness(D ,G)
    greedy = calculate_happiness(Dg ,G)

    if careful >= greedy:
        return (careful, D)
    else:
        return (greedy, Dg)


if __name__ == '__main__':
    # small_hitlist = [5, 12, 14, 17, 21, 25, 29, 31, 36, 40, 41, 42, 43, 44, 
    # 49, 57, 58, 62, 64, 65, 66, 67, 68, 70, 76, 81, 82, 84, 85, 89, 
    # 91, 92, 93, 96, 98, 102, 104, 106, 107, 112, 117, 118, 119, 122,
    # 125, 126, 129, 132, 134, 135, 136, 138, 141, 143, 149, 150, 154,
    # 155, 157, 160, 163, 165, 167, 169, 171, 179, 181, 183, 185, 194, 
    # 210, 212, 216, 219, 222, 231, 234, 236, 239]

    # maybe = [141]
    # small_hitlist = [14, 29, 85, 117, 129, 134, 155, 
    # 234]

    # print(len(small_hitlist))

    # for i in range(len(small_hitlist[:1])):
        # num = small_hitlist[i]

    # paths = ["data/inputs/small-{}.in".format(num)]*num_rollouts


    num_rollouts = 2
    inputs = glob.glob('data/inputs/large?*.in')
    for input_path in inputs:

        cores = multiprocessing.cpu_count()
        paths = [input_path] * num_rollouts
        output_path = 'data/anik_large_outputs/' + basename(normpath(input_path))[:-3] + '.out'

        with multiprocessing.Pool(cores) as p:
            rollouts = p.map(solo_main, paths)

    
        rollouts = sorted(rollouts, key=lambda x: -x[0])
        max_score, max_Dict = rollouts[0][0], rollouts[0][1]
        # print("Medium-{} Total Happiness: {}".format(input_path[-3:], max_score))
        write_output_file(max_Dict, output_path)

    # for _ in range(num_rollouts):
    #     D, k = solve(G, s, greed=False, max_step=50)
    #     assert is_valid_solution(D, G, s, k)

    #     Dg, kg = solve(G, s, greed=True, max_step=60)
    #     assert is_valid_solution(Dg, G, s, kg)
    #     careful = calculate_happiness(D ,G)
    #     greedy = calculate_happiness(Dg ,G)
    #     if careful > max_c:
    #         max_c = careful
    #         max_D = D

    #     if greedy > max_g:
    #         max_g = greedy
    #         max_Dg = Dg

    # if max_c >= max_g:
    #     print("Total Happiness: {}".format(max_c))
    #     # write_output_file(D, 'new_outputs/small-1.out')

    # else:
    #     print("Total Happiness: {}".format(max_g))
    #     # write_output_file(Dg, 'new_outputs/small-1.out')

# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('data/inputs/medium?*.in')
#     for input_path in inputs:
#         output_path = 'data/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path)


#         D, k = solve(G, s, greed=False, max_step=50)
#         assert is_valid_solution(D, G, s, k)

#         Dg, kg = solve(G, s, greed=True, max_step=60)
#         assert is_valid_solution(Dg, G, s, kg)

#         careful = calculate_happiness(D ,G)
#         greedy = calculate_happiness(Dg ,G)

#         if careful >= greedy:
#             write_output_file(D, output_path)

#         else:
#             write_output_file(Dg, output_path)

# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'new_ outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         happiness = calculate_happiness(D, G)
#         write_output_file(D, output_path)