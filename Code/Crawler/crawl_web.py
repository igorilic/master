def crawl_web(seed):  # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)

            outlinks = get_all_links(content)
            graph[page] = outlinks # pravljenje grafa

            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph
