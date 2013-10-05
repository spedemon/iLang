
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


from distutils.core import setup

setup(
    name='ilang',
    version='0.1.0',
    author='Stefano Pedemonte',
    author_email='stefano.pedemonte@gmail.com',
    packages=['ilang', 'ilang.test','ilang.webgui','ilang.examples'],
    package_data={'ilang.webgui':['*.html','*.js']},
    #scripts=['bin/multivariate_normal.py','bin/sum_poisson.py'],
    url='http://ilang.com/',
    license='LICENSE.txt',
    description='Imaging Inference Language.',
    long_description=open('README.txt').read(),
    install_requires=[
        #"NiftyRec >= 1.7.0",
    ],
)


