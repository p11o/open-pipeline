# OpenPipeline

Create a pipeline with AI


## Getting started

**Prerequisites**

* nvidia GPU
* nvkind https://github.com/NVIDIA/nvkind
* opentofu
* kubectl
* helm

**Running**

```bash
# Create nvkind cluster
cd tofu/01
tofu init
tofu apply

# Deploy services
cd tofu/02
tofu init
tofu apply
```
