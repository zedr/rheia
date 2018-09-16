from distutils.core import setup
from setuptools import find_packages

setup(
    name='rheia',
    version='0.6',
    package_dir={"": "src"},
    packages=find_packages('src'),
    include_package_data=True,
    entry_points={
        'console_scripts': ['rheia-manage=rheia.commands.manage:main']
    }
)
