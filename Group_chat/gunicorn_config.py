bind = "0.0.0.0:8080"  # Bind to all interfaces on port 8080
module = "Group_chat.wsgi:application"

# SSL configuration
certfile = "/etc/letsencrypt/live/outofthegc.com/fullchain.pem"
keyfile = "/etc/letsencrypt/live/outofthegc.com/privkey.pem"
