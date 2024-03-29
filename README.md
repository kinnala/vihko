<center><img src="https://user-images.githubusercontent.com/973268/148241958-c0cdbf08-2155-4bac-bcea-bc9952aa2df5.png" alt="vihko" /></center>

This is a simple offline version of `digabi/rich-text-editor`.  A Python
application serves the content of `static/` and a variant of
https://math-demo.abitti.fi/.
The contents of the text
area are saved periodically to a file.

## Usage

A new browser tab is opened after launching the application.  You can open a new or
an existing page by writing its name into the input box below the editor.
Existing names can be found in the dropdown menu.  The page is saved
automatically every 5 seconds to a HTML file under `<installation
directory>/sivut/`.  Remember to close the backend when closing the application.
Launching multiple instances of the application may lead to confusion
because they might modify the same pages.

## Installation

### Windows

Download `vihko-windows-*.zip` under
[releases](https://github.com/kinnala/vihko/releases).  Unzip the package and
launch the backend via the shortcut `vihko.lnk`.

### Linux & macOS

If you have Python 3.7 or greater, you can use the development version by
cloning the repository and installing the dependencies, i.e. `pip install -r
requirements.txt`.  The backend is launched as follows: `python app.py`.

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
