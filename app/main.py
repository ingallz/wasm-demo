from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from service import calculate_fibonacci, calculate_fibonacci_wasm

app = FastAPI(
    title="Backend API",
    description="API backend for Fibonacci calculation",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fibonacci calculation API endpoint
@app.get("/fibonacci/{n}")
async def get_fibonacci(n: int):
    try:
        import time
        start_time = time.time()
        result = calculate_fibonacci(n)
        execution_time = time.time() - start_time
        return {
            "number": n,
            "fibonancy": result,
            "message": f"Fibonancy of {n} is {result}",
            "execution_time": execution_time
        }
    except Exception as e:
        raise e;

# Fibonacci calculation API endpoint using WASM
@app.get("/fibonacci-wasm/{n}")
async def get_fibonacci_wasm(n: int):
    try:
        import time
        start_time = time.time()
        result = calculate_fibonacci_wasm(n)
        execution_time = time.time() - start_time
        return {
            "number": n,
            "fibonancy": result,
            "message": f"Fibonancy of {n} is {result} (calculated using WASM)",
            "method": "WASM",
            "execution_time": execution_time
        }
    except Exception as e:
        raise e;

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 