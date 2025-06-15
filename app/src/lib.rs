#[no_mangle]
pub extern "C" fn calculate_fibonacci(n: u32) -> u64 {
    if n == 0 {
        return 0;
    }
    if n == 1 || n == 2 {
        return 1;
    }
    
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2);
} 