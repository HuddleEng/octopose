import json
import octo
import time
import argparse
import shutil
import os
import nu
from pprint import pprint

def deploy_to_environment(environment, wait, force, data):
    deployments = {}
    for key, value in data['Projects'].items():
        if value is None:
            continue
        project_name = key
        proj_id = octo.get_project_id(project_name)
        if 'Version' not in value:
            version = None
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


def deploy_local(data):
    staging = os.path.normpath(data['StagingLocation'])
    if os.path.exists(staging):
        shutil.rmtree(staging)
    os.makedirs(staging)

    for key, value in data['Projects'].items():
        project_name = key
        proj_id = octo.get_project_id(project_name)
        if 'Version' not in value:
            version = None
            latest_release = octo.get_latest_release(proj_id)
            version = latest_release['Version']
        else:
            version = value['Version']

        if version is None:
            continue
        for package in value['Packages']:
            nu.get_deployable(package, version, staging)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--environment', default="local", type=str)
    parser.add_argument('--wait', action="store_true",
                        help="Wait and poll for deploy")
    parser.add_argument('--force', action='store_true',
                        help='Force deployment')
    args = parser.parse_args()
    environment = args.environment
    wait = args.wait
    force = args.force

    environments = octo.get_environments()
    if environment in environments:
        env_id = environments[environment]
    else:
        print("please supply a valid environment and try again")
        exit()

    with open('manifest.json') as data_file:
        data = json.load(data_file)
    
    if environment is not "local":
        deploy_to_environment(environment, wait, force, data)
    else:
        deploy_local(data)
