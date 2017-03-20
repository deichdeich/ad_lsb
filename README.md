# ad_lsb
Steganography conceals information inside non-secret data.  The method used here conceals a plaintext message inside an image without noticably changing the look of the image to the naked eye.  Doing a subtraction of the original image with the output image would reveal pixel differences in the coordinates with the message data, however.

Least Significant Bit (LSB) steganography works by changing the least significant bit of some piece of data to contain a message.  In this case, the LSB of each R,G,B value for the pixels of the input image is swapped with the next bit of the message (in this way, an 8 megapixel image could hold 3 megabytes of message).

I thought LSB steganography sounded neat, so I made this.  It's probably not the most efficient method, but this was really just for my personal satisfaction.  In particular, I couldn't figure out a good way of iterating through each pixel in the output from PIL, so it's just a triple-nested for loop, which is *great* for efficiency.

# Usage
This code relies on numpy and PIL, both readily pip'd.

There are two functions the user needs concern themselves with.  `insert_message()` which puts some plaintext inside an image, and `retrieve_message()` which reads it from the image.

### `insert_message()`
`insert_message()` has the following arguments:

`message`: plain text which will be inserted in the message

`img_path`: path of the image into which the message will be inserted

`fname`: the name of the output image file, *optional, default: img_path_encoded.png*

`end_string`: the string to tell the decoder that the message has ended.  *optional, default: 999*

### `retieve_message()`
`retrieve_message()` has the following arguments:

`img_path`: path of an image containing a message

`end_string`:  the string used to end the message.  *optional, but must match the string used in insert_message.  default: 999*

### Example
```
  import ad_lsb
  ad_lsb.insert_message('A quick brown fox jumps over the lazy dog.',
                                  'lazydog.png',
                                   end_string = 'bS&L/TaYq*YD3m`k')
  retr_string = retrieve_message('lazydog_encoded.png', end_string = 'bS&L/TaYq*YD3m`k')
  print('Retrieved message: ', retr_string)
```
