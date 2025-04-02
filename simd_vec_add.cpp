// Uses AVX or SSE intrinsics for parallel execution.
#include <iostream>
#include <vector>
#include <chrono>
#include <immintrin.h>

const int SIZE = 1000000;

void simd_add(float* a, float* b, float* c, int size) {
    for (int i = 0; i < size; i += 4) {  // SSE processes 4 floats at a time
        __m128 va = _mm_loadu_ps(&a[i]);
        __m128 vb = _mm_loadu_ps(&b[i]);
        __m128 vc = _mm_add_ps(va, vb);
        _mm_storeu_ps(&c[i], vc);
    }
}

int main() {
    std::vector<float> a(SIZE, 1.0f), b(SIZE, 2.0f), c(SIZE, 0.0f);

    auto start = std::chrono::high_resolution_clock::now();
    simd_add(a.data(), b.data(), c.data(), SIZE);
    auto end = std::chrono::high_resolution_clock::now();

    std::cout << "SIMD Execution Time: " 
              << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() 
              << " microseconds" << std::endl;

    return 0;
}
