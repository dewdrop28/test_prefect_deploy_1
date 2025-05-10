import subprocess
from prefect import flow, task, get_run_logger

@task
def check_packages():
    logger = get_run_logger()
    result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
    logger.info(result.stdout)

@flow
def list_all_packages():
    check_packages()

if __name__ == "__main__":
    list_all_packages()