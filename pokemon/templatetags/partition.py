from django import template

register = template.Library()

@register.filter
def partition(theList, n):
	try:
		n = int(n)
		thelist = list(theList)
	except(ValueError, TypeError):
		return [theList]

	list_len = len(thelist)
	split = list_len // n

	if list_len % n!= 0:
		split += 1

	return [thelist[split*i:split*(i+1)] for i in range(n)]

@register.filter
def partition_horizontal(thelist, n):
    try:
        n = int(n)
        thelist = list(thelist)
    except (ValueError, TypeError):
        return [thelist]
    newlists = [list() for i in range(n)]
    for i, val in enumerate(thelist):
        newlists[i%n].append(val)
    return newlists