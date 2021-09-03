openssl req -newkey rsa:2048 -sha256 -nodes -keyout private.key -x509 -days 3650 -out public.pem -subj "/C=vn/ST=hn/L=hn/O=lg/CN=${HOST}"
mv private.key public.pem ../ssl
