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

import json
import remote_deploy
import argparse
from local_deploy import LocalDeploy
import sys
import octo


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('rb'), default=sys.stdin)
    parser.add_argument('-e', '--environment', default="local", type=str,
                        help="Supply the environment that you would like to deploy to.")
    parser.add_argument('--wait', action="store_true", help="Wait and poll for deploy")
    parser.add_argument('--force', action='store_true', help='Force deployment')
    parser.add_argument('-v', '--verbose', action='store_true', help="Do not suppress logging from deploy scripts.")

    args = parser.parse_args()
    environment = args.environment
    wait = args.wait
    force = args.force
    verbose = args.verbose

    environments = octo.get_environments()
    if environment in environments:
        env_id = environments[environment]
    else:
        print("please supply a valid environment and try again")
        exit()

    infile_contents = args.infile.read()
    try:
        # If the infile is supplied (rather than coming from stdin) we read as bytes and decode using utf-16 because
        # it appears Powershell uses this by default when using the > operator to create a file
        manifest_string = infile_contents.decode('utf-16')
    except AttributeError:
        manifest_string = infile_contents

    manifest = json.loads(manifest_string)

    if environment != "local":
        remote_deploy.deploy_to_environment(env_id, wait, force, manifest)
    else:
        LocalDeploy(verbose).deploy(manifest)
