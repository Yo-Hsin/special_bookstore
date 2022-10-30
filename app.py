import requests
import streamlit as st



def GetAllBookstore():
    url = "https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    res = response.json()
    return res

def GetCountyOption(items):
    option_list = []
    for item in items:
        if item['cityName'][0:3] not in option_list:
            option_list.append(item['cityName'][0:3])
    return option_list

def GetDistrictOption(items, target):
    option_list = []
    for item in items:
        name = item['cityName']
        if target not in name:
            continue
        name.strip()
        district = name[5:]
        if len(district) == 0:
            continue
        if district not in option_list:
            option_list.append(district)
    return option_list

def GetSpecificBookstore(items, county, districts):
    specific_bookstore_list = []
    for item in items:
        name = item['cityName']
        if county not in name:
            continue
        for district in districts:
            if district not in name:
                specific_bookstore_list.append(item)
    return specific_bookstore_list

def GetBookstoreInfo(items):
    expanderList = []
    for item in items:
        expander = st.expander(item['name'])
        expander.image(item['representImage'])
        expander.metric('hitRate', item['hitRate'])
        expander.subheader('Introduction')
        expander.write(item['intro'])
        expander.subheader('Address')
        expander.write(item['address'])
        expander.subheader('Open Time')
        expander.write(item['openTime'])
        expander.subheader('Email')
        expander.write(item['email'])
        expanderList.append(expander)
    return expanderList

def app():
    bookstore_list = GetAllBookstore()
    county_list = GetCountyOption(bookstore_list)
    st.header('特色書店地圖')
    st.metric('Total bookstore', len(bookstore_list)) # 將 118 替換成書店的數量
    county = st.selectbox('請選擇縣市', county_list)
    district = st.multiselect('請選擇區域', GetDistrictOption(bookstore_list, county))

    specific_bookstore = GetSpecificBookstore(bookstore_list, county, district)
    st.write(f'Total{len(specific_bookstore)} results')

    specific_bookstore.sort(key = lambda item: item['hitRate'], reverse=True)
    bookstore_info = GetBookstoreInfo(specific_bookstore)

if __name__ == '__main__':
    app()