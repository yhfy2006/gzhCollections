import json

class WeikouArticle(object):
    title = ''
    author_link = ''
    author_name = ''
    # author_id = ''
    image_url = ''
    content = ''

    
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4, ensure_ascii=False)
    def to_DICT(self):
        return json.loads(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)
