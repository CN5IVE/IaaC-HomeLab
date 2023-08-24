#!/bin/bash

# Patching services in the 'monitoring' namespace
kubectl --namespace monitoring patch svc prometheus-k8s -p '{"spec": {"type": "LoadBalancer"}}'
kubectl --namespace monitoring patch svc alertmanager-main -p '{"spec": {"type": "LoadBalancer"}}'
kubectl --namespace monitoring patch svc grafana -p '{"spec": {"type": "LoadBalancer"}}'

# Patching service in the 'kubernetes-dashboard' namespace
kubectl --namespace kubernetes-dashboard patch svc kubernetes-dashboard -p '{"spec": {"type": "LoadBalancer"}}'
