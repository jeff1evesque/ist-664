#!/usr/bin/python

'''

select.py, select specified data from mongodb endpoint.

'''


from bson.code import Code

def select(client, database, collection):
    # database + collection
    db = client[database]
    col = db[collection]

    ## nonunique 'collapsed' key combines all documents
    map = Code(
        "function () {"
        "  emit("
        "    'collapsed',"
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
        "  var match_id = [];"
        "  for (var i = 0; i < values.length; i++) {"
        "    if ("
        "      values[i] &&"
        "      values[i].parent_id"
        "    ) {"
        "      var wantedParent = values[i].parent_id.split('_')[1];"
        "      for (var j = 0; j < values.length; j++) {"
        "        if ("
        "            wantedParent == values[j].id &&"
        "            values[j].body != values[i].body"
        "        ) {"
        "          replies.push(values[j].body);"
        "          comments.push(values[i].body);"
        "          match_id.push(wantedParent);"
        "        }"
        "      }"
        "    }"
        "  }"
        "  return {"
        "    'id': values[0].id,"
        "    'comments': comments,"
        "    'replies': replies,"
        "    'match_id': match_id,"
        "  }"
        "}"
    )

    # select data
    return col.map_reduce(map, reduce, 'to_from')
