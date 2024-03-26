import pathlib
from setuptools import find_packages, setup

setup(
    name="clspack",
    version="0.0.1",
    description="clspack is a python library that packagizes python classes",
    long_description=pathlib.Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    Homepage="https://github.com/not-lain/clspack",
    url="https://github.com/not-lain/clspack",
    Issues="https://github.com/not-lain/clspack/issues",
    authors=[{"name": "hafedh hichri", "email": "hhichri60@gmail.com"}],
    author_email="hhichri60@gmail.com",
    license="Apache 2.0 License",
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    classifiers=["Topic :: Utilities", "Programming Language :: Python :: 3.9"],
    requires=["setuptools", "wheel"],
)
