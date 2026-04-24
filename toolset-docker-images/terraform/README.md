# Terraform Toolset

A Docker image with **Terraform**, **TFLint**, and **Terraform Validator** pre-installed for infrastructure-as-code provisioning and validation.

## Included Tools

- **Terraform** - Infrastructure-as-code provisioning engine
- **TFLint** - Linter and best-practice validator for Terraform
- **Terraform Validator** - Policy validation for Terraform configurations

## Quick Start

Build the toolset:

```bash
docker compose build alpine
```

Test it:

```bash
docker compose run alpine terraform version
docker compose run alpine tflint --version
docker compose run alpine asdf current
```

## Customization

Edit `.env` to change versions or registry:

```bash
TERRAFORM_PACKAGES="terraform:1.8.0:set tflint:0.50.0:set terraform-validator:latest:set"
ASDF_REGISTRY_TOOLSET="ghcr.io/your-org/toolsets"
```

Then rebuild:

```bash
docker compose build alpine
```

## More Info

See [Toolsets Overview](../README.md) for detailed build and customization instructions.
