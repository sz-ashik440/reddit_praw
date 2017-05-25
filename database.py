from peewee import *

DB = MySQLDatabase('reddit', host='localhost', port=3306, user="root", passwd="admin123", use_unicode=True, charset='utf8')


class Sub_Cring(Model):
    title = CharField(null=False)
    url = CharField(null=False)

    class Meta:
        database = DB
        primary_key = False


def add_to_table(title, url):
    DB.connect()
    cring = Sub_Cring(title=title, url=url)

    if Sub_Cring.table_exists() is False:
        DB.create_table(Sub_Cring)

    cring.save()
    DB.close()


if __name__ == "__main__":
    DB.connect()
    # db.create_tables([Sub_Cring])

    cring1 = Sub_Cring(title='Some Title', url='https://www.someurl.com')
    cring1.save()
    DB.close()
