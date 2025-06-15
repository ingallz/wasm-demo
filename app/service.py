def calculate_fibonacci(n: int) -> int:
    """
    Calculate the Fibonacci number at position n using recursion.
    
    Args:
        n (int): The position in the Fibonacci sequence (must be non-negative)
        
    Returns:
        int: The Fibonacci number at position n
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    
    if n == 0:
        return 0
    if n == 1 or n == 2:
        return 1
    
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
