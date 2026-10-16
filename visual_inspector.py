from pathlib import Path
from datetime import datetime

def attach_visual_evidence(filename: str, screenshot_name_1: str, screenshot_name_2: str, ocr_summary: str):
    # Look for the packet in Approved or Outbox
    approved_dir = Path("05_Handoff_Staging/Approved_Ready_To_Deploy")
    outbox_dir = Path("05_Handoff_Staging/Outbox_To_Boss")
    
    packet_path = approved_dir / filename
    if not packet_path.exists():
        packet_path = outbox_dir / filename
        
    if not packet_path.exists():
        print(f"Error: Packet '{filename}' not found.")
        return

    content = packet_path.read_text()
    
    # Format Section 4 with actual visual evidence logs
    old_section_4 = """4. Visual Evidence & Source Artifacts (Screenshot Logs)
Captured Visual Proof (via iOS Capture Engine):
📸 Screenshot Asset 1: [Drive Link / Filename: YYYYMMDD_Project_01.png]
📸 Screenshot Asset 2: [Drive Link / Filename: YYYYMMDD_Project_02.png]

Visual Inspector Notes:
OCR / Data Summary: [Summary of charts, table data, or UI proof extracted by Visual Inspector Agent kwamelockley.91+vision@gmail.com]"""

    new_section_4 = f"""4. Visual Evidence & Source Artifacts (Screenshot Logs)
Captured Visual Proof (via iOS Capture Engine):
📸 Screenshot Asset 1: [Drive Link / Filename: {screenshot_name_1}]
📸 Screenshot Asset 2: [Drive Link / Filename: {screenshot_name_2}]

Visual Inspector Notes (Verified by kwamelockley.91+vision@gmail.com):
OCR / Data Summary: {ocr_summary}"""

    if old_section_4 in content:
        content = content.replace(old_section_4, new_section_4)
        packet_path.write_text(content)
        print(f"Visual Inspector Success: Screenshot assets and OCR notes appended to {packet_path.name}")
    else:
        print("Note: Section 4 template structure already updated or customized.")

if __name__ == "__main__":
    # Test run injecting screenshot logs into our packet
    attach_visual_evidence(
        filename="20261015_MASTER_LEDGER_SETUP_Handoff.md",
        screenshot_name_1="20261015_MasterLedger_UI_01.png",
        screenshot_name_2="20261015_StagingFolders_02.png",
        ocr_summary="Confirmed directory paths [Outbox_To_Boss, Approved_Ready_To_Deploy, Revisions_Requested] active and verified in VS Code workspace."
    )
