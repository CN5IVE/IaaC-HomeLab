#!/bin/bash

# Step 1: Switch to root user
sudo su -

# Step 2: Create directory /etc/containerd if not exists
mkdir -p /etc/containerd

# Step 3: Redirect containerd config to /etc/containerd/config.toml
containerd config default > /etc/containerd/config.toml

# Step 4: Modify SystemdCgroup option in config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

# Step 5: Exit from su
exit
