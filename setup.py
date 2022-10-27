from setuptools import find_packages, setup

setup(
    name='flask_app',
    version='1.0.0',
    description='COMP0034 Coursework 2 2021-22',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask'
        'plotly',
        'pandas',
        'dash',
        'dash-bootstrap-components'
    ],
)