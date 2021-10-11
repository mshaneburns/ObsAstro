[Home](index.md) | Resources

------

## Learning Python
All of the code and tutorials on this site assume you are at least somewhat familiar with Python programming. If you've taking beginning programing course in Python you will be well prepared to start the tutorials. If you need to learn Python before starting there are a vast number of online resources. Here's a list of a few free ones that I have found to be useful:

- [How to Think Like a Computer Scientist: Learning with Python 3](http://openbookproject.net/thinkcs/python/english3e/) is a very good introduction to learning programming using Python. 
- [Scientific Computing Toolbox](https://faculty1.coloradocollege.edu/~sburns/toolbox/index.html) is an elementary introduction to Python with special emphasis on software tools useful to science students.
- [Practical Python for Astronomers](https://python4astronomers.github.io/index.html) is a series of hands-on workshops with and emphasis on using Python to solve real-world problems that astronomers are likely to encounter in research.
- [Python for Astronomers](https://prappleizer.github.io) is a free textbook and set of interactive tutorials for learning scientific computing. It is intended for students and researchers just starting out with coding in an astrophysical research context.  

## Astronomical image processing systems
Here is a short list of some of the astronomical image processing systems currently used by astronomers. 

- [Astropy Project](https://www.astropy.org): The Astropy Project is a community effort by professional astronomers to develop a common set of core Python packages for use in astronomy. The image processing code and tutorials on this site use several Astropy modules.</dd>
- [AstroConda](https://astroconda.readthedocs.io/en/latest/): AstroConda is a collection of software packages maintained by the [Space Telescope Science Institute](https://www.stsci.edu) (STScI). Astroconda provides tools and utilities required to process and analyze data from the Hubble Space Telescope (HST), James Webb Space Telescope (JWST), and others.
- [Image Reduction and Analysis Facility](http://ast.noao.edu/data/software) (IRAF): IRAF is an extensive collection of software written at the [National Optical Astronomy Observatories](http://ast.noao.edu) (NOAO) and until recently was the most widely used image processing system used by professional astronomers. NOAO discontinued the development and maintenance of IRAF in 2013. The easiest way to install IRAF is probably to use [Astroconda](https://astroconda.readthedocs.io/en/latest/installation.html#iraf-install).


## Image display
You can always display an image from Python using the matplotlib function [`imshow()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html). The Jupyter Notebook tutorials on this site include examples of ways to use `imshow()`. However, in many cases `imshow()` is awkward to use. You will often find it easier to use a dedicated image display program. One of the best dedicated image display programs is [SAOImageDS9](https://sites.google.com/cfa.harvard.edu/saoimageds9/home). DS9 is a stand-alone application that runs on MacOS, Linux, and Windows operating systems. It opens and displays FITS images and supports many advanced features. DS9 allows you to easily change color maps, change the display scaling, zoom, rotate and crop images. You can even [make true color images from as set of RGB images](https://ds9.si.edu/doc/user/rgb/index.html).

