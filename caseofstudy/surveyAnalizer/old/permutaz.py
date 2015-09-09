

maxElements = 10

roomList = []
roomListTokens = []

for setSize in range(0, maxElements):

	for i in range(0, maxElements):

		for iBody in range(i+setSize, maxElements):	

			currentSet = set()


			for iHead in range(i,i+setSize):
				currentSet.add(iHead)

			currentSet.add(iBody)

			token = "ID_" + str(list(currentSet))
			if token not in roomListTokens:
				roomList.append(currentSet)
				roomListTokens.append(token)


for room in roomList:
	print room
		