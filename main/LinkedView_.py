import os, time, datetime
from ij import IJ, ImagePlus
from ij import WindowManager as WM
from ij.gui import ImageCanvas, GenericDialog
from ij.io import FileSaver
from ij.plugin import ScreenGrabber
from ij.plugin.frame import RoiManager as RM
from javax.swing import JFrame, JButton
from java.awt import GridLayout, Rectangle, Dimension

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
	window : ImageWindow
		ImageWindow for image
	
	"""
	def __init__(self, imp):
		self.imp = imp
		self.title = self.imp.getTitle()
		self.ID = self.imp.getID()
		self.canvas = self.imp.getCanvas()
		self.window = self.imp.getWindow()
		self.calibration = self.imp.getCalibration()
		self.units = self.calibration.getUnit()
		IJ.log("Loaded image " + self.imp.getTitle())

	def getWindowSize(self):
		""" Gets window size in pixel units of current window from ImageWindow """
		return self.window.getSize()

	def matchWindowSizes(self, ref_window_size):
		""" Matches window dimensions to the reference image

		Parameters
		----------
		ref_window_size : list
			Dimension [width, height] of ImageWindow to resize to in physical units
		
		"""
		self.window.setSize(ref_window_size)

	def getViewPhysicalUnits(self):
		""" Gets source rectangle in physical units 

		Returns
		-------
		list
			Contains x, y, width, height as doubles
		"""
		height = self.calibration.getY(self.canvas.getSrcRect().height)
		width = self.calibration.getX(self.canvas.getSrcRect().width)
		x = self.calibration.getX(self.canvas.getSrcRect().x)
		y = self.calibration.getY(self.canvas.getSrcRect().y)
		return [x, y, width, height]

	def transformRefView(self, ref):
		""" Transforms ref src_rect from physical units to pixels 
		
		Parameters
		----------
		ref : list
			Rectangle (x, y, width, height) to display. x and y are coordinates of
			upper-left corner of the Rectangle. ref is in physical units.
			
		"""
		x = int(self.calibration.getRawX(ref[0]))
		y = int(self.calibration.getRawY(ref[1]))
		width = int(self.calibration.getRawX(ref[2]))
		height = int(self.calibration.getRawY(ref[3]))

		return Rectangle(x, y, width, height)
	
	def updateView(self, ref):
		""" Sets display to ref src_rect

		Parameters
		----------
		ref : list
			Rectangle (x, y, width, height) to display. x and y are coordinates of
			upper-left corner of the Rectangle. ref is in physical units.

		"""
		ref_px_units = self.transformRefView(ref)
		self.canvas.setSourceRect(ref_px_units)
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
	ref_image : Image
		Image instance used as ref display, i.e. all other Image instances
		will be matched to the same source rect as this ref_image.	

	"""
	def __init__(self):
		self.active_IDs = WM.getIDList()
		if self.active_IDs is None:
			IJ.error("Error", "No images imported")
		if len(self.active_IDs) < 2:
			IJ.error("Error", "Must have at least two images open")
		self.Images = {ID:Image(WM.getImage(ID)) for ID in self.active_IDs} # create Images
		self.ref_image = self.Images.values()[0] # by default, ref image is first image

	def checkImages(self):
		""" Raise error if images have changed """
		current_active_IDs = WM.getIDList()
		if self.active_IDs != current_active_IDs:
			IJ.error("Change of images", "Active images have changed, please restart LinkedView")
		else:
			pass

	def getRef(self, event):
		""" Dialog to update ref image attribute when get_ref button is pressed """
		self.checkImages()
		gd = GenericDialog("Choose a reference image")
		gd.addChoice("Reference image", 
			[Image.title for Image in self.Images.values()],
			self.Images.values()[0].title) # add all Image instances to a drop-down list
		gd.showDialog()
		ref_image_name = gd.getNextChoice()
		ref_image_ID = WM.getImage(ref_image_name).getID()
		self.ref_image = self.Images[ref_image_ID] # update ref_image attribute
		IJ.log("Reference image is " + self.ref_image.title)

	def linkView(self, event):
		""" 
		Match all Image instances to ref image source rect when link_view button
		is pressed
		"""
		self.checkImages()
		ref_window_size = self.ref_image.getWindowSize() # [width, height] in physical units
		ref_src_rect = self.ref_image.getViewPhysicalUnits() # java.awt.Rectangle object
		for Image in self.Images.values(): # updates all Image instances
			Image.updateView(ref_src_rect)
			Image.matchWindowSizes(ref_window_size)

	def createExportDir(self, export_name):
		""" Creates export directory 

		Parameters
		----------
		export_name : str
			Name of folder. i.e. <img directory>/<export_name>

		Returns
		-------
		current_export_dir : str, path-like
			Path to export directory <img_directory>/<export_name>/<current_datetime>
			
		"""
		IJ.selectWindow(self.ref_image.ID) # make ref image active window
		current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M")
		export_dir = os.path.join(IJ.getDir("image"), export_name)
		if os.path.isdir(export_dir) == False:
			IJ.log("Created export directory: " + export_dir)
			os.mkdir(export_dir)
		current_export_dir = os.path.join(export_dir, current_datetime)
		os.mkdir(current_export_dir)
		IJ.log("Currently exporting to: " + current_export_dir)

		return current_export_dir
	
	def exportView(self, event):
		""" Export current view of all images as individual tiffs when 
		export_view button is pressed

		1. Export directory is created in same dir as ref image
		2. Folder created for specific time
		3. ScreenGrabber returns current views of all images to be saved

		These images can be loaded into FigureJ for figure making
		"""
		# Create export dir, if not already present
		current_export_dir = self.createExportDir("LV_export")

		# Save image
		for Image in self.Images.values(): # for all Image instances
			IJ.selectWindow(Image.ID)
			screengrab = ScreenGrabber().captureImage()
			filename = os.path.join(current_export_dir, Image.title)
			if os.path.splitext(filename)[1] != ".tif":
				os.path.join(filename, ".tif")
			FileSaver(screengrab).saveAsTiff(filename)
			IJ.log("Image saved: " + os.path.join(current_export_dir, Image.title))

	def saveCroppedROIs(self, event):
		""" Duplicates cropped ROIs and saves """
		# Create export dir, if not already present
		current_export_dir = self.createExportDir("Cropped_ROI")
		
		for Image in self.Images.values(): # for all Image instances
			# save image
			cropped_copy = Image.imp.crop() # returns cropped image as an imp
			img_filename = os.path.join(current_export_dir, Image.title)
			if os.path.splitext(img_filename)[1] != ".tif":
				os.path.join(img_filename, ".tif")
			FileSaver(cropped_copy).saveAsTiff(img_filename)

			# save roi
			roi_filename = os.path.splitext(img_filename)[0] + "_roi.roi"
			roi = Image.imp.getRoi()
			if roi != None:
				rm = RM.getInstance()
				if rm == None:
					rm = RM()
				rm.addRoi(roi)
				rm.runCommand("Save", roi_filename) # which one does it save
				rm.runCommand("Delete")
			IJ.log("Cropped ROI saved: " + os.path.join(current_export_dir, Image.title))
	
	def UI(self):
		""" User interface for LinkedView """
		frame = JFrame("LinkedView")
		frame.setSize(300,200)
		frame.setLayout(GridLayout(4,1))
		link_view = JButton("Link Views", actionPerformed = self.linkView)
		get_ref = JButton("Update Reference Image", actionPerformed = self.getRef)
		export_view = JButton("Export Views", actionPerformed = self.exportView)
		crop_ROIs = JButton("Export Cropped ROIs", actionPerformed = self.saveCroppedROIs)
		frame.add(link_view)
		frame.add(get_ref)
		frame.add(export_view)
		frame.add(crop_ROIs)
		frame.setVisible(True)

launch = LinkedView()
launch.UI()
