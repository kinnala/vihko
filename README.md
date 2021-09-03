# vihko

This is a simple offline version of `digabi/rich-text-editor`.  A Flask
application serves the content of `static/` and a variant of
https://math-demo.abitti.fi/.
The variant has been modified to send periodically the contents of the text
area to the Flask backend which saves them to a file.
