import os

kernels = ["kernel_grid", "kernel_mlp_fused", "advance_pos_nerf_kernel", "generate_next_nerf_network_inputs", "init_rays_with_payload_kernel_nerf"]

scenes = ["chair", "drums", "ficus", "hotdog","lego", "materials", "mic", "ship"]

Metrics = [
    # L1 Cache
    "gld_throughput",
    "gst_throughput",
    "gld_transactions",
    "gst_transactions",
    "tex_cache_hit_rate",
    # L2 Cache
    "l2_tex_read_transactions",
    "l2_tex_write_transactions",
    "l2_tex_hit_rate",
    "l2_tex_read_hit_rate",
    "l2_tex_write_hit_rate",
    # Dram
    "dram_read_transactions",
    "dram_write_transactions",
]


if __name__ == "__main__":
    # Create Results Directory
    os.makedirs("NvprofResults", exist_ok=True)
    for scene in scenes:
        # Create Scene Directory
        scene_path = os.path.join(".", "NvprofResults", scene)
        os.makedirs(scene_path, exist_ok=True)
        for kernel in kernels:
            # Create Kernel Directory
            kernel_path = os.path.join(scene_path, kernel+".txt")
            #os.makedirs(kernel_path, exist_ok=True)
            config_metrics = ""
            for metric in Metrics:
                # Run Nvprof
                config_metrics += metric + ","
            command = f"sudo nvprof --timeout 10 --kernels {kernel} --metrics {config_metrics} --csv --log-file {kernel_path} ./instant-ngp --snapshot=./snapshots/NsightComputeData/{scene}.msgpack"
            print(command)
            os.system(command)
