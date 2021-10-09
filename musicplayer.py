from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore
from PyQt5.QtCore import Qt , QTimer
from PyQt5.QtGui import * 
import sys
import os
import pygame
import mutagen.mp3

class main(QMainWindow):

	def __init__(self):
		super().__init__()
		self.x = 0
		self.musics = {
			'a' : '1' ,
		}
		self.paused = False
		self.show_ui()


	def show_ui(self):
		self.setWindowTitle("Simple Music Player")
		self.setGeometry(10 , 10 , 300+70 , 340)
		self.setStyleSheet("background-color:#465254;color:white")
		self.musicsarray = []
		self.lists = QListWidget(self)
		volume_label = QLabel("Volume : " , self)
		self.lists.resize(280+70, 100)
		self.lists.setStyleSheet("background-color:#5dcbde;color:black")
		self.timer = QTimer()
		self.que = 0
		self.slider = QSlider(Qt.Horizontal , self)
		self.slider.setSingleStep(0.1)
		self.slider.setMaximum(10)
		self.slider.setSliderPosition(7)
		buttonopen = QPushButton("Open file" , self)
		buttonplay = QPushButton("Play" , self)
		buttonplay.resize(70 , 60)
		buttonstop = QPushButton("Stop" , self)
		buttonstop.resize(70 , 60)
		buttonpause = QPushButton("Pause" , self)
		buttonpause.resize(70 , 60)
		buttondelete = QPushButton("Delete" , self)
		buttondelete.resize(70 , 60)
		buttonopen.resize(70 , 60)
		buttonopen.move(5 , 40)
		buttonplay.move(75 , 40)
		buttonstop.move(145 , 40)
		buttonpause.move(215 , 40)
		buttondelete.move(285 , 40)
		volume_label.move(0 , 1)
		self.slider.move(50 , 1)
		self.lists.move(5 , 130)
		self.slider.valueChanged.connect(self.change_volume)
		buttonopen.clicked.connect(self.openfile)
		buttonplay.clicked.connect(self.playmusic1)
		buttonpause.clicked.connect(self.pause_music)
		buttonstop.clicked.connect(self.stop_music)
		buttondelete.clicked.connect(self.delete_music)

	def openfile(self):
		file = QFileDialog.getOpenFileName(self , "Open file" , "" , "Music Files (*.mp3)")
		if len(file[0]) > 1:
			musicname = os.path.basename(file[0])
			self.musics[musicname] = file[0]
			self.lists.insertItem(self.x , musicname)
			self.x = self.x + 1
			self.musicsarray.append(file[0])
			print(self.musics)

	def playmusic1(self):
		if self.paused == False:
			self.que = self.lists.currentRow()
			pygame.mixer.quit()
			song = mutagen.mp3.MP3(self.musicsarray[self.que])
			pygame.mixer.init(frequency=song.info.sample_rate)
			pygame.mixer.music.load(self.musicsarray[self.que])
			pygame.mixer.music.play()
			pygame.mixer.music.set_volume(self.slider.value()/10)
			self.setWindowTitle(os.path.basename(self.musicsarray[self.que]))
			self.timer.timeout.connect(self.playmusic)
			self.timer.start(1000)
		else:
			pygame.mixer.music.unpause()
			self.paused = False

	def playmusic(self):
		pos = pygame.mixer.music.get_pos()
		if int(pos) == -1:
			self.que = self.que + 1
			if self.que+1 > len(self.musicsarray):
				self.que = 0
			
			song = mutagen.mp3.MP3(self.musicsarray[self.que])
			pygame.mixer.quit()
			pygame.mixer.init(frequency=song.info.sample_rate)
			pygame.mixer.music.load(self.musicsarray[self.que])
			pygame.mixer.music.play()
			pygame.mixer.music.set_volume(self.slider.value()/10)
			self.setWindowTitle(os.path.basename(self.musicsarray[self.que]))

	def change_volume(self):
		try:
			pygame.mixer.music.set_volume(self.slider.value() / 10)
		except pygame.error:
			return

	def stop_music(self):
		pygame.mixer.music.stop()
		pygame.mixer.quit()
		self.timer.stop()
		self.que = 0

	def pause_music(self):
		pygame.mixer.music.pause()
		self.paused = True

	def delete_music(self):
		musicname = self.lists.currentItem().text()
		del self.musics[musicname]
		row = self.lists.currentRow()
		del self.musicsarray[row]
		self.lists.takeItem(row)


if __name__=='__main__':
	app = QApplication(sys.argv)
	ex = main()
	ex.show()
	sys.exit(app.exec_())