# LinkedView

A [Fiji/ImageJ](https://imagej.net/Fiji) plugin for intuitive visualisation and shared annotation of correlative image datasets. Users can interactively explore matching regions in correlative images, annotate these images and transfer annotations between imaging modalities. The annotated regions can be saved individually.

## Demo

This video shows how to install and run LinkedView, and demonstrates how LinkedView helps you explore correlative image datasets. 

## Installation

Download [Fiji/ImageJ](https://imagej.net/Fiji/Downloads). Download this repository and place LinkedView_.py into your Fiji plugins folder. Restart Fiji and LinkedView will be in the Plugins menu of your Fiji/ImageJ installation.

## Preparing your images

Any images supported in Fiji/ImageJ can be used with LinkedView. Please ensure that pixel/voxel sizes are set to physical units and that there are no significant deformations between images. Image deformations can be corrected by registration. Here is a (non-exhaustive) list of examples of software for you to do this:

* [Elastix](https://elastix.lumc.nl/) - if you're comfortable with scripting
* [BigWarp](https://imagej.net/BigWarp) - manual landmark based registration
* [bUnwarpJ](https://imagej.net/BUnwarpJ)
* [Correlia](https://onlinelibrary.wiley.com/doi/full/10.1111/jmi.12928)
* [List of Python projects for image registration](http://pyimreg.github.io/) - if you're a Python user

## Running LinkedView

Once your images are open in Fiji, start LinkedView by clicking on LinkedView in the Plugins menu. Some error messages may show up in the console but these can be ignored. The LinkedView menu will appear.

#### Link Views

This button matches the displayed regions in all images.

#### Update reference image

LinkedView matches all images to the displayed region of the reference image. 

#### Export Views

Export views screenshots each open image in its current view, including any selected regions. Please ensure that there are no other windows on the screen area covered by the images, as these will be included in the screenshot. Screenshots will be saved in the same directory as your images, under the LV_export/<date>_<time> folder. The export directory is printed in the Log window.
  
#### Export cropped ROIs

Export cropped ROIs saves the image data in each selection at its native resolution. If the image is a stack, only the selection in the current slice will be saved. The locations of these ROIs are also saved which can be imported into ROI Manager later.

#### Transferring annotations between images

Use [Sync Windows](https://imagej.net/Sync_Windows) to annotate all images at once. Run Sync Windows by clicking Analyze > Tools > Sync Windows, ensure that all the checkboxes are ticked and click Synchronize All. 

## Support

Report bugs and request features by raising an issue on the [issue tracker](https://github.com/elainehoml/LinkedView/issues).

## Cite us

This work was supported by the Engineering and Physical Sciences Research Council (EPSRC), UK and the Institute for Life Sciences, University of Southampton, UK.

If you found this helpful, please cite us:
