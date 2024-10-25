from setuptools import setup, find_packages

setup(
    name="farwas",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["zoneinfo;python_version<'3.9'"],
    python_requires=">=3.9",
)
