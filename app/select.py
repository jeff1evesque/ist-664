#!/usr/bin/python

'''

select.py, select specified data from mongodb endpoint.

'''


from bson.code import Code

def select(client, database, collection):
    # database + collection
    db = client[database]
    col = db[collection]

    # emit the 'values' to the reduce
    map = Code('''
        function() {
          if (
            this.body != 'repost' &&
            this.body != '[deleted]' &&
            this.body != '[removed]'
          ) {
            emit(
              this.link_id,
              {
                'id': [this.id],
                'score': [this.score],
                'parent_id': [this.parent_id],
                'body': [this.body],
                'comment': [this.body]
              }
            );
          }
        }
    ''')

    #
    # @to (key), the parent post
    # @from (value), reply to parent posts
    #
    reduce = Code('''
        function (key, values) {
          var results = { posts: [], comments: [], match_id: [], score: [] };
          for (var i = 0; i < values.length; i++) {
            if (
              values[i] &&
              values[i].body &&
              values[i].parent_id
            ) {
              var comment = values[i].body;
              var score = values[i].score;
              var wantedParent = values[i].parent_id[0].split('_')[1];
              for (var j = 0; j < values.length; j++) {
                if (
                    values[j] &&
                    values[j].body &&
                    values[j].body != values[i].body &&
                    wantedParent == values[j].id
                ) {
                  //
                  // posts + comments: collapse all whitespace to single
                  //     whitespace, then append to array.
                  //
                  results.posts = results.posts.concat(
                    values[j].body[0].replace(/\s+/g, ' ').trim().split(/[ ,]+/)
                  );
                  results.comments = results.comments.concat(
                    comment[0].replace(/\s+/g, ' ').trim().split(/[ ,]+/)
                  );
                  results.match_id = results.match_id.concat(wantedParent);
                  results.score = results.score.concat(score);
                }
              }
            }
          }

          if (
            results.posts.length > 0 &&
            results.comments.length > 0 &&
            results.match_id.length > 0 &&
            results.score.length > 0
          ) {
            return { results };
          }
        }
    ''')

    # finalize: remove single case (reducer skipped)
    finalize = Code('''
        function finalize(key, values) {
          if (
            values &&
            values.results &&
            values.results.posts &&
            values.results.comments &&
            values.results.posts[0].length > 0 &&
            values.results.comments[0].length > 0 &&
            values.results.posts[0] != values.results.comments[0]
          ) {
            return values.results;
          }
        }
    ''')

    # select data
    return col.map_reduce(
        map=map,
        reduce=reduce,
        finalize=finalize,
        out='to_from'
    )
