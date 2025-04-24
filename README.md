# Thales CRDP (CipherTrust Restful Data Protection)
This project is meant to deploy a CRDP workload in a K8s cluster. Along the way:
- the CRDP deployment will be exposed via a Gateway API. This Gateway API will be exposed to the outside world as a NodePort.
- Calls to CRDP will be performed through this Gateway API
- We are using the Nginx Gateway Fabric here as the Gateway API; feel free to change it.
- In the authorised mode, calls to CRDP will authorised through Keycloak IDP; feel free to use any other OIDC supporting IDP (not implemented yet)

# Why this project? 
One could simply use Thales helm chart to deploy CRDP; this project was meant to: 
- deploy an gateway API standing before (CRDP) workloads: it should be easy to find posts or resources explaining why one may want to use Gateway API insted of Ingress in  K8s
- Thales default Helm Chart defines a NodePort svc for CRDP, this is of course acceptable for demos but we wanted to go one step further
- Use kustomize.

## Promise
As long as you fulfill the general prereqs, you should be able to amend the config files, deploy things and verify CRDP is up and running in less than 10 mins.

# Important Note
This is intended as demo/poc only; some bad practises are followed here.

# Usage 
0. Create a namespace where CRDP objects will be deployed.

1. Place tls.key and tls.cert in folder gw-api/tls. They will represent the TLS endpoint exposed at the Gateway level. 
    a. If you do not have such files, run the following command:
````
openssl req -x509 -newkey rsa:2048 -sha256 -days 365 -nodes -keyout tls.key -out tls.crt -subj "/C=UK/ST=Eng/L=Limoges/O=yourorg/CN=*.env.local"
````
2. Get a Registration Token
    - Log onto your CipherTrust Manager > Application Protection > Add Application > Connector Type set to 'CRDP' and follow wizard (leave default values if unsure)
    - Click on the created application and click 'Copy' to copy the Registration Token
    - Create a file named 'value' in crdp/regtoken folder and simply copy this token in this file 'value'

3. Update crdp-routes/kustomization.yaml: 
    - Replace 'namespace: kust' by 'namespace: \<your-created-namespace\> (See step 0.)
    - Replace 'hostname=crdp-kust.kiukairor.local' by 'hostname=\<your-crdp-hostname\>' (Hostname of your choice, your clients should be able to resolve it)

4. Update crdp/kustomization.yaml:
    - Replace 'namespace: kust' by 'namespace: \<your-created-namespace\> (See step 0.)
    - Replace 'CM_HOST=cm-ninja.kiukairor.com' by CM_HOST=\<you-ciphertrust-hostname-ip\> (If using hostname, ensure your (CRDP) pods will be able to resolve your ciphertrust)
5. Run 'kubectl apply -k .' at the root level.

6. To get your gateway NodePort, run:
````
➜  ~ kubectl -n nginx-gateway get svc
NAME            TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
nginx-gateway   NodePort   10.100.156.252   <none>        80:30116/TCP,443:31244/TCP   13h
````
Here my https port is 31244.
Browse/Curl to https://\<your-crdp-hostname\>:\<https-port\>/liveness and see CRDP is running

````
curl --request GET --url https://<your-crdp-hostname>:<https-port>/liveness
````
7. Check https://thalesdocs.com/ctp/con/crdp/latest/admin/crdp-quick-start/index.html and https://thalesdocs.com/ctp/con/crdp/latest/crdp-apis/index.html 

8. To uninstall things, run 'kubectl apply -k .', at the root level again.
    - Don't worry if you see 'NotFound' errors, it is likely due to the fact that some CRDs are deleted before the objects themselves. It should not a be a concern for this demo project.



# General Prereqs
- CipherTrust manager with CRDP licensed,
- a reasonably recent K8s cluster (this was tested on 1.29, with kustomize 5.0)
- a way to resolve to NodePorts for external clients.


# Cluster Prereqs

## Secrets
- Ideally, a TLS key and TLS cert for the Gateway API or generate them on the fly has describe above.
- A way to resolve to your exposed Gateway API.

# Next Steps
- Add the possibility to deploy a keycloak IDP to handle CRDP authorisation (See https://thalesdocs.com/ctp/cm/2.19/admin/adp_ag/adp-cm-crdp/defn-app-crdp/index.html)
- Use Secrets Manager for dealing with secrets (e.g. tls secret, reg token)
- Add TLS between Gateway and/or passthrough mode.


