# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:20:18 2024

@author: Shadow
"""

import csv
import random
#input raw data exemple
#1/7/2024 15:25:14,I have read the event rules,Yes,Yes,"https://drive.google.com/open?id=1p9D4xot_Ec5UDWINlzlwyWL5C7B6SmjC, https://drive.google.com/open?id=1wFWkes3JzaOGQwAsduqzCbKzCbwl3qet, https://drive.google.com/open?id=1JDKt7Ufhl94bgGQLdei3wkv2z6DNjLRx, https://drive.google.com/open?id=1N9tmToPSy65QjQxvTF8IrnrsbnD9zCTO, https://drive.google.com/open?id=1xYUMXGRjcSLyYmzc-YtwTjkzhTFg64yZ","Human, Humanoid, Men/Male, Women/Female, MLP",No Gore,No,No,No with your OC,No,No,Yes,Yes,Yes,"Humanoid, Men/Male, Women/Female, MLP",No Gore,Yes,Yes,No with your OC,No,Yes,Yes,No,Yes,Yes,Spoopy.-Ghost#6963,4,ghostadopts.5653@gmail.com,Maybe a quick tutorial on how to fill this form for the harder parts like Id and uploading files to this site but otherwise. Nothing else :3
#{'Are you 18+ ?': 'Yes', 'Do you want your present to be public ?': 'Yes', 'OC Reference (1 to 5 pics, 10MB max)': 'https://drive.google.com/open?id=1ZWclAE5E4Saqt9PWcMlml38qtnOcg7Yw', 'Your OC Tags': 'Anthro', 'Gore ? ': 'No Gore', 'Genderbend ? ': 'No', 'Simplify design': 'No', 'Ship ': 'No with your OC', 'Species swap': 'No', 'Alt palettes': 'No', 'Alt outfit': 'Yes', 'Anthro to feral': 'No', 'Feral to anthro': 'No', 'Your tags': 'Furry (dog, cat, reptile, bird, insect, fishs, horse, cow...), Anthro', 'Are you available to make a second present ?': 'No', 'Your discord id (xxxx#yyyy)': 'Obsidian_sodapop ', 'Your disponibility for secret santa': '4', 'Your email': 'kurogray844@gmail.com'}

#processable data exemple
#[[discordid_string],[artist_bool=0],[oc_tags_matrix],[oc_prefs_matrix]]
#[[discordid_string],[artist_bool=1],[artist_tags_matrix],[artist_prefs_matrix]]
#[[discordid_string],[oc_links_list],[oc_tags_matrix],[oc_prefs_matrix],[remarks_string],[public_bool]]

#tag coding table
#000 = furry
#001 = anthro
#002 = feral
#003 = mecha
#004 = human
#005 = male
#006 = female
#007 = close species
#008 = dragon
#009 = object head
#010 = monster|demon
#011 = lego monkey
#012 = mlp
#013 = pokemon

#tag list exemple :
#[1,0,0,0,0,0,1,0,0,0,0,0,0,0] = furry female

#prefs coding table
#000 = gore [0;3]
#001 = genderbend
#002 = simplify design
#003 = ship [0;4]
#004 = species swap
#005 = alt palettes
#006 = alt outfit
#007 = anthro to feral
#008 = feral to anthro

#pref list exemple
#[0,0,0,1,0,1,1,0,0] = nogore, nogenderbend, nosimplify,ship, nospeciesswap,altpalette,altoutfit,noanthrotoferal,noferaltoanthro

def associate (artist_list,oc_list):
    output = []
    total_dist=0
    for i in range(len(oc_list)):
        mindist = find_min_dist(oc_list[i],artist_list)
        output += [[oc_list[i][0],i,artist_list[mindist[1]][0],mindist[0]]]
        total_dist += mindist[0]
        artist_list.pop(mindist[1])
    verif(output)
    return [output,total_dist]

def verif (output_list):
    verif_list = []
    for i in output_list:
        verif_list += i
    #print('verif list = '+str(verif_list)) #DEBUG
    for i in output_list:
        if verif_list.count(i[0]) != 2:
            raise Exception('Match number error',i[0], verif_list.count(i))

def distance (coord_a_list,coord_b_list):
    if (len(coord_a_list))!=(len(coord_b_list)):
        raise Exception("dimension error : coords need same dimension number "+str(len(coord_a_list))+' vs '+str(len(coord_b_list)))
    else:
        acc = 0
        for i in range(len(coord_a_list)):
            acc += (coord_a_list[i]-coord_b_list[i])**2
    output = acc**0.5
    return output

def find_min(input_list=[0],min_value=[0],min_index = 0):
    min_value = input_list[0]
    for i in range(len(input_list)):
        if input_list[i] < min_value:
            min_value = input_list[i]
            print(i)
            min_index = i
        else:
            break
    return [min_value,min_index]

def find_min_dist(coord_a_list,coordlist_list):
    min_value = 65535
    min_index = 0
    for i in range(len(coordlist_list)):
        if coord_a_list[0]!=coordlist_list[i][0]:
            y = coordlist_list[i][1]+coordlist_list[i][2]
            dist = distance(coord_a_list[1]+coord_a_list[2],y)
            if dist < min_value:
                min_value = dist
                min_index = i
        else:
            continue
    return [min_value,min_index]

def tags_encode(taglist_string):
    outlist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if taglist_string.find("Furry") > -1:
        outlist[0]=4
    if taglist_string.find("Anthro") > -1:
        outlist[1]=4
    if taglist_string.find("Feral") > -1:
        outlist[2]=4    
    if taglist_string.find("Mecha") > -1:
        outlist[3]=4    
    if taglist_string.find("Human,") > -1:
        outlist[4]=4    
    if taglist_string.find("Humanoid") > -1:
        outlist[5]=4    
    if taglist_string.find("Men") > -1:
        outlist[6]=1    
    if taglist_string.find("Women") > -1:
        outlist[7]=1    
    if taglist_string.find("Closed species") > -1:
        outlist[8]=4    
    if taglist_string.find("Dragon") > -1:
        outlist[9]=4    
    if taglist_string.find("Monster") > -1:
        outlist[10]=4    
    if taglist_string.find("Lego") > -1:
        outlist[11]=4
    if taglist_string.find("MLP") > -1:
        outlist[12]=4
    if taglist_string.find("Pokemon") > -1:
        outlist[13]=4
    return outlist

def prefs_encode(preflist_list):
    outlist = [0,0,0,0,0,0,0,0,0]
    if (preflist_list[0]=='Yes Gore'):
        outlist[0] = 3
    if (preflist_list[0]=='Mid Gore'):
        outlist[0] = 2
    if (preflist_list[0]=='Candy Gore'):
        outlist[0] = 1
    if (preflist_list[1]=='Yes'):
        outlist[1] = 1
    if (preflist_list[2]=='Yes'):
        outlist[2] = 1
    if (preflist_list[3]=='Yes Ship OC'):
        outlist[3] = 4
    if (preflist_list[3]=='Only mention Ship OC'):
        outlist[3] = 3
    if (preflist_list[3]=='Yes with your OC'):
        outlist[3] = 2
    if (preflist_list[3]=='No with your OC'):
        outlist[3] = 1
    if (preflist_list[4]=='Yes'):
        outlist[4] = 1
    if (preflist_list[5]=='Yes'):
        outlist[5] = 1
    if (preflist_list[6]=='Yes'):
        outlist[6] = 1
    if (preflist_list[7]=='Yes'):
        outlist[7] = 1
    if (preflist_list[8]=='Yes'):
        outlist[8] = 1
    return outlist

# splicer function
# récupérer la list
# générer trois listes en sortie
# liste OC
#   [inputlist[26],inputlist[5],inputlist[6:14]]
# liste artiste
#   [inputlist[26],inputlist[15],inputlist[16:24]]
# liste public output
#   [inputlist[26],inputlist[5],inputlist[6:14]],inputlist[4],inputlist[29],inputlist[3]

def data_splice(row_list):
    output_oc = [row_list[26],tags_encode(row_list[5]),prefs_encode(row_list[6:15])]
    output_artist = [row_list[26],tags_encode(row_list[15]),prefs_encode(row_list[16:25])]
    output_public= [row_list[26],row_list[5],'|'.join(row_list[6:15]),row_list[4],row_list[29],row_list[3]]
    output = [output_oc,output_artist,output_public]
    return output

test_row = ['11/7/2024 14:21:26', 'I have read the event rules', 'Yes', 'Yes', 'https://drive.google.com/open?id=1ZWclAE5E4Saqt9PWcMlml38qtnOcg7Yw', 'Anthro', 'Mid Gore', 'No', 'No', 'No Ship OC', 'No', 'No', 'Yes', 'No', 'No', 'Furry (dog, cat, reptile, bird, insect, fishs, horse, cow...), Anthro', 'No Gore', 'No', 'No', 'No with your OC', 'No', 'No', 'Yes', 'No', 'No', 'No', 'Obsidian_sodapop ', '4', 'kurogray844@gmail.com', "Make sure the person who gets me, gets to read his design notes,\n His piercings r non optional! Must be drawn w/ his piercings! (He has 17, 16 if drawn w/ mouth close)\n\nHis clothes r also non optional! Must be wearing his clothes or any other type of clothes!\n\nDraw him w/ as little fur as possible due to him being a Boston Terrier!\n\nHe has big ears! Plz don't draw his ears small\n\nHe has a stubby tail! Do not draw w/ long fluffy tail!\n\n"]
    
def csv_parser(filepath='D:\\@Downloads\\Secret Santa Artshare (Responses) - Form Responses 1(1).csv'):
    outlist = []
    with open(filepath,newline='',encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            outlist += [row]
    return outlist

def row_slicer(outlist):
    public_output_formater(['Santa Discord ID','Recipient Discord ID','OC Tags','Gore ? ', 'Genderbend ? ', 'Simplify design', 'Ship ', 'Species swap', 'Alt palettes', 'Alt outfit', 'Anthro to feral', 'Feral to anthro','OC References','Recipient Comments','Can the artwork be public'])
    for i in range(len(outlist[1])):
        output = [outlist[0][0][i][2]]+outlist[1][i]
        print('\n',outlist[0][0][i][2],'\n',outlist[1][i],'\n',public_output_formater(output))

def public_output_formater(outputlist_list):
    with open(file='D:\\@Downloads\\Secret Santa Artshare output.csv',mode='a',newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='|',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(outputlist_list)
        
def data_preparation():
    raw_data = csv_parser()
    oc_list = []
    artist_list = []
    output_list = []
    for i in range(1,len(raw_data)):
        sliced_data = data_splice(raw_data[i])
        oc_list += [sliced_data[0]]
        artist_list += [sliced_data[1]]
        output_list += [sliced_data[2]]
    return [oc_list,artist_list,output_list]



def multi_associate(oc_list,artist_list,tries_int):
    history = []
    output = []
    optimal = 65535
    for i in range(tries_int):
        random.shuffle(oc_list)
        test = associate(oc_list[:],artist_list[:])
        history += [test[1]]
        if test[1] < optimal:
            output = test
            optimal = test[1]
    print('history = ',history)
    print('optimal = ',optimal)
    return output


j=data_preparation()
#k=associate(j[0],j[1]),j[2]

k=multi_associate(j[0],j[1],100),j[2]
row_slicer(k)