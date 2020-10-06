from setuptools import setup, find_packages

setup(
    name='python-switchbot',
    version='1.0.0',
    url='https://github.com/jonghwanhyeon/python-switchbot',
    author='Jonghwan Hyeon',
    author_email='hyeon0145@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords='switchbot',
    packages=find_packages(),
    install_requires=['pycognito', 'requests'],
)