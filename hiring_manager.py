from pathlib import Path
import json
from datetime import datetime

def provision_new_agent(agent_name: str, specialty: str, tag: str):
    """
    Provisions a new specialized agent, registers their plus-address, 
    and sets up their dedicated project directory workspace.
    """
    registry_path = Path("05_Handoff_Staging/agent_registry.json")
    
    # Load existing registry or create a new one
    registry = {}
    if registry_path.exists():
        try:
            registry = json.loads(registry_path.read_text())
        except json.JSONDecodeError:
            registry = {}
            
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M EST")
    
    # Register agent details matching your master email standard
    agent_email = f"kwamelockley.91+{tag}@gmail.com"
    registry[tag] = {
        "agent_name": agent_name,
        "specialty": specialty,
        "email": agent_email,
        "status": "Active & Provisioned",
        "provisioned_at": timestamp
    }
    
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(json.dumps(registry, indent=4))
    
    # Create a dedicated working directory for this agent
    agent_workspace = Path(f"02_Active_Projects/{agent_name.replace(' ', '_')}")
    agent_workspace.mkdir(parents=True, exist_ok=True)
    
    print(f"👔 Hiring Manager Action:")
    print(f"   - Spawned Agent: {agent_name} [{specialty}]")
    print(f"   - Assigned Alias: {agent_email}")
    print(f"   - Workspace Created: {agent_workspace}")
    print(f"   - Registry Updated: {registry_path}")

if __name__ == "__main__":
    # Test provisioning a new agent from Section 6 delegation request
    provision_new_agent(
        agent_name="Visual Inspector Agent",
        specialty="iOS Screenshot OCR & UI Verification",
        tag="vision"
    )