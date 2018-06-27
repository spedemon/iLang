======
iLang
======

Inference language for medical imaging. It provides an inference engine for computational tasks 
such as reconstruction, registration, segmentation. 
iLang enables the definition of Probabilistic Graphical Models that operate on imaging data and implements 
optimizers and Bayesian samplers to perform inference (tomographic reconstruction, registration, segmentation). 


Installation
============

Linux, MacOsX, Windows
----------------------

There are two ways to install under Linux, MacOsX and Windows: 

1. If pip is installed: 

pip install ilang

2. Download source files, uncompress, at the command line cd to the downloaded folder and run: 

python setup.py build test install 


Features
========

Samplers
--------

1. Metropolis Hastings Markov Chain Monte Carlo

2. Hamiltonian Monte Carlo 

3. Langevin Adjusted Metropolis Hastings Markov Chain Monte Carlo 


Optimizers
----------

3. Gradient Descent

4. Stochastic Gradient Descent

5. Expectation Maximization



Website
=======

`ilang home page <http://tomographylab.scienceontheweb.net/software/ilang/>`_. 



