cmake_minimum_required(VERSION 2.8.3)
project(state_machine)

find_package(OpenCV REQUIRED)
find_package(catkin REQUIRED)

find_package(catkin REQUIRED COMPONENTS
rospy
image_transport
cv_bridge
rosconsole
sensor_msgs
std_msgs
)

catkin_install_python(PROGRAMS src/statemachine.py DESTINATION $(CATKIN_PACKAGE_BIN_DESTINATION))
