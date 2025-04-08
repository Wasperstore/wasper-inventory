from setuptools import setup, find_packages

setup(
    name='wasper_inventory',
    version='1.0.0',
    description='Multi-company inventory and accounting system like Busy',
    author='Wasper Solutions',
    author_email='contact@waspersolution.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'frappe>=15.0.0',
        'erpnext>=15.0.0'
    ]
)
