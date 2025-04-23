# Important Note
This is intended as demo/poc only; some bad practises are followed here

# Usage 
0. Place tls.key and tls.cert in folder gw-api/tls. If you do not have such files, run the following command 



# CRDP
This project is meant to deploy a CRDP workload in a K8s cluster. Along the way:
- the CRDP deployment will be exposed via a Gateway API. This Gateway API will be exposed to the outside world as a NodePort.
- Calls to CRDP will be performed through this Gateway API
- We are using the Nginx Gateway Fabric here as the Gateway API; feel free to change it.
- In the authorised mode, calls to CRDP will authorised through Keycloak IDP; feel free to use any other OIDC supporting IDP (not implemented yet)


# General Prereqs
- CipherTrust manager with CRDP licensed,
- a K8s cluster,
- a way to resolve to NodePorts for external clients.


# Cluster Prereqs

## Secrets
- a TLS key and TLS cert for the Gateway API
- a way to resolve to your exposed Gateway API

# Next Steps
- Add the possibility to deploy a keycloak IDP to handle CRDP authorisation (See https://thalesdocs.com/ctp/cm/2.19/admin/adp_ag/adp-cm-crdp/defn-app-crdp/
index.html)
- Use Secrets Manager for dealing with secrets (e.g. tls secret, reg token)
- Add TLS between Gateway and/or passthrough mode (note CRDP TLS secret from secrets manager)


