import os
from pathlib import Path
from importlib import import_module
from prefect.logging import get_logger
from prefect_github import GitHubCredentials
from prefect.runner.storage import GitRepository

# Configuration
FLOWS_DIR = "flows"
WORK_POOL_NAME = "DewDrop_Pool"
FLOW_FUNCTION_NAME = "flow_start" # Assumes each file defines a flow named `flow_start`
GITHUB_TOKEN = "github-token"

logger = get_logger()

def deploy_all_flows():
    flow_files = Path(FLOWS_DIR).glob("*.py")
    
    for flow_file in flow_files:
        module_path = flow_file.with_suffix("")  # Remove .py
        module_name = f"{FLOWS_DIR}.{module_path.name}"

        try:
            mod = import_module(module_name)
            flow_fn = getattr(mod, FLOW_FUNCTION_NAME)

            #logger.info(f"Deploying flow from {module_name}.{FLOW_FUNCTION_NAME}...")
            
            github_credentials = GitHubCredentials(token=GITHUB_TOKEN)
            
            logger.info(f"check: ./{FLOWS_DIR}/{module_path.name}.py:{FLOW_FUNCTION_NAME}")
            deployment = flow_fn.from_source(source=source, entrypoint=f"./{FLOWS_DIR}/{module_path.name}.py:{FLOW_FUNCTION_NAME}").deploy(
                name=f"{module_path.name}-deployment",
                work_pool_name=WORK_POOL_NAME,
                tags=["ci", module_path.name]
            )

            logger.info(f"✅ Deployed: {module_path.name}-deployment")
        except Exception as e:
            logger.error(f"❌ Failed to deploy flow from {module_name}: {e}")

if __name__ == "__main__":
    source = GitRepository(
        url="https://github.com/dewdrop28/test_prefect_deploy_1.git",
        credentials=GitHubCredentials.load(GITHUB_TOKEN)
    )

    deploy_all_flows()
