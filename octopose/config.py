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

import yaml
import os

config = None
try:
    with open(os.path.expanduser("~\\.octopose\\config.yaml"), 'r') as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.SafeLoader)
except FileNotFoundError:
    print("""Config file not found. Octopose expects a ~\\.octopose\\config.yaml in the following format:
OCTOPUS_URI: ""
OCTOPUS_HEADERS:
  "x-octopus-apikey": ""
PROJECTS:
  - ""
STAGING: "~\\\\StagingLocation"
PACKAGE_SOURCES:
  - \"\"""")
    exit(1)

OCTOPUS_URI = config['OCTOPUS_URI']
OCTOPUS_HEADERS = config['OCTOPUS_HEADERS']
PROJECTS = config['PROJECTS']
STAGING = config['STAGING']
PACKAGE_SOURCES = config['PACKAGE_SOURCES']
