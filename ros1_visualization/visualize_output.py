import argparse
import csv
from sensor_msgs.msg import JointState
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import rospy
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualizer")
    parser.add_argument("input_trajectory_file", type=str, help="Input trajectory file in csv")
    parser.add_argument("output_motion_file", type=str, help="Output motion file in csv")
    args = parser.parse_args()

    rospy.init_node('visualize_output', anonymous=True)
    joint_pub = rospy.Publisher('/joint_states', JointState, queue_size=2)
    path_pub = rospy.Publisher('/trajectory_vis', Path, queue_size=2, latch=True)

    with open(args.input_trajectory_file) as f:
        in_trajectory = csv.reader(f, delimiter=',', quotechar='|')
        trajectory = Path()
        for i, line in enumerate(in_trajectory):
            if i==0: continue
            p = PoseStamped()
            p.pose.position.x = float(line[1])
            p.pose.position.y = float(line[2])
            p.pose.position.z = float(line[3])
            p.pose.orientation.x = float(line[4])
            p.pose.orientation.y = float(line[5])
            p.pose.orientation.z = float(line[6])
            p.pose.orientation.w = float(line[7])
            trajectory.poses.append(p)
        trajectory.header.frame_id = "world"
        path_pub.publish(trajectory)
    
    with open(args.output_motion_file) as f:
        out_motion = csv.reader(f, delimiter=',', quotechar='|')

        js = JointState()
        start_time = rospy.Time.now()
        for i, line in enumerate(out_motion):
            js.position = []
            if i==0:
                for j,val in enumerate(line):
                    if j==0: continue
                    modified_joint_name = val.split("-")[1]
                    js.name.append(modified_joint_name)  # REMOVE PREFIX "panda-panda_joint1" -> "panda_joint1"
            else:
                for j,val in enumerate(line):
                    if j==0: 
                        playback_time = float(val)
                        continue
                    js.position.append(float(val))

            if i!=0:
                current_time = start_time + rospy.Duration(playback_time)
                rospy.sleep(current_time - rospy.Time.now())
                js.header.stamp = rospy.Time.now()
                joint_pub.publish(js)


