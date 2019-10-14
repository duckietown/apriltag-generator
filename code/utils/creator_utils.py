import yaml


def load_file(path):
    with open('../data/' + path + '.yaml', 'r') as stream:
        try:
            data = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return data

