import unittest
import subprocess
import shutil
from pathlib import Path

import watchdog_listener

BASE_DIR = Path(__file__).resolve().parent
STAGING_DIR = BASE_DIR / "05_Handoff_Staging"
OUTBOX_DIR = STAGING_DIR / "Outbox_To_Boss"
APPROVED_DIR = STAGING_DIR / "Approved_Ready_To_Deploy"
REVISIONS_DIR = STAGING_DIR / "Revisions_Requested"
REPORT_PATH = STAGING_DIR / "MASTER_LEDGER_REPORT.md"


class TestMasterLedgerPipeline(unittest.TestCase):
    """Automated test suite for the Master Ledger Handoff pipeline."""

    def setUp(self):
        """Ensure staging directories exist and are clean before each test."""
        OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
        APPROVED_DIR.mkdir(parents=True, exist_ok=True)
        REVISIONS_DIR.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        """Clean up test artifacts after each run."""
        for directory in [OUTBOX_DIR, APPROVED_DIR, REVISIONS_DIR]:
            for md_file in directory.glob("test_*.md"):
                md_file.unlink(missing_ok=True)

    def test_boss_review_approval(self):
        """Test that boss_review.py successfully evaluates and approves a test packet."""
        test_packet = OUTBOX_DIR / "test_packet_approve.md"
        test_packet.write_text("# Unit Test Packet\nTesting approval execution flow.")

        script_path = BASE_DIR / "boss_review.py"
        result = subprocess.run(
            ["python3", str(script_path), "--packet", str(test_packet), "--decision", "APPROVE", "--notes", "Test approval."],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"Boss review approval failed: {result.stderr}")
        expected_path = APPROVED_DIR / "test_packet_approve.md"
        self.assertTrue(expected_path.exists(), "Packet was not moved to Approved_Ready_To_Deploy")
        expected_path.unlink(missing_ok=True)

    def test_boss_review_rejection(self):
        """Test that boss_review.py correctly routes rejected packets to Revisions_Requested."""
        test_packet = OUTBOX_DIR / "test_packet_reject.md"
        test_packet.write_text("# Unit Test Packet\nTesting rejection execution flow.")

        script_path = BASE_DIR / "boss_review.py"
        result = subprocess.run(
            ["python3", str(script_path), "--packet", str(test_packet), "--decision", "REJECT", "--notes", "Needs changes."],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"Boss review rejection failed: {result.stderr}")
        expected_path = REVISIONS_DIR / "test_packet_reject.md"
        self.assertTrue(expected_path.exists(), "Packet was not moved to Revisions_Requested")
        expected_path.unlink(missing_ok=True)

    def test_master_ledger_report_generation(self):
        """Test that master_ledger.py successfully compiles the status report."""
        ledger_script = BASE_DIR / "master_ledger.py"
        if not ledger_script.exists():
            self.skipTest("master_ledger.py not found.")

        result = subprocess.run(
            ["python3", str(ledger_script)],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"Ledger compilation failed: {result.stderr}")
        self.assertTrue(REPORT_PATH.exists(), "MASTER_LEDGER_REPORT.md was not generated.")

    def test_watchdog_folder_flattening(self):
        """Test that the pipeline detects, flattens, and processes nested Apple Notes folder bundles."""
        fake_bundle = OUTBOX_DIR / "Mock_iPhone_Note_Folder"
        fake_bundle.mkdir(exist_ok=True)
        
        nested_md = fake_bundle / "test_note_packet.md"
        nested_md.write_text("# Nested iPhone Note\nTesting programmatic folder extraction.")

        watchdog_listener.process_and_flatten_outbox()

        approved_target = APPROVED_DIR / "test_note_packet.md"
        self.assertTrue(approved_target.exists(), "Nested folder bundle packet was not processed and moved.")
        
        approved_target.unlink(missing_ok=True)
        if fake_bundle.exists():
            shutil.rmtree(fake_bundle)


if __name__ == "__main__":
    unittest.main()



    #   Run your test suite:
    #   python3 test_pipeline.py
