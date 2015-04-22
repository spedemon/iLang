
# iLang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 
# Martinos Center for Biomedical Imaging - MGH/Harvard University, Jan 2015


from setuptools import setup
from glob import glob 

setup(
    name='ilang',
    version='0.2.1',
    author='Stefano Pedemonte',
    author_email='stefano.pedemonte@gmail.com',
	packages=['ilang', 'ilang.test','ilang.examples',],
    test_suite="ilang.test",
    scripts=[],
    url='http://www.occiput.io',
    license='LICENSE.txt',
    description='Inference Language for Volumetric Imaging',
    long_description=open('README.rst').read(),
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    install_requires=[
        "numpy >= 1.6.0",
        "pil >= 1.0.0",
        "DisplayNode >= 0.2.0", 
        "nibabel >= 2.0.0",
        "ipy_table >= 1.11.0", 
    ],
)


