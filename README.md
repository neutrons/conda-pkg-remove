# conda-pkg-remove

GitHub action to remove old packages of a specific label from [anaconda.org](https://anaconda.org),
keeping the N most recent versions.

## Usage

```yaml
jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Remove old dev packages
        uses: neutrons/conda-pkg-remove@main
        with:
          anaconda_token: ${{ secrets.ANACONDA_TOKEN }}
          organization: neutrons
          package_name: my-package
          label: dev
          keep: 5
```

## Inputs

| Input            | Description                            | Required | Default |
|------------------|----------------------------------------|----------|---------|
| `anaconda_token` | Anaconda.org API token                 | Yes      | - |
| `organization`   | Anaconda.org organization or user name | Yes      | - |
| `package_name`   | Name of the conda package to clean up  | Yes      | - |
| `label`          | Label to target for cleanup (e.g., `dev`, `nightly`, `rc`) | Yes | - |
| `keep`           | Number of most recent package versions to keep | No | `5` |
| `dry_run`        | If `true`, only print what would be deleted without actually deleting | No | `false` |

## Outputs

| Output        |                                       |
|---------------|---------------------------------------|
| `num_removed` | Number of files that would be deleted |

Available inputs and outputs are also listed in [`action.yml`](action.yml).
