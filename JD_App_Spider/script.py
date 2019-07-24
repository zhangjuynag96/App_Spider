#-*-coding:UTF-8-*-
import pymongo
import json
from mitmproxy import ctx
import re
import jsonpath_rw_ext

def response(flow):
    client = pymongo.MongoClient('localhost')
    db = client['jd']
    products_collection = db['products']
    comments_collection = db['comments']
    products_detail_collection = db['detail']

    product_url = 'client.action?functionId=wareBusiness'
    if product_url in flow.request.url:
        text = flow.response.text
        data = json.loads(text)
        name = jsonpath_rw_ext.match('$..wareInfo[name]',data)[0]
        id = jsonpath_rw_ext.match('$..wareInfo[skuId]',data)[0]
        wareImage = jsonpath_rw_ext.match('$..wareImage',data)[0]
        image = jsonpath_rw_ext.match('$..big',wareImage)[0]
        price = jsonpath_rw_ext.match('$..shareImgInfo[jprice]',data)[0]
        products_collection.insert({
            'id': id,
            'name': name,
            'images': image,
            'price':price
        })

    info_url = 'https://in.m.jd.com/product/guige/'
    if info_url in flow.request.url:
        text = flow.response.text
        pattern_id = re.compile('<input type="hidden" name="wareId" id="wareId" value=\'(\d+)\'/>')
        id = pattern_id.findall(text)[0]
        pattern_info = re.compile('<input type="hidden" name="wareGuigNew" id="wareGuigNew" value=\\\'(.*?)\\\'/>')
        info = pattern_info.findall(text)[0]
        info = eval(info)
        products_detail_collection.insert({
            'id':id,
            'info':info
        })

    comment_url = '/client.action?functionId=getCommentListWithCard'
    if comment_url in flow.request.url:
        text = flow.response.text
        data = json.loads(text)
        # 提取商品id
        re_id = jsonpath_rw_ext.match('$..ckeKeyWordBury',data)
        re_id = re_id[0]
        pattern = re.compile('\^\^sku=(\d+)\^\^')
        id = pattern.findall(re_id)
        id = id[0]
        #提取评论信息
        comments = jsonpath_rw_ext.match('$..commentInfo',data)
        for comment in comments:
            usernickname = jsonpath_rw_ext.match('$..userNickName',comment)[0]
            userlevel = jsonpath_rw_ext.match('$..userLevel',comment)[0]
            commentid = jsonpath_rw_ext.match('$..commentId',comment)[0]
            date = jsonpath_rw_ext.match('$..commentDate',comment)[0]
            commentstar = jsonpath_rw_ext.match('$..commentScore',comment)[0]
            content = jsonpath_rw_ext.match('$..commentData',comment)[0]
            type = jsonpath_rw_ext.match('$..wareAttribute',comment)[0]
            comments_collection.insert({
                'id': id,
                'usernickname':usernickname,
                'userid':commentid,
                'userlevel':userlevel,
                'date':date,
                'commentstar':commentstar,
                'content':content,
                'type':type
            })


