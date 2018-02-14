import re
schema = {"No": int, "Source": str, "Host": str, "Link": str, "Date(ET)": str, "Time(ET)": str, "LocalTime": str, "Category": str, "Author ID": str, "Author Name": str, "Author URL": str, "Authority": str, "Followers": int, "Following": int, "Age": str,
          "Gender": str, "Language": str, "Country": str, "Province/State": str, "City": str, "Location": str, "Sentiment": str, "Alexa Rank": int, "Alexa Reach": int, "Title": str, "Snippet": str, "Contents": str, "Summary": str, "Bio": str, "Unique ID": int, }

splitter = r'(?<=[0-9,"]),(?=[0-9,"])'
comma_splitter = r','


def rough_split(text):
    # print text
    if len(text) > 2:
        parts = []
        # print text
        if text[0] == '"':
            head = text[:2]
            body = text[2:]
            splitter_to_use = splitter
        elif text[0] == ',':
            head = ""
            body = text
            splitter_to_use = comma_splitter
        else:
            head = ""
            body = text
            splitter_to_use = splitter
        split_result = re.split(splitter_to_use, body, maxsplit=1)
        while len(split_result) == 2:
            head += split_result[0]
            parts.append(head)
            text = split_result[1]
            if not text:
                break
            # print text
            if text[0] == '"':
                head = text[:2]
                body = text[2:]
                splitter_to_use = splitter
            elif text[0] == ',':
                head = ""
                body = text
                splitter_to_use = comma_splitter
            else:
                head = ""
                body = text
                splitter_to_use = splitter
            split_result = re.split(splitter_to_use, body, maxsplit=1)
        parts.append(text)
        # print parts
        return parts
    else:
        return [text]


def correct_split(init_result):
    # init_result = re.split(splitter, text)
    correct = []
    index = 0
    while index < len(init_result):
        next_index = index
        cur_part = init_result[index]
        if cur_part.startswith('"'):
            if cur_part.endswith('"'):
                correct.append(cur_part)
                index += 1
            else:
                next_index += 1
                while next_index < len(init_result):
                    if init_result[next_index].endswith('"'):
                        break
                    next_index += 1
                next_index += 1
                correct.append("".join(init_result[index:next_index]))
                index = next_index
        elif not cur_part.startswith('"'):
            if not cur_part.endswith('"'):
                correct.append(cur_part)
                index += 1
            else:
                next_index += 1
                while next_index < len(init_result):
                    if not init_result[next_index].endswith('"'):
                        break
                    next_index += 1
                next_index += 1
                correct.append("".join(init_result[index:next_index]))
                index = next_index
    return correct


def main():
    with open("./Archive 2/lunesta1.csv", "r") as csvfile:
        counter = 0
        headers = {}
        all_data = {}
        for line in csvfile:
            if counter == 0:
                row = line.split(",")
                if len(row) > 25 and row[0] == '"No"' and row[1] == '"Source"':
                    print "found header row"
                    for index, r in enumerate(row[:30]):
                        if r:
                            headers[index] = r.strip('"')
                            all_data[r.strip('"')] = []
                    counter += 1
            else:
                row = correct_split(rough_split(line))
                data_buffer = []
                use_buffer = True
                try:
                    for index, r in enumerate(row[:30]):
                        if index in headers:
                            if schema[headers[index]] == str:
                                if r:
                                    data_buffer.append(str(r.strip('"')))
                                else:
                                    data_buffer.append(str(""))
                            elif schema[headers[index]] == int:
                                if r:
                                    data_buffer.append(int(r))
                                else:
                                    data_buffer.append(0)
                except:
                    use_buffer = False
                    pass
                if use_buffer:
                    for index, r in enumerate(data_buffer):
                        all_data[headers[index]].append(r)
                    counter += 1
        print counter

if __name__ == '__main__':
    main()
