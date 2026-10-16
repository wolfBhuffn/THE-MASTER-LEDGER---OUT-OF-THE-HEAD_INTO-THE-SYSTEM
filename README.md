# The Master Ledger — Out of the Head, Into the System

A multi-agent automation pipeline designed to capture tasks, route them through specialized agent channels, validate output, and log every execution step into a structured system.

---

## 🏗 System Architecture

```mermaid
graph TD
    A[Task Input / Manual Entry] --> B[setup_staging.py]
    B --> C[create_packet.py]
    C --> D[Handoff Packet Generated]
    D --> E[Boss Agent / Router]
    E --> F[Specialized AI Agents / +CLAUDE]
    F --> G[Visual Inspector / Validation]
    G --> H[send_packet_email.py]
    H --> I[Master Ledger Logged]
