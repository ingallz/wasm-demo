from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from service import calculate_fibonacci

# Tạo instance FastAPI
app = FastAPI(
    title="Backend API",
    description="API backend đơn giản với FastAPI",
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
    """
    Calculate the fibonacci of number n.
    
    Args:
        n (int): The number to calculate fibonacci for (must be non-negative)
        
    Returns:
        dict: Contains the input number and its fibonacci result
        
    Raises:
        HTTPException: If n is negative or calculation fails
    """
    try:
        result = calculate_fibonacci(n)
        return {
            "number": n,
            "fibonancy": result,
            "message": f"Fibonancy of {n} is {result}"
        }
    except Exception as e:
        raise e;

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 