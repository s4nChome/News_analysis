from newspaper import Article
from flask import jsonify
import requests
from urllib.parse import urlparse
from models import Logs
from datetime import datetime
from app import db
import config
import jieba.analyse

Fakebox_url = 'http://localhost:8080/fakebox/check'

# 判断是否为合法url
def is_valid_url(url):
    if 'http://' in url or 'https://' in url:
        return True
    else:
        return False

# 获取单个页面的标题和内容
def get_single_article(url):
    article = Article(url, language='zh')
    article.download()
    article.parse()
    article.text = article.text.replace('\n', '')
    return article.title, article.text

# 判断新闻来源是否为官方新闻
def is_offical_news_url(url):
    official_domains = [
                        'news.cn',
                        'news.sina.com.cn',
                        'news.qq.com', 
                        'news.163.com', 
                        'news.ifeng.com', 
                        'news.sohu.com', 
                        'cctv.com', 
                        'news.xinhuanet.com'
                       ]
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return any(domain == official_domain or domain.endswith('.' + official_domain) for official_domain in official_domains)

# 判断新闻真实性
def is_real_news(url=None,title=None,content=None):
    data = {
        "url": url,
	    "title": title,
	    "content": content
    }

    res = requests.post(Fakebox_url, json=data)
    if res.status_code == 200:
        res = res.json()
        title_decision = res['title'].get('decision','')
        title_score = res['title'].get('score',None)
        content_decision = res['content'].get('decision','')
        content_score = res['content'].get('score',None)
        domain_category = res['domain'].get('category','')
    return title_decision, title_score, content_decision, content_score, domain_category

# 提取新闻关键词
def extract_keywords(content):
    jieba.analyse.set_stop_words("/home/s4nchome/文档/Code/military_news_analysis/backend/cn_stopwords.txt")
    keywords = jieba.analyse.extract_tags(content, topK=5)
    keywords = ','.join(keywords)
    return keywords

# 保存新闻数据
def save_news_data(res):
    save_news_data = Logs(
        url=res['url'],
        domain_category=res['domain_category'],
        key_words=res['key_words'],
        title=res['title'],
        title_decision=res['title_decision'],
        title_score=res['title_score'],
        content=res['content'],
        content_decision=res['content_decision'],
        content_score=res['content_score'],
        time=datetime.now(),
    )
    db.session.add(save_news_data)
    db.session.commit()
    return save_news_data.id

# 分析新闻
def analysis_news(content):
    import qianfan
    chat_comp = qianfan.ChatCompletion()

    res = chat_comp.do(model="ERNIE-SPEED-128K",messages=[
    {
        "role": "user",
        "content": "你是一个军事新闻分析专家，请你从包括但不限于战略意义，国际反应，经济后果，公众舆论，长远影响等方面对"+ content + "进行分析"
    }
])
    res = res['body']['result'].replace('\n','')

    return res


def api_response(data=None, message=None, code=200):
    response = {
        "data": data,
        "message": message,
        "code": code,
    }
    return jsonify(response)

# 保存分析结果
def save_analysis_result(id, result):
    save_analysis_result = Logs.query.filter_by(id=id).first()
    save_analysis_result.analysis_result = result
    db.session.commit()
    return save_analysis_result.id