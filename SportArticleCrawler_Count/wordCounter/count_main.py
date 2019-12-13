#from konlpy.tag import Komoran
from konlpy.tag import Okt
from collections import Counter

import csv

RDataLocation = 'readfile_location'
WDataLocation = 'writefile_location'


nlp = Okt()  # nlp 이름의 객체 생성

file = open(RDataLocation + 'readfile_name', 'r', encoding='euc-kr')
outfile = open(WDataLocation + 'writefile_name.csv', 'w', encoding='euc-kr', newline="")

line = csv.reader(file)
wcsv = csv.writer(outfile)


contents = ""

Rank = 500

# 각 csv 파일의 라인을 가져옴
for i in line:

    content = i[2]+i[3]  # 형태소 분석할 csv 데이터 저장

    contents += content


print(contents)

wcsv.writerow([contents])

noun_list = nlp.nouns(contents)  # 명사를 분리하여 저장
count = Counter(noun_list)


# Count 객체를 생성하고 참조변수 nouns 할당

result = {}

#  단어 검색 및 추가
for noun, count in count.most_common(Rank):

    print(noun + " : " + str(count) + "회")
    wcsv.writerow([noun, count])

