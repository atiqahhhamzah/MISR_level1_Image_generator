# MISR_level1_Image_generator

<b>Introduction</b>
<p>
This is a pretty simple image generator that will generate any image for any level 1 MISR hdf file regardless of resolution (since it'll check for that). This is written for hdf4 files and uses the pyhdf API which you can get from the hdfeos website.
I've listed which python libraries I am using under libraries and you can just install those libraries using pip or conda if you don't have them and it should work. It's a little slow if you stitch many images together and does take a lot of computing resources, so take heed of that.
</p>
<b>Operation</b>
<p>
Run "python lvl1_image_gen.py MISR_HDF_Filename.hdf image_name.jpeg"
</p>

<b>Libraries</b>
<p>PIL<br>pyhdf<br>numpy<br>colour</p>


