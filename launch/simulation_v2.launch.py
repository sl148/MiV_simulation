import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import SetEnvironmentVariable
import xacro


def generate_launch_description():

    pkg_name = 'gantry_test' #the package name
    
    pkg_share= get_package_share_directory(pkg_name)
    
    gantry_path = 'description/gantry.urdf.xacro'
    mea_path = 'description/mea.urdf.xacro'

    rviz_relative_path= 'rviz/config.rviz'

    rviz_absolute_path = os.path.join(pkg_share, rviz_relative_path)
    
    # extracting the robot deffinition from the xacro file
    gantry_file = os.path.join(pkg_share, gantry_path)
    gantry_description_content = xacro.process_file(gantry_file).toxml()

    mea_file = os.path.join(pkg_share, mea_path)
    mea_description_content = xacro.process_file(mea_file).toxml()
    
    # add the path to the model file to  gazebo
    # models_path = os.path.join(get_package_share_directory(pkg_name),'models')

    # if 'GAZEBO_MODEL_PATH' in os.environ:
    #     model_path =  os.environ['GAZEBO_MODEL_PATH'] + ':' + models_path
    # else:
    #     model_path =  models_path

    world_path=os.path.join(pkg_share, 'worlds', 'workstation.world')
    
    # robot state publisher node
    node_gantry_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': gantry_description_content}]
    )

    node_mea_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': mea_description_content}]
    )

    # Rviz2 node
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments= ['-d', rviz_absolute_path]
    )
    # Gazebo launch file
    launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
        launch_arguments={'world' : world_path}.items()
    )
    # entity spawn node (to spawn the robot from the /robot_description topic)
    node_spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'gantry'],
                        output='screen')
    
    # node_spawn_entity_mea = Node(package='gazebo_ros', executable='spawn_entity.py',
    #                     arguments=['-topic', 'robot_description',
    #                                '-entity', 'mea'],
    #                     output='screen')
    
    # spawning the joint broadcaster
    spawn_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )
    
    spawn_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_trajectory_controller"],
        output="screen",
    )




    # Run the nodes
    return LaunchDescription([
        # SetEnvironmentVariable(name='GAZEBO_MODEL_PATH', value=model_path),
        node_gantry_state_publisher,
        node_mea_state_publisher,
        launch_gazebo,
        node_spawn_entity,
        # node_spawn_entity_mea,
        # node_rviz,
        spawn_broadcaster,
        spawn_controller,
    ])
