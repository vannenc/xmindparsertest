import xml.etree.ElementTree as ET

NAMESPACE = '{urn:xmind:xmap:xmlns:content:2.0}'


def parse_node(element):
    node_title = element.find(NAMESPACE + 'title').text
    node_children = element.find(NAMESPACE + 'children')

    print node_title
    print node_children

    return {'title': node_title, 'children': node_children}


def main():
    try:
        tree = ET.parse('content.xml')
        root = tree.getroot()

        #going through each sheet
        for sheet in root:

            # sheet container and title
            topics_container = \
                sheet.find(NAMESPACE + 'topic')
            sheet_title = sheet[1].text
            print 'Sheet title: ' + sheet_title

            #topic, title
            topic_root_title = topics_container.find(NAMESPACE + 'title').text
            topics_root = topics_container.find(NAMESPACE + 'children')

            print 'root topic title: >' + topic_root_title

            topics_children_attached = None
            topics_children_detached = None

            if len(topics_root) > 1:

                for child in topics_root:

                    if child.get('type') == 'attached':
                        topics_children_attached = child

                    elif child.get('type') == 'detached':
                        topics_children_detached = child

            else:
                topics_children_attached = topics_root[0]

            for child in topics_children_attached:
                first_pass = parse_node(child)
                sheet_end = False

                if 'children' in first_pass:

                    topic_children = first_pass['children']

                    while sheet_end is False:
                        tmp = parse_node(topic_children)
                        print tmp

                        if 'children' in tmp and tmp['children'] is not None:

                            topic_children = tmp['children']
                        else:
                            sheet_end = True

            #{urn:xmind:xmap:xmlns:content:2.0}title
            print '-----------------------------'
            print ''

    except Exception, e:
        print e

if __name__ == '__main__':
    main()
