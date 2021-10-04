from setuptools import setup, find_packages


setup(
    name='fractal-napari-plugins-colletion:ptif-reader',
    version='1.1.0',
    author='Dario Vischi, Marco Franzon',
    author_email='dario.vischi@fmi.ch, marco.franzon@exact-lab.it',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license='BSD3',
    description=(
        'Plugin for reading multi-scale (pyramidal) TIFF files into Napari.'
    ),
    long_description=open('README.md').read(),
    python_requires='>=3.7',
    install_requires=[
        "napari[all] >= 0.4.7",
        "napari_plugin_engine >= 0.1.9",
        "dask[complete] >= 2021.4.0",
        "numpy >= 1.20.2",
        "imagecodecs >= 2020.5.30",
        "pylibtiff @ git+https://github.com/fractal-napari-plugins-collection/pylibtiff.git@v1.0.7",
    ],
    entry_points={
        'napari.plugin': [
            'napari_ptif_reader = napari_ptif_reader.napari_ptif_reader',
        ],
    },
    setup_requires=['pytest-runner',],
    tests_require=['pytest',],

)
