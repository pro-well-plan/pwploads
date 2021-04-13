from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pwploads',
    packages=['pwploads', 'pwploads.axial', 'pwploads.burst', 'pwploads.collapse'],
    version='0.4.1',
    license='LGPL v3',
    description='Load Cases for Well Design',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Pro Well Plan AS',
    author_email='juan@prowellplan.com',
    url='https://github.com/pro-well-plan/pwploads',
    keywords='well design',
    classifiers=['Programming Language :: Python :: 3',
                 'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                 'Natural Language :: English',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Software Development',
                 'Topic :: Software Development :: Libraries',
                 'Topic :: Utilities'],
    install_requires=['numpy', 'plotly', 'torque_drag', 'well_profile']
)
