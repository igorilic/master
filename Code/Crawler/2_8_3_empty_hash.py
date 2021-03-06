NUMBER_OF_BUCKETS = 10  # number of buckets in index list
MAX_PAGES = 5  # number of pages to crawl


def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""


def union(p, q):
    for e in q:
        if e not in p:
            p.append(e)


def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
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


def make_hash_table(nbuckets):
    i = 0
    table = []
    while i < nbuckets:
        table.append([])
        i = i + 1
    return table


def hash_string(keyword, buckets):
    h = 0
    for c in keyword:
        h = (h + ord(c)) % buckets
    return h


# pomocna funkcija: vraca koficu u kojoj je keyword
def hashtable_get_bucket(htable, keyword):
    return htable[hash_string(keyword, len(htable))]


# funkcija dodavanja u tabelu
def hashtable_add(htable, key, value):
    bucket = hashtable_get_bucket(htable, key)
    for entry in bucket:
        if entry[0] == key:
            entry[1].append(value)
            return
    bucket.append([key, [value]])


# funkcija trazenja
def hashtable_lookup(htable, key):
    bucket = hashtable_get_bucket(htable, key)
    for i in bucket:
        if i[0] == key:
            return i[1]
    return None


# funkcija update-a
def hashtable_update(htable, key, value):
    bucket = hashtable_get_bucket(htable, key)
    for i in bucket:
        if i[0] == key:
            i[1] = value
            return
    bucket.append([key, value])


def add_page_to_index(htable, page, content):
    for entry in content.split():
        hashtable_add(htable, entry, page)


# crawl_web
def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = make_hash_table(NUMBER_OF_BUCKETS)
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
index = crawl_web('http://poincare.matf.bg.ac.rs/~vladaf/index_e.html')
print(index)
