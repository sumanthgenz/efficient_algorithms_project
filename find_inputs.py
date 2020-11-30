import random
import glob
import json
import filecmp 


if __name__ == "__main__":
    targets = ["proj-inputs/50.in", "proj-inputs/20.in", "proj-inputs/10.in"]
    matches = []
    for path in glob.glob('inputs/*'): 
        for t in targets:
            if filecmp.cmp(t, path): 
                matches.append((t, path))

    with open('found_inputs.json', 'w') as f:
        f.write(json.dumps(matches))