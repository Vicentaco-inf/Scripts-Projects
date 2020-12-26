#!/usr/bin/env python
import os
from subprocess import call
from Tkinter import *	#sudo apt-get install python-tk
import ttk as tk
import tkMessageBox

#http://ubuntuhandbook.org/index.php/2019/01/install-openscad-ubuntu-18-10-18-04/
#sudo add-apt-repository ppa:openscad/releases
#sudo apt-get install openscad

import openpyscad as ops	 
				 


#https://likegeeks.com/es/ejemplos-de-la-gui-de-python/



'''
	CREATED BY VICENTE GRAS MAS AND JAVIER SANCHEZ MARTINEZ
	
	This code is divided by ### in 6 sections, the creation of the save window, the creation of the main window, the creation of the 3 models windows, and 
	the main launch code at the bottom of the script which make possible the active status of the app through the time.
	In each block, it will be structed as follows: first the creation of the interactive part, then the methods on it (button actions) and then the creation of 
	the interactive parts of the window(layers, buttons, textboxes...)


	Enjoy :-)
'''


####################################################################################################################################################################
#CREATION OF THE SAVE WINDOW

class creation:
	def __init__(self, root, List):
#def create(ListOfObjects):

		self.root = root
		self.root.geometry("500x300")
		self.root["bg"] = "white"

		ListOfObjects = List
		def clicked():

			name = str(saveEnt.get())

			if name is "":
				tkMessageBox.showinfo("Warning","not found name of the model, used \"sample\" as name")
				name = "sample"
			o = ops.Cube([0,0,0])
			for object in ListOfObjects:
				o = o + object
			
			(o).write(name+".scad")
				#Create scad
			if scad.instate(['selected']) and not stl.instate(['selected']):
					tkMessageBox.showinfo("Model generated",name +".scad model generated sucessfully at the path where this app is")			

			#Create stl
			elif not scad.instate(['selected']) and stl.instate(['selected']):
					tkMessageBox.showinfo("Model generated",name +".stl model generated sucessfully at the path where this app is")
					#generate stl model		
					cmd = 'openscad -o '+name+'.stl '+name+'.scad'
					os.system(cmd)
					#remove scad model
					cmd = 'rm '+name+'.scad'
					os.system(cmd)

			#Create scad and stl
			elif scad.instate(['selected']) and stl.instate(['selected']):
				tkMessageBox.showinfo("Models generated",name +".stl model and" + name+ " generated sucessfully at the path where this app is")
				#generate stl model		
				cmd = 'openscad -o '+name+'.stl '+name+'.scad'
				os.system(cmd)
			else:
				tkMessageBox.showinfo("Error", "Check at least 1 type of format to the model (stl or scad)")
				return
			self.root.destroy()
				

		#"Save" Label
		Table = Label(root, text= "Save the model/s")
		Table.place(x = 10, y = 10,width = 480, height = 30)
		#INFO
		Inf = Label(root, text = "Check the model that you want to save")
		Inf.place(x = 10, y = 40,width = 480, height = 30)
		#Round or square
		stl = tk.Checkbutton(root, text = "STL format")
		stl.place(x=10, y = 80, width = 480, height = 30)
		stl.state(['!alternate'])
		stl.state(['!selected'])
		scad = tk.Checkbutton(root, text = "SCAD format")
		scad.place(x=10, y = 120, width = 480, height = 30)
		scad.state(['!alternate'])
		scad.state(['!selected'])

		#save label
		save = Label(root, text= "Save as...")
		save.place(x=10, y = 180, width = 70, height = 30)
		#save name input
		saveEnt = Entry(root)
		saveEnt.place(x=90, y = 180, width = 400, height = 30)
		#Create button
		but = Button(root, text ="Save", command=clicked)
		but.place(x=330,y=260,width=160,height=30)
		#CLOSE WINDOW
		self.button_rename = tk.Button(self.root, text = "Back", command= lambda: self.root.destroy()).place(x=10, y= 260, width=50, height=30)

####################################################################################################################################################################
#CREATION OF THE MAIN WINDOW

class Win:
	def __init__(self, root):

		self.root = root
		self.root.geometry("890x380")
		self.root["bg"] = "white"
				#PLACE DESCRIPTION
		label = Label(root, text= "Choose one of the models clicking the button:")
		label.place(x=10, y = 10, width = 400, height = 30)

		#PLACE THE IMAGES OF THE MODELS 
		imgT = PhotoImage(file = "Table.png")
		labelT = Label(image = imgT)
		labelT.image = imgT
		labelT.place(x=10,y=50,width=280,height=280)
		imgO = PhotoImage(file = "DESK.png")
		labelO = Label(image = imgO)
		labelO.image = imgO
		labelO.place(x=300,y=50,width=280,height=280)
		imgD = PhotoImage(file = "oneLeg.png")
		labelD = Label(image = imgD)
		labelD.image = imgD
		labelD.place(x=600,y=50,width=280,height=280)
	
	
		#NAVEGATE BETWEEN THE 3 TYPES OF TABLE
		self.button_rename = tk.Button(self.root, text = "Table model", command= lambda: self.new_window(Table)).place(x=100,y=340,width=100,height=30)
 
		self.button_rename = tk.Button(self.root, text = "Desk model", command= lambda: self.new_window(Desk)).place(x=400,y=340,width=100,height=30)
	
		self.button_rename = tk.Button(self.root, text = "One leg table model", command= lambda: self.new_window(OneLegTable)).place(x=700,y=340,width=100,height=30)

		self.button_rename = tk.Button(self.root, text = "Close", command= lambda: self.root.destroy()).place(x=780, y = 10, width = 100, height = 30)


	def new_window(self, _class):
	        self.new = Toplevel(self.root)
	        _class(self.new)
	

	"""
	the method .place recives four arguments:
	from (x = 0,y = 0) which is placed upper-left the screen.
	x means the relative displace to left
	y means the relative displace down
	width and height are the width and height of the object 
	"""
####################################################################################################################################################################
#CREATION OF THE TABLE
class Table:

	def __init__(self, root):
	
		self.root = root
		self.root.geometry("500x810")
		self.root["bg"] = "white"

		def clicked():
							#PARAMETRIZE THE TABLE AND LEGS
			posL = -1
			WTab = 0
			HTab = 0
			Thk = 0
			alt = 0
			WLeg = 0
			HLeg = 0
			RLeg = 0
			RTab = 0
			#TABLE
			#capture thickness
			try:
				Thk = int(ThicknessEnt.get())
			except:
				tkMessageBox.showinfo("Error", "Table model needs a thickness")
				return

			#Square or round table
			if sq.instate(['selected']) and not ro.instate(['selected']):
				#Create squared table
				try:
					WTab = int(anchEnt.get())
					HTab = int(LargeEnt.get())
				except:
					tkMessageBox.showinfo("Error", "Anchor or weight inputs are wrong or missing")
				#Tab = ops.Cube([WTab, HTab, Thk])
				Pos = [-int(WTab/2), -int(HTab/2)]
				TabSz = [WTab, HTab, Thk]
			elif not sq.instate(['selected']) and ro.instate(['selected']):
			#Create Round table
				try:
					RTab = int(RadEnt.get())
				except: 
					tkMessageBox.showinfo("Error", "Error on radius of the table input")
				#Tab = ops.Cylinder(h = Thk, r = RTab)
				Pos = [RTab, RTab]
				TabSz = [Thk, RTab]
			else:
				tkMessageBox.showinfo("Error", "cant genenerate, 0 or 2 checkboxes of table checked")
			
			#LEGS
			#get position of legs at the table
			try:
				posL = int(InsideEntL.get())
			
			except:
				tkMessageBox.showinfo("Waring", "Position of legs not found, using 0 as value")
				posL = 0
			#get altura of legs at the table and pos the table in the space
			try:
				alt = int(AltEntL.get())
				Pos.append(alt)
				
			except:
				tkMessageBox.showinfo("Error", "Altura value invalid")

			#Square or round legs
			if sqL.instate(['selected']) and not roL.instate(['selected']):
				#Create squared legs
				try:
					WLeg = int(anchEntL.get())
					HLeg = int(LargeEntL.get())
				except:
					tkMessageBox.showinfo("Error", "Anchor or weight inputs are wrong or missing")
				LegSz = [WLeg, HLeg, alt]

				
			elif not sqL.instate(['selected']) and roL.instate(['selected']):
				#Create Round legs
				try:
					RLeg = int(RadEntL.get())
				except: 
					tkMessageBox.showinfo("Error", "Error on radius of the legs input")
				LegSz = [alt, RLeg]
			else:
				tkMessageBox.showinfo("Error", "cant genenerate, 0 or 2 checkboxes of legs checked")
		


						#CREATE THE OBJECTS


			#CREATE THE TABLE
			if sq.instate(['selected']) and not ro.instate(['selected']):
				
				try:
					Tab = ops.Cube(TabSz).color(str(ColEnt.get())).translate(Pos)
				except:
					tkMessageBox.showinfo("Error", "invalid color for table")
					return

			elif not sq.instate(['selected']) and ro.instate(['selected']):
				
				try:
					Tab = ops.Cylinder(h=Thk,r=RTab).color(str(ColEnt.get())).translate([0,0,alt])
				except:
					tkMessageBox.showinfo("Error", "invalid color for table")
					return	
			ListOfObjects = [Tab]
			#CREATE THE LEGS
			x = Pos[0]
			y = Pos[1]
			#square legs
			if sqL.instate(['selected']) and not roL.instate(['selected']):

				try:
					if sq.instate(['selected']) and not ro.instate(['selected']):
						Leg1 = ops.Cube(LegSz).color(str(ColEntL.get())).translate([x+posL,y+posL,0])
						Leg2 = ops.Cube(LegSz).color(str(ColEntL.get())).translate([-x-WLeg-posL,y+posL,0])
						Leg3 = ops.Cube(LegSz).color(str(ColEntL.get())).translate([x+posL,-y-HLeg-posL,0])
						Leg4 = ops.Cube(LegSz).color(str(ColEntL.get())).translate([-x-WLeg-posL,-y-HLeg-posL,0])
					elif not sq.instate(['selected']) and ro.instate(['selected']):
						Leg1 = ops.Cube(LegSz).color(str(ColEntL.get())).translate([x-posL-RLeg,0,0])
						Leg2 = ops.Cube(LegSz).color(str(ColEntL.get())).translate([0,y - posL - RLeg,0])
						Leg3 = ops.Cube(LegSz).color(str(ColEntL.get())).translate([-x+posL + RLeg,0,0])
						Leg4 = ops.Cube(LegSz).color(str(ColEntL.get())).translate([0,-y+posL + RLeg,0])
				except:
					tkMessageBox.showinfo("Error", "invalid color for legs")
					return
			#round legs
			elif not sqL.instate(['selected']) and roL.instate(['selected']):
				
				try:
					if sq.instate(['selected']) and not ro.instate(['selected']):
						Leg1 = ops.Cylinder(h=alt,r=RLeg).color(str(ColEntL.get())).translate([x+posL,y+posL,0])
						Leg2 = ops.Cylinder(h=alt,r=RLeg).color(str(ColEntL.get())).translate([-x-WLeg-posL,y+posL,0])
						Leg3 = ops.Cylinder(h=alt,r=RLeg).color(str(ColEntL.get())).translate([x+posL,-y-HLeg-posL,0])
						Leg4 = ops.Cylinder(h=alt,r=RLeg).color(str(ColEntL.get())).translate([-x-WLeg-posL,-y-HLeg-posL,0])
					elif not sq.instate(['selected']) and ro.instate(['selected']):
						Leg1 = ops.Cylinder(h=alt,r=RLeg).color(str(ColEntL.get())).translate([x-posL-RLeg,0,0])
						Leg2 = ops.Cylinder(h=alt,r=RLeg).color(str(ColEntL.get())).translate([0,y - posL - RLeg,0])
						Leg3 = ops.Cylinder(h=alt,r=RLeg).color(str(ColEntL.get())).translate([-x+posL + RLeg,0,0])
						Leg4 = ops.Cylinder(h=alt,r=RLeg).color(str(ColEntL.get())).translate([0,-y+posL + RLeg,0])
				except:
					tkMessageBox.showinfo("Error", "invalid color for legs")
					return
			ListOfObjects.append(Leg1)	
			ListOfObjects.append(Leg2)
			ListOfObjects.append(Leg3)
			ListOfObjects.append(Leg4)
		
			#check if all parameters are okey 
			if  posL < 0 or Thk <= 0 or alt <= 0 or ((WLeg <= 0 or HLeg <= 0) and sqL.instate(['selected'])) or (RLeg <= 0 and roL.instate(['selected'])) or (sq.instate(['selected']) and ((HTab <= 0 or WTab <= 0) and (posL > WTab/2 or HTab/2 < posL))) or (ro.instate(['selected']) and RTab <= 0 and posL > RTab) or (WTab < RLeg) or (HTab < RLeg) or (WTab < WLeg * 2) or (HTab < HLeg * 2):
				tkMessageBox.showinfo("Error", "some used parameters are negative, zero, or have conflict with other parameters")
				return
			else:
				self.new = Toplevel(self.root)
				creation(self.new,ListOfObjects)
			#saveWindow = creation(root, ListOfObjects)

		#"Table" Label
		Table = Label(root, text= "Table")
		Table.place(x = 10, y = 10,width = 480, height = 30)
		#INFO
		Inf = Label(root, text = "If you check Square, radius will be ignored\nIf you check Square, anchor and large will be ignored")
		Inf.place(x = 10, y = 40,width = 480, height = 60)
		#Round or square
		sq = tk.Checkbutton(root, text = "Square")
		sq.place(x=10, y = 110, width = 480, height = 30)
		sq.state(['!alternate'])
		sq.state(['selected'])
		ro = tk.Checkbutton(root, text = "Round")
		ro.place(x=10, y = 150, width = 480, height = 30)
		ro.state(['!alternate'])
		ro.state(['!selected'])

		#Large 
		anchor = Label(root, text= "Large of the table:")
		anchor.place(x=10, y = 190, width = 480, height = 30)
		anchEnt = Entry(root)
		anchEnt.place(x=410, y = 190, width = 70, height = 30)
		#Anchor
		Large = Label(root, text= "Anchor of the table:")
		Large.place(x=10, y = 230, width = 480, height = 30)
		LargeEnt = Entry(root)
		LargeEnt.place(x=410, y = 230, width = 70, height = 30)
		#Thickness
		Thick = Label(root, text= "Thickness of the table:")
		Thick.place(x=10, y = 270, width = 480, height = 30)
		ThicknessEnt = Entry(root)
		ThicknessEnt.place(x=410, y = 270, width = 70, height = 30)
		#Radius
		Radius = Label(root, text= "Radius of the table:")
		Radius.place(x=10, y = 310, width = 480, height = 30)
		RadEnt = Entry(root)
		RadEnt.place(x=410, y = 310, width = 70, height = 30)
		#Color
		Col = Label(root, text= "Color of the table (red, blue, ...):")
		Col.place(x=10, y = 350, width = 480, height = 30)
		ColEnt = Entry(root)
		ColEnt.place(x=410, y = 350, width = 70, height = 30)
		#Separator
		separator = Label(root, text= ".")
		separator.place(x = 10, y = 400,width = 480, height = 1)
		#"Legs" Label
		Table = Label(root, text= "Legs")
		Table.place(x = 10, y = 420,width = 480, height = 30)
		#Round or square Table
		sqL = tk.Checkbutton(root, text = "Square")
		sqL.place(x=10, y = 460, width = 480, height = 30)
		sqL.state(['!alternate'])
		sqL.state(['selected'])
		roL = tk.Checkbutton(root, text = "Round")
		roL.place(x=10, y = 490, width = 480, height = 30)
		roL.state(['!alternate'])
		#Large Leg
		anchorL = Label(root, text= "Large of the leg:")
		anchorL.place(x=10, y = 530, width = 480, height = 30)
		anchEntL = Entry(root)
		anchEntL.place(x=410, y = 530, width = 70, height = 30)
		#Anchor Leg
		LargeL = Label(root, text= "Anchor of the leg:")
		LargeL.place(x=10, y = 570, width = 480, height = 30)
		LargeEntL = Entry(root)
		LargeEntL.place(x=410, y = 570, width = 70, height = 30)
		#Radius Leg
		RadiusL = Label(root, text= "Radius of the leg:")
		RadiusL.place(x=10, y = 610, width = 480, height = 30)
		RadEntL = Entry(root)
		RadEntL.place(x=410, y = 610, width = 70, height = 30)
		#height Leg
		AltL = Label(root, text= "height of the legs:")
		AltL.place(x=10, y = 650, width = 480, height = 30)
		AltEntL = Entry(root)
		AltEntL.place(x=410, y = 650, width = 70, height = 30)
		#Inside Table Legs
		InsideL = Label(root, text= "place inside the table:")
		InsideL.place(x=10, y = 690, width = 480, height = 30)
		InsideEntL = Entry(root)
		InsideEntL.place(x=410, y = 690, width = 70, height = 30)
		#Color
		ColL = Label(root, text= "Color of the legs (red...):")
		ColL.place(x=10, y = 730, width = 480, height = 30)
		ColEntL = Entry(root)
		ColEntL.place(x=410, y = 730, width = 70, height = 30)
		
		
		#Create button
		but = Button(root, text ="Generate model", command=clicked)
		but.place(x=330,y=770,width=160,height=30)
		#CLOSE WINDOW
		self.button_rename = tk.Button(self.root, text = "Back", command= lambda: 	
		self.root.destroy()).place(x = 10, y = 770, width = 110, height = 30)


####################################################################################################################################################################
#CREATION OF THE DESK TABLE
	
class Desk:


	def __init__(self, root):

		self.root = root
		self.root.geometry("500x600")
		self.root["bg"] = "white"

		def clicked():

			HTab = 0
			WTab = 0
			Thk = 0
			alt = 0
			ancDr = 0
			larDr = 0
			#capture thickness
			try:
				Thk = int(ThicknessEnt.get())
			except:
				tkMessageBox.showinfo("Error", "Table model needs a thickness")
				return
			try:
				alt = int(HEnt.get())
			except:
				tkMessageBox.showinfo("Error", "Table model needs a height")
				return

				#Create squared table
			try:
				WTab = int(anchEnt.get())
				HTab = int(LargeEnt.get())
			except:
				tkMessageBox.showinfo("Error", "Anchor or weight inputs are wrong or missing")

			Pos = [-int(WTab/2), -int(HTab/2),alt]
			TabSz = [WTab, HTab, Thk]
			Tab = ops.Cube(TabSz).color(str(ColEnt.get())).translate(Pos)
			ListOfObjects = [Tab]
			back = ops.Cube([1, HTab, alt/2]).translate([-int(WTab/2),-int(HTab/2),alt/2])
			ListOfObjects.append(back)
			try:
				ancDr = int(anchEntL.get())
			except:
				ancDr = 0
			try:
				larDr = int(LargeEntL.get())
			except:
				larDr = 0
			
			if (ancDr == 0 or larDr == 0) and (sqL.instate(['selected']) or roL.instate(['selected'])):
				tkMessageBox.showinfo("Error", "some drawers are selected so they need anchor and large meassures")
				return

			tamD = [WTab, larDr, ancDr]
			tamTir = [5, int(larDr/5),int(ancDr/10)]
			try:
				cantDrawers = int(str(alt / ancDr).split(".")[0])
				
				try:
					colorD = str(ColEntL.get())
				except:
					pass
				#sqL are left drawers roL are right drawers
				#check left side
				if sqL.instate(['selected']) and not roL.instate(['selected']):
					#<>
					despIzq = [-int(WTab/2), -int(HTab/2), alt-larDr]
					auxPiece = ops.Cube([WTab, 1, alt]).translate([-int(WTab/2),int(HTab/2) - 1,0])
					ListOfObjects.append(auxPiece)
					drw = ops.Cube(tamD).translate(despIzq).color(colorD)
					ListOfObjects.append(drw)
					drwTir = ops.Cube(tamTir).translate([int(WTab/2),-int(HTab/2)+int(larDr/2)-int(larDr/10), alt])
					ListOfObjects.append(drwTir)
					aux = alt
					while cantDrawers > 0:
						despIzq[2] = despIzq[2] - larDr
						drw = ops.Cube(tamD).translate(despIzq)				
						ListOfObjects.append(drw)
						aux = aux - ancDr
						if aux > 10:
							drwTir = ops.Cube(tamTir).translate([int(WTab/2),-int(HTab/2)+int(larDr/2)-int(larDr/10), aux])
							ListOfObjects.append(drwTir)
						else:
							pass
						cantDrawers = cantDrawers - 1
					rest = alt - larDr*cantDrawers
					tamD[2] = rest
					despIzq[2] = 0
					restC = ops.Cube(tamD).translate(despIzq)
					ListOfObjects.append(restC)

				#check right side	
				elif not sqL.instate(['selected']) and roL.instate(['selected']):
				
					#<>
					despIzq = [-int(WTab/2), +int(HTab/2)-larDr, alt-larDr]
					auxPiece = ops.Cube([WTab, 1, alt]).translate([-int(WTab/2),-int(HTab/2),0])
					ListOfObjects.append(auxPiece)
					drw = ops.Cube(tamD).translate(despIzq).color(colorD)
					ListOfObjects.append(drw)
					drwTir = ops.Cube(tamTir).translate([int(WTab/2),int(HTab/2)-int(larDr/2)-int(larDr/10), alt])
					ListOfObjects.append(drwTir)
					aux = alt
					while cantDrawers > 0:
						despIzq[2] = despIzq[2] - larDr
						drw = ops.Cube(tamD).translate(despIzq)				
						ListOfObjects.append(drw)
						aux = aux - ancDr
						if aux > 10:
							drwTir = ops.Cube(tamTir).translate([int(WTab/2),+int(HTab/2)-int(larDr/2)-int(larDr/10), aux])
							ListOfObjects.append(drwTir)
						else:
							pass
						cantDrawers = cantDrawers - 1
					rest = alt - larDr*cantDrawers
					tamD[2] = rest
					despIzq[2] = 0
					restC = ops.Cube(tamD).translate(despIzq)
					ListOfObjects.append(restC)

				#Check both sides
				elif sqL.instate(['selected']) and roL.instate(['selected']):
					#<>
					despIzq = [-int(WTab/2), -int(HTab/2), alt-larDr]
					despDer = [-int(WTab/2), +int(HTab/2)-larDr, 0]
					auxPiece = ops.Cube([WTab, 1, alt]).translate([-int(WTab/2),int(HTab/2) - 1,0])
					ListOfObjects.append(auxPiece)
					drw = ops.Cube(tamD).translate(despIzq).color(colorD)
					ListOfObjects.append(drw)
					drwTir = ops.Cube(tamTir).translate([int(WTab/2),-int(HTab/2)+int(larDr/2)-int(larDr/10), alt])
					ListOfObjects.append(drwTir)
					drw = ops.Cube(tamD).translate(despIzq).color(colorD)
					ListOfObjects.append(drw)
					drwTir = ops.Cube(tamTir).translate([int(WTab/2),int(HTab/2)-int(larDr/2)-int(larDr/10), alt])
					ListOfObjects.append(drwTir)					
					aux = alt
					while cantDrawers > 0:
						despIzq[2] = despIzq[2] - larDr
						#despDer[2] = despDer[2] - larDr
						drw = ops.Cube(tamD).translate(despIzq)				
						ListOfObjects.append(drw)
						drw = ops.Cube(tamD).translate(despDer)				
						ListOfObjects.append(drw)
						aux = aux - ancDr
						if aux > 10:
							drwTir = ops.Cube(tamTir).translate([int(WTab/2),-int(HTab/2)+int(larDr/2)-int(larDr/10), aux])
							ListOfObjects.append(drwTir)
							drwTir = ops.Cube(tamTir).translate([int(WTab/2),+int(HTab/2)-int(larDr/2)-int(larDr/10), aux])
							ListOfObjects.append(drwTir)
						else:
							pass
						cantDrawers = cantDrawers - 1
					rest = alt - larDr*cantDrawers
					tamD[2] = rest
					despIzq[2] = 0
					restC = ops.Cube(tamD).translate(despIzq)
					ListOfObjects.append(restC)
					
				else:
					pass
					
			except:
				#check if nothing is selected
				if not sqL.instate(['selected']) and not roL.instate(['selected']):
					auxPiece = ops.Cube([WTab, 1, alt]).translate([-int(WTab/2),int(HTab/2) - 1,0])
					ListOfObjects.append(auxPiece)
					auxPiece = ops.Cube([WTab, 1, alt]).translate([-int(WTab/2),-int(HTab/2),0])
					ListOfObjects.append(auxPiece)
					tkMessageBox.showinfo("Warning", "There is no drawer/s selected, the model will be a desk without drawers")

			#check all the parameters okey
			if HTab <= 0 or WTab <= 0 or Thk <= 0 or alt <= 0 or ((ancDr <= 0 or larDr <= 0) and (sqL.instate(['selected']) or roL.instate(['selected']))) or ((HTab < larDr*2) and (sqL.instate(['selected']) or roL.instate(['selected']))) or ((alt < ancDr) and (sqL.instate(['selected']) or roL.instate(['selected']))):
				tkMessageBox.showinfo("Error", "some used parameters are negative, zero, or have conflict with other parameters")
				return
			else:
				self.new = Toplevel(self.root)
				creation(self.new,ListOfObjects)
				#saveWindow = creation(root, ListOfObjects)

		#"Table" Label
		Table = Label(root, text= "Table")
		Table.place(x = 10, y = 10,width = 480, height = 30)
		#INFO
		Inf = Label(root, text = "If you dont select drawers, legs will be placed")
		Inf.place(x = 10, y = 40,width = 480, height = 30)
		#Large
		anchor = Label(root, text= "Large of the table:")
		anchor.place(x=10, y = 80, width = 480, height = 30)
		anchEnt = Entry(root)
		anchEnt.place(x=410, y = 80, width = 70, height = 30)
		#Anchor
		Large = Label(root, text= "Anchor of the table:")
		Large.place(x=10, y = 120, width = 480, height = 30)
		LargeEnt = Entry(root)
		LargeEnt.place(x=410, y = 120, width = 70, height = 30)
		#Thickness
		Thick = Label(root, text= "Thickness of the table:")
		Thick.place(x=10, y = 160, width = 480, height = 30)
		ThicknessEnt = Entry(root)
		ThicknessEnt.place(x=410, y = 160, width = 70, height = 30)
		#Height
		Radius = Label(root, text= "height of the table:")
		Radius.place(x=10, y = 200, width = 480, height = 30)
		HEnt = Entry(root)
		HEnt.place(x=410, y = 200, width = 70, height = 30)
		#Color
		Col = Label(root, text= "Color of the table (red, blue, ...):")
		Col.place(x=10, y = 240, width = 480, height = 30)
		ColEnt = Entry(root)
		ColEnt.place(x=410, y = 240, width = 70, height = 30)
		#Separator
		separator = Label(root, text= ".")
		separator.place(x = 10, y = 280,width = 480, height = 1)
		#"Drawers" Label
		Table = Label(root, text= "Drawers")
		Table.place(x = 10, y = 320,width = 480, height = 30)
		#Drawers selector
		sqL = tk.Checkbutton(root, text = "Drawers on left")
		sqL.place(x=10, y = 360, width = 480, height = 30)
		sqL.state(['!alternate'])
		sqL.state(['!selected'])
		roL = tk.Checkbutton(root, text = "Drawers on right")
		roL.place(x=10, y = 400, width = 480, height = 30)
		roL.state(['!alternate'])
		sqL.state(['!selected'])
		#Height drawer
		anchorL = Label(root, text= "Height of the drawers:")
		anchorL.place(x=10, y = 440, width = 480, height = 30)
		anchEntL = Entry(root)
		anchEntL.place(x=410, y = 440, width = 70, height = 30)
		#Anchor drawer
		LargeL = Label(root, text= "Anchor of the drawers:")
		LargeL.place(x=10, y = 480, width = 480, height = 30)
		LargeEntL = Entry(root)
		LargeEntL.place(x=410, y = 480, width = 70, height = 30)
		#Color
		ColL = Label(root, text= "Color of the legs (red...):")
		ColL.place(x=10, y = 520, width = 480, height = 30)
		ColEntL = Entry(root)
		ColEntL.place(x=410, y = 520, width = 70, height = 30)
		
		#Create button
		but = Button(root, text ="Generate model", command=clicked)
		but.place(x=330,y=560,width=160,height=30)
		#CLOSE WINDOW
		self.button_rename = tk.Button(self.root, text = "Back", command= lambda: self.root.destroy()).place(x = 10, y = 560, width = 110, height = 30)


####################################################################################################################################################################
#CREATION OF THE ONE LEG TABLE

class OneLegTable:
	def __init__(self, root):

		self.root = root
		self.root.geometry("500x1010")
		self.root["bg"] = "white"

		def clicked():

							
			Thk = 0
			alt = 0
			WLeg = 0
			HLeg = 0
			RLeg = 0
			HTab = 0
			WTab = 0
			RTab = 0
			siz = 0
			rad = 0
			#capture thickness
			try:
				Thk = int(ThicknessEnt.get())
			except:
				tkMessageBox.showinfo("Error", "Table model needs a thickness")
				return

			#Square or round table
			if sq.instate(['selected']) and not ro.instate(['selected']):
				#Create squared table
				try:
					WTab = int(anchEnt.get())
					HTab = int(LargeEnt.get())
				except:
					tkMessageBox.showinfo("Error", "Anchor or weight inputs are wrong or missing")
				#Tab = ops.Cube([WTab, HTab, Thk])
				Pos = [-int(WTab/2), -int(HTab/2)]
				TabSz = [WTab, HTab, Thk]
			elif not sq.instate(['selected']) and ro.instate(['selected']):
				#Create Round table
				try:
					RTab = int(RadEnt.get())
				except: 
					tkMessageBox.showinfo("Error", "Error on radius of the table input")
				#Tab = ops.Cylinder(h = Thk, r = RTab)
				Pos = [RTab, RTab]
				TabSz = [Thk, RTab]
			else:
				tkMessageBox.showinfo("Error", "cant genenerate, 0 or 2 checkboxes of table checked")
			
			#LEGS
			#get altura of legs at the table and pos the table in the space
			try:
				alt = int(AltEntL.get())
				Pos.append(alt)
				
			except:
				tkMessageBox.showinfo("Error", "Altura value invalid")

			#Square or round legs
			if sqL.instate(['selected']) and not roL.instate(['selected']):
				#Create squared legs
				try:
					WLeg = int(anchEntL.get())
					HLeg = int(LargeEntL.get())
				except:
					tkMessageBox.showinfo("Error", "Anchor or weight inputs are wrong or missing")
				LegSz = [WLeg, HLeg, alt]

				
			elif not sqL.instate(['selected']) and roL.instate(['selected']):
				#Create Round legs
				try:
					RLeg = int(RadEntL.get())
				except: 
					tkMessageBox.showinfo("Error", "Error on radius of the legs input")
				LegSz = [alt, RLeg]
			else:
				tkMessageBox.showinfo("Error", "cant genenerate, 0 or 2 checkboxes of legs checked")
			


			#CREATE THE OBJECTS


			#CREATE THE TABLE
			if sq.instate(['selected']) and not ro.instate(['selected']):
				
				try:
					Tab = ops.Cube(TabSz).color(str(ColEnt.get())).translate(Pos)
				except:
					tkMessageBox.showinfo("Error", "invalid color for table")
					return

			elif not sq.instate(['selected']) and ro.instate(['selected']):
				
				try:
					Tab = ops.Cylinder(h=Thk,r=RTab).color(str(ColEnt.get())).translate([0,0,alt])
				except:
					tkMessageBox.showinfo("Error", "invalid color for table")
					return	
			ListOfObjects = [Tab]
			#CREATE THE LEG
			x = LegSz[0]
			y = LegSz[1]
			if sqL.instate(['selected']) and not roL.instate(['selected']):

				try:
					
					Leg1 = ops.Cube(LegSz).color(str(ColEntL.get())).translate([-x/2,-y/2,0])

						
				except:
					tkMessageBox.showinfo("Error", "invalid color for legs")
					return

			elif not sqL.instate(['selected']) and roL.instate(['selected']):
				
				try:

					Leg1 = ops.Cylinder(h=x,r=y).color(str(ColEntL.get()))

				except:
					tkMessageBox.showinfo("Error", "invalid color for leg")
					return
			ListOfObjects.append(Leg1)

			try:
				thkB = int(TBas.get())
			except:
				pass
			if BaseC.instate(['selected']) and not BaseR.instate(['selected']):
			
				siz = int(SBas.get())
				Base = ops.Cube([siz, siz, thkB]).color(str(ColEntL.get())).translate([-siz/2,-siz/2,0])
					
			
		
			elif not BaseC.instate(['selected']) and BaseR.instate(['selected']):
			
				rad = int(RBasEnt.get())
				Base = ops.Cylinder(h=thkB,r=rad).color(str(ColEntL.get()))

			else:
				tkMessageBox.showinfo("Warning", "Form of base not selected, the model will dont have base")
				Base = ops.Cube([0,0,0])	

			#check all the parameters are okey
			if Thk <= 0 or alt <= 0 or ((WLeg <= 0 or HLeg <= 0) and sqL.instate(['selected'])) or (RLeg <= 0 and roL.instate(['selected'])) or (sq.instate(['selected']) and (HTab <= 0 or WTab <= 0)) or (ro.instate(['selected']) and RTab <= 0) or (BaseC.instate(['selected']) and siz <= 0) or (BaseR.instate(['selected']) and rad <= 0) or (HTab < RLeg) or (WTab < WLeg * 2) or (HTab < HLeg * 2):
				tkMessageBox.showinfo("Error", "some used parameters are negative, zero, or have conflict with other parameters")
				return
			else:
				ListOfObjects.append(Base)
				self.new = Toplevel(self.root)
				creation(self.new,ListOfObjects)
			#saveWindow = creation(root, ListOfObjects)


			
		#"Table" Label
		Table = Label(root, text= "Table")
		Table.place(x = 10, y = 10,width = 480, height = 30)
		#INFO
		Inf = Label(root, text = "If you check Square, radius will be ignored\nIf you check Square, anchor and large will be ignored")
		Inf.place(x = 10, y = 40,width = 480, height = 60)
		#Round or square
		sq = tk.Checkbutton(root, text = "Square")
		sq.place(x=10, y = 110, width = 480, height = 30)
		sq.state(['!alternate'])
		sq.state(['selected'])
		ro = tk.Checkbutton(root, text = "Round")
		ro.place(x=10, y = 150, width = 480, height = 30)
		ro.state(['!alternate'])
		ro.state(['!selected'])

		#Large 
		anchor = Label(root, text= "Large of the table:")
		anchor.place(x=10, y = 190, width = 480, height = 30)
		anchEnt = Entry(root)
		anchEnt.place(x=410, y = 190, width = 70, height = 30)
		#Anchor
		Large = Label(root, text= "anchor of the table:")
		Large.place(x=10, y = 230, width = 480, height = 30)
		LargeEnt = Entry(root)
		LargeEnt.place(x=410, y = 230, width = 70, height = 30)
		#Thickness
		Thick = Label(root, text= "Thickness of the table:")
		Thick.place(x=10, y = 270, width = 480, height = 30)
		ThicknessEnt = Entry(root)
		ThicknessEnt.place(x=410, y = 270, width = 70, height = 30)
		#Radius
		Radius = Label(root, text= "Radius of the table:")
		Radius.place(x=10, y = 310, width = 480, height = 30)
		RadEnt = Entry(root)
		RadEnt.place(x=410, y = 310, width = 70, height = 30)
		#Color
		Col = Label(root, text= "Color of the table (red, blue, ...):")
		Col.place(x=10, y = 350, width = 480, height = 30)
		ColEnt = Entry(root)
		ColEnt.place(x=410, y = 350, width = 70, height = 30)
		#Separator
		separator = Label(root, text= ".")
		separator.place(x = 10, y = 390,width = 480, height = 1)
		#"Legs" Label
		Table = Label(root, text= "Leg")
		Table.place(x = 10, y = 400,width = 480, height = 30)
		#Round or square Table
		sqL = tk.Checkbutton(root, text = "Square")
		sqL.place(x=10, y = 440, width = 480, height = 30)
		sqL.state(['!alternate'])
		sqL.state(['selected'])
		roL = tk.Checkbutton(root, text = "Round")
		roL.place(x=10, y = 480, width = 480, height = 30)
		roL.state(['!alternate'])
		roL.state(['!selected'])
		#Large Leg
		anchorL = Label(root, text= "Large of the leg:")
		anchorL.place(x=10, y = 520, width = 480, height = 30)
		anchEntL = Entry(root)
		anchEntL.place(x=410, y = 520, width = 70, height = 30)
		#Anchor Leg
		LargeL = Label(root, text= "Anchor of the leg:")
		LargeL.place(x=10, y = 560, width = 480, height = 30)
		LargeEntL = Entry(root)
		LargeEntL.place(x=410, y = 560, width = 70, height = 30)
		#Radius Leg
		RadiusL = Label(root, text= "Radius of the leg:")
		RadiusL.place(x=10, y = 600, width = 480, height = 30)
		RadEntL = Entry(root)
		RadEntL.place(x=410, y = 600, width = 70, height = 30)
		#height Leg
		AltL = Label(root, text= "height of the leg:")
		AltL.place(x=10, y = 640, width = 480, height = 30)
		AltEntL = Entry(root)
		AltEntL.place(x=410, y = 640, width = 70, height = 30)
		#Color
		ColL = Label(root, text= "Color of the legs (red...):")
		ColL.place(x=10, y = 680, width = 480, height = 30)
		ColEntL = Entry(root)
		ColEntL.place(x=410, y = 680, width = 70, height = 30)
		#Separator
		separator = Label(root, text= ".")
		separator.place(x = 10, y = 720,width = 480, height = 1)
		#"Legs" Label
		another = Label(root, text= "Base")
		another.place(x = 10, y = 730,width = 480, height = 30)
		#Round or square Table
		BaseC = tk.Checkbutton(root, text = "Square")
		BaseC.place(x=10, y = 770, width = 480, height = 30)
		BaseC.state(['!alternate'])
		#BaseC.state(['selected'])
		BaseR = tk.Checkbutton(root, text = "Round")
		BaseR.place(x=10, y = 810, width = 480, height = 30)
		BaseR.state(['!alternate'])
		#BaseC.state(['!selected'])
		#Radius of the base
		RBas = Label(root, text = "Radius of the base")
		RBas.place(x = 10, y = 850,width = 480, height = 30)
		RBasEnt = Entry(root)
		RBasEnt.place(x=410, y = 850, width = 70, height = 30)
		#size of the base
		SBas = Label(root, text = "size of the base")
		SBas.place(x = 10, y = 890,width = 480, height = 30)
		SBas = Entry(root)
		SBas.place(x=410, y = 890, width = 70, height = 30)
		#thickness of the base
		TBas = Label(root, text = "thickness of the base")
		TBas.place(x = 10, y = 930,width = 480, height = 30)
		TBas = Entry(root)
		TBas.place(x=410, y = 930, width = 70, height = 30)
		
		
		#Create button
		but = Button(root, text ="Generate model", command=clicked)
		but.place(x=330,y=970,width=160,height=30)
		#CLOSE WINDOW
		self.button_rename = tk.Button(self.root, text = "Back", command= lambda: self.root.destroy()).place(x = 10, y = 970, width = 110, height = 30)

####################################################################################################################################################################
#RUN MAIN APP

if __name__ == "__main__":
	#RUN MAIN
    root = Tk()
    app = Win(root)
    app.root.title("Parametric modeler")
    root.mainloop()
