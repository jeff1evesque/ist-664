#!/usr/bin/python

'''

select.py, select specified data from mongodb endpoint.

'''


from pymongo import MongoClient
from bson.code import Code

def select(client):
    map = Code(
        "function () {"
        "  emit("
        "    'jeffbob',"
        "    {"
        "      'id': this.id,"
        "      'parent_id': this.parent_id,"
        "      'body': this.body,"
        "    }"
        "  );"
        "}"
    )

    #
    # @to (key), the parent comment
    # @from (value), reply to parent comment
    #
    reduce = Code(
        "function (key, values) {"
        "  var results = {'to': [], 'from': []};"
        "  for (var i = 0; i < values.length; i++) {"
        "    wantedKey = 'parent_id';"
        "    wantedVal = values[i].parent_id.split('_',1)[1];"
        "    for(var j = 0; j < values.length; j++) {"
        "      if ("
        "        values[j].hasOwnProperty(wantedKey) &&"
        "        values[j][wantedKey] === wantedVal &&"
        "        values[j].body != values[i].body"
        "      ) {"
        "        results.to.push(values[j].body);"
        "        results.from.push(values[i].body);"
        "      }"
        "    }"
        "  }"
        "  return {"
        "    'id': 'jeff',"
        "    'parent_id': this.parent_id,"
        "    'body': this.body,"
        "  }"
        "}"
    )

    # select data
    return col.map_reduce(map, reduce, 'to_from')

