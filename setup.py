from setuptools import setup, find_packages

setup(
    name='json_pointer',
    author='Chris Ermel',
    author_email='ermel272@gmail.com',
    version='0.0.0',
    description='An implementation of IETF RFC 6901',
    license='MIT',
    url='github.com/ermel272/json-pointer',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='JSON pointer IETF RFC 6901',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True
)
