import os,subprocess
import numpy as np
import argparse
import platform

def read_data(filepath: str):
    with open(filepath, "r") as f:
        out = f.readlines()
        validdata = out[-20:-1]
        validres = []
        for vd in validdata:
            validres.append(float(vd.strip()))
        return np.mean(validres)


# Create Argparse
parser = argparse.ArgumentParser(description='FPS Runner')
parser.add_argument("--auto", action = "store_true", help = "Run all resolutions with all resolutions")
parser.add_argument("--width", type = int, default = 800, help = "Width of the image")
parser.add_argument("--height", type = int, default = 800, help = "Height of the image")


scenes = ["chair", "drums", "ficus", "hotdog","lego", "materials", "mic", "ship"]

if __name__ == "__main__":
    args = parser.parse_args()
    for scene in scenes:
        os.makedirs(os.path.join("FPSRes","{}".format(scene)),exist_ok= True)
        if(args.auto):
            res = [(200, 200), (400,400), (800,800)]
        else:
            res = [(args.width, args.height)]
        
        
        for r in res:
            print(f"Scene: {scene} Resolution: {r}")
            if platform.system() == "Windows":
                p = subprocess.run(fr".\instant-ngp.exe --snapshot=.\snapshots\NsightComputeData\{scene}.msgpack --width={r[0]} --height={r[1]} >.\FPSRes\{scene}\{r[0]}x{r[1]}_org",shell = True)
            else:
                p = subprocess.run(fr"./instant-ngp --snapshot=./snapshots/NsightComputeData/{scene}.msgpack --width={r[0]} --height={r[1]} >./FPSRes/{scene}/{r[0]}x{r[1]}_org",shell = True)

    ## Reader
    result = []
    for r in res:
        r_res = []
        for scene in scenes:
            path = os.path.join("FPSRes",scene,f"{r[0]}x{r[1]}_org")
            r_res.append(read_data(path))
        result.append(r_res)
    final_resul = np.array(result)
    print(np.mean(final_resul, axis = 1))