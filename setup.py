import io
from setuptools import find_packages, setup

def long_description():
  with io.open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()
  return readme

setup(name='lotto',
  version='1.0',
  description='practice python with solving algorithms',
  long_description=long_description(),
  url='https://github.com/dnjsakf/lotto',
  author='dnjsakf',
  author_email='dnjsakf@naver.com',
  license='MIT',
  packages=find_packages(),
  classifiers=[
    # 'Programming Language :: Python :: 2.7',
    # 'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6.8',
    ],
  zip_safe=False)