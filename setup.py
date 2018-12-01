import os
import sys
from setuptools import setup, find_packages
from tethys_apps.app_installation import custom_develop_command, custom_install_command

### Apps Definition ###
app_package = 'hydrologic_data_viewer_colombia'
release_package = 'tethysapp-' + app_package
app_class = 'hydrologic_data_viewer_colombia.app:HydrologicDataViewerColombia'
app_package_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tethysapp', app_package)

### Python Dependencies ###
dependencies = []

setup(
    name=release_package,
    version='0.0.1',
    tags='Hydrology',
    description='This app shows the historical data for the Colombian Hydrologic Alert System of tThe Institute of Hydrology, Meteorology and Environmental Studies - IDEAM',
    long_description='',
    keywords='',
    author='Jason Biesinger &amp; Jorge Luis Sanchez',
    author_email='',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['tethysapp', 'tethysapp.' + app_package],
    include_package_data=True,
    zip_safe=False,
    install_requires=dependencies,
    cmdclass={
        'install': custom_install_command(app_package, app_package_dir, dependencies),
        'develop': custom_develop_command(app_package, app_package_dir, dependencies)
    }
)
