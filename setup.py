import os

from setuptools import find_packages, setup

install_requires = [
    "Click>=7.0",
    "PyYAML>=5.1.2",
    "yamlordereddictloader",
    "jsonschema>=3.0.0",
    "semver>=2.8.1",
    "requests",
    "ruamel.yaml",
    "modelcatalog-api"
]


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def find_package_data(dirname):
    def find_paths(dirname):
        items = []
        for fname in os.listdir(dirname):
            path = os.path.join(dirname, fname)
            if os.path.isdir(path):
                items += find_paths(path)
            elif not path.endswith(".py") and not path.endswith(".pyc"):
                items.append(path)
        return items

    items = find_paths(dirname)
    return [os.path.relpath(path, dirname) for path in items]


version = {}
with open("src/caps/__init__.py") as fp:
    exec(fp.read(), version)


setup(
    name="caps-cli",
    version=version["__version__"],
    author="Dhruv Patel",
    author_email="dhruvpa@isi.edu",
    description=__doc__,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license="Apache-2",
    url="https://github.com/mintproject/ModelCatalogInsertion",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
    ],
    entry_points={"console_scripts": ["caps-cli = caps.__main__:cli"]},
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["caps.tests*"]),
    package_data={"caps-cli": find_package_data("src/caps")},
    exclude_package_data={"caps-cli": ["tests/*"]},
    zip_safe=False,
    install_requires=install_requires,
    python_requires=">=3.5.0",
)
