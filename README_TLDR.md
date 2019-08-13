# Octopose steps

`octopose generate` -> manifest.json -> `octopose deploy`

```sh
octopose --help

octopose generate > manifest.json
octopose generate -p Files > manifest.json; cat ./manifest.json

octopose generate -p Files -e staging > manifest.json; cat ./manifest.json
octopose deploy ./manifest.json

# For showoffs
octopose generate -p Files -e staging | octopose deploy
octopose generate -p Files -e staging | octopose deploy --wait --force --verbose
```
