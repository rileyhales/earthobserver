import os
import sys
from setuptools import setup, find_packages
from tethys_apps.app_installation import custom_develop_command, custom_install_command

# -- Apps Definition -- #
app_package = 'earthobserver'
release_package = 'tethysapp-' + app_package
app_class = 'earthobserver.app:Earthobserver'
app_package_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tethysapp', app_package)

# -- Python Dependencies -- #
dependencies = []

setup(
    name=release_package,
    version='0.0.1',
    tags='&quot;Earth Observations&quot;, &quot;Time Series&quot;, &quot;Maps&quot;, &quot;Charts&quot;, &quot;Downloads&quot;',
    description='A tethys app for visualizing Earth Observation r(EO) products  including GLDAS and GFS',
    long_description='',
    keywords='',
    author='Riley Hales',
    author_email='',
    url='',
    license='BSD 3-Clause License',
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