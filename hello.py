# write a function called add that adds two numbers together
def add(a: int, b: int) -> int:
    return a + b

def multiply(a: int, b: int) -> int:
    return a * b

def divide(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def exponent(base: int, exp: int) -> int:
    return base ** exp

def main():
    """
    Main entry point of the program.

    This function prints a greeting message and demonstrates basic arithmetic operations
    by calling the add, multiply, divide, and exponent functions with sample values.

    Returns:
        None
    """
    print("Hello from api-versioning-github-copilot!")
    print(add(1, 2))
    print(multiply(2, 3))
    print(divide(10, 2))
    print(exponent(2, 3))


if __name__ == "__main__":
    main()
