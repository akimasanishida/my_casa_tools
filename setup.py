from setuptools import setup, find_packages

setup(
    name='skrbcr_casa_scripts',
    version='0.1',
    description='A collection of scripts for CASA',
    author='Akimasa NISHIDA',
    packages=find_packages(),
    install_requires=[ 'numpy', 'matplotlib' ],
    license='MIT',
)
