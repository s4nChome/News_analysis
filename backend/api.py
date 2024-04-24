from flask import request
from app import app
from methods import *

@app.route('/')
def hello():
    return 'Flask is running!'

@app.route('/api/getResult', methods=['POST'])
def getResult():
    try:
        data = request.json.get('data')

        if is_valid_url(data):
            title, content = get_single_article(data)
            key_words = extract_keywords(content)
            if is_offical_news_url(data):
                res = {
                    "url": data,
                    "title": title,
                    "key_words": key_words,
                    "content": content,
                    "title_decision": "impartial",
                    "title_score": 1,
                    "content_decision": "impartial",
                    "content_score": 1,
                    "domain_category": "trusted"
                 }
            else:
                title_decision, title_score, content_decision, content_score, domain_category = is_real_news(data,title,content)
                res = {
                    "url": data,
                    "title": title,
                    "key_words": key_words,
                    "content": content,
                    "title_decision": title_decision,
                    "title_score": title_score,
                    "content_decision": content_decision,
                    "content_score": content_score,
                    "domain_category": domain_category
                }
            
            save_news_data(res)
            return api_response(data=res,message='新闻获取成功！')

        else:
            title_decision, title_score, content_decision, content_score, domain_category = is_real_news(content=data)
            key_words = extract_keywords(data)
            res = {
                "url": "",
                "title": "",
                "key_words": key_words,
                "content": data,
                "title_decision": title_decision,
                "title_score": title_score,
                "content_decision": content_decision,
                "content_score": content_score,
                "domain_category": domain_category
            }

            save_news_data(res)
            return api_response(data=res,message='新闻真实性判断成功！')
        
            
    
    except Exception as e:
        return api_response(message=str(e), code=400)
     

@app.route('/api/analysis', methods=['POST'])
def analysis():
    try:
        content = request.json.get('data')
        res = analysis_news(content)
        return api_response(data=res,message='新闻分析成功！')
    
    except Exception as e:
        return api_response(message=str(e), code=400)