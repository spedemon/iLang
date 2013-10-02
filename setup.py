from distutils.core import setup

setup(
    name='ilang',
    version='0.1.0',
    author='Stefano Pedemonte',
    author_email='stefano.pedemonte@gmail.com',
    packages=['ilang', 'ilang.test'],
    scripts=['bin/multivariate_normal.py','bin/sum_poisson.py'],
    url='http://ilang.com/',
    license='LICENSE.txt',
    description='Imaging Inference Language.',
    long_description=open('README.txt').read(),
    install_requires=[
        "NiftyRec >= 1.7.0",
        "nose == 1.4.0",
    ],
)


