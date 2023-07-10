import os, sys
import argparse
from os import makedirs
from os.path import join


# Create Parser
parser = argparse.ArgumentParser(description='Nsight Compute Runner')
parser.add_argument("--ncu_path", default = "/usr/local/cuda/bin/ncu", help = "Path of the Nsight Compute CLI")

# Set Profiling Kernels and Scenes
kernels = ["kernel_grid", 
            "kernel_mlp_fused", 
            "advance_pos_nerf_kernel", 
            "generate_next_nerf_network_inputs", 
            "init_rays_with_payload_kernel_nerf"]
scenes = ["chair", "drums", "ficus", "hotdog","lego", "materials", "mic", "ship"]


if __name__ == "__main__":
    args = parser.parse_args()
    ncu_path = args.ncu_path
    print("NCU Runner!")
    makedirs("NsightComputeResults", exist_ok= True)
    # Get Reports dir
    makedirs(join("NsightComputeResults", "Reports"), exist_ok= True)
    # Get Datas dir
    makedirs(join("NsightComputeResults", "Datas"), exist_ok= True)
    for scene in scenes:
        report_path = join("NsightComputeResults", "Reports",f"{scene}")
        makedirs(report_path, exist_ok= True)
        data_path = join("NsightComputeResults", "Datas",f"{scene}")
        makedirs(data_path, exist_ok= True)
        for kernel in kernels:
            instruction = f"{ncu_path} --csv --page=details --details-all --export {report_path}/{kernel} --force-overwrite --kernel-name {kernel} --set full /home/hypoxanthine/Workspace/instant-ngp/instant-ngp --snapshot=/home/hypoxanthine/Workspace/instant-ngp/snapshots/NsightComputeData_Big/{scene}.msgpack --width=800 --height=800 > {data_path}/{kernel}.txt"
            os.system(instruction)
