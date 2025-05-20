![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/jrosco/docker-container-asdf/docker-push.yaml?label=PUSHED&style=for-the-badge) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/jrosco/docker-container-asdf/docker-build.yaml?label=TEST&style=for-the-badge) ![GitHub Tag](https://img.shields.io/github/v/tag/jrosco/docker-container-asdf?style=for-the-badge) ![GitHub last commit](https://img.shields.io/github/last-commit/jrosco/docker-container-asdf?display_timestamp=author&style=for-the-badge) ![GitHub forks](https://img.shields.io/github/forks/jrosco/docker-container-asdf?style=for-the-badge) ![GitHub Issues or Pull Requests by label](https://img.shields.io/github/issues-pr/jrosco/docker-container-asdf/dependencies?style=for-the-badge&label=Dependency%20Pull%20Requests) ![GitHub License](https://img.shields.io/github/license/jrosco/docker-container-asdf?style=for-the-badge)

### Current versions
![Go](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/jrosco/docker-container-asdf/refs/heads/main/docs/badges/golang.json)
![Alpine](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/jrosco/docker-container-asdf/refs/heads/main/docs/badges/alpine.json)
![Debian](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/jrosco/docker-container-asdf/refs/heads/main/docs/badges/debian.json)
![ASDF](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/jrosco/docker-container-asdf/refs/heads/main/docs/badges/asdf.json)

### Docker Latest Builds
![Docker Image Version (tag)](https://img.shields.io/docker/v/asdfvm/asdf/debian?sort=date&style=for-the-badge&label=Docker&color=red)
![Docker Image Version (tag)](https://img.shields.io/docker/v/asdfvm/asdf/alpine?sort=date&style=for-the-badge&label=Docker)

# `asdf-vm` base images

Works with [asdf] `>=0.16.0`

This repository contains base Docker images tailored for the versatile version manager tool, `asdf-vm`. These base images are designed with a flexible `ONBUILD` feature, enabling the creation of specialized images pre-equipped with predefined [asdf] plugins.

## Overview

### Base Image Structure

The base image Dockerfile provided here serves as a fundamental building block. It includes essential configurations to set up `asdf-vm` along with necessary tools like Git, curl, and bash within an Linux environment. An `ONBUILD` directive is employed to facilitate the automatic installation of specified [asdf] plugins and versions when building new images based on this template.

### Utilising ToolSet Images

Examples of other Dockerfiles demonstrate how these base images can be utilized to construct specialized images for different tools or software stacks. By leveraging the base image and utilizing a docker-compose file, users can easily set up and install asdf plugins as per their requirements.

To make this your own repository, you can [fork](https://github.com/jrosco/docker-container-asdf/fork) this repo and update the following [environment] variables to your liking.

```bash
# labels
NAME="asdf-vm"
MAINTAINER="jrosco"
DESCRIPTION="asdf version manager toolset"
URL="https://github.com/jrosco/docker-container-asdf"
REPOSITORY=$URL

# docker registries
ASDF_REGISTRY_BASE="ghcr.io/jrosco/$NAME"
ASDF_REGISTRY_TOOLSET="$ASDF_REGISTRY_BASE-toolsets"
```

An example is showcased using Helm packages within an Alpine Linux environment and other examples found in the [toolset-docker-images] directory.

docker-compose.yml:

```yaml
services:
  alpine:
        image: ghcr.io/jrosco/asdf-vm-toolsets/helm:alpine
    build:
      context: .
      dockerfile: Dockerfile
      args:
        asdf_image: "ghcr.io/jrosco/asdf-vm:alpine"
        packages: "helm helmfile helm-diff"
      platforms:
        - "linux/amd64"
```

Example `Dockerfile` and build:

```dockerfile
FROM ghcr.io/jrosco/asdf-vm:alpine
```

#### Build the image

```bash
docker build \
    --build-arg \
    packages="awscli:latest:set helmfile:latest:set helm:latest:set kustomize:latest:set" \
    -t helm-toolset:alpine .
```

#### Get the installed package versions and details

```bash
docker run -it helm-toolset:alpine asdf info
docker run -it helm-toolset:alpine asdf current
```

### Docker Build Arguments `--build-arg`

Each Dockerfile utilizes the following build arguments:

- `asdf_image`: The base image to use for the build. This should be one of the base images provided in the [base-images] directory.
- `packages`: A list of [asdf] plugins to install. These should be space-separated and match the names of the plugins in the [asdf-community GitHub repository](https://github.com/asdf-community)

`packages` support the following formats

| Format            | Description                                                                                                                   |
| ---               | ---                                                                                                                           |
| `helm`            | Install the plugins repo details only (no versions downloaded)                                                                |
| `helm:3.10.3`     | Install plugin (if not present) and download helm version `3.10.3`                                                            |
| `helm:3.10.3:set` | Install plugin (if not present) and download helm version `3.10.3` and set this as the default version in `.tool-versions`    |
| `helm:latest`     | Install plugin (if not present) and download latest version of `helm`                                                         |

The `asdf_image`  and `packages` arguments are optional. If not provided, the build will default to installing the latest version of asdf and no plugins.

### Adding Your Own `.tool-versions` File on Build

You can add your own `.tool-versions` file, for example:

```text
package_name1 version_number
package_name2 version_number
```

Naming the file `.tool-versions` will automatically detect the file and `COPY` it to the image on build.

To add a custom file (e.g., using a different name), you need to use the Docker `COPY` command and set ASDF's environment variable correctly:

```dockerfile
WORKDIR /tmp/  # Only required if you want to put the file in a different location from the default `/asdf/`
ENV ASDF_DEFAULT_TOOL_VERSIONS_FILENAME=custom-tool-version
COPY custom-tool-version ./
RUN bash /init/install-asdf-package
```
See the [asdf reference for more details](https://asdf-vm.com/manage/configuration.html#tool-versions).

## Getting Started

To get started, follow these steps:

1. **Clone the Repository:** Clone this repository to your local environment.
2. **Explore Base Images:** Navigate to the [base-images] directory to explore the base images available.
3. **Customize Dockerfiles:** Review and customize the Dockerfiles provided in the [base-images] directory to suit your needs. Modify the `ONBUILD` directives, add or remove packages, and adjust versions as required.
4. **Build Specialized Images:** Utilize the base images as templates to construct specialized images for your toolsets or software stacks. Refer to the provided examples and adjust the docker-compose files and build configurations according to your preferences.
5. **Run and Test:** Once built, run the images in your environment and test to ensure proper functioning.

## Contributing

Contributions to enhance or expand the existing base images or examples are welcome. Feel free to submit pull requests, suggest improvements, or report issues in the repository.

## License

MIT License

See [COPYING](COPYING) to see the full text.

[asdf]: https://asdf-vm.com/
[base-images]: https://github.com/jrosco/docker-container-asdf/tree/main/base-images
[toolset-docker-images]: https://github.com/jrosco/docker-container-asdf/tree/main/toolset-docker-images
[environment]: https://github.com/jrosco/docker-container-asdf/blob/main/config/environment
