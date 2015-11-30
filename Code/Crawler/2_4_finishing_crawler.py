def get_page(url):
    try:
        if url == "http://neki.sajt.com":
            return '<some html code...>'
        elif url == "http://moze.i.ovaj.com":
            return '<some html code...> '
    except:
        return ""
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


def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            union(tocrawl, get_all_links(get_page(page)))
            crawled.append(page)
    return crawled
        