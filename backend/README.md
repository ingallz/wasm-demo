# Backend FastAPI

Backend API đơn giản sử dụng FastAPI với endpoint hello world.

## Cài đặt

1. Tạo virtual environment (khuyến nghị):
```bash
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

### Cách 1: Chạy trực tiếp
```bash
python main.py
```

### Cách 2: Sử dụng uvicorn
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server sẽ chạy tại: http://localhost:8000

## API Endpoints

- `GET /` - Hello world message
- `GET /hello/{name}` - Chào hỏi với tên cụ thể
- `GET /health` - Kiểm tra trạng thái server
- `GET /docs` - Swagger UI documentation (tự động tạo bởi FastAPI)
- `GET /redoc` - ReDoc documentation

## Ví dụ sử dụng

```bash
# Hello world
curl http://localhost:8000/

# Chào hỏi với tên
curl http://localhost:8000/hello/Nam

# Kiểm tra health
curl http://localhost:8000/health
``` 