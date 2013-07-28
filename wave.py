# -*- coding: utf-8 -*-

import tkinter as tk, threading
from random import randint
from time import sleep

colors = ["white", "red", "black", "grey", "yellow", "purple", "blue", "green", "pink", "orange"]
vertRectNum = 7

class Wave():
	def __init__(self, canvas, app):
		self.canvas = canvas
		self.app = app
		
		self.app.lock.acquire()
		self.rectSize = float(canvas['height']) / vertRectNum
		self.new_color = randint(0, len(colors)-1)
		if self.new_color == app.current_color:
			self.new_color -= 1
		app.current_color = self.new_color
		self.app.lock.release()
	
	def start(self):
		drawingThread = threading.Thread(target = self.draw)
		drawingThread.start()
	
	def draw(self):
		current_x = 0.0
		y = self.rectSize * 3
		while(current_x < (float(self.canvas['width']) + ((vertRectNum-1)/2)*self.rectSize)):
			self.canvas.create_rectangle(current_x, y, current_x + self.rectSize, y + self.rectSize, fill = colors[self.new_color])
			for i in range(1, int((vertRectNum-1)/2 + 1)):
				self.canvas.create_rectangle(current_x - self.rectSize*i, y - self.rectSize*i, current_x - self.rectSize*(i-1), y - self.rectSize*(i-1), fill = colors[self.new_color])
				self.canvas.create_rectangle(current_x - self.rectSize*i, y + self.rectSize*i, current_x - self.rectSize*(i-1), y + self.rectSize*(i+1), fill = colors[self.new_color])
			sleep(0.5)
			current_x += self.rectSize
		

class Application(tk.Frame):
	def __init__(self, width, height, master = None):
		super().__init__(master)
		self.pack()
		self.w = tk.Canvas(self, width = width, height = height)
		self.w.pack()
		self.w.create_rectangle(0, 0, width, height, fill=colors[0])
		self.w.bind("<Button-1>", self.mouse_click)
		self.current_color = 0
		self.lock = threading.Lock()
	
	def mouse_click(self, event):
		new_wave = Wave(self.w, self)
		new_wave.start()
	
	

root = tk.Tk()
app = Application(800, 800, master = root)
app.mainloop()