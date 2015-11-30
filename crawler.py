'''
@author: Igor Ilic
'''
max_pages = 100

'''
modul veb-pauka
uzima url
vraca index i graph, kao mape
'''
def crawl_web(seed): # vraca index, graph inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # hiperveza, [lista stranica na koje pokazuje]
    index = {} 
    count = 0
    while tocrawl and count<max_pages:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content) # linkovi ka
            graph[page]=outlinks #pravi se graph
            union(tocrawl, outlinks)
            crawled.append(page)
            count+=1
    return index, graph
# get_page uzima url i vraca html kod stranice
def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""
# get_next_target uzima kod stranice
# vraca prvu hipervezu na koju nailazi
# i poziciju u kodu stranice na kojoj prestaje url    
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote
# get_all_links uzima kod stranice
# vraca sve hiperveze u obliku liste
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
# pomocna funkcija, sluzi za pravljenje unije dve liste
def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)
# add_page_to_index uzima index(mapa), hipervezu
# i listu kljucnih reci iz koda stranice
# dodaje sve stranice i kljucne reci u index
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
# add_to_index dodaje par kljucna rec, hiperveza
# u indeks        
def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]
# lookup trazi kljucnu rec u indexu
# vraca hiperveze koje odgovaraju kljucnoj reci
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
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for unused in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            
            for node in graph:
                if page in graph[node]:
                    newrank += ranks[node]*d/len(graph[node])
            
            newranks[page] = newrank
        ranks = newranks
    return ranks
# sortira hiperveze po rangu koji imaju pocev od najpopularnije
def rank_list(ranks):
    return sorted(ranks, key=ranks.__getitem__, reverse=True)
'''
modul rezultata
uzima index, rang i kljucnu rec
vraca hipervezu koja odgovara kljucnoj reci i ima najveci rang
'''
def lucky_search(index, ranks, keyword):
    url_list = lookup(index, keyword)
    if url_list == None:
        return None
        
    key = ''
    maximum = 0
    for entry in url_list:
            if ranks[entry]>= maximum:
                maximum = ranks[entry]
                key=entry
    return key

'''
primer
'''    
index, graph = crawl_web('http://localhost/prva.html')
print(rank_list(compute_ranks(graph)))
