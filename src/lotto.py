from bs4 import BeautifulSoup
import requests
import json

head_Html_lottp = 'https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'
res = requests.get(head_Html_lottp, timeout=30)
soup = BeautifulSoup(res.text, 'lxml')


def lottery_day(css_class):
    if (css_class != None):
        if ("Lotto649Control_history_dlQuery_L649_DDate_" in css_class or "Lotto649Control_history_dlQuery_L649_EDate_" in css_class):
            return css_class


lottery_day_Info = soup.find_all(id=lottery_day)


winning_Numbers_Sort_lotto = [
    "Lotto649Control_history_dlQuery_No1_",
    "Lotto649Control_history_dlQuery_No2_",
    "Lotto649Control_history_dlQuery_No3_",
    "Lotto649Control_history_dlQuery_No4_",
    "Lotto649Control_history_dlQuery_No5_",
    "Lotto649Control_history_dlQuery_No6_",
    "Lotto649Control_history_dlQuery_SNo_",
]


def search_winning_numbers(css_class):
    # 在函式裡使用全域變數要加 global
    # global winning_Numbers_Sort_lotto
    if (css_class != None):
        for i in range(len(winning_Numbers_Sort_lotto)):
            if winning_Numbers_Sort_lotto[i] in css_class:
                return css_class


# find_all會把所有的標籤一個一個網內丟去比對想要篩選的項目
# 當進去之後會先過第一關，發現是要篩選id，所以沒有id的標籤就會轉換成None
# 如果有id的標籤，就會把篩選過後的id丟進去後方的function
# 然後只要丟進來的是None就不執行for
# 不是None就把傳進來的每一個標籤的id
# 去看有沒有包含winning_Numbers_Sort_lotto所定義的片段
# 也就是每一個不是None的標籤都會最多比7次
# 當比到有符合條件的
# 就會return這一個id
# 然後就會push一個包含這個id的標籤屬性與內容進header_Info
header_Info = soup.find_all(id=search_winning_numbers)


def parse_tw_lotto_html(data_Info, number_count):
    data_Info_List = []
    data_Info_Dict = {}
    # 標示這是哪一組大樂透
    tem_index = 0
    for index in range(len(data_Info)):
        # 因為每一組的index跟list都只append一次，而資料是7筆資料一組
        # 所以number_count = 7，所以每7的倍數就會進到下一組
        # 所以一數到7的倍數就要append進dict，然後清空list，index加一
        # 但是最初的那一次不用append跟清空任何東西，所以拉出來先做
        if (index == 0):
            # append like push
            data_Info_List.append(data_Info[index].text)
        else:
            if (index % number_count != 0):
                data_Info_List.append(data_Info[index].text)
            else:
                data_Info_Dict[str(tem_index)] = {
                    "public_day": lottery_day_Info[tem_index * 2].text,
                    "expire_day": lottery_day_Info[tem_index * 2 + 1].text,
                    "winning_numbers": data_Info_List
                }
                tem_index += 1
                data_Info_List = []
                data_Info_List.append(data_Info[index].text)
    data_Info_Dict[str(tem_index)] = {
        "public_day": lottery_day_Info[tem_index * 2].text,
        "expire_day": lottery_day_Info[tem_index * 2 + 1].text,
        "winning_numbers": data_Info_List
    }
    return data_Info_Dict


data_Info_Dict = parse_tw_lotto_html(header_Info, 7)

# 寫入json型別資料
with open("./public/data_Info_Dict.json", 'w') as f:
    json.dump(data_Info_Dict, f)  # python資料結構(一般為字典)轉換為JSON編碼的字串

# 讀取json型別資料
with open("./public/data_Info_Dict.json", 'r') as g:
    result_data = json.load(g)  # load是將一個JSON編碼的字串轉換回一個python資料結構
