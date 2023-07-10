# Test for NGP's FPS
## 程序修改
在 `testbed.cu` 的4327行 加上：
```cpp
std::cout << 1000.0f / m_frame_ms.ema_val() << std::endl;
```

### 具体位置：
`render_nerf_main` 函数的如下部分：
```cpp
if (!m_render_ground_truth || m_ground_truth_alpha < 1.0f) {
    render_nerf(device.stream(), device.render_buffer_view(), *device.nerf_network(), device.data().density_grid_bitfield_ptr, focal_length, camera_matrix0, camera_matrix1, nerf_rolling_shutter, screen_center, foveation, visualized_dimension);
    std::cout << 1000.0f / m_frame_ms.ema_val() << std::endl;
}
break;
```
## Scripts
Run `python3 FPS_Getter.py` to get the FPS of each scene.