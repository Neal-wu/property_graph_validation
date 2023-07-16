import json

# based on the edge of source gp of ggd, search the same edge from G, and then based on the fromID and toID to search the corresponding fromLabel and toLabel, check whether this two 
# lables are the same as the labels of source gp, if they are same then we find a match, if not search for another edge. 
# When we retrive a match, we need to validate whether the target gp exists in G, so we use the edge of target gp to search the same edge in G, if we can't find one, then return FALSE, 
# if we find the edge, then we need to based on this edge to search the corresponding labels in G and compare whether they are as same as the labels in target gp. 
# IF they are the same, then it is validated, if not then violated. 
# To return TRUE, for each match, it has to be validated.

# get source gp of ggd: source edge, fromLabel, toLabel
# get target gp of ggd: target edge and target toLabel
# for edge in edges of G: retrive each match of source gp from G
#  
#       if edge != source edge:
#           continue (skip the current iteration and search for another edge)
#       else:
#           if fromLabel != source fromLabel or toLabel != source toLabel:
#               continue (skip the current iteration and search for another edge) 
#           else (a source match is retrived):
#             
#               for edge in edges of G (search for target edge)
#                   if edge != target edge:
#                       continue
#                   else:
#                       if fromLabel != source fromLabel or toLabel != target toLabel:
#                           continue
#                       else:
#                           break (this match satisfy target gp and is validated, break the loop)
#               else:
#                   return False (no target match)
#               
#               continue
# return True (no match needs to be validated)

# Limitations: 1. The solution did not consider source and target contrains which should always exist in the ggd, even though they might be empty; 
# 2. The solution only consider the situation that there is only one ggd in the input;
# 3. The solution did not condider the situation that the target graph pattern might be empty;
# 4. The solution did not condider the situation that the property graph can be empty;
# 4. The solution is limited by the formats of ggd and property graph, which means the algorithm should change when the formats change;
# 5. The solution requests that for each node in property graph, it should have unique identifier which is 'id'.

# read json file
def read_json(filename):

    with open(filename, "r") as json_file:
        data = json.load(json_file)

    return data

# get source gp of ggd: source edge, fromLabel, toLabel
def get_source_gp(ggd):

    source_edge = ggd['sourceGP'][0]['edges'][0]['label']
    source_fromVariable = ggd['sourceGP'][0]['edges'][0]['fromVariable']
    source_toVariable = ggd['sourceGP'][0]['edges'][0]['toVariable']
    source_vertice_dict = ggd['sourceGP'][0]['vertices']
    for value_dict in source_vertice_dict:
        variable = value_dict['variable']
        if variable == source_fromVariable:
            source_fromLabel = value_dict['label']
        if variable == source_toVariable:
            source_toLabel = value_dict['label']

    return source_edge, source_fromLabel, source_toLabel

# get target gp of ggd: target edge, fromLabel, toLabel
def get_target_gp(ggd):

    target_edge = ggd['targetGP'][0]['edges'][1]['label']
    target_fromVariable = ggd['targetGP'][0]['edges'][1]['fromVariable']
    target_toVariable = ggd['targetGP'][0]['edges'][1]['toVariable']
    target_vertice_dict = ggd['targetGP'][0]['vertices']
    for value_dict in target_vertice_dict:
        variable = value_dict['variable']
        if variable == target_fromVariable:
            target_fromLabel = value_dict['label']
        if variable == target_toVariable:
            target_toLabel = value_dict['label']

    return target_edge, target_fromLabel, target_toLabel

# get property graph edge, fromLabel, toLabel
def get_pg_edge_info(pg_edge):

    pg_edge_label = pg_edge['label']
    pg_edge_fromId = pg_edge['fromId']
    pg_edge_toId = pg_edge['toId']

    return pg_edge_label, pg_edge_fromId, pg_edge_toId

# pg edge fromId, toId -> pg vertices fromLabel, toLabel
def id_label(pg, id):

    for vertice in pg['vertices']:
        if vertice['id'] == id:
            return vertice['label']

def validate_ggd(pg, source_edge, source_fromLabel, source_toLabel, target_edge, target_fromLabel, target_toLabel):

    for pg_source_edge in pg['edges']:
        pg_source_edge_label, pg_source_edge_fromId, pg_source_edge_toId = get_pg_edge_info(pg_source_edge)
        if pg_source_edge_label != source_edge:
            continue
        else:
            pg_source_fromLabel = id_label(pg, pg_source_edge_fromId)
            pg_source_toLabel = id_label(pg, pg_source_edge_toId)
            if pg_source_fromLabel != source_fromLabel or pg_source_toLabel != source_toLabel:
                continue 
            else:
    # there is a source match, validate target match
                for pg_target_edge in pg['edges']:
                    pg_target_edge_label, pg_target_edge_fromId, pg_target_edge_toId = get_pg_edge_info(pg_target_edge)
                    if pg_target_edge_label != target_edge:
                        continue
                    else:
                        pg_target_edge_toLabel = id_label(pg, pg_target_edge_toId)
                        if pg_target_edge_fromId != pg_source_edge_fromId or pg_target_edge_toLabel != target_toLabel:
                            continue
                        else:
                            break
                else:
                    return False
                
                continue
    return True 

if __name__=='__main__':

    # read ggd
    ggd_filename = 'input/ggd.json'
    ggd = read_json(ggd_filename)

    # read property graph
    pg_filename = 'input/pg.json'
    pg = read_json(pg_filename)

    # get source gp of ggd: source edge, fromLabel, toLabel
    source_edge, source_fromLabel, source_toLabel = get_source_gp(ggd)
    print('source_edge, source_fromLabel, source_toLabel >>>',source_edge, source_fromLabel, source_toLabel)
    # get target gp of ggd: target edge, fromLabel, toLabel
    target_edge, target_fromLabel, target_toLabel =  get_target_gp(ggd)
    print('target_edge, target_fromLabel, target_toLabel >>>', target_edge, target_fromLabel, target_toLabel)
        
    # get the validation result
    result = validate_ggd(pg, source_edge, source_fromLabel, source_toLabel, target_edge, target_fromLabel, target_toLabel)

    if result == True:
        print("Yes, d holds on G")

    else: 
        print("No, d does not hold on G")

    # print('finished!')