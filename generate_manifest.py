import json
import argparse
import octo
import config
from pprint import pprint

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--versions', default={}, type=json.loads)
    parser.add_argument('-e', '--environment', default="local", type=str)

    args = parser.parse_args()
    specific_versions = args.versions
    env = args.environment

    manifest = {'StagingLocation': config.staging, 'Projects': {}}
    environments = octo.get_environments()

    for project in config.projects:
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
