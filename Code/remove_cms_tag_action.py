"""
remove_cms_tag_action
Author :ywu
Date : 3/6/2024:08:29
project : pycharm

this function is used to delete all cms provisionde svc-tag-action and svc-match-list on EXA. the profiles are begin with @***. find and remove
"""
import re
import time

from e7_ont_telnet import *


# match_list = """service match-list "@123":
# Untagged Rules:
# Rule Source MAC                                   EtherType  VPI  VCI
# ---- -------------------------------------------- ---------- ---- ------
# 2    12:24:38:00:11:12 (mask: ff:ff:ff:00:00:00)  any        none none
# 3    <any MAC> (mask: ff:ff:ff:00:00:00)          any        none none
# 4    <any MAC> (mask: <none>)                     any        none none
#
# Tagged Rules:
# Rule Outer Tag
# ---- --------------------------
# 4    ignore VLAN, p-bit: 0
# 5    ignore VLAN, p-bit: 1
# 6    ignore VLAN, p-bit: 2
# 7    ignore VLAN, p-bit: 3
# 8    ignore VLAN, p-bit: 4
# 9    ignore VLAN, p-bit: 5
# 10   ignore VLAN, p-bit: 6
# 11   ignore VLAN, p-bit: 7
# 12   ignore VLAN & p-bit"""


def get_svc_tag():
    res = exa.exa_cli('show svc-tag-action ')
    # print(f'tag action result is {res}')
    return res

def del_found_tag_action():
    res = exa.exa_cli('show svc-tag-action ')
    tag = re.findall('(@.*? )',res)
    print(f'tag action with @ is {tag}')
    for item in tag:
        exa.exa_cli('delete svc-tag-action ' + item)
        time.sleep(1)

def found_svc_match_list():
    res = exa.exa_cli('show svc-match-list ')
    tag = re.findall('service match-list "(@.*?)"',res)
    print(f'svc match list with @ is {tag} *******')
    return tag


def deprecate_found_rule_in_matchlist(match_list_name):
    """not used, replaced by found_rule_in_matchlist """
    mlist = exa.exa_cli('show svc-match-list ' + match_list_name)
    time.sleep(3)
    print(f'match list {match_list_name} has content {mlist}')
    rule_num = re.findall("\n(\d+) ",mlist,re.S)
    print(f'rule number in match list {match_list_name} is {rule_num}')
    # if re.findall(tag_p,match_list_name,re.S):
    #     tag = 1
    # else:
    #     tag = 0
    # if re.findall(untag_p,match_list_name,re.S):
    #     utag = 1
    # else:
    #     utag = 0
    # # print(tag,utag)
    return rule_num

def deprecate_remove_rule_from_matchlist_add_delete(match_list_name):
    """not used, replaced by remove_rule_from_matchlist_add_delete """
    match_list_name = '"'+match_list_name+'"'
    print(f'match list name is {match_list_name}')
    # match_list = exa.exa_cli('show svc-match-list '+ match_list_name)
    rule_num =found_rule_in_matchlist(match_list_name)
    if len(rule_num) ==0:
        exa.exa_cli('delete svc-match-list ' + match_list_name)
    else:
        for item in rule_num:
            exa.exa_cli('remove untagged-rule '+ item + ' from-svc-match-list ' + match_list_name)
            time.sleep(1)
        for item in rule_num:
            exa.exa_cli('remove tagged-rule ' + item + ' from-svc-match-list ' + match_list_name)
            time.sleep(1)
        exa.exa_cli('delete svc-match-list ' + match_list_name)



def delete_tag_action():
    host = '10.245.37.198'
    username = b'e7'
    password = b'admin'
    exa = E7telnet(host, 23)
    exa.telnetEXA(host, 23, username, password)
    time.sleep(3)
    exa.exa_cli('set session pager disabled')
    time.sleep(1)
    """delete tag action with @"""
    del_found_tag_action()




def delete_match_list():
    """use found_svc_match_list() to find all svc match list start with @ and use remove_rule_from_matchlist_add_delete to delete them """
    svc_matc_list = found_svc_match_list()
    for item in svc_matc_list:
        print(f'match list {item} will be deleted')
        remove_rule_from_matchlist_add_delete(item)


def found_rule_in_matchlist(match_list_name):
    """seperate the svc match list with tagged rule, the first one is for untagged rule, the second one is for tagged rule. finf each part rule number and return """
    mlist = exa.exa_cli('show svc-match-list ' + match_list_name)
    time.sleep(3)
    res = re.split("Tagged Rules:", mlist, re.S)
    # res= match_list.split('Tagged Rules:')
    untag_rule=re.findall('\n(\d+)',res[0],re.S)
    tag_rule=re.findall('\n(\d+)',res[1],re.S)
    return untag_rule,tag_rule

def remove_rule_from_matchlist_add_delete(match_list_name):
    """some match list name contain space, so need to add "" to include it """
    match_list_name = '"'+match_list_name+'"'
    print(f'match list name is {match_list_name}')
    untag_rule,tag_rule =found_rule_in_matchlist_1(match_list_name)
    if len(untag_rule) ==0:
        exa.exa_cli('delete svc-match-list ' + match_list_name)
    else:
        for item in untag_rule:
            exa.exa_cli('remove untagged-rule '+ item + ' from-svc-match-list ' + match_list_name)
            time.sleep(1)
        exa.exa_cli('delete svc-match-list ' + match_list_name)

    if len(tag_rule) ==0:
        exa.exa_cli('delete svc-match-list ' + match_list_name)
    else:
        for item in tag_rule:
            exa.exa_cli('remove tagged-rule '+ item + ' from-svc-match-list ' + match_list_name)
            time.sleep(1)
        exa.exa_cli('delete svc-match-list ' + match_list_name)


if __name__ == '__main__':
    host = '10.245.37.198'
    username = b'e7'
    password = b'admin'
    exa = E7telnet(host, 23)
    exa.telnetEXA(host, 23, username, password)
    time.sleep(3)
    exa.exa_cli('set session pager disabled')
    time.sleep(1)
    delete_match_list()







