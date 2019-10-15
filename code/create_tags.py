## This file creates Apriltags as output
from shutil import copyfile
from datetime import datetime
from utils.creator_utils import load_file
import codecs
import argparse


def main():
    # Parse user input TODO: read from file
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1, help="Tag number to start with, min is 1")
    parser.add_argument("--end", type=int, default=6, help="Tag number to end with, max is 511")
    parser.add_argument("--no_pic", action="store_true", default="False", help="Remove picture")
    parser.add_argument("--id_text", default="Tag ID", help="String written under Apriltag")
    parser.add_argument("--offset", type=int, default=1,
                        help="Offset in numbering, 400 for Autobots, 1 for localization")
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

    id_text = args.id_text
    offset = 1  # Autobots = 400, Localization = 1

    # Load Apriltags database
    apriltags_db = load_file('config/' + args.database_name)

    # Load latex strings
    t_str = load_file('latex/latex_strings')
    t_str['AprilTagIDTextFront'] = t_str['AprilTagIDTextFront_pre'] + str(id_text) + t_str['AprilTagIDTextFront_post']

    def create_tags(tags=None, text_ids=None, with_text=None):
        assert tags is not None, "You need to provide some tags!"
        if with_text:
            assert text_ids is not None, "If you want to write ids, provide some text!"

        t = []
        d = []
        for idx, tag in enumerate(tags):
            if type(tag) != int:
                t.append("\\Picture{"+str(tag)+".png")
            else:
                t.append("\\AprilTagPicture{"+str(int(tag)))
                d.append(str(text_ids[idx]))

        string = t_str['april1'] + t[0] + t_str['april2'] + t[1] + t_str['april3'] + t[2] + t_str['april4'] + t_str[
            'distance_row']
        if with_text:
            string += t_str['text1'] + d[0] + t_str['text2'] + d[1] + t_str['text3'] + d[2] + t_str['text4']
        else:
            string += t_str['notext1'] + t_str['notext2'] + t_str['notext3'] + t_str['text4']

        return string

    time = "{:%Y%m%d-%H%M}".format(datetime.now())
    src = 'data/latex/template.tex'
    filename = 'output/AprilTags_' + time + '.tex'
    copyfile(src, filename)

    output = open(filename, 'a')
    output.write(codecs.decode(t_str['AprilTagIDTextFront'], 'unicode_escape'))
    output.write(codecs.decode(t_str['AprilTagIDNoTextFront'], 'unicode_escape'))
    output.write(codecs.decode(t_str['AprilTagIDText'], 'unicode_escape'))

    for tag_id in range(start, end+1, tagsppage):
        tag_types = []
        traffic_sign_types = []
        for in_page_idx in range(tagsppage):
            tag_types.append(apriltags_db[tag_id + in_page_idx]['tag_type'])
            if apriltags_db[tag_id]['traffic_sign_type'] is not None:
                traffic_sign_types.append(apriltags_db[tag_id]['traffic_sign_type'])
            else:
                traffic_sign_types[in_page_idx].append('empty')

        # Write either 6 apriltags or 3 apriltags and 3 pictures on the front page
        # TODO: add possibility to specify single ids
        tag_ids = list(range(tag_id, tag_id + tagsppage))
        output.write(codecs.decode(t_str['new_page'], 'unicode_escape'))
        if withpicture:
            output.write(codecs.decode(create_tags(tags=traffic_sign_types, with_text=False), 'unicode_escape'))
            output.write(codecs.decode(t_str['distance_row'], 'unicode_escape'))
            output.write(codecs.decode(create_tags(tags=tag_ids, with_text=False), 'unicode_escape'))
        else:
            output.write(codecs.decode(create_tags(tags=tag_ids[0:3],
                                     text_ids=[_id - offset for _id in tag_ids[0:3]],
                                     with_text=True), 'unicode_escape'))
            output.write(codecs.decode(t_str['distance_row'], 'unicode_escape'))
            output.write(codecs.decode(create_tags(tags=tag_ids[3:],
                                     text_ids=[_id - offset for _id in tag_ids[3:]],
                                     with_text=True), 'unicode_escape'))

        output.write(codecs.decode(t_str['end_page'], 'unicode_escape'))

        # This writes the IDs on the next page, either 6 or 3
        output.write(codecs.decode(t_str['new_page'], 'unicode_escape'))
        if withpicture:
            output.write(codecs.decode(create_tags(tags=['empty']*3, with_text=False), 'unicode_escape'))
            output.write(codecs.decode(t_str['distance_row'], 'unicode_escape'))
            output.write(codecs.decode(create_tags(tags=['empty']*3,
                                     text_ids=[_id - offset for _id in tag_ids[0:3]],
                                     with_text=True), 'unicode_escape'))
        else:
            output.write(codecs.decode(create_tags(tags=['empty']*3, with_text=False), 'unicode_escape'))
            output.write(codecs.decode(t_str['distance_row'], 'unicode_escape'))
            output.write(codecs.decode(create_tags(tags=['empty']*3, with_text=False), 'unicode_escape'))

        output.write(codecs.decode(t_str['end_page'], 'unicode_escape'))

    output.write(codecs.decode('\\end{document}', 'unicode_escape'))
    output.close()


if __name__ == '__main__':
    main()
