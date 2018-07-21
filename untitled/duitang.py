import requests
import urllib.parse
import threading

# 设置最大线程数
threading_lock = threading.BoundedSemaphore(value=3)

def get_page(url):
    page =  requests.get(url)
    content = page.content
    utf8content = content.decode("utf-8")
    return utf8content


def pages_from_duitang(keyword):
    pages = []
    url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={}&type=feed&include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Clike_id%2Csender%2Calbum%2Creply_count%2Cfavorite_blog_id&_type=&start={}&_=1532173302983&limit=100'
    label = urllib.parse.quote(keyword)
    for index in range(0, 300, 100):
        u = url.format(label, index)
        print(u)
        page = get_page(u)
        pages.append(page)
    return pages


def findall_in_page(page, startpart, endpart):
    all_strings = []
    end = 0
    while page.find(startpart, end) != -1:
        start = page.find(startpart, end) + len(startpart)
        end = page.find(endpart, start)
        string = page[start: end]
        print(string)
        all_strings.append(string)
    return all_strings


def pic_urls_from_pages(pages):
    pic_urls = []
    for page in pages:
        urls = findall_in_page(page, 'path":"', '"')
        pic_urls.extend(urls)
    return pic_urls


def download_pics(url, n):
    r = requests.get(url)
    path = 'pics/' + str(n) + '.jpg'
    with open(path, 'wb') as f:
        f.write(r.content)
    # 释放锁
    threading_lock.release()


def duitang_main(keyword):
    pages = pages_from_duitang(keyword)
    pic_urls = pic_urls_from_pages(pages)
    n = 0
    for url in pic_urls:
        n += 1
        print("正在下载第 {} 张图片".format(n))
        if n > 10:
            break
        else:
            # 申请锁
            threading_lock.acquire()
            t = threading.Thread(target=download_pics, args=(url, n))
            # 开始执行线程
            t.start()


def run():
    duitang_main("校花")


if __name__ == "__main__":
    run()