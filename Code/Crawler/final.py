"""
Veb-pauk koji vrsi prikupljanje URL-ova i kljucnih reci za zeljeni broj veb
strana.
Kako bi se generisala dokumentacija koristite komandu:
    pydoc -w crawler
"""


"""Broj stranica koje ce obici veb-pauk."""
MAX_PAGES = 10


def crawl_web(seed):
    """Veb pauk - seed: URL pocetne stranice. Vraca index i graph"""
    tocrawl = [seed]
    crawled = []
    graph = {}
    index = {}
    count = 0
    while tocrawl and count < MAX_PAGES:
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


def get_page(url):
    """Funkcija get_page - url: URL koji se ucitava. Vraca HTML kod stranice"""
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""


def get_next_target(page):
    """Funkcija get_next_target - page: HTML kod stranice
    Vraca URL i polozaj krajnjeg navodnika u linku
    """
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote


def get_all_links(page):
    """Funkcija get_all_links - HTML kod stranice
    Vraca listu svih URL-ova sa stranice
    """
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
    """Funkcija union uzima dve liste i vraca njihovu uniju."""
    for e in b:
        if e not in a:
            a.append(e)


def add_page_to_index(index, url, content):
    """
    Funkcija add_page_to_index

    index: Mapa u koju se prikupljaju podaci
    url: URL stranice sa koje se skuplja sadrzaj
    content: Niska koja predstavlja sadrzaj stranice
    Ne vraca nista
    """
    words = content.split()
    for word in words:
        add_to_index(index, word, url)


def add_to_index(index, keyword, url):
    """Funkcija add_to_index
    index: Mapa u koju se prikupljaju podaci
    keyword: Niska koja predstavlja rec koja se dodaje u index
    url: URL na kojoj je nadjen keyword
    Ne vraca nista
    """
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]


def lookup(index, keyword):
    """Funkcija lookup
    index: Mapa u koju se prikupljaju podaci
    keyword: rec koja se trazi u indexu
    Vraca sve URL koji odgovaraju keyword-u
    """
    if keyword in index:
        return index[keyword]
    else:
        return None


def compute_ranks(graph):
    """
    Funkcija compute_ranks
    graph: Mapa u kojoj se nalaze veze izmedju stranica
    Vraca mapu u kojoj su dati rangovi stranica
    """
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
    """Funkcija rank_list - ranks: Mapa u kojoj su dati rangovi stranica
    Vraca listu URL-ova iz mape ranks, sortiranih po rangu
    """
    return sorted(ranks, key=ranks.__getitem__, reverse=True)


"""
Primer koji daje rezultate rangiranja stranica u odnosu na pocetnu
"""
index, graph = crawl_web('http://poincare.matf.bg.ac.rs/~vladaf/index_e.html')
rang = compute_ranks(graph)
print(graph)
print(rang)
print(rank_list(rang))
