newDict = {}
with open('Places.txt','r') as lines:
	for i in lines:
		k=i.split(',')
		v=k[2].strip("\n")
		cord=[k[1],v]
		newDict[k[0]] = cord
print newDict
		
