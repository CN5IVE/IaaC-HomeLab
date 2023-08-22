resource "proxmox_vm_qemu" "servers" {
  for_each = var.vm_list

  clone  = "ubuntu-server-jammy"
  vmid   = each.value.vmid
  name   = each.key
  cores  = each.value.cores
  memory = each.value.memory

  target_node = "hydra"
  agent       = 1
  cpu         = "host"
  qemu_os     = "l26"

  scsihw    = "virtio-scsi-single"
  os_type   = "cloud-init"
  ipconfig0 = each.value.ipconfig0

  disk {
    cache   = "none"
    file    = "vm-${each.value.vmid}-disk-0"
    format  = "raw"
    size    = each.value.disk
    storage = "VMs"
    type    = "virtio"
    volume  = "VMs:vm-${each.value.vmid}-disk-0"
  }

  lifecycle {
    ignore_changes = [
      network,
    ]
  }
}
