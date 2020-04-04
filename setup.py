from setuptools import setup
setup(name='ytcrawl',
      version='0.1.0',
      packages=['ytcrawl'],
      entry_points={
          'console_scripts': [
              'ytcrawl = ytcrawl.command_line:main'
          ]
      },
      )
