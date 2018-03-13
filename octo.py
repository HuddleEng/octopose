""" This module is used to call through to the Octopus Deploy APIs"""

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

import re
import requests
import config

requests.packages.urllib3.disable_warnings()


def get_task(rel_link):
    """get_task will get the information about a specific deploy task"""
    uri = config.OCTOPUS_URI + rel_link
    r = requests.get(uri, headers=config.OCTOPUS_HEADERS, verify=False)
    return r.json()


def deploy_release(rel_id, env_id):
    """deploy_release will start deploying a release to a given environment"""
    uri = config.OCTOPUS_URI + "/api/deployments"
    r = requests.post(uri, headers=config.OCTOPUS_HEADERS, verify=False,
                      json={'ReleaseId': rel_id, 'EnvironmentId': env_id})
    return r.json()


def get_environments():
    """get_environments gets all environments that are accessible in Octopus Deploy"""
    uri = config.OCTOPUS_URI + "/api/environments/all"
    r = requests.get(uri, headers=config.OCTOPUS_HEADERS, verify=False)
    environments = {}
    for env in r.json():
        environments[env['Name']] = env['Id']
    return environments


def get_project_id(name):
    """get_project_id gets the id of a project given a friendly name"""
    slug = re.sub("\.|\s", "-", name).lower()
    uri = config.OCTOPUS_URI + "/api/projects/" + slug
    r = requests.get(uri, headers=config.OCTOPUS_HEADERS, verify=False)
    return r.json()['Id']


def get_release_for_version(proj_id, version):
    """get_deploy_for_version gets the deploy for a project and version"""
    uri = config.OCTOPUS_URI + "/api/projects/{0}/releases/{1}".format(proj_id, version)
    r = requests.get(uri, headers=config.OCTOPUS_HEADERS, verify=False)
    if r.status_code == 200:
        return r.json()
    return None


def get_release_for_env(proj_id, env_id):
    """get_deploy_for_env will get information about the last deploy of a project onto an environment"""
    uri = config.OCTOPUS_URI + "/api/deployments?environments={0}&projects={1}".format(env_id, proj_id)
    r = requests.get(uri, headers=config.OCTOPUS_HEADERS, verify=False)
    if r.status_code == 200:
        uri = config.OCTOPUS_URI + r.json()['Items'][0]['Links']['Release']
        r = requests.get(uri, headers=config.OCTOPUS_HEADERS, verify=False)
        if r.status_code == 200:
            return r.json()


def action_is_a_deployable_and_is_deployed_to_environment(action, environment_id):
    return action['ActionType'] == 'Octopus.TentaclePackage' and \
        (environment_id is None or len(action['Environments']) == 0 or environment_id in action['Environments'])


def get_specific_packages(release, environment_id=None):
    """get_specific_packages given a deployment get all the steps needed for a deploy"""
    uri = config.OCTOPUS_URI + release['Links']['ProjectDeploymentProcessSnapshot']
    r = requests.get(uri, headers=config.OCTOPUS_HEADERS, verify=False)
    if r.status_code == 200:
        packages = []
        steps = r.json()['Steps']
        for step in steps:
            for action in step['Actions']:
                if action_is_a_deployable_and_is_deployed_to_environment(action, environment_id):
                    package_id = action['Properties']['Octopus.Action.Package.PackageId']
                    if package_id not in packages:
                        packages.append(package_id)

        return packages


def get_latest_packages(proj_id):
    """get_latest_packages will find the latest deployment and packages for the project"""
    uri = config.OCTOPUS_URI + "/api/deploymentprocesses/deploymentprocess-{0}/template".format(proj_id)
    r = requests.get(uri, headers=config.OCTOPUS_HEADERS, verify=False)
    res = []
    for package in r.json()['Packages']:
        if package['NuGetPackageId'] not in res:
            res.append(package['NuGetPackageId'])
    return res


def get_last_deploy_for_env(proj_id, env_id):
    """get_last_deploy_for_env will get the information about the last deploy that was run in an enviroment"""
    uri = config.OCTOPUS_URI + "/api/deployments?environments={0}&projects={1}&take=4".format(env_id, proj_id)
    r = requests.get(uri, headers=config.OCTOPUS_HEADERS, verify=False)
    return r.json()['Items'][0]


def get_last_failed_deploy_for_env(proj_id, env_id):
    """get_last_failed_deploy_for_env will get the last failed deploy to an environment"""
    uri = config.OCTOPUS_URI + "/api/deployments?environments={0}&projects={1}&take=4&taskState=Failed".format(env_id, proj_id)
    r = requests.get(uri, headers=config.OCTOPUS_HEADERS, verify=False)
    if len(r.json()['Items']) > 0:
        return r.json()['Items'][0]
    else:
        return None


def get_latest_release(proj_id):
    """get_latest_release gets the latest release that was created for a project"""
    uri = config.OCTOPUS_URI + "/api/projects/{0}/releases".format(proj_id)
    r = requests.get(uri, headers=config.OCTOPUS_HEADERS, verify=False)
    return r.json()['Items'][0]
