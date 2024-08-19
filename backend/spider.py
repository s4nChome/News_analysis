from playwright.sync_api import sync_playwright

def scrape_links_and_titles(url, keyword='mil'):
    with sync_playwright() as playwright:
        # 启动浏览器，这里使用无头模式的 Firefox
        browser = playwright.firefox.launch(headless=True)
        page = browser.new_page()  # 打开新页面

        # 访问指定的 URL
        page.goto(url)

        # 等待页面加载完成
        page.wait_for_load_state('networkidle')

        # 使用 CSS 选择器找到所有的 <a> 标签
        links = page.query_selector_all('a')

        # 创建一个字典来存储唯一的链接和标题
        unique_links = {}

        # 遍历所有找到的链接，并提取 URL 和文本内容
        for link in links:
            href = link.get_attribute('href')  # 获取 href 属性
            if href and keyword in href:  # 确保 href 包含关键词 'mil'
                title = link.text_content()  # 获取链接的文本内容
                # 如果链接已存在但没有标题，或者新的标题更有信息价值，则更新
                if href not in unique_links or not unique_links[href]:
                    unique_links[href] = title

        # 关闭浏览器
        browser.close()

        # 将字典转换为列表，包含链接和标题的字典
        result_links = [{'url': url, 'title': title} for url, title in unique_links.items() if title]

        return result_links

# # 测试脚本
# url = 'http://www.news.cn/milpro/index.htm'  # 替换为实际的 URL
# links_with_titles = scrape_links_and_titles(url)
# print(links_with_titles)
