from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ml_belt',
    version='0.1',
    description='The machine learning utility belt',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://adrianogfreitas.github.io/ml_belt/',
    author='Adriano Freitas',
    author_email='agf.adriano@gmail.com',
    packages=find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False)
