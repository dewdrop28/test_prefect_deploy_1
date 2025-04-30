from prefect import flow


@flow
def my_flow() -> str:
    print("Welcome to our first flow!")
    return "Hello, world!"

if __name__ == "__main__":
    print(my_flow())
