class Level () :
    def __init__(self):
        self.header = []
        self.lvl = []

    def loadLevels(self):
        f = open("levels.txt","r")
        #every level will take 14 lines,
        #levelName, levleCreator, accomplanying song location, 10 lines of levelgrid and 1 empty to separate from next level
        #game ships with 3 inital levels
        #but game is adaptive to levels with grid that is less than 10 or more than 10 in height
        cn = -1
        for line in f:
            if len(line) > 1 :
                if line[1] == "#" :
                    cn += 1
                    self.header.append([line])
                    self.lvl.append([])
                elif line[0] == "#" :
                    self.header[cn].append(line)
                elif line[0] == '@' :
                    self.lvl[cn].append(line)

        f.close()
        return self.header, self.lvl