
# coding: utf-8

# # modules

# In[23]:


import pandas as pd
import numpy as np
import requests
import json
import time
ts = time.time()
import pymongo
from bs4 import BeautifulSoup
import datetime


# # naver 100

# In[26]:


def naver_cat_id_maker(catID):
    url = "https://search.shopping.naver.com/best100v2/detail.nhn?catId=5000000" + str(catID)
    return url


# In[29]:


def naver_top100():
    df = pd.DataFrame(columns=["from", "catID" ,"rank","item_name", "price", "link", "date"])
    for ID in range(0, 9):
        response = requests.get(naver_cat_id_maker(ID)) # html code로 가져옴
        dom = BeautifulSoup(response.content, "html.parser") # 파싱
        lists = dom.select(".type_normal li") #여러개의 데이터 (리스트)
        for rnk, lst in enumerate(lists):
            df.loc[len(df)] = {
                "from":"Naver",
                "catID":list(filter(lambda x: x!="", [cat if i == ID else "" for i, cat in enumerate (['패션의류', '패션잡화', '화장품/미용', '디지털/가전', '가구/인테리어', '출산/육아', '스포츠/레저', '식품', '생활/건강',])]))[0], 
                "rank":rnk + 1,
                "item_name":lst.select_one(".cont a").text,
                "price":lst.select_one(".price .num").text,
                "link":lst.select_one(".cont a").attrs['href'],
                "date":datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            }
    return df


# In[30]:


get_ipython().run_cell_magic('time', '', 'naver_df = naver_top100()')


# In[31]:


naver_df


# # 도매꾹 100
# - 데이터 깨짐

# In[32]:


def domaeggook_cat_id_maker(catID):
    url = "http://domeggook.com/main/item/itemPopular.php?cat=01_0" + str(catID)
    return url


# In[33]:


def domaeggook_top100():
    df = pd.DataFrame(columns=["from", "catID" ,"rank","item_name", "price", "link", "date"])
    for ID in range(0, 6):
        response = requests.get(domaeggook_cat_id_maker(ID + 1)) # html code로 가져옴
        response.encoding = 'euc_kr'
        html = response.text
        dom = BeautifulSoup(html, "html.parser") # 파싱
        lists = dom.select("#itemPopularsUl li") #여러개의 데이터 (리스트)
        for rnk, lst in enumerate(lists):
            df.loc[len(df)] = {
                "from":"도매꾹",
                "catID":list(filter(lambda x: x!="", [cat if i == ID else "" for i, cat in enumerate (['패션잡화', '패션의류', '출산/육아', '가구/인테리어', '스포츠/레저', '디지털/가전',])]))[0], 
                "rank":rnk + 1,
                "item_name":lst.select_one(".info .title a").text.replace('\r','').replace('\n','').replace('\t',''),
                "price":lst.select_one(".info div:nth-of-type(2)").text[:len(lst.select_one(".info div:nth-of-type(2)").text)-1],
                "link":"http://domeggook.com/" + lst.select_one(".info .title a").attrs['href'],
                "date":datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            }
    return df


# In[34]:


get_ipython().run_cell_magic('time', '', 'domaeggook_df = domaeggook_top100()')


# In[35]:


domaeggook_df


# # 도매매 100

# In[287]:


# def domaemae_cat_id_maker(catID1, catID2):
#     url = "http://domeme.domeggook.com/main/item/supplyList.php?cat=0"+str(catID1)+"_0"+str(catID2)+"_00_00" 
#     return url


# In[299]:


# def domaemae_top100():
#     df = pd.DataFrame(columns=["from", "catID" ,"rank","item_name", "price", "link"])
#     for ID1 in range(0, 6):
#         for ID2 in range(0, 5):
#             response = requests.get(domaemae_cat_id_maker(ID1 + 1, ID2 + 1)) # html code로 가져옴
#             response.encoding = 'euc-kr'
#             html = response.content
#             dom = BeautifulSoup(html, "html.parser") # 파싱
#             lists = dom.select(".lItemList li") #여러개의 데이터 (리스트)
#             for rnk, lst in enumerate(lists):
#                 df.loc[len(df)] = { 
#                     "from":"도매매",
#                     "catID":list(filter(lambda x: x!="", [cat if i == ID1 else "" for i, cat in enumerate (['패션잡화', '패션의류', '출산/육아', '가구/인테리어', '스포츠/레저', '디지털/가전',])]))[0], 
#                     "rank":rnk + 1,
#                     "item_name":lst.select_one(".main a:nth-of-type(1)").text,
#                     "price":lst.select_one(".amtqty .infoDeli b").text,
#                     "link":"http://domeme.domeggook.com" + lst.select_one(".main a").attrs['href']
#                 }
#     return df


# In[300]:


# %%time
# domaemae_df = domaemae_top100()


# In[302]:


# domaemae_df


# # 11번가 100

# In[36]:


def eleventhst_cat_id_maker(catID):
    url = "http://www.11st.co.kr/html/bestSellerMain" + str(catID) + ".html" 
    return url


# In[37]:


def eleventhst_top100():
    df = pd.DataFrame(columns=["from", "catID" ,"rank","item_name", "price", "link", "date"])
    for ID in range(0, 9):
        response = requests.get(eleventhst_cat_id_maker(ID + 2)) # html code로 가져옴
        dom = BeautifulSoup(response.content, "html.parser") # 파싱
        lists = dom.select(".thumbnail_list ul li") #여러개의 데이터 (리스트)
        for rnk, lst in enumerate(lists):
            df.loc[len(df)] = {
                "from":"11번가",
                "catID":list(filter(lambda x: x!="", [cat if i == ID else "" for i, cat in enumerate (['패션의류', '패션잡화', '화장품/미용', '식품', '출산/육아', '가구/인테리어', '생활/건강', '스포츠/레저', '디지털/가전',])]))[0], 
                "rank":rnk + 1,
                "item_name":lst.select_one(".pup_info .pup_title a").text,
                "price":lst.select_one(".pup_info .pub_priceW .pub_salep").text.replace('~','').replace('원',''),
                "link":lst.select_one(".product_conts .pub_photo a").attrs['href'],
                "date":datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            }
    return df


# In[38]:


get_ipython().run_cell_magic('time', '', 'eleventhst_df = eleventhst_top100()')


# In[39]:


eleventhst_df


# # G마켓 200
# - request로 불가능 (태그안에 데이터를 가져오지 못함)

# In[101]:


# def gmarket_cat_id_maker(catID):
#     url = "http://corners.gmarket.co.kr/Bestsellers?viewType=G&groupCode=G0" + str(catID)
#     return url


# In[250]:


# response = requests.get(gmarket_cat_id_maker(1)) # html code로 가져옴
# response.encoding = 'euc-kr'
# html = response.text
# dom = BeautifulSoup(html, "html.parser") # 파싱
# lists = dom.select(".best-list li") #여러개의 데이터 (리스트)


# In[116]:


# def gmarket_top200():
#     df = pd.DataFrame(columns=["from", "catID" ,"rank","item_name", "price", "link"])
#     for ID in range(0, 9):
#         response = requests.get(gmarket_cat_id_maker(ID + 1)) # html code로 가져옴
#         dom = BeautifulSoup(response.content, "html.parser") # 파싱
#         lists = dom.select(".best-list li") #여러개의 데이터 (리스트)
#         for rnk, lst in enumerate(lists):
#             df.loc[len(df)] = {
#                 "from":"Gmarket",
#                 "catID":list(filter(lambda x: x!="", [cat if i == ID else "" for i, cat in enumerate (['패션의류', '패션잡화', '화장품/미용', '출산/육아', '스포츠/레저', '디지털/가전', '식품', '생활/건강', '가구/인테리어',])]))[0], 
#                 "rank":rnk + 1,
#                 "item_name":lst.select_one(".thumb a:nth-of-type(2)").text,
#                 "price":lst.select_one(".item_price div:nth-of-type(2) span").text,
#                 "link":lst.select_one(".thumb a").attrs['href']
#             }
#     return df


# In[117]:


# %%time
# gmarket_df = gmarket_top200()


# # DB 저장

# In[40]:


client = pymongo.MongoClient("mongodb://localhost:27017/")
client


# In[41]:


db = client.crawl_data


# In[42]:


data = client.crawl_data.data


# In[43]:


naver = naver_df.to_dict('records')


# In[44]:


domaeggook = domaeggook_df.to_dict('records')


# In[45]:


eleventhst = eleventhst_df.to_dict('records')


# In[46]:


data.insert_many(naver)
data.insert_many(domaeggook)
data.insert_many(eleventhst)


# In[47]:


MONGO_QUERY = {}


# In[48]:


data.find(MONGO_QUERY).count()

