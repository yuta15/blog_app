"""
実行用ファイル
"""

from blog_app import create_app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="172.19.0.2",
        port=5000
    )