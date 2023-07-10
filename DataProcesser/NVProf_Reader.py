import os
import pandas as pd

kernels = ["kernel_grid", "kernel_mlp_fused", "advance_pos_nerf_kernel", "generate_next_nerf_network_inputs", "init_rays_with_payload_kernel_nerf"]

scenes = ["chair", "drums", "ficus", "hotdog","lego", "materials", "mic", "ship"]

if __name__ == "__main__":
    # Create Results Directory
    for scene in scenes:
        # Create Scene Directory
        scene_path = os.path.join(".", "NvprofResults", scene)
        for kernel in kernels:
            # Create Kernel Directory
            kernel_path = os.path.join(scene_path, kernel+".txt")
            with open(kernel_path, "r") as f:
                lines = f.readlines()
                # Remova lines starting with "=="
                lines = [line for line in lines if not line.startswith("==")]
            with open(kernel_path, "w") as f:
                f.writelines(lines)
    
    # Transform to CSV
    for scene in scenes:
        # Create Scene Directory
        os.makedirs(os.path.join("./Outputs"), exist_ok=True)
        scene_path = os.path.join(".", "NvprofResults", scene)
        os.makedirs(scene_path, exist_ok=True)
        for kernel in kernels:
            # Create Kernel Directory
            kernel_path = os.path.join(scene_path, kernel+".txt")
            
            data = pd.read_csv(kernel_path)
            # Remove first two columns
            data = data.drop(data.columns[[0, 1, 2]], axis=1)
            
            os.makedirs(os.path.join("./Outputs", scene), exist_ok=True)
            data.to_csv(os.path.join("./Outputs", scene, kernel+".csv"), index=False)
