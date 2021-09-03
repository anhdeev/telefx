curl \
-F "url=https://${HOST}/webhook" \
-F "certificate=/home/ubuntu/telefx/ssl/public.pem" \
-F "allowed_updates[]=message" \
https://api.telegram.org/bot${TELEGRAM_KEY}/setWebhook
