from setuptools import setup

setup(
    name='test2',
    entry_points={
        'console_scripts': [
            'test2=test2:main',
        ],
    }
)