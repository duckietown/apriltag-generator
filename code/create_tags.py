import codecs
import csv
from datetime import datetime
import os
import pandas as pd
import numpy as np
from shutil import copyfile

from utils.creator_utils import build_tags, load_file, get_parser, Bunch


def main():

    # Paths
    strings_file = os.path.join('data', 'latex', 'latex_strings.yaml')
    template_file = os.path.join('data', 'latex', 'template.tex')
    database_file = os.path.join('data', 'config', args.database_name)

    if args.withpicture:
        tagsppage = 3
    else:
        tagsppage = 6

    offset = args.offset

    # Load Apriltags database
    apriltags_db = load_file(database_file)

    # Load latex strings
    t_str = load_file(strings_file)

    t_str['AprilTagIDTextFront'] = ''.join([t_str['AprilTagIDTextFront_pre'],
                                            str(args.id_text),
                                            t_str['AprilTagIDTextFront_post']])

    time = "{:%Y%m%d-%H%M}".format(datetime.now())

    # If a specific set name is define, use as filename, else the config name, if nothing is specified, datetime.
    if args.set_name:
        out_file = args.set_name + '.tex'
    elif args.config:
        out_file = args.config + '.tex'
    else:
        out_file = 'AprilTags_' + time + '.tex'
    out_file = os.path.join('output', out_file)
    copyfile(template_file, out_file)

    output = open(out_file, 'a')
    output.write(codecs.decode(t_str['AprilTagIDTextFront'], 'unicode_escape'))
    output.write(codecs.decode(t_str['AprilTagIDNoTextFront'], 'unicode_escape'))
    output.write(codecs.decode(t_str['AprilTagIDText'], 'unicode_escape'))

    # If you requested a set of IDs with a proper name, load it
    if args.config and args.set_name:
        set_file = os.path.join('data', 'lists', args.set_name + '.csv')
        tag_list = list(np.squeeze(pd.read_csv(set_file, header=None).values))
        tag_list = [int(i) for i in tag_list]
    else:
        tag_list = range(args.start, args.end)

    for idx in range(0, len(tag_list), tagsppage):
        tag_types = []
        traffic_sign_types = []
        for in_page_idx in range(tagsppage):
            real_index = tag_list[idx + in_page_idx]
            tag_types.append(apriltags_db[real_index]['tag_type'])
            if apriltags_db[real_index]['traffic_sign_type'] is not None:
                traffic_sign_types.append(apriltags_db[real_index]['traffic_sign_type'])
            else:
                traffic_sign_types.append('empty')

        # Write either 6 apriltags or 3 apriltags and 3 pictures on the front page
        output.write(codecs.decode(t_str['new_page'], 'unicode_escape'))
        tag_ids = tag_list[idx:idx+tagsppage]
        pdf_ids = [id_ + 1 for id_ in tag_ids]
        if args.withpicture:
            output.write(codecs.decode(build_tags(tags=traffic_sign_types,
                                                  with_text=False,
                                                  t_str=t_str), 'unicode_escape'))
            output.write(codecs.decode(t_str['distance_row'], 'unicode_escape'))
            output.write(codecs.decode(build_tags(tags=pdf_ids[:],
                                                  with_text=False,
                                                  t_str=t_str), 'unicode_escape'))
        else:
            output.write(codecs.decode(build_tags(tags=pdf_ids[0:3],
                                                  text_ids=[_id - offset for _id in pdf_ids[0:3]],
                                                  with_text=True, t_str=t_str), 'unicode_escape'))
            output.write(codecs.decode(t_str['distance_row'], 'unicode_escape'))
            output.write(codecs.decode(build_tags(tags=pdf_ids[3:],
                                                  text_ids=[_id - offset for _id in pdf_ids[3:]],
                                                  with_text=True, t_str=t_str), 'unicode_escape'))

        output.write(codecs.decode(t_str['end_page'], 'unicode_escape'))

        # This writes the IDs on the next page, either 6 or 3
        output.write(codecs.decode(t_str['new_page'], 'unicode_escape'))
        if args.withpicture:
            output.write(codecs.decode(build_tags(tags=['empty']*3,
                                                  with_text=False,
                                                  t_str=t_str), 'unicode_escape'))
            output.write(codecs.decode(t_str['distance_row'], 'unicode_escape'))
            output.write(codecs.decode(build_tags(tags=['empty']*3,
                                                  text_ids=[_id - offset for _id in pdf_ids[::-1]],
                                                  with_text=True, t_str=t_str), 'unicode_escape'))
        else:
            output.write(codecs.decode(build_tags(tags=['empty']*3,
                                                  with_text=False,
                                                  t_str=t_str), 'unicode_escape'))
            output.write(codecs.decode(t_str['distance_row'], 'unicode_escape'))
            output.write(codecs.decode(build_tags(tags=['empty']*3,
                                                  with_text=False,
                                                  t_str=t_str), 'unicode_escape'))

        output.write(codecs.decode(t_str['end_page'], 'unicode_escape'))

    output.write(codecs.decode('\\end{document}', 'unicode_escape'))
    output.close()


if __name__ == '__main__':
    # Parse user input
    parser = get_parser()
    args = parser.parse_args()

    # If a config file is specified, it overwrites the parsed args and their defaults
    if args.config:
        pdf_specs = os.path.join('data', 'config', 'pdf_specs.yaml')
        config_dict = load_file(pdf_specs)

        # If a set is required, we load it and throw error if not specified
        if args.config == 'set':
            assert args.set_name, 'If you specify a set, you need to pass its name as argument'
            config_dict[args.config]['set_name'] = args.set_name
        args = Bunch(config_dict[args.config])

    main()
