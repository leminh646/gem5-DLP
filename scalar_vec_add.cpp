//Uses a traditional loop-based implementation.
#include <iostream>
#include <vector>
#include <chrono>

const int SIZE = 1000000;

void scalar_add(float* a, float* b, float* c, int size) {
    for (int i = 0; i < size; i++) {
        c[i] = a[i] + b[i];
    }
}

int main() {
    std::vector<float> a(SIZE, 1.0f), b(SIZE, 2.0f), c(SIZE, 0.0f);

    auto start = std::chrono::high_resolution_clock::now();
    scalar_add(a.data(), b.data(), c.data(), SIZE);
    auto end = std::chrono::high_resolution_clock::now();

    std::cout << "Scalar Execution Time: " 
              << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() 
              << " microseconds" << std::endl;

    return 0;
}
