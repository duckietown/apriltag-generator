import os

import yaml


def get_useful_ids(DB_copy, set):
    """Extracts required IDs from database.

    Given a particular required set, looks for the required amount of tags of each required type,
    when the match is found, it saves the relative ID to a list and remove the particular tag from the database.
    If the entire sets finds enough matches, it returns a list of the matched IDs and the shortened database, otherwise
    it return 0.

    Args:
        DB_copy (:obj:`list`): list of dicts containing the signs database
        set (:obj:`dict`): dict containing how many signs of which type are required by set

    Return:
        DB_copy (:obj:`list`): shortened list of dicts containing the signs database
        int_IDs (:obj:`list`): list of matched IDs

    """

    total_tags = sum(set.values())

    for required_sign, required_amount in set.items():
        # Check if we still need a certain sign
        while required_amount:

            if required_sign == 'empty':
                tag = DB_copy[-1]
                useful_IDs.append(tag['tag_id'])
                required_amount -= 1

            else:
                # Find match
                i = next((i for i, tag in enumerate(DB_copy) if tag["traffic_sign_type"] == required_sign), None)

                if i:
                    tag = DB_copy[i]
                    # If we have a match, save the id, reduce the required number and remove it from list
                    useful_IDs.append(tag['tag_id'])
                    required_amount -= 1
                    DB_copy.pop(i)
                else:
                    # No match was found
                    return 0, DB_copy

    # Return the ids of the last N of the list
    int_IDs = useful_IDs[-total_tags:]
    return int_IDs, DB_copy


def save_id_list(filename, id_list):
    """Saves list of ids to a file.

    Args:
        filename (:obj:`str`): filename (csv) where the data is saved
        id_list (:obj:`list`): list of ids to be saved

    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    file_ = open(filename, "w")
    print(filename, id_list)
    row = ','.join([str(i) for i in id_list])
    file_.write(row)
    file_.close()


if __name__ == '__main__':

    config_dir = os.path.join('data', 'config')
    lists_dir = os.path.join('data', 'lists')

    # Load the database
    database_file = os.path.join(config_dir, 'apriltagsDB.yaml')
    with open(database_file, 'r') as stream:
        try:
            apriltagsDB = yaml.load(stream, Loader=yaml.SafeLoader)
        except yaml.YAMLError as exc:
            print(exc)

    # Load the intersection definitions
    set_specs_file = os.path.join(config_dir, 'set_specs.yaml')
    with open(set_specs_file, 'r') as stream:
        try:
            intersections = yaml.load(stream, Loader=yaml.SafeLoader)
        except yaml.YAMLError as exc:
            print(exc)

    # We create a copy of the DB so we can pop values safely
    apriltagsDB_copy = apriltagsDB.copy()
    useful_IDs = []

    # First we create the set for the duckiebox
    duckiebox_file = os.path.join(lists_dir, 'duckiebox_signs.csv')
    intersection_IDs, apriltagsDB_copy = get_useful_ids(apriltagsDB_copy, intersections['duckiebox_signs'])
    if intersection_IDs:
        save_id_list(duckiebox_file, intersection_IDs)
    else:
        print('Not enough tags left! Stopping.')
        exit(1)
    # Then we create any special set we need
    special_set_file = os.path.join(lists_dir, 'special_set.csv')
    intersection_IDs, apriltagsDB_copy = get_useful_ids(apriltagsDB_copy, intersections['special_set'])
    if intersection_IDs:
        save_id_list(special_set_file, intersection_IDs)
    else:
        print('Not enough tags left!Stopping!')
        exit(1)
    # We create as many intersections as possible, always a 4 way then a 3 way
    int_number = 0
    while True:
        intersection_name = ''.join(['4_intersection_', str(int_number), '.csv'])
        intersection_file = os.path.join(lists_dir, intersection_name)
        intersection_IDs, apriltagsDB_copy = get_useful_ids(apriltagsDB_copy, intersections['intersection4way'])
        if intersection_IDs:
            save_id_list(intersection_file, intersection_IDs)
        else:
            print('Not enough tags left! Stopping..')
            exit(1)

        intersection_name = ''.join(['3_intersection_', str(int_number), '.csv'])
        intersection_file = os.path.join(lists_dir, intersection_name)
        intersection_IDs, apriltagsDB_copy = get_useful_ids(apriltagsDB_copy, intersections['intersection3way'])
        if intersection_IDs:
            save_id_list(intersection_file, intersection_IDs)
        else:
            print('Not enough tags left! Stopping...')
            exit(1)

        # Increase count for file naming
        int_number += 1

