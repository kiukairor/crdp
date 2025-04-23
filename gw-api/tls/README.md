# No TLS files
If you do not have a TLS cert & key. Place the 2 created file in this folder tls/.

````
openssl req -x509 -newkey rsa:2048 -sha256 -days 365 -nodes -keyout tls.key -out tls.crt -subj "/C=UK/ST=Eng/L=London/O=yourorg/CN=*.env.local"
````

# Use your TLS details
Place in this folder your 2 files:
- tls.key
- tls.crt
Where tls.crt is the cert on tls.key, issued by a CA of your choice. 
For the demo to be more elegant, you may want the CA to be trusted by your browsers/machine.