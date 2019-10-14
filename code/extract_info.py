

import yaml

with open("apriltagsDB.yaml", 'r') as stream:
    try:
        apriltagsDB = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

print(apriltagsDB[1]['tag_id'])
