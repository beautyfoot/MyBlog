from django.test import TestCase

# Create your tests here.



# a = [{"name": "egon"}, {"name": "leo"}]
#
# print(a)
#
# l = {"name": "batman"}
#
# a.append(l)
#
# print(a)
#
# l["name"] = "spiderman"
#
# print(a)

comment_list = [

    {"id": 1, "content": "111", "Pid": None, "children_comment": []},
    {"id": 2, "content": "222", "Pid": None, "children_comment": []},
    {"id": 3, "content": "333", "Pid": None, "children_comment": []},
    {"id": 4, "content": "444", "Pid": 1, "children_comment": []},
    {"id": 5, "content": "555", "Pid": 1, "children_comment": []},
    {"id": 6, "content": "666", "Pid": 4, "children_comment": []},
    {"id": 7, "content": "777", "Pid": 3, "children_comment": []},
    {"id": 8, "content": "888", "Pid": 7, "children_comment": []},
    {"id": 9, "content": "999", "Pid": None, "children_comment": []},

]

comment_list2 = {}
for comment in comment_list:
    comment_list2[comment["id"]] = comment
    if comment["Pid"]:
        pid = comment["Pid"]
        comment_list2[pid]["children_comment"].append(comment)
    else:
        pass

print(comment_list)