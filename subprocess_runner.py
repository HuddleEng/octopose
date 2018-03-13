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

import subprocess
import sys


class SubprocessRunner:
    def __init__(self, verbose):
        """Runs subprocesses and manages logging of outputs"""
        self.verbose = verbose

    def run(self, command, error_msg):
        """run the specified command in a subprocess and log the stdout of the subprocess (if it errors or verbose is
        True) and the error_msg (if it errors)"""
        completed_process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)

        if completed_process.returncode != 0:
            print(completed_process.stdout.decode('utf-8'))
            print(error_msg, file=sys.stderr)
            exit()

        if self.verbose:
            print(completed_process.stdout.decode('utf-8'))
