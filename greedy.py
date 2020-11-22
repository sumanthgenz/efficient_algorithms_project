import random


IN_FN = "input-versions/20v7.txt"
OUT_FN = "input-versions/20v7_out.txt"
IDEAL_ROOMS = [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11], [12, 13], [14, 15], [16, 17], [18, 19]]
NUM_ITER = 1000

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
		
	def run(self):
		for i in range(self.n):
			self.rooms.append(Room([i], self.array, 0, 0))
		while(True):
			maxHappinessAdded = 0
			maxAddedIndex = []
			maxMergedFromIndex = []
			for i in range(len(self.rooms)):
				for j in range(i+1, len(self.rooms)):
					mergeHappiness, mergeStress = self.rooms[i].getMergeValues(self.rooms[j])
					if mergeHappiness > maxHappinessAdded and mergeStress <= self.totalStress/(len(self.rooms) - 1):
						maxHappinessAdded = mergeHappiness
						maxAddedIndex = [i]
						maxMergedFromIndex = [j]
					elif mergeHappiness == maxHappinessAdded:
						maxAddedIndex.append(i)
						maxMergedFromIndex.append(j)
			if (maxAddedIndex != []):
				randInd = random.randrange(len(maxMergedFromIndex))
				self.rooms[maxAddedIndex[randInd]].merge(self.rooms[maxMergedFromIndex[randInd]])
				self.rooms.remove(self.rooms[maxMergedFromIndex[randInd]])
			else:
				break
			
		# while we can still merge groups
			# find the best pair of rooms to merge (based on either happiness added or happiness/stress added)
			# merge the pair of rooms --> update the total happiness, update the stress in the combined room as well
			# keep track of the best happiness so far

def printRooms(rooms, toFile=False, fn=""):
	print([("Room: " + str(room.students), "Happiness:" + str(room.happiness), "Stress: " + str(room.stress)) for room in rooms])
	print("Total Happiness: " + str(sum([room.happiness for room in rooms])))
	print([[(j, i) for j in maxRooms[i].students] for i in range(len(rooms))])
	if toFile:
		f = open(fn, "w")
		f.write("\n".join(["\n".join([str(j) + " " +  str(i) for j in maxRooms[i].students]) for i in range(len(rooms))]))
		f.close()

maxHappiness = -1
maxRooms = []
for i in range(NUM_ITER):
	main = Main(IN_FN)
	main.run()
	if (sum([room.happiness for room in main.rooms]) > maxHappiness):
		maxHappiness = sum([room.happiness for room in main.rooms])
		maxRooms = main.rooms


print("Greedy:")
printRooms(maxRooms)
print("\nIdeal:")
printRooms(main.idealRooms, toFile=False)#, fn=OUT_FN)



