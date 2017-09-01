import sublime
import sublime_plugin
import os
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import pathname2url
from urllib.request import url2pathname
from collections import OrderedDict
from .languageServer import *
from .event_hub import EventHub
debug = True


def plugin_name():
    return 'dxmate'


def dxProjectFolder():
    for window in sublime.windows():
        open_folders = window.folders()
        for folder in open_folders:
            for root, dirs, files in os.walk(folder, topdown=False):
                for name in files:
                    if name == 'sfdx-project.json':
                        return folder
    return ''


def run_events():
    if dxProjectFolder() != '':
        return True
    return False

def active_file():
    return sublime.active_window().active_view().file_name()


def active_file_extension():
    current_file = active_file()
    file_name, file_extension = os.path.splitext(current_file)
    return file_extension


def file_extension(view):
    if view and view.file_name():
        file_name, file_extension = os.path.splitext(view.file_name())
        return file_extension


def get_plugin_folder():
    packages_path = os.path.join(sublime.packages_path(), plugin_name())
    debug(packages_path)
    return packages_path


def get_syntax_folder():
    plugin_folder = get_plugin_folder()
    syntax_folder = os.path.join(plugin_folder, "sublime", "lang")
    debug(syntax_folder)
    return syntax_folder


def filename_to_uri(path: str) -> str:
    return urljoin('file:', pathname2url(path))


def uri_to_filename(uri: str) -> str:
    return url2pathname(urlparse(uri).path)


def get_document_position(view, point):
    if point:
        (row, col) = view.rowcol(point)
    else:
        view.sel()
    uri = filename_to_uri(view.file_name())
    position = OrderedDict(line=row, character=col)
    dp = OrderedDict()  # type: Dict[str, Any]
    dp["textDocument"] = {"uri": uri}
    dp["position"] = position
    debug('position:', dp)
    return dp


def debug(*args):
    """Print args to the console if the "debug" setting is True."""
    if debug:
        print(*args)


def handle_close():
    if dxProjectFolder() == '':
        client.kill()


EventHub.subscribe('on_pre_close', handle_close)


