from setuptools import setup, find_packages

setup(
    name="target-nix-fetchers-fetch-git",
    version="1.0.0",
    description=("Fetch git repositories quickly."),
    license="MIT",
    keywords="nix, git",
    url="https://github.com/target/nix-fetchers",
    packages=find_packages(),
    py_modules=['fetchgit'],
    entry_points={
        'console_scripts': [
            'fetch-git = fetchgit.fetchgit:main'
        ]
    },
)
