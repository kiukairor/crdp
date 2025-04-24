# No TLS files
If you do not have a TLS cert & key, replace 'yourdomain' by the domain of your choice and run the command below
````
openssl req -x509 -newkey rsa:2048 -sha256 -days 365 -nodes -keyout tls.key -out tls.crt -subj "/C=XX/ST=YY/L=Limoges/O=yourorg/CN=*.yourdomain"
````

Place the 2 created files in gw-api/tls/ folder. Check root README for details.

# Use your TLS details
Place in this folder your 2 files:
- tls.key,
- tls.crt,
where tls.crt is the cert on tls.key, issued by a CA of your choice. 
For the demo to be more elegant, you may want the CA to be trusted by your browsers/machine.