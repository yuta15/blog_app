# Docker DB

このフォルダは、MySQLデータベースコンテナを設定および管理するためのものです。
このフォルダ内には、必要な環境変数の設定ファイルとREADMEが含まれています。

## フォルダの構成
```
.
├── .env
└── README.md
```

## 必要な環境変数
 以下の環境変数を設定して、MySQLコンテナを正しく構成します。
 - `MYSQL_ROOT_PASSWORD`: MySQLのrootユーザーのパスワード。
 - `MYSQL_DATABASE`: コンテナ起動時に作成されるデータベースの名前。
 - `MYSQL_USER`: 新しく作成されるユーザーの名前。
 - `MYSQL_PASSWORD`: 新しく作成されるユーザーのパスワード。

## 注意事項
- パスワード情報等が含まれるため、GithubにPushしないよう.gitignoreに含めること。
