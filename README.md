# Thales CRDP (CipherTrust Restful Data Protection)
This project is meant to deploy a CRDP workload in a K8s cluster. Along the way:
- the CRDP deployment will be exposed via a Gateway API. This Gateway API will be exposed to the outside world as a NodePort.
- Calls to CRDP will be performed through this Gateway API
- We are using the Nginx Gateway Fabric here as the Gateway API; feel free to change it.
- In the authorised mode, calls to CRDP will authorised through Keycloak IDP; feel free to use any other OIDC supporting IDP (not implemented yet)

# Why this project? 
One could simply use Thales helm chart to deploy CRDP; this project was meant to: 
- deploy an gateway API standing before (CRDP) workloads: lets use Gateway API rather than Ingress in K8s;
- Thales default Helm Chart defines a NodePort svc for CRDP, this is more than enough for demos but we wanted to go one step further;
- Use kustomize to deploy things.

## Promise
As long as you fulfill the general prereqs, you should be able to amend the config files, deploy things and verify CRDP is up and running in around **5 mins**.

# Important Note
This is intended as demo/poc only; some bad practises are followed here.


# Right before starting
Explanation of the variables involved below:
- \<crdp-namespace\>: K8s Namespace that will hold CRDP resources.
- \<domain-name\>: the domain name of your set up. It can be a local domain name.
- \<crdp-hostname\>: it is the hostname you will reach out to. It should be something like 'crdp.\<domain-name\>'. For a local setup, you can simply add an entry in /etc/hosts to make your client resolve 'crdp.\<domain-name\>' to your worker nodes.
- tls.key/tls.crt: they are the TLS credentials that will be used at the gateway level for incoming connections. You can either use existing ones or generate new ones on the fly as described below.
- \<ciphertust-hostname\>: Hostname or IP address to your CipherTrust Manager. Your pods must be able to resolve to it and/or to reach the corresponding IP address.

# Usage 
0. Create the namespace \<crdp-namespace\>.
````
➜  ~  kubectl create ns <crdp-namespace>
````

At the root of this project:

1. Place tls.key and tls.cert in folder ./gw-api/tls/. 
    - If you do not have such files, run the following command:
````
➜  crdp git:(main) ✗ ls
README.md  crdp  crdp-routes  gw-api  kustomization.yaml
➜  crdp git:(main) ✗ openssl req -x509 -newkey rsa:2048 -sha256 -days 365 -nodes -keyout tls.key -out tls.crt -subj "/C=UK/ST=Eng/L=Limoges/O=yourorg/CN=*.\<domain-name\>"
➜  crdp git:(main) ✗ mv tls.key tls.cert ./gw-api/tls
````
2. Get a Registration Token
    - Log onto your CipherTrust Manager > Application Protection > Add Application > Connector Type set to 'CRDP' and follow wizard (leave default values if unsure)
    - Click on the created application and click 'Copy' to copy the Registration Token
    - Create a file named 'value' in crdp/regtoken folder and simply copy this token in this file 'value'. For example, run:
    ````
    ➜  crdp git:(main) ✗ echo <your-registration-token> ./crdp/regtoken/value
    ````    

3. Update **crdp-routes/kustomization.yaml**: 
Modify Lines 4 and 15 as prescribed below.:
````
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: kust

configMapGenerator:
- name: route-config
  literals:
  - hostname=crdp-kust.kiukairor.local # Modify here to your hostname for CRDP
...
````
  - Replace 'namespace: kust' by 'namespace: \<crdp-namespace\> (See step 0.)
  - Replace 'hostname=crdp-kust.kiukairor.local' by 'hostname=\<crdp-hostname\>' (Hostname of your choice, your clients should be able to resolve it).
Hence the file should look like:
````
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: \<crdp-namespace\>
...
configMapGenerator:
- name: route-config
  literals:
  - hostname=\<crdp-hostname\> # Modify here to your hostname for CRDP
...
````

4. Update **crdp/kustomization.yaml**:

````
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: kust
...
configMapGenerator:
- name: crdp-config
  literals:
  - TLS_MODE=no-tls                 # no-tls, tls-cert-opt, tsl-cert
  - CM_HOST=cm-ninja.kiukairor.com  # Modify here to your hostname/IP for CipherTrust

...
````
  - Replace 'namespace: kust' by 'namespace: \<crdp-namespace\> (See step 0.)
  - Replace 'CM_HOST=cm-ninja.kiukairor.com' by CM_HOST=\<ciphertrust-hostname\> (If using hostname, ensure your (CRDP) pods will be able to resolve your ciphertrust)

Hence the file should become: 

````
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: \<crdp-namespace\>
...
configMapGenerator:
- name: crdp-config
  literals:
  - TLS_MODE=no-tls                   # no-tls, tls-cert-opt, tsl-cert
  - CM_HOST=\<ciphertrust-hostname\>  # Modify here to your hostname/IP for CipherTrust

...
````

5. At root level of this project, run:
````
➜  crdp git:(main) ✗ kubectl apply -k .
```` 

6. To get your gateway NodePort, run:
````
➜  crdp git:(main) ✗ kubectl -n nginx-gateway get svc
NAME            TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
nginx-gateway   NodePort   10.100.156.252   <none>        80:30116/TCP,443:31244/TCP   13h
````
Here the https port is 31244. 
Browse/Curl to https://\<crdp-hostname\>:\<https-port\>/liveness and verify that CRDP is running (you may need to accept SSL/TLS certificate warning).

````
➜  crdp git:(main) ✗  curl --request GET -k --url https://<your-crdp-hostname>:<https-port>/liveness
````
7. Start using CRDP capabilities. 
Check https://thalesdocs.com/ctp/con/crdp/latest/admin/crdp-quick-start/index.html and https://thalesdocs.com/ctp/con/crdp/latest/crdp-apis/index.html 

8. To uninstall things, at the root level again:
````
➜  crdp git:(main) ✗ kubectl delete -k .
➜  crdp git:(main) ✗ kubectl delete ns <crdp-namespace>
```` 
Don't worry if you see 'NotFound' errors, it is likely due to the fact that some CRDs are deleted before the objects themselves. It should not a be a concern for this demo project.


# Prereqs
- CipherTrust manager with CRDP licensed,
- A reasonably recent K8s cluster with kubectl configured (this was tested on 1.29, with kustomize 5.0),
- A way to resolve to the proper K8s worker node for clients. When your client try to access 'crdp.\<domain-name\>', it should be redirected to the worker node where the Gateway API is running.


## Cluster Prereqs
- a TLS key and TLS cert for the Gateway API or generate them on the fly as describe above. 


# Next Steps
- Add the possibility to deploy a keycloak IDP to handle CRDP authorisation (See https://thalesdocs.com/ctp/cm/2.19/admin/adp_ag/adp-cm-crdp/defn-app-crdp/index.html)
- Use Secrets Manager for dealing with secrets (e.g. tls secret, reg token)
- Add TLS between Gateway and/or passthrough mode.


