import csv
import random
import time
import  os
import datetime
import sys
from PyQt5.QtWidgets import QApplication

class XPManager:
    def __init__(self, setup_data, widget, main_window):
        
        self.user_id = setup_data['user_id']
        self.technique = setup_data['technique']
        self.repetitions = setup_data['repetitions'] 
        
        self.widget = widget
        self.main_window = main_window
        
        self.current_trial_index = -1
        self.error_count = 0
        self.trial_queue = []
        self.log_dir = "results"

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

        self.log_filename = os.path.join(self.log_dir, f"user_{self.user_id}_{self.technique}_{timestamp}.csv")
        self._init_log_file()
        
        self._generate_experiment_plan()
        
        self.next_trial()

    def _init_log_file(self):
        with open(self.log_filename, 'w', newline='') as f:
            writer = csv.writer(f)

            writer.writerow([
                "User", "Technique", "Density", "Size", "Repetition", 
                "Target_ID", "Timestamp", "Errors", "Time_ms"
            ])

    def _generate_experiment_plan(self):
        densities = [30, 90]
        sizes = [8,18]
        
        factors = []
        for d in densities:
            for s in sizes:
                factors.append((d, s))
        
        for rep in range(1, self.repetitions + 1):

            random.shuffle(factors)
            
            for (dens, size) in factors:

                seq_filename = f"sequence_{dens}_{size}.csv"
                try:
                    with open(seq_filename, 'r') as f:
                        reader = csv.reader(f)
                        target_sequence = [int(row[0]) for row in reader]
                except FileNotFoundError:
                    print(f"ERREUR: Fichier {seq_filename} manquant ! Avez-vous lancé generate_files.py ?")
                    target_sequence = list(range(20)) 

                for i, target_id in enumerate(target_sequence):
                    trial = {
                        "density": dens,
                        "size": size,
                        "repetition": rep,
                        "target_order": i + 1, 
                        "target_id": target_id
                    }
                    self.trial_queue.append(trial)

    def next_trial(self):
        self.current_trial_index += 1
        
        if self.current_trial_index >= len(self.trial_queue):
            print("Expérience terminée ! Merci.")
            self.main_window.close()
            return

        trial = self.trial_queue[self.current_trial_index]
        
        new_condition = False
        if self.current_trial_index == 0:
            new_condition = True
        else:
            prev = self.trial_queue[self.current_trial_index - 1]
            if prev['density'] != trial['density'] or prev['size'] != trial['size']:
                new_condition = True
        
        if new_condition:
            print(f"--- Changement de Condition: D={trial['density']}, S={trial['size']} ---")

            target_file = f"targets_{trial['density']}_{trial['size']}.csv"
            self.widget.load_scenario(target_file, trial['size'])


        self.widget.set_active_target(trial['target_id'])
        

        self.error_count = 0
        self.start_time = time.time() * 1000

    def handle_success(self):
        end_time = time.time() * 1000
        duration = end_time - self.start_time
        
        trial = self.trial_queue[self.current_trial_index]
        
        with open(self.log_filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                self.user_id,
                self.technique,
                trial['density'],
                trial['size'],
                trial['repetition'],
                trial['target_id'], 
                time.time(), 
                self.error_count,
                round(duration, 2)
            ])
            
        print(f"Essai réussi en {round(duration)}ms (Erreurs: {self.error_count})")
        
        self.next_trial()

    def handle_error(self):
        self.error_count += 1
        print("Erreur !")