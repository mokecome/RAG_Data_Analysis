
#分析對雀巢咖啡 優點缺點 ->提出行銷建議
#對公關人員(負面事件討論方向)  想快速掌握危機事件中網友關注焦點，以採取適當的應對處理
#產品經理 自身與競品的好感度差異解讀
import requests
import re
import json
import datetime
from typing import List


def get_spider():
    data_to_write = []
    processed_data=[]
    first = 1
    for i in range(1, 50):
        url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=1233203&score=0&sortType=5&pageSize=10&isShadowSku=0&fold=1&page='
        finalurl = url + str(i) + '&pageSize=10&isShadowSku=0&fold=1'

        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
                  }
        data = requests.get(url=finalurl,headers=header).text
        remodel_comment = re.compile(r'\"content\":\"([^"]+)\",\"(?:creationTime|vcontent)\"')  # 匹配评论
        comment_list = remodel_comment.findall(data)
        processed_data.extend(comment_list)

    for p in processed_data:
        with open("coffee.txt", "a",encoding='utf-8') as f:
            f.write(p)
    


    headers = ["評論"]
    result_text = '\n'.join(f"{header}: {data}" for header, data in zip(headers, [processed_data]))
    data_to_write.append(result_text)
   
    return json.dumps(data_to_write, ensure_ascii=False)


def result_pipiline(keywords: str):
    all_results = []

    real_data=get_spider()
    all_results.append({
        "keyword": keywords,
        "real_data": real_data
    })
    print(f"all_results: {json.dumps(all_results, indent=4, ensure_ascii=False)}")

    return all_results


