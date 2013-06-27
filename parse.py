#! /usr/bin/env python

from mekk.xmind import XMindDocument


def get_children(elem):

    if elem is not None and elem.get_subtopics():
        for t in elem.get_subtopics():
            yield t
    else:
        yield None


def main():

    xmind = XMindDocument.open("mmaps.xmind")

    for sheet in xmind.get_all_sheets():

        print "Sheet title: ", sheet.get_title()

        root = sheet.get_root_topic()
        print "Root title: ", root.get_title()
        print "Root note: ", root.get_note()
        level = ''

        for topic in root.get_subtopics():
            print "* ", topic.get_title()
            #print "   label: ", topic.get_label()
            #print "   link: ", topic.get_link()
            #print "   markers: ", list(topic.get_markers())

            #level 1
            for topic_1 in topic.get_subtopics():
                print "** ", topic_1.get_title()

                #level 2
                for topic_2 in topic_1.get_subtopics():
                    print "***", topic.get_title()

                    #level 3
                    for topic_3 in topic_2.get_subtopics():
                        print "****", topic.get_title()

            print ''
            print '----------------------------'

if __name__ == '__main__':
    main()
