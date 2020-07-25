import logging
import re
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem

logger = logging.getLogger(__name__)


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


def listwidget_item(text, data):
    item = QListWidgetItem()
    item.setText(text)
    item.setData(Qt.UserRole, data)
    return item


def listwidget_text_items(listwidget):
    for i in range(listwidget.count()):
        yield listwidget.item(i).text()


def listwidget_data_items(listwidget):
    for i in range(listwidget.count()):
        yield listwidget.item(i).data(Qt.UserRole)


def noop_action(source, dest):
    logger.info(f"noop_action('{source}', '{dest}')")
    return


def relative_symlink(source, dest):
    relsource = os.path.relpath(source, dest)
    return os.symlink(relsource, dest)
