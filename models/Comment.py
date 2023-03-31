class Comment:
    def __init__(self, postid, id, author, content, created_utc):
        self.postid = postid
        self.id = id
        self.author = author
        self.content = content
        self.created_utc = created_utc

    def addname(self, name):
        self.author = name