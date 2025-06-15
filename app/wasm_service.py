import os
from wasmtime import Engine, Store, Module, Instance, Func, FuncType, ValType

def calculate_fibonacci_wasm(n: int) -> int:
    """
    Calculate the Fibonacci number at position n using WASM module.
    
    Args:
        n (int): The position in the Fibonacci sequence (must be non-negative)
        
    Returns:
        int: The Fibonacci number at position n
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")

    # Đường dẫn đến file WASM
    wasm_path = os.path.join(os.path.dirname(__file__), 'simple_wasm', 'fibonacci_wasm.wasm')
    
    # Tạo Wasmtime engine và store
    engine = Engine()
    store = Store(engine)
    
    # Đọc và compile WASM module
    with open(wasm_path, 'rb') as f:
        wasm_bytes = f.read()
    
    module = Module(engine, wasm_bytes)
    
    # Tạo instance
    instance = Instance(store, module, [])
    
    # Lấy hàm calculate_fibonacci từ instance
    calculate_fibonacci_func = instance.exports(store)["calculate_fibonacci"]
    
    # Gọi hàm với tham số n
    result = calculate_fibonacci_func(store, n)
    
    return result 