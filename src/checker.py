import itertools
import numpy as np
import tqdm
from tqdm import tqdm



def fill_matrix(file):
    f = open(file, "r")
    n_students = int(next(f))
    s_max = float(next(f))
    H, S = np.zeros((n_students, n_students)), np.zeros((n_students, n_students))
    for line in f:
        val = line.split()
        r, c, h, s = int(val[0]), int(val[1]), float(val[2]), float(val[3])
        H[r][c], H[c][r] = h, h
        S[r][c], S[c][r] = s, s
    return H, S, n_students, s_max

#limited to roughly same room sizes, else "intractable" to enumerate all balls/bins permutations
def compute_optimal(n_rooms, s_max, H, S):
    best_score = 0
    best_assign = []
    room_budget = s_max/n_rooms
    room_size = n_students//n_rooms
    for perm in tqdm(itertools.permutations(np.arange(n_students))):
        perm_happy = 0
        perm_stress = 0
        assign = []
        for i in range(0, n_students, room_size):
            invalid_room = False
            room_stress = 0
            room = perm[i:i+room_size]
            for comb in itertools.combinations(room, 2):
                perm_happy += H[comb[0], comb[1]]
                perm_stress += S[comb[0], comb[1]]
                room_stress += S[comb[0], comb[1]]
            if room_stress > room_budget:
                invalid_room = True
                break
            assign += [room]
        if not invalid_room and perm_stress <= s_max:
            if perm_happy > best_score:
                best_assign = assign
                best_score = perm_happy
    return best_assign, best_score
                
def check_assignment(assign, s_max, n_rooms, H, S):
    perm_happy = 0
    perm_stress = 0
    room_budget = s_max/n_rooms

    for room in assign:
        room_stress = 0
        for comb in itertools.combinations(room, 2):
            perm_happy += H[comb[0], comb[1]]
            perm_stress += S[comb[0], comb[1]]
            room_stress += S[comb[0], comb[1]]
            if room_stress > room_budget:
                return False
    # return perm_happy, perm_stress
    return perm_happy
        
    

if __name__=="__main__":
    n_students = 10
    H, S, n_students, s_max = fill_matrix("input10.txt")
    compute_optimal(4, s_max, H, S)
    check_assignment([[0, 2, 4, 8], [6, 5, 4], [1, 9], [1]], s_max, 4, H, S)


