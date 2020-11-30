import random
import glob


IN_FN = "input-versions/20-cluster.txt" #input-versions/50-cluster.txt"#proj-inputs/10.in"#input-versions/20v7.txt"#proj-inputs/10.in"#input-versions/20v7.txt"#10-sample.in"#20v7.txt"
OUT_FN = "proj-inputs/20.out"#"input-versions/20v7_out.txt"
IDEAL_ROOMS = []#[[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11], [12, 13], [14, 15], [16, 17], [18, 19]]#[[7, 2, 1], [5, 0, 9], [8, 6, 3, 4]]#[[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11], [12, 13], [14, 15], [16, 17], [18, 19]]#[]#[[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24], [25, 26, 27, 28, 29], [30, 31, 32, 33, 34], [35, 36, 37, 38, 39], [40, 41, 42, 43, 44], [45, 46, 47, 48, 49]]#[[6, 3, 4, 5], [1, 8, 7], [2, 14, 13, 12],  [18, 0, 19], [16, 17, 15], [11, 10, 9]]
#[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19]]#[]#
NUM_ITER = 500
TOP_RAND_SEL = 5
#7.245+7.522+7.532+7.026+7.093+7.56+6.922+7.353+7.094+7.063
class Room:
	def __init__(self, students, array, stress, happiness):
		self.students = students
		self.stress = stress
		self.happiness = happiness
		self.array = array
	def autofill(self):
		self.stress = self.happiness = 0
		for i in range(len(self.students)):
			for j in range(i+1, len(self.students)):
				self.stress += self.array[self.students[i]][self.students[j]][1]
				self.happiness += self.array[self.students[i]][self.students[j]][0]
	def getMergeValues(self, otherRoom): # Returns a room's stress and happiness if the two rooms merge
		totalHappiness = self.happiness + otherRoom.happiness
		totalStress = self.stress + otherRoom.stress
		for student in otherRoom.students:
			for selfStudent in self.students:
				totalHappiness += self.array[student][selfStudent][0]
				totalStress += self.array[student][selfStudent][1]
		return totalHappiness, totalStress
	def merge(self, otherRoom): # merges the two rooms
		self.happiness, self.stress = self.getMergeValues(otherRoom)
		self.students.extend(otherRoom.students)
	def studentValues(self, student):
		removeHappiness = 0
		removeStress = 0
		for other in self.students:
			removeHappiness += self.array[other][student][0]
			removeStress += self.array[other][student][1]
		return removeHappiness, removeStress
class Main:
	def __init__(self, fn): 
		self.array = []
		self.rooms = []
		self.ideal = IDEAL_ROOMS
		self.idealRooms = []
		self.n = 0
		self.totalStress = 0
		self.readFile(fn)

	def readFile(self, fn):
		f = open(fn, "r")
		self.n = int(next(f)) # read first line
		self.totalStress = float(next(f))
		self.array = [ [ [ 0 for i in range(2) ] for j in range(self.n) ] for k in range(self.n) ]
		for line in f: # read rest of lines
			i, j, happiness, stress = [float(x) for x in line.split()]
			i, j = int(i), int(j)
			self.array[i][j][0], self.array[j][i][0] = happiness, happiness
			self.array[i][j][1], self.array[j][i][1] = stress, stress
		f.close()
		self.idealRooms = []
		for students in self.ideal:
			room = Room(students, self.array, 0, 0)
			room.autofill()
			self.idealRooms.append(room)
		'''print("\nIdeal:")
		print('Num Rooms: ' + str(len(IDEAL_ROOMS)))
		print('Max Stress per room: ' + str(self.totalStress/len(IDEAL_ROOMS)))
		printRooms(self.idealRooms)#, toFile=True, fn=OUT_FN)'''
		
	def run(self):
		self.rooms = []
		for i in range(self.n):
			self.rooms.append(Room([i], self.array, 0, 0))
		while(True):
			'''maxHappinessAdded = 0
			maxAddedIndex = []
			maxMergedFromIndex = []'''
			maxHappiness = []
			for i in range(len(self.rooms)):
				for j in range(i+1, len(self.rooms)):
					mergeHappiness, mergeStress = self.rooms[i].getMergeValues(self.rooms[j])
					if mergeStress <= self.totalStress/(len(self.rooms) - 1):
						maxHappiness.append((i, j, mergeHappiness))
					'''if mergeHappiness > maxHappinessAdded and mergeStress <= self.totalStress/(len(self.rooms) - 1):
						maxHappinessAdded = mergeHappiness
						maxAddedIndex = [i]
						maxMergedFromIndex = [j]
					elif mergeHappiness == maxHappinessAdded:
						maxAddedIndex.append(i)
						maxMergedFromIndex.append(j)'''
			maxHappiness = sorted(maxHappiness, key=lambda x: -x[2])
			topHappinesses = []
			topMerges = []
			for merge in maxHappiness:
				if (len(topHappinesses) < TOP_RAND_SEL):
					if (merge[2] not in topHappinesses):
						topHappinesses.append(merge[2])
					topMerges.append(merge)
				else:
					break
			if (topMerges != []):
				randInd = random.randrange(len(topMerges))
				randMerge = topMerges[randInd]
				self.rooms[randMerge[0]].merge(self.rooms[randMerge[1]])
				self.rooms.remove(self.rooms[randMerge[1]])
			else:
				break

			'''if (maxAddedIndex != []):
				randInd = random.randrange(len(maxMergedFromIndex))
				self.rooms[maxAddedIndex[randInd]].merge(self.rooms[maxMergedFromIndex[randInd]])
				self.rooms.remove(self.rooms[maxMergedFromIndex[randInd]])
			else:
				break'''
			#printRooms(self.rooms)
		for x in range(200):
			random.shuffle(self.rooms)
			for room in self.rooms:
				random.shuffle(room.students)
				for student in room.students:
					maxGainRoom = room
					removeHappiness, removeStress = room.studentValues(student)
					maxGain, maxStress = removeHappiness, removeStress
					for toRoom in self.rooms:
						newHappiness, newStress = toRoom.studentValues(student)
						stressLimit = self.totalStress/(len(self.rooms) - (len(room.students) - 1 == 0))
						if toRoom.stress + newStress < stressLimit: # TODO adjust the denominator if we end up emptying a room
							if newHappiness > maxGain:
								maxGain = newHappiness
								maxStress = newStress
								maxGainRoom = toRoom
					if maxGainRoom is not room:
						room.students.remove(student)
						room.stress -= removeStress
						room.happiness -= removeHappiness
						if len(room.students) == 0:
							self.rooms.remove(room)
						maxGainRoom.students.append(student)
						maxGainRoom.stress += maxStress
						maxGainRoom.happiness += maxGain
		# while we can still merge groups
			# find the best pair of rooms to merge (based on either happiness added or happiness/stress added)
			# merge the pair of rooms --> update the total happiness, update the stress in the combined room as well
			# keep track of the best happiness so far

def printRooms(rooms, toFile=False, fn=""):
	print([("Room: " + str(room.students), "Happiness:" + str(room.happiness), "Stress: " + str(room.stress)) for room in rooms])
	print("Total Happiness: " + str(sum([room.happiness for room in rooms])))
	print([[(j, i) for j in rooms[i].students] for i in range(len(rooms))])
	if toFile:
		f = open(fn, "w")
		f.write("\n".join(["\n".join([str(j) + " " +  str(i) for j in rooms[i].students]) for i in range(len(rooms))]))
		f.close()


files = glob.glob("inputs/large/*.in")
print(files)
for file in files:
	maxHappiness = -1
	maxRooms = []
	main = Main(file)
	for i in range(NUM_ITER):
		
		main.run()
		if (sum([room.happiness for room in main.rooms]) > maxHappiness):
			maxHappiness = sum([room.happiness for room in main.rooms])
			maxRooms = main.rooms


	print("\n" + file)
	print("Greedy:")
	print('Num Rooms: ' + str(len(maxRooms)))
	print('Max Stress per room: ' + str(main.totalStress/len(maxRooms)))
	printRooms(maxRooms, toFile=True, fn=file.replace("in", "out").replace("inputs", "outputs"))
	'''if IDEAL_ROOMS is not []:
		print("\nIdeal:")
		print('Num Rooms: ' + str(len(IDEAL_ROOMS)))
		print('Max Stress per room: ' + str(main.totalStress/len(IDEAL_ROOMS)))
		printRooms(main.idealRooms)#ƒ, toFile=True, fn=OUT_FN)'''



