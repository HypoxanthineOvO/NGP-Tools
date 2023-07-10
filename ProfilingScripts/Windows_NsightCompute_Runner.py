import os
from os import makedirs
from os.path import join
import argparse

# Create Parser
parser = argparse.ArgumentParser(description='Nsight Compute Runner')
parser.add_argument("--sysbits", default = "64", help = "System bits")
parser.add_argument("--ncu_version", default = "2023.1.0", help = "Nsight Compute Version")
parser.add_argument("--ncu_path", default = None, help = "Path of the Nsight Compute CLI")

kernels = ["kernel_grid",
           "kernel_mlp_fused",
           "advance_pos_nerf_kernel",
           "generate_next_nerf_network_inputs",
           "init_rays_with_payload_kernel_nerf"]
scenes = ["chair", "drums", "ficus", "hotdog","lego", "materials", "mic", "ship"]



if __name__ == "__main__":
    args = parser.parse_args()
    ncu_path = join("C","Program Files","NVIDIA Corporation",f"Nsight Compute {args.ncu_version}","target",f"windows-desktop-win7-x{64}","ncu.exe")
    if args.ncu_path is not None:
        ncu_path = args.ncu_path
    # Set Executable Path
    ngp_path = os.path.join("instant-ngp.exe")
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
        snapshot_path = join("snapshots","NsightComputeData",f"{scene}.msgpack")
        for kernel in kernels:
            instruction = f"ncu --config-file off  --csv --page=details --print-details=all --export {report_path}/{kernel} --force-overwrite --kernel-name {kernel} --set full {ngp_path} --snapshot={snapshot_path} --width=800 --height=800 > {data_path}/{kernel}.txt"
            ##continue
            os.system(instruction)