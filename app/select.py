#!/usr/bin/python

'''

select.py, select specified data from mongodb endpoint.

'''


from bson.code import Code

def select(client, database, collection):
    # database + collection
    db = client[database]
    col = db[collection]

    #
    # nonunique 'collapsed' key combines all documents within
    #     the same collection.
    #
    # Note: 'comment' is a needed structure by the below reducer.
    #
    map = Code('''
        function() {
          emit(
            this.link_id,
            {
              'id': this.id,
              'score': this.score,
              'parent_id': this.parent_id,
              'body': this.body,
              'comment': this.body,
            }"
          );"
        '''}
    )

    #
    # @to (key), the parent post
    # @from (value), reply to parent posts
    #
    reduce = Code('''
        function (key, values) {
          var results = { posts: [], comments: [], match_id: [], score: [], link_id: key };
          return {values};
        '''}
    )

    # select data
    return col.map_reduce(map, reduce, 'to_from')
