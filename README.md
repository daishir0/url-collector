# URL Collector

## Overview
URL Collector is a Python program that starts from a specified initial URL, follows links to collect HTML pages, and saves them in an SQLite database. The URLs collected are limited to those containing a specified filter string.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/daishir0/url-collector.git
    cd url-collector
    ```
2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Run the program with the initial URL and filter string:
    ```sh
    python url-collector.py <initial_url> <filter_string>
    ```
    Example:
    ```sh
    python url-collector.py http://example.com example
    ```

## Notes
- Ensure you have an active internet connection.
- The program will create a SQLite database named `urls.db` in the current directory.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

# URLコレクター

## 概要
URLコレクターは、指定された初期URLから始まり、リンクを辿ってHTMLページを収集し、SQLiteデータベースに保存するPythonプログラムです。収集するURLは、指定されたフィルタ文字列を含むものに限定されます。

## インストール方法
1. リポジトリをクローンします:
    ```sh
    git clone https://github.com/daishir0/url-collector.git
    cd url-collector
    ```
2. 必要なパッケージをインストールします:
    ```sh
    pip install -r requirements.txt
    ```

## 使い方
1. 初期URLとフィルタ文字列を指定してプログラムを実行します:
    ```sh
    python url-collector.py <initial_url> <filter_string>
    ```
    例:
    ```sh
    python url-collector.py http://example.com example
    ```

## 注意点
- インターネット接続が必要です。
- プログラムは現在のディレクトリに `urls.db` という名前のSQLiteデータベースを作成します。

## ライセンス
このプロジェクトはMITライセンスの下でライセンスされています。詳細はLICENSEファイルを参照してください。
