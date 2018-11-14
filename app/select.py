#!/usr/bin/python

'''

select.py, select specified data from mongodb endpoint.

'''


from bson.code import Code

def select(client, database, collection):
    # database + collection
    db = client[database]
    col = db[collection]

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
        "  wantedKey = 'parent_id';"
        "  var comments = [];"
        "  var replies = [];"
        "  for (var i = 0; i < values.length; i++) {"
        "    if ("
        "      values[i] &&"
        "      values[i].parent_id"
        "    ) {"
        "      wantedVal = values[i].parent_id.split('_')[1];"
        "      for (var j = 0; j < values.length; j++) {"
        "        if ("
        "            values[j].id === wantedVal &&"
        "            values[j].body != values[i].body"
        "        ) {"
        "          comments.push(values[j].body);"
        "          replies.push(values[j].body);"
        "        }"
        "      }"
        "    }"
        "  }"
        "  return {"
        "    'id': values[0].id,"
        "    'comments': comments,"
        "    'replies': replies,"
        "    'wanted_val': wantedVal"
        "  }"
        "}"
    )

    # select data
    return col.map_reduce(map, reduce, 'to_from')
