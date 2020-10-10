from setuptools import setup, find_packages

with open('README.md', 'r') as input_file:
    long_description = input_file.read()

setup(
    name='python-switchbot',
    version='1.0.0',
    description='A Python library to control SwitchBot devices connected to SwitchBot Hub',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jonghwanhyeon/python-switchbot',
    author='Jonghwan Hyeon',
    author_email='hyeon0145@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Home Automation',
    ],
    keywords='switchbot',
    packages=find_packages(),
    install_requires=['pycognito', 'requests'],
)