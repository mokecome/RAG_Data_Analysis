
#分析對雀巢咖啡 優點缺點 ->提出行銷建議
#對公關人員(負面事件討論方向)  想快速掌握危機事件中網友關注焦點，以採取適當的應對處理
#產品經理 自身與競品的好感度差異解讀
import requests
import re
import json
import datetime
from typing import List

#模擬數據
#商品留言數 點讚數  
mock_data = [
        {'brand': '雀巢（Nestle）', 'arcurl': 'https://item.jd.com/100021363497.html', 
         'title': '雀巢（Nestle）咖啡粉1+2原味低糖*微研磨三合一学生工作速溶冲调饮品30条450g',
         'description': '原味\n中度烘焙\n普通盒装',
         'play': 2123,'favorites': 1039}]
def fetch_comments(start,end):
    comments_list = []
    for i in range(start,end):
        url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=1233203&score=0&sortType=5&pageSize=10&isShadowSku=0&fold=1&page='
        finalurl = url + str(i) + '&pageSize=10&isShadowSku=0&fold=1'

        header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"}

        data = requests.get(url=finalurl,headers=header).text
        remodel_comment = re.compile(r'\"content\":\"([^"]+)\",\"(?:creationTime|vcontent)\"')  # 匹配评论
        comment_list = remodel_comment.findall(data)
        comments_list.extend(comment_list)

    for p in comments_list:
        with open("coffee.txt", "a",encoding='utf-8') as f:
            f.write(p)
    return comments_list


def process_search_result(result):#mock_data
    data_to_write = []
    for item in result:
        comments = fetch_comments(1,50)  #獲取評論
        processed_data = [
            item.get('brand', '未知作者'),
            item.get('arcurl', '无链接'),
            item.get('title', '无标题'),
            item.get('play', 0),
            item.get('favorites', 0),
            comments,
        ]
        headers = ["品牌","商品鏈結","商品名","留言數","點讚數","評論"]
        result_text = '\n'.join(f"{header}: {data}" for header, data in zip(headers, processed_data))
        data_to_write.append(result_text)
    return json.dumps(data_to_write, ensure_ascii=False)



def result_pipiline(keywords: str):
    all_results = []
    for keyword in keywords:
        keyword_results = []
        for page in range(1, 2):
            real_data=process_search_result(mock_data)
            all_results.append({
                "keyword": keyword,
                "real_data": real_data
            })
        print(f"all_results: {json.dumps(all_results, indent=4, ensure_ascii=False)}")
        return all_results


if __name__ == '__main__':
    result_pipiline(keywords="雀巢咖啡的正負評論")