import re
import requests
import config

requests.packages.urllib3.disable_warnings()


def get_task(rel_link):
    uri = config.octopus_uri + rel_link
    r = requests.get(uri, headers=config.octopus_headers, verify=False)
    return r.json()


def deploy_release(rel_id, env_id):
    uri = config.octopus_uri + "/api/deployments"
    r = requests.post(uri, headers=config.octopus_headers, verify=False,
                      json={'ReleaseId': rel_id, 'EnvironmentId': env_id})
    return r.json()


def get_environments():
    uri = config.octopus_uri + "/api/environments/all"
    r = requests.get(uri, headers=config.octopus_headers, verify=False)
    environments = {}
    for env in r.json():
        environments[env['Name']] = env['Id']
    return environments


def get_project_id(name):
    slug = re.sub("\.|\s", "-", name).lower()
    uri = config.octopus_uri + "/api/projects/" + slug
    r = requests.get(uri, headers=config.octopus_headers, verify=False)
    return r.json()['Id']


def get_deploy_for_version(proj_id, version):
    uri = config.octopus_uri + "/api/projects/{0}/releases/{1}".format(proj_id, version)
    r = requests.get(uri, headers=config.octopus_headers, verify=False)
    if r.status_code == 200:
        return r.json()
    return None


def get_specific_packages(deployment):
    uri = config.octopus_uri + deployment['Links']['ProjectDeploymentProcessSnapshot']
    r = requests.get(uri, headers=config.octopus_headers, verify=False)
    selected = []
    for p in deployment['SelectedPackages']:
        selected.append(p['StepName'])
    if r.status_code == 200:
        packages = []
        for step in r.json()['Steps']:
            if step['Name'] in selected:
                packages.append(step['Actions'][0]['Properties']['Octopus.Action.Package.PackageId'])
        return packages


def get_latest_packages(proj_id):
    uri = config.octopus_uri + "/api/deploymentprocesses/deploymentprocess-{0}/template".format(proj_id)
    r = requests.get(uri, headers=config.octopus_headers, verify=False)
    res = []
    for package in r.json()['Packages']:
        res.append(package['NuGetPackageId'])
    return res


def get_deploy_for_env(proj_id, env_id):
    uri = config.octopus_uri + "/api/deployments?environments={0}&projects={1}".format(env_id, proj_id)
    r = requests.get(uri, headers=config.octopus_headers, verify=False)
    if r.status_code == 200:
        uri = config.octopus_uri + r.json()['Items'][0]['Links']['Release']
        r = requests.get(uri, headers=config.octopus_headers, verify=False)
        if r.status_code == 200:
            return r.json()


def get_last_deploy_for_env(proj_id, env_id):
    uri = config.octopus_uri + "/api/deployments?environments={0}&projects={1}&take=4".format(env_id, proj_id)
    r = requests.get(uri, headers=config.octopus_headers, verify=False)
    return r.json()['Items'][0]


def get_last_failed_deploy_for_env(proj_id, env_id):
    uri = config.octopus_uri + "/api/deployments?environments={0}&projects={1}&take=4&taskState=Failed".format(env_id, proj_id)
    r = requests.get(uri, headers=config.octopus_headers, verify=False)
    if len(r.json()['Items']) > 0:
        return r.json()['Items'][0]
    else:
        return None


def get_latest_release(proj_id):
    uri = config.octopus_uri + "/api/projects/{0}/releases".format(proj_id)
    r = requests.get(uri, headers=config.octopus_headers, verify=False)
    return r.json()['Items'][0]
