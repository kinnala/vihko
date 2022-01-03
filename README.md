# vihko

This is a simple offline version of `digabi/rich-text-editor`.  A Flask
application serves the content of `static/` and a variant of
https://math-demo.abitti.fi/.
The variant has been modified to send periodically the contents of the text
area to the Flask backend which saves them to a file.

## Installation

### Windows

Download `vihko-windows-*.zip` under
[releases](https://github.com/kinnala/vihko/releases).  Unzip the package and
launch the backend via the shortcut `vihko.lnk`.

### Linux & macOS

If you have Python 3.7 or greater, you can use the development version by
cloning the repository and installing the dependencies, i.e. `pip install -r
requirements.txt`.  The backend is launched as follows: `python app.py`.

## Instructions

A new browser tab is opened after launching the backend.  You can open a new or
an existing page by writing its name in the input box below the editor.
Existing names can be found in the dropdown menu.  The page is saved
automatically every 5 seconds to a HTML file under `<installation
directory>/sivut/`.  When closing the application you should also close the
backend.  Launching multiple instances of the application may lead to confusion
because nothing prevents them from modifying the same pages.
