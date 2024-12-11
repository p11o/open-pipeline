locals {
  name = "open-pipeline"
}

data "external" "check_kind_cluster" {
  program = ["${abspath(path.module)}/nvkind/status.sh"]
}

resource "null_resource" "kind_cluster" {
  provisioner "local-exec" {
    command = data.external.check_kind_cluster.result.status ? "echo 'Cluster already exists'" : "nvkind cluster create --name ${local.name} --config-template ${abspath(path.module)}/nvkind/cluster.yaml"
  }
  provisioner "local-exec" {
    when    = destroy
    command = "kind delete cluster --name open-pipeline"
  }
}
