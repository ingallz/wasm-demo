# Tích hợp WebAssembly (WASM) với Python/FastAPI

Repository này chứa demo việc tích hợp WebAssembly (WASM) với Python/FastAPI để tối ưu hóa tính toán. Ví dụ sử dụng hàm tính Fibonacci để so sánh hiệu suất giữa Python thuần túy và WASM.

## Cấu trúc dự án

```
wasm-demo/
├── backend/
│   ├── main.py             # FastAPI server
│   ├── service.py          # Dịch vụ Python thông thường
│   ├── wasm_service.py     # Dịch vụ sử dụng WASM
│   ├── Cargo.toml          # Cấu hình dự án Rust
│   ├── src/
│   │   └── lib.rs          # Mã nguồn Rust của hàm Fibonacci
│   └── simple_wasm/
│       └── fibonacci_wasm.wasm  # WASM module đã biên dịch
```

## Cài đặt các công cụ cần thiết

### 1. Cài đặt Rust và target WASM

```bash
# Cài đặt Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Thêm target WASM
rustup target add wasm32-unknown-unknown
```

### 2. Cài đặt Python dependencies

```bash
pip install fastapi uvicorn wasmtime
```

## Tạo module WASM từ Rust

### 1. Viết mã Rust (src/lib.rs)

```rust
#[no_mangle]
pub extern "C" fn calculate_fibonacci(n: u32) -> u64 {
    if n == 0 {
        return 0;
    }
    if n == 1 || n == 2 {
        return 1;
    }
    
    // Sử dụng iterative approach thay vì recursive để tối ưu performance
    let mut prev = 0u64;
    let mut curr = 1u64;
    
    for _ in 2..=n {
        let next = prev + curr;
        prev = curr;
        curr = next;
    }
    
    curr
}
```

### 2. Cấu hình Cargo.toml

```toml
[package]
name = "fibonacci-wasm"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[profile.release]
lto = true
opt-level = 3
```

### 3. Build WASM module

```bash
cargo build --release --target wasm32-unknown-unknown
mkdir -p simple_wasm
cp target/wasm32-unknown-unknown/release/fibonacci_wasm.wasm simple_wasm/
```

## Tích hợp WASM với Python

### 1. Tạo service sử dụng WASM (wasm_service.py)

```python
import os
from wasmtime import Engine, Store, Module, Instance

def calculate_fibonacci_wasm(n: int) -> int:
    """
    Calculate the Fibonacci number at position n using WASM module.
    
    Args:
        n (int): The position in the Fibonacci sequence (must be non-negative)
        
    Returns:
        int: The Fibonacci number at position n
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
```

### 2. Tạo API endpoints (main.py)

```python
from fastapi import FastAPI, HTTPException
from service import calculate_fibonacci
from wasm_service import calculate_fibonacci_wasm

app = FastAPI()

@app.get("/fibonacci/{n}")
async def get_fibonacci(n: int):
    try:
        result = calculate_fibonacci(n)
        return {
            "number": n,
            "fibonancy": result,
            "message": f"Fibonacci of {n} is {result}",
            "method": "Python"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/fibonacci-wasm/{n}")
async def get_fibonacci_wasm(n: int):
    try:
        result = calculate_fibonacci_wasm(n)
        return {
            "number": n,
            "fibonancy": result,
            "message": f"Fibonacci of {n} is {result} (calculated using WASM)",
            "method": "WASM"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## Chạy API server

```bash
cd wasm-demo
python backend/main.py
```

## Test APIs

```bash
# Test API sử dụng Python thuần túy
curl http://localhost:8000/fibonacci/10

# Test API sử dụng WASM
curl http://localhost:8000/fibonacci-wasm/10
```

## So sánh hiệu suất

Để thấy rõ lợi ích của WASM, hãy thử các giá trị lớn của n (ví dụ: n=40) và so sánh thời gian phản hồi giữa hai endpoints:

```bash
# So sánh thời gian phản hồi
time curl http://localhost:8000/fibonacci/40
time curl http://localhost:8000/fibonacci-wasm/40
```

WASM thường mang lại hiệu suất tốt hơn nhiều cho các tính toán phức tạp vì nó được biên dịch thành mã máy gần với native code. 