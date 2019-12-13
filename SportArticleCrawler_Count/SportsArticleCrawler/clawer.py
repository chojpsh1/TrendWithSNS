
from articlecrawler import ArticleCrawler
# 2019년 4월부터 2019년 4월까지 크롤링 시작
if __name__ == "__main__":
    Crawler = ArticleCrawler()
    Crawler.set_category("e스포츠")  # 뉴스 카테고리: 야구. 해외야구, 축구, 해외축구, 농구, 배구, 골프, 일반, e스포츠
    Crawler.set_date_range(2019, 6, 12, 2019, 6, 18)  # (시작 연도, 시작 월, 시작 일, 종료 연도, 종료 월, 종료 일)
    Crawler.start()
