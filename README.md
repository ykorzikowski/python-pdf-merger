# Python PDF Merger

## Abstract

This little tool can be used as a helper for workflow engines like n8n for merging two pdf files together without installing additional packages on the n8n host. It provides a HTTP Post endpoint. 

## Usage

## Setup Local Dev

1. Setup python env

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```


## Setup

This is a possible configurstion using ansible to deploy: 

### Docker Compose

```yaml
version: "3.4"
services:
    pdf-merger:
        image: swokiz/tool-python-pdf-merger
        ports:
            - 8080:8000
        restart: always
```

### Reverse Proxy Configuration

```yaml
  - server_name: tool-pdf-merger.vpn.***.***
    vpn_only: true
    ssl:
      certificate_path: /etc/letsencrypt/live/***.com/fullchain.pem
      certificate_key_path:  /etc/letsencrypt/live/***.com/privkey.pem
    log:
      access_log_path: /var/log/nginx/acc_***_vpn_tool-pdf-merger.log
      error_log_path: /var/log/nginx/err_***_vpn_tool-pdf-merger.log
    proxy:
      proxy_pass: http://10.10.10.203:8080/
      proxy_options: |
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
```