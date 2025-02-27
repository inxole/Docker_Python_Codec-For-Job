# release

`subdomain.example.com`は、
「フロントエンド、バックエンド、証明書の中身と利用者PCの`hosts`」
の全てで統一する必要がある。

## Setup

### opensslコマンドの設定ファイル作成

```san.ext
[ san_ext ]
subjectAltName = @alt_names

[alt_names ]
DNS.1 = subdomain.example.com
IP.1 = x.x.x.x
```

`x.x.x.x`の部分はホストになるOSのIP

### 認証局証明書作成

ブラウザにインストールする認証局証明書`ca.crt`を作成

```bash
# CA 秘密鍵の生成
openssl genrsa -out ca.key 2048

# CA 証明書の生成
openssl req -x509 -new -nodes -key ca.key -sha256 -days 1024 -out ca.crt \
  -subj "/C=JP/ST=Aichi/L=Nagoya/O=YourOrganization/OU=IT/CN=your-ca.com"
```

`-subj`フラグの値は状況に応じて修正。

### サーバー証明書作成

Nginxにインストールするサーバー証明書`*.crt`とその秘密鍵`*.key`を作成

```bash
# subdomain1の証明書生成
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr \
  -subj "/C=JP/ST=Aichi/L=Nagoya/O=YourOrganization/OU=Server/CN=subdomain.example.com"
openssl x509 -req -in server.csr \
  -extfile san.ext -extensions san_ext \
  -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha256
```

`-subj`フラグの値は状況に応じて修正。

### コンテナ設定

#### `release/compose.yaml`で使うために証明書を配置する

```bash
mkdir -p ./backup/
cp ./certs/* ./backup/ # 期限切れ証明書のバックアップ
mv ./server.{crt,key} ./certs/
```

#### 環境変数を設定

```.env
Front_URL=http://subdomain.example.com
VITE_BACK_URL=http://subdomain.example.com/api
```

### コンテナ起動

`../deploy.sh`でdockerコンテナを起動

<https://localhost/>と<http://localhost:8000>にアクセスして動作確認

## How to access from client

任意のPCで上記の`ca.crt`をインストールする。

Windowsの`hosts`ファイルに下記を追記

`x.x.x.x`はこのドッカーコンテナを起動している物理マシンのIPもしくはhostname

```text
x.x.x.x subdomain.example.com 
```

<https://subdomain.example.com> と
<https://subdomain.example.com/api/docs>
にアクセスして動作確認。
