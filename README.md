# Octopose

**Octopose** is a manifest / state driven deployment framework for [Octopus Deploy](https://octopus.com/). Octopose allows you to create a manifest file based on your releases or deployments that are in Octopus Deploy.

## Why Octopose?

## Instillation

```
git clone git@github.com:Huddle/octopose.git
cd octopose
mkdir env
virtualenv env
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

This will generate a new `manifest.py` based on those projects and the pacakges wihtin them:

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
    
You can also generate a based on packages in a given environment:

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

### Deploy to local envirionment

Deploying to a local environment helps set up developers with the latest code or reproduce a given environment for debugging on your developer workstation.

It reads in the `manifest.json` file that describes the state of the local environment.

```
python .\octopose.py
```

This will pull down releases (or given versions) from the NuGet package sources specified in `config.py`. The run through the `PreDeploy.ps1`, `Deploy.ps1`, and `PostDeploy.ps1` executing them for the given release.

### Deploy to a known Octopus Deploy environment

Octopose can also be used to deployed to remote environments such as staging and production using the releases and versions specified in the `manifest.json` file.

The following command will deploy the state described in the `manifest.json` to the environment `uklive`.

```
python .\octopose.py -e uklive
```

Adding a `--force` flag will ensure the package is redownloaded even if it is already deployed into the target environment.

Adding the `--wait` flag will cause **octopose** to continually poll the Octopus Deploy Tasks till they are complete.

```
python .\octopose.py -e staging --wait --force
```


