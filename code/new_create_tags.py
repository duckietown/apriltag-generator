## This file creates Apriltags as output
from shutil import copyfile
from datetime import datetime
from .utils.creator_utils import load_file

import argparse

# Parse user input TODO: read from file
parser = argparse.ArgumentParser()
parser.add_argument("--start", help="Tag number to start with, min is 1")
parser.add_argument("--end", help="Tag number to end with, min is 511")
parser.add_argument("--no_pic", action="store_true", default="False", help="Remove picture")
parser.add_argument("--id_text", default="Tag ID", help="String written under Apriltag")
parser.add_argument("--offset", default=1, help="Offset in numbering, 400 for Autobots, 1 for localization")
parser.add_argument("--database_name", default="apriltagsDB", help="Yaml file containing IDs informations")
args = parser.parse_args()


start = args.start  # min 1
end = args.end  # max 551

# Code only works with this setting atm
withpicture = not args.no_pic
if withpicture:
    tagsppage = 3
else:
    tagsppage = 6

IDtext = args.id_text
offset = 1  # Autobots = 400, Localization = 1

# Load Apriltags database
apriltagsDB = load_file('config/' + args.database_name)

# Load latex strings
t_str = load_file('/latex_t_str')


def create_tags(tag1, tag2, tag3, text):
    if type(tag1) != int:
        t1 = "\\Picture{"+str(tag1)+".png"
    else:
        t1 = "\\AprilTagPicture{"+str(int(tag1))
        d1 = str(tag1 - offset)

    if type(tag2) != int:
        t2 = "\\Picture{"+str(tag2)+".png"
    else:
        t2 = '\\AprilTagPicture{'+str(int(tag2))
        d2 = str(tag2 - offset)

    if type(tag3) != int:
        t3 = "\\Picture{"+str(tag3)+".png"
    else:
        t3 = "\\AprilTagPicture{"+str(int(tag3))
        d3 = str(tag3 - offset)

    string = t_str['april1'] + t1 + t_str['april2'] +t2 +t_str['april3'] + t3 + t_str['april4'] + t_str['distance_row']
    # if not withpicture:
    #     string = string + t_str['april1'] + t1 + t_str['april2'] + t2 + t_str['april3'] + t3 + t_str['april4'] + t_str['distance_row']
    #
    #     #string = string + t_str['text1'] + t_str['text2'] + d2 +t_str['text3'] + d3 +t_str['text4']
    #     #string = string + t_str['text1'] + t_str['text2']  +t_str['text3']  +t_str['text4']
    #
    # else:
    #
    #     1+1 #TODO fix

    if text is True:
        string = string + t_str['text1'] + d1 + t_str['text2'] + d2 + t_str['text3'] + d3 + t_str['text4']
    else:
        string = string + t_str['notext1'] + t_str['notext2'] + t_str['notext3'] + t_str['text4']
    return string


time = "{:%Y%m%d-%H%M}".format(datetime.now())
src = 'template.tex'
filename = 'AprilTags_' + time + '.tex'
copyfile(src, filename)

output = open(filename, 'a')
output.write(t_str['AprilTagIDTextFront'])
output.write(t_str['AprilTagIDNoTextFront'])
output.write(t_str['AprilTagIDText'])

# Because Apriltags start with Number 0
start += 1
end += 1

for tag_id in range(start, end+1, tagsppage):
    tag_type1 = apriltagsDB[tag_id]['tag_type']
    traffic_sign_type1 = apriltagsDB[tag_id]['traffic_sign_type']

    tag_type2 = apriltagsDB[tag_id+1]['tag_type']
    traffic_sign_type2 = apriltagsDB[tag_id+2]['traffic_sign_type']

    tag_type3 = apriltagsDB[tag_id+2]['tag_type']
    traffic_sign_type3 = apriltagsDB[tag_id+2]['traffic_sign_type']

    if traffic_sign_type1 is None: 
        traffic_sign_type1 = "empty"
    if traffic_sign_type2 is None:
        traffic_sign_type2 = "empty"
    if traffic_sign_type3 is None:
        traffic_sign_type3 = "empty"

    output.write(t_str['new_page'])
    output.write(create_tags(tag_id, tag_id+1, tag_id+2, True))
    output.write(t_str['distance_row'])
    output.write(create_tags(tag_id+3, tag_id+4, tag_id+5, True))
    output.write(t_str['end_page'])

    # This writes the IDs on the next page
    output.write(t_str['new_page'])
    if withpicture:
        output.write(create_tags("empty", "empty", "empty", False))
    else:
        output.write(create_tags("empty", "empty", "empty", tag_id, tag_id+1, tag_id+2, True))
    output.write(t_str['distance_row'])
    if withpicture:
        output.write(create_tags("empty", "empty", "empty", tag_id, tag_id+1, tag_id+2, True))
    else:
        output.write(create_tags(tag_id+3, tag_id+4, tag_id+5, True))

    output.write(t_str['end_page'])

output.write('\\end{document}')
output.close()
