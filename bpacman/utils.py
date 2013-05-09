
def is_in(lst, e, comp=None):
	if comp:
		for x in lst:
			if(comp(x,e)):
				return True;
	else:
		for x in lst:
			if x == e:
				return True;
	return False;
