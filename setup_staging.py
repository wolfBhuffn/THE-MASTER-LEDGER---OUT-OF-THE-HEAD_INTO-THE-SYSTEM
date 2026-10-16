from pathlib import Path

def setup_handoff_staging():
    # Define the base directory and subdirectories
    base_dir = Path("05_Handoff_Staging")
    subdirs = [
        base_dir / "Outbox_To_Boss",
        base_dir / "Approved_Ready_To_Deploy",
        base_dir / "Revisions_Requested"
    ]
    
    # Create directories if they don't already exist
    for folder in subdirs:
        folder.mkdir(parents=True, exist_ok=True)
        print(f"Directory ready: {folder}")

if __name__ == "__main__":
    setup_handoff_staging()
