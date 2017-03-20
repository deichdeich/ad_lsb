"""
Author: Alex Deich
Date: March 2017

ad_lsb.py:  This is a simple implementation of Least Significant Bit steganography.
"""
from __future__ import division, print_function
import numpy as np
from PIL import Image
import binascii


def str_to_bin(in_str):
    out = bin(int(binascii.hexlify(in_str), 16))
    return(out[2:])
    
def bin_to_str(in_bin):
    in_bin = int(in_bin, 2)
    return(binascii.unhexlify('%x' % in_bin))

def get_binary_pixel_vals(img_path):
    im = Image.open(img_path)
    pix = im.load()
    x,y = im.size
    image_array = np.zeros((x,y,3))
    for i in xrange(x):
        for j in xrange(y):
            for k in xrange(3):
                image_array[i,j,k] = bin(pix[i,j][k])[2:]
    return(image_array, x, y)

def insert_message(message, img_path, fname = ""):
    message += '999'
    bin_image, x, y = get_binary_pixel_vals(img_path)
    bin_message = str_to_bin(message)
    new_image = Image.new('RGB', (x,y), 'black')
    new_pixels = new_image.load()
    inx = 0
    for i in xrange(x):
        for j in xrange(y):
            for k in xrange(3):
                if inx >= len(bin_message):
                    break
                n = list(str(int(bin_image[i,j,k])))
                n[-1] = bin_message[inx]
                bin_image[i,j,k] = int("".join(n))
                inx += 1

            new_pixels[i,j] = (int(str(int(bin_image[i,j,0])), 2),
                               int(str(int(bin_image[i,j,1])), 2),
                               int(str(int(bin_image[i,j,2])), 2))
    if fname == "":
        fname = img_path[:-4] + "_encoded" + img_path[-4:]

    new_image.save(fname)
    print("Message encoded in image titled {}".format(fname))
    return()

def retrieve_message(img_path):
    bin_image, x, y = get_binary_pixel_vals(img_path)
    out_bin = ''
    for i in xrange(x):
        if len(out_bin) >= 22 and out_bin[-22:] == '1110010011100100111001':
            break
        for j in xrange(y):
            if len(out_bin) >= 22 and out_bin[-22:] == '1110010011100100111001':
                break
            for k in xrange(3):
                if len(out_bin) >= 22 and out_bin[-22:] == '1110010011100100111001':
                    break
                out_bin += str(int(bin_image[i,j,k]))[-1]
    out_str = bin_to_str(str(out_bin))[:-3]
    if len(out_str) > 1000:
        with open("{}_decoded.txt".format(img_path), "w") as text_file:
            text_file.write(out_str)
        print('Output string longer than 1000 characters.  Automatically written to file at {}_decoded.txt'.format(img_path))
    return(out_str)


if __name__ == "__main__":
    new_pic = insert_message('A quick brown fox jumps over the lazy dog.', 'lion.png')
    print('Retrieved message: ', retrieve_message('lion_encoded.png'))
    

