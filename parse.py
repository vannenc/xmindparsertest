#! /usr/bin/env python

from mekk.xmind import XMindDocument


def main():

    xmind = XMindDocument.open("mmaps.xmind")

    sheet = xmind.get_first_sheet()
    print "Sheet title: ", sheet.get_title()

    root = sheet.get_root_topic()
    print "Root title: ", root.get_title()
    print "Root note: ", root.get_note()
    level = ''

    for topic in root.get_subtopics():
        print "* ", topic.get_title()
        print "   label: ", topic.get_label()
        print "   link: ", topic.get_link()
        print "   markers: ", list(topic.get_markers())

        for topic in topic.get_subtopics():
            print "** ", topic.get_title()


if __name__ == '__main__':
    main()
