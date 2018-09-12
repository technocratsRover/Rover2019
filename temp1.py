import curses
import time
import sys
window = curses.initscr()
window.nodelay(1)

while True:
	window.addstr(0, 0, "Hello, world!")
	window.refresh()
	time.sleep(1)
	ch = window.getch()
	print(ch)

window.endwin()
