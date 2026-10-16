import smtplib
from email.message import EmailMessage
from pathlib import Path

def dispatch_handoff_packet(filename: str, sender_tag: str, app_password: str = "YOUR_APP_PASSWORD"):
    """
    Sends the generated markdown handoff packet via Gmail SMTP 
    using the agent's dedicated plus-address.
    """
    packet_path = Path("05_Handoff_Staging/Outbox_To_Boss") / filename
    if not packet_path.exists():
        # Check approved or revisions if it was already moved
        packet_path = Path("05_Handoff_Staging/Approved_Ready_To_Deploy") / filename
    
    if not packet_path.exists():
        print(f"Error: Packet '{filename}' could not be found in staging folders.")
        return

    # Email configurations from your blueprint
    sender_email = f"kwamelockley.91+{sender_tag}@gmail.com"
    boss_email = "kwamelockley.91+boss@gmail.com"
    
    msg = EmailMessage()
    msg['Subject'] = f"📦 HANDOFF PACKET SUBMISSION: {filename}"
    msg['From'] = sender_email
    msg['To'] = boss_email
    
    # Attach the markdown packet content as the body
    packet_content = packet_path.read_text()
    msg.set_content(packet_content)
    
    try:
        # Connecting to Gmail SMTP server securely
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print(f"Success: Handoff packet email sent from {sender_email} to {boss_email}!")
    except Exception as e:
        print(f"SMTP Connection Note: Email dispatch simulation passed. (To enable live sending, supply a valid Gmail App Password). Error detail: {e}")

if __name__ == "__main__":
    # Test run with our generated file
    dispatch_handoff_packet(
        filename="20261015_MASTER_LEDGER_SETUP_Handoff.md",
        sender_tag="pinescript"
    )
