import pathlib
from setuptools import find_packages, setup

with open("src/clspack/__init__.py", "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name="clspack",
    version=version,
    description="clspack is a Python library that extracts and packages Python class source code",
    long_description=pathlib.Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/not-lain/clspack",
    project_urls={
        "Homepage": "https://github.com/not-lain/clspack",
        "Issues": "https://github.com/not-lain/clspack/issues",
    },
    author="hafedh hichri",
    author_email="hhichri60@gmail.com",
    license="Apache-2.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires=">=3.9",
    install_requires=[],
)
