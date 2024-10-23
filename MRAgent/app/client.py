import streamlit as st
from langserve import RemoteRunnable

import streamlit as st


# Function to generate word cloud
def generate_wordcloud(s):
    import re
    import jieba
    import wordcloud
    import matplotlib.pyplot as plt

    ls = jieba.lcut(s) # 生成分词列表
    text = ' '.join(ls) # 连接成字符串
    stopwords = ["的","是","了"] # 去掉不需要显示的词
    
    wc = wordcloud.WordCloud(font_path="msyh.ttc",
                         width = 1000,
                         height = 700,
                         background_color='white',
                         max_words=100,stopwords=stopwords).generate(text)

    plt.figure(figsize=(5, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# 使用 Markdown 和样式增强标题，包括图标和渐变色
st.markdown("""
<h1 style='text-align: center; color: blue; background: linear-gradient(to right, red, purple); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
      📊 社群 实时数据分析
</h1>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["chat", "詞雲圖"])

with tab1:
    input_text = st.text_input("请输入问题:", key="2")

    if input_text:
        with st.spinner("正在处理..."):
            try:
                app = RemoteRunnable("http://localhost:8000/socialagent_chat")
                responses = []
                for output in app.stream({"input": input_text}):
                    responses.append(output)
                if responses:
                    st.subheader('分析结果')
                    last_response = responses[-1]
                    st.markdown(last_response["generate"]["generation"])

                    # 收缩显示 documents 的内容
                    with st.expander("查看详细推荐信息"):
                        for idx, doc in enumerate(last_response.get("documents", [])):
                            st.write(f"### 视频 {idx + 1}")
                            st.json(doc)  # 展示每个文档的详细内容
                else:
                    st.info("没有返回结果。")
            except Exception as e:
                st.error(f"处理时出现错误: {str(e)}")

with tab2:
    #直接抓取數據可能會有代理問題 採用測試數據
    s=''  
    with open('./coffee.txt', 'r',encoding='utf-8') as file:
         s = file.read()
    generate_wordcloud(s)

