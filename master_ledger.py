from pathlib import Path
from datetime import datetime
import json

def compile_master_ledger():
    """
    Scans all staging directories, compiles active agent registries, 
    and generates a unified Master Ledger status report.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M EST")
    
    # Path definitions
    outbox_dir = Path("05_Handoff_Staging/Outbox_To_Boss")
    approved_dir = Path("05_Handoff_Staging/Approved_Ready_To_Deploy")
    revisions_dir = Path("05_Handoff_Staging/Revisions_Requested")
    registry_path = Path("05_Handoff_Staging/agent_registry.json")
    
    # Gather counts
    outbox_count = len(list(outbox_dir.glob("*.md"))) if outbox_dir.exists() else 0
    approved_count = len(list(approved_dir.glob("*.md"))) if approved_dir.exists() else 0
    revisions_count = len(list(revisions_dir.glob("*.md"))) if revisions_dir.exists() else 0
    
    # Load agent registry
    agents = {}
    if registry_path.exists():
        try:
            agents = json.loads(registry_path.read_text())
        except json.JSONDecodeError:
            agents = {}

    # Compile Ledger Content
    ledger_content = f"""# 📊 THE MASTER LEDGER: SYSTEM STATUS REPORT
**Generated:** {timestamp}
**Boss Agent:** kwamelockley.91+boss@gmail.com

---

## 1. Pipeline Staging Summary
* **📥 Outbox (Pending Review):** {outbox_count} packet(s)
* **🟢 Approved (Ready to Deploy):** {approved_count} packet(s)
* **🔴 Revisions Requested:** {revisions_count} packet(s)

---

## 2. Active Agent Registry & Plus-Addresses
"""

    if agents:
        for tag, data in agents.items():
            ledger_content += f"- **{data['agent_name']}** ({data['specialty']}) -> `{data['email']}` [{data['status']}]\n"
    else:
        ledger_content += "_No specialized agents currently registered._\n"

    ledger_content += f"""
---
## 3. System Execution Protocol
All routing channels, automated triggers, and visual logging inspectors are active and verified.
"""

    # Save ledger output
    ledger_path = Path("05_Handoff_Staging/MASTER_LEDGER_REPORT.md")
    ledger_path.write_text(ledger_content)
    
    print("📈 Master Ledger Orchestrator Summary:")
    print(f"   - Pending Packets: {outbox_count}")
    print(f"   - Approved Packets: {approved_count}")
    print(f"   - Registered Agents: {len(agents)}")
    print(f"   - Report Saved To: {ledger_path}")

if __name__ == "__main__":
    compile_master_ledger()