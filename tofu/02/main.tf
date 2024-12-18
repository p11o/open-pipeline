locals {
  name = "open-pipeline"
}

data "external" "check_kind_cluster" {
  program = ["${abspath(path.module)}/kind/status.sh"]
}

resource "null_resource" "kind_cluster" {
  # Use a trigger to force re-evaluation if the status changes
  triggers = {
    cluster_status = data.external.check_kind_cluster.result.status
  }

  provisioner "local-exec" {
    when = create
    command = <<-EOT
      if [[ "${data.external.check_kind_cluster.result.status}" == "false" ]]; then
        echo "Creating cluster..."
        kind create cluster --name ${local.name} --config ${abspath(path.module)}/kind/cluster.yaml
      else
        echo "Cluster already exists."
      fi
    EOT
  }
  provisioner "local-exec" {
    when    = destroy
    command = "kind delete cluster --name ${local.name}"
  }
}
