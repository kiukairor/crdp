# Important Note
All security bad practises will be followed in the first iterations :)

# CRDP
This project is meant to deploy a CRDP workload in a K8s cluster. Along the way:
- the CRDP deployment will be exposed via a Gateway API. This Gateway API will be exposed to the outside world as a NodePort.
- Calls to CRDP will be performed through this Gateway API
- We are using the Nginx Gateway Fabric here as the Gateway API; feel free to change it.
- In the authorised mode, calls to CRDP will authorised through Keycloak IDP; feel free to use any other OIDC supporting IDP.

# General Prereqs
- CipherTrust manager with CRDP licensed,
- a K8s cluster,
- a way to resolve to NodePorts for external clients.
- An IDP, or rather a JWKS for verifying and authorising calls to CRDP.
 - More precisely, the IDP will allow an application to authenticate and get a JWT
 - this JWT will be sent to CRDP that will authorise the calls depending on the CRDP policy (See https://thalesdocs.com/ctp/cm/2.19/admin/adp_ag/adp-cm-crdp/defn-app-crdp/index.html)

# Cluster Prereqs

## ConfigMaps
- configMap to specify hostname of CipherTrust Manager
- configMap 
## Secrets
- a TLS Secret for Gateway API TLS
- a way to resolve to your exposed Gateway API

## values to sort
- CRDP: CM hostname, tls mode, reg token
- GW: tls secret, 
- Routes: hostname for crdp 


# More Notes
- For now, we enable TLS offload at the gateway and we forward calls with http only; other modes will be added later; note that CRDP service can of course leverage TLS communication

