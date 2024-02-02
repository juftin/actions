# juftin/actions

This repository contains a collection of GitHub Actions that are
used in various projects. These actions are designed to be used in
conjunction with other actions and are not standalone.

-   [docker-build-push](#docker-build-push) - Build and optionally push a Docker image
-   [github-pages](#github-pages) - Deploy a static site to GitHub Pages
-   [hatch-docs](#hatch-docs) - Build Documentation with hatch
-   [hatch-lint](#hatch-lint) - Lint Python Code with hatch
-   [hatch-setup](#hatch-setup) - Setup Python Environment with hatch
-   [hatch-test](#hatch-test) - Test Python Code with hatch
-   [hatch-version](#hatch-version) - Get the Version of a Python Package with hatch
-   [semantic-release](#semantic-release) - Automate Semantic Versioning and Releases

## docker-build-push

The `docker-build-push` action is a composite action that uses the `docker/build-push-action` to build
and push a docker image to a registry.

### Inputs

-   `push` - Push the image to the registry. Default: `false`
-   `name` - The name of the package to build. Required
-   `version` - The version of the package to build. Required
-   `registry` - The registry to push the image to. Default: `juftin`
-   `latest` - Tag the image as latest. Default: `true`
-   `username` - The username for the registry. Default: `""`
-   `password` - The password for the registry. Default: `""`
-   `context` - The context to use for the build. Default: `.`
-   `load` - Load the image into docker after building. Default: `false`

### Usage

```yaml
- name: Docker Build and Push
  uses: juftin/actions/docker-build-push@v1
  with:
      push: true
      name: "my-package"
      version: "1.0.0"
      registry: "juftin"
      latest: true
      username: ${{ secrets.DOCKER_USERNAME }}
      password: ${{ secrets.DOCKER_PASSWORD }}
```

## github-pages

The `github-pages` action is a composite action that uses
the `actions/configure-pages`, `actions/upload-pages-artifact`,
and `actions/deploy-pages` actions to deploy a static site to GitHub Pages.

### Inputs

-   `path` - The directory to publish. Default: `site`

### Outputs

-   `page_url` - The URL of the deployed site

### Usage

```yaml
permissions:
    pages: write
    id-token: write
environment:
    name: github-pages
    url: ${{ steps.deployment.outputs.page_url }}
steps:
    - name: Set up Github Workspace
      uses: actions/checkout@v4
    - name: Setup Hatch
      uses: juftin/actions/hatch-setup@v1
      with:
          python_version: "3.11"
    - name: Build Docs
      uses: juftin/actions/hatch-docs@v1
    - name: Publish Docs
      uses: juftin/actions/github-pages@v1
      id: deployment
```

## hatch-docs

The `hatch-docs` action is a composite action that uses [hatch] to build documentation.

### Inputs

-   `path` - The directory to publish. Default: `site`
-   `env` - hatch docs environment. Default: `docs`
-   `build_command` - Docs build command to run. Default: `build`
-   `shell` - Shell to use. Default: `bash`

### Usage

```yaml
- name: Setup Hatch
  uses: juftin/actions/hatch-setup@v1
  with:
      python_version: "3.11"
- name: Build Documentation
  uses: juftin/actions/hatch-docs@v1
```

## hatch-lint

The `hatch-lint` action is a composite action that uses [hatch] to lint Python code.

### Inputs

-   `env` - hatch linting environment. Default: `lint`
-   `style_command` - Style Command to run. Default: `style`
-   `typing_command` - Typing Command to run. Default: `typing`
-   `shell` - Shell to use. Default: `bash`

### Usage

```yaml
- name: Setup Hatch
  uses: juftin/actions/hatch-setup@v1
  with:
      python_version: "3.11"
- name: Lint Python Code
  uses: juftin/actions/hatch-lint@v1
```

## hatch-setup

The `hatch-setup` action is a composite action that uses [hatch] to setup a Python environment.

### Inputs

-   `python_version` - Python Version to install. Required
-   `create_env` - Create a new virtual environment. Default: `""`
-   `additional_dependencies` - Additional dependencies to install. Default: `""`
-   `shell` - Shell to use for running commands. Default: `bash`

### Usage

```yaml
- name: Setup Python Environment
  uses: juftin/actions/hatch-setup@v1
  with:
      python_version: "3.11"
      additional_dependencies: "pre-commit black"
```

## hatch-test

The `hatch-test` action is a composite action that uses [hatch] to run tests.
This action can be used in a matrix to test multiple versions of Python - or
it can be used in a standalone environment as well.

### Inputs

-   `env` - hatch testing environment. Default: `test`
-   `coverage_command` - Coverage Command to run. Default: `cov`
-   `shell` - Shell to use. Default: `bash`
-   `matrix` - Test matrix. Default: `""`

### Usage

```yaml
jobs:
    test:
        name: test
        runs-on: ubuntu-latest
        strategy:
            matrix:
                include:
                    - { name: Python 3.10, python: "3.10" }
                    - { name: Python 3.9, python: "3.9" }
                    - { name: Python 3.8, python: "3.8" }
        steps:
            - name: Check out the repository
              uses: actions/checkout@v4
              with:
                  fetch-depth: 0
            - name: Setup Hatch
              uses: juftin/actions/hatch-setup@v1
              with:
                  python_version: ${{ matrix.python }}
            - name: Test
              uses: juftin/actions/hatch-test@v1
              with:
                  env: matrix
                  coverage_command: cov
                  matrix: "+py=${{ matrix.python }}"
```

## hatch-version

The `hatch-version` action is a composite action that uses [hatch] to
get the version of a Python package and its name.

### Usage

```yaml
- name: Setup Hatch
  uses: juftin/actions/hatch-setup@v1
  with:
      python_version: "3.11"
- name: Get Package Name and Version
  uses: juftin/actions/hatch-version@v1
  id: package
- name: Echo Package Info
  run: |
      echo "Package Name: ${{ steps.package.outputs.name }}"
      echo "Package Version: ${{ steps.package.outputs.version }}"
```

## semantic-release

The `semantic-release` action is a composite action
that uses [semantic-release] to automate the versioning and
releasing of a package.

`semantic-release` comes pre-configured with the following plugins:

-   `@semantic-release/exec` - Run commands during the release process
-   `@semantic-release/git` - Commit release assets to the repository
-   `@semantic-release/github` - Create a GitHub release
-   `semantic-release-gitmoji` - Use gitmoji for commit messages

You must also have a semantic-release configuration file in your repository
root for this action to work.

### Inputs

-   `github_token` - GitHub Token. Required

### Usage

```yaml
- name: Semantic Release
  uses: juftin/actions/semantic-release@v1
  with:
      github_token: ${{ secrets.GITHUB_TOKEN }}
```

[semantic-release]: https://github.com/semantic-release/semantic-release
[hatch]: https://github.com/pypa/hatch
