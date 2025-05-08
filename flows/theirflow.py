from prefect import flow, task, get_run_logger

@flow(name="Their Flow", description="Their flow description", log_prints=True) 
def flow_start1():
    get_run_logger().info("Hello and welcome to their flow deployed from GitHub!!!")
    get_run_logger().info("Hello again in their flow...")

if __name__ == "__main__":
    my_flow()