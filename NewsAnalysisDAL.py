from peewee import *

database = MySQLDatabase('NewsAnalysis', **{'password': '**********', 'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Platform(BaseModel):
    commentaryurl = CharField(db_column='CommentaryUrl', null=True)
    deleted = IntegerField(db_column='Deleted', null=True)
    name = CharField(db_column='Name')
    newscssclass = CharField(db_column='NewsCSSClass')
    newsdomelement = CharField(db_column='NewsDOMElement')
    objectid = PrimaryKeyField(db_column='ObjectId')
    urldomain = CharField(db_column='UrlDomain')

    class Meta:
        db_table = 'Platform'

def get_platform_list():
    return Platform.select().where(Platform.deleted == 0)


def get_platform_by_domain(domain):
    try:
        return Platform.get(Platform.urldomain == domain)
    except DoesNotExist:
        return None
