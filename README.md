# LinkedView

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3996281.svg)](https://doi.org/10.5281/zenodo.3996281)

A [Fiji/ImageJ](https://imagej.net/Fiji) plugin for intuitive visualisation and shared annotation of correlative image datasets. Users can interactively explore matching regions in correlative images, annotate these images and transfer annotations between imaging modalities. The annotated regions can be saved individually.

## Demo

This video shows how to install and run LinkedView, and demonstrates how LinkedView helps you explore correlative image datasets.

[![LinkedView Demo Video](LinkedView_Demo_Thumbnail.JPG)](https://youtu.be/zJYk_rE0DdI "LinkedView Demo")

## Installation

Download [Fiji/ImageJ](https://imagej.net/Fiji/Downloads). Download this repository and place LinkedView_.py into your Fiji plugins folder. LinkedView_.py can be found in the ```main/``` directory. Restart Fiji and LinkedView will be in the Plugins menu of your Fiji/ImageJ installation.

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

Report bugs and request features by raising an issue on the [issue tracker](https://github.com/elainehoml/LinkedView/issues). This version of LinkedView (19-Aug-2020) was tested on (Fiji Is Just) ImageJ 2.0.0-rc-69/1.53c.

## Cite us

This work was supported by the Engineering and Physical Sciences Research Council (EPSRC), UK and the Institute for Life Sciences, University of Southampton, UK.

If you found this helpful, please cite us:

Elaine M. L. Ho, Orestis L. Katsamenis, Gareth J. Thomas, Peter M. Lackie, & Philipp Schneider. (2020, August 22). LinkedView: A Fiji/ImageJ Plugin for Visualisation and Annotation of Correlative Images (Version v1.0.0-alpha). Zenodo. http://doi.org/10.5281/zenodo.3996281

## Notes

#### 28th Aug 2020: Installation not working?

If LinkedView does not run on your version of Fiji, please raise an issue on the [issue tracker](https://github.com/elainehoml/LinkedView/issues). Alternatively, for a 'plug-and-play' experience you can download [this LinkedView release](https://github.com/elainehoml/LinkedView/releases/tag/v1.0.1-alpha) which comes with Fiji (for Windows) with LinkedView pre-installed under 'Plugins'.

#### 28th Aug 2020: Console errors when running LinkedView

The error "console: Failed to install '': java.nio.charset.UnsupportedCharsetException: cp0." appears after running LinkedView (it is a Jython script), but LinkedView still works. You can ignore this error message. If you would like to stop it entirely, modify/create the file jvm.cfg in the same directory as the Fiji launcher and adding the following:
``` -Dpython.console.encoding=UTF-8 ```

References: [This Github issue](https://github.com/StuartLab/MiNA/issues/13) and [this image.sc forum post](https://forum.image.sc/t/script-editor-error-when-working-with-python-scripts/5893)

Thanks to OLK for sorting this!
