from pathlib import Path
from datetime import datetime

def process_packet(filename: str, decision: str, notes: str = ""):
    outbox = Path("05_Handoff_Staging/Outbox_To_Boss")
    approved_dir = Path("05_Handoff_Staging/Approved_Ready_To_Deploy")
    revisions_dir = Path("05_Handoff_Staging/Revisions_Requested")
    
    packet_path = outbox / filename
    if not packet_path.exists():
        print(f"Error: Packet '{filename}' not found in Outbox.")
        return

    content = packet_path.read_text()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M EST")
    
    # Update Status and Audit Log based on decision
    if decision.upper() == "APPROVE":
        content = content.replace(
            "Status: 🟡 Pending Boss Review | 🟢 Approved | 🔴 Revisions Required",
            "Status: 🟢 Approved"
        )
        content = content.replace(
            "[ ] APPROVED – Move to 📁 05_Handoff_Staging/Approved_Ready_To_Deploy",
            "[x] APPROVED – Move to 📁 05_Handoff_Staging/Approved_Ready_To_Deploy"
        )
        target_dir = approved_dir
    else:
        content = content.replace(
            "Status: 🟡 Pending Boss Review | 🟢 Approved | 🔴 Revisions Required",
            "Status: 🔴 Revisions Required"
        )
        content = content.replace(
            "[ ] REJECTED – Return to Sender with notes below",
            "[x] REJECTED – Return to Sender with notes below"
        )
        target_dir = revisions_dir

    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)

    # Fill in notes and signature
    content = content.replace("Notes: ___________________________________________________________", f"Notes: {notes}")
    content = content.replace("Date/Time: ___________________________", f"Date/Time: {timestamp}")
    
    packet_path.write_text(content)
    
    # Move file to the correct destination folder
    target_path = target_dir / filename
    packet_path.rename(target_path)
    print(f"Boss Agent Action: Packet successfully moved to {target_path}")

if __name__ == "__main__":
    process_packet(
        filename="20261015_MASTER_LEDGER_SETUP_Handoff.md",
        decision="APPROVE",
        notes="All workspace assets and metadata look solid. Ready for deployment."
    )
