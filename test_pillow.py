from __future__ import print_function
import glob, os
# from PIL import Image, ImageDraw

# for infile in glob.glob("*.png"):
# 	filename, extension = os.path.splitext(infile)
# 	im = Image.open(filename + ".png")
# 	# print(im.format, im.size, im.mode)
# 	# im = im.rotate(90)
# 	# print(im.format, im.size, im.mode)
# 	# im.show()
# 	# im.save(filename + "_rot" + ".png")

# 	draw = ImageDraw.Draw(im)
# 	draw.line((0, 0) + im.size, fill=128)
# 	draw.line((0, im.size[1], im.size[0], 0), fill=128)
# 	del draw

# 	im.save(filename + "_cross" + ".png")
	
# ------------------------------------------------------------

# from PIL import Image, ImageMath

# im1 = Image.open("stealth_base.png")
# im2 = Image.open("stealth_base_rot.png")

# # im1.show()
# # im1 = im1.convert(mode='1', dither=127)
# # im1.show()

# modes = ['1','L','P','RGB','RGBA','CMYK','YCbCr','HSV','I','F',]
# # modes = ['1','L','P','RGB','RGBA','CMYK','YCbCr','LAB','HSV','I','F',]

# for mode in modes:
# 	im1.convert(mode=mode, dither=127).show()

# ------------------------------------------------------------
from PIL import Image, ImageFilter
import glob, os

compression = 32

def paintToColor(image, color):
	source = image.split()
	print(source)

	R, G, B, A = 0, 1, 2, 3

	# select regions where red is less than 100
	mask = source[A].point(lambda i: i > 127 and 255)

	# process the green band
	source[R].paste(source[R].point(lambda i: color), None, mask)
	source[G].paste(source[G].point(lambda i: color), None, mask)
	source[B].paste(source[B].point(lambda i: color), None, mask)
	source[A].paste(source[A].point(lambda i: 255), None, mask)

	# build a new multiband image
	return Image.merge(im.mode, source)

def roundUpTransparency(image):
	source = image.split()
	print(source)

	R, G, B, A = 0, 1, 2, 3

	# select regions where red is less than 100
	mask = source[A].point(lambda i: i < 200 and 255)

	# process the green band
	source[R].paste(source[R].point(lambda i: 0), None, mask)
	source[G].paste(source[G].point(lambda i: 0), None, mask)
	source[B].paste(source[B].point(lambda i: 0), None, mask)
	source[A].paste(source[A].point(lambda i: 0), None, mask)

	# build a new multiband image
	return Image.merge(im.mode, source)

def quantizeAndSave(img, power):
	imq = img.quantize(16)
	imq.save(filename + "_quantized_" + str(power) + extension, "PNG")

for infile in glob.glob("stealth_base.png"):
# for infile in glob.glob("*.png"):
	filename, extension = os.path.splitext(infile)

	im = Image.open(filename + extension)

	# for x in range(1, 5):
		# quantizeAndSave(im, 2**x)

	# im = roundUpTransparency(im)
	# im.save("stealth_base_roundupped.png", "PNG")

	base = im.copy()
	im = im.filter(ImageFilter.GaussianBlur(radius=16))

	start_size = im.size
	tmp_size_list = list(start_size)
	box = (compression, compression, tmp_size_list[0], tmp_size_list[1])
	shifted_box = (compression / 2, compression / 2, 
		tmp_size_list[0] - compression / 2, tmp_size_list[1] - compression / 2)
	tmp_size_list[0] /= compression
	tmp_size_list[1] /= compression
	compressed_size = tuple(tmp_size_list)
	print (box, shifted_box)
	print (compressed_size)

	# print (im.getbbox())
	im = im.resize(compressed_size, Image.NEAREST)

	im = im.filter(ImageFilter.GaussianBlur(radius=1))
	im = roundUpTransparency(im)
	im = paintToColor(im, 255)

	im = im.convert(mode='1')
	print (repr(im.tobytes()))
	print (repr(im.tostring()))
	print (repr(im.tobitmap()))
	
	
	im = im.resize(start_size)
	# im = im.convert(mode='LA')
	# im = im.convert(mode='RGBA')

	# im.save(filename + "_mask" + "." + extension, "PNG")
	region = im.crop(box)
	im.paste(region, shifted_box)

	# im2 = Image.blend(im, base, 0.5)
	im2 = Image.alpha_composite(base, im)


	# im.save("stealth_base_mask2.png", "PNG")

	im2.save(filename + "_masked" + extension, "PNG")
	# im2.save("stealth_base_masked.png", "PNG")
# ------------------------------------------------------------


        # 1 (1-bit pixels, black and white, stored with one pixel per byte)
        # L (8-bit pixels, black and white)
        # P (8-bit pixels, mapped to any other mode using a color palette)
        # RGB (3x8-bit pixels, true color)
        # RGBA (4x8-bit pixels, true color with transparency mask)
        # CMYK (4x8-bit pixels, color separation)
        # YCbCr (3x8-bit pixels, color video format)
        # LAB (3x8-bit pixels, the L*a*b color space)
        # HSV (3x8-bit pixels, Hue, Saturation, Value color space)
        # I (32-bit signed integer pixels)
        # F (32-bit floating point pixels)


# im2 = im2.convert('L')

# out = ImageMath.eval("convert(min(a, b), 'L')", a=im1, b=im2)
# out.save("result.png")


# # im.rotate(90).show()

# from PIL import Image, ImageDraw

# im = Image.open("hopper.jpg")

# draw = ImageDraw.Draw(im)
# draw.line((0, 0) + im.size, fill=128)
# draw.line((0, im.size[1], im.size[0], 0), fill=128)
# del draw

# # write to stdout
# im.save(sys.stdout, "PNG")