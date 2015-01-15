
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


from setuptools import setup
from glob import glob 

setup(
    name='ilang',
    version='0.1.0',
    author='Stefano Pedemonte',
    author_email='stefano.pedemonte@gmail.com',
	packages=['ilang', 'ilang.tests','ilang.examples',],
    test_suite="ilang.tests",
    scripts=[],
    url='http://niftyrec.scienceontheweb.net/',
    license='LICENSE.txt',
    description='Imaging Inference Language.',
    long_description=open('README.txt').read(),
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
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
        "DisplayNode >= 0.1.0", 
        "nibabel >= 1.3.0",
        "ipy_table >= 1.11.0", 
    ],
)


