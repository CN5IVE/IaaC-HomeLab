import json
import os
import paramiko

state_files = {
    ("/home/tshepo/IaaC-HomeLab/terraform/terraform.tfstate", "k8s-node"),
    ("/home/tshepo/IaaC-HomeLab/terraform/terraform.tfstate", "k8s-cntlr"),
    ("/home/tshepo/IaaC-HomeLab/terraform/terraform.tfstate", "kube-andreas"),

}

grouped_instances = {}

for state_file, group_name in state_files:
    with open(state_file, 'r') as f:
        state_data = json.load(f)

        for resource in state_data.get('resources', []):
            if resource.get('type', '') == 'proxmox_vm_qemu':
                instances = resource.get('instances', [])

                for instance in instances:
                    attributes = instance.get('attributes', {})
                    ipconfig0 = attributes.get('ipconfig0', '').replace("ip=", "")
                    ipconfig0 = ipconfig0.split("/24,gw=133.14.14.1")[0].strip()
                    name = attributes.get('name', '') + ".localnetwork.lan"

                    if name.startswith(group_name):
                        if group_name not in grouped_instances:
                            grouped_instances[group_name] = []
                        grouped_instances[group_name].append((name, ipconfig0))

# Add all instances to a single group
grouped_instances['all'] = [instance for instances in grouped_instances.values() for instance in instances]

# Remove duplicates
for group_instances in grouped_instances.values():
    group_instances.sort()  # Sort to make duplicates adjacent
    group_instances[:] = [group_instances[i] for i in range(len(group_instances)) if i == 0 or group_instances[i] != group_instances[i - 1]]

inventory_file = "/home/tshepo/IaaC-HomeLab/ansible/inventory.ini" # Change directory based on your structure

with open(inventory_file, 'w') as f:
    for group_name, instances in grouped_instances.items():
        f.write(f"[{group_name}]\n")
        
        for instance in instances:
            f.write(f"{instance[0]} ansible_host={instance[1]}\n")
        
        f.write("\n")
        
print(f"Inventory file '{inventory_file}' created successfully.")

dns_entries_file = "/home/tshepo/IaaC-HomeLab/dns-pihole/dns_entries.txt" # Change directory based on your structure

with open(dns_entries_file, 'w') as f:
    for instance in grouped_instances['all']:
        f.write(f"{instance[1]} {instance[0]}\n")
        
print(f"DNS entries file '{dns_entries_file}' created successfully.")

output_file = "/home/tshepo/IaaC-HomeLab/dns-pihole/proxmox_vm_names.txt" # Change directory based on your structure

with open(output_file, 'w') as f:
    for instance in grouped_instances['all']:
        vm_name = instance[0].replace(".local.lan", "")
        f.write(f"{vm_name}\n")
        
print(f"Output file '{output_file}' created successfully.")

config_to_append = "[k8s_cluster:children]\nk8s-cntlr\nk8s-node\n"

with open("/home/tshepo/IaaC-HomeLab/ansible/inventory.ini" , "a") as file: # Change directory based on your structure
    file.write(config_to_append)

print("Configuration appended to inventory.ini")