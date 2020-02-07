import argparse
import yaml


def build_tags(tags=None, text_ids=None, with_text=None, t_str=None):
    assert tags is not None, "You need to provide some tags!"
    assert tags is not None, "You need to provide some tags!"
    if with_text:
        assert text_ids is not None, "If you want to write ids, provide some text!"

    t = []
    d = []
    for idx, tag in enumerate(tags):
        if type(tag) != int:
            t.append("\\Picture{" + str(tag) + ".png")
            if with_text:
                d.append(str(text_ids[idx]))
        else:
            t.append("\\AprilTagPicture{" + str(int(tag)))
            if with_text:
                d.append(str(text_ids[idx]))

    string = t_str['april1'] + t[0] + t_str['april2'] + t[1] + t_str['april3'] + t[2] + t_str['april4'] + t_str[
        'distance_row']
    if with_text:
        string += t_str['text1'] + d[0] + t_str['text2'] + d[1] + t_str['text3'] + d[2] + t_str['text4']
    else:
        string += t_str['notext1'] + t_str['notext2'] + t_str['notext3'] + t_str['text4']

    return string


def load_file(filename):
    data = None
    with open(filename, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return data


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int,
                        default=1,
                        help="Tag number to start with, min is 1")
    parser.add_argument("--end",
                        type=int,
                        default=6,
                        help="Tag number to end with, max is 511")
    parser.add_argument("--withpicture",
                        action="store_true",
                        default="False",
                        help="Remove picture")
    parser.add_argument("--id_text",
                        default="Tag ID",
                        help="String written under Apriltag")
    parser.add_argument("--offset",
                        type=int,
                        default=1,
                        help="Offset in numbering, 400 for Autobots, 1 for localization (front text)")
    parser.add_argument("--database_name",
                        default="apriltagsDB",
                        help="Yaml file containing IDs informations")
    parser.add_argument("--config",
                        default='',
                        type=str,
                        help='Pass name of configuration specified in pdf-specs.yaml')
    parser.add_argument("--set_name",
                        default='',
                        type=str,
                        help='Pass name of the required set')
    return parser


class Bunch(object):
    def __init__(self, d):
        self.__dict__.update(d)
