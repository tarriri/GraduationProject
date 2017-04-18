from peewee import *

database = SqliteDatabase('/GraduationProject/NewsAnalysis/GraduationProject/project.db', **{})
# database = SqliteDatabase('project.db', **{})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Collectednews(BaseModel):
    articletext = TextField(db_column='ArticleText')
    url = TextField(db_column='Url')

    class Meta:
        db_table = 'CollectedNews'

class Platform(BaseModel):
    commentaryurl = TextField(db_column='CommentaryUrl')
    deleted = BooleanField(db_column='Deleted')
    name = TextField(db_column='Name')
    newscssclass = TextField(db_column='NewsCSSClass')
    newsdomelement = TextField(db_column='NewsDOMElement')
    objectid = PrimaryKeyField(db_column='ObjectId')
    urldomain = TextField(db_column='UrlDomain')

    class Meta:
        db_table = 'Platform'

class Urlinformation(BaseModel):
    iscollected = BooleanField(db_column='IsCollected', null=True)  # bit
    objectid = PrimaryKeyField(db_column='ObjectId')
    platformid = ForeignKeyField(db_column='PlatformId', rel_model=Platform, to_field='objectid')
    urltext = TextField(db_column='UrlText')

    class Meta:
        db_table = 'UrlInformation'

class SqliteSequence(BaseModel):
    name = UnknownField(null=True)  # 
    seq = UnknownField(null=True)  # 

    class Meta:
        db_table = 'sqlite_sequence'


def get_platform_list():
    return Platform.select().where(Platform.deleted == 0)


def get_url_information_list():
    return Urlinformation.select().where(Urlinformation.iscollected == 0)


def get_platform_by_domain(domain):
    try:
        return Platform.get(Platform.urldomain == domain)
    except DoesNotExist:
        return None


def get_platform_by_object_id(object_id):
    try:
        return Platform.get(Platform.objectid == object_id)
    except DoesNotExist:
        return None


def mark_as_collected_url(object_id):
    query = Urlinformation.update(iscollected=1).where(Urlinformation.objectid == object_id)
    query.execute()


@database.transaction()
def create_collected_news(text, url):
    Collectednews.create(articletext=text, url=url)


@database.transaction()
def create_url_information(url, platform_id):
    Urlinformation.create(iscollected=False, urltext=url, platformid=platform_id)
