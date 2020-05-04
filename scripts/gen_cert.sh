openssl req -newkey rsa:2048 -sha256 -nodes -keyout private.key -x509 -days 365 -out public.pem -subj "/C=vn/ST=hn/L=hn/O=lg/CN=34.87.149.238"
mv private.key public.pem ../ssl
