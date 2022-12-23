# image_processing
Image processing of files in the pgm format.
Loads image file as a matrix in the form of nested lists, and then checks if the matrix is in valid format; in either compressed or decompressed form. 
Then performs a variety of actions such as inverting, compressing, decompressing, flipping (horizontally ie via rows of matrix or vertically ie via columns of matrix), cropping, and finding the end of a repetition of an integer in the matrix. This modified matrix is then saved as a new pgm file, either in regular(decompressed) or compressed pgm format.
