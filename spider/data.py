from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium
from selenium.webdriver.chrome.service import Service
from time import sleep
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',  
    db='db',
    port=3306,
)


service = Service('msedgedriver.exe')
service.start()
dr = webdriver.Remote(service.service_url)

dr.get('https://gkcx.eol.cn/school/46/provinceline')
dr.execute_script('localStorage.setItem("localprovincename","广州市")')
dr.execute_script('localStorage.setItem("localprovinceid","44")')
dr.execute_script("""localStorage.setItem("birthplace",'{"id":"44","name":"广东"}')""")

flag = 0
# for i in range(2906,4000):
for i in list:
    
    try:
        url = 'https://gkcx.eol.cn/school/'+str(i)+'/provinceline'
        dr.get(url)
        # dr.refresh()
            
        sleep(1)
        if not dr.current_url.endswith("provinceline"):
            continue
        name = ""
        try :
            name = dr.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div/div/div[1]/div[2]/div/div[3]/div[2]/div[1]/span").text
        except selenium.common.exceptions.NoSuchElementException:
            continue
        cursor = connection.cursor()

        #切换时间
        year_box_active_btn = dr.find_element(By.XPATH,"""//*[@id="form3"]/div/div/div/span/div/div/span/i""")
        year_box_active_btn.click()
        year_box_active_btn.click()
        sleep(1)
        year_box = dr.find_elements(By.XPATH,"""/html/body/div[3]/div/div/div/ul/li""")
        liyear = None
        for iyear in year_box:
            if iyear.text == "2019":
                liyear = iyear
                break;
        year_box_active_btn.click()
        sleep(1)
        liyear.click()
        # 获取文科理科
        type_box_active_btn = dr.find_element(By.XPATH,"""//*[@id="proline"]/div[1]/div/div[3]/div/div/span/i""")
        type_box_active_btn.click()
        type_box_active_btn.click()
        sleep(1)
        type_box = dr.find_elements(By.XPATH,"""/html/body/div[3]/div/div/div/ul/li""")
        for type_btn in type_box:
            # 切换文科理科
            type_box_active_btn.click()
            sleep(1)
            student_type = type_btn.text
            if student_type == "科类":
                continue
            type_btn.click()
            sleep(1)
            # 获取对应信息
            txt = dr.find_element(By.XPATH,"""//*[@id="proline"]/div[2]/div[1]/table/tbody""")
            datalist = txt.text.split('\n')[1:]
            if datalist[0].startswith("-"):
                raise Exception("-")
            
            for data_item in datalist:
                s = data_item.split(' ')
                sql = "insert into school_info (year,school_name,epoch,lowest_score,lowest_rank,student_type) value ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(s[0],name,s[1],s[3].split("/")[0],s[3].split("/")[1],student_type)
                cursor.execute(sql)
            
            for data_item in datalist:
                s = data_item.split(' ')
                sql = "insert into school_info (year,school_name,epoch,lowest_score,lowest_rank,subject_choose,student_type,type_985,type_211) value ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(s[0],name,s[1],s[3].split("/")[0],s[3].split("/")[1],s[-1],student_type,is_985,is_211)
                cursor.execute(sql)

        subject_year =  dr.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div[3]/div[1]/div/div[2]/form/div/div/div/span/div/div/div/div").text
        student_type = dr.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div[3]/div[1]/div/div[3]/div/div/div/div").text

        # 获取文科理科
        type_box_active_btn = dr.find_element(By.XPATH,"""//*[@id="scoreline"]/div[1]/div/div[3]/div/div/span/i""")
        type_box_active_btn.click()
        type_box_active_btn.click()
        sleep(1)
        type_box = dr.find_elements(By.XPATH,"""/html/body/div[4]/div/div/div/ul/li""")
        for type_btn in type_box:
            # 切换文科理科
            type_box_active_btn.click()
            sleep(1)
            student_type = type_btn.text
            if student_type == "科类":
                continue
            type_btn.click()
            sleep(1)
            # 获取对应信息
            pagenation_box = dr.find_elements(By.XPATH,"""//*[@id="scoreline"]/div[2]/div[3]/div/div/ul/li""")[1:-1]
            for page_btn in pagenation_box:
                if page_btn.is_displayed():
                    page_btn.click()
                    sleep(1)
                subject_data_table = dr.find_element(By.XPATH,"""//*[@id="scoreline"]/div[2]/div[1]/table/tbody""")
                subject_data=subject_data_table.find_elements(By.TAG_NAME,"tr")[1:]
                for j in subject_data:
                    tds = j.find_elements(By.TAG_NAME,"td")
                    if tds[0].text.startswith("-"):
                        raise Exception("-")
                    sql2 = "insert into school_subject_info (school_name,profession_name,student_type,year,lowest_score,avg_score,lowest_rank,epoch) value ('%s','%s','%s','%s','%s','%s','%s','%s')"%(name,tds[0].text,student_type,subject_year,tds[3].text.split("/")[0],tds[2].text,tds[3].text.split("/")[1],tds[1].text)
                    cursor.execute(sql2)

        connection.commit()
        cursor.close()
        flag = 0
        print("success " + str(i) + "\n")
    except:
        with open("err.txt","a") as file :
            file.write(str(i)+"\n")
        continue
        
    
    
    
    
connection.close()

dr.quit()