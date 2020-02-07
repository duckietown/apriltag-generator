def tag_writer(id_, tag_type, street_name, vehicle_name, sign_type):
    yaml.write('- tag_id: ' + str(id_) + '\n')
    yaml.write('  tag_type: ' + tag_type + '\n')
    yaml.write('  street_name: ' + street_name + '\n')
    yaml.write('  vehicle_name: ' + vehicle_name + '\n')
    yaml.write('  traffic_sign_type: ' + sign_type + '\n')
    yaml.write('\n')


yaml = open('newDB.yaml', 'w+')
tag_type = 'Localization'
start = 300
end = 400
for id in range(start, end):
    tag_writer(id, tag_type, '', '', '')
