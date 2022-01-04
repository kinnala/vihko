# vihko

This is a simple offline version of `digabi/rich-text-editor`.  A Flask
application serves the content of `static/` and a variant of
https://math-demo.abitti.fi/.
The variant has been modified to send periodically the contents of the text
area to the Flask backend which saves them to a file.

<center><img src="https://user-images.githubusercontent.com/973268/148090191-72e45352-a8a9-4f2e-9910-19eb0660985b.png" /></center>

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

## Licensing

My contributions to `app.py` are in
the public domain.
`rich-text-editor` has the following license:
```
Copyright 2017 Matriculation Examination Board, Finland

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
The licenses of the remaining components (BSD/MIT) are included
in the respective folders and files under `/static` and inside `/windows.zip`.
