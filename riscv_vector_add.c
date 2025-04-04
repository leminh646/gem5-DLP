#include <riscv_vector.h>

// Simple vector addition function using RISC-V Vector Extension
void vec_add(int *a, int *b, int *c, int n) {
    size_t vl;
    for (size_t i = 0; i < n; i += vl) {
        vl = __riscv_vsetvl_e32m1(n - i);
        vint32m1_t va = __riscv_vle32_v_i32m1(a + i, vl);
        vint32m1_t vb = __riscv_vle32_v_i32m1(b + i, vl);
        vint32m1_t vc = __riscv_vadd_vv_i32m1(va, vb, vl);
        __riscv_vse32_v_i32m1(c + i, vc, vl);
    }
}

// Bare-metal entry point
int main() {
    // Static arrays to avoid malloc/free
    int a[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int b[10] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
    int c[10] = {0};
    
    // Perform vector addition
    vec_add(a, b, c, 10);
    
    // Result is in c array (we can't print it without stdio.h)
    // But the program will execute correctly
    
    // Return success
    return 0;
}
