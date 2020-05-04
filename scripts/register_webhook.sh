BOT_KEY="1102340901:AAFwABs_KFtsth_BVRjOXjEMWxQMOawpFQc"
SERVER_DOMAIN="34.87.149.238"
curl \
-F "url=https://${SERVER_DOMAIN}/webhook" \
-F "certificate=@/cygdrive/d/workspace/telefx/ssl/public.pem" \
-F "allowed_updates[]=message" \
https://api.telegram.org/bot${BOT_KEY}/setWebhook
