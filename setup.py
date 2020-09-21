from setuptools import setup, find_packages
from readme_renderer.markdown import render

long_description = ""
with open('README.md', encoding='utf-8') as file:
  long_description = file.read()

setup(
    name='checklist-seo',
    version='0.0.4',
    license='MIT',
    author='RIGAUDIE David',
    url='https://github.com/itarverne/checklist-seo',
    description='The full checklist to provide tools inside Django in order to write right content',
    long_description=render(long_description),
    packages=find_packages(exclude=["testing"]),
    long_description_content_type="text/markdown",
    platforms='any',
    python_requires='>=3.7',
    install_requires=['Django>=3.1,<3.2'],
    include_package_data=True,
    test_suite='testing.test_api',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django :: 3.1'
    ],
)
