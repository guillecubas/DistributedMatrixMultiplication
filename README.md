# Distributed Matrix Multiplication (Simulated with Hazelcast and Multiprocessing)

This project performs distributed-style matrix multiplication using:

- ✅ `multiprocessing` to simulate parallel computation (multiple nodes)
- ✅ `Hazelcast` distributed map for shared storage (Matrix A, B, and result)
- ✅ Logging of performance metrics to a CSV file for analysis (memory, CPU, execution time)

---

## 📦 Project Structure

```
python_distributed_matrix/
├── main.py                 # Main orchestration script
├── matrix_utils.py         # Matrix generation and printing
├── matrix_multiplier.py    # Row-based parallel multiplication
├── metrics_logger.py       # Logs execution time, memory, CPU to CSV
├── requirements.txt        # Dependencies
└── README.md               # This file
```

