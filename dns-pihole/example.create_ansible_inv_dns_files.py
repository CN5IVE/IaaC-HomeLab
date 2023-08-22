import json

state_files_and_groups = [
    ("path-to-files/terraform/k8s-node/terraform.tfstate", "k8s-node"),
    ("path-to-files/terraform/k8s-cntlr/terraform.tfstate", "k8s-cntlr"),
    ("path-to-files/terraform/ceph/terraform.tfstate", "ceph"),
    ("path-to-files/terraform/ceph/terraform.tfstate", "mons"),
    ("path-to-files/terraform/ceph/terraform.tfstate", "mgrs"),
    ("path-to-files/terraform/ceph/terraform.tfstate", "mdss"),
    ("path-to-files/terraform/ceph/terraform.tfstate", "osds"),
    ("path-to-files/terraform/others/terraform.tfstate", "grafana-server"),
    ("path-to-files/terraform/others/terraform.tfstate", "loadbalancer"),
    ("path-to-files/terraform/others/terraform.tfstate", "cephadmin"),
    ("path-to-files/terraform/others/terraform.tfstate", "gwss"),
]

grouped_instances = {group_name: [] for _, group_name in state_files_and_groups}

for state_file, group_name in state_files_and_groups:
    with open(state_file, 'r') as f:
        state_data = json.load(f)

        for resource in state_data.get('resources', []):
            if resource.get('type', '') == 'proxmox_vm_qemu':
                instances = resource.get('instances', [])
                
                for instance in instances:
                    attributes = instance.get('attributes', {})
                    ipconfig0 = attributes.get('ipconfig0', '').replace("ip=", "")
                    ipconfig0 = ipconfig0.split("/24,gw=133.14.14.1")[0].strip()
                    name = attributes.get('name', '') + ".ribaseleke.lan"

                    grouped_instances[group_name].append((name, ipconfig0))

# Add all instances to a single group and remove duplicates
all_instances = [instance for instances in grouped_instances.values() for instance in instances]
grouped_instances['all'] = list(set(all_instances))

# Write the results to the file
inventory_file_path = "path-to-files/ansible/inventory.ini"
with open(inventory_file_path, 'w') as inventory_file:
    for group_name, instances in grouped_instances.items():
        inventory_file.write(f"[{group_name}]\n")
        for instance in instances:
            name, ip = instance
            inventory_file.write(f"{name} ansible_host={ip}\n")
        inventory_file.write("\n")

print(f"Inventory written to {inventory_file_path}")
print(f"Inventory file '{inventory_file_path}' created successfully.")

dns_entries_file = "path-to-files/dns-pihole/dns_entries.txt" # Change directory based on your structure

with open(dns_entries_file, 'w') as f:
    for instance in grouped_instances['all']:
        f.write(f"{instance[1]} {instance[0]}\n")
        
print(f"DNS entries file '{dns_entries_file}' created successfully.")

config_to_append = "[k8s_cluster:children]\nk8s-cntlr\nk8s-node\n"

with open(inventory_file_path, "a") as file:
    file.write(config_to_append)

print("Configuration appended to inventory.ini")


