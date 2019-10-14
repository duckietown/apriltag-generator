import yaml
import pdb

with open("apriltagsDB.yaml", 'r') as stream:
    try:
        apriltagsDB = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

intersection4way = {'stop':4,'t-light-ahead':4,'4-way-intersect':4,'T-intersection':0,'right-T-intersect':0,'left-T-intersect':0}
intersection3way = {'stop':3,'t-light-ahead':3,'4-way-intersect':0,'T-intersection':1,'right-T-intersect':1,'left-T-intersect':1}

apriltagsDB_copy = apriltagsDB.copy()
usefulIDs = list()
initialSize = len(apriltagsDB_copy)

def getUsefulIDs(apriltagsDB_copy,intersection,nIntersections,initial_size):
    shortList = list()
    while nIntersections > 0:
        nIntersections = nIntersections-1
        intersection_ = intersection.copy()
        while intersection_['stop']> 0:

            for element in apriltagsDB_copy[:]:
                if element['traffic_sign_type']=='stop':
                    if element['tag_id'] not in usefulIDs:
                        usefulIDs.append(element['tag_id'] )
                        break
            intersection_['stop'] = intersection_['stop']-1

        while intersection_['t-light-ahead']> 0:
            for element in apriltagsDB_copy:
                if element['traffic_sign_type']=='t-light-ahead':
                    if element['tag_id'] not in usefulIDs:
                        usefulIDs.append(element['tag_id'] )
                        break
            intersection_['t-light-ahead'] = intersection_['t-light-ahead']-1

        while intersection_['4-way-intersect']> 0:
            for element in apriltagsDB_copy:
                if element['traffic_sign_type']=='4-way-intersect':
                    if element['tag_id'] not in usefulIDs:
                        usefulIDs.append(element['tag_id'] )
                        break
            intersection_['4-way-intersect'] = intersection_['4-way-intersect']-1

        while intersection_['T-intersection']> 0:
            for element in apriltagsDB_copy:
                if element['traffic_sign_type']=='T-intersection':
                    if element['tag_id'] not in usefulIDs:
                        usefulIDs.append(element['tag_id'] )
                        break
            intersection_['T-intersection'] = intersection_['T-intersection']-1

        while intersection_['right-T-intersect']> 0:
            for element in apriltagsDB_copy:
                if element['traffic_sign_type']=='right-T-intersect':
                    if element['tag_id'] not in usefulIDs:
                        usefulIDs.append(element['tag_id'] )
                        break
            intersection_['right-T-intersect'] = intersection_['right-T-intersect']-1

        while intersection_['left-T-intersect']> 0:
            for element in apriltagsDB_copy:
                if element['traffic_sign_type']=='left-T-intersect':
                    if element['tag_id'] not in usefulIDs:
                        usefulIDs.append(element['tag_id'] )
                        break
            intersection_['left-T-intersect'] = intersection_['left-T-intersect']-1


    if intersection == intersection4way:
        shortList = usefulIDs.copy()
        shortList = shortList[-12:]

    if intersection == intersection3way:
        shortList = usefulIDs.copy()
        shortList = shortList[-9:]
    return shortList



for i in range(7):
    file = open("lists/4intersection_"+str(i)+".csv","w")
    listt = getUsefulIDs(apriltagsDB_copy,intersection4way,1,initialSize)
    print (listt)
    for element in listt:
        file.write(str(element)+",")
    file.close
    file = open("lists/3intersection_"+str(i)+".csv","w")
    listt = (getUsefulIDs(apriltagsDB_copy,intersection3way,1,initialSize))
    print (listt)
    for element in listt:
        file.write(str(element)+",")

    file.close()




#print (getUsefulIDs(intersection4way,1,usefulIDs))
