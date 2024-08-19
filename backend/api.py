from flask import request
from app import app
from methods import *
from spider import *

@app.route('/')
def hello():
    return 'Flask is running!'

@app.route('/api/getUrls', methods=['POST'])
def getUrls():
    try:
        data = request.json.get('data')
        res = scrape_links_and_titles(data)
        print(res)
        return api_response(data=res,message='链接获取成功！')
    except Exception as e:
        return api_response(message=str(e), code=400)

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
            
            id = save_news_data(res)
            res['id'] = id
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

            id = save_news_data(res)
            res['id'] = id
            return api_response(data=res,message='新闻真实性判断成功！')
        
            
    
    except Exception as e:
        return api_response(message=str(e), code=400)
     

@app.route('/api/analysis', methods=['POST'])
def analysis():
    try:
        id = request.json.get('id')
        content = request.json.get('data')
        res = analysis_news(content)
        test = save_analysis_result(id,res)
        print(test)
        return api_response(data=res,message='新闻分析成功！')
    
    except Exception as e:
        return api_response(message=str(e), code=400)
    

@app.route('/api/history', methods=['GET'])
def getHistory():
    pageNum = request.args.get('pageNum', 1,type=int)
    pageSize = request.args.get('pageSize', 10,type=int)

    total = Logs.query.count()
    totalPages = (total - 1) // pageSize + 1

    if pageNum > totalPages:
        pageNum = totalPages

    history_list = Logs.query.paginate(page=pageNum, per_page=pageSize, error_out=False)

    res = {
        "total": total,
        "list": [
            {
                "id":Logs.id,
                "url":Logs.url,
                "domain_category":Logs.domain_category,
                "title":Logs.title,
                "key_words":Logs.key_words,
                "content":Logs.content,
                "title_decision":Logs.title_decision,
                "title_score":Logs.title_score,
                "content_decision":Logs.content_decision,
                "content_score":Logs.content_score,
                "time":Logs.time,
                "analysis_result":Logs.analysis_result
            }
            for Logs in history_list.items
        ]
    }
    return api_response(data=res,message='历史记录获取成功！')
