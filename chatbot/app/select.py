#!/usr/bin/python

'''

select.py, select specified data from mongodb endpoint

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
          const apostrophes = {
            "ain't": 'am not',
            "aren't": 'are not',
            "can't": 'cannot',
            "can't've": 'cannot have',
            "'cause": 'because',
            "could've": 'could have',
            "couldn't": 'could not',
            "couldn't've": 'could not have',
            "didn't": 'did not',
            "doesn't": 'does not',
            "don't": 'do not',
            "hadn't": 'had not',
            "hadn't've": 'had not have',
            "hasn't": 'has not',
            "haven't": 'have not',
            "he'd": 'he would',
            "he'd've": 'he would have',
            "he'll": 'he will',
            "he'll've": 'he will have',
            "he's": 'he is',
            "how'd": 'how did',
            "how'd'y": 'how do you',
            "how'll": 'how will',
            "how's": 'how is',
            "I'd": 'I would',
            "I'd've": 'I would have',
            "I'll": 'I will',
            "I'll've": 'I will have',
            "I'm": 'I am',
            "I've": 'I have',
            "isn't": 'is not',
            "it'd": 'it had',
            "it'd've": 'it would have',
            "it'll": 'it will',
            "it'll've": 'it will have',
            "it's": 'it is',
            "let's": 'let us',
            "ma'am": 'madam',
            "mayn't": 'may not',
            "might've": 'might have',
            "mightn't": 'might not',
            "mightn't've": 'might not have',
            "must've": 'must have',
            "mustn't": 'must not',
            "mustn't've": 'must not have',
            "needn't": 'need not',
            "needn't've": 'need not have',
            "o'clock": 'of the clock',
            "oughtn't": 'ought not',
            "oughtn't've": 'ought not have',
            "shan't": 'shall not',
            "sha'n't": 'shall not',
            "shan't've": 'shall not have',
            "she'd": 'she would',
            "she'd've": 'she would have',
            "she'll": 'she will',
            "she'll've": 'she will have',
            "she's": 'she is',
            "should've": 'should have',
            "shouldn't": 'should not',
            "shouldn't've": 'should not have',
            "so've": 'so have',
            "so's": 'so is',
            "that'd": 'that would',
            "that'd've": 'that would have',
            "that's": 'that is',
            "there'd": 'there had',
            "there'd've": 'there would have',
            "there's": 'there is',
            "they'd": 'they would',
            "they'd've": 'they would have',
            "they'll": 'they will',
            "they'll've": 'they will have',
            "they're": 'they are',
            "they've": 'they have',
            "to've": 'to have',
            "wasn't": 'was not',
            "we'd": 'we had',
            "we'd've": 'we would have',
            "we'll": 'we will',
            "we'll've": 'we will have',
            "we're": 'we are',
            "we've": 'we have',
            "weren't": 'were not',
            "what'll": 'what will',
            "what'll've": 'what will have',
            "what're": 'what are',
            "what's": 'what is',
            "what've": 'what have',
            "when's": 'when is',
            "when've": 'when have',
            "where'd": 'where did',
            "where's": 'where is',
            "where've": 'where have',
            "who'll": 'who will',
            "who'll've": 'who will have',
            "who's": 'who is',
            "who've": 'who have',
            "why's": 'why is',
            "why've": 'why have',
            "will've": 'will have',
            "won't": 'will not',
            "won't've": 'will not have',
            "would've": 'would have',
            "wouldn't": 'would not',
            "wouldn't've": 'would not have',
            "y'all": 'you all',
            "y'alls": 'you alls',
            "y'all'd": 'you all would',
            "y'all'd've": 'you all would have',
            "y'all're": 'you all are',
            "y'all've": 'you all have',
            "you'd": 'you had',
            "you'd've": 'you would have',
            "you'll": 'you you will',
            "you'll've": 'you you will have',
            "you're": 'you are',
            "you've": 'you have'
          },
          regexParts = [
              /(<([^>]+)>)/,
              /&gt;|&lt;/,
              /(https?:\/\/|https?;\/\/)?((?:www\.|(?!www)|[a-zA-Z]+\.)[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,})/,
              /(https?:\/\/|https?;\/\/)?((?:www\.|(?!www)|[a-zA-Z]+\.)[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,})/,
              /https?/,
              /[^\x01-\x7F]+/,
              /\$?[0-9]+|[0-9]{6,}|\s[0-9]\s/,
			  /\s-*\s|\s[\\\*]*\s|%|\s-\s|\s-|-\s|--|\?|!|\+|=|;|\]|\[|\(|\)|\*|\s\.|\s\.\s,|\s'|'\s|\"|_|\s-\s|\s\/\s|:|%|~|\\n|,|\.{2,}|\/{2,}|\s\/\s|\s\.\s/,
              /\s{2,}/
          ],
          regexString  = regexParts.map(function(x){return x.source}).join('|'),
          tokenRegex = new RegExp(regexString, 'g');

          var results = { posts: [], comments: [], match_id: [], scores: [] };
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
                  //     whitespace, remove bracket and parentheses, then
                  //     append tokenized sentence.
                  //
                  results.posts = results.posts.concat(
                    [values[j].body[0].replace(/(.*?)/g, function (match, capture) {
                      return apostrophes[capture];
                    }).replace(tokenRegex, ' ').replace(/\s{2,}/g, ' ').trim()]
                  );
                  results.comments = results.comments.concat(
                    [comment[0].replace(/(.*?)/g, function (match, capture) {
                      return apostrophes[capture];
                    }).replace(tokenRegex, ' ').replace(/\s{2,}/, ' ').trim()]
                  );

                  results.match_id = results.match_id.concat(wantedParent);
                  results.scores = results.scores.concat(score);
                }
              }
            }
          }

          if (
            results.posts.length > 0 &&
            results.comments.length > 0 &&
            results.match_id.length > 0 &&
            results.scores.length > 0
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
            values.results.posts[0] &&
            values.results.comments &&
            values.results.comments[0] &&
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