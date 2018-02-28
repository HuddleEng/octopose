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


import octo
import time


def deploy_to_environment(env_id, wait, force, data):
    """deploy_to_environment will use the manifest to do a remote deploy into another environment"""
    deployments = {}
    for key, value in data['Projects'].items():
        if value is None:
            continue

        project_name = key
        proj_id = octo.get_project_id(project_name)

        if 'Version' not in value:
            latest_release = octo.get_latest_release(proj_id)
            version = latest_release['Version']
        else:
            version = value['Version']

        if version is None:
            continue

        to_deploy = octo.get_deploy_for_version(proj_id, version)
        current_deploy = octo.get_deploy_for_env(proj_id, env_id)
        if version == current_deploy['Version']:
            last_deploy = octo.get_last_deploy_for_env(proj_id, env_id)
            last_fail = octo.get_last_failed_deploy_for_env(proj_id, env_id)
            if (last_fail is not None) and (last_deploy['TaskId'] == last_fail['TaskId']):
                print("Failed Last Deploy - will try again")
            elif force:
                print("Forcing Deploy")
            else:
                deployments[project_name] = {'Link': None,
                                             'Status': 'Already Deployed',
                                             'Version': version}
                continue

        if to_deploy:
            print("{0} - Deploying {1}".format(project_name, version))
            for package in to_deploy['SelectedPackages']:
                print("  - {0}".format(package['StepName']))
            deploy = octo.deploy_release(to_deploy['Id'], env_id)
            deployments[project_name] = {'Link': deploy['Links']['Task'],
                                         'Status': 'Queued',
                                         'Version': version}

    if wait:
        pending = len(deployments)
        while pending > 0:
            for key, value in deployments.items():
                task_link = value['Link']
                if task_link is None:
                    continue
                task = octo.get_task(task_link)
                if task['State'] == 'Failed':
                    deployments[key]['Link'] = None
                    deployments[key]['Status'] = 'Failed'
                else:
                    deployments[key]['Status'] = task['State']

            pending = 0
            for key, value in deployments.items():
                status = value['Status']
                if (status == 'Queued') or (status == 'Executing'):
                    pending = pending + 1
                time.sleep(10)

    for key, value in deployments.items():
        print("{0} - {1} - {2}".format(value['Status'], key,
                                       value['Version']))