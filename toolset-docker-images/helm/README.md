# Helm Toolset

A Docker image with **Helm**, **Helmfile**, and **Helm Diff** pre-installed for Kubernetes package management and deployment.

## Included Tools

- **Helm** - Kubernetes package manager and templating engine
- **Helmfile** - Declarative Helm charts management
- **Helm Diff** - Preview Helm upgrades before applying

## Quick Start

Build the toolset:

```bash
docker compose build alpine
```

Test it:

```bash
docker compose run alpine helm version
docker compose run alpine helmfile --version
docker compose run alpine asdf current
```

## Customization

Edit `.env` to change versions or registry:

```bash
HELM_PACKAGES="helm:3.14.0:set helmfile:latest:set helm-diff:latest:set"
ASDF_REGISTRY_TOOLSET="ghcr.io/your-org/toolsets"
```

Then rebuild:

```bash
docker compose build alpine
```

## More Info

See [Toolsets Overview](../README.md) for detailed build and customization instructions.
