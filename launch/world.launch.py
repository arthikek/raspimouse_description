import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    robot_name = 'raspimouse_description'
    world_file_name = 'simple.world'

    # full path to urdf and world file
    world = os.path.join(get_package_share_directory(robot_name), 'worlds', world_file_name)
    urdf = os.path.join(get_package_share_directory(robot_name), 'urdf', 'raspimouse.urdf')
    
    # read urdf contents because to spawn an entity in 
    # gazebo we need to provide entire urdf as string on command line
    xml = open(urdf, 'r').read()

    # double quotes need to be with escape sequence
    xml = xml.replace('"', '\\"')

    # this is argument format for spwan_entity service 
    spwan_args = '{name: \"pimouse\", xml: \"'  +  xml + '\" }'
    
    # Path to the diff_drive_controller.yaml file
    param_file = os.path.join(get_package_share_directory(robot_name), 'config', 'params.yaml')

    return LaunchDescription([
        # start gazebo, notice we are using libgazebo_ros_factory.so instead of libgazebo_ros_init.so
        # That is because only libgazebo_ros_factory.so contains the service call to /spawn_entity
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_factory.so'],
            output='screen'),

        # tell gazebo to spawn your robot in the world by calling service
        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/spawn_entity', 'gazebo_msgs/SpawnEntity', spwan_args],
            output='screen'),

        # start controller manager
        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[param_file],
            output={
                'stdout': 'screen',
                'stderr': 'screen',
            },
        ),

        # spawn controller
        Node(
            package='controller_manager',
            executable='spawner.py',
            arguments=['differential_drive_controller'],
            output='screen',
        ),
    ])
