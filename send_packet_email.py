import smtplib
from email.message import EmailMessage
from pathlib import Path
import os

def dispatch_handoff_packet(filename: str, sender_tag: str, app_password: str = None):
    """
    Sends the generated markdown handoff packet via Gmail SMTP 
    using the agent's dedicated plus-address.
    """
    # Pull app password from environment if not explicitly provided
    if not app_password:
        app_password = os.environ.get("GMAIL_APP_PASSWORD")
        
    packet_path = Path("05_Handoff_Staging/Outbox_To_Boss") / filename
    if not packet_path.exists():
        # Check approved or revisions if it was already moved
        packet_path = Path("05_Handoff_Staging/Approved_Ready_To_Deploy") / filename
    
    if not packet_path.exists():
        print(f"Error: Packet '{filename}' could not be found in staging folders.")
        return

    # Email configurations
    sender_email = f"kwamelockley.91+{sender_tag}@gmail.com"
    boss_email = "kwamelockley.91+boss@gmail.com"
    is_github = os.getenv("GITHUB_ACTIONS") == "true"
    runner_tag = "[Cloud Runner / iOS]" if is_github else "[macOS Local Watchdog]"
    msg = EmailMessage()
    msg['Subject'] = f"{runner_tag} HANDOFF PACKET SUBMISSION: {filename}"
    msg['From'] = sender_email
    msg['To'] = boss_email
    
    # Attach the markdown packet content as the body
    packet_content = packet_path.read_text()
    msg.set_content(packet_content)
    
    # Fallback to simulation if no password is configured yet
    if not app_password:
        print(f"[NOTE] No GMAIL_APP_PASSWORD found. Email dispatch simulation passed for {sender_email} -> {boss_email}.")
        return

    try:
        # Connecting to Gmail SMTP server securely
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print(f"Success: Handoff packet email sent live from {sender_email} to {boss_email}!")
    except Exception as e:
        print(f"[ERROR] Live email dispatch failed: {e}")
        raise e

if __name__ == "__main__":
    import sys
    # Allow passing filename and tag via CLI arguments, with defaults for testing
    filename = sys.argv[1] if len(sys.argv) > 1 else "test_note_packet.md"
    sender_tag = sys.argv[2] if len(sys.argv) > 2 else "pinescript"
    
    dispatch_handoff_packet(filename=filename, sender_tag=sender_tag)
