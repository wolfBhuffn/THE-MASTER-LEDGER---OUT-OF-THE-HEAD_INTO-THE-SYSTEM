import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent
STAGING_DIR = BASE_DIR / "05_Handoff_Staging"
OUTBOX_DIR = STAGING_DIR / "Outbox_To_Boss"
BOSS_REVIEW_SCRIPT = BASE_DIR / "boss_review.py"
EMAIL_SCRIPT = BASE_DIR / "send_packet_email.py"
LEDGER_SCRIPT = BASE_DIR / "master_ledger.py"


def process_and_flatten_outbox():
    """Scans Outbox_To_Boss (and subfolders) for any .md files ready for processing."""
    if not OUTBOX_DIR.exists():
        return

    # Find all .md files in Outbox root or nested subdirectories (ignoring hidden files)
    all_files = list(OUTBOX_DIR.glob("**/*.md")) + list(OUTBOX_DIR.glob("*.md"))
    valid_packets = [f for f in set(all_files) if not f.name.startswith(".")]

    for file_path in valid_packets:
        # If nested inside a subfolder created by Apple Notes, flatten it to Outbox root
        if file_path.parent != OUTBOX_DIR:
            target_path = OUTBOX_DIR / file_path.name
            try:
                file_path.rename(target_path)
                file_path = target_path
                print(f"[ACTION] Extracted mobile drop '{file_path.name}' to main Outbox root.")
            except Exception as e:
                print(f"[WARN] Could not move {file_path.name}: {e}")
                continue

        print(f"\n[EVENT] Processing packet: {file_path.name}")
        execute_pipeline(file_path)


def execute_pipeline(packet_path: Path):
    print(f"[ACTION] 1. Triggering Boss Review for: {packet_path.name}...")
    try:
        # Step 1: Run Boss Review
        subprocess.run(
            ["python3", str(BOSS_REVIEW_SCRIPT), "--packet", str(packet_path), "--decision", "APPROVE"],
            check=True
        )
        print(f"[SUCCESS] Boss Review approved and routed.")

        # Step 2: Dispatch Email Notification
        if EMAIL_SCRIPT.exists():
            print(f"[ACTION] 2. Dispatches notification email...")
            subprocess.run(["python3", str(EMAIL_SCRIPT)], check=False)

        # Step 3: Compile Master Ledger Status Report
        if LEDGER_SCRIPT.exists():
            print(f"[ACTION] 3. Updating Master Ledger status report...")
            subprocess.run(["python3", str(LEDGER_SCRIPT)], check=False)
            print(f"[SUCCESS] Master Ledger report updated successfully.")

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Pipeline execution failed for {packet_path.name}: {e}")


class PacketHandler(FileSystemEventHandler):
    """Monitors Outbox_To_Boss and triggers processing on any file system change."""

    def on_any_event(self, event):
        # Trigger scan on creation, modification, or move events (e.g. iCloud download completion)
        if event.event_type in ["created", "modified", "moved"]:
            time.sleep(1) # Allow sync completion
            process_and_flatten_outbox()


def start_watcher():
    if not OUTBOX_DIR.exists():
        print(f"[ERROR] Directory not found: {OUTBOX_DIR}")
        return

    # Run an initial scan immediately on startup to catch existing mobile drops
    print("\n🔍 Running initial scan for pending iCloud drops...")
    process_and_flatten_outbox()

    event_handler = PacketHandler()
    observer = Observer()
    observer.schedule(event_handler, path=str(OUTBOX_DIR), recursive=True)
    
    print("=" * 60)
    print(" 👁️  MASTER LEDGER ICLOUD-AWARE WATCHDOG ONLINE")
    print(f" Monitoring: {OUTBOX_DIR}")
    print(" Press Ctrl+C to stop.")
    print("=" * 60)

    observer.start()
    try:
        while True:
            time.sleep(2)
            # Periodic pulse check for background iCloud file syncs
            process_and_flatten_outbox()
    except KeyboardInterrupt:
        observer.stop()
        print("\n[STOPPED] Watchdog listener shut down safely.")
    
    observer.join()


if __name__ == "__main__":
    start_watcher()


# RUN:
# python3 watchdog_listener.py
