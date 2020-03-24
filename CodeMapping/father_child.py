# -*- coding: utf-8 -*-
import os
import os.path
import gzip
import json
import jmespath
import time
 
def read_gz_file(path):
    if os.path.exists(path):
        with gzip.open(path, 'r') as pf:
            for line in pf:
                yield line
    else:
        print('the path [{}] is not exist!'.format(path))


def query(json_data):
    # with open('test.json','r') as fp:
    #   json_data = json.load(fp)
    Q_father_item_id = 'claims.P279[*].mainsnak.datavalue.value.id'  # P279:subclass of, P31: instance of
    Q_child_item_id = 'id'
    Q_child_item_name = 'labels.en.value'
    Q_en_page = 'sitelinks.enwiki'

    child_item_id = jmespath.search(Q_child_item_id, json_data)
    child_item_name = jmespath.search(Q_child_item_name, json_data)
    father_item_id = jmespath.search(Q_father_item_id, json_data)
    en_page = jmespath.search(Q_en_page, json_data)

    return child_item_id,child_item_name, father_item_id, en_page

if __name__ == '__main__':
    con = read_gz_file('D:\\Datasets\\wikidata-20180827-all.json.gz')
    id_name_dict = {}
    child_father_dict = {}
    i = 0
    starttime = time.time()
    if getattr(con, '__iter__', None):
        for line in con:
            i += 1
            data = line.decode('utf-8')

            if not data.startswith('[') and not data.startswith(']'):
                if data.endswith(',\n'):
                    json_data = json.loads(data[:-2])
                else:
                    json_data = json.loads(data[:-1])
                # print(json_data)
                child_id, child_name, father_id, en_page = query(json_data)
                if en_page is None:
                    continue
                '''
                if father_id:

                    child_father_dict[child_id] = father_id
                '''
                if child_name:
                    id_name_dict[child_id] = child_name
                    if father_id:
                        child_father_dict[child_id] = father_id
            print(id_name_dict)          
            print('%d done'%i)

    # write id--name to file
    #output = open('id_name_wikidata.txt', 'w', encoding='utf-8')
    for key in id_name_dict.keys():
        print(key)
        output.write(key + '\t' + id_name_dict[key] + '\n')
    #output.close()

    ''''
    # A_id subclass of B_id
    output = open('A_subclass_B_id.txt', 'w', encoding='utf-8')
    for key in child_father_dict.keys():
        father_id = child_father_dict[key]
        if isinstance(father_id, list):
            for id in father_id:
                output.write(key + '\t' + id + '\n')
        else:
            output.write(key + '\t' + father_id + '\n')
    output.close()
    #endtime = time.time()
    #print(endtime - starttime)
    '''
'''
    # A_name is father of B_name
    output = open('result_en.txt', 'w', encoding='utf-8')
    for key in child_father_dict.keys():
#        print(key)
        father_id = child_father_dict[key]
        child_name = id_name_dict[key]
        if isinstance(father_id, list):
            for id in father_id:
                if id in id_name_dict.keys():
                    output.write(id + '\t' + id_name_dict[id] + '\t||\t' + key + '\t' + child_name + '\n')
        else:
            if father_id in id_name_dict.keys():
                output.write(father_id + '\t' + id_name_dict[father_id] + '\t||\t' + key + '\t' + child_name + '\n')
    output.close()
    print('Done')
    endtime = time.time()
    print(endtime - starttime)
    
'''
