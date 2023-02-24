from setuptools import find_packages, setup

with open("requirements.txt") as req:
    requirements = req.readlines()   # might need to port it to list

setup(
    name='FSM',
    packages=find_packages(include=['finite_state_machine_lib']),
    version='0.1.5',
    description='My first Python library',
    author='Me',
    license='ME',
    python_requires=">=3.10", # might be strictly ">3.10"
    install_requires=requirements,
    setup_requires=[],  # tror inte den här är nödvändig
    tests_require=[],   # skulle gissa att den här bara är specifikt för tester
    test_suite= '',
)
