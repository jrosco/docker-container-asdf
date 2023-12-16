# `asdf-vm` images for Docker

This repository contains base Docker images tailored for the versatile version manager tool, `asdf-vm`. These base images are designed with a flexible `ONBUILD` feature, enabling the creation of specialized images pre-equipped with predefined asdf plugins.

## Overview

### Base Image Structure

The base image Dockerfile provided here serves as a fundamental building block. It includes essential configurations to set up `asdf-vm` along with necessary tools like Git, curl, and bash within an Alpine Linux environment. An `ONBUILD` directive is employed to facilitate the automatic installation of specified asdf plugins and versions when building new images based on this template.

### Utilising ToolSet Images

Examples of other Dockerfiles demonstrate how these base images can be utilized to construct specialized images for different tools or software stacks. By leveraging the base image and utilizing a docker-compose file, users can easily set up and install asdf plugins as per their requirements.

To make this your own repository, you can [fork](https://github.com/jrosco/docker-container-asdf/fork) this repo and update the following [environment](config/environment) variables to your liking.

```bash
# labels
NAME="asdf-vm"
MAINTAINER="jrosco"
DESCRIPTION="asdf version manager toolset"
URL="https://github.com/jrosco/docker-container-asdf"
REPOSITORY=$URL

# docker registries
ASDF_REGISTRY_BASE="ghcr.io/jrosco/$NAME"
ASDF_REGISTRY_TOOLSET="$ASDF_REGISTRY_BASE"
```

An example is showcased using Helm packages within an Alpine Linux environment and other examples found in the [toolset-docker-images] directory.

docker-compose.yml:

```yaml
services:
  alpine:
    image: ghcr.io/jrosco/asdf-vm-toolset/helm:alpine
    build:
      context: .
      dockerfile: Dockerfile
      args:
        image: "ghcr.io/jrosco/asdf-vm:alpine"
        packages: "helm helmfile helm-diff"
        asdf_version: "v0.13.1"
      platforms:
        - "linux/amd64"
```

Example `Dockerfile` and build:

```dockerfile
FROM ghcr.io/jrosco/asdf-vm:alpine
```

#### Build the image

```bash
docker build --build-arg packages="helmfile:latest:set helm:latest:set" -t helm:alpine .
```

#### Get the helm version

```bash
docker run -it helm:alpine helm version
```

### Docker Build Arguments `--build-arg`

Each Dockerfile utilizes the following build arguments:

- `image`: The base image to use for the build. This should be one of the base images provided in the [base-images] directory.
- `packages`: A list of asdf plugins to install. These should be space-separated and match the names of the plugins in the [asdf-community GitHub repository](https://github.com/asdf-community)
- `asdf_version`: The version of asdf to install. This should be a valid tag from the [asdf GitHub repository](https://github.com/asdf-vm/asdf).

`packages` support the following formats

| Format            | Description                                                                                                                   |
| ---               | ---                                                                                                                           |
| `helm`            | Install the plugins repo details only (no versions downloaded)                                                                |
| `helm:3.10.3`     | Install plugin (if not present) and download helm version `3.10.3`                                                            |
| `helm:3.10.3:set` | Install plugin (if not present) and download helm version `3.10.3` and set this as the default version in `.tool-versions`    |
| `helm:latest`     | Install plugin (if not present) and download latest version of `helm`                                                         |

The `image` , `packages` and `asdf_version` arguments are optional. If not provided, the build will default to installing the latest version of asdf and no plugins.

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

This project is licensed under the MIT License.

Feel free to adjust this README according to your specific repository details, adding more sections or details as necessary. This description aims to provide a clear overview, instructions for usage, and guidance for contributions in a concise and user-friendly manner.

[base-images]: /base-images/
[toolset-docker-images]: /toolset-docker-images/