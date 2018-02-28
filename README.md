# Octopose

**Octopose** is a manifest / state driven deployment framework for [Octopus Deploy](https://octopus.com/). Octopose allows you to create a manifest file based on your releases or deployments that are in Octopus Deploy.

## Why Octopose?

## Installation

For Python3.3+
```
git clone git@github.com:Huddle/octopose.git
cd octopose
python3 -m venv env
.\env\Scripts\activate.ps1
```

## Configuration

Running Octopose requires various configuration variables which can be found in `config.master.py`:

```
octopus_uri = ""
octopus_headers = {"x-octopus-apikey": ""}
projects = []
staging = "~\StagingLocation"
package_sources = []
```

Create a copy of this file called `config.py` with your desired variables.

## Usage

### Creating a Manifest File

Create a manifest file from the `projects` in `config.py`:

```
python .\generate_manifest.py
```

This will output to stdout a manifest based on those projects and the packages within them:

```
{
    'Projects':
    {
        'Huddle.ABC':
            {
                'Packages': ['Huddle.ABC']
            },
        'Huddle.XYZ':
            {
                'Packages': ['Huddle.XYZ1', 'Huddle.XYZ2']
            }
    },
    'StagingLocation': 'D:\\dev\\huddle\\StagingLocation'
}
```

### Generate a manifest based on packages in a given environment

```
python .\generate_manifest.py -e uklive
```

This will add the specific versions of the releases that are currently deployed into that environment:

```
{
    'Projects':
    {
        'Huddle.ABC':
            {
                'Packages': ['Huddle.ABC'],
                'Version': '1.0.0'
            },
        'Huddle.XYZ':
            {
                'Packages': ['Huddle.XYZ1', 'Huddle.XYZ2'],
                'Version': '2.3.0'
            }
    },
    'StagingLocation': 'D:\\dev\\huddle\\StagingLocation'
}
```

### Generate a manifest to only deploy certain packages

```
python .\generate_manifest.py -p Huddle.ABC Huddle.XYZ
```

This will only add the specified projects to the manifest:

```
{
    'Projects':
    {
        'Huddle.ABC':
            {
                'Packages': ['Huddle.ABC'],
                'Version': '1.0.0'
            },
        'Huddle.XYZ':
            {
                'Packages': ['Huddle.XYZ1', 'Huddle.XYZ2']
            }
    },
    'StagingLocation': 'D:\\dev\\huddle\\StagingLocation'
}
```

### Save manifest to a file

```
python .\generate_manifest.py > manifest.json
```

### Deploy to local environment

Deploying to a local environment helps set up developers with the latest code or reproduce a given environment for debugging on your developer workstation.

It reads in the manifest file supplied that describes the state of the local environment.

```
python .\octopose.py .\manifest.json
```

Or
```
cat .\manifest.json | python .\octopose.py
```


This will pull down releases (or given versions) from the NuGet package sources specified in `config.py`. The run through the `PreDeploy.ps1`, `Deploy.ps1`, and `PostDeploy.ps1` executing them for the given release.

The commands can also be piped together:

```
python .\generate_manifest.py | python .\octopose.py
```

### Deploy to a known Octopus Deploy environment

Octopose can also be used to deployed to remote environments such as staging and production using the releases and versions specified in the `manifest.json` file.

The following command will deploy the state described in the supplied `manifest.json` to the environment `uklive`.

```
python .\octopose.py -e uklive .\manifest.json
```

`--force` flag will ensure the package is re-downloaded even if it is already deployed into the target environment.

`--wait` flag will cause **octopose** to continually poll the Octopus Deploy Tasks till they are complete.

`--verbose` (or `-v`) flag will cause **octopose** to output all logs from the `*Deploy.ps1` files. Otherwise there will only be logs from a script if a non-zero exit code is returned.

```
python .\octopose.py -e staging --wait --force --verbose
```


