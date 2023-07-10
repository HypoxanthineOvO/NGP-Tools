import numpy as np
import msgpack
import json, os

def load_msgpack(path:str):
    '''
    Load .msgpack file
    @param[in]: path path to .msgpack file
    @param[out]: config The config of a instant-ngp msgpack
    '''
    with open(path, 'rb') as f:
        unpacker = msgpack.Unpacker(f, raw=False)
        config = next(unpacker)
        return config

def write_msgpack(path:str,msg_config):
    with open(path,'wb') as f:
        f.write(msgpack.packb(msg_config,use_bin_type = True))
    print("Save Config in {}".format(path))
    
def nerf_to_ngp(nerf_mat, scale = 0.33, offset = np.array([0.5,0.5,0.5])):
    nerf_mat[0] *= 1
    nerf_mat[1] *= -1
    nerf_mat[2] *= -1
    nerf_mat[3] = nerf_mat[3] *scale + offset
    return np.roll(nerf_mat, -1, axis=1)


scenes = ["chair", "drums", "ficus", "hotdog","lego", "materials", "mic", "ship"]

if __name__ == "__main__":
    """
    Set the Snapshots' camera matrix to the same as the nerf_synthetic's first test scenes' camera matrix
    """
    for scene in scenes:
        name = scene
        json_path = os.path.join("data","nerf_synthetic",scene,"transforms_test.json")
        datas = json.load(open(json_path))
        
        config = load_msgpack(f"./snapshots/NsightComputeData/{name}.msgpack")
        mat = datas["frames"][0]["transform_matrix"][:3]
        np_t_mat = np.array(mat).T
        trans_mat = (nerf_to_ngp(np_t_mat)).T
        config["snapshot"]["camera"]["matrix"] = trans_mat.tolist()
        write_msgpack(f"./snapshots/NsightComputeData/{name}.msgpack",config)