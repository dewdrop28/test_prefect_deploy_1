from prefect import flow, task, get_run_logger

@flow(name="My Flow", description="My flow description", log_prints=True) 
def flow_entry():
    get_run_logger().info("Hello and welcome to my flow deployed from GitHub!!!")
    get_run_logger().info("Hello again")

if __name__ == "__main__":
    my_flow()