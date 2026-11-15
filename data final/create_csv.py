import os
import glob
import pandas as pd

NUMBER_OF_PARTICIPANTS = 7
LINES_PER_TECHNIQUE = 240
TECHNIQUES = 3
EXPECTED_LINES_PER_PARTICIPANT = LINES_PER_TECHNIQUE * TECHNIQUES # 720 lines
TOTAL_EXPECTED_LINES = NUMBER_OF_PARTICIPANTS * EXPECTED_LINES_PER_PARTICIPANT # 5040 lines
# -----------------------

def create_master_dataset():
    print("🔍 Scanning for participant files...")
    
    search_pattern = os.path.join('.', '**', 'merged_user_*.csv')
    matched_files = glob.glob(search_pattern, recursive=True)
    
    if not matched_files:
        print("❌ Error: No 'merged_user_X.csv' files found in any subfolders.")
        return

    print(f"📁 Found {len(matched_files)} merged participant files.\n")
    
    dataframes = []
    actual_total_lines = 0
    participants_found = 0
    warnings = []

    # Read and validate each file
    for file in matched_files:
        df = pd.read_csv(file)
        lines = len(df)
        user_id = df['User'].iloc[0] if not df.empty else "Unknown"
        
        print(f"  -> Reading User {user_id} ({os.path.basename(file)}): {lines} lines")
        
        # Individual Security Check
        if lines != EXPECTED_LINES_PER_PARTICIPANT:
            warnings.append(f"User {user_id} has {lines} lines (Expected: {EXPECTED_LINES_PER_PARTICIPANT})")
            
        dataframes.append(df)
        actual_total_lines += lines
        participants_found += 1

    # Merge into one massive dataframe
    master_df = pd.concat(dataframes, ignore_index=True)
    
    # Save the file to the current directory (data_raw)
    output_path = 'data.csv'
    master_df.to_csv(output_path, index=False)
    
    # --- FINAL SECURITY CHECKS ---
    print("\n" + "="*40)
    print("🛡️  FINAL SECURITY CHECKS")
    print("="*40)
    
    # Check 1: Participant Count
    if participants_found == NUMBER_OF_PARTICIPANTS:
        print(f"✅ Participant Count: Perfect ({participants_found}/{NUMBER_OF_PARTICIPANTS})")
    else:
        print(f"❌ Participant Count: Mismatch! Found {participants_found}, Expected {NUMBER_OF_PARTICIPANTS}")
        
    # Check 2: Total Lines Count
    if actual_total_lines == TOTAL_EXPECTED_LINES:
        print(f"✅ Total Data Rows: Perfect ({actual_total_lines}/{TOTAL_EXPECTED_LINES})")
    else:
        print(f"❌ Total Data Rows: Mismatch! Found {actual_total_lines}, Expected {TOTAL_EXPECTED_LINES}")
        
    # Display individual warnings if any
    if warnings:
        print("\n⚠️  WARNINGS:")
        for w in warnings:
            print(f"  - {w}")
            
    print("="*40)
    
    if participants_found == NUMBER_OF_PARTICIPANTS and actual_total_lines == TOTAL_EXPECTED_LINES:
        print("\n🎉 SUCCESS! The dataset is flawless.")
        print("📊 'data.csv' has been generated and is officially READY FOR RSTUDIO! 🚀\n")
    else:
        print("\n⚠️ 'data.csv' was created, but please review the security warnings above before taking it to R.\n")

if __name__ == "__main__":
    create_master_dataset()