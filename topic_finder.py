#! /usr/bin/python3
import os


def get_documents(year, filename):
    documents_list = []
    global topics
    global undef_count

    read_file = open('output2/' + str(year) + '/' + filename, 'r')

    line = read_file.readline()
    while line != '':
        line = line.strip()
        if(line == '<DOC>'):
            document = []

            # Add date to document
            document.append(filename.strip('.txt') + ' ' + str(year))

            # Add title to document
            line = read_file.readline().strip()
            line = line.lstrip('<DOC_NAME>')
            line = line.rstrip('</DOC_NAME>')
            document.append(line)

            # Add contents to document
            read_file.readline()
            line = read_file.readline().strip()
            parts = line.rsplit('Topics', 1)
            read_file.readline()

            topic = ''

            if len(parts) == 1:
                document.append(parts[0])
                undef_count += 1
                document.append('UNDEFINED')
            else:
                document.append(parts[0])
                topic = parts[1].rsplit('First posted')[0]

                topic = topic.rsplit('More stories')[0]
                topic = ''.join(i for i in parts[1] if not i.isdigit())
                topic = topic.strip(' ')
                topic = topic.split(' ')[0]

                if topic not in topics:
                    topics.append(topic)

                document.append(topic)

            read_file.readline()

            documents_list.append(document)

            line = read_file.readline()
        else:
            print('Should never get here!\n')

    read_file.close()
    return documents_list

def main():
    global topics
    doc_count = 0
    if not os.path.exists('topics/'):
        os.makedirs('topics/')

    for year in range(2003, 2016):

        if not os.path.exists('topics/' + str(year)):
            os.makedirs('topics/' + str(year))

        for filename in os.listdir('output2/' + str(year)):

            document_list = get_documents(year, filename)
            doc_count += len(document_list)

            new_file = open('topics/' + str(year) + '/' + filename, 'w')

            for document in document_list:
                new_file.write('<Date>' + document[0] + '</Date>\n')
                new_file.write('<Title>' + document[1] + '</Title>\n')
                new_file.write('<Contents>' + document[2] + '</Contents>\n')
                new_file.write('<Topic>' + document[3] + '</Topic>\n')

            new_file.close()

    print(str(doc_count) + '\n')
    print(topics)
    print(str(undef_count))

if __name__ == '__main__':
    topics = []
    undef_count = 0
    main()
