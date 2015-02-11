#gwise

#The 'contains' functions are taken from 
#http://www.cs.cmu.edu/~112/notes/SmileyClassAnimationDemo.py

from Tkinter import *
import sys
import time
import random
import copy
from PIL import Image, ImageTk


#Taken Directly from 
#http://www.cs.cmu.edu/~112/notes/eventBasedAnimationClass.py
class EventBasedAnimationClass(object): 
    #http://www.cs.cmu.edu/~112/notes/eventBasedAnimationClass.py
    #EventBasedAnimationClass Taken directly from course notes
    def __init__(self, width=300, height=300):
        self.width = width
        self.height = height
        self.timerDelay = 20 # in milliseconds (set to None to turn off timer)

    def onMousePressedWrapper(self, event):
        if (not self._isRunning): return
        self.onMousePressed(event)
        self.redrawAll()

    def onKeyPressedWrapper(self, event):
        if (not self._isRunning): return
        self.onKeyPressed(event)
        self.redrawAll()

    def onTimerFiredWrapper(self):
        if (not self._isRunning): self.root.destroy(); return
        if (self.timerDelay == None): return # turns off timer
        self.onTimerFired()
        self.redrawAll()
        self.canvas.after(self.timerDelay, self.onTimerFiredWrapper)         

    def quit(self):
        if (not self._isRunning): return
        self._isRunning = False
        if (self.runningInIDLE):
            # in IDLE, must be sure to destroy here and now
            self.root.destroy()
        else:
            # not IDLE, then we'll destroy in the canvas.after handler
            self.root.quit()

    def run(self,root=None):
        # create the root and the canvas
        if root == None: #Help from my mentor, Joel Choo
            self.root = Tk()
        else:
            self.root = root
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.initAnimation()
        # set up events
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.quit())
        self._isRunning = True
        self.runningInIDLE =  ("idlelib" in sys.modules)
        # DK: You can use a local function with a closure
        # to store the canvas binding, like this:
        def f(event): self.onMousePressedWrapper(event)    
        self.root.bind("<Button-1>", f)
        # DK: Or you can just use an anonymous lamdba function, like this:
        self.root.bind("<Key>", lambda event: self.onKeyPressedWrapper(event))
        self.onTimerFiredWrapper()
        # and launch the app (This call BLOCKS, so your program waits
        # until you close the window!)
        self.root.mainloop()

class TermProject(EventBasedAnimationClass):
    def __init__(self):
        rows = 11
        cols = 17
        margin = 80
        sideMargin = 250
        cellSize = 40
        canvasWidth = 2*sideMargin + cols*cellSize
        canvasHeight = 2*margin + rows*cellSize
        self.width = canvasWidth
        self.height = canvasHeight
        self.rows = rows
        self.cols = cols
        self.margin = margin
        self.sideMargin = sideMargin
        self.cellSize = cellSize
        super(TermProject, self).__init__(canvasWidth, canvasHeight)
        self.inHelpScreen = False

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.drawBackground()
        if not self.inHelpScreen:
            self.canvas.create_text(self.width/2, self.margin, 
            text = "Zombie Defense",font = "Helvetica 95 bold",fill = "red")
            self.drawLevelBox1()
            self.drawLevelBox2()
            self.drawLevelBox3()
            self.drawLevelBox4()
            self.drawHelpBox()
        elif self.inHelpScreen:
            self.drawHelpBackground()
            self.drawBackButton()
            self.drawHelpText()

    def drawHelpText(self):
        text = """Instructions:

Welcome to Zombie Defense!

Object of the game is to defend your country, as the zombies move right
you need to place the appropriate towers on the map in a strategic way,
in order to kill all zombies the come through your territory. If a zombie gets
through your map without being killed, you lose a life. If you lose 50 lives,
the game, and the world, is over. Choose your tower on the right side, but 
make sure you have enough cash and manage your money wisely.
You can upgrade your tower by selecting it and clicking the upgrade buttons
on the left. You can upgrade the tower distance and firing speed, the distance
is represented by the circle around the weapon, the sniper his unlimited range.
Grenade is to be placed on the path, and it fires 3 seconds after placement.
Press 'delete' to remove tower without compensation. Press 'r' to reset the 
current level. Be careful with that key. You can also change your
weapons quickly with number keys 1-4 and launch the next wave with 'ScaceBar.'

This is a mental test of true defender skills, the weak will perish quickly,
and only the strong will get through wave by wave, saving their people, 
their country, and their freedom. 

Choose Wisely. The time is now.




                           
                                                        (main menu)
                           
"""
        self.canvas.create_text(self.width/2, self.margin, 
            text = text, anchor = N)

    def drawHelpBackground(self):
        image = Image.open("help.gif")
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0,0,image=photo, anchor=NW)
        label = Label(image=photo)
        label.image = photo

    def drawBackButton(self):
        width = self.width
        height = self.height
        left = width/2-45
        right = left + 90
        bottom = height-10
        top = bottom-90
        boxWidth = right - left
        boxHeight = bottom - top
        (self.backT, self.backL) = (top, left)
        (self.backW,self.backH) = (boxWidth, boxHeight)
        image = Image.open("back.gif")
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(left,top,image=photo, anchor=NW)
        label = Label(image=photo)
        label.image = photo

    def drawBackground(self):
        image = Image.open("background.gif")
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0,0,image=photo, anchor=NW)
        label = Label(image=photo)
        label.image = photo

    def drawLevelBox1(self):
        width = self.width
        height = self.height
        left = self.sideMargin
        right = left + width/5.0
        top = self.margin*2
        bottom = top + height/8.0
        boxWidth = right - left
        boxHeight = bottom - top
        (self.box1T, self.box1L) = (top, left)
        self.box1W = boxWidth
        image = Image.open("button1.gif")
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(left,top,image=photo, anchor=NW)
        label = Label(image=photo)
        label.image = photo
        self.box1H = boxHeight

    def drawLevelBox2(self):
        width = self.width
        height = self.height
        left = width - self.sideMargin - width/5.0
        right = width - self.sideMargin
        top = self.margin*2
        bottom = self.margin*2 + height/8.0 
        boxWidth = right - left
        boxHeight = bottom - top
        (self.box2T, self.box2L) = (top, left)
        self.box2W = boxWidth
        self.box2H = boxHeight
        image = Image.open("button2.gif")
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(left,top,image=photo, anchor=NW)
        label = Label(image=photo)
        label.image = photo

    def drawLevelBox3(self):
        spacer = 50
        width = self.width
        height = self.height
        left = self.sideMargin
        right = left + width/5.0
        top = self.margin*2 + height/8.0 + spacer
        bottom = top + height/8.0
        boxWidth = right - left
        boxHeight = bottom - top
        self.canvas.create_text( left + boxWidth/2, top + boxHeight/2,
            text = "Map 3")
        (self.box3T, self.box3L) = (top, left)
        self.box3W = boxWidth
        self.box3H = boxHeight
        image = Image.open("button3.gif")
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(left,top,image=photo, anchor=NW)
        label = Label(image=photo)
        label.image = photo


    def drawLevelBox4(self):
        spacer = 50
        width = self.width
        height = self.height
        left = width - self.sideMargin - width/5.0
        right = width - self.sideMargin
        top = self.margin*2 + height/8.0 + spacer
        bottom = top + height/8.0
        boxWidth = right - left
        boxHeight = bottom - top
        self.canvas.create_text( left + boxWidth/2, top + boxHeight/2,
            text = "Map 4")
        (self.box4T, self.box4L) = (top, left)
        self.bo4W = boxWidth
        self.box4H = boxHeight
        image = Image.open("button4.gif")
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(left,top,image=photo, anchor=NW)
        label = Label(image=photo)
        label.image = photo

    def drawHelpBox(self):
        width = self.width
        height = self.height
        left = width/2 - width/10.0
        right = width/2 + width/10.0
        bottom = height - self.margin
        top = bottom - height/8
        boxWidth = right - left
        boxHeight = bottom - top
        (self.box5T, self.box5L) = (top, left)
        self.box5W = boxWidth
        self.box5H = boxHeight
        image = Image.open("button5.gif")
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(left,top,image=photo, anchor=NW)
        label = Label(image=photo)
        label.image = photo



    def initAnimation(self):
        pass

    def onTimerFired(self):
        pass

    def onKeyPressed(self, event):
        pass
        


    def loadLevel1(self):
        rows = self.rows
        cols = self.cols
        level = [ ]
        startRow = 5
        for row in range(rows): level += [[0] * cols] #0 means green
        for length in xrange(10): #Straight to column 10
            level[startRow][length] = 1 #1 means path
        for up in xrange(3,6): #How high the path will be: Row 4 -> row 6
            level[up][10] = 1 #10 = current col
        for length in xrange(10, 15):
            level[2][length] = 1 #2 = current row
        for down in xrange(2, 7):
            level[down][15] = 1
        for length in xrange(15, 17):
            level[7][length] = 1
        self.level = level
        self.startRow = startRow

    def loadLevel2(self):
        level=[
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,0,0,0,0,0,0,0,0,1,1,1,0,0],
        [0,1,1,1,0,0,0,0,0,0,1,0,1,0,0],
        [0,0,0,1,1,1,1,1,0,0,1,0,1,0,0],
        [0,0,0,0,0,0,0,1,0,0,1,0,1,0,0],
        [0,0,0,0,0,0,0,1,1,1,1,0,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        self.level = level

    def loadLevel3(self):
        level=[
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
        [0,0,0,0,1,1,1,1,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,1,0,0,1,1,1,0,0],
        [0,0,1,1,1,1,0,1,0,0,0,0,1,0,0],
        [0,0,1,0,0,1,0,1,0,0,0,0,1,1,0],
        [0,0,1,0,0,1,1,1,0,0,0,0,0,1,0],
        [1,1,1,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]]
        self.level = level

    def loadLevel4(self):
        level=[
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,1,0,0,0,0],
        [0,1,1,1,1,0,0,0,0,0,1,0,0,0,0],
        [0,1,0,0,1,0,0,0,0,0,1,0,0,0,0],
        [0,1,0,0,1,0,0,0,0,0,1,1,1,0,0],
        [1,1,0,0,1,1,1,1,1,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,1,1,1,1],
        [0,0,0,0,0,0,0,0,1,0,0,1,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        self.level = level
        
    def onMousePressed(self, event):
        (x,y) = (event.x, event.y)
        if not self.inHelpScreen:
            if self.box1L < x < (self.box1L + self.box1W):
                if self.box1T < y < (self.box1T + self.box1H):
                    self.loadLevel1()
                    self.canvas.destroy()
                    TowerDefense(self.level, self.canvas).run(self.root)
                elif self.box3T < y < (self.box3T + self.box3H):
                    self.loadLevel3()
                    self.canvas.destroy()
                    TowerDefense(self.level, self.canvas).run(self.root)
            elif self.box2L < x < (self.box2L + self.box2W):
                if self.box2T < y < (self.box2T + self.box2H):
                    self.loadLevel2()
                    self.canvas.destroy()
                    TowerDefense(self.level, self.canvas).run(self.root)
                elif self.box4T < y < (self.box4T + self.box4H):
                    self.loadLevel4()
                    self.canvas.destroy()
                    TowerDefense(self.level, self.canvas).run(self.root)
            elif self.box5L < x < (self.box5L + self.box5W):
                if self.box5T < y < (self.box5T + self.box5H):
                    self.inHelpScreen = True
        else: 
            if self.backL < x < (self.backL + self.backW):
                if self.backT < y < (self.backT + self.backH):
                    self.inHelpScreen = False


class TowerDefense(TermProject):
    def __init__(self, level, canvas):
        self.canvas = canvas
        self.level = level
        rows = len(level)
        cols = len(level[0])
        super(TowerDefense, self).__init__()
        self.rows = rows
        self.cols = cols
        self.getStartRow()
        self.textColor1 = "white"
        self.textColor2 = "red"


    def initAnimation(self):
        self.gameOver = False
        self.enemies = []
        self.towers = []
        self.timer = 0
        self.passedThrough = 0
        self.waveLevel = 0
        self.waveList = []
        self.bankAccount = 650
        self.pause = True
        self.loadWaveList()
        self.lives = 50
        self.towerType = 1
        self.towerSelected = None

    def getStartRow(self):
        for row in self.level:
            if row[0] == 1:
                self.startRow = self.level.index(row) 

    def loadEnemy(self):
        row = self.startRow
        x = self.sideMargin
        y = self.cellSize*row + self.margin+self.cellSize/2
        newEnemy = Enemy1(x,y,self.level)
        newEnemy.move()
        self.enemies.append(newEnemy)

    def loadEnemy2(self):
        row = self.startRow
        x = self.sideMargin
        y = self.cellSize*row + self.margin+self.cellSize/2
        newEnemy = Enemy2(x,y,self.level)
        self.enemies.append(newEnemy)

    def loadEnemy3(self):
        row = self.startRow
        x = self.sideMargin
        y = self.cellSize*row + self.margin+self.cellSize/2
        newEnemy = Enemy3(x,y,self.level)
        self.enemies.append(newEnemy)

    def loadEnemy4(self):
        row = self.startRow
        x = self.sideMargin
        y = self.cellSize*row + self.margin+self.cellSize/2
        newEnemy = Enemy4(x,y,self.level)
        self.enemies.append(newEnemy)


    def loadLevel1(self):
        rows = self.rows
        cols = self.cols
        level = [ ]
        startRow = 5
        for row in range(rows): level += [[0] * cols] #0 means green
        for length in xrange(10): #Straight to column 10
            level[startRow][length] = 1 #1 means path
        for up in xrange(3,6): #How high the path will be: Row 4 -> row 6
            level[up][10] = 1 #10 = current col
        for length in xrange(10, 15):
            level[2][length] = 1 #2 = current row
        for down in xrange(2, 7):
            level[down][15] = 1
        for length in xrange(15, 17):
            level[7][length] = 1
        self.level = level
        self.startRow = startRow

    def loadLevel2(self):
        rows = self.rows
        cols = self.cols
        level = [ ]
        for row in range(rows): level += [[0] * cols]
        for length in xrange(10):
            level[5][length] = 1
        self.startRow = 5
        for up in xrange(2,6):
            level[up][10] = 1
        for length in xrange(10, 15):
            level[2][length] = 1
        self.level = level

    def loadWaveList(self): #Generates the list for waves
        level = self.waveLevel
        if 2 <= level < 3:
            selectList = [0] * (120-abs(self.waveLevel))
            selectList = selectList + ([1,1,1,1]*(level+1))
            random.shuffle(selectList)
        elif 3 <= level < 8:
            selectList = [0] * (115-abs(self.waveLevel))
            selectList = selectList + ([1,1]*(level)) + ([2,2]*(level-2))
            selectList = selectList + [3]*level
            random.shuffle(selectList)
        elif 8 <= level < 10:
            selectList = [0] * (150-abs(self.waveLevel))
            selectList = selectList + ([1,1]*(level)) + ([2,2]*(level-2))
            selectList = selectList + ([3,3,3])*level
            random.shuffle(selectList)    
        elif 10 <= level < 15:
            selectList = [0] * (150-abs(self.waveLevel))
            selectList = selectList + ([1,1]*(level-3)) + ([2,2]*(level-2))
            selectList = selectList + ([3,3,3])*level
            random.shuffle(selectList)
        elif 15 == level:
            selectList = [0] * (170-abs(self.waveLevel))
            selectList = selectList + ([1]*(level-5)) + ([2]*(level-5))
            selectList = selectList + ([3])*(level-10)
            selectList = selectList + [4,4,4,4]
            random.shuffle(selectList)
        elif 15 < level:
            selectList = [0] * (115-abs(self.waveLevel))
            selectList = selectList + ([1]*(level-1)) + ([2,2]*(level-2))
            selectList = selectList + ([3,3,3,3])*(level/2)
            selectList = selectList + [4,4,4,4] * int(level/5)
        if level > 1:
            self.waveList = []
            waveListLength = ((len(selectList)-50) * 
                            (self.waveLevel-1)*self.waveLevel+15)
            self.waveList = [0]*waveListLength
            for i in xrange(waveListLength):
                self.waveList[i] = random.choice(selectList)
    
    def drawLevel(self):
        level = self.level
        rows = self.rows
        cols = self.cols
        for row in xrange(rows):
            for col in xrange(cols):
                self.drawCell(row, col)

    def drawCell(self, row, col):
        color = self.level[row][col] #0 -> green #1 or higher -> path 
        margin = self.margin
        sideMargin = self.sideMargin
        cellSize = self.cellSize
        left = sideMargin + col * cellSize
        right = left + cellSize
        top = margin + row * cellSize
        bottom = top + cellSize
        if color >= 1:
            image = Image.open("brick.gif")
            photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(left+(cellSize/2),bottom-(cellSize/2),
                            image=photo)
            label = Label(image=photo)
            label.image = photo
        else:
            self.canvas.create_rectangle(left, top, right, bottom, 
            fill="dark green", width = 1, outline = "dark green")

    def getRowAndCol(self, x, y):
    #Gets the row and col of where the mouse press was
        level = self.level
        margin = self.margin
        sideMargin = self.sideMargin
        cellW = cellH = self.cellSize
        vertBound = self.rows*self.cellSize
        horBound = self.cols*self.cellSize
        row = None
        col = None
        if (sideMargin < x < sideMargin+horBound): #Make sure click on board
            if (margin < y < margin+vertBound):
                col = (x-sideMargin)/(cellW)
                row = (y-margin)/(cellH)
            else: col = row = None
        else: row = row = None
        return (row, col)

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.drawBackground()
        self.drawLevel()
        self.drawEnemies()
        self.drawTowers()
        self.drawIfPausedText()  
        self.drawTowerText()
        self.drawWeapons()
        self.drawTopTexts()
        self.drawTowerInformation()
        self.drawMenuButton()
        if self.gameOver:
            self.canvas.create_text(self.width/2,self.height/2, 
            text = "Game Over",font = "Helvetica 50 bold",fill = "white")

    def drawMenuButton(self):
        color = self.textColor2
        right = self.width-self.sideMargin
        left = right - 50
        top = self.margin/2
        bottom = top + 25
        width = right-left
        height = bottom-top
        (self.menuBoxL, self.menuBoxW) = (left, width)
        (self.menuBoxB, self.menuBoxH) = (bottom, height)
        self.canvas.create_rectangle(left, top, right, bottom, 
            fill=color, width = 1, outline = "white")
        self.canvas.create_text(left+width/2,top+height/2,
            text = "MENU", fill = "black")


    def drawTowerInformation(self):
        color = self.textColor2
        self.canvas.create_text(self.sideMargin/2, self.margin, 
            text = "Tower Information", fill = color, anchor = N, 
            font = "Helvetica 16 bold underline")
        if not self.towerSelected:
            self.canvas.create_text(self.sideMargin/2, self.margin+20, 
            text = "No Tower Selected", fill = color, anchor = N, 
            font = "arial 12 italic")
        else:
            self.drawTowerDetails()
            self.drawUpgradeBoxes()

    def drawTowerDetails(self):
        color = self.textColor2
        fireTime = self.towerSelected.fireTime
        self.canvas.create_text(self.sideMargin/2, self.margin*2, 
            text = "Rate of Fire: %0.2f Seconds" %fireTime,fill=color,anchor = N, 
            font = "arial 13")
        killR = self.towerSelected.killR
        self.canvas.create_text(self.sideMargin/2, self.margin*2.25, 
            text = "Tower Distance: %0.2f feet" %killR,fill=color, anchor = N, 
            font = "arial 13")
        bodyCount = self.towerSelected.killCount
        self.canvas.create_text(self.sideMargin/2, self.margin*2.5, 
            text = "Body Count: %d Zombies" %bodyCount,fill=color, anchor = N, 
            font = "arial 13")

    def drawUpgradeBoxes(self):
        self.drawSpeedUpgrade()
        self.drawDistanceUpgrade()

    def drawSpeedUpgrade(self):
        (color1, color2) = (self.textColor1, self.textColor2)
        tower = self.towerSelected
        spacer = 10
        left = self.sideMargin/2 - 70
        right = self.sideMargin/2 + 70
        top = self.margin*2.75 + spacer
        bottom = self.margin*3.33 + spacer
        width = right-left
        height = bottom-top
        (self.uBox1L, self.uBox1W) = (left, width)
        (self.uBox1B, self.uBox1H) = (bottom, height)
        if tower.numOfSpeedUpgrades < 6:
            speedUpgradePrice = (100+(5**(tower.numOfSpeedUpgrades+1)))
            self.canvas.create_rectangle(left, top, right, bottom, 
                    fill=color2, width = 1, outline = color1)
            self.canvas.create_text(left+width/2,top+spacer, 
                text = "Upgrade Rate of Fire", fill = color1)
            self.canvas.create_text(left+width/2,top+spacer*3, 
                text = "Price: $%d" %speedUpgradePrice, fill = color1)
            tower.speedUpgradePrice = speedUpgradePrice

    def drawDistanceUpgrade(self):
        (color1, color2) = (self.textColor1, self.textColor2)
        tower = self.towerSelected
        spacer = 10
        left = self.sideMargin/2 - 70
        right = self.sideMargin/2 + 70
        top = self.margin*3.33 + spacer*2
        bottom = self.margin*3.85 + spacer*2
        (width,height) = (right-left, bottom-top)
        (self.uBox2L, self.uBox2W) = (left, width)
        (self.uBox2B, self.uBox2H) = (bottom, height)
        if tower.numOfDistanceUpgrades < 6:
            disUpgradePrice = (100+(5**(tower.numOfDistanceUpgrades+1)))
            self.canvas.create_rectangle(left, top, right, bottom, 
                    fill=color2, width = 1, outline = color1)
            self.canvas.create_text(left+width/2,top+spacer, 
                text = "Upgrade Distance", fill = color1)
            self.canvas.create_text(left+width/2,top+spacer*3, 
                text = "Price: $%d" %disUpgradePrice, fill = color1)
            tower.disUpgradePrice = disUpgradePrice

    def drawTopTexts(self):
        self.drawBankText()
        self.drawWaveText()
        self.drawLivesText()

    def drawBackground(self):
        self.canvas.create_rectangle(0,0,self.width,self.height,
            fill = "black")

    def drawWeapons(self):
        self.drawGunner()
        self.drawSniper()
        self.drawCentry()
        self.drawGrenade()

    def drawGunner(self):
        right = self.width-self.sideMargin/2+60
        left = self.width-self.sideMargin/2-60
        top = self.margin
        bottom = self.margin*2.5
        (self.gunnerRight,self.gunnerLeft) = (right,left)
        (self.gunnerTop,self.gunnerBottom) = (top,bottom)
        image = Image.open("gunner.gif")
        photo = ImageTk.PhotoImage(image)
        if self.towerType == 1:
            self.canvas.create_rectangle(left, top, right, bottom, 
                fill=None, width = 1, outline = self.textColor2)
        self.canvas.create_image(self.width-self.sideMargin/2,
            self.margin, image=photo, anchor = N)
        label = Label(image=photo)
        label.image = photo

    def drawSniper(self):
        right = self.width-self.sideMargin/2+60
        left = self.width-self.sideMargin/2-60
        top = self.margin*3
        bottom = self.margin*3 + 40
        (self.sniperRight,self.sniperLeft) = (right,left)
        (self.sniperTop,self.sniperBottom) = (top,bottom)
        image = Image.open("sniper.gif")
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(self.width-self.sideMargin/2,
            self.margin*3, image=photo, anchor = N)
        label = Label(image=photo)
        label.image = photo
        if self.towerType == 2:
            self.canvas.create_rectangle(left, top, right, bottom, 
                fill=None, width = 1, outline = self.textColor2)

    def drawCentry(self):
        right = self.width-self.sideMargin/2+60
        left = self.width-self.sideMargin/2-60
        top = self.margin*4
        bottom = self.margin*5.5
        (self.centryRight,self.centryLeft) = (right,left)
        (self.centryTop,self.centryBottom) = (top,bottom)
        if self.towerType == 3:
            self.canvas.create_rectangle(left, top, right, bottom, 
                fill=None, width = 1, outline = self.textColor2)
        image = Image.open("centry.gif")
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(self.width-self.sideMargin/2,
            self.margin*4,
                            image=photo, anchor = N)
        label = Label(image=photo)
        label.image = photo

    def drawGrenade(self):
        right = self.width-self.sideMargin/2+20
        left = self.width-self.sideMargin/2-20
        top = self.margin*5.75-5
        bottom = top+42
        (self.grenadeRight,self.grenadeLeft) = (right,left)
        (self.grenadeTop,self.grenadeBottom) = (top,bottom)
        if self.towerType == 4:
            self.canvas.create_rectangle(left, top, right, bottom, 
                fill=None, width = 1, outline = self.textColor2)
        image = Image.open("grenade_1.gif")
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(self.width-self.sideMargin/2,
            self.margin*5.5,
                            image=photo, anchor = N)
        label = Label(image=photo)
        label.image = photo

    def drawTowerText(self):
        color = self.textColor1
        if self.towerType == 1: towerType = "Gunner  - $250"
        elif self.towerType == 2: towerType = "Sniper  - $350"
        elif self.towerType == 3: towerType = "Centry  - $2000"
        elif self.towerType == 4: towerType = "Grenade - $400"
        towerText = 'Weapon Type: %s' % towerType
        self.canvas.create_text(self.width/2, self.height-self.margin/2+10,
                text = towerText , anchor = N, fill = color)

    def drawLivesText(self):
        color = self.textColor1
        livesText = "Lives: %d" % self.lives
        self.canvas.create_text(self.width/2, self.margin/2, text = livesText,
            anchor = N, fill = color)

    def drawIfPausedText(self):
        if self.pause:
            color = self.textColor2
            self.canvas.create_text(self.width/2, self.height-self.margin/2,
                text = "Press SpaceBar to Launch Next Wave", fill = color)

    def drawBankText(self):
        color = self.textColor1
        bankText = "Bank Account: $%d" % self.bankAccount
        self.canvas.create_text(self.margin, self.margin/2, text = bankText,
            anchor = W, fill = color)

    def drawWaveText(self):
        color = self.textColor1
        level = self.waveLevel
        width = self.width
        margin = self.margin
        sideMargin = self.sideMargin
        waveText = "Wave: %d" % (level+1)
        self.canvas.create_text(width-sideMargin/2, margin/2, 
            text = waveText, fill = color)

    def onKeyPressed(self, event):        
        if event.keysym == "a":
            self.loadEnemy()
        elif event.keysym == "s":
            self.loadEnemy2()
        elif event.keysym == "d":
            self.loadEnemy3() 
        elif event.keysym == "f":
            self.loadEnemy4()   
        elif event.keysym == "b":
            self.bankAccount += 1000
        elif event.keysym == "o":
            self.waveLevel -= 1
            self.loadWaveList()
        elif event.keysym == "p":
            self.waveLevel += 1
            self.loadWaveList()

        elif event.keysym == "BackSpace":
            for tower in self.towers:
                if tower.showKillR == True:
                    self.towerSelected = None
                    self.towers.remove(tower)
        elif event.keysym == "r":
            self.initAnimation()
        elif event.keysym == "space":
            if self.pause:
                self.pause = False
        elif event.keysym == "1":
            self.towerType = 1
        elif event.keysym == "2":
            self.towerType = 2
        elif event.keysym == "3":
            self.towerType = 3
        elif event.keysym == "4":
            self.towerType = 4

    def checkEnemyStatus(self):
        for enemy in self.enemies:
            if (enemy.testRowAndCol(enemy.x+(self.cellSize/2), 
                                enemy.y) == (None, None)):
                self.enemies.remove(enemy)
                if type(enemy) == Enemy1: self.lives -= 1 #Subtract 1 life
                elif type(enemy) == Enemy2: self.lives -= 2 #Subtract 2 lives 
                elif type(enemy) == Enemy3: self.lives -= 4 #Subtract 4 lives
                elif type(enemy) == Enemy4: self.lives -= 15 
            for tower in self.towers:
                if type(tower) == Grenade:
                    if (tower.fireTime+.2 >= 
                        time.time()-tower.initTime > tower.fireTime):
                        if tower.containsInKillRadius(enemy.x,enemy.y):
                            try: 
                                if type(enemy) != Enemy4:
                                    self.enemies.remove(enemy)
                                else: enemy.hitCount += 5
                            except: pass
                    elif (tower.fireTime+.2 < time.time()-tower.initTime):
                        self.towers.remove(tower)
                for projectile in tower.projectileList:
                    if enemy.contains(projectile.x,projectile.y):
                        if type(enemy) == Enemy1:
                            self.bankAccount += 2 #Adds 2 dollars 
                        elif type(enemy) == Enemy2:
                            self.bankAccount += 4 #Adds 4 dollars
                            newEnemy = Enemy1(enemy.x,
                                        enemy.y,self.level, enemy.lastMove)
                            self.enemies.append(newEnemy)
                        elif type(enemy) == Enemy3:
                            self.bankAccount += 4 #Adds 4 dollars
                            for i in xrange(4):
                                newEnemy = Enemy2(enemy.x,
                                enemy.y,self.level, enemy.lastMove)
                                self.enemies.append(newEnemy)
                        elif type(enemy) == Enemy4:
                            enemy.hitCount += 1
                            self.bankAccount += 2
                            if enemy.hitCount == 20:
                                self.launchBigBoyEnemies(enemy.x,
                                enemy.y,self.level, enemy.lastMove)
                        try: #In Case both hit at the same time
                            if type(enemy) != Enemy4:
                                self.enemies.remove(enemy)
                            elif type(enemy)==Enemy4 and enemy.hitCount==20:
                                self.enemies.remove(enemy)
                        except: pass
                        if type(projectile) != Projectile2:
                            tower.projectileList.remove(projectile)
                        tower.killCount += 1#Keeps track of how many kills
            else: enemy.move()

    def launchBigBoyEnemies(self, x, y, level, lastMove):
        for i in xrange(10):
            newEnemy = Enemy2(x,y,level,lastMove)
            self.enemies.append(newEnemy)
        for i in xrange(15):
            newEnemy = Enemy1(x,y,level,lastMove)
            self.enemies.append(newEnemy)
        for i in xrange(5):
            newEnemy = Enemy3(x,y,level,lastMove)
            self.enemies.append(newEnemy)

    def waveZero(self):
        if self.timer <= 600: #Good Zombie Time
            if self.timer % 40 == 0:
                self.loadEnemy()
            self.timer += 1    

        elif (self.timer == 601 and 
            len(self.enemies) == 0):
            self.timer = 0
            self.pause = True
            self.waveLevel+=1
            self.bankAccount += 200

    def waveOne(self):
        if self.timer <= 600:
            if self.timer % 30 == 0:
                self.loadEnemy()
            if self.timer % 60 == 0:
                self.loadEnemy2()
            self.timer += 1
        elif (self.timer == 601 and len(self.enemies)) == 0:
            self.timer = 0
            self.pause = True
            self.waveLevel += 1
            self.bankAccount += 250
            self.loadWaveList()

    def launchWaves(self):
        if self.waveLevel == 0: self.waveZero()
        elif self.waveLevel == 1: self.waveOne()
        if self.waveLevel > 1:
            if self.timer < len(self.waveList):
                currentEnemy = self.waveList[self.timer]
                if currentEnemy == 0: #Do Nothing
                    pass
                elif currentEnemy == 1: self.loadEnemy()
                elif currentEnemy == 2: self.loadEnemy2()
                elif currentEnemy == 3: self.loadEnemy3()
                elif currentEnemy == 4: self.loadEnemy4()
                self.timer += 1
            elif (self.timer == len(self.waveList) and 
                len(self.enemies) == 0):
                self.pause = True
                self.waveLevel += 1
                self.timer = 0
                self.bankAccount += (self.waveLevel+1)*150
                self.loadWaveList()

    def onTimerFired(self):
        if self.lives <= 0: 
            self.gameOver = True
        if not self.gameOver:
            self.checkEnemyStatus()
            if self.pause == False: #Start Waves
                self.launchWaves()
            for tower in self.towers: #Checks projectiles and moves them
                tower.checkEnemyAndKill(self.enemies)                            
                if len(tower.projectileList) > 0:
                    for projectile in tower.projectileList:
                        if tower.containsInKillRadius(projectile.x,
                                                      projectile.y):
                            projectile.move()
                        else: 
                            tower.projectileList = []

    def getWeaponClicked(self, x, y):
        if self.gunnerTop < y < self.gunnerBottom:
            self.towerType = 1
        elif self.sniperTop < y < self.sniperBottom:
            self.towerType = 2
        elif self.centryTop < y < self.centryBottom:
            self.towerType = 3
        elif self.grenadeLeft < x < self.grenadeRight:
            if self.grenadeTop < y < self.grenadeBottom:
                self.towerType = 4

    def getUpgradeClick(self, x, y):
        tower = self.towerSelected
        if self.uBox1B > y > (self.uBox1B - self.uBox1H):
            if tower.numOfSpeedUpgrades < 6:
                if self.bankAccount > tower.speedUpgradePrice:
                    self.upgrade1()
        elif self.uBox2B > y > (self.uBox2B - self.uBox2H):
            if self.towerSelected.numOfSpeedUpgrades < 6:
                if self.bankAccount > tower.disUpgradePrice:
                    self.upgrade2()

    def upgrade1(self):
        tower = self.towerSelected
        tower.fireTime *= .8
        self.bankAccount -= tower.speedUpgradePrice
        tower.numOfSpeedUpgrades += 1

    def upgrade2(self):
        tower = self.towerSelected
        tower.initKillR += 10
        self.bankAccount -= tower.disUpgradePrice
        tower.numOfDistanceUpgrades += 1

    def onMousePressed(self, event): 
        (x, y) = (event.x, event.y)
        if self.gunnerLeft < x < self.gunnerRight:
            self.getWeaponClicked(x,y)
            pass
        elif (self.towerSelected and 
            self.uBox1L < x < self.uBox1L + self.uBox1W):
            self.getUpgradeClick(x,y)
            pass
        elif self.menuBoxL < x < (self.menuBoxL + self.menuBoxW):
            if self.menuBoxB > y > (self.menuBoxB - self.menuBoxH):
                self.mainMenu()
        if not self.showKillR(x,y):
            (row, col) = self.getRowAndCol(event.x, event.y)
            if row != None and self.level[row][col] == 0:     
                self.createTower(x,y)
            elif (row!=None and self.level[row][col] == 1 and 
                self.towerType == 4):
                self.createGrenade(x,y)

    def mainMenu(self):
        self.canvas.destroy()
        TermProject().run(self.root)


    def showKillR(self, x, y):
        clickOnTower = False #Sees if there is a selected tower
        for tower in (self.towers):
            if (tower.contains(x, y)):
                clickOnTower = True
                self.towerSelected = tower
                if tower.showKillR == True: 
                    self.towerSelected = None
                    tower.showKillR = False
                elif tower.showKillR == False:
                    tower.showKillR = True
            elif x > self.sideMargin: 
                tower.showKillR = False 
        return clickOnTower

    def createGrenade(self, x, y):
        if self.bankAccount >= 400:
            self.bankAccount -= 400
            newTower = Grenade(x,y)
            self.towers.append(newTower)

    def createTower(self, x, y):
        if self.towerType == 1:
            if self.bankAccount >= 250:
                self.bankAccount -= 250
                newTower = Tower1(x,y)
                self.towerSelected = newTower
                self.towers.append(newTower)
        elif self.towerType == 2:
            if self.bankAccount >= 350:
                self.bankAccount -= 350
                newTower = Tower2(x,y)
                self.towerSelected = newTower
                self.towers.append(newTower)
        elif self.towerType == 3:
            if self.bankAccount >= 2000:
                self.bankAccount -= 2000
                newTower = Tower3(x,y)
                self.towerSelected = newTower
                self.towers.append(newTower)

    def drawEnemies(self):
        for enemy in self.enemies:
            enemy.draw(self.canvas)

    def drawTowers(self):
        for tower in self.towers:
            tower.draw(self.canvas)
            for projectile in tower.projectileList:
                projectile.draw(self.canvas)


class Enemy1(object):
    def __init__(self, x, y, level, lastMove = "right"):
        self.x = x
        self.y = y
        self.r = 12
        self.color = "blue"
        self.level = level
        self.margin = 80
        self.sideMargin = 250
        self.cellSize = 40
        self.rows = len(level) 
        self.cols = len(level[0])
        self.lastMove = lastMove
        self.speed = 2
        self.image = "zombie_1.4.gif"


    def draw(self, canvas):
        (x, y, r) = (self.x, self.y, self.r)
        image = Image.open(self.image)
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(x,y,image=photo)
        label = Label(image=photo)
        label.image = photo

    def move(self): #Long but easy to understand, it reads the map and moves
        move = self.speed
        testRight = (self.x)+self.cellSize/2
        testLeft = (self.x)-self.cellSize/2
        testUp = (self.y)-self.cellSize
        testDown = (self.y)+self.cellSize
        if self.lastMove == "up":
            if self.isLegalMovement(self.x, (testUp)):
                self.lastMove = "up"
                self.y -= move
            elif self.isLegalMovement(testRight, self.y):
                if self.isLegalMovement(self.x, (testUp + self.cellSize/2)):
                    self.lastMove = "up"
                    self.y -= move
                else:
                    self.lastMove = "right"
                    self.x += move
            elif self.isLegalMovement(testLeft, self.y):
                if self.isLegalMovement(self.x, (testUp + self.cellSize/2)):
                    self.lastMove = "up"
                    self.y -= move
                else:
                    self.lastMove = "left"
                    self.x -= move
        elif self.lastMove == "left":
            if self.isLegalMovement(testLeft, self.y):
                self.lastMove = "left"
                self.x -= move
            elif self.isLegalMovement(self.x, (testUp)):
                self.lastMove = "up"
                self.y -= move
        elif self.lastMove == "right" or self.lastMove == None:
            if self.isLegalMovement(testRight, self.y):
                self.lastMove = "right"
                self.x += move
            elif (self.isLegalMovement(self.x, (testDown)) and not
                self.isLegalMovement(self.x, (testUp))):
                    self.lastMove = "down"
                    self.y += move
            elif (self.isLegalMovement(self.x, (testUp+40)) and not
                self.isLegalMovement(self.x, (testDown+40))):
                    self.lastMove = "up"
                    self.y -= move
            elif (self.isLegalMovement(self.x, (testDown)) and 
                self.isLegalMovement(self.x, (testUp))):
                choice = random.choice(["up", "down"])
                if choice == "down":
                    self.lastMove = "down"
                    self.y += move
                else:
                    self.lastMove = "up"
                    self.y -= move
            elif self.isLegalMovement(self.x, (testDown)):
                self.lastMove = "down"
                self.y += move
            elif self.isLegalMovement(self.x, int(testUp)):
                self.lastMove = "up"
                self.y -= move
        elif self.lastMove == "down":
            if self.isLegalMovement(self.x, (testDown)):
                self.lastMove = "down"
                self.y += move
            elif self.isLegalMovement(testRight, self.y):
                if self.isLegalMovement(self.x, (testDown - self.cellSize/2)):
                    self.lastMove = "down"
                    self.y += move
                else:
                    self.lastMove = "right"
                    self.x += move

            



    def isLegalMovement(self, x, y):
        (row, col) = self.testRowAndCol(x, y)
        if row == None or col == None:
            return False
        elif self.level[row][col] == 0:
            return False
        return True


    def testRowAndCol(self, x, y):
    #Gets the row and col of where the test is
        level = self.level
        margin = self.margin
        sideMargin = self.sideMargin
        cellW = cellH = self.cellSize
        vertBound = self.rows*self.cellSize
        horBound = self.cols*self.cellSize
        row = None
        col = None
        if (sideMargin < x < sideMargin+horBound): #Make sure click on board
            if (margin < y < margin+vertBound):
                col = (x-sideMargin)/(cellW)
                row = (y-margin)/(cellH)
            else: col = row = None
        else: row = row = None
        return (row, col)

    #http://www.cs.cmu.edu/~112/notes/SmileyClassAnimationDemo.py
    def contains(self, x, y): #From Kosbie's smiley animation Class
        return ((self.x - x)**2 + (self.y - y)**2 <= self.r**2)

class Enemy2(Enemy1):
    def __init__(self, x, y, level, lastMove = "right"):
        super(Enemy2, self).__init__(x, y, level, lastMove)
        self.speed = 4
        self.image = "zombie_1.3.gif"

class Enemy3(Enemy1):
    def __init__(self, x, y, level, lastMove = "right"):
        super(Enemy3, self).__init__(x, y, level, lastMove)
        self.speed = 6
        self.image = "zombie_1.0.gif"

class Enemy4(Enemy1): #Big Boy
    def __init__(self, x, y, level, lastMove = "right"):
        super(Enemy4, self).__init__(x, y, level, lastMove)
        self.speed = 1
        self.image = "bigboy.gif"
        self.hitCount = 0


class Tower1(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.distance = 10
        self.r = 10
        self.killR = 0
        self.initKillR = 50
        self.showKillR = True
        self.projectileList = [ ]
        self.timer = 0
        self.killCount = 0
        self.towerLevel = 0
        self.initTime = time.time()
        self.color = "red"
        self.fireTime = 1
        self.numOfSpeedUpgrades = 0
        self.numOfDistanceUpgrades = 0
        self.projectileType = Projectile1


    def draw(self, canvas):
        (x, y, r) = (self.x, self.y, self.r)
        self.getLevel()
        self.killR = self.initKillR
        r2 = self.killR
        canvas.create_oval(x-r, y-r, x+r, y+r, 
            fill=self.color, outline="black", width=3)
        if self.showKillR == True:
            canvas.create_oval(x-r2, y-r2, x+r2, y+r2, 
                fill=None, outline="black", width=1)
        self.killR = r2

    def getLevel(self):
        self.towerLevel = self.killCount/5

    #http://www.cs.cmu.edu/~112/notes/SmileyClassAnimationDemo.py
    def contains(self, x, y): #From Kosbie's smiley animation Class
        return ((self.x - x)**2 + (self.y - y)**2 <= self.r**2)

    #Modified From
    #http://www.cs.cmu.edu/~112/notes/SmileyClassAnimationDemo.py
    def containsInKillRadius(self, x, y): #Modified Function from Smiley
        return ((self.x - x)**2 + (self.y - y)**2 <= self.killR**2+self.r)


    def checkEnemyAndKill(self, enemyList):
        for enemy in enemyList:
            if self.containsInKillRadius(enemy.x, enemy.y):
                if float(time.time()-(self.initTime)) >= self.fireTime:
                    self.fireProjectile(enemy.x, enemy.y)
                    self.initTime = time.time()

    def fireProjectile(self, enemyX, enemyY):
        if len(self.projectileList) < 1:
            newProjecticle = self.projectileType(self.x,self.y,
                                enemyX, enemyY, self.killR)
            self.projectileList.append(newProjecticle)

class Tower2(Tower1): #Sniper tower
    def __init__(self, x, y):
        super(Tower2, self).__init__(x, y)
        self.initKillR = 1000
        #Makes sure it hits everything on the map
        self.color = "orange"
        self.projectileType = Projectile2
        self.fireTime = random.choice([1.7,2])
        #Chooses a random fire time
        randomOffset = [0, self.fireTime/2]
        self.initTime = time.time()+random.choice(randomOffset)
        #Creates an offest for the firing, randomly
        


    def draw(self, canvas):
        (x, y, r) = (self.x, self.y, self.r)
        self.getLevel()
        self.killR = self.initKillR
        r2 = self.killR
        canvas.create_oval(x-r, y-r, x+r, y+r,
            fill=self.color, outline="black", width=3)

class Grenade(Tower1):
    def __init__(self,x,y):
        super(Grenade, self).__init__(x, y)
        self.initKillR = 75
        self.fireTime = 2
        self.initTime = time.time()

    def draw(self, canvas):
        (x, y, r) = (self.x, self.y, self.r)
        self.getLevel()
        self.killR = self.initKillR
        r2 = self.killR
        image = Image.open("grenade.gif")
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(x,y,image=photo)
        label = Label(image=photo)
        label.image = photo
        canvas.create_oval(x-r2, y-r2, x+r2, y+r2, 
                fill=None, outline="grey15", width=1)

    def fireProjectile(self, enemyX, enemyY):
        pass

    def checkEnemyAndKill(self, enemyList):
        pass

class Tower3(Tower1): #Centry Tower
    def __init__(self, x, y):
        super(Tower3, self).__init__(x, y)
        self.initKillR = 40
        self.fireTime = .05
        self.color = "cyan"

class Projectile1(object):
    def __init__(self,x,y, enemyX, enemyY, killR):
        self.x = x
        self.y = y
        self.enemyX = enemyX
        self.enemyY = enemyY
        self.dX = enemyX-x
        self.dY = enemyY-y
        self.r = 5
        self.killR = killR
        self.speed = 5

    def move(self):
        self.x += float(self.dX)/self.speed
        self.y += float(self.dY)/self.speed


    def draw(self, canvas):
        (x, y, r) = (self.x, self.y, self.r)
        canvas.create_oval(x-r, y-r, x+r, y+r, 
            fill="dark red", outline="red", width=1)

class Projectile2(Projectile1):
    def __init__(self,x,y, enemyX, enemyY, killR):
        super(Projectile2, self).__init__(x,y, enemyX, enemyY, killR)
        self.speed = 1
        


TermProject().run()
