import sys
import random
import math
import csv
import argparse


LARGEUR = 1024
HAUTEUR = 800
MARGIN = 50 

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)



def generate_targets(n_targets, size, min_spacing):
    
    targets = []
    attempts = 0
    max_attempts = n_targets * 1000 

    while len(targets) < n_targets and attempts < max_attempts:

        x = random.randint(MARGIN, LARGEUR - MARGIN)
        y = random.randint(MARGIN, HAUTEUR - MARGIN)
        collision = False
        
        for t in targets:
            tx, ty, t_id = t
            dist = distance(x, y, tx, ty)
            
            if dist < (size + min_spacing):
                collision = True
                break
        
        if not collision:
            targets.append((x, y, len(targets)))
        
        
        attempts += 1

    if len(targets) < n_targets:
        print(f"Attention: Seulement {len(targets)} cibles générées (manque de place ?)")
        
    return targets






def save_csv(targets, filename_targets, filename_sequence, n_trials=20):
    
    with open(filename_targets, 'w', newline='') as f:
        writer = csv.writer(f)
        for t in targets:
            writer.writerow([t[2], t[0], t[1]]) 
            
    print(f"Fichier cibles généré")

    all_ids = [t[2] for t in targets]
    
    random.shuffle(all_ids)
    
    sequence = all_ids[:n_trials]
    
    with open(filename_sequence, 'w', newline='') as f:
        writer = csv.writer(f)
        for target_id in sequence:
            writer.writerow([target_id])
            
    print(f"Fichier séquence généré")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Générateur de cibles aléatoires")
    parser.add_argument("-n", "--number", type=int, required=True, help="Nombre de cibles")
    parser.add_argument("-s", "--size", type=int, required=True, help="Taille des cibles (en pixels)")
    parser.add_argument("-m", "--min_space", type=int, default=10, help="Espacement minimal entre cibles")
    
    args = parser.parse_args()
    
    f_targets = f"targets_{args.number}_{args.size}.csv"
    f_sequence = f"sequence_{args.number}_{args.size}.csv"
    
    targets_list = generate_targets(args.number, args.size, args.min_space)
    
    save_csv(targets_list, f_targets, f_sequence)