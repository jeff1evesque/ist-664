#!/usr/bin/python

'''

select.py, select specified data from mongodb endpoint.

'''


from bson.code import Code

def select(client, database, collection):
    # database + collection
    db = client[database]
    col = db[collection]

    ##
    ## nonunique 'collapsed' key combines all documents within
    ##     the same collection.
    ##
    map = Code(
        "function() {"
        "  emit("
        "    'collapsed',"
        "    {"
        "      'id': this.id,"
        "      'score': this.score,"
        "      'parent_id': this.parent_id,"
        "      'body': this.body"
        "    }"
        "  );"
        "}"
    )

    #
    # @to (key), the parent post
    # @from (value), reply to parent posts
    #
    reduce = Code(
        "function (key, values) {"
        "  var posts = [];"
        "  var comments = [];"
        "  var match_id = [];"
        "  for (var i = 0; i < values.length; i++) {"
        "    if ("
        "      values[i] &&"
        "      values[i].body &&"
        "      values[i].parent_id &&"
        "      values[i].body.trim() != '[deleted]'"
        "    ) {"
        "      var comment = values[i].body;"
        "      var wantedParent = values[i].parent_id.split('_')[1];"
        "      for (var j = 0; j < values.length; j++) {"
        "        if ("
        "            values[j] &&"
        "            values[j].body &&"
        "            values[j].body != values[i].body &&"
        "            values[j].body.trim() != '[deleted]' &&"
        "            wantedParent == values[j].id"
        "        ) {"
        "          posts = posts.concat(values[j].body);"
        "          match_id = match_id.concat(wantedParent);"
        "          comments = comments.concat(comment);"
        "        }"
        "      }"
        "    }"
        "  }"
        "  return {"
        "    posts: posts,"
        "    comments: comments,"
        "    match_id: match_id"
        "  };"
        "}"
    )

    # select data
    return col.map_reduce(map, reduce, 'to_from')
