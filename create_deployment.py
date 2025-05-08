from pathlib import Path
from importlib import import_module
from prefect.deployments import Deployment

flow_files = Path("flows").glob("*.py")

for file in flow_files:
    module_name = f"flows.{file.stem}"
    mod = import_module(module_name)
    flow = getattr(mod, "my_flow")

    Deployment.build_from_flow(
        flow=flow,
        name=f"{file.stem}-deployment",
        work_pool_name="DewDrop_Pool"
    ).apply()