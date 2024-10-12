from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Define the URDF file path
    urdf_file = os.path.join(
        get_package_share_directory('diff_drive'),
        'urdf',
        'robot_model.urdf'
    )
    
    rviz_config_path = os.path.join(
        get_package_share_directory('diff_drive'),
        'rviz',
        'diff_drive_config.rviz'
    )

    # Ensure the URDF file is read correctly
    with open(urdf_file, 'r') as file:
        robot_description = file.read()

    return LaunchDescription([
        DeclareLaunchArgument(
            name='use_sim_time',
            default_value='false',
            description='Use simulation time'
        ),

        # Load the URDF model in robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description, 'use_sim_time': LaunchConfiguration('use_sim_time')}],
            arguments=['--ros-args', '--log-level', 'debug']
        ),

        # Add joint_state_publisher_gui
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen',
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
            arguments=['--ros-args', '--log-level', 'debug']
        ),

        # Run RViz2 and load the RViz config file
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_path, '--ros-args', '--log-level', 'debug'],
            output='screen'
        ),
    ])