import os

from ament_index_python.packages import get_package_share_directory
from launch.actions import ExecuteProcess
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    package_name='raspimouse_description' 

    robot_name = 'raspimouse_description'
    world_file_name = 'pimouse_world.world'

    world = os.path.join(get_package_share_directory(robot_name), 'worlds', world_file_name)
    urdf_file_path = os.path.join(get_package_share_directory(robot_name), 'urdf', 'raspimouse.urdf')

    # Load the URDF file as a string.
    with open(urdf_file_path, 'r') as f:
        urdf = f.read()

    urdf_for_spawn = urdf.replace('"', '\\"')
    spawn_args = '{name: \"pimouse\", xml: \"'  +  urdf_for_spawn + '\" }'
    
    rsp = Node(package='robot_state_publisher',
           executable='robot_state_publisher',
           output='both',               
           parameters=[{'robot_description': urdf}])

    # rest of your code




    return LaunchDescription([
        rsp,
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_factory.so'],
            output='screen'),

        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/spawn_entity', 'gazebo_msgs/SpawnEntity', spawn_args],
            output='screen')
    ])
