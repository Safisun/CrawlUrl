# -*- coding: utf-8 -*-
# author:Safi
# 根据数据库表中或者url爬取html页面相关内容

from selenium import webdriver
from bs4 import BeautifulSoup
import MySQLdb
import time
import os
from urllib import request


def get_img_by_jd_url(url):
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
        main_img_arr = soup.select('[id=spec-list] img')
        main_path = '{}{}{}'.format(file_path, os.sep, 'main')
        for main_img in main_img_arr:
            if main_img.get('src'):
                m_img_src = main_img.get('src').replace('75x75', '450x450')
                if 'https' in m_img_src or 'http' in m_img_src:
                    m_img_src = m_img_src
                else:
                    m_img_src = 'https:' + m_img_src
                file_name = os.path.basename(m_img_src)
                save_img(m_img_src, file_name, main_path)
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


def get_img_by_kaola_url(sku, url):
    """
    考拉sku
    :return:
    """
    driver = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe', port=0,
                                 desired_capabilities={'browserName': 'chrome', 'platform': 'windows',
                                                       'javascriptEnabled': True, 'version': ''}, service_args=None,
                                 service_log_path=None)
    try:
        driver.get(url)

        js = "document.body.scrollTop+=100"
        height = driver.execute_script("return document.body.scrollHeight")
        print(height)
        count = int(height / 100)
        for i in range(0, count):
            driver.implicitly_wait(10)
            time.sleep(1)
            driver.execute_script(js)

        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')
        file_path = '{}{}{}'.format(os.getcwd(), os.sep, sku)
        print(file_path)

        main_img_arr = soup.select('[id=litimgUl] img')
        main_path = '{}{}{}'.format(file_path, os.sep, 'main')
        for index, main_img in enumerate(main_img_arr):
            if main_img.get('src'):
                m_img_src = main_img.get('src').replace('64x0', '800x0')
                file_suffix = os.path.splitext(m_img_src)[1].split('?')[0]
                if 'https' in m_img_src or 'http' in m_img_src:
                    m_img_src = m_img_src
                else:
                    m_img_src = 'https:' + m_img_src
                file_name = "{}{}".format(index + 1, file_suffix)
                save_img(m_img_src, file_name, main_path)
        img_arr = soup.select("[id=textareabox] img")
        for index, img in enumerate(img_arr):
            if img.get('src'):
                img_src = img.get('src')
                file_suffix = os.path.splitext(img_src)[1].split('?')[0]
                if 'https' in img_src or 'http' in img_src:
                    img_src = img_src
                else:
                    img_src = 'https:' + img_src
            file_name = "{}{}".format(index + 1, file_suffix).split('?')[0]
            save_img(img_src, file_name, file_path)

    except Exception as e:
        print(e)


def get_img_by_tmall_url(sku, url):
    """
    天猫sku
    :return:
    """
    driver = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe', port=0,
                                 desired_capabilities={'browserName': 'chrome', 'platform': 'windows',
                                                       'javascriptEnabled': True, 'version': ''}, service_args=None,
                                 service_log_path=None)
    try:
        driver.get(url)
        js = "document.body.scrollTop+=100"
        height = driver.execute_script("return document.body.scrollHeight")
        print(height)
        count = int(height / 100)
        for i in range(0, count):
            driver.implicitly_wait(10)
            time.sleep(1)
            driver.execute_script(js)

        html = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html, 'html.parser')
        file_path = '{}{}{}'.format(os.getcwd(), os.sep, sku)
        print(file_path)
        main_path = '{}{}{}'.format(file_path, os.sep, 'main')
        main_img_arr = soup.select('[id=J_UlThumb] img')
        print(len(main_img_arr))
        for index, img in enumerate(main_img_arr):
            if img.get('src'):
                img_src = img.get('src').replace('60x60', '430x430')
                file_suffix = os.path.splitext(img_src)[1]
                if 'https' in img_src or 'http' in img_src:
                    img_src = img_src
                else:
                    img_src = 'https:' + img_src
            file_name = "{}{}".format(index + 1, file_suffix).split('?')[0]
            save_img(img_src, file_name, main_path)
        img_arr = soup.select("[id=description] img")
        print(len(img_arr))
        for index, img in enumerate(img_arr):
            if img.get('src'):
                img_src = img.get('src')
                file_suffix = os.path.splitext(img_src)[1]
                if 'https' in img_src or 'http' in img_src:
                    img_src = img_src
                else:
                    img_src = 'https:' + img_src
            file_name = "{}{}".format(index + 1, file_suffix).split('?')[0]
            save_img(img_src, file_name, file_path)
        print(u'结束')
    except Exception as e:
        print(u'内部错误')
        print(e.message)


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
    get_img_by_tmall_url('5111804',
                         'https://detail.tmall.hk/hk/item.htm?spm=a1z10.5-b-s.w4011-17375697126.40.RVMYJo&id=560736321825&rn=20c384ef585885c70ba34e410ec27360&abbucket=13')
    get_img_by_tmall_url('5111805',
                         'https://detail.tmall.hk/hk/item.htm?spm=a1z10.5-b-s.w4011-17375697126.34.RVMYJo&id=559769233971&rn=20c384ef585885c70ba34e410ec27360&abbucket=13&sm=true&smToken=ea01b523938148f6942b24ab2f7b6937&smSign=zU1m1i%20ywn7r5nREhWwnUA==')
