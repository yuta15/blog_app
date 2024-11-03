# local環境にてtestを実行する際に使用するDBを作成するためのDockerfile
# テスト実行前にこのファイルをビルドし、実行
FROM mysql:latest
ENV MYSQL_ROOT_PASSWORD iv9vGZMmGeJ8
ENV MYSQL_USER testuser
ENV MYSQL_PASSWORD sW5KMr5xiTWA
ENV MYSQL_DATABASE blog_app
EXPOSE 33060

# コマンド
# cd test_blog_app
# docker build -t mysql-test .
# docker run -dit --name mysql-test -p 33060:33060 mysql-test