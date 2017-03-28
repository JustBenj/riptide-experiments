chmod +x SimulatorMap_ros.py
chmod +x DebugViewer_ros.py
chmod +x Simulator_ros.py

roscore &
rosrun image_view image_view image:=/map_view &
rosrun image_view image_view image:=/sim_view &
python Simulator_ros.py
