""" Pretty standard setup.py file, I think"""

import setuptools

setuptools.setup(
    name="email_blast",
    version="1",
    author="Max Caudle",
    author_email="maxwell.caudle@gmail.com",
    description="A tool to send emails based on local weather to users.",

    url="https://github.com/MasonCaiby/weather_app",
    packages=['src'],
    package_data={
        'src': ['*'] # want to make sure we grabe the config file and cities file
    }
    ,
    entry_points = {
        'console_scripts': ['email_blast=src.__main__:main'],
    },
)
