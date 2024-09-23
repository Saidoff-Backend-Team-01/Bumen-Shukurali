#!/bin/sh
echo "restarting gunicorn..."
sudo systemctl restart gunicorn
sudo systemctl restart nginx
echo "gunicorn restarted"
