from selenium import webdriver
import time
from bs4 import BeautifulSoup
import sys



# 问题内容爬取模块
def question_crawler(web):
    # 打开某个问题的网址
    driver.get("http://www.zhihu.com" + web)
    print(web)  # test
    fp = open((web.replace('/', '') + '.txt'), 'w', encoding='utf-8')

    # 加载所有回答
    answer_num_now = len(driver.find_elements_by_class_name('List-item'))
    answer_num_last = 0
    while answer_num_now > answer_num_last:
        execute_times(1)
        # time.sleep(1)
        answer_num_last = answer_num_now
        answer_num_now = len(driver.find_elements_by_class_name('List-item'))

    # 展开问题,有些问题无需展开
    try:
        execute_times(1)
        expand_question_button = driver.find_element_by_css_selector('Button.QuestionRichText-more.Button--plain')
        change_location(expand_question_button)
        expand_question_button.click()
        time.sleep(1)
    except:
        print('not need expand question')

    # 读取文本
    html_question = driver.page_source
    soup2 = BeautifulSoup(html_question, 'lxml')

    # 问题标题
    question_header_title = soup2.find('h1', class_='QuestionHeader-title').text
    fp.write('问题标题：' + question_header_title + '\n')

    # 问题明细page_source
    question_header_detail = soup2.find('span', class_='RichText')  # 相关问题
    if question_header_detail == None:
        fp.write('问题明细：' + '无' + '\n')
    else:
        fp.write('问题明细：' + question_header_detail.text + '\n')

    # 关注者和被浏览
    nodes = soup2.find('div', class_='NumberBoard QuestionFollowStatus-counts NumberBoard--divider').find_all('div',
                                                                                                              class_='NumberBoard-item')
    follower_num = nodes[0].find('strong', class_='NumberBoard-itemValue').text
    view_num = nodes[1].find('strong', class_='NumberBoard-itemValue').text
    fp.write('关注者：' + follower_num + '\n')

    fp.write('被浏览：' + view_num + '\n')

    # 回答者
    answerer = soup2.find_all('span', class_='UserLink AuthorInfo-name')

    # 答案
    answer = soup2.find_all('span', class_='RichText CopyrightRichText-richText')

    # 答案的赞同数
    agreement_num = soup2.find_all('button', class_='Button VoteButton VoteButton--up')

    # 评论
    for num in range(1, answer_num_now + 1):
        fp.write('\n\n')
        fp.write('回答者：' + answerer[num - 1].text + '\n')
        fp.write('答案：' + answer[num - 1].text + '\n')
        fp.write('答案赞同数：' + agreement_num[num - 1].text + '\n')
        fp.write('\n')
        fp.write('评论：' + '\n')

        try:
            # execute_times(1)
            slider_down()
            button = driver.find_element_by_xpath(
                '/html/body/div[1]/div/main/div/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[' + str(
                    num) + ']/div/div[2]/div[3]/button[1]')
        except:
            # execute_times(1)
            slider_down()
            button = driver.find_element_by_xpath(
                '/html/body/div[1]/div/main/div/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[' + str(
                    num) + ']/div/div[2]/div[3]/div/button[1]')

        if button.text == '添加评论':
            fp.write('无评论\n')
        else:
            comment_num = int(button.text.replace(' 条评论', ''))
            fp.write(str(comment_num) + '条评论\n')
            execute_times(1)
            change_location(button)
            # 点开评论
            button.click()
            time.sleep(1)
            read_comment_num = 0
            while comment_num > read_comment_num:
                # execute_times(1)
                slider_down()
                # 找出评论者
                comment_users = driver.find_elements_by_class_name('CommentItem-meta')
                # 找出评论内容
                comment_contents = driver.find_elements_by_class_name('RichText.CommentItem-content')
                # 将评论写入文件
                for i in range(1, len(comment_users) + 1):
                    fp.write(
                        comment_users[i - 1].text.replace('\n', '    ') + '\n' + comment_contents[i - 1].text + '\n')
                read_comment_num = read_comment_num + 20
                if comment_num > read_comment_num:
                    # execute_times(1)
                    slider_down()
                    try:
                        nextpage_button = driver.find_element_by_class_name(
                            'Button.PaginationButton.PaginationButton-next.Button--plain')
                        change_location(nextpage_button)
                        # 评论翻页
                        nextpage_button.click()
                        time.sleep(1)
                    except:
                        break
            # execute_times(1)
            try:
                # execute_times(1)
                slider_down()
                button = driver.find_element_by_xpath(
                    '/html/body/div[1]/div/main/div/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[' + str(
                        num) + ']/div/div[2]/div[3]/button[1]')
            except:
                # execute_times(1)
                slider_down()
                button = driver.find_element_by_xpath(
                    '/html/body/div[1]/div/main/div/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[' + str(
                        num) + ']/div/div[2]/div[3]/div/button[1]')

            change_location(button)
            # 收起评论
            button.click()
            #收起评论无需等待太长时间
            time.sleep(0.1)
    # 关闭当前问题的文件
    fp.close()


# 下拉滑动条，等待加载完成
def execute_times(times):
    for i in range(times + 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)


# 下拉滑动条,无需等待加载
def slider_down():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.1)


# 窗口上移5行
def change_location(button):
    button.location_once_scrolled_into_view
    driver.execute_script("window.scrollByLines(-10);")





#相关问题URL获取模块


#搜索子模块
driver = webdriver.Firefox()  # 用chrome浏览器打开
driver.get("https://www.zhihu.com/question/20714926")  # 打开知乎的某一个网站，跳过登入
time.sleep(1)

topic = input('话题：')
driver.find_element_by_css_selector('Input').send_keys(topic)
driver.find_element_by_xpath(
    '/html/body/div[1]/div/div[2]/header/div[1]/div[1]/div/form/div/div/div/div/button').click()
time.sleep(3)


#加载子模块
# 加载所有问题
question_num_now = len(driver.find_elements_by_class_name('List-item'))
question_num_last = 0
while question_num_now > question_num_last:
    print('已加载问题:' + str(question_num_now))
    execute_times(1)
    question_num_last = question_num_now
    question_num_now = len(driver.find_elements_by_class_name('List-item'))

html = driver.page_source

soup1 = BeautifulSoup(html, 'lxml')
lines = soup1.find_all('a', attrs={'target': '_blank'})
question_urls = []


#筛选子模块
# 筛选question
for i in lines:
    if str(i.get('href'))[1:9] == 'question':
        question_urls.append(i.get('href'))

print('问题数'+str(len(question_urls)))
if len(question_urls) <= 1:
    print('没有相关内容')
    sys.exit(0)
for question_url in question_urls[0:len(question_urls)-1]:#不爬取最后的知乎指南
    # 问题的编号可能有6位的和7位的
    # 调用问题内容爬取模块
    print('当前url'+str(question_url))
    try:
        if len(str(question_url)) < 20:
            question_crawler(str(question_url))
        elif str(question_url)[18] == '/':
            question_crawler(str(question_url)[0:18])
        elif str(question_url)[19] == '/':
            question_crawler(str(question_url)[0:19])
        else:
            pass
    except:
        pass
print('爬虫结束')
sys.exit(0)








#
# attention
# click前移动界面确保不被遮挡，click后等待三秒，找元素前移至最底端，
# css_selector 空格换成点

# encode decode 报错
# 问题有7位的编码
