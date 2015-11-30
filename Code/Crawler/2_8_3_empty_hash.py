def make_hash_table(nbuckets):
    i = 0
    table = []
    while i < nbuckets:
        table.append([])
        i = i + 1
    return table

# pomocna funkcija: vraca koficu u kojoj je keyword
def hashtable_get_bucket(htable, keyword):
    return htable[hash_string(keyword, len(htable))]


# funkcija dodavanja u tabelu
def hashtable_add(htable, key, value):
    return hashtable_get_bucket(htable, key).append([key, value])


# funkcija trazenja
def hashtable_lookup(htable, key):
    bucket = hashtable_get_bucket(htable, key)
    for i in bucket:
        if i[0]==key:
            return i[1]
    return None