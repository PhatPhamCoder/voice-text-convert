```
Tạo môi trường venv
```
## Truy cập đường dẫn thư mục home/ptech/ và tạo folder lưu source

``
mkdir ~/flaskApp
```

```
cd ~/flaskApp
```
## Tạo môi trường đặt tên là teton trong thư mục chưa source
python3 -m venv teton

## Kích hoạt môi trường ảo venv vừa tạo
```
source /home/ptech/env/teton/bin/active
```
## Cài dặt các thư viện trong thư mục requirements.txt
```
pip install -r requirements.txt
```
## Cài đặt ffmpeg và ffprobe cho thư viện Pydub

### Download the latest git build.

```
wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz

```

### Check MD5 file vừa download

```
wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz.md5

```

```
md5sum -c ffmpeg-git-amd64-static.tar.xz.md5

```
Kết quả trả về: ffmpeg-git-amd64-static.tar.xz: OK

### Giải nén thư mục ffmpeg vừa tải về


```
tar xvf ffmpeg-git-amd64-static.tar.xz
```

sudo mv ffmpeg-git-<version>-amd64-static/ffmpeg ffmpeg-git-<version>-amd64-static/ffprobe <Thư mục env>

Lưu ý chọn thư mục cần nạp ffmpeg và ffprobe vào đúng thư mục của môi trường đã tạo nằm trong source code

```
sudo mv ffmpeg-git-20180203-amd64-static/ffmpeg ffmpeg-git-20180203-amd64-static/ffprobe /home/ptech/env/teton/bin/
```

### Kiểm tra đường dẫn ffmpeg và ffprobe

```
whereis ffmpeg

whereis ffprobe

```


## Tại thư mục Source cài đặt thêm thư viện gunicorn để thiết đặt server giống với pm2


### Tạo và truy cập file service chạy gunicorn

```
sudo nano /etc/systemd/system/flask.service

```
### Lưu ý chỗ User chọn User đang dùng để đăng nhập Server

```
[Unit]
Description=Gunicorn instance to serve Flask app
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/ptech/hike
Environment="PATH=/home/ptech/env/teton/bin"
ExecStart=/home/ptech/env/teton/bin/gunicorn --workers 3 --bind unix:flask.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```

### Start dịch vụ vừa được tạo bằng các lệnh sau

```
sudo systemctl start flask.service

sudo systemctl enable flask.service

sudo systemctl status flask.service

```


### Cấu hình nginx

```
apt install nginx
```
### Installing and configure Firewall

```
apt install ufw
```

```
ufw enable
```

```
ufw allow "Nginx Full"
```


```
rm /etc/nginx/sites-available/default
```

```
rm /etc/nginx/sites-enabled/default
```

### Tạo file config mới

```
sudo nano /etc/nginx/sites-available/ptech
```

```
server {
    server_name tools.ptech.id.vn;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ptech/hike/flask.sock;
        client_max_body_size 30M;
    }
}

```

### Kiểm tra lỗi nginx

```
nginx -t
```

```
sudo systemctl start nginx
```

```
sudo systemctl reload nginx
```

```
sudo systemctl restart nginx
```


### Thiết lập SSL cho domain

```
apt install certbot python3-certbot-nginx
```

```
certbot --nginx -d tools.ptech.id.vn
```

### Setuo bot tự động renew chứng chỉ SSL

```
systemctl status certbot.timer
```
















