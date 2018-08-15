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

import argparse
import sys

from octopose import generate_manifest, deploy, __version__


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, prog='octopose',
                                     description='Octopose is a manifest/state driven deployment framework for Octopus Deploy.',
                                     usage='%(prog)s [generate] [deploy] [-h] [--version]',
                                     epilog='For documentation see https://github.com/HuddleEng/octopose/blob/master/README.md')
    parser.add_argument('command', choices=['generate', 'deploy'],
                        help='generate      Creates a new manifest file from the projects in config.yaml.\r'
                             'deploy        Deploys the state described in the specified manifest file.')

    parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(__version__))

    args = parser.parse_args(sys.argv[1:2])

    if args.command == 'generate':
        generate_manifest.main()
    elif args.command == 'deploy':
        deploy.main()
    else:
        parser.print_help()


