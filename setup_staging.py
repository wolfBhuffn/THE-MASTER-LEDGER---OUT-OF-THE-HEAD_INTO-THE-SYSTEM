import glob 
import os 

def
get_unprocessed_notes(staging_dir="05_Handoff_Staging"): 
    """Scans staging directory for Markdown notes.""" 
    pattern = os.path.join(staging_dir, "task_*.md") 
    notes = glob.glob(pattern) return sorted(notes) 
    
    if __name__ == "__main__": 
    pending = get_unprocessed_notes()
    print(f"Found {len(pending)} pending note(s) in staging.")