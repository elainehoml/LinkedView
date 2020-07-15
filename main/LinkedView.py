import os, time
from ij import IJ, ImagePlus
from ij import WindowManager as WM
from ij.gui import ImageCanvas, GenericDialog
from javax.swing import JFrame, JButton
from java.awt import GridLayout

class Image():
	""" Class for images to link views
	
	Attributes
	----------
	imp : ImagePlus
		ImagePlus for image to link views
	title : str
		Title of image given by imp.getTitle()
	ID : int
		Unique numeric ID assigned to this imp
	canvas : ImageCanvas
		ImageCanvas for image
	
	"""
	def __init__(self, imp):
		self.imp = imp
		self.title = self.imp.getTitle()
		self.ID = self.imp.getID()
		self.canvas = self.imp.getCanvas()
		IJ.log("Loaded image " + self.imp.getTitle())

	def getView(self):
		""" Gets source rectangle of current view from ImageCanvas """
		return self.canvas.getSrcRect() # java.awt.Rectangle object
	
	def updateView(self, target):
		""" Sets display to target src_rect

		Parameters
		----------
		target : java.awt.Rectangle
			Rectangle (height, width, x, y) to display. x and y are coordinates of
			upper-left corner of the Rectangle

		"""
		self.canvas.setSourceRect(target)
		self.imp.updateAndDraw()

class LinkedView():
	""" Class for tasks to link displays of Image instances

	Attributes
	----------
	active_IDs : list
		List of IDs for current image windows
	Images : dict
		Dictionary of Image instances created from all open image windows, key
		value pairs are {ID:Image instances}. Call a specific Image instance by 
		Images[ID], where ID is the unique image identifier for each ImagePlus.
	target_image : Image
		Image instance used as target display, i.e. all other Image instances
		will be matched to the same source rect as this target_image.	

	"""
	def __init__(self):
		self.active_IDs = WM.getIDList()
		if self.active_IDs is None:
			IJ.error("Error", "No images imported")
		if len(self.active_IDs) < 2:
			IJ.error("Error", "Must have at least two images open")
		self.Images = {ID:Image(WM.getImage(ID)) for ID in self.active_IDs} # create Images
		self.target_image = self.Images.values()[0] # by default, target image is first image

	def checkImages(self):
		""" Raise error if images have changed """
		current_active_IDs = WM.getIDList()
		if self.active_IDs != current_active_IDs:
			IJ.error("Change of images", "Active images have changed, please restart LinkedView")
		else:
			pass

	def getTarget(self, event):
		""" Dialog to update target image attribute when get_target button is pressed """
		self.checkImages()
		gd = GenericDialog("Choose a target image")
		gd.addChoice("Target image", 
			[Image.title for Image in self.Images.values()],
			self.Images.values()[0].title) # add all Image instances to a drop-down list
		gd.showDialog()
		target_image_name = gd.getNextChoice()
		target_image_ID = WM.getImage(target_image_name).getID()
		self.target_image = self.Images[target_image_ID] # update target_image attribute
		IJ.log("Target image is " + self.target_image.title)

	def linkView(self, event):
		""" 
		Match all Image instances to target image source rect when link_view button
		is pressed
		"""
		self.checkImages()
		target_src_rect = self.target_image.getView() # java.awt.Rectangle object
		for Image in self.Images.values(): # updates all Image instances
			Image.updateView(target_src_rect)

	def UI(self):
		""" User interface for LinkedView """
		frame = JFrame("LinkedView")
		frame.setSize(300,100)
		frame.setLayout(GridLayout(2,1))
		link_view = JButton("Link Views", actionPerformed = self.linkView)
		get_target = JButton("Update Target Image", actionPerformed = self.getTarget)
		frame.add(link_view)
		frame.add(get_target)
		frame.setVisible(True)

launch = LinkedView()
launch.UI()
