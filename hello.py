def add(a: int, b: int) -> int:
    """
    Add two numbers together.

    Args:
        a (int): First number to add
        b (int): Second number to add

    Returns:
        int: The sum of a and b
    """
    return a + b

def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers together.

    Args:
        a (int): First number to multiply
        b (int): Second number to multiply

    Returns:
        int: The product of a and b
    """
    return a * b

def divide(a: int, b: int) -> float:
    """
    Divide first number by second number.

    Args:
        a (int): Numerator
        b (int): Denominator

    Returns:
        float: Result of division a/b

    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def exponent(base: int, exp: int) -> int:
    """
    Calculate the exponential power of a number.

    Args:
        base (int): The base number
        exp (int): The exponent to raise the base to

    Returns:
        int: The result of base raised to the power of exp
    """
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
