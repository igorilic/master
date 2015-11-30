def get_page(url):
    try:
        if url == "http://neki.sajt.com":
            return '<some html code...>'
        elif url == "http://moze.i.ovaj.com":
            return '<some html code...> '
        
    except:
        return ""
    return ""

#za potrebe glavne funkcije promenjena je procedura unije
def union(p,q):
    for i in range(len(q[0])):
        if q[0][i] in p:
            del q[0][i]
    if q[0]:
        p.append(q)

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


def crawl_web(seed, max_depth):
    tocrawl = [[seed], 0]
    crawled = []
    while tocrawl:
        layer = tocrawl.pop()
        depth = layer[1]
        if depth <= max_depth:
            for url in layer[0]:
                if url not in crawled:
                    union(tocrawl, [get_all_links(get_page(url)), depth+1])
                    crawled.append(url)
    return crawled
        