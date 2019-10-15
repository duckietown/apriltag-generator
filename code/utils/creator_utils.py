import yaml


def load_file(path):
    data = None
    with open('data/' + path + '.yaml', 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return data

