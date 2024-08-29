# release

## Setup

ブラウザにインストールする認証局証明書`ca.crt`

```bash
# CA 秘密鍵の生成
openssl genrsa -out ca.key 2048

# CA 証明書の生成
openssl req -x509 -new -nodes -key ca.key -sha256 -days 1024 -out ca.crt \
  -subj "/C=JP/ST=Aichi/L=Nagoya/O=YourOrganization/OU=IT/CN=your-ca.com"
```

Nginxにインストールするサーバー証明書

```bash
# subdomain1の証明書生成
openssl genrsa -out subdomain1.key 2048
openssl req -new -key subdomain1.key -out subdomain1.csr \
  -subj "/C=JP/ST=Aichi/L=Nagoya/O=YourOrganization/OU=Server/CN=subdomain1.example.com"
openssl x509 -req -in subdomain1.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial -out subdomain1.crt -days 365 -sha256

# subdomain2の証明書生成
openssl genrsa -out subdomain2.key 2048
openssl req -new -key subdomain2.key -out subdomain2.csr \
  -subj "/C=JP/ST=Aichi/L=Nagoya/O=YourOrganization/OU=Server/CN=subdomain2.example.com"
openssl x509 -req -in subdomain2.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial -out subdomain2.crt -days 365 -sha256
```

`release/compose.yaml`で使うために配置する

```bash
mkdir -p ./backup/
cp ./certs/server.* ./backup/ # 期限切れ証明書のバックアップ
mv ./server.* ./certs/
```

## How to access from client

Windowsの`hosts`ファイルに下記を追記

```text
subdomain1.example.com x.x.x.x
subdomain2.example.com x.x.x.x
```

ipではなくpcのhostnameでも可能

