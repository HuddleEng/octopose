# MIT License
#
# Copyright (c) 2018 Huddle
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from setuptools import setup

setup(
    name="octopose",
    packages=["octopose"],
    entry_points={
        "console_scripts": ['octopose = octopose.octopose:main']
    },
    version="0.1.2",
    description="Command line tools for managing local and remote octopus deploys using manifests.",
    author="George Ayris",
    author_email="george.ayris@huddle.com",
    url="https://github.com/HuddleEng/octopose",
    install_requires=[
        'certifi>=2017.7.27.1',
        'chardet>=3.0.4',
        'idna>=2.6',
        'requests>=2.18.4',
        'urllib3>=1.22',
        'pyyaml==3.12'
    ],
    include_package_data=True
)

