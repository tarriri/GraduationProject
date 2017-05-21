from peewee import *
import re

# database = SqliteDatabase('project.db', **{})
database = SqliteDatabase('/GraduationProject/NewsAnalysis/GraduationProject/project.db', **{})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Collectedarticles(BaseModel):
    article = TextField(db_column='Article')
    objectid = PrimaryKeyField(db_column='ObjectId')
    url = TextField(db_column='Url')

    class Meta:
        db_table = 'CollectedArticles'


class Collectednews(BaseModel):
    articletext = TextField(db_column='ArticleText')
    url = TextField(db_column='Url')

    class Meta:
        db_table = 'CollectedNews'


class Lsaresult(BaseModel):
    deleted = BooleanField(db_column='Deleted')
    objectid = PrimaryKeyField(db_column='ObjectId')
    result = TextField(db_column='Result')

    class Meta:
        db_table = 'LSAResult'


class Lsadataset(BaseModel):
    article = TextField(db_column='Article')
    deleted = BooleanField(db_column='Deleted')
    objectid = PrimaryKeyField(db_column='ObjectId')
    resultid = ForeignKeyField(db_column='ResultId', rel_model=Lsaresult, to_field='objectid')
    url = TextField(db_column='Url')

    class Meta:
        db_table = 'LSADataSet'


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
    iscollected = UnknownField(db_column='IsCollected', null=True)  # bit
    objectid = PrimaryKeyField(db_column='ObjectId')
    platformid = ForeignKeyField(db_column='PlatformId', rel_model=Platform, to_field='objectid')
    urltext = TextField(db_column='UrlText')

    class Meta:
        db_table = 'UrlInformation'


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


def update_lsa_result(object_id, text):
    query = Lsaresult.update(result=text).where(Lsaresult.objectid == object_id)
    query.execute()


def get_sample_document_list():
    news_list = Collectedarticles.select().order_by(fn.Random()).limit(10)
    result = []
    url_list = []
    for item in news_list:
        result.append(re.sub(r'[^a-zA-Z]', " ", item.article))
        url_list.append(item.url)
    return result, url_list


@database.transaction()
def create_collected_news(text, url):
    Collectedarticles.create(article=text, url=url)


@database.transaction()
def create_url_information(url, platform_id):
    Urlinformation.create(iscollected=False, urltext=url, platformid=platform_id)


@database.transaction()
def create_lsa_data_set(lsa_result_id, article, url):
    Lsadataset.create(resultid=lsa_result_id, article=article, url=url, deleted=False)


@database.transaction()
def create_lsa_result():
    r = Lsaresult.create(result="", deleted=False)
    return r.objectid
