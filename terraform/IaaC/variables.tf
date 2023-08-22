variable "proxmox_api_url" {
  type = string
}
variable "proxmox_api_token_id" {
  type = string
}
variable "proxmox_api_token_secret" {
  type      = string
  sensitive = true
}


variable "user" {
	default     = "ubuntu" #change to your username
	description = "User used to SSH into the machine and provision it"
}


variable "vm_list" {
    type = map(object({

        vmid = string
        ipconfig0 = string
        memory = string
        cores = string
        disk = string 
    }))
    default = {
      "kube-andreas-01" = {
        vmid = "102"
        ipconfig0 = "ip=133.14.14.5/24,gw=133.14.14.1" # ip for vm 
        memory = "8192"
        cores = "2"
        disk = "20G"
      }
      "ceph-01" = {
        vmid = "103"
        ipconfig0 = "ip=133.14.14.6/24,gw=133.14.14.1" # ip for vm 
        memory = "8192"
        cores = "2"
        disk = "20G"
	  	}
		"ceph-02" = {
        vmid = "104"
        ipconfig0 = "ip=133.14.14.7/24,gw=133.14.14.1" # ip for vm 
        memory = "8192"
        cores = "2"
        disk = "20G"
      }
	   "ceph-03" = {
        vmid = "105"
        ipconfig0 = "ip=133.14.14.8/24,gw=133.14.14.1" # ip for vm 
        memory = "8192"
        cores = "2"
        disk = "20G"
      }
	    "k8s-cntlr-01" = {
        vmid = "201"
        ipconfig0 = "ip=133.14.14.10/24,gw=133.14.14.1" # ip for vm 
        memory = "4096"
        cores = "2"
        disk = "20G"

      }
      "k8s-cntlr-02" = {
        vmid = "202"
        ipconfig0 = "ip=133.14.14.11/24,gw=133.14.14.1" # ip for vm 
        memory = "4096"
        cores = "2"
        disk = "20G"

      }
      "k8s-cntlr-03" = {
        vmid = "203"
        ipconfig0 = "ip=133.14.14.12/24,gw=133.14.14.1" # ip for vm 
        memory = "4096"
        cores = "2"
        disk = "20G"

      }
      "k8s-node-01" = {
        vmid = "301"
        ipconfig0 = "ip=133.14.14.13/24,gw=133.14.14.1" # ip for vm 
        memory = "4096"
        cores = "2"
        disk = "20G"

      }
      "k8s-node-02" = {
        vmid = "302"
        ipconfig0 = "ip=133.14.14.14/24,gw=133.14.14.1" # ip for vm 
        memory = "4096"
        cores = "2"
        disk = "20G"

      }
      "k8s-node-03" = {
        vmid = "303"
        ipconfig0 = "ip=133.14.14.15/24,gw=133.14.14.1" # ip for vm 
        memory = "4096"
        cores = "2"
        disk = "20G"

      }      
    }
}


