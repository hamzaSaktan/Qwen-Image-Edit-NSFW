"""
Bootstrap loader for directly uploaded compiled ZeroGPU Space.
Loads and executes the compiled `backend/app.so` binary within this process.
"""
import os
import sys
import importlib.util

# Path to the subfolder where your compiled app.so lives
BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")

if not os.path.isdir(BACKEND_DIR):
    raise SystemExit(
        f"Error: '{BACKEND_DIR}' directory not found. "
        "Please make sure you uploaded the 'backend' folder containing your 'app.so'."
    )

# 1. Insert backend directory to the top of Python's search path & switch working directory
sys.path.insert(0, BACKEND_DIR)
os.chdir(BACKEND_DIR)

print("[bootstrap] searching for compiled app binary in backend/ ...")

# 2. Look for the compiled module (e.g. app.so or app.cpython-xxx.so)
spec = importlib.util.find_spec("app")
if spec is None:
    raise ImportError(
        "Could not find the compiled 'app' binary module inside the backend folder.\n"
        "Ensure the file is compiled for Linux x86_64 and matches the Space's Python version."
    )

# 3. Load the binary module dynamically
compiled_app = importlib.util.module_from_spec(spec)

# 4. Simulate the "__main__" environment (crucial for ZeroGPU decorators and imports)
compiled_app.__name__ = "__main__"

print("[bootstrap] launching compiled app ...")

# 5. Execute the binary in the current process space
spec.loader.exec_module(compiled_app)