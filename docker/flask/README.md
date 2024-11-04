# Docker Flask

このフォルダは、Flaskアプリケーションコンテナを設定および管理するためのものです。このフォルダ内には、必要な環境変数の設定ファイル、README、およびDockerfileが含まれています。

## フォルダの構成
```
.
├── .env
├── README.md
└── dockerfile
```

## .envファイルの内容
`.env`ファイルには、Flaskアプリケーションを設定するための環境変数が含まれています。

## 必要な環境変数
以下の環境変数を設定して、Flaskコンテナを正しく構成します。

- `FLASK_APP`: Flaskのアプリケーションを登録
- `FLASK_ENV`: Flaskの環境（開発、テスト、本番など）。
- `FLASK_ROOT_DIR`: Flaskアプリケーションのルートディレクトリ。
- `DB_USERNAME`: データベースのユーザー名。
- `DB_PASSWORD`: データベースのパスワード。
- `DB_PORT`: データベースのポート番号。
- `DB_HOSTNAME`: データベースのホスト名（開発環境用）。
- `TEST_DB_HOSTNAME`: データベースのホスト名（テスト環境用）。
- `TEST_DB_PORT`: テストデータベースのポート番号。

## 注意事項
- パスワード情報等が含まれるため、GithubにPushしないよう.gitignoreに含めること。
