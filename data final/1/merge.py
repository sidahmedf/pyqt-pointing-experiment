import os
import pandas as pd
import glob

def merge_participant_data(folder_path='.'):
    # 1. Read the correct User ID from Id.txt
    id_file_path = os.path.join(folder_path, 'Id.txt')
    try:
        with open(id_file_path, 'r') as f:
            # Read first line, strip whitespace, get the very first character
            first_char = f.readline().strip()[0]
            new_user_id = int(first_char)
            print(f"Found User ID in Id.txt: {new_user_id}")
    except FileNotFoundError:
        print("Error: Id.txt not found in the folder.")
        return
    except (IndexError, ValueError):
        print("Error: Id.txt is empty or does not contain a valid number at the start.")
        return

    # 2. Identify the CSV files in the specific order requested
    # Note: This assumes you have already removed the 5KB practice files from the folder!
    file_patterns = ['*Normal*.csv', '*Bubble*.csv', '*Rope*.csv']
    files_to_merge = []
    
    for pattern in file_patterns:
        matches = glob.glob(os.path.join(folder_path, pattern))
        if matches:
            # Grab the first match (assuming one valid file per technique in the folder)
            files_to_merge.append(matches[0])
        else:
            print(f"Warning: No file matching '{pattern}' found in the folder.")

    if not files_to_merge:
        print("No CSV files found to merge. Exiting.")
        return

    # 3. Read, update, and merge the datasets
    dataframes = []
    total_original_rows = 0
    
    for file in files_to_merge:
        # Read the CSV
        df = pd.read_csv(file)
        
        # Count original rows for the security check
        original_rows = len(df)
        total_original_rows += original_rows
        
        # 4. Overwrite the User column with the ID from Id.txt
        df['User'] = new_user_id
        
        dataframes.append(df)
        print(f"Loaded {os.path.basename(file)}: {original_rows} rows.")

    # Concatenate all dataframes in the exact order they were loaded
    merged_df = pd.concat(dataframes, ignore_index=True)
    
    # 5. Security Check: Verify no lines were lost
    merged_rows = len(merged_df)
    print("\n--- Security Check ---")
    print(f"Sum of rows from individual files: {total_original_rows}")
    print(f"Total rows in merged dataset:      {merged_rows}")
    
    if total_original_rows == merged_rows:
        print("Check Passed: No lines were lost during the merge! ✓")
    else:
        print("WARNING: Row count mismatch! Some lines may have been lost or duplicated. ❌")

    # 6. Save the final compiled file
    output_filename = os.path.join(folder_path, f"merged_user_{new_user_id}.csv")
    merged_df.to_csv(output_filename, index=False)
    print(f"\nSuccessfully saved merged data to: {os.path.basename(output_filename)}")

if __name__ == "__main__":
    # Execute the function on the current directory
    merge_participant_data()