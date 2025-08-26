import torch

# Check if MPS (Apple GPU backend) is available
print("MPS available:", torch.backends.mps.is_available())

# Pick device: mps if available, otherwise cpu
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print("Using device:", device)

# Quick tensor test
x = torch.randn(1000, 1000, device=device)
y = torch.randn(1000, 1000, device=device)
z = x @ y  # matrix multiply (GPU heavy op)

print("Result tensor device:", z.device)
