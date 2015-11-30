#Define a procedure, lookup,
#that takes two inputs:

#   - an index
#   - keyword

#The output should be a list
#of the urls associated
#with the keyword. If the keyword
#is not in the index, the output
#should be an empty list.

index = [['udacity', ['http://udacity.com', 'http://npr.org']], ['computing', ['http://acm.org']]]

#lookup(index,'udacity') => ['http://udacity.com','http://npr.org']


def lookup(index,keyword):
    lookup_list = []
    for entry in index:
        if entry[0]==keyword:
            for entry_url in entry[1]:
                lookup_list.append(entry_url)
    return lookup_list
