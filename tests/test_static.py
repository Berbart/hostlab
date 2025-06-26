import os
from playwright.sync_api import sync_playwright


def test_index_page():
    file_path = os.path.abspath(os.path.join('public', 'index.html'))
    assert os.path.exists(file_path), 'index.html missing'

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f'file://{file_path}')
        header = page.text_content('h1')
        assert header == 'Welcome to Codex Playground'
        browser.close()
