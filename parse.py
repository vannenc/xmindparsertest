#! /usr/bin/env python

from mekk.xmind import XMindDocument

import sqlite3

DATABASE = 'business.db'
CONNECTION = None


def connect(f):

    def inner_func(*args, **kwargs):
        global CONNECTION
        global DATABASE

        if CONNECTION is None:
            CONNECTION = sqlite3.connect(DATABASE)

        return f(*args, **kwargs)

    return inner_func


def prepare_connection():
    global CONNECTION

    if CONNECTION is None:
        CONNECTION = sqlite3.connect(DATABASE)


def close_connection():
    global CONNECTION

    if CONNECTION is not None:
        CONNECTION.commit()
        CONNECTION.close()


def get_children(elem):

    if elem is not None and elem.get_subtopics():
        for t in elem.get_subtopics():
            yield t
    else:
        yield None


def fetch():

    if CONNECTION is not None:

        c = CONNECTION.cursor()
        recordset = c.execute('select * from business')

        for row in recordset:
            print row


@connect
def add_sheet(sheetyear):

    if CONNECTION is not None:

        c = CONNECTION.cursor()

        if c is not None:

            c.execute('INSERT INTO paper_year VALUES(NULL, "%s")' % sheetyear)
            CONNECTION.commit()

            last_rowid = c.lastrowid
            c.close()
            return last_rowid
        else:
            return -1


@connect
def make_topic_answer(topic_id):

    if CONNECTION is not None:
        c = CONNECTION.cursor()

        if c is not None:
            c.execute('UPDATE topic set answer= ? WHERE topic_id = ? ', (1, topic_id))
            CONNECTION.commit()

            print 'answer: ..' + str(topic_id)
            c.close()


@connect
def add_topic(sheet_id, topic_name, topic_parent, is_answer):

    if CONNECTION is not None:

        c = CONNECTION.cursor()

        if c is not None:

            try:
                if topic_parent is None and is_answer is None:
                    c.execute('INSERT INTO topic VALUES \
                                    (NULL, ?, NULL, NULL, ?)',
                             (topic_name, sheet_id))

                elif topic_parent is None and is_answer is not None:
                    c.execute('INSERT INTO topic VALUES \
                                    (NULL, ?, NULL, ?, ?)',
                             (topic_name, is_answer, sheet_id))

                elif topic_parent is not None and is_answer is None:
                    c.execute('INSERT INTO topic VALUES \
                                    (NULL, ?, ?, NULL, ?)',
                             (topic_name, topic_parent, sheet_id))

                else:
                    # id, name, parent, answer, sheet_id
                    c.execute('INSERT INTO topic VALUES (NULL, ?, ?, ?, ?)',
                             (topic_name, topic_parent, is_answer, sheet_id))

                CONNECTION.commit()
                last_rowid = c.lastrowid
                c.close()
                return last_rowid

            except Exception, e:
                raise e

        else:
            return -1


def main():

    xmind = XMindDocument.open("mmaps.xmind")

    for sheet in xmind.get_all_sheets():

        print "Sheet title: ", sheet.get_title()

        root = sheet.get_root_topic()
        print "Root title: ", root.get_title()
        print "Root note: ", root.get_note()
        level = ''

        sheet_id = add_sheet(sheet.get_title())

        for topic in root.get_subtopics():
            topic_name = r'' + topic.get_title()
            print "* ", topic.get_title()

            topic_id = add_topic(sheet_id=sheet_id,
                                 topic_name=topic_name,
                                 topic_parent=None,
                                 is_answer=False)

            #level 1
            for topic_1 in topic.get_subtopics():
                topic_1_name = topic_1.get_title()

                topic_1_id = add_topic(sheet_id=sheet_id,
                                       topic_name=topic_1_name,
                                       topic_parent=topic_id,
                                       is_answer=False)
                topic_1_children = True
                topic_2_children = False

                #level 2
                for topic_2 in topic_1.get_subtopics():

                    topic_2_name = topic_2.get_title()
                    topic_2_id = add_topic(sheet_id=sheet_id,
                                           topic_name=topic_2_name,
                                           topic_parent=topic_1_id,
                                           is_answer=False)
                    topic_2_children = True
                    topic_3_children = False

                    #level 3
                    for topic_3 in topic_2.get_subtopics():
                        print 'topic_3_id'
                        topic_3_name = topic_2.get_title()
                        topic_3_id = add_topic(sheet_id=sheet_id,
                                               topic_name=topic_3_name,
                                               topic_parent=topic_2_id,
                                               is_answer=1)
                        topic_3_children = True

                    #if level2 has no child
                    if topic_3_children is False:
                        make_topic_answer(topic_2_id)

                #if level1 has no child
                if topic_2_children is False:
                    make_topic_answer(topic_1_id)

            print ''
            print '----------------------------'

if __name__ == '__main__':
    main()
