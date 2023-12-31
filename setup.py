from setuptools import setup
import os
from glob import glob

package_name = 'gantry_test'

models_paths = []
directories= glob('models/')+glob('models/*/')+glob('models/*/*/')
for directory in directories:
    models_paths.append((os.path.join('share',package_name,directory),glob(f'{directory}/*.*')))
    
setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        #Add all xacro and URDF files that descripe the robot to the share directory
        (os.path.join('share',package_name,'description'),glob('description/*.xacro')),
        #Adding visual and collision mehses to the share directory
        (os.path.join('share',package_name,'meshes','visual'),glob('meshes/visual/*.stl')),
        (os.path.join('share',package_name,'meshes','collision'),glob('meshes/collision/*.dae')),
        #Adding Rviz2 configuration files
        (os.path.join('share',package_name,'rviz'),glob('rviz/*.rviz')),
        #Adding launch files
        (os.path.join('share',package_name,'launch'),glob('launch/*.launch.*')),
        (os.path.join('share',package_name,'config'),glob('config/*.yaml')),
        (os.path.join('share',package_name,'worlds'),glob('worlds/*')),
        (os.path.join('lib',package_name), glob('gantry_test/coordinatorClass.py'))
        ]+models_paths,
    
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Zein Alabedeen Barhoum and Rahaf Alshaowa',
    maintainer_email='zein.barhoum799@gmail.com',
    description='Franka Emika Panda manipulator playing chess',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'controller = gantry_test.controller:main',
            'multi_point_controller = gantry_test.multi_point_controller:main',
            'example_game = gantry_test.example_game:main',
            'spawn_object = gantry_test.spawn_object:main'
        ],
    },
)
