from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="ai-battle",
    version="0.0.1",
    description="A ai battle game.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ian Laird",
    author_email="irlaird@gmail.com",
    url="https://github.com/en0/ai-battle",
    install_requires=[
        "pygame==2.1.2",
        "pyioc3==1.3.0",
        ],
    packages=["airena"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
