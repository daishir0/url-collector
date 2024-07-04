import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
import sqlite3
import sys
import os
from datetime import datetime

# プログラムの概要説明:
# このプログラムは、指定された初期URLから始まり、リンクを辿ってHTMLページを収集し、
# SQLiteデータベースに保存します。収集するURLは、指定されたフィルタ文字列を含むものに限定されます。

# 処理の仕様:
# 1. 初期URLをデータベースに保存。
# 2. データベース内の未処理URLを取得し、処理を開始。
# 3. URLのHTMLコンテンツを取得し、ページ内のリンクを抽出。
# 4. 抽出したリンクがフィルタ文字列を含み、HTMLページである場合、データベースに保存。
# 5. 処理済みURLをデータベースに記録。
# 6. 上記のプロセスを未処理URLがなくなるまで繰り返す。

# コマンド例:
# 1. 初期URLが "http://example.com" で、フィルタ文字列が "example" の場合:
#    python url-collector.py http://example.com example
# 2. 初期URLが "http://test.com" で、フィルタ文字列が "test" の場合:
#    python url-collector.py http://test.com test

def is_html(url, cache={}):
    if url in cache:
        return cache[url]

    try:
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get("content-type", "").lower()
        is_html_result = "text/html" in content_type
    except Exception:
        is_html_result = False

    cache[url] = is_html_result
    return is_html_result

def get_domain(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS urls (url TEXT UNIQUE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS processed_urls (url TEXT UNIQUE)''') 
    conn.commit()

def process_urls(conn, initial_url, filter_string):
    create_tables(conn) 
    cursor = conn.cursor()

    cursor.execute('INSERT OR IGNORE INTO urls (url) VALUES (?)', (initial_url,))
    conn.commit()

    domains = []
    processed_urls = set()
    processed_count = 0 

    while True:
        cursor.execute('SELECT url FROM urls WHERE url NOT IN (SELECT url FROM processed_urls)')
        url_row = cursor.fetchone()
        if not url_row:
            break

        url = url_row[0]
        processed_count += 1  # 処理されたURLのカウント
        print(f"Processing URL {processed_count}: {url}")  # 処理中のURLとカウントを表示
        domain = get_domain(url)
        domains.append(domain)
        processed_urls.add(url)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")

        for link in links:
            href = link.get("href")
            if href and "#" in href:
                continue  # ページ内リンクをスキップ

            joined_url = urljoin(url, href)
            if not any(joined_url.startswith(domain) for domain in domains):
                continue

            if filter_string in joined_url and is_html(joined_url):
                cursor.execute('INSERT OR IGNORE INTO urls (url) VALUES (?)', (joined_url,))
                conn.commit()
                print(f"Adding new URL: {joined_url}")

        # 処理されたURLをデータベースに追加
        cursor.execute('INSERT OR IGNORE INTO processed_urls (url) VALUES (?)', (url,))
        conn.commit()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python url-collector.py initial_url filter_string")
        sys.exit(1)

    initial_url = sys.argv[1]
    filter_string = sys.argv[2]
    db_name = "urls.db"
    with sqlite3.connect(db_name) as conn:
        process_urls(conn, initial_url, filter_string)
