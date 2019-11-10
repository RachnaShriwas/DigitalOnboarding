import re
import math
global_name=re.compile("([A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+)|([A-Z][a-z]+\s[A-Z][a-z]+)")
# date_pattern = re.compile(r'(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})|(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})')
# dl_number_pattern = re.compile(r'([A-Z]{2}(-){0,1}[0-9]{2}C{0,1}(19[0-9][0-9]|20[0,1][0-9])[0-9]{7})|([A-Z]{2}(-){0,1}[0-9]{3}(19[0-9][0-9]|20[0,1][0-9])[0-9]{7})|([A-Z]{2}[0-9]{2}/[0-9]{6,7}/[0-9]{2,4})|([A-Z]{2}-[0-9]{2}-[0-9]{6,7}-[0-9]{2})|([A-Z]{2}[0-9]{2}-[0-9]{4,7}-[0-9]{2})|([0-9]{2}/[0-9]{5,7}/(19[0-9][0-9]|20[0,1][0-9]))|([A-Z]{2}[0-9]{2,3}/DLC/[0-9]{2}/[0-9]{6,7})|([0-9]{2}/[0-9]{5,7}/[0-9]{2})')
# doi_pattern = re.compile(r'DOI|Issue')
# cog_pattern = re.compile(r'LMV|MCWG|MCWOG')
# def text_within(document,x1,y1,x2,y2):
#     text=""
#     for page in document.pages:
#         for block in page.blocks:
#             for paragraph in block.paragraphs:
#                 for word in paragraph.words:
#                     for symbol in word.symbols:
#                         min_x=min(symbol.bounding_box.vertices[0].x,symbol.bounding_box.vertices[1].x,symbol.bounding_box.vertices[2].x,symbol.bounding_box.vertices[3].x)
#                         max_x=max(symbol.bounding_box.vertices[0].x,symbol.bounding_box.vertices[1].x,symbol.bounding_box.vertices[2].x,symbol.bounding_box.vertices[3].x)
#                         min_y=min(symbol.bounding_box.vertices[0].y,symbol.bounding_box.vertices[1].y,symbol.bounding_box.vertices[2].y,symbol.bounding_box.vertices[3].y)
#                         max_y=max(symbol.bounding_box.vertices[0].y,symbol.bounding_box.vertices[1].y,symbol.bounding_box.vertices[2].y,symbol.bounding_box.vertices[3].y)
#                         if(min_x >= x1 and max_x <= x2 and min_y >= y1 and max_y <= y2):
#                             text+=symbol.text
#                             if(symbol.property.detected_break.type==1 or
#                                symbol.property.detected_break.type==3):
#                                 text+=' '
#                             if(symbol.property.detected_break.type==2):
#                                 text+='\t'
#                             if(symbol.property.detected_break.type==5):
#                                 text+='\n'
#     return text
def assemble_word(word):
    assembled_word=""
    for symbol in word.symbols:
        assembled_word+=symbol.text
    return assembled_word


def find_word_location(document,word_to_find):
    print("in function")
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled_word=assemble_word(word)
                    if(assembled_word==word_to_find):
                        print(word.bounding_box)
                        return word.bounding_box

def text_within(document,x1,y1,x2,y2):
    text=""
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        min_x=min(symbol.bounding_box.vertices[0].x,symbol.bounding_box.vertices[1].x,symbol.bounding_box.vertices[2].x,symbol.bounding_box.vertices[3].x)
                        max_x=max(symbol.bounding_box.vertices[0].x,symbol.bounding_box.vertices[1].x,symbol.bounding_box.vertices[2].x,symbol.bounding_box.vertices[3].x)
                        min_y=min(symbol.bounding_box.vertices[0].y,symbol.bounding_box.vertices[1].y,symbol.bounding_box.vertices[2].y,symbol.bounding_box.vertices[3].y)
                        max_y=max(symbol.bounding_box.vertices[0].y,symbol.bounding_box.vertices[1].y,symbol.bounding_box.vertices[2].y,symbol.bounding_box.vertices[3].y)
                        if(min_x >= x1 and max_x <= x2 and min_y >= y1 and max_y <= y2):
                            text+=symbol.text
                            if(symbol.property.detected_break.type==1 or
                               symbol.property.detected_break.type==3):
                                text+=' '
                            if(symbol.property.detected_break.type==2):
                                text+='\t'
                            if(symbol.property.detected_break.type==5):
                                text+='\n'
    return text
def find_compound_word_location(document,word_to_find):
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for idx,word in enumerate(paragraph.words):
                    try:
                        assembled_word=assemble_word(word)+ " " + assemble_word(paragraph.words[idx+1])
                        if(assembled_word==word_to_find):
                            return word.bounding_box
                    except:
                        pass

def find_nearest_words(document, word, radius):
    word_bounding_box = find_word_location(document, word)
    print("BB: ", word_bounding_box)
    text = ""
    if (not word_bounding_box):
        return text
    centroid_x = (word_bounding_box.vertices[0].x + word_bounding_box.vertices[2].x) / 2
    centroid_y = (word_bounding_box.vertices[0].y + word_bounding_box.vertices[2].y) / 2

    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        x_c = (word.bounding_box.vertices[0].x + word.bounding_box.vertices[2].x) / 2
                        y_c = (word.bounding_box.vertices[0].y + word.bounding_box.vertices[2].y) / 2

                        distance = math.sqrt((x_c - centroid_x) ** 2 + (y_c - centroid_y) ** 2)
                        if (distance <= radius):
                            text += symbol.text
                            if (symbol.property.detected_break.type == 1 or
                                    symbol.property.detected_break.type == 3):
                                text += ' '
                            if (symbol.property.detected_break.type == 2):
                                text += '\t'
                            if (symbol.property.detected_break.type == 5):
                                text += '\n'

    return text


'''def find_compound_word_location(document,word_to_find):
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for idx,word in enumerate(paragraph.words):
                    try:
                        assembled_word=assemble_word(word)+ " " + assemble_word(paragraph.words[idx+1])
                        if(assembled_word==word_to_find):
                            return word.bounding_box
                    except:
                        pass'''

def dl_check(text):
    dl_regex = re.compile(r'[A-Z]{2}[0-9]{2}[\s|-][0-9]{11}')
    dl_name = re.compile(r'NAME\s:.*\n')
    #dl_num_pattern= re.compile(r'([A-Z]{2}(-|\s){0,1}[0-9]{2}C{0,1}(19[0-9][0-9]|20[0,1][0-9])[0-9]{7})|([A-Z]{2}(-){0,1}[0-9]{3}(19[0-9][0-9]|20[0,1][0-9])[0-9]{7})|([A-Z]{2}[0-9]{2}/[0-9]{6,7}/[0-9]{2,4})|([A-Z]{2}-[0-9]{2}-[0-9]{6,7}-[0-9]{2})|([A-Z]{2}[0-9]{2}-[0-9]{4,7}-[0-9]{2})|([0-9]{2}/[0-9]{5,7}/(19[0-9][0-9]|20[0,1][0-9]))|([A-Z]{2}[0-9]{2,3}/DLC/[0-9]{2}/[0-9]{6,7})|([0-9]{2}/[0-9]{5,7}/[0-9]{2})')
    dl_num=dl_regex.findall(text)[0].replace(" ",'')
    dl_nme=dl_name.findall(text)
    dl_nme = dl_nme[0][7:].lstrip().rstrip()
    return {
        "Name": dl_nme,
        "Dl_number": dl_num
    }

def pan_check(text):
    pan_num_pattern = re.compile("[A-Z]{5}[0-9]{4}[A-Z]")
    pan_name_pattern=re.compile("[A-Z]+")
    pan_num=pan_num_pattern.findall(text)[0]
    pan_name=pan_name_pattern.findall(text)
    pan_name=pan_name[6:-8]
    pn=""
    for i in range(0,len(pan_name)//2):
        pn+=(pan_name[i]+" ")
    print(pn)
    if(pan_num==None):
        return False, {}
    pan_json={
        'name':pn,
        'pan_no':pan_num
    }
    return True, pan_json

def aadhar_check(text):
    adhaar_num_pattern = re.compile("\d{4}\s?\d{4}\s?\d{4}")
    adhaar_name_pattern = global_name
    adhaar_dob_pattern = re.compile("^(0[1-9]|1[012])[-/.](0[1-9]|[12][0-9]|3[01])[-/.][0-9]{4}")

    aadhar_no=adhaar_num_pattern.search(text).group().replace(" ","")
    aadhar_name=adhaar_name_pattern.search(text).group()
    aadhar_dob=adhaar_dob_pattern.search(text)
    if(aadhar_dob==None):
        adhaar_dob_pattern = re.compile("\d{4}")
        aadhar_dob = adhaar_dob_pattern.search(text).group()
    else:
        aadhar_dob=' '.join(aadhar_dob.group())

    aadhar_json={
        'uidai':aadhar_no,
        'name': aadhar_name,
        'DOB/year': aadhar_dob
    }

    mult = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 0, 6, 7, 8, 9, 5], [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
                [3, 4, 0, 1, 2, 8, 9, 5, 6, 7], [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
                [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], [7, 6, 5, 9, 8, 2, 1, 0, 4, 3], [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
                [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]
    perm = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 7, 6, 2, 8, 3, 0, 9, 4], [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
                [8, 9, 1, 6, 0, 4, 3, 5, 2, 7], [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
                [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]

    try:
        i = len(aadhar_no)
        j = 0
        x = 0

        while i > 0:
            i -= 1
            x = mult[x][perm[(j % 8)][int(aadhar_no[i])]]
            j += 1
            if x == 0:
                return False,aadhar_json
            else:
                return True,aadhar_json

    except ValueError:
        return False,aadhar_json
    except IndexError:
        return False,aadhar_json