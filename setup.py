from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='game-of-life-nodeps',
    version='0.0.2',
    description='Game of Life with only Python builtin libraries',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/johnliu55tw/game-of-life',
    author='John Liu',
    author_email='johnliu55tw@gmail.com',
    keywords=['game-of-life tk tkinter simple'],
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'game-of-life=game_of_life.cli:main'
        ],
    },
)
