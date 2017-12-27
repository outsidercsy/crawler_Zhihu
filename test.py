from bs4 import BeautifulSoup
html='''
<a target="_blank" data-za-detail-view-element_name="Title" href="/question/264110454/answer/280636972" data-reactid="497">中兴 42 岁员工坠亡悲剧发生后，你如何看待 30+ 职场危机？</a>
<a target="_blank" data-za-detail-view-element_name="Title" href="/question/62241319/answer/282123638" data-reactid="353">商业史上有哪些降维打击的经典案例？</a>
<div class="ContentItem-meta" data-reactid="354"></div>
'''

# soup1=BeautifulSoup(html,'lxml')
# tag_as=soup1.find_all('a',attrs={'target':'_blank'})
#
# for tag_a in tag_as:
#     print(tag_a.get('href'))

html2='<a class="UserLink-link" data-za-detail-view-element_name="User" href="/people/momo-jennie">Momo Jennie</a>'
soup2=BeautifulSoup(html2,'lxml')
# answerer=soup2.find('a',attrs={'class':'UserLink-link','data-za-detail-view-element_name':'User'}).text
answerer=soup2.find('a',class_='UserLink-link').text

print(answerer)
