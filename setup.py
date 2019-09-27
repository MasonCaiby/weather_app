import setuptools

setuptools.setup(
    name="email_blast",
    version="1",
    author="Max Caudle",
    author_email="maxwell.caudle@gmail.com",
    description="A tool to send emails based on local weather to users.",

    url="https://github.com/MasonCaiby/weather_app",
    packages = ['emailer'],
    entry_points = {
        'console_scripts': ['email_blast=emailer.__main__:main'],
    },
)
