import re

def longest_common_prefix(*strings):
    end = 0
    for c in zip(*strings):
        if len(set(c)) != 1:
            break
        end += 1
    return strings[0][:end]

def guess_title(*titles):
    result = longest_common_prefix(*titles)
    result = re.fullmatch(r'([\[(].*?[\])])?(.*)', result).group(2)  # Strip leading [] and ()
    result = re.fullmatch(r'[^a-zA-Z0-9]*(.*?)[^a-zA-Z0-9]*', result).group(1) # Strip non-word characters
    result = result.replace('_', ' ')
    return result

def listwidget_items(listwidget):
    for i in range(listwidget.count()):
        yield listwidget.item(i).text()
