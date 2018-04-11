# Next Release

* Move configuration files to well known location ([#24](https://github.com/HuddleEng/octopose/issues/24))

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
* Optionally force packages to be re-eeployed even if it is currently in the environment.

