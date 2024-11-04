# Docker Environment Setup

このディレクトリには、FlaskアプリケーションおよびMySQLデータベースをDockerコンテナで実行するための設定ファイルが含まれています。


## ディレクトリの構成
```
.
├── db                      DB用のディレクトリ
│   ├── .env                dbの環境変数を定義。詳細はREADMEを参照
│   └── README.md
├── docker-compose.yml
└── flask                   Flaskコンテナ用のディレクトリ
    ├── .env
    ├── README.md
    └── dockerfile          Flaskコンテナの環境変数を定義。詳細はREADMEを参照
```

## 環境の構築方法

### 1. DockerとDocker Composeのインストール
まず、DockerとDocker Composeがインストールされていることを確認してください。
インストールされていない場合は、公式サイトの手順に従ってインストールしてください。
- [Docker インストールガイド](https://docs.docker.com/get-docker/)
- [Docker Compose インストールガイド](https://docs.docker.com/compose/install/)

### 2. 環境変数の設定

#### db/.env
MySQLデータベース用の環境変数を設定します。
[方法はこちら](docker/db/README.md)

#### flask/.env
Flaskコンテナ用の環境変数を設定します。
[方法はこちら](docker/flask/README.md)

#### 起動方法
1. ディレクトリの移動
```
$cd docker
```

2. ビルド
```
$docker compose build
```

3. コンテナ起動
```
$docker compose up -d
```

4. コンテナ起動確認
以下のように起動を確認する。
正常に動作しない場合、再起動を繰り替えす可能性があります。
```
$docker compose ps

NAME        IMAGE          COMMAND                  SERVICE   CREATED             STATUS             PORTS
dev_db      mysql:latest   "docker-entrypoint.s…"   db        About an hour ago   Up About an hour   0.0.0.0:3306->3306/tcp, :::3306->3306/tcp, 33060/tcp
flask_app   docker-flask   "python3 -m blog_app…"   flask     About an hour ago   Up About an hour   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp
test_db     mysql:latest   "docker-entrypoint.s…"   test      About an hour ago   Up About an hour   33060/tcp, 0.0.0.0:33060->3306/tcp, :::33060->3306/tcp

```

5. コンテナの停止・削除
```
$docker compose down
```