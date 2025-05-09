import os
import argparse
from pathlib import Path
from importlib import import_module
from prefect.logging import get_logger
from prefect_github import GitHubCredentials
from prefect.runner.storage import GitRepository

logger = get_logger()

def deploy_flow(deployment_name, flows_dir, flow_file_name, flow_function_name, work_pool_name, github_token):        
    
        module_path = Path(f"{flow_file_name}").stem  # Remove .py
        module_name = f"{flows_dir}.{module_path}"

        try:
            mod = import_module(module_name)
            flow_fn = getattr(mod, flow_function_name)

            logger.info(f"Deploying flow from {module_name}.{flow_function_name}...")
            
            github_credentials = GitHubCredentials(token=github_token)
            
            logger.info(f"check: {flows_dir}/{flow_file_name}:{flow_function_name}")
            
            deployment = flow_fn.from_source(source=source, entrypoint=f"./{flows_dir}/{module_path}.py:{flow_function_name}").deploy(
                name=f"{deployment_name}",
                work_pool_name=work_pool_name,
                tags=["ci", module_path],
                infrastructure_overrides={
                    "install_requires": [
                        "prefect-azure",
                        "azure-storage-blob"
                    ],
                    "env": {
                        "PREFECT_LOGGING_LEVEL": "DEBUG"
                    }
                }
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
    parser.add_argument("github_token", type=str, help="Input GitHub token")
    
    args = parser.parse_args()
    
    source = GitRepository(
        url="https://github.com/dewdrop28/test_prefect_deploy_1.git",
        credentials=GitHubCredentials.load(args.github_token)
    )

    deploy_flow(args.deployment_name, args.flows_dir, args.flow_file_name, args.flow_function_name, args.work_pool_name, args.github_token)
