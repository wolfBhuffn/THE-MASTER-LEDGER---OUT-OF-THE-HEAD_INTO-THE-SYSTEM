from pathlib import Path
from datetime import datetime

def generate_handoff_packet(project_name: str, sender_agent: str, tag: str):
    # Target directory matching our architecture
    outbox_dir = Path("05_Handoff_Staging/Outbox_To_Boss")
    outbox_dir.mkdir(parents=True, exist_ok=True)
    
    # Format current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d | %H:%M EST")
    date_str = datetime.now().strftime("%Y%m%d")
    
    # Filename format
    filename = f"{date_str}_{project_name.upper()}_Handoff.md"
    file_path = outbox_dir / filename
    
    # Template content matching your master blueprint
    packet_content = f"""📦 HANDOFF PACKET: {project_name.upper()}

1. Metadata & Sender Verification
Sender Agent: {sender_agent} (kwamelockley.91+{tag}@gmail.com)
Recipient: Boss Agent (kwamelockley.91+boss@gmail.com) / User
Timestamp: {timestamp}
Status: 🟡 Pending Boss Review | 🟢 Approved | 🔴 Revisions Required
Priority: [ Low | Medium | High | Critical ]

2. Executive Summary
Objective: Brief 2–3 sentence overview of what this packet delivers and how it directly supports the core objective.
Primary Deliverable Link: [Insert Google Drive / Sheet / Doc / Notebook Link]
Target Execution Date: YYYY-MM-DD

3. Work Completed & Output Breakdown
Completed Milestones:
[Milestone 1 Details & Verification]
[Milestone 2 Details & Verification]

Associated Workspace Assets:
📊 Google Sheet: [Link]
📝 Notebook / Document: [Link]
📅 Calendar Logged: [Yes/No - Link to Event]
📂 Drive Folder: [Link to Active Project Subfolder]

4. Visual Evidence & Source Artifacts (Screenshot Logs)
Captured Visual Proof (via iOS Capture Engine):
📸 Screenshot Asset 1: [Drive Link / Filename: {date_str}_{project_name}_01.png]
📸 Screenshot Asset 2: [Drive Link / Filename: {date_str}_{project_name}_02.png]

Visual Inspector Notes:
OCR / Data Summary: [Summary of charts, table data, or UI proof extracted by Visual Inspector Agent kwamelockley.91+vision@gmail.com]

5. Audit & Risk Analysis (Boss Agent Checklist)
Edge Cases & Failure Points Identified:
[Potential failure point 1 or technical risk]
[Data anomaly or dependency requirement]

Verification Steps Completed:
[ ] Output checked against user core objective guidelines.
[ ] Formatting, hyperlinks, and folder destinations validated.
[ ] Screenshots attached and matched to deliverable claim.

6. Next Action Items & Execution Protocol
Immediate Step: [Action needed from Boss Agent / User]
Automated Trigger: [Downstream workflow or script execution]
Delegation / Provisioning: [Does this require the Hiring Manager Agent kwamelockley.91+hiringmanager@gmail.com to spawn a new agent?]

7. Sign-off & Decision Log
====================================================================
BOSS AGENT AUDIT LOG:
[ ] APPROVED – Move to 📁 05_Handoff_Staging/Approved_Ready_To_Deploy
[ ] REJECTED – Return to Sender with notes below

Notes: ___________________________________________________________
Signature: Boss Agent (kwamelockley.91+boss@gmail.com)
Date/Time: ___________________________

USER FINAL SIGN-OFF:
[ ] EXECUTE NOW
====================================================================
"""
    
    file_path.write_text(packet_content)
    print(f"Generated Handoff Packet: {file_path}")

if __name__ == "__main__":
    generate_handoff_packet(
        project_name="Master_Ledger_Setup", 
        sender_agent="PineScript Specialist", 
        tag="pinescript"
    )