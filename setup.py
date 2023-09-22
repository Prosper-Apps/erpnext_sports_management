from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sports_management/__init__.py
from sports_management import __version__ as version

setup(
	name="sports_management",
	version=version,
	description="Manage many sports",
	author="KAINOTOMO PH LTD",
	author_email="info@kainotomo.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
