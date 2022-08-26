import pyautogui as pg
from ReadWriteMemory import ReadWriteMemory

# The map starts at memory address 0x01005700
# Each row of the map is 32 bytes long
# and the map has 27 rows

# 0x10 Indicates an border of the map

# 0x8# Indicates an mine cell
# 0x4# Indicates an explored cell
# 0x0# Indicates an safe cell

# 0x#F Indicates an unexplored cell
# 0x#D Indicates an [?] makerd cell
# 0x#E Indicates an flag marked cell
# 0x#A Indicates an mine cell (when you loose the game)

# 0x40 Indicates an empty cell (explored)
# 0x41 Indicates an number 1 cell (explored)
# 0x42 Indicates an number 2 cell (explored)
...
# 0x47 Indicates an number 7 cell (explored)





rwm = ReadWriteMemory()
process = rwm.get_process_by_name('winmine.exe')
process.open()

msWindow = pg.getWindowsWithTitle("Minesweeper")[0] 

wx, wy = msWindow.topleft

# Coordinates to first cell
mapX, mapY = wx + 23, wy + 107 

msWindow.restore()
msWindow.activate()

pg.PAUSE = 0.005 # Change this to 0 if you want this FAST!

for row in range(26):
	rowOffset = row * 0x20 # Jump 32 bytes for each row.
	# Read each cell from the row an store into this list
	# Skips the first row as it just contains 0x10 cells (border cells) 
	cols = [process.read(0x01005700 + 0x20 + rowOffset + byteOffset) & 0xFF for byteOffset in range(32)] # This line of code is ugly and I really regret making it. I'm sorry. One day I'll fix it, I promise.

	# The first byte of a row is always 0x10 if not outside the map range
	# All cells outside the map are 0x0F
	# If both are equal it can only be 0x10 (bottom border of the map) or 0x0F (outside the map)
	if cols[0] == cols[1]:
		break
	
	for index in range(len(cols)):
		
		# Will be overwriten by the following line 
		byteItem = cols[1:][index]

		# Read again the byte as the map changes. 
		# You can comment this line to slow things a bit
		byteItem = process.read(0x01005720 + rowOffset + index + 1) & 0xFF
		

		# Break if reach border
		if byteItem == 0x10:
			break

		# Unexplored cell
		if byteItem == 0x0F:
			pg.moveTo(mapX+index*16,mapY + row*16)
			pg.click()

		# Mine cell
		elif byteItem == 0x8F:
			pg.moveTo(mapX+index*16,mapY + row*16)
			pg.rightClick()




