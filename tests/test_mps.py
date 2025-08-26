import torch
import time

def benchmark(device, size=5000):
    print(f"\nRunning on {device} ...")
    x = torch.randn(size, size, device=device)
    y = torch.randn(size, size, device=device)

    # Warm-up (important for fair GPU timing)
    _ = x @ y  

    torch.cuda.synchronize() if device.type == "cuda" else None
    if device.type == "mps":
        torch.mps.synchronize()

    start = time.time()
    z = x @ y
    if device.type == "cuda":
        torch.cuda.synchronize()
    if device.type == "mps":
        torch.mps.synchronize()
    end = time.time()

    print(f"Time: {end - start:.4f} sec")
    return z

# CPU benchmark
cpu_device = torch.device("cpu")
benchmark(cpu_device)

# MPS benchmark (if available)
if torch.backends.mps.is_available():
    mps_device = torch.device("mps")
    benchmark(mps_device)
else:
    print("\nMPS not available on this machine.")

