variable "baseImage" {
}

variable "targetImage" {
}

variable "targetTag" {
}

source "docker" "image" {
  image = var.baseImage
  pull = true
  commit = true
  changes = [
    "ENTRYPOINT [\"/entrypoint.sh\"]",
    "CMD []"
  ]
}

build {
  sources = [
    "source.docker.image"
  ]

  provisioner "file" {
    source = "entrypoint.sh"
    destination = "/entrypoint.sh"
  }

  provisioner "shell" {
    script = "provision.sh"
  }

  post-processor "docker-tag" {
    repository = var.targetImage
    tag = [var.targetTag]
  }

  post-processor "shell-local" {
    command = "tox"
  }
}
