# release

`subdomain1.example.com`は、
「フロントエンド、バックエンド、証明書の中身と利用者PCの`hosts`」
の全てで統一する必要がある。

## Setup

### 認証局証明書作成

ブラウザにインストールする認証局証明書`ca.crt`を作成

```bash
# CA 秘密鍵の生成
openssl genrsa -out ca.key 2048

# CA 証明書の生成
openssl req -x509 -new -nodes -key ca.key -sha256 -days 1024 -out ca.crt \
  -subj "/C=JP/ST=Aichi/L=Nagoya/O=YourOrganization/OU=IT/CN=your-ca.com"
```

### サーバー証明書作成

Nginxにインストールするサーバー証明書`*.crt`とその秘密鍵`*.key`を作成

```bash
# subdomain1の証明書生成
openssl genrsa -out subdomain1.key 2048
openssl req -new -key subdomain1.key -out subdomain1.csr \
  -subj "/C=JP/ST=Aichi/L=Nagoya/O=YourOrganization/OU=Server/CN=subdomain1.example.com"
openssl x509 -req -in subdomain1.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial -out subdomain1.crt -days 365 -sha256
```

### コンテナ設定

#### `release/compose.yaml`で使うために証明書を配置する

```bash
mkdir -p ./release/backup/
cp ./release/certs/* ./release/backup/ # 期限切れ証明書のバックアップ
mv ./release/subdomain1.{crt,key} ./release/certs/
```

#### 環境変数を設定

```.env
Front_URL=http://subdomain1.example.com
VITE_BACK_URL=http://subdomain1.example.com/api
```

### コンテナ起動

`../deploy.sh`でdockerコンテナを起動

<https://localhost/>と<http://localhost:8000>にアクセスして動作確認

## How to access from client

任意のPCで上記の`ca.crt`をインストールする。

Windowsの`hosts`ファイルに下記を追記

`x.x.x.x`はこのドッカーコンテナを起動している物理マシンのIPもしくはhostname

```text
x.x.x.x subdomain1.example.com 
```

<https://subdomain1.example.com> と
<https://subdomain1.example.com/api/docs>
にアクセスして動作確認。
