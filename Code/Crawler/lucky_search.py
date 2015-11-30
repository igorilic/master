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