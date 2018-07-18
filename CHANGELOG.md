# Next Release

# v0.2.4
* Improve help text ([#35](https://github.com/HuddleEng/octopose/issues/35))
* Update setup.py info ([#39](https://github.com/HuddleEng/octopose/issues/39))

# v0.2.3
* Allow deploying of packages that have a different version to the release version ([#33](https://github.com/HuddleEng/octopose/issues/33))
* Improve logging when can't find *.ps1 file ([#32](https://github.com/HuddleEng/octopose/issues/32))
* Only fail deploy for given project (and not all projects), if a package deploy step fails ([#34](https://github.com/HuddleEng/octopose/34))

# v0.2.2
* Fix local deploy not downloading correct packages when specifying version ([#30](https://github.com/HuddleEng/octopose/issues/30))

# v0.2.1
* Fix installation issue

# v0.2.0

* Move configuration files to well known location ([#24](https://github.com/HuddleEng/octopose/issues/24))
* Make Octopose `pip install` friendly ([#10](https://github.com/HuddleEng/octopose/issues/10))
* Fix bug with `octopose generate` ([#28](https://github.com/HuddleEng/octopose/issues/28))

# v0.1.0

First Release of Octopose.

* Unix style piping between commands over writing directly to file ([#2](https://github.com/HuddleEng/octopose/issues/2))
* Works with 32-bit and 64-bit Python ([#12](https://github.com/HuddleEng/octopose/issues/12))
* Logs now human readable ([#14](https://github.com/HuddleEng/octopose/issues/14))
* Added Octopose Logo ([#9](https://github.com/HuddleEng/octopose/issues/9))

# Pre-Release

### Manifest to Represent State

* From Octopus Deploy to represent the latest state of projects in the system.
* From a given environment to represnt the state of that environment.
* For a single deployable

### Local Deployment

* Deploy state from a manifest file to local machine (via Nuget)

### Remote Deployment

* Deploy state from a manifest file to a deployment known to Octopus Deploy.
* Optionally blocks till all deployments are complete.
* Optionally force packages to be re-deployed even if it is currently in the environment.

