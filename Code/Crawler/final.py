# graph je dictionary
# url  : [ url, url, ... ]
# page   pages that link to target


max_pages = 5


def crawl_web(seed):  # vraca index, graph inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    count = 0
    while tocrawl and count < max_pages:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)  # linkovi ka
            graph[page] = outlinks  # pravi se graph
            union(tocrawl, outlinks)
            crawled.append(page)
            count += 1
    return index, graph


# cache = { 'http://neka_strana.com/index.html': <html>kod<html>}

def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""


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


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)


def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)


def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]


def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

'''
modul rangiranja
uzima graf
vraca mapu sa parovima: hiperveze i ranga
'''


def compute_ranks(graph):
    d = 0.8  # damping faktor
    numloops = 10
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for unused in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d)/npages

            for node in graph:
                if page in graph[node]:
                    newrank += ranks[node]*d/len(graph[node])

            newranks[page] = newrank
        ranks = newranks
    return ranks


def rank_list(ranks):
    return sorted(ranks, key=ranks.__getitem__, reverse=True)


'''
primer
'''
index, graph = crawl_web('http://poincare.matf.bg.ac.rs/~vladaf/index_e.html')
rang = compute_ranks(graph)
print(rang)
print(rank_list(rang))
