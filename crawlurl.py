# -*- coding: utf-8 -*-
# author:Safi
# 根据数据库url爬取html页面相关内容

from selenium import webdriver
from bs4 import BeautifulSoup
import MySQLdb
import time
import os
from urllib import request


def get_href_by_url(url):
    """
    京东sku
    :return:
    """
    driver = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe', port=0,
                                 desired_capabilities={'browserName': 'chrome', 'platform': 'windows',
                                                       'javascriptEnabled': True, 'version': ''}, service_args=None,
                                 service_log_path=None)
    try:
        driver.get(url)
        file_path = '{}{}{}'.format(os.getcwd(), os.sep, os.path.basename(url).split('.')[0])
        print(file_path)

        js = "document.body.scrollTop+=100"
        height = driver.execute_script("return document.body.scrollHeight")
        count = int(height / 100)
        for i in range(0, count):
            driver.implicitly_wait(30)
            time.sleep(1)
            driver.execute_script(js)

        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')

        img_arr = soup.select("[id=J-detail-content] img")
        for img in img_arr:
            if img.get('src'):
                img_src = img.get('src')
                file_suffix = os.path.splitext(img_src)[1]
                print(img.get('src'))
                if file_suffix.lower() != '.jpg':
                    if img.has_attr('data-lazyload'):
                        img_src = img.attrs['data-lazyload']
                if 'https' in img_src or 'http' in img_src:
                    img_src = img_src
                else:
                    img_src = 'https:' + img_src
            file_name = os.path.basename(img_src)
            save_img(img_src, file_name, file_path)

    except Exception as e:
        print(e)


def save_img(img_url, file_name, file_path):
    """
    保存图片到磁盘文件夹
    :param img_url: 原图url
    :param file_name: 图片名
    :param file_path: 保存目录
    :return:
    """
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        filename = '{}{}{}'.format(file_path, os.sep, file_name)
        request.urlretrieve(img_url, filename)

    except IOError as e:
        print('文件操作失败', e)
    except Exception as e:
        print('错误 ：', e)


def get_href_by_url():
    """
    根据数据库url抓取
    :return:
    """
    driver = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    try:
        db = MySQLdb.connect(host="192.168.1.244", user="ypgbbc", passwd="ypgbbc", db="bbc_v2", port=3309)

        cursor = db.cursor()
        select_sql = 'SELECT * from s_crawler where status =\'%d\'' % 10
        try:
            cursor.execute(select_sql)
            result = cursor.fetchall()
        except Exception as e:
            result = ''
            print(e.message)
        if result:
            for row in result:
                driver.get(row[3])

                js = "document.body.scrollTop+=100"
                height = driver.execute_script("return document.body.scrollHeight")
                count = int(height / 100)
                for i in range(0, count):
                    driver.implicitly_wait(30)
                    time.sleep(1)
                    driver.execute_script(js)

                html = driver.page_source
                driver.save_screenshot('1.png')
                driver.quit()
                soup = BeautifulSoup(html, 'html.parser')
                tm_price = soup.select("[id=J_PromoPrice] [class=tm-price]")
                crawl_price = 0
                if tm_price:
                    crawl_price = tm_price[0].text

                img_urls = []
                for img in soup.select("[id=description] img"):
                    if img.get('src'):
                        img_urls.append(img.get('src'))

                strs_img_urls = ';'.join(img_urls)
                img_gallery = []
                for img in soup.select("[id=J_UlThumb] img"):
                    if img.get('src'):
                        img_gallery.append(img.get('src'))
                strs_img_gallerys = ';'.join(img_gallery)

                update_sql = 'UPDATE s_crawler SET img_url = \'%s\',crawl_price = \'%s\',img_gallery = \'%s\', ' \
                             'status= 20 where crawl_url = \'%s\' ' % (strs_img_urls, crawl_price, strs_img_gallerys,
                                                                       row[3])
                try:
                    cursor.execute(update_sql)
                    db.commit()
                except Exception as e:
                    db.rollback()
                    print(u'更新失败')
                    print(e.message)

            db.close()
        else:
            print(u'没有可抓取的数据')
    except Exception as e:
        print(u'内部错误')
        print(e.message)
        get_href_by_url()


if __name__ == '__main__':
    get_href_by_url("https://item.jd.hk/2289449.html")
    get_href_by_url("https://item.jd.hk/2355514.html")
    get_href_by_url("https://item.jd.hk/2289451.html")
    get_href_by_url("https://item.jd.hk/2622752.html")
    get_href_by_url("http://item.jd.hk/1938922.html")
    get_href_by_url("https://item.jd.hk/2366129.html")
    get_href_by_url("https://item.jd.hk/1926187.html")
    get_href_by_url("https://item.jd.hk/2366119.html")
    get_href_by_url("https://item.jd.hk/2356463.html")
    get_href_by_url("https://item.jd.hk/2123768.html")
    get_href_by_url("http://item.jd.hk/2356469.html")

    get_href_by_url("https://item.jd.hk/2451575.html")
    get_href_by_url("http://item.jd.hk/2481303.html")
    get_href_by_url("https://item.jd.hk/2288508.html")
    get_href_by_url("https://item.jd.hk/1938923.html")
    get_href_by_url("http://item.jd.hk/2289457.html")
    get_href_by_url("https://item.jd.hk/2288506.html")
    get_href_by_url("https://item.jd.hk/2608225.html")
    get_href_by_url("https://item.jd.hk/2622474.html")
    get_href_by_url("http://item.jd.hk/2656316.html")
    get_href_by_url("https://item.jd.hk/2356461.html")
    get_href_by_url("http://item.jd.hk/2365174.html")
    get_href_by_url("http://item.jd.hk/2365264.html")
    get_href_by_url("https://item.jd.hk/2365252.html")
    get_href_by_url("https://item.jd.hk/2356465.html")
    get_href_by_url("https://item.jd.hk/2365188.html")
    get_href_by_url("https://item.jd.hk/3516276.html")
    get_href_by_url("https://item.jd.hk/3516222.html")
    get_href_by_url("http://item.jd.hk/3572010.html")
    get_href_by_url("https://item.jd.hk/3572036.html")
    get_href_by_url("https://item.jd.hk/3562384.html")
    get_href_by_url("https://item.jd.hk/4279152.html")
    get_href_by_url("https://item.jd.hk/3705503.html")
    get_href_by_url("https://item.jd.hk/3705549.html")
    get_href_by_url("http://item.jd.hk/4279176.html")
    get_href_by_url("https://item.jd.hk/3791179.html")
    get_href_by_url("https://item.jd.hk/4279190.html")
    get_href_by_url("https://item.jd.hk/4484113.html")
    get_href_by_url("https://item.jd.hk/4484111.html")
    get_href_by_url("https://item.jd.hk/4732245.html")
