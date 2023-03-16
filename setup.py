from setuptools import find_packages, setup

with open("requirements.txt") as req:
    requirements = req.readlines()

with open("license.txt") as l:
    lic = l.read()

setup(
    name='PyFSMwDB',
    packages=find_packages(include=['PyFSMwDB']),
    version='1.0.0',
    description='A python lib for FSM with DB',
    author='Arian Asghari, Andreas Söderman, Felix Mårtensson, Mattias Öz',
    license=lic,
    python_requires=">=3.10",
    install_requires=requirements,
    setup_requires=[],
    tests_require=[],
    test_suite='',
)
