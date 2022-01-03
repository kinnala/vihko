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
launch the application via the shortcut `vihko.lnk`.

### Linux & macOS

If you have Python 3.7 or greater, you can use the development version by
cloning the repository and installing the dependencies, i.e. `pip install -r
requirements.txt`.  The application is launched as follows: `python app.py`.
