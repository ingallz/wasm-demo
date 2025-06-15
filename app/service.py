import os
from wasmtime import Engine, Store, Module, Instance, Func, FuncType, ValType


def calculate_fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    
    if n == 0:
        return 0
    if n == 1 or n == 2:
        return 1
    
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)


def calculate_fibonacci_wasm(n: int) -> int:
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")

    wasm_path = os.path.join(os.path.dirname(__file__), 'wasm/build', 'fibonacci_wasm.wasm')
    
    engine = Engine()
    store = Store(engine)
    
    with open(wasm_path, 'rb') as f:
        wasm_bytes = f.read()
    
    module = Module(engine, wasm_bytes)
    
    instance = Instance(store, module, [])
    
    calculate_fibonacci_func = instance.exports(store)["calculate_fibonacci_optimized"]
    
    result = calculate_fibonacci_func(store, n)
    
    return result 
