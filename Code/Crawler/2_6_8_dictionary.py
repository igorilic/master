def get_page(url):
    try:
        import urllib
        return urllib.open(url).read()
    except:
        return ""


def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_pages(page):
    while True:
        links = []
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

# sada ubacujemo i index
def add_to_index(index,keyword,url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword]=[url]

def add_page_to_index(index,url,content):
    for entry in content.split():
        add_to_index(index, entry, url)

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None


def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = {} #inicijalizacija dictionary-ja
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page) #get_page je "skupa" p-dura
            add_page_to_index(index, page, content) # pravi se index
            union(tocrawl, get_all_links(content))
            crawled.append(page)
    return crawled

