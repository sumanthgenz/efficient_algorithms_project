import itertools
import numpy as np
import tqdm
from tqdm import tqdm

n_students = 10
h_matrix, s_matrix = np.zeros((n_students, n_students)), np.zeros((n_students, n_students))
s_max = 1000

def fill_matrix(file):
    f = open(file, "r")
    for line in f:
        val = line.split()
        r, c, h, s = int(val[0]), int(val[1]), float(val[2]), float(val[3])
        h_matrix[r][c], h_matrix[c][r] = h, h
        s_matrix[r][c], s_matrix[c][r] = s, s


#faulty
def compute_optimal(n_rooms):
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
                perm_happy += h_matrix[comb[0], comb[1]]
                perm_stress += s_matrix[comb[0], comb[1]]
                room_stress += s_matrix[comb[0], comb[1]]
            if room_stress > room_budget:
                invalid_room = True
                break
            assign += [room]
        if not invalid_room and perm_stress <= s_max:
            if perm_happy > best_score:
                best_assign = assign
                best_score = perm_happy
    return best_assign, best_score
                
def check_assignment(assign, n_rooms):
    perm_happy = 0
    perm_stress = 0
    room_budget = s_max/n_rooms

    for room in assign:
        room_stress = 0
        for comb in itertools.combinations(room, 2):
            perm_happy += h_matrix[comb[0], comb[1]]
            perm_stress += s_matrix[comb[0], comb[1]]
            room_stress += s_matrix[comb[0], comb[1]]
            if room_stress > room_budget:
                return False
    return perm_happy, perm_stress
        
    

if __name__=="__main__":
    fill_matrix("input10.txt")
    compute_optimal(4)
    check_assignment([[0, 2, 4, 8], [6, 5, 4], [1, 9], [1]], 4)


