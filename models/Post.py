class Post:
    def __init__(self, authorid, id, title, author, tags, preview, content, comments, created_utc):
        self.authorid = authorid
        self.id = id
        self.title = title
        self.author = author
        self.tags = tags
        self.preview = preview
        self.content = content
        self.comments = comments
        self.created_utc = created_utc

    def addtags(self, tags):
        self.tags = tags

    def addauthor(self, author):
        self.author = author

    def addcomments(self, comments):
        self.comments = comments