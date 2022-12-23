# Ayo Eyesan
# Image Processing

def is_valid_image(n_l):
    """ (list<anyType>) -> (bool)
    Returns True if the nested list represents
    a valid non - compressed PGM image matrix and False otherwise
    
    >>> is_valid_image([["0x5", "200x2"], ["111x7"]])
    False
    >>> is_valid_image([1, 2, 3, 4], [5, 6, 7, 8], [254, 0, 78, 2])
    True
    >>> print(is_valid_image([[1, 2], [5, 6, 7, 8], [-5]]))
    False
    """
    for l in n_l:
        new_list = []
        if len(l) != len(n_l[0]):
            return False
        for t in l:
            if type(t) != int:
                return False
        new_list += l
        for i in range(len(new_list)):
            if new_list[i] < 0 or new_list[i] > 255:
                return False
    else:
        return True

def is_valid_compressed_image(n_l):
    """ (list<anyType>) -> (bool)
    Returns True if the nested list represents
    a valid compressed PGM image matrix and False otherwise
    
    >>> is_valid_compressed_image([["0x5", "200x2"], ["111x7"]])
    True
    >>> is_valid_compressed_image([["8x4", "70x3"], [111 * 7], ["3x6", "0x1"]])
    False
    >>> is_valid_compressed_image([["8x4", "70x3"], ["300x10"], ["3x6", "0x1"]])
    False
    """
    check_sum = -1
    for l in n_l:
        sum_1 = 0
        new_list = []
        for t in l:
            if type(t) == str:
                if 'x' in t:
                    t = t.split('x')
                    new_list += t
                else:
                    return False
            else:
                return False
        for i in range(len(new_list)):
            if i == 0 or i % 2 == 0:
                if int(new_list[i]) < 0 or int(new_list[i]) > 255:
                    return False
            elif i % 2 != 0:
                if int(new_list[i]) <= 0:
                    return False
                else:
                    sum_1 += int(new_list[i])
        if check_sum == -1:
            check_sum = sum_1
        else:
            if sum_1 != check_sum:
                return False
    else:
        return True

def load_regular_image(s):
    """
    (str) -> (str)
    Loads in the image contained in the file and returns it as an image matrix
    
    >>> load_regular_image("comp.pgm")
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 187, 187, 187, 187, 0, 255,
    255, 255, 255, 0],
    [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 255, 0],
    [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 255, 255, 255,
    0],
    [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0],
    [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0,
    0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    >>> save_image([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]], 'docstring')
    >>> load_regular_image('docstring')
    [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
    
    >>> save_image([[1, 1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 2, 2]], 'docstring2')
    >>> load_regular_image('docstring2')
    [[1, 1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 2, 2]]
    """
    image = []
    filename = s
    fobj = open(s, 'r')
    line_counter = 0
    for line in fobj:
        image_substrings = []
        line_counter += 1
        if line_counter <= 3:
            continue
        s = line
        s = s.split(' ')
        copy = []
        for elm in s:
            copy.append(elm)
        for elm in copy:
            if elm == '':
                s.remove('')
        s[len(s) - 1] = s[len(s) - 1].strip('\n')
        image_substrings += s
        image.append(image_substrings)
    fobj.close()
    regular_image = []
    for l in image:
        regular_image_substring = []
        for elm in l:
            if elm == '':
                continue
            regular_image_substring.append(int(elm))
        regular_image.append(regular_image_substring)
    if not is_valid_image(regular_image):
        raise AssertionError("Image matrix contained in file not of PGM format")
    return regular_image

def load_compressed_image(s):
    """
    (str) -> (str)
    Loads in the image contained in the file and returns it as a compressed image matrix
    
    >>> load_compressed_image("comp.pgm.compressed")
    [['0x24'],
    ['0x1', '51x5', '0x1', '119x5', '0x1', '187x5', '0x1', '255x4', '0x1'],
    ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1',
    '187x1', '0x1', '255x1', '0x2', '255x1', '0x1'],
    ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1',
    '187x1', '0x1', '255x4', '0x1'],
    ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1',
    '187x1', '0x1', '255x1', '0x4'],
    ['0x1', '51x5', '0x1', '119x5', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1',
    '255x1', '0x4'],
    ['0x24']]
    
    >>> save_image([['25x25', '4x50']], 'docstring3')
    >>> load_compressed_image('docstring3')
    [['25x25', '4x50']]
    
    >>> save_image([['0x1', '254x100', '1x1'], ['1x2', '4x97', '2x3']], 'docstring4')
    >>> x = [['0x1', '254x100', '1x1'], ['1x2', '4x97', '2x3']]
    >>> load_compressed_image('docstring4') == x
    True
    """
    image = []
    fobj = open(s, 'r')
    i = 0
    for line in fobj:
        if i < 3:
            i += 1
            continue
        image.append(line.strip().split())
    fobj.close()
    if not is_valid_compressed_image(image):
        raise AssertionError("Image matrix contained in file not of PGM format")
    return image

def load_image(s):
    """
    (str) -> (list<list>)
    Checks the first line of the file. If it is 'P2',
    then loads in the file as a regular PGM image and returns the image matrix.
    If it is 'P2C', then loads in the file as a compressed PGM image and returns the
    compressed image matrix
    
    >>> save_image([[1], [2], [3]], 'xyz')
    >>> load_image("xyz")
    [[1], [2], [3]]
    
    >>> save_image([['1x100', '2x3'], ['4x50', '2x2']], 'error')
    >>> load_image('error')
    Traceback (most recent call last):
    AssertionError: Input matrix is not a valid PGM image matrix
    
    >>> save_image([['1x2', '2x3', '3x4'], ['2x2', '3x3', '4x4']], 'squares')
    >>> load_image('squares')
    [['1x2', '2x3', '3x4'], ['2x2', '3x3', '4x4']]
    """
    filename = s
    fobj = open(s, 'r')
    file_content = fobj.read(4)
    if 'P2C' in file_content:
        return load_compressed_image(filename)
    elif 'P2' in file_content:
        return load_regular_image(filename)
    else:
        raise AssertionError("Image matrix contained in file not of PGM format")

def save_regular_image(n_l, s):
    """
    (list<list>, str) -> NoneType
    Saves nested list and filename in the PGM format to a file with the given filename
    
    >>> image = [[0]*10, [255]*10, [0]*10]
    >>> save_regular_image(image, "test.pgm")
    >>> image2 = load_image("test.pgm")
    >>> image == image2
    True
    
    >>> save_regular_image([[254, 253, 252, 251, 250], [249, 248, 247, 246, 245], [244, 243,
    242, 241, 240]], 'doctest5')
    >>> load_image('doctest5')
    [[254, 253, 252, 251, 250], [249, 248, 247, 246, 245], [244, 243, 242, 241, 240]]
    
    >>> save_regular_image([[255, 6, 4, 256], [1, 2, 3, 4], [60, 89, 74, 3]], 'doctest6')
    >>> load_image('doctest6')
    Traceback (most recent call last):
    AssertionError: Input matrix is not a valid PGM image matrix
    """
    if not is_valid_image(n_l):
        raise AssertionError("Input matrix is not a valid PGM image matrix")
    number_of_rows_counter = 0
    length_of_rows = 0
    string_of_list = ''
    for l in n_l:
        if length_of_rows == 0:
            length_of_rows += len(l)
        number_of_rows_counter += 1
        string_of_list += ('\n')
        for elm in l[ :len(l) - 1]:
            string_of_list += str(elm) + ' '
        for elm in l[len(l) - 1:]:
            string_of_list += str(elm)
    number_of_rows_counter = ' ' + str(number_of_rows_counter)
    length_of_rows = '\n' + str(length_of_rows)
    filename = s
    fobj = open(filename, 'w')
    fobj.write('P2')
    fobj.write(length_of_rows), fobj.write(number_of_rows_counter)
    fobj.write('\n255')
    fobj.write(string_of_list)
    fobj.close
    
def save_compressed_image(n_l, s):
    """
    (list<list>, s) -> NoneType
    Saves nested list and filename in the compressed PGM format to a file with the given
    filename
    
    >>> image = [["0x5", "200x2"], ["111x7"]]
    >>> save_compressed_image(image, "test.pgm")
    >>> image2 = load_compressed_image("test.pgm")
    >>> image == image2
    True
    
    >>> save_compressed_image([['254x4', '1x6'], ['200x10']], 'doctest7')
    >>> load_image('doctest7')
    [['254x4', '1x6'], ['200x10']]
    
    >>> save_compressed_image([['254x4', '1x6'], ['200x100']], 'doctest8')
    >>> load_image('doctest7')
    Traceback (most recent call last):
    AssertionError: Input matrix is not a valid PGM image matrix
    """
    if not is_valid_compressed_image(n_l):
        raise AssertionError("Input matrix is not a valid PGM image matrix")
    number_of_rows_counter = 0
    length_of_rows = ''
    string_of_list = ''
    for l in n_l:
        number_of_rows_counter += 1
        string_of_list += ('\n')
        x = 0
        for elm in l[ :len(l) - 1]:
            string_of_list += (elm + ' ')
            x += int(elm.split('x')[1])
        for elm in l[len(l) - 1: ]:
            string_of_list += (elm)
            x += int(elm.split('x')[1])
        if length_of_rows == '':
            length_of_rows += ('\n' + str(x))
    number_of_rows_counter = ' ' + str(number_of_rows_counter)
    filename = s
    fobj = open(filename, 'w')
    fobj.write('P2C')
    fobj.write(length_of_rows), fobj.write(number_of_rows_counter)
    fobj.write('\n255')
    fobj.write(string_of_list)
    fobj.close
    
def save_image(n_l, s):
    """
    (list<list>, str) -> NoneType
    >>> save_image([["0x5", "200x2"], ["111x7"]], "test.pgm.compressed")
    >>> fobj = open("test.pgm.compressed", 'r')
    >>> fobj.read()
    'P2C\\n7 2\\n255\\n0x5 200x2\\n111x7\\n'
    >>> fobj.close()
    
    >>> save_image([["0x3", "4x8", "2x4"], ["9x7", "6x9"]], "doctest9")
    >>> load_image("doctest9")
    Traceback (most recent call last):
    AssertionError: Input matrix is not a valid PGM image matrix
    
    >>> save_image([[0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2], [9, 9, 9, 9, 9, 9, 9, 6, 6, 6,
    6, 6, 6]], "doctest9")
    >>> load_image("doctest9")
    [[0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2], [9, 9, 9, 9, 9, 9, 9, 6, 6, 6, 6, 6, 6]]
    """
    for l in n_l:
        for elm in l:
            if type(elm) != str and type(elm) != int:
                raise AssertionError("Input matrix is not a valid PGM image matrix")
    for l in n_l[len(n_l) - 1:]:
        for elm in l[len(l) - 1:] :
            if type(elm) == str:
                x = save_compressed_image(n_l, s)
            if type(elm) == int:
                x = save_regular_image(n_l, s)
                
def invert(image):
    """
    (list<list>) -> (list<list>)
    Returns the inverted image matrix
    
    >>> image = [[0, 100, 150], [200, 200, 200], [255, 255, 255]]
    >>> invert(image)
    [[255, 155, 105], [55, 55, 55], [0, 0, 0]]
    >>> image == [[0, 100, 150], [200, 200, 200], [255, 255, 255]]
    True
    
    >>> image = [[0, 100, 150, 2], [200, 200, 200], [255, 255, 255]]
    >>> invert(image)
    Traceback (most recent call last):
    AssertionError: Input matrix is not a valid PGM image matrix
    
    >>> x = [[4], [3]]
    >>> invert(x)
    [[251], [252]]
    """
    new_image = []
    if not is_valid_image(image):
        raise AssertionError("Input matrix is not a valid PGM image matrix")
    else:
        for l in image:
            new_image_sublists = []
            for elm in l:
                new_image_sublists.append(abs(elm - 255))
            new_image.append(new_image_sublists)
        return new_image

def flip_horizontal(image):
    """
    (list<list>) -> (list<list>)
    Returns the image matrix flipped horizontally
    
    >>> image = [[1, 2, 3, 4, 5], [0, 0, 5, 10, 10], [5, 5, 5, 5, 5]]
    >>> flip_horizontal(image)
    [[5, 4, 3, 2, 1], [10, 10, 5, 0, 0], [5, 5, 5, 5, 5]]
    
    >>>  image = [[1, 2, 3, 4, 5], [0, 0, -1, 10, 10], [5, 5, 5, 5, 5]]
    >>> flip_horizontal(image)
    Traceback (most recent call last):
    AssertionError: Input matrix is not a valid PGM image matrix
    
    >>> x = [[0, 0], [0, 0, 5, 10, 10], [5, 5, 5, 5, 5]]
    >>> flip_horizontal(x)
    Traceback (most recent call last):
    AssertionError: Input matrix is not a valid PGM image matrix
    """
    new_image = []
    if not is_valid_image(image):
        raise AssertionError("Input matrix is not a valid PGM image matrix")
    for l in image:
        new_image.append(l[len(l) - 1: : -1])
    return new_image

def flip_vertical(image):
    """
    (list<list>) -> (list<list>)
    Returns the image matrix flipped vertically
    
    >>> image = [[1, 2, 3, 4, 5], [0, 0, 5, 10, 10], [5, 5, 5, 5, 5]]
    >>> flip_vertical(image)
    [[5, 5, 5, 5, 5], [0, 0, 5, 10, 10], [1, 2, 3, 4, 5]]
    
    >>> y = [[16, 12,13, 5, 6, 0], [6, 2,3, 5, 6, 0], [1, 1,1, 5, 6, 0]]
    >>> flip_vertical_image(y)
    [[1, 1, 1, 5, 6, 0], [6, 2, 3, 5, 6, 0], [16, 12, 13, 5, 6, 0]]
    
    >>> x = [[0], [2], [5]]
    >>> flip_vertical(x)
    [[5], [2], [0]]
    
    """
    new_image = []
    if not is_valid_image(image):
        raise AssertionError("Input matrix is not a valid PGM image matrix")
    new_image += image[len(image) - 1: : -1]
    return new_image

def crop(image, tl_r, tl_c, n_r, n_c):
    """
    (list<list>, int, int, int, int) -> (list<list>)
    Returns an image matrix corresponding to the pixels contained in the target rectangle. 
    
    >>> crop([[5, 5, 5], [5, 6, 6], [6, 6, 7]], 1, 1, 2, 2)
    [[6, 6], [6, 7]]
    
    >>> crop([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]], 0, 2, 3, 3)
    [[3, 4, 5], [8, 9, 10], [13, 14, 15]]
    
    >>> crop([[255, 256, 255], [88, 89, 88], [100, 101, 100]], 0, 0, 2, 2)
    Traceback (most recent call last):
    AssertionError: Input matrix is not a valid PGM image matrix
    """
    new_image = []
    for l in image[tl_r: tl_r + n_r]:
        new_image_sublists = []
        for i in range(len(l)):
            if i < tl_c:
                continue
            if i > tl_c + (n_c - 1):
                break
            new_image_sublists.append(l[i])
        new_image.append(new_image_sublists)
    if not is_valid_image(new_image):
        raise AssertionError("Input matrix is not a valid PGM image matrix")
    return new_image
                
def find_end_of_repetition(l, index, t_n):
    """
    (list<int>, int, int) -> (int)
    Returns the index of the last consecutive occurrence of the target number
    
    >>> find_end_of_repetition([1, 2, 3, 4, 5, 6, 7], 6, 7)
    6
    >>> find_end_of_repetition([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 0, 1)
    10
    >>> find_end_of_repetition([1, 2, 3, 4], 0, 5)
    -1
    """
    for i in range(len(l)):
        if i < index:
            continue
        elif l[i] != t_n:
            return (i - 1)
    else:
        return len(l) - 1

def compress(n_l):
    """
    (list<list<int>>) -> (list<list<str>>)
    Returns the compressed matrix
    
    >>> compress([[11, 11, 11, 11, 11], [1, 5, 5, 5, 7], [255, 255, 255, 0, 255]])
    [['11x5'], ['1x1', '5x3', '7x1'], ['255x3', '0x1', '255x1']]
    >>> compress([[1, 5, 5, 5, 7, 5, 5, 5], [255, 255, 255, 0, 255]])
    Traceback (most recent call last):
    AssertionError: Input matrix is not a valid PGM image matrix
    >>> compress([[1, 5, 5, 5, 7, 5, 5, 5], [255, 255, 255, 0, 255, 1, 254, 1]])
    [['1x1', '5x3', '7x1', '5x3'], ['255x3', '0x1', '255x1', '1x1', '254x1', '1x1']]
    """
    if is_valid_image(n_l) ==  False:
        raise AssertionError("Input matrix is not a valid PGM image matrix")
    compressed_image = []
    for l in n_l:
        compressed_image_sublist = []
        traversing_index = -1
        index = 0
        current_elm = 300
        for elm in l:
            traversing_index += 1
            if elm == current_elm:
                continue
            else:
                current_elm = elm
                index = find_end_of_repetition(l, traversing_index, elm)
                B = index - traversing_index
            compressed_image_sublist.append( str(elm) + 'x' + str(B + 1))
        compressed_image.append(compressed_image_sublist)
    return compressed_image

def decompress(n_l):
    """
    (list<list<str>>) -> (list<list<int>>)
    Returns the decompressed matrix
    
    >>> image = [[11, 11, 11, 11, 11], [1, 5, 5, 5, 7], [255, 255, 255, 0, 255]]
    >>> compressed_image = compress(image)
    >>> image2 = decompress(compressed_image)
    >>> image == image2
    True
    
    >>> x = [[1*20], [2*0], [1*5]]
    >>> decompress(x)
    Traceback (most recent call last):
    AssertionError: Input matrix is not a valid compressed PGM image matrix
    
    >>> z = [['10x50'], ['4x2', '3x48']]
    >>> decompress(z)
    [[10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10], [4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3]]
    """
    if is_valid_compressed_image(n_l) ==  False:
        raise AssertionError("Input matrix is not a valid compressed PGM image matrix")
    uncompressed_n_l_s = []
    for l in n_l:
        uncompressed_sublists_s = []
        for elm in l:
            x = 0
            y = 0
            x += int(elm.split('x')[1])
            y += int(elm.split('x')[0])
            for i in range(x):
                uncompressed_sublists_s.append(y)
        uncompressed_n_l_s.append(uncompressed_sublists_s)
    return uncompressed_n_l_s

def process_command(s):
    """
    (str) -> NoneType
    Executes each command of string in turn
    
    >>> process_command("LOAD<comp.pgm> CP DC INV INV SAVE<comp2.pgm>")
    >>> image = load_image("comp.pgm")
    >>> image2 = load_image("comp2.pgm")
    >>> image == image2
    True
    
    >>> process_command('LOAD<doctest9> INV CP SAVE<doctest9.2>')
    >>> load_image('doctest9.2')
    [['255x3', '251x8', '253x2'], ['246x7', '249x6']]
    
    >>> process_command('LOAD<doctest5> INV CP CC SAVE<doctest5.2>')
    Traceback (most recent call last):
    AssertionError: Input not a valid commnad
    """
    list_1 = []
    list_1 += s.split(' ')
    z = []
    for elm in list_1:
        if 'LOAD' in elm:
            s = ''
            for i in range(len(elm)):
                if i <= 3 or elm[i] == '<' or elm[i] == '>':
                    continue
                s += elm[i]
            z = load_image(s)

        elif 'SAVE' in elm:
                t = ''
                for i in range(len(elm)):
                    if i <= 3 or elm[i] == '<' or elm[i] == '>':
                        continue
                    t += elm[i]
                z = save_image(z, t)
            
        elif elm == 'INV':
            z = invert(z)
            
        elif elm == 'FH':
            z = flip_horizontal(z)
            
        elif elm == 'FV':
            z = flip_vertical(z)
            
        elif elm == 'CR':
            v = []
            for i in range(len(elm)):
                if i <= 1 or elm[i] == '<' or elm[i] == '>':
                    continue
                v.append(int(elm[i]))
            z = crop(z, v[0], v[1], v[2], v[3])
            
        elif elm == 'CP':
            z = compress(z)
            
        elif elm == 'DC':
            z = decompress(z)
            
        else:
            raise AssertionError("Input not a valid commnad")
