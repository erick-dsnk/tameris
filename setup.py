from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_desc = f.read()

setup(
    name='tameris',
    version='0.1.1',
    description='A Python Discord API Wrapper based around customizability and expandability!',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author='Tabacaru Eric',
    author_email='erick.8bld@gmail.com',
    url='https://github.com/erick-dsnk/tameris',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.5'
)