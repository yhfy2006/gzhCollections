import json

class WeixinAccount(object):
    accountName = ''
    aid = ''
    url = ''
    total_articles = 0
    last_week_read = 0
    last_modified_date = ''
    category = ''
    ctgTag = ''

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4, ensure_ascii=False)
    def to_DICT(self):
        return json.loads(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)