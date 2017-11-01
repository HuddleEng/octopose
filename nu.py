import config
import subprocess
import os

def get_deployable(name, version, staging_location):
    for source in config.package_sources:
        FNULL = open(os.devnull, 'w')    #use this if you want to suppress output to stdout from the subprocess
        args = "third_party\\NuGet.exe install {0} -Source {1} -OutputDirectory {2}".format(name, source, staging_location)
        if version is not None:
            args = args + " -Version {0}".format(version)
        subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)