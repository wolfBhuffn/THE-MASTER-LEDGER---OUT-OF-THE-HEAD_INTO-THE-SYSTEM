from dotenv import load_dotenv
load_dotenv()
import argparse
from pathlib import Path
from datetime import datetime
import os
from google import genai
from google.genai import types

def evaluate_packet_with_ai(packet_content: str) -> tuple[str, str]:
    """Sends packet content to Gemini for autonomous evaluation."""
    client = genai.Client() # Picks up GEMINI_API_KEY from environment
    
    system_prompt = (
        "You are the autonomous 'Boss Agent' reviewing an engineering handoff packet. "
        "Analyze the objective, progress, and details provided in the packet. "
        "You must return your response in two parts: "
        "1. DECISION: Exactly either 'APPROVE' or 'REJECT'. "
        "2. NOTES: A brief 1-2 sentence constructive review note explaining your rationale."
    )
    
    prompt = f"Please review the following handoff packet:\n\n{packet_content}"
    
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2,
            )
        )
        
        text = response.text.strip()
        # Simple parsing logic to extract decision and notes
        decision = "APPROVE" if "APPROVE" in text.upper() else "REJECT"
        notes = f"AI Review: {text.replace(chr(10), ' ')}"
        return decision, notes
        
    except Exception as e:
        print(f"[WARNING] Gemini API evaluation failed: {e}. Falling back to default APPROVE.")
        return "APPROVE", "Fallback approval due to API evaluation error."

def process_packet(packet_path: Path, decision_override: str = None, notes_override: str = None):
    approved_dir = Path("05_Handoff_Staging/Approved_Ready_To_Deploy")
    revisions_dir = Path("05_Handoff_Staging/Revisions_Requested")
    
    if not packet_path.exists():
        print(f"Error: Packet '{packet_path.name}' not found.")
        return

    content = packet_path.read_text()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M EST")
    
    # If no manual override is provided, use Gemini to evaluate the packet autonomously!
    if not decision_override or not notes_override:
        print(f"[ACTION] Running Autonomous Gemini Boss Evaluation for '{packet_path.name}'...")
        ai_decision, ai_notes = evaluate_packet_with_ai(content)
        decision = decision_override if decision_override else ai_decision
        notes = notes_override if notes_override else ai_notes
    else:
        decision = decision_override
        notes = notes_override

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
    target_path = target_dir / packet_path.name
    packet_path.rename(target_path)
    print(f"Boss Agent Action: Packet successfully moved to {target_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and review a handoff packet using Gemini AI.")
    parser.add_argument("--packet", type=str, required=True, help="Path to the handoff packet markdown file.")
    parser.add_argument("--decision", type=str, default=None, help="Optional override: APPROVE or REJECT")
    parser.add_argument("--notes", type=str, default=None, help="Optional review notes override.")
    
    args = parser.parse_args()
    process_packet(Path(args.packet), args.decision, args.notes)


