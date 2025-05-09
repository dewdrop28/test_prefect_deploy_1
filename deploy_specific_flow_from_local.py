import os
import argparse
from pathlib import Path
from importlib import import_module
from prefect.logging import get_logger

logger = get_logger()

def deploy_flow(deployment_name, flows_dir, flow_file_name, flow_function_name, work_pool_name):        
    
        module_path = Path(f"{flow_file_name}").stem  # Remove .py
        module_name = f"{flows_dir}.{module_path}"

        try:
            mod = import_module(module_name)
            flow_fn = getattr(mod, flow_function_name)

            logger.info(f"Deploying flow from {module_name}.{flow_function_name}...")
            
            logger.info(f"check: ./{flows_dir}/{flow_file_name}:{flow_function_name}")
            
            deployment = flow_fn.from_source(source=f"./{flows_dir}", entrypoint=f"./{module_path}.py:{flow_function_name}").deploy(
                name=f"{deployment_name}",
                work_pool_name=work_pool_name,
                tags=["ci", module_path]
            )

            logger.info(f"✅ Deployed: {deployment_name}")
        except Exception as e:
            logger.error(f"❌ Failed to deploy flow from {module_name}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy the specific flow.")
    parser.add_argument("deployment_name", type=str, help="Input deployment name")
    parser.add_argument("flows_dir", type=str, help="Input flow directory")
    parser.add_argument("flow_file_name", type=str, help="Input flow file name with py extension")
    parser.add_argument("flow_function_name", type=str, help="Input flow function name as an entery point")
    parser.add_argument("work_pool_name", type=str, help="Input Work-Pool name")
    
    args = parser.parse_args()
    
    deploy_flow(args.deployment_name, args.flows_dir, args.flow_file_name, args.flow_function_name, args.work_pool_name)
