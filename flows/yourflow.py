from prefect import flow, task, get_run_logger

@flow(name="Your Flow", description="Your flow description", log_prints=True) 
def flow_start():
    get_run_logger().info("Hello and welcome to your flow deployed from GitHub!!!")
    get_run_logger().info("Hello again in your flow...")

if __name__ == "__main__":
    my_flow()