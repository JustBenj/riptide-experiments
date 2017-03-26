import rospy
import sys
import cv2
import SimulatorMap
import numpy as np
import time
import DebugViewer
from std_msgs.msg import String

entities = []
FRAME_RATE = 20
ROBOT_SPEED = 10 #no units
ROBOT_ROTATE_SPEED = 0.01
FOV = 50
class Entity():
	def __init__(self, name, x_pos, y_pos, spherical, orientation, floor_object, width):
		self.name = name
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.Spherical = spherical
		self.orientation = orientation
		self.floor_object = floor_object
		self.width = width
def Simulator():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("command/command", String, callback)
	load_entities()

	#Always keep robot as ent. 0
	robot = entities[0]
	print "mapping"
	simmap = SimulatorMap.SimulatorMap(entities, FOV)
	debug_viewer = DebugViewer.DebugViewer(entities, FOV)

	print "Past map creation"
	#time.sleep(0.1)
	while 1:
		start = time.time()
		simmap.handle_robot_rotation()
		simmap.draw_map()
		debug_viewer.update_view_window()
		rospy.spin()

def update_robot_position(robot, speed, direction):
	#direction = 1 for side to side and 0 for forward/backward
	robot.x_pos += int(speed * np.cos(robot.orientation + direction * np.pi / 2.0))
	robot.y_pos -= int(speed * np.sin(robot.orientation + direction * np.pi / 2.0))
	robot.orientation = robot.orientation % (2.0 * np.pi)
	if robot.orientation < 0:
		robot.orientation = 2.0 * np.pi + robot.orientation
def load_entities():
	robot = Entity("robot", 900, 1800, 0, np.pi / 2.3, 0, 10)
	entities.append(robot)

	gate = Entity("gate",800, 1500,0, -1 * np.pi / 5.0, 0, 50)
	entities.append(gate)

	ofm = Entity("ofm", 1000, 700, 0, np.pi / 2.25, 1, 40)
	entities.append(ofm)

	redb = Entity("redb", 1050, 200, 1, 0, 0, 30)
	entities.append(redb)

	yellowb = Entity("yellowb", 1200, 200, 1, 0, 0, 30)
	entities.append(yellowb)

	greenb = Entity("greenb", 1350, 200, 1, 0, 0, 30)
	entities.append(greenb)

def callback(data):
	print "callback"
	direction = data.data
	if direction is "tx+":
		updateRobotPosition(entities[0], ROBOT_SPEED, 0)
	elif direction is "tx-":
		updateRobotPosition(entities[0], -1 * ROBOT_SPEED, 0)
	elif direction is "ty-":
		updateRobotPosition(entities[0], ROBOT_SPEED, 1)
	elif direction is "tz-":
		updateRobotPosition(entities[0], -1 * ROBOT_SPEED, 1)
	elif direction is "rx+":
		entities[0].orientation -= ROBOT_ROTATE_SPEED
	elif direction is "rx-":
		entities[0].orientation += ROBOT_ROTATE_SPEED

if __name__ == '__main__':

	Simulator()