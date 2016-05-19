from setuptools import setup, find_packages
setup(

    name = "senseictl",
    version = "0.1",
    packages = find_packages(),

    entry_points = {
        'console_scripts': [
            'senseictl = sensei.senseictl:main'
        ]
    },

    # metadata for upload to PyPI
    author = "Demetrio Menezes Neto",
    author_email = "neto.demetrio@gmail.com",
    description = "A tool to configure the SteelSeries Sensei Raw Gaming Mouse",

    license = "GPL2",
    keywords = "steelseries sensei",
    url = "https://github.com/dneto/senseictl",

    install_requires=[
        'ioctl-opt>=1.2',
        'pyudev>=0.16',
        'webcolors>=1.4',
        'pyyaml>=3.10'
    ],

)
