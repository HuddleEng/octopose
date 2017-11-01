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


### Deploy to a known Octopus Deploy environment