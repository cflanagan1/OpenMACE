cmake_minimum_required(VERSION 2.8.3)
project(mace_matlab)

add_compile_options(-std=c++11)

## Find catkin and any catkin packages
find_package(catkin REQUIRED COMPONENTS 
  roscpp
  rospy
  std_msgs
  gencpp
  geometry_msgs
  message_generation
)

## Define custom message files
add_message_files(
  FILES
  UPDATE_ATTITUDE.msg
  UPDATE_BATTERY.msg
  UPDATE_CMD_STATUS.msg
  UPDATE_GPS.msg
  UPDATE_HEARTBEAT.msg
  UPDATE_POSITION.msg
  UPDATE_VEHICLE_TARGET.msg
)

## Generate services in the 'srv' folder
add_service_files(
  FILES
  CMD_TAKEOFF.srv
  CMD_LAND.srv
  CMD_ARM.srv
  CMD_DATUM.srv
  CMD_WPT.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
)

## Declare a catkin package
catkin_package(
  INCLUDE_DIRS include ${catkin_INCLUDE_DIRS}
  CATKIN_DEPENDS roscpp geometry_msgs sensor_msgs std_msgs message_runtime
  LIBRARIES mace_matlab
)

include_directories(include ${catkin_INCLUDE_DIRS})

add_library(mace_matlab src/matlab_listener.cpp src/mace_listener.cpp)
