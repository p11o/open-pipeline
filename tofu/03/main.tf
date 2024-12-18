
resource "kubernetes_namespace" "nvidia" {
  metadata {
    name = "nvidia"
  }
}

resource "helm_release" "nvdp" {
  name = "nvdp"

  repository = "https://nvidia.github.io/k8s-device-plugin"
  chart      = "nvidia-device-plugin"

  values = [file("${path.module}/helm/nvdp.yaml")]

  namespace = kubernetes_namespace.nvidia.id
}

resource "helm_release" "ollama" {
  name = "ollama"

  repository = "https://otwld.github.io/ollama-helm/"
  chart      = "ollama"

  values = [file("${path.module}/helm/ollama.yaml")]
}

resource "helm_release" "dagster" {
  name = "dagster"

  repository = "https://dagster-io.github.io/helm"
  chart      = "dagster"

  values = [file("${path.module}/helm/dagster.yaml")]
}

