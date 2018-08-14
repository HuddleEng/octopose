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

import os
import shutil
import sys

from octopose import nu, octo, subprocess_runner
from enum import Enum


class DeployStatus(Enum):
    Success = 1
    Failure = 2
    Skipped = 3

class LocalDeploy:
    def __init__(self, verbose):
        """LocalDeploy deploys Octopus packages (on the current machine) without needing a tentacle service"""
        self.subprocess_runner = subprocess_runner.SubprocessRunner(verbose)
        self.nu = nu.Nu(self.subprocess_runner)

    def invoke_deploy(self, step_path):
        """invoke_deploy start a deploy for a given powershell script (*Deploy.ps1)"""
        print("- {0}".format(step_path))
        if os.path.exists(step_path):
            if is_64_bit_python_installation():
                args = "powershell.exe {0}".format(step_path)
            else:
                args = "c:\\windows\\sysnative\\cmd.exe /c powershell.exe {0}".format(step_path)

            succeeded, message = self.subprocess_runner.run(args, "Running of {0} failed".format(step_path), step_path)
            if succeeded:
                return DeployStatus.Success, message
            else:
                return DeployStatus.Failure, message
            #return self.subprocess_runner.run(args, "Running of {0} failed".format(step_path), step_path)
        else:
            print("Can't find path - skipping this file")
            return DeployStatus.Success, None

    def deploy(self, force, data):
        """deploy will use the manifest to deploy all packages to the local machine"""
        staging = os.path.normpath(data['StagingLocation'])
        if os.path.exists(staging):
            if force:
                shutil.rmtree(staging)
                os.makedirs(staging, mode=0o777)
        else:
            os.makedirs(staging, mode=0o777)

        deployment_results = []
        for key, value in data['Projects'].items():
            successful_deployment = DeployStatus.Failure
            error_message = None
            project_name = key
            proj_id = octo.get_project_id(project_name)
            if 'Version' not in value:
                latest_release = octo.get_latest_release(proj_id)
                release_version = latest_release['Version']
            else:
                release_version = value['Version']

            print("{0} - {1}".format(project_name, release_version))
            for package in get_package_versions(proj_id, release_version, value['Packages']):
                package_name = package['PackageId']
                version = package['Version']
                print("- NuGet - {0} - {1}".format(package_name, version))
                package_path = os.path.join(staging, "{0}.{1}".format(package_name, version))

                if os.path.exists(package_path):
                    print("Package exists in staging area {0} skipping install".format(package_path))
                    successful_deployment = DeployStatus.Skipped
                    continue

                self.nu.get_deployable(package_name, version, staging)

                for script in ["{0}\PreDeploy.ps1", "{0}\Deploy.ps1", "{0}\PostDeploy.ps1"]:
                    successful_deployment, error_message = self.invoke_deploy(script.format(package_path))
                    if successful_deployment == DeployStatus.Failure:
                        break

                if successful_deployment == DeployStatus.Failure:
                    print("WARNING: Deploy of {0} has failed. Skipping any remaining packages in the project.".format(project_name))
                    shutil.rmtree(package_path)
                    break

            deployment_results.append((project_name, release_version, successful_deployment, error_message))

        print_deployment_results(deployment_results)

        all_deployments_succeeded = all(result[2] for result in deployment_results)
        if not all_deployments_succeeded:
            exit(1)


def get_package_versions(proj_id, release_version, package_ids_to_deploy):
    release = octo.get_release_for_version(proj_id, release_version)
    step_names_and_versions = release['SelectedPackages']
    package_ids_and_step_names = octo.get_specific_packages(release)

    packages_to_deploy = []
    for step_name_and_version in step_names_and_versions:
        for package_id_and_step_name in package_ids_and_step_names:

            if step_name_and_version['StepName'] == package_id_and_step_name['StepName']:

                if package_id_and_step_name['PackageId'] in package_ids_to_deploy:
                    packages_to_deploy.append({"PackageId": package_id_and_step_name['PackageId'],
                                               "Version": step_name_and_version['Version']})

                break

    return packages_to_deploy


def is_64_bit_python_installation():
    return sys.maxsize > 2**32


def print_deployment_results(deployment_results):
    print("")
    print("-- Error Messages --")
    for result in deployment_results:
        if result[2] == DeployStatus.Failure:
            print(result[3])

    print("")
    print("-- Deployment Results --")
    for result in deployment_results:
        print("{0} - {1} - {2}".format(result[0], result[1], result[2]))
