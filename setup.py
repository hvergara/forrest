from setuptools import setup, find_packages

setup(
    name='forrest',
    version='0.0.8',
    description='Utility for run ephemeral applications on cloud instances',
    author='Hector Vergara',
    author_email='hvergara@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'forrest = forrest:cli'
        ]
    },
    install_requires = [
        'awscli'
    ]
)
