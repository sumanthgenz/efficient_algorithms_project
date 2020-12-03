import random
import glob
import json
import filecmp 


if __name__ == "__main__":
    targets = ["data/proj-inputs/50.in", "data/proj-inputs/20.in", "data/proj-inputs/10.in"]
    matches = []
    for path in glob.glob('data/inputs/*'): 
        for t in targets:
            if filecmp.cmp(t, path): 
                matches.append((t, path))

    with open('data/found_inputs.json', 'w') as f:
        f.write(json.dumps(matches))

    #python3 find_inputs.py data/found_inputs.json