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
import time
class main(QMainWindow):

	def __init__(self):
		super().__init__()
		self.x = 0
		self.repeat_type = "Play all music(Repeat)"
		self.musics = {
			'a' : '1' ,
		}
		
		self.paused = False
		self.show_ui()


	def show_ui(self):
		self.setWindowTitle("Simple Music Player")
		self.weight = 300+70+80
		self.setGeometry(10 , 10 , self.weight , 340)
		#self.setStyleSheet("background-color:#465254;color:white")
		self.musicsarray = []
		self.lists = QListWidget(self)
		volume_label = QLabel("Volume : " , self)
		self.lists.resize(280+70, 100)
		#self.lists.setStyleSheet("background-color:#5dcbde;color:black")
		self.time_start = QLabel("00:00:00" , self)
		self.time_end = QLabel("00:00:00" , self)
		#self.timer = QTimer()
		self.que = 0
		self.slider = QSlider(Qt.Horizontal , self)
		self.slider.setSingleStep(1)
		self.slider.setMaximum(100)
		self.slider.setSliderPosition(7)
		buttonopen = QPushButton("Open file" , self)
		buttonplay = QPushButton("Play" , self)
		buttonplay.resize(70 , 60)
		buttonstop = QPushButton("Stop" , self)
		buttonstop.resize(70 , 60)
		buttonpause = QPushButton("Pause" , self)
		buttonpause.resize(70 , 60)
		buttondelete = QPushButton("Delete" , self)
		self.buttonrepeat = QPushButton("Repeat all" , self)
		self.buttonrepeat.resize(70 , 60)
		self.timer = QTimer(self)
		buttondelete.resize(70 , 60)
		buttonopen.resize(70 , 60)
		buttonopen.move(5 , 40)
		buttonplay.move(75 , 40)
		buttonstop.move(145 , 40)
		self.changed = False
		buttonpause.move(215 , 40)
		buttondelete.move(285 , 40)
		self.buttonrepeat.move(355 , 40)
		self.buttonrepeat.clicked.connect(self.repeat)
		volume_label.move(5 , 1)
		self.slider.move(57 , 1)
		self.lists.move(5 , 130)
		self.music_progress = QSlider(Qt.Horizontal , self)
		self.music_progress.resize(200 , 30)
		self.music_progress.setSingleStep(1)
		self.time_start.move(5 , 240)
		self.music_progress.move(60 , 240)
		self.music_progress.setTickInterval(1)
		self.music_progress.setPageStep(1)

		self.time_end.move(280 , 240)
		self.slider.valueChanged.connect(self.change_volume)
		buttonopen.clicked.connect(self.openfile)
		buttonplay.clicked.connect(self.playmusic1)
		buttonpause.clicked.connect(self.pause_music)
		buttonstop.clicked.connect(self.stop_music)
		buttondelete.clicked.connect(self.delete_music)
		#self.lists.doubleClicked.connect(self.playmusic1)
		self.music_progress.valueChanged.connect(self.change_progress)

	def openfile(self):
		
		file = QFileDialog.getOpenFileName(self , "Open file" , "" , "Music Files (*.mp3)")
		
		if len(file[0]) > 1:
			musicname = os.path.basename(file[0])
			self.musics[musicname] = file[0]
			self.lists.insertItem(self.x , musicname)
			self.x = self.x + 1
			self.musicsarray.append(file[0])
			print(self.musics)

	def change_progress(self):
		if self.changed == False:
			try:
				pygame.mixer.music.set_pos(self.music_progress.value())
			except Exception as e:
				print("a")
			

		

	def playmusic1(self):
		if self.paused == False:
			self.timer.stop()
			self.timer = QTimer(self)
			self.que = self.lists.currentRow()
			pygame.mixer.quit()
			song = 1
			try:
				song = mutagen.mp3.MP3(self.musicsarray[self.que])
			except Exception as e:
				#print("[ERROR]" , e)
				error_msg = QMessageBox.question(self, str(e), "Do you want to remove this file?", QMessageBox.Yes | QMessageBox.No)
				if error_msg == QMessageBox.Yes:
					musicname = self.lists.currentItem().text()
					del self.musics[musicname]
					row = self.lists.currentRow()
					del self.musicsarray[row]
					self.lists.takeItem(row)
				#exit()
			if song == 1:
				return
			print(round(song.info.length))
			self.music_progress.setMaximum(0)
			self.music_progress.setSliderPosition(0)
			self.music_progress.setMaximum(round(song.info.length))
			pygame.mixer.init(frequency=song.info.sample_rate)
			try:
				a = pygame.mixer.music.load(self.musicsarray[self.que])
			#self.music_progress.setMaximum(pygame.mixer.music.get_length())
				pygame.mixer.music.play()

			except Exception as e:
				print("[ERROR]" , e)
				#exit()
			duration = time.strftime("%H:%M:%S" , time.gmtime(int(song.info.length)))
			self.time_end.setText(str(duration))
			#pygame.mixer.music.set_pos(20)
			title = os.path.basename(self.musicsarray[self.que])
	
			pygame.mixer.music.set_volume(self.slider.value()/100)
			self.setWindowTitle(os.path.basename(self.musicsarray[self.que]))
			#self.lists.setCurrentItem(2)
			#print(self.lists.item(0))
			#self.lists.setCurrentItem(self.lists.item(0))
			#self.timer = QTimer(self)
			#self.timer.stop()
			self.timer.timeout.connect(self.playmusic)
			self.timer.stop()
			self.timer.start(1000)
		else:
			pygame.mixer.music.unpause()
			self.paused = False

	def playmusic(self):
		pos = pygame.mixer.music.get_pos()
		if int(pos) == -1:
			if self.repeat_type == "Play all music(Repeat)":
				self.que = self.que + 1
				if self.que+1 > len(self.musicsarray):
					self.que = 0
				song = 1
				try:
					song = mutagen.mp3.MP3(self.musicsarray[self.que])
				except Exception as e:
					error_msg = QMessageBox.question(self, str(e), "Do you want to remove this file?", QMessageBox.Yes | QMessageBox.No)
					if error_msg == QMessageBox.Yes:
						musicname = os.path.basename(self.musicsarray[self.que])
						del self.musics[musicname]
						del self.musicsarray[self.que]
						self.lists.takeItem(self.que)
						self.que = self.que + 1
					#exit()

				if song == 1:
					return

				duration = time.strftime("%H:%M:%S" , time.gmtime(round(song.info.length)))
				self.time_end.setText(str(duration))
				self.music_progress.setMaximum(0)
				self.music_progress.setSliderPosition(0)
				self.music_progress.setMaximum(round(song.info.length))
			
				print(song.info)
				pygame.mixer.quit()
				pygame.mixer.init(frequency=song.info.sample_rate)
				print(song.info)
				try:
					pygame.mixer.music.load(self.musicsarray[self.que])
					pygame.mixer.music.play()
				except Exception as e:
					print("[ERROR]" , e)
				pygame.mixer.music.set_volume(self.slider.value()/100)
			
				self.setWindowTitle(os.path.basename(self.musicsarray[self.que]))
				self.lists.setCurrentItem(self.lists.item(self.que))

			else:
				song = 1
				try:
					song = mutagen.mp3.MP3(self.musicsarray[self.que])

				except Exception as e:
					print("[ERROR]" , e)
					error_msg = QMessageBox.question(self, str(e), "Do you want to remove this file?", QMessageBox.Yes | QMessageBox.No)
					if error_msg == QMessageBox.Yes:
						musicname = os.path.basename(self.musicsarray[self.que])
						del self.musics[musicname]
						del self.musicsarray[self.que]
						self.lists.takeItem(self.que)
						self.que = self.que + 1
					#exit()

				if song == 1:
					return
				self.music_progress.setSliderPosition(0)
				pygame.mixer.quit()
				pygame.mixer.init(frequency=song.info.sample_rate)
				try:
					pygame.mixer.music.load(self.musicsarray[self.que])
					pygame.mixer.music.play()
				except Exception as e:
					print("[ERROR]" , e)
				pygame.mixer.music.set_volume(self.slider.value()/100)

		else:
			if self.paused == False:
				self.changed = True
				print(pos)
				#print(self.music_progress.value()+1)
				print(pygame.mixer.music.get_pos())
				self.music_progress.setSliderPosition(self.music_progress.value()+1)
				duration = time.strftime("%H:%M:%S" , time.gmtime(self.music_progress.value()))
				self.time_start.setText(str(duration))
				self.changed = False

	def change_volume(self):
		try:
			pygame.mixer.music.set_volume(self.slider.value() / 100)
		except pygame.error:
			return

	def stop_music(self):
		pygame.mixer.music.stop()
		pygame.mixer.quit()
		self.paused = False
		self.que = 0
		self.timer.stop()
		

	def pause_music(self):
		pygame.mixer.music.pause()
		self.paused = True


	def delete_music(self):
		musicname = self.lists.currentItem().text()
		del self.musics[musicname]
		row = self.lists.currentRow()
		del self.musicsarray[row]
		self.lists.takeItem(row)

	def skip_music(self):
		if self.que == len(self.musicsarray)-1:
			print("a")
		else:
			self.que = self.que + 1
			pygame.mixer.music.quit()
			freq = mutagen.mp3.MP3(self.musicsarray[self.que])
			pygame.mixer.init(frequency=fred.info.sample_rate)
			pygame.mixer.music.load()

	def repeat(self):
		if self.repeat_type == "Play all music(Repeat)":
			self.repeat_type = "Only repeat this song"
			self.buttonrepeat.resize(120 , 60)
			self.buttonrepeat.setText("Repeat this song")
			self.weight = self.weight + 50
			x = str(self.pos())
			print(x)
			y = x.split("PyQt5.QtCore.QPoint")
			print(y)
			z = y[1].split(", ")
			#print(z[0].replace("(" , ""))
			self.setGeometry(int(z[0].replace("(" , "")) , int(z[1].replace(")" , "")) , self.weight , 340)


		else:
			self.repeat_type="Play all music(Repeat)"
			
			self.weight = 300+70+80
			self.buttonrepeat.resize(70 , 60)
			self.buttonrepeat.setText("Repeat all")
			x = str(self.pos())
			print(x)
			y = x.split("PyQt5.QtCore.QPoint")
			z = y[1].split(", ")
			self.setGeometry(int(z[0].replace("(" , "")) , int(z[1].replace(")" , "")) , self.weight , 340)


if __name__=='__main__':
	app = QApplication(sys.argv)
	ex = main()
	ex.show()
	sys.exit(app.exec_())