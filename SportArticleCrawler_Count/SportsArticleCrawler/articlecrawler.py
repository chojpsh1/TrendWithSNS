#!/usr/bin/env python
# -*- coding: utf-8, euc-kr -*-

from time import sleep
from bs4 import BeautifulSoup
from multiprocessing import Process
from exceptions import *
from articleparser import ArticleParser
import os
import platform
import calendar
import requests
import csv
import re

from selenium import webdriver

dataset_location = 'data_location'
class ArticleCrawler(object):
    def __init__(self):
        self.parser = ArticleParser()
        self.categories = {'야구': "kbaseball", '해외야구': "wbaseball",'축구':"kfootball", '해외축구':"wfootball",
                           '농구': "basketball", '배구':"volleyball",'골프':"golf",'일반':"general", 'e스포츠':"esports"}

        self.selected_categories = []
        self.date = {'start_year': 0, 'start_month': 0, 'start_day': 0, 'end_year': 0, 'end_month': 0, 'end_day': 0}
        self.user_operating_system = str(platform.system())

    def set_category(self, *args):
        for key in args:
            if self.categories.get(key) is None:
                raise InvalidCategory(key)
        self.selected_categories = args

    def set_date_range(self, start_year, start_month, start_day, end_year, end_month, end_day):
        args = [start_year, start_month, start_day, end_year, end_month, end_day]

        if start_year > end_year:
            raise InvalidYear(start_year, end_year)

        if start_month < 1 or start_month > 12:
            raise InvalidMonth(start_month)
        if end_month < 1 or end_month > 12:
            raise InvalidMonth(end_month)

        if start_day < 1 or start_day > calendar.monthrange(start_year, start_month)[1]:
            raise InvalidDay(start_day)
        if end_day < 1 or end_day > calendar.monthrange(start_year, start_month)[1]:
            raise InvalidDay(end_day)

        for key, date in zip(self.date, args):
            self.date[key] = date
        print(self.date)

    def make_news_page_url(self, category_url, start_year, end_year, start_month, end_month, start_day, end_day):
        total_url_list = []
        for year in range(start_year, end_year + 1):
            if start_year == end_year:
                year_start_month = start_month
                year_end_month = end_month
            else:
                if year == start_year:
                    year_start_month = start_month
                    year_end_month = 12
                elif year == end_year:
                    year_start_month = 1
                    year_end_month = end_month
                else:
                    year_start_month = 1
                    year_end_month = 12

            for month in range(year_start_month, year_end_month + 1):
                if year_start_month == year_end_month:
                    start_day_tmp = start_day
                    end_day_tmp = end_day
                else:
                    if month == year_start_month:
                        start_day_tmp = start_day
                        end_day_tmp = calendar.monthrange(year, month)[1]
                    elif month == year_end_month:
                        start_day_tmp = 1
                        end_day_tmp = end_month
                    else:
                        start_day_tmp = 1
                        end_day_tmp = calendar.monthrange(year, month)[1]

                for month_day in range(start_day_tmp, end_day_tmp + 1):
                    if len(str(month)) == 1:
                        month = "0" + str(month)
                    if len(str(month_day)) == 1:
                        month_day = "0" + str(month_day)

                    # page 날짜 정보만 있고 page 정보가 없는 url 저장
                    url = category_url + str(year) + str(month) + str(month_day)


                    # totalpage는 네이버 페이지 구조를 이용해서 page=10000으로 지정해 totalpage를 알아냄
                    # page=10000을 입력할 경우 페이지가 존재하지 않기 때문에 기사 리스트의 가장 마지막 페이지 (page=totalpage)로 이동 됨
                    totalpage = 0
                    totalpage = self.parser.find_news_totalpage(url + "&page=10000")

                    for page in range(1, totalpage + 1):
                        if totalpage:
                            total_url_list.append(url + "&page=" + str(page))

        # 월, 일의 자릿수를 2자리로 맞추기
        print_start_month = self.appendI2S(start_month)
        print_end_month = self.appendI2S(end_month)

        print_start_day = self.appendI2S(start_day)
        print_end_day = self.appendI2S(end_day)

        print('Crawling date range: ' + str(start_year) + str(print_start_month) + str(print_start_day) +
              '~' + str(end_year) + str(print_end_month) + str(print_end_day))
        return total_url_list

    def crawling(self, category_name):
        # MultiThread PID
        print(category_name + " PID: " + str(os.getpid()))    
        
        # csv 파일 이름에 들어갈 month 자릿수 맞추기
        save_start_month = self.appendI2S(self.date['start_month'])
        save_end_month = self.appendI2S(self.date['end_month'])
        save_start_day = self.appendI2S(self.date['start_day'])
        save_end_day = self.appendI2S(self.date['end_day'])

        
        # 각 카테고리 기사 저장 할 CSV
        # Windows use euc-kr
        file = open(
            dataset_location + 'Article_' + category_name + '_' + str(self.date['start_year']) + save_start_month
            + save_start_day + '_' + str(self.date['end_year']) + save_end_month + save_end_day
            + '.csv', 'w', encoding='euc-kr', newline='')

        wcsv = csv.writer(file)
        del save_start_month, save_end_month

        # 기사 리스트 URL 형식
        url = "https://sports.news.naver.com/" + str(self.categories.get(category_name)) +"/news/index.nhn?isphoto=N&date="
        print(url)
        # start_year년 start_month월 ~ end_year의 end_month 날짜까지 기사를 수집
        #url_list = self.make_news_page_url(url, self.date['start_year'], self.date['end_year'], self.date['start_month'], self.date['end_month'])
        url_list = self.make_news_page_url(url, self.date['start_year'], self.date['end_year'],
                                                self.date['start_month'], self.date['end_month'],
                                                self.date['start_day'], self.date['end_day'])

        print(category_name + " Urls are generated")
        print("The crawler starts")
        print("=========================================")
        article_count = 0

        for URL in url_list:
            regex = re.compile("date=(\d+)")
            news_date = regex.findall(URL)[0]

            driver = webdriver.Chrome('chromedriver.exe_location')

            driver.get(URL)

            html = driver.page_source  # 페이지의 html 정보 load
            bs_obj = BeautifulSoup(html, 'html.parser')

            # html의 class를 이용하여 각 페이지에 있는 기사들 가져오기
            article_url_list = bs_obj.select('.news_list .text')

            # 각 페이지에 있는 기사들의 url 저장
            post_url_list = []
            for line in article_url_list:
                post_url_list.append("https://sports.news.naver.com"+line.a.get('href')) # 해당되는 page에서 모든 기사들의 URL을 post 리스트에 넣음
            del article_url_list

            for content_url in post_url_list:  # 기사 URL
                # 크롤링 대기 시간
                sleep(0.01)
                # 기사 HTML 가져옴
                request_content = requests.get(content_url)
                document_content = BeautifulSoup(request_content.content, 'html.parser')

                try:

                    # 기사 제목 가져옴
                    tag_headline = document_content.find_all('h4', {'class': 'title'})
                    text_headline = ''  # 뉴스 기사 제목 초기화
                    text_headline = text_headline + self.parser.clear_headline(str(tag_headline[0].find_all(text=True)))
                    if not text_headline:  # 공백일 경우 기사 제외 처리
                        continue

                    # 기사 제목 가져옴
                    tag_time = document_content.find('div', {'class': 'info'}).find('span')

                    regex = re.compile("오[전,후]\s\d\d:\d\d")
                    match = regex.findall(str(tag_time))[0]

                    text_time = ''  # 뉴스 기사 제목 초기화
                    text_time = text_time + match

                    if not text_time:  # 공백일 경우 기사 제외 처리
                        exit()

                    # 기사 본문 가져옴
                    tag_content = document_content.find_all('div', {'id': 'newsEndContents'})
                    text_sentence = ''  # 뉴스 기사 본문 초기화
                    text_sentence = text_sentence + self.parser.clear_content(str(tag_content[0].find_all(text=True)))
                    if not text_sentence:  # 공백일 경우 기사 제외 처리
                        continue

                    # CSV 작성
                    wcsv.writerow([news_date, text_time, text_headline, text_sentence, content_url])
                    article_count = article_count+1

                    del text_sentence, text_headline, text_time
                    del tag_content, tag_headline
                    del request_content, document_content


                except Exception as ex:  # UnicodeEncodeError ..
                    # wcsv.writerow([ex, content_url])
                    del request_content, document_content
                    pass

        print("The crawler finished!!")
        print("Number of crawling articles : "+str(article_count))
        file.close()

    def appendI2S(self, input_int):
        if len(str(input_int)) == 1:
            out_string = "0" + str(input_int)
        else:
            out_string = str(input_int)
        return out_string

    def start(self):
        # MultiProcess 크롤링 시작
        for category_name in self.selected_categories:
            proc = Process(target=self.crawling, args=(category_name,))
            proc.start()