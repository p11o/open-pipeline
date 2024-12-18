provider "helm" {
  kubernetes {
    config_path    = "~/.kube/config"
    config_context = "kind-open-pipeline"
  }
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "kind-open-pipeline"
}
