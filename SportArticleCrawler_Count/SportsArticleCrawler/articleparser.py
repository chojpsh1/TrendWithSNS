from bs4 import BeautifulSoup
import requests
import re

from selenium import webdriver


class ArticleParser(object):
    def __init__(self):
        self.special_symbol = re.compile('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$&▲▶◆◀■【】\\\=\(\'\"]')
        self.content_pattern = re.compile('본문 내용|TV플레이어| 동영상 뉴스|flash 오류를 우회하기 위한 함수 추가function  flash removeCallback|tt|앵커 멘트|xa0')

    # 뉴스 데이터의 불필요 데이터 삭제
    def clear_content(self, text):
        # 기사 본문에서 필요없는 특수문자 및 본문 양식 등을 다 지움
        newline_symbol_removed_text = text.replace('\\n', '').replace('\\t', '')
        special_symbol_removed_content = re.sub(self.special_symbol, ' ', newline_symbol_removed_text)
        end_phrase_removed_content = re.sub(self.content_pattern, '', special_symbol_removed_content)
        blank_removed_content = re.sub(' +', ' ', end_phrase_removed_content).lstrip()  # 공백 에러 삭제
        reversed_content = ''.join(reversed(blank_removed_content))  # 기사 내용을 reverse 한다.
        content = ''
        for i in range(0, len(blank_removed_content)):
            # reverse 된 기사 내용중, ".다"로 끝나는 경우 기사 내용이 끝난 것이기 때문에 기사 내용이 끝난 후의 광고, 기자 등의 정보는 다 지움
            if reversed_content[i:i + 2] == '.다':
                content = ''.join(reversed(reversed_content[i:]))
                break
        return content

    def clear_headline(self, text):
        # 기사 제목에서 필요없는 특수문자들을 지움
        newline_symbol_removed_text = text.replace('\\n', '').replace('\\t', '')
        special_symbol_removed_headline = re.sub(self.special_symbol, '', newline_symbol_removed_text)
        return special_symbol_removed_headline

    def get_bs_obj(url):
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser")

        return bs_obj

    def find_news_totalpage(self, url):
        # 당일 기사 목록의 마지막 페이지 확인

        try:
            driver = webdriver.Chrome('chromedriver.exe_location')
            # waiting time for web data load
            #driver.implicitly_wait(10)
            driver.get(url)

            html = driver.page_source  # 페이지의 html 정보 load
            bs_obj = BeautifulSoup(html, 'html.parser')
            headline_tag = bs_obj.find('div', {'class': 'paginate'}).find('strong')

            regex = re.compile(r'<strong>(?P<num>\d+)')
            match = regex.findall(str(headline_tag))

            return int(match[0])

        except Exception:
            return 0
