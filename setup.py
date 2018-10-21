import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drfaddons",
    version=__import__('drfaddons').__version__,
    author=__import__('drfaddons').__author__,
    author_email="pypidev@civilmachines.com",
    description="A collection package for Django REST Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=__import__('drfaddons').__license__,
    url="https://github.com/101Loop/drf-addons",
    python_requires=">=3.4",
    install_requires=open('requirements.txt').read().split(),
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP'
    ),
)
