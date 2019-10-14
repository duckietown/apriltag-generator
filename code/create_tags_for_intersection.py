## This file creates Apriltags as output
from shutil import copyfile
from datetime import datetime
import pandas as pd
import yaml

#USER INPUT##################################################
start=1 #min 1
end = 99 #max 551


## code only works with this setting atm
withpicture = True
if withpicture:
    tagsppage = 3
else:
    tagsppage = 6

IDtext = 'ID =' #TODO change with id
offset = 1 # Megabot = 400, Localization = 1

#GET DATA FROM APRILTAGS DATABASE
with open("../apriltagsDB.yaml", 'r') as stream:
    try:
        apriltagsDB = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)




#LATEX TEXTBLOCKS #################################################
# commands for April Tag Text #NOTE uncomment next line to write a line
AprilTagIDTextFront= '\n\\newcommand{\\AprilTagIDTextFront}[1]{%parameter 1:ID Number \n \\centering \n	\\Large{\\textbf{'+ IDtext +' #1}}\\\\ \n	%\\small{\\today} \n	\\vspace*{2mm}\\vspace{50mm} \n}\n'
AprilTagIDNoTextFront= '\n\\newcommand{\\AprilTagIDNoTextFront}{ \n \\centering \n	\\Large{\\textbf{\\textcolor{white}{simple} }}\\\\ \n	%\\small{\\today} \n	\\vspace*{2mm}\\vspace{50mm} \n}\n'

#AprilTagIDTextFront= '\n\\newcommand{\\AprilTagIDTextFront}[1]{  \n \\centering \n	\\Large{\\textbf{ }}\\\\ \n	%\\small{\\today} \n	\\vspace*{2mm}\\vspace{50mm} \n}\n'



AprilTagIDText ='\n\\newcommand{\\AprilTagIDText}[1]{THISISME\n	\\centering\n	\\rotatebox[origin=c]{180}{\\huge{'+"HEYTHERE" +'#1}}\\\\\n	\\rotatebox[origin=c]{180}{\\small{\\today}}\n	\\vspace{60mm}\n}\n'


# start new page (front)
new_page = '\\clearpage\n\n\\begin{table}[p]\n	\\centering\n	\\begin{tabular}{m{15mm}m{80mm}m{80mm}m{80mm}m{15mm}}\n		%CutMarkRow\n		\\multicolumn{1}{c|}{}	& \\multicolumn{1}{c|}{\\CutMarkCell{}} & \\multicolumn{1}{c|}{} &        \\multicolumn{1}{c|}{}              &  \\\\ \\cline{1-1} \\cline{5-5}\n\n		%Distance Row\n		& \\TopBottomCell{}  & & & \\\\\n\n'
# Apriltag row:
#1
april1 = '\n%April Tag\n		& \\AprilTagCell{'
#2
april2 = '}}  & \\AprilTagCell{'
#3
april3 = '}}  & \\AprilTagCell{'
#4
april4 = '}} &  \\\\\n'

trafficsign = '\n%April Tag\n		& \\AprilTagCell{\\TrafficSignPicture{'

# text row
#1

#text1 = '\n%Text Row\n		& \\BetweenCell{} \\AprilTagIDTextFront{'
text1 = '\n%Text Row\n		& \\AprilTagIDTextFront{'
notext1 = '\n%Text Row\n		& \\AprilTagIDNoTextFront{'
#2
text2 = '} & \\AprilTagIDTextFront{'
notext2 = '} & \\AprilTagIDNoTextFront{'
#3
text3 ='}& \\AprilTagIDTextFront{'
notext3 ='}& \\AprilTagIDNoTextFront{'
#4
text4 ='}& \\\\	\\cline{1-1} \\cline{5-5}\n'

# Distance Row
distance_row = '\n		%Distance Row\n		& \TopBottomCell{}  & & & \\\\\n'



# end page
end_page = '\n		%Distance Row\n		& \\TopBottomCell{}  & & & \\\\\n		%CutMarkRow\n		\\multicolumn{1}{c|}{}	& \\multicolumn{1}{c|}{\\CutMarkCell{}} & \\multicolumn{1}{m{80mm}|}{} &        \\multicolumn{1}{c|}{}              &  \n\n	\\end{tabular}\n\\end{table}\n'

#END LATEX TEXTBLOCKS #################################################



def create_tags(tag1,tag2,tag3,description1, description2, description3,text):
    if type(tag1) != int:
        t1 = "\\Picture{"+str(tag1)+".png"
    else:
        t1 = "\\AprilTagPicture{"+str(int(tag1))


    if type(tag2) != int:
        t2 = "\\Picture{"+str(tag2)+".png"
    else:
        t2 = '\\AprilTagPicture{'+str(int(tag2))


    if type(tag3) != int:
        t3 = "\\Picture{"+str(tag3)+".png"
    else:
        t3 = "\\AprilTagPicture{"+str(int(tag3))

    d1 = str(int(description1))
    d2 = str(int(description2))
    d3 = str(int(description3))

    string = april1 + t1 + april2 +t2 +april3 +t3+april4 +distance_row
    if not withpicture:
        #string = string + text1 ++ text2 + d2 +text3 +d3 +text4
        2+2

    else:

        1+1 #TODO fix
    #if text is True:
    if text is True:
        string = string + text1 +d1+ text2 +d2+ text3  +d3+ text4
    else:
        string = string + notext1 + notext2  + notext3 + text4
    return string

time = "{:%Y%m%d-%H%M}".format(datetime.now())
src = 'template.tex'
filename = 'AprilTags_' + time + '.tex'
copyfile(src, filename)

output = open(filename, 'a')
output.write(AprilTagIDTextFront)
output.write(AprilTagIDNoTextFront)
output.write(AprilTagIDText)

# Cuz Apriltags start with Number 0
start += 1
end += 1

# intersectionNumber  = input("Tell me int numb")
# filename = '../lists/4intersection_'+str(intersectionNumber)+'.csv'
# fh = open(filename, 'r')
# rawList = list()
# for line in fh:
#     rawList.append(line.strip().split(','))
# rawList = rawList[0]
# idList = rawList[:-1]
# print idList

for i in range(0,1):

    tag_id = int(95)
    tag_id2 = int(96)
    tag_id3 = int(97)

    print tag_id
    print tag_id2
    print tag_id3


    tag_type1 = apriltagsDB[tag_id]['tag_type']
    traffic_sign_type1 = apriltagsDB[tag_id]['traffic_sign_type']

    tag_type2 = apriltagsDB[tag_id2]['tag_type']
    traffic_sign_type2 = apriltagsDB[tag_id2]['traffic_sign_type']

    tag_type3 = apriltagsDB[tag_id3]['tag_type']
    traffic_sign_type3 = apriltagsDB[tag_id3]['traffic_sign_type']

    if traffic_sign_type1 is None: traffic_sign_type1="empty"
    if traffic_sign_type2 is None: traffic_sign_type2="empty"
    if traffic_sign_type3 is None: traffic_sign_type3="empty"





    output.write(new_page)
    output.write(create_tags(traffic_sign_type1,traffic_sign_type2,traffic_sign_type3,tag_id-offset,tag_id2-offset,tag_id3-offset,False))
    output.write(distance_row)
    output.write(create_tags(tag_id+1,tag_id2+1,tag_id3+1,tag_id-offset,tag_id2-offset,tag_id3-offset,False))
    output.write(end_page)

    #This writes the IDs on the next page
    output.write(new_page)
    output.write(create_tags("empty","empty","empty",tag_id-offset,tag_id2-offset,tag_id3-offset,False))
    output.write(distance_row)
    output.write(create_tags("empty","empty","empty",tag_id,tag_id2,tag_id3,True))
    output.write(end_page)






output.write('\\end{document}')
output.close()
