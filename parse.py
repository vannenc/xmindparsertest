#! /usr/bin/env python

from mekk.xmind import XMindDocument

import sqlite3

DATABASE = 'business.db'
CONNECTION = None
TOPIC_DELIMITER = '$$'


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
def add_sheet(sheetyear, root_title):

    if CONNECTION is not None:

        c = CONNECTION.cursor()

        if c is not None:

            c.execute('INSERT INTO sheet VALUES(NULL, ?, ?)',
                     (sheetyear, root_title))
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
            c.execute('UPDATE topic set answer= ? WHERE topic_id = ? ',
                     (1, topic_id))
            CONNECTION.commit()

            print 'answer: ..' + str(topic_id)
            c.close()


@connect
def add_topic(sheet_id, topic_name, topic_parent,
              is_answer, level, order, visible_menu):

    if CONNECTION is not None:

        c = CONNECTION.cursor()

        if c is not None:

            try:
                if topic_parent is None and is_answer is None:
                    c.execute('INSERT INTO topic\
                                (topic_id, name, parent, answer,\
                                    sheet_id, level, topic_order,\
                                                    visible_menu )\
                                    VALUES \
                                    (NULL, ?, NULL, NULL, ?, ?, ?, ?)',
                             (topic_name, sheet_id, level,
                              order, visible_menu))

                elif topic_parent is None and is_answer is not None:
                    c.execute('INSERT INTO topic\
                                (topic_id, name, parent, answer,\
                                    sheet_id, level, topic_order,\
                                                    visible_menu )\
                                    VALUES \
                                    (NULL, ?, NULL, ?, ?, ?, ?, ?)',
                             (topic_name, is_answer,
                              sheet_id, level, order, visible_menu))

                elif topic_parent is not None and is_answer is None:
                    c.execute('INSERT INTO topic\
                                (topic_id, name, parent, answer,\
                                    sheet_id, level, topic_order,\
                                                    visible_menu )\
                                    VALUES \
                                    (NULL, ?, ?, NULL, ?, ?, ?, ?)',
                             (topic_name, topic_parent,
                              sheet_id, level, order, visible_menu))

                else:
                    # id, name, parent, answer, sheet_id
                    c.execute('INSERT INTO topic\
                                (topic_id, name, parent, answer,\
                                    sheet_id, level, topic_order,\
                                                    visible_menu )\
                                    VALUES (NULL, ?, ?, ?,\
                                                         ?, ?, ? ,?)',
                             (topic_name, topic_parent,
                              is_answer, sheet_id, level, order, visible_menu))

                CONNECTION.commit()
                last_rowid = c.lastrowid
                c.close()
                return last_rowid

            except Exception, e:
                print e
                raise e

        else:
            return -1


def process_xmind_file(xmind_file='mmaps.xmind'):

    xmind = XMindDocument.open(xmind_file)

    for sheet in xmind.get_all_sheets():

        print "Sheet title: ", sheet.get_title()

        root = sheet.get_root_topic()
        root_title = root.get_title()
        print "Root title: ", root.get_title()
        print "Root note: ", root.get_note()
        level = 0

        #add year and question title
        sheet_id = add_sheet(sheet.get_title(), root_title)

        #direct parent, that is the titles
        for topic in root.get_subtopics():
            topic_name = r'' + topic.get_title()
            print "* ", topic.get_title()

            visible_in_menu = 1
            level = 0
            is_ignored = False
            is_numbered = False
            topic_number = 0
            internal_topic_number = 0

            #split to find numbering and any ignore flag
            topic_name_parts = topic_name.split(TOPIC_DELIMITER)
            topic_name_parts_len = len(topic_name_parts)

            if topic_name_parts_len == 4:
                topic_name = topic_name_parts[3].strip()
                is_ignored = True

                try:
                    topic_number = int(topic_name_parts[1])
                    is_numbered = True

                except:
                    print 'Error parsing number in topic ' + topic_name
                    is_numbered = False

            elif topic_name_parts_len == 3:
                topic_name = topic_name_parts[2].strip()
                is_ignored = False

                try:
                    topic_number = int(topic_name_parts[1])
                    is_numbered = True

                except:
                    print 'Error parsing number in topic ' + topic_name
                    is_numbered = False

            else:
                is_numbered = False
                is_ignored = False

            if is_numbered is False:
                internal_topic_number += 1
                topic_number = internal_topic_number

            if is_ignored is True:
                visible_in_menu = 0

            topic_id = add_topic(sheet_id=sheet_id,
                                 topic_name=topic_name,
                                 topic_parent=None,
                                 is_answer=False,
                                 level=level,
                                 order=topic_number,
                                 visible_menu=visible_in_menu)
            #increment order
            print 'Number: ' + str(topic_number) + ' -' + str(topic_id)

            #children nodes, that's the answers
            for topic_1 in topic.get_subtopics():
                topic_1_name = topic_1.get_title()
                level = 1
                topic_1_id = add_topic(sheet_id=sheet_id,
                                       topic_name=topic_1_name,
                                       topic_parent=topic_id,
                                       is_answer=1,
                                       level=level,
                                       order=topic_number,
                                       visible_menu=0)

                print 'Answer: ' + str(topic_1_id)

            print ''
            print '----------------------------'


if __name__ == '__main__':
    process_xmind_file()
