from setuptools import setup, find_packages


# HACK: allows the execution of this script via pip, e.g. on a CI server.
# pip tries to download private git repositories also they are already
# installed on the system - which failes due missing credentials.
private_install_requires = []
try:
    import pylibtiff
except ModuleNotFoundError:
    private_install_requires.append(
        "pylibtiff @ git+https://github.com/fractal-analytics-platform/pylibtiff.git@v1.0.7"
    )


setup(
    name='fractal-napari-plugins-colletion:ptif-reader',
    version='1.0.0',
    author='Dario Vischi, Marco Franzon',
    author_email='dario.vischi@fmi.ch, marco.franzon@exact-lab.it',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license='MIT',
    description=(
        'Plugins for reading multi-scale/multi-dimensional images/shapes into Napari.'
    ),
    long_description=open('README.md').read(),
    python_requires='>=3.6',
    install_requires=[
        "napari[all] >= 0.3.8",
        "napari_plugin_engine >= 0.1.9",
        "dask[complete] >= 2021.3.0",
        "numpy >= 1.19.5",
        "imagecodecs >= 2020.5.30",
        *private_install_requires
    ],
    entry_points={
        'napari.plugin': [
            'napari_ptif_reader = napari_ptif_reader.napari_ptif_reader',
        ],
    },
    setup_requires=['pytest-runner',],
    tests_require=['pytest',],

)
