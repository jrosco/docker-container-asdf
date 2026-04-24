# AWS CLI Toolset

A Docker image with **AWS CLI** and related AWS utilities pre-installed for infrastructure and secrets management.

## Included Tools

- **AWS CLI** - Official AWS command-line interface
- **AWS Vault** - Securely store and access AWS credentials

## Quick Start

Build the toolset:

```bash
docker compose build alpine
```

Test it:

```bash
docker compose run alpine aws --version
docker compose run alpine aws-vault --version
docker compose run alpine asdf current
```

## Customization

Edit `.env` to change versions or registry:

```bash
AWSCLI_PACKAGES="awscli:2.13.0:set aws-vault:latest:set"
ASDF_REGISTRY_TOOLSET="ghcr.io/your-org/toolsets"
```

Then rebuild:

```bash
docker compose build alpine
```

## More Info

See [Toolsets Overview](../README.md) for detailed build and customization instructions.
