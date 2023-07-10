import os
from os import makedirs
from os.path import join
import pandas as pd
import numpy as np
from tqdm import tqdm

def remove_unused_lines(path):
    '''
    Remove the first lines of the file until the line is truly data
    '''
    assert(os.path.isfile(path))
    fin = open(path, 'r')
    lines = fin.readlines()
    fin.close()
    while(lines[0][:4] != "\"ID\""):
        lines.pop(0)
    output_lines = "".join(lines)
    
    fout = open(path, "w")
    fout.write(output_lines)
    fout.close()

kernels = ["kernel_grid", 
           "kernel_mlp_fused", 
           "advance_pos_nerf_kernel", 
           "generate_next_nerf_network_inputs", 
           "init_rays_with_payload_kernel_nerf"]
scenes = ["chair", "drums", "ficus", "hotdog","lego", "materials", "mic", "ship"]


L1_idx = [
    "l1tex__t_requests_pipe_lsu_mem_global_op_ld.sum",
    "l1tex__t_output_wavefronts_pipe_lsu_mem_global_op_ld.sum",
    "l1tex__t_sectors_pipe_lsu_mem_global_op_ld.sum",
    "l1tex__m_xbar2l1tex_read_sectors_mem_lg_op_ld.sum",
    "l1tex__t_requests_pipe_lsu_mem_global_op_st.sum",
    "l1tex__t_output_wavefronts_pipe_lsu_mem_global_op_st.sum",
    "l1tex__t_sectors_pipe_lsu_mem_global_op_st.sum",
    "l1tex__m_l1tex2xbar_write_sectors_mem_lg_op_st.sum"
]
L2_idx = [
    "lts__t_requests_srcunit_tex_op_read.sum",
    "lts__t_sectors_srcunit_tex_op_read.sum",
    "lts__t_sectors_srcunit_tex_aperture_device_op_read_lookup_miss.sum",
    "lts__t_requests_srcunit_tex_op_write.sum",
    "lts__t_sectors_srcunit_tex_op_write.sum",
    "lts__t_sectors_srcunit_tex_aperture_device_op_write_lookup_miss.sum"
]
L3_idx = [
    "dram__sectors_read.sum",
    "dram__sectors_write.sum",
]

if __name__ == "__main__":
    res_base_path = join("NsightComputeResults","Results")
    makedirs(res_base_path, exist_ok=True)
    base_path = join("NsightComputeResults","Datas")
    for scene in tqdm(scenes):
        data_path = join(base_path, scene)
        makedirs(join(res_base_path, scene), exist_ok=True)
        for kernel in kernels:
            # Remove Data First
            file_name = kernel + ".txt"
            file_path = join(data_path, file_name)
            print(file_path)
            remove_unused_lines(file_path)
            
            # Define Result Dataframe
            L1_res = pd.DataFrame(
                index = ["Loads", "stores"],
                columns = ["Requests", "Wavefronts", "Sectors","Sector Miss to L2"]
            )
            L2_res = pd.DataFrame(
                index = ["L1/TEX Loads", "L1/TEX Stores"],
                columns = ["Requests",  "Sectors", "Sector Miss to Device"]
            )
            Device_res = pd.DataFrame(
                index = ["Loads", "Stores"],
                columns = ["Sectors"]
            )
            datas = pd.read_csv(file_path,sep=",",on_bad_lines='skip')
            
            # Get data
            bil = "L1/TEX Cache"
            for i in range(8):
                mn = L1_idx[i]
                pd_res = datas[(datas["Body Item Label"] == bil) & (datas["Metric Name"] == mn)].loc[:,["Metric Value"]]
                list_res = np.array(pd_res).reshape(1,-1)#.squeeze().tolist()
                
                list_res = list_res.squeeze().tolist()
                if isinstance(list_res, str):
                    list_res = [list_res]
                
                rem_res = []
                for lr in list_res:
                    if "," in lr:
                        lr = lr.replace(",","")
                    rem_res.append(int(lr))
                #print(f"scene:{scene}, kernel:{kernel}, {rem_res}")
                sum_value = np.sum(rem_res)
                #sum_value = np.sum(list(map(lambda x: int(x), rem_res)))
                idx_row = i // 4
                idx_column = i % 4
                L1_res.iloc[idx_row,idx_column] = sum_value

            bil = "L2 Cache"
            for i in range(6):
                mn = L2_idx[i]
                pd_res = datas[(datas["Body Item Label"] == bil) & (datas["Metric Name"] == mn)].loc[:,["Metric Value"]]
                list_res = np.array(pd_res).reshape(1,-1)#.squeeze().tolist()
                
                list_res = list_res.squeeze().tolist()
                if isinstance(list_res, str):
                    list_res = [list_res]
                
                rem_res = []
                for lr in list_res:
                    if "," in lr:
                        lr = lr.replace(",","")
                    rem_res.append(int(lr))
                #print(f"scene:{scene}, kernel:{kernel}, {rem_res}")
                sum_value = np.sum(rem_res)
                idx_row = i // 3
                idx_column = i % 3
                L2_res.iloc[idx_row,idx_column] = sum_value

            bil = "Device Memory"
            for i in range(2):
                mn = L3_idx[i]
                pd_res = datas[(datas["Body Item Label"] == bil) & (datas["Metric Name"] == mn)].loc[:,["Metric Value"]]
                list_res = np.array(pd_res).reshape(1,-1)#.squeeze().tolist()
                
                list_res = list_res.squeeze().tolist()
                if isinstance(list_res, str):
                    list_res = [list_res]
                
                rem_res = []
                for lr in list_res:
                    if "," in lr:
                        lr = lr.replace(",","")
                    rem_res.append(int(lr))
                #print(f"scene:{scene}, kernel:{kernel}, {rem_res}")
                sum_value = np.sum(rem_res)
                idx_row = i // 1
                idx_column = i % 1
                Device_res.iloc[idx_row,idx_column] = sum_value
            makedirs(join(res_base_path, scene, kernel), exist_ok=True)
            L1_res.to_csv(join(res_base_path, scene, kernel, kernel + "_L1.csv"))
            L2_res.to_csv(join(res_base_path, scene, kernel, kernel + "_L2.csv"))
            Device_res.to_csv(join(res_base_path, scene, kernel, kernel + "_Device.csv"))
