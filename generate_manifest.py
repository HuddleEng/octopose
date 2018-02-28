""" This module generates manifest files based on Octopus Deploy releases"""

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

import json
import argparse
import octo
import config


def required_to_deploy_this_project(project, specific_projects):
    return len(specific_projects) == 0 or project in specific_projects


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--versions', default={}, type=json.loads, 
                        help="Supply specific versions of projects that you like in the manifest. "
                             "Supplied as a string dictionary. (Will need to escape quotes)")
    parser.add_argument('-e', '--environment', default="local", type=str,
                        help="Create a manifest based on an existing deploy to an environment.")
    parser.add_argument('-p', '--projects', nargs='+', default=None, type=str,
                        help="Supply specific projects, to only deploy those projects. "
                             "Supplied with spaces between project names.")

    args = parser.parse_args()
    specific_versions = args.versions
    env = args.environment
    specific_projects = args.projects

    environments = octo.get_environments()
    if env not in environments:
        print("please supply a valid environment and try again")
        exit()

    manifest = {'StagingLocation': config.STAGING, 'Projects': {}}
    for project in config.PROJECTS:
        project_id = octo.get_project_id(project)
        project_detail = {}
        if required_to_deploy_this_project(project, specific_projects):
            if project in specific_versions:
                if specific_versions[project] is None:
                    manifest['Projects'][project] = project_detail = None
                    continue
                release = octo.get_release_for_version(project_id, specific_versions[project])
                project_detail['Version'] = specific_versions[project]
                project_detail['Packages'] = octo.get_specific_packages(release)
            elif env != "local":
                print(project_id)
                print(environments[env])
                release = octo.get_release_for_env(project_id, environments[env])
                project_detail['Version'] = release['Version']
                packages = octo.get_specific_packages(release, environments[env])
                project_detail['Packages'] = packages
            else:
                project_detail['Packages'] = octo.get_latest_packages(project_id)

            manifest['Projects'][project] = project_detail

    print(json.dumps(manifest, indent=1))
