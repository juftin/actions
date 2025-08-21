# taskfile

This GitHub Action installs [Task](https://taskfile.dev/) and runs tasks from your Taskfile.
It provides a simple way to execute Task commands in your GitHub workflows.

## Features

- Installs Task automatically
- Executes specified tasks from your Taskfile
- Optional repository checkout
- Optional setup of [uv](https://github.com/astral-sh/uv) Python package manager
- Optional Docker Buildx setup
- Control over PR Annotations for Popular Tools

## Usage

### Basic Example

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: juftin/actions/taskfile@v1
        with:
          task: test
          github: ${{ secrets.GITHUB_TOKEN }}
```

### Complete Example

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: juftin/actions/taskfile@v1
        with:
          # The task to run from your Taskfile (required)
          task: test
          # Arguments to pass to the task - .CLI_ARGS (default: None)
          args: ""
          # Whether to use the setup-tasks action (default: true)
          setup-task: true
          # Version of Task to install (default: 3.x)
          task-version: 3.x
          # GitHub Token for setup-task (default: "")
          github-token: ""
          # Whether to run the `install` task before the main task (default: false)
          install: false
          # Whether to checkout the repository (default: false)
          checkout: false
          # Fetch depth for checkout (default: 1)
          fetch-depth: 1
          # Git ref to checkout (default: github.ref)
          ref: ${{ github.ref }}
          # Whether to use the setup-uv action (default: false)
          setup-uv: false
          # Version of uv to install (default: latest)
          uv-version: latest
          # Setup Docker Buildx (default: false)
          buildx: false
          # Enable PR annotations for ruff (default: false)
          annotations-ruff: false
          # Enable PR annotations for mypy (default: false)
          annotations-mypy: false
          # Enable PR annotations for pytest (default: false)
          annotations-pytest: false
          # Enable Pytest Coverage PR Comments (default: false)
          pytest-coverage: false
          # Pytest Coverage XML Report Path (default: coverage.xml)
          pytest-coverage-xml: coverage.xml
          # Pytest Coverage junit XML Path (default: pytest.xml)
          pytest-coverage-junit: pytest.xml
          # Arguments to pass to the Task CLI (default: "")
          task-args: ""
```

## Inputs

| Name                    | Description                                            | Required | Default             |
|-------------------------|--------------------------------------------------------|----------|---------------------|
| `task`                  | Task to run from your Taskfile                         | Yes      |                     |
| `args`                  | Arguments to pass to the task (.CLI_ARGS)              | No       |                     |
| `setup-task`            | Whether to use the setup-tasks action                  | No       | `true`              |
| `task-version`          | Version of Task to install                             | No       | `3.x`               |
| `github-token`          | GitHub Token for setup-task                            | No       | `""`                |
| `install`               | Whether to run the `install` task before the main task | No       | `false`             |
| `checkout`              | Whether to checkout the repository                     | No       | `false`             |
| `fetch-depth`           | Fetch depth for checkout                               | No       | `1`                 |
| `ref`                   | Git ref to checkout                                    | No       | `${{ github.ref }}` |
| `setup-uv`              | Whether to use the setup-uv action                     | No       | `false`             |
| `uv-version`            | Version of uv to install                               | No       | `latest`            |
| `buildx`                | Whether to setup Docker Buildx                         | No       | `false`             |
| `annotations-ruff`      | Whether to enable PR annotations for ruff              | No       | `false`             |
| `annotations-mypy`      | Whether to enable PR annotations for mypy              | No       | `false`             |
| `annotations-pytest`    | Whether to enable PR annotations for pylint            | No       | `false`             |
| `pytest-coverage`       | Whether to enable Pytest Coverage PR Comments          | No       | `false`             |
| `pytest-coverage-xml`   | Pytest Coverage XML Report Path                        | No       | `coverage.xml`      |
| `pytest-coverage-junit` | Pytest Coverage junit XML Path                         | No       | `pytest.xml`        |
| `task-args`             | Arguments to pass to the Task CLI                      | No       |                     |

## Workflow Steps

1. (Optional) Checkout the repository if `checkout` is set to `true`
2. (Optional) Setup uv Python package manager if `setup-uv` is set to `true`
3. (Optional) Setup Task if `setup-task` is set to `true`
5. (Optional) Setup Docker Buildx if `buildx` is set to `true`
7. (Optional) Run the `install` task if `install` is set to `true`
8. Run the specified task from your Taskfile
9. (Optional) Post PR Comments for Pytest Coverage Results

## Configuration

### pytest-coverage

If you enable `pytest-coverage`, the action will run use the generated XML Reports from pytest
and post them as a PR comment. The following `pyproject.toml` configuration is reccomended in
combination with this action:

```toml
[tool.pytest.ini_options]
addopts = [
    "-v",
    "--cov=src_code",
    "--cov-report=term-missing",
    "--cov-report=xml:coverage.xml",
    "--junitxml=pytest.xml"
]
```

The following permissions are required for the action to post PR comments:

```yaml
permissions:
  contents: read
  id-token: write
  pull-requests: write
```
