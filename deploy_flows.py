import os
from pathlib import Path
from importlib import import_module
from prefect.logging import get_logger

# Configuration
FLOWS_DIR = "flows"
WORK_POOL_NAME = "DewDrop_Pool"
FLOW_FUNCTION_NAME = "flow_start"

logger = get_logger()

def deploy_all_flows():
    flow_files = Path(FLOWS_DIR).glob("*.py")

    for flow_file in flow_files:
        module_path = flow_file.with_suffix("")  # Remove .py
        module_name = f"{FLOWS_DIR}.{module_path.name}"

        try:
            mod = import_module(module_name)
            flow_fn = getattr(mod, FLOW_FUNCTION_NAME)

            logger.info(f"Deploying flow from {module_name}.{FLOW_FUNCTION_NAME}...")

            deployment = flow_fn.deploy(
                name=f"{module_path.name}-deployment",
                work_pool_name=WORK_POOL_NAME,
                path=".",
                tags=["ci", module_path.name]
            )

            deployment.apply()

        except Exception as e:
            logger.error(f"Failed to deploy flow from {module_name}: {e}")

if __name__ == "__main__":
    deploy_all_flows()
