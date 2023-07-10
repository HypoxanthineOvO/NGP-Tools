import os, sys
from multiprocessing import cpu_count

if __name__ == "__main__":
    os.system("cmake . -B build")
    
    if cpu_count() >= 12:
        os.system("cmake --build build --config RelWithDebInfo -j")
    else:
        os.system("cmake --build build --config RelWithDebInfo")