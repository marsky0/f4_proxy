wget https://raw.githubusercontent.com/marsky0/f4_proxy/refs/heads/main/ping.py
mv ping.py /bin/

rm /etc/systemd/system/ping.service

echo "
[Unit]
Description=Binance Ping
After=network.target

[Service]
ExecStart=/bin/python3 /bin/ping.py 
Restart=always

[Install]
WantedBy=multi-user.target
" >> /etc/systemd/system/ping.service

systemctl daemon-reload
systemctl enable --now ping.service

echo "Installation complete"
