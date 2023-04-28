from setuptools import find_packages, setup
import src.geeS2downloader

setup(
    name='geeS2Downloader',
    version=src.geeS2downloader.__version__,
    author="Maurício Cordeiro",
    author_email="cordmaur@gmail.com",
    url="https://github.com/cordmaur/GEES2Downloader",
    extras_require=dict(tests=['pytest']),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'setuptools>=58',
        'rasterio>=1.2.10',
        'earthengine-api~=0.1.290',
        'numpy>=1.20',
        'matplotlib>=3.4.3',
        'requests>=2.26.0',
        'geojson>=2.5.0',
        'tqdm>=4.62.3',
    ]
)

