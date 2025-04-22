# CRDP
This project is meant to deploy a CRDP workload in a K8s cluster. Along the way:
- the CRDP deployment will be exposed via a Gateway API
- Calls to CRDP will be performed through this Gateway API (we used Nginx Gateway Fabric here)
- Calls to CRDP will authorised through Keycloak IDP

# Prereqs
- CipherTrust manager with CRDP licensed
- a K8S cluster
- Cert and Key to be used as a TLS secret for Gateway API endpoint
- An IDP, or rather a JWKS for verifying and authorising calls to CRDP

