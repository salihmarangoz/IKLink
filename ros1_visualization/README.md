Video: https://youtu.be/QoZakQe-J5U

Dependencies:

- ROS Noetic
- https://github.com/justagist/franka_panda_description.git


```bash
# Terminal-1:
cd ros1_visualization
roslaunch start_visualization.launch
```


```bash
# Terminal-2:
cd ros1_visualization
python visualize_output.py ../input_trajectories/panda_2023-08-25_11-37-55.csv  ../output_motions/panda_2023-08-25_11-37-55.csv
#python visualize_output.py [INPUT_TRAJECTORY] [OUTPUT_MOTION]
```