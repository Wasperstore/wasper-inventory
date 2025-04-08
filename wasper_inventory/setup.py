from setuptools import setup, find_packages

setup(
    name="wasper_inventory",
    version="1.0.0",
    description="Wasper Inventory Solution",
    author="Wasper",
    author_email="support@wasper.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "frappe",
    ]
) 