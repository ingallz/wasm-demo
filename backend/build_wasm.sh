#!/bin/bash

# Kiểm tra xem wasm-pack có được cài đặt chưa
if ! command -v wasm-pack &> /dev/null; then
    echo "wasm-pack chưa được cài đặt. Đang cài đặt..."
    curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh
fi

# Build WASM module
echo "Đang build WASM module..."
wasm-pack build --target web --out-dir wasm_pkg

echo "Build hoàn thành! WASM module đã được tạo trong thư mục wasm_pkg/" 