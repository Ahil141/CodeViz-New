import sys
import torch
import platform

def check_gpu():
    print("\n" + "="*50)
    print("      GPU COMPATIBILITY CHECK")
    print("="*50)
    
    print(f"Python Platform: {sys.platform}")
    print(f"PyTorch Version: {torch.__version__}")
    
    cuda_available = torch.cuda.is_available()
    print(f"\nCUDA Available:  {cuda_available}")
    
    if cuda_available:
        print(f"Device Count:    {torch.cuda.device_count()}")
        print(f"Current Device:  {torch.cuda.current_device()}")
        print(f"Device Name:     {torch.cuda.get_device_name(0)}")
        print("\n✅ SUCCESS: Your code will run on the GPU.")
    else:
        print("\n❌ FAILURE: PyTorch cannot see your GPU.")
        print("   Reason: You likely have the CPU-only version of PyTorch installed.")
        print("   Solution: You need to reinstall PyTorch with CUDA support.")
    
    print("="*50 + "\n")

if __name__ == "__main__":
    check_gpu()