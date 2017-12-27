
from selenium import webdriver
import time
from bs4 import BeautifulSoup


driver=webdriver.Firefox()                 #用chrome浏览器打开
driver.get("http://www.zhihu.com")       #打开知乎
time.sleep(1)
#找到输入账号的框，并自动输入账号
driver.find_element_by_name('username').send_keys('15927117721')
time.sleep(1)
#找到输入密码的框，并自动输入账密码
driver.find_element_by_name('password').send_keys('csy001')
time.sleep(1)

try:
    driver.find_element_by_name('captcha').send_keys('')
    yanzhengma = input('验证码:')
    driver.find_element_by_name('captcha').send_keys(yanzhengma)

except:
    print('not need verification code')



driver.find_element_by_css_selector('Button.SignFlow-submitButton.Button--blue').click()
time.sleep(1)


cookie=driver.get_cookies()
time.sleep(2)

driver.find_element_by_css_selector('Input').send_keys('科技')
time.sleep(1)
driver.find_element_by_css_selector('Button.SearchBar-searchIcon.Button--primary').click()
time.sleep(1)


#加载更多问题
def execute_times(times):
    for i in range(times + 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
execute_times(10)

html=driver.page_source


soup1=BeautifulSoup(html,'lxml')
lines=soup1.find_all('a',attrs={'target':'_blank'})
question_urls=[]


#筛选question
for i in lines:
    if str(i.get('href'))[1:9] == 'question':
        question_urls.append(i.get('href'))
print(question_urls)

#打开某个问题的网址
driver.get("http://www.zhihu.com" + str(question_urls[4])[0:18])
#展开问题
try:
    driver.find_element_by_css_selector('Button.QuestionRichText-more.Button--plain').click()
except:
    print('not need expand question')

#展开评论
#driver.find_element_by_class_name('ContentItem-actions').click()
#driver.find_element_by_class_name('ContentItem-actions.Sticky.RichContent-actions.is-bottom').click()
 #   .find_element_by_css_selector('Button.ContentItem-action.Button--plain.Button--withIcon.Button--withLabel').click()
#comment_button_list=driver.find_elements_by_class_name('ContentItem-actions')       #包含的也算


# comment_button_list=driver.find_elements_by_class_name('Button.ContentItem-action.Button--plain.Button--withIcon.Button--withLabel')
# for comment_button in comment_button_list[3:12]:
#     print(comment_button.text)
#     if comment_button.text[-2]== '评':
#         comment_button.click()
#     time.sleep(1)

# for i in range(1,10):
#     print(comment_button_list[i].get_attribute('class'))
#    # if  comment_button_list[i-1].get_attribute('class')=='ContentItem-actions.RichContent-actions':
#     comment_button_list[i].find_element_by_css_selector('Button.ContentItem-action.Button--plain.Button--withIcon.Button--withLabel').click()
#     time.sleep(1)









html_question=driver.page_source
soup2=BeautifulSoup(html_question,'lxml')

#问题标题
question_header_title=soup2.find('h1',class_='QuestionHeader-title').text
print(question_header_title)

#问题明细page_source
question_header_detail=soup2.find('span',class_='RichText').text   #相关问题
print(question_header_detail)

#浏览次数
view_num=soup2.find('div',class_='NumberBoard QuestionFollowStatus-counts NumberBoard--divider')\
    .find('div',class_='NumberBoard-item')\
    .find('strong',class_='NumberBoard-itemValue').text
print(view_num)

#回答者
answerer=soup2.find_all('span',class_='UserLink AuthorInfo-name')
#answerer_list.find('a',class_='UserLink-link')

#答案
answer=soup2.find_all('span',class_='RichText CopyrightRichText-richText')

#答案的赞同数
agreement_num=soup2.find_all('button',class_='Button VoteButton VoteButton--up')


#评论



with open('question.txt', 'w') as f:
    f.write(question_header_title)
    f.write(question_header_detail)
    f.write(view_num)
    for i in range(1,20):
        f.write(answerer[i-1].text)
        f.write(answer[i-1].text)
        f.write(agreement_num[i-1].text)
    f.close


