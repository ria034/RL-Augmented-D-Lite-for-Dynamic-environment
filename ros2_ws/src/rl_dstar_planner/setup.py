from setuptools import setup

# TODO: fill in once package structure is finalized
package_name = "rl_dstar_planner"

setup(
    name=package_name,
    version="0.0.1",
    packages=[package_name],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Ria Mendes",
    maintainer_email="mendes.ri@northeastern.edu",
    description="RL-integrated D* Lite motion planner (ROS2 package)",
    license="TODO",
    entry_points={
        "console_scripts": [
            "planner_node = rl_dstar_planner.planner_node:main",
        ],
    },
)
