import sys
path = r'C:\MyGit\FileBrowser'
# add current tool path to the syspath so that it can be importted
if not path in sys.path:
    sys.path.append(path)

# import module
import FileBrowser
reload(FileBrowser)

# create the file browser
fb = FileBrowser.MyQtApp(True)
fb.show()