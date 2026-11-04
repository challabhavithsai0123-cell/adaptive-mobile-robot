from setuptools import find_packages, setup

package_name = 'sentry_camera'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bhavisai',
    maintainer_email='bhavisai@example.com',
    description='ROS 2 webcam image publisher',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'camera_publisher = sentry_camera.camera_publisher:main',
	    'camera_subscriber = sentry_camera.camera_subscriber:main',
	    'target_controller = sentry_camera.target_controller:main',
            'obstacle_avoidance = sentry_camera.obstacle_avoidance:main',
            'data_logger = sentry_camera.data_logger:main',
        ],
    },
)
