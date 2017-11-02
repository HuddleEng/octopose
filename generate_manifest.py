""" This module generates manifest files based on Octopus Deploy releases"""

# MIT License
#
# Copyright (c) 2017 Huddle
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

import json
import argparse
from pprint import pprint

import octo
import config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--versions', default={}, type=json.loads, 
                        help="Supply specific versions of projects that you like in the manifest.")
    parser.add_argument('-e', '--environment', default="local", type=str,
                        help="Create a manifest based on an existing deploy to an environment.")

    args = parser.parse_args()
    specific_versions = args.versions
    env = args.environment

    manifest = {'StagingLocation': config.STAGING, 'Projects': {}}
    environments = octo.get_environments()
    if env not in environments:
        print("please supply a valid environment and try again")
        exit()

    for project in config.PROJECTS:
        proj_id = octo.get_project_id(project)
        project_detail = {}
        if project in specific_versions:
            deployment = octo.get_deploy_for_version(proj_id, specific_versions[project])
            project_detail['Version'] = specific_versions[project]
            project_detail['Packages'] = octo.get_specific_packages(deployment)
        elif env != "local":
            deployment = octo.get_deploy_for_env(proj_id, environments[env])
            project_detail['Version'] = deployment['Version']
            project_detail['Packages'] = octo.get_specific_packages(deployment)
        else:
            project_detail['Packages'] = octo.get_latest_packages(proj_id)
        manifest['Projects'][project] = project_detail

    pprint(manifest)
    with open('manifest.json', 'w') as outfile:
        json.dump(manifest, outfile)
