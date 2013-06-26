import xml.etree.ElementTree as ET

NAMESPACE = '{urn:xmind:xmap:xmlns:content:2.0}'


class Topic(object):
    ''' base class for topic'''
    def __init__(self, title, children):
        super(Topic, self).__init__()
        self._title = title
        self._children = children

    def get_children(self):
        return self._children

    def get_title(self):
        return self._title


def parse_node(element):
    node_title = element.find(NAMESPACE + 'title').text
    node_children = element.find(NAMESPACE + 'children')
    return Topic(node_title, node_children)


def main():

    try:
        tree = ET.parse('content.xml')
        root = tree.getroot()

        #going through each sheet
        for sheet in root:

            # sheet container and title
            topic_root = parse_node(sheet.find(NAMESPACE + 'topic'))
            sheet_title = sheet[1].text
            print 'Sheet title: ' + sheet_title
            print topic_root.get_title()

            sheet_end = False
            topic_current = topic_root
            level = 0
            children_attached = None
            children_detached = None

            while sheet_end is False:

                if topic_current.get_children() is not None:

                    topic_current_children = topic_current.get_children().findall(NAMESPACE + 'topics')

                    for inner_topics_xml in topic_current_children:

                        if inner_topics_xml.get('type') == 'attached':
                            children_attached = inner_topics_xml.findall(NAMESPACE + 'topic')

                            for inner_topic_xml in children_attached:
                                _topic = parse_node(inner_topic_xml)
                                print _topic.get_title()

                        elif inner_topics_xml.get('type') == 'detached':
                            children_detached = inner_topics_xml.findall(NAMESPACE + 'topic')

                else:
                    sheet_end = True


            #{urn:xmind:xmap:xmlns:content:2.0}title
            print '-----------------------------'
            print ''

    except Exception, e:
        print e

if __name__ == '__main__':
    main()
