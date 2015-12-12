import time


MAX_PAGES = 50  # maksimalan broj strana koji se ucitava


def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)


def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote


def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


# dodavanje svih reci sa stranice u index
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)


# dodavanje hiperveze u index
def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]


# funkcija trazenja
def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None


# crawl_web
def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = {}
    count = 0
    while tocrawl and count < MAX_PAGES:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            union(tocrawl, get_all_links(content))
            crawled.append(page)
            count += 1
    return index


# TEST
start = time.clock()  # pocetak testa
index = crawl_web('http://poincare.matf.bg.ac.rs/~vladaf/index_e.html')
# print(index)
vreme = time.clock() - start  # kraj testa
print("Vreme izvrsenja u testu hash tabele sa mapama: ")
print(vreme)
