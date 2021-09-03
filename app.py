import urllib.parse
import random
import secrets
import time
import zipfile
import glob
import logging
import os.path
import webbrowser
from pathlib import Path
from io import BytesIO
from datetime import datetime
from flask import Flask, request, redirect, url_for, send_from_directory
import string

# printing lowercase
letters = string.ascii_lowercase
path = ''.join(random.choice(letters) for i in range(10))
app = Flask(__name__, static_url_path='')
app.logger.setLevel(logging.INFO)


@app.route('/{}/static/<path:path>'.format(path))
def send_static(path):
    return send_from_directory('static', path)


@app.route('/{}/save/<fid>'.format(path), methods=['POST'])
def save_answer(fid):
    app.logger.info("Saving {}".format(fid))
    with open("sivut/vihko_{}.html".format(fid), "w") as handle:
        handle.write(urllib.parse.unquote_plus(request.get_data()[7:].decode('utf-8')))
    return {}


@app.route('/{}/'.format(path))
def test():
    files = glob.glob('sivut/vihko_*.html')
    options = ""
    for fname in files:
        options += '<option value="{}">'.format(fname[len('sivut/vihko_'):-5])
    return r"""
<!DOCTYPE html>
<html>
<head>
  <title>Vihko</title>
  <script src="static/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
  <script>
  $(document).ready(function(){
    $(frm.txt).keyup(function(){
      $(frm).get(0).setAttribute('action', '/""" + path + r"""/edit/'+$(frm.txt).val());
    });
  });
  </script>
  <style>
    body { margin-top: 50px; font-family: sans-serif;}
    h1 {font-size: 2em; line-height: 2; margin-bottom: 4em;}
    .answer { border: 1px solid #aaa; padding: 5px; box-sizing: content-box; min-height: 100px; font: 17px "Times New Roman"; }
    .rich-text-editor img[src^="data:image/svg+xml"] { vertical-align: middle; margin: 4px; padding: 3px 10px; cursor: pointer; border: 1px solid transparent; }
    .rich-text-editor.rich-text-focused img[src^="data:image/svg+xml"],
    .rich-text-editor:focus img[src^="data:image/svg+xml"] { background: #EDF9FF; border: 1px solid #E6F2F8; }
    .rich-text-editor img[src*="data:image/png"] { margin: 4px; }
    .rich-text-editor:focus img[src*="data:image/png"],
    .rich-text-editor.rich-text-focused img[src*="data:image/png"] { box-shadow: 0 0 3px 1px rgba(0, 0, 0, .2); }
    .result { display: none; }
  </style>
</head>
<body>
  <h1>Vihko</h1>
  <p>Kirjoita sivun nimi alla olevaan kenttään:</p>
  <form id="frm" action=".">
    <input list="files" type="text" id="txt" />
    <datalist id="files">
""" + options + r"""
    </datalist>
    <input type="submit" id="sub" value="Avaa sivu" />
  </form>
</body>
</html>
"""


@app.route('/{}/edit/<fid>'.format(path))
def index(fid):
    fname = "sivut/vihko_{}.html".format(fid)
    if os.path.exists(fname):
        with open(fname, "r") as handle:
            answer = handle.read()
    else:
        answer = ""
        with open(fname, "w") as handle:
            handle.write("")
    files = glob.glob('sivut/vihko_*.html')
    options = ""
    for f in files:
        options += '<option value="{}">'.format(f[len('sivut/vihko_'):-5])
    return r"""
<!DOCTYPE html>
<html>
<head>
  <meta charset='utf-8'>
  <title>Vihko</title>
  <link rel="stylesheet" type="text/css" href="../static/mathquill.css">
  <link rel="stylesheet" type="text/css" href="../static/rich-text-editor.css"/>
  <script src="../static/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
  <script src="../static/Bacon.min.js"></script>
  <script src="../static/rich-text-editor-bundle.js"></script>
  <script type="text/javascript" src="../static/MathJax.js">
  </script>
  <script>
  $(document).ready(function(){
    $(frm.txt).keyup(function(){
      $(frm).get(0).setAttribute('action', '/""" + path + """/edit/'+$(frm.txt).val());
    });
  });
  </script>
  <style>
    body { margin-top: 50px; font-family: sans-serif;}
    h1 {font-size: 2em; line-height: 2; margin-bottom: 4em;}
    .answer { border: 1px solid #aaa; padding: 5px; box-sizing: content-box; min-height: 100px; font: 17px "Times New Roman"; }
    .rich-text-editor img[src^="data:image/svg+xml"] { vertical-align: middle; margin: 4px; padding: 3px 10px; cursor: pointer; border: 1px solid transparent; }
    .rich-text-editor.rich-text-focused img[src^="data:image/svg+xml"],
    .rich-text-editor:focus img[src^="data:image/svg+xml"] { background: #EDF9FF; border: 1px solid #E6F2F8; }
    .rich-text-editor img[src*="data:image/png"] { margin: 4px; }
    .rich-text-editor:focus img[src*="data:image/png"],
    .rich-text-editor.rich-text-focused img[src*="data:image/png"] { box-shadow: 0 0 3px 1px rgba(0, 0, 0, .2); }
    .result { display: none; }
  </style>
<style type="text/css">#MathJax_Zoom {position: absolute; background-color: #F0F0F0; overflow: auto; display: block; z-index: 301; padding: .5em; border: 1px solid black; margin: 0; font-weight: normal; font-style: normal; text-align: left; text-indent: 0; text-transform: none; line-height: normal; letter-spacing: normal; word-spacing: normal; word-wrap: normal; white-space: nowrap; float: none; -webkit-box-sizing: content-box; -moz-box-sizing: content-box; box-sizing: content-box; box-shadow: 5px 5px 15px #AAAAAA; -webkit-box-shadow: 5px 5px 15px #AAAAAA; -moz-box-shadow: 5px 5px 15px #AAAAAA; -khtml-box-shadow: 5px 5px 15px #AAAAAA; filter: progid:DXImageTransform.Microsoft.dropshadow(OffX=2, OffY=2, Color='gray', Positive='true')}
#MathJax_ZoomOverlay {position: absolute; left: 0; top: 0; z-index: 300; display: inline-block; width: 100%; height: 100%; border: 0; padding: 0; margin: 0; background-color: white; opacity: 0; filter: alpha(opacity=0)}
#MathJax_ZoomFrame {position: relative; display: inline-block; height: 0; width: 0}
#MathJax_ZoomEventTrap {position: absolute; left: 0; top: 0; z-index: 302; display: inline-block; border: 0; padding: 0; margin: 0; background-color: white; opacity: 0; filter: alpha(opacity=0)}
</style><style type="text/css">#MathJax_About {position: fixed; left: 50%; width: auto; text-align: center; border: 3px outset; padding: 1em 2em; background-color: #DDDDDD; color: black; cursor: default; font-family: message-box; font-size: 120%; font-style: normal; text-indent: 0; text-transform: none; line-height: normal; letter-spacing: normal; word-spacing: normal; word-wrap: normal; white-space: nowrap; float: none; z-index: 201; border-radius: 15px; -webkit-border-radius: 15px; -moz-border-radius: 15px; -khtml-border-radius: 15px; box-shadow: 0px 10px 20px #808080; -webkit-box-shadow: 0px 10px 20px #808080; -moz-box-shadow: 0px 10px 20px #808080; -khtml-box-shadow: 0px 10px 20px #808080; filter: progid:DXImageTransform.Microsoft.dropshadow(OffX=2, OffY=2, Color='gray', Positive='true')}
#MathJax_About.MathJax_MousePost {outline: none}
.MathJax_Menu {position: absolute; background-color: white; color: black; width: auto; padding: 5px 0px; border: 1px solid #CCCCCC; margin: 0; cursor: default; font: menu; text-align: left; text-indent: 0; text-transform: none; line-height: normal; letter-spacing: normal; word-spacing: normal; word-wrap: normal; white-space: nowrap; float: none; z-index: 201; border-radius: 5px; -webkit-border-radius: 5px; -moz-border-radius: 5px; -khtml-border-radius: 5px; box-shadow: 0px 10px 20px #808080; -webkit-box-shadow: 0px 10px 20px #808080; -moz-box-shadow: 0px 10px 20px #808080; -khtml-box-shadow: 0px 10px 20px #808080; filter: progid:DXImageTransform.Microsoft.dropshadow(OffX=2, OffY=2, Color='gray', Positive='true')}
.MathJax_MenuItem {padding: 1px 2em; background: transparent}
.MathJax_MenuArrow {position: absolute; right: .5em; padding-top: .25em; color: #666666; font-size: .75em}
.MathJax_MenuActive .MathJax_MenuArrow {color: white}
.MathJax_MenuArrow.RTL {left: .5em; right: auto}
.MathJax_MenuCheck {position: absolute; left: .7em}
.MathJax_MenuCheck.RTL {right: .7em; left: auto}
.MathJax_MenuRadioCheck {position: absolute; left: .7em}
.MathJax_MenuRadioCheck.RTL {right: .7em; left: auto}
.MathJax_MenuLabel {padding: 1px 2em 3px 1.33em; font-style: italic}
.MathJax_MenuRule {border-top: 1px solid #DDDDDD; margin: 4px 3px}
.MathJax_MenuDisabled {color: GrayText}
.MathJax_MenuActive {background-color: #606872; color: white}
.MathJax_MenuDisabled:focus, .MathJax_MenuLabel:focus {background-color: #E8E8E8}
.MathJax_ContextMenu:focus {outline: none}
.MathJax_ContextMenu .MathJax_MenuItem:focus {outline: none}
#MathJax_AboutClose {top: .2em; right: .2em}
.MathJax_Menu .MathJax_MenuClose {top: -10px; left: -10px}
.MathJax_MenuClose {position: absolute; cursor: pointer; display: inline-block; border: 2px solid #AAA; border-radius: 18px; -webkit-border-radius: 18px; -moz-border-radius: 18px; -khtml-border-radius: 18px; font-family: 'Courier New',Courier; font-size: 24px; color: #F0F0F0}
.MathJax_MenuClose span {display: block; background-color: #AAA; border: 1.5px solid; border-radius: 18px; -webkit-border-radius: 18px; -moz-border-radius: 18px; -khtml-border-radius: 18px; line-height: 0; padding: 8px 0 6px}
.MathJax_MenuClose:hover {color: white!important; border: 2px solid #CCC!important}
.MathJax_MenuClose:hover span {background-color: #CCC!important}
.MathJax_MenuClose:hover:focus {outline: none}
</style><style type="text/css">.MathJax_Preview .MJXf-math {color: inherit!important}
</style><style type="text/css">.MJX_Assistive_MathML {position: absolute!important; top: 0; left: 0; clip: rect(1px, 1px, 1px, 1px); padding: 1px 0 0 0!important; border: 0!important; height: 1px!important; width: 1px!important; overflow: hidden!important; display: block!important; -webkit-touch-callout: none; -webkit-user-select: none; -khtml-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none}
.MJX_Assistive_MathML.MJX_Assistive_MathML_Block {width: 100%!important}
</style><style type="text/css">.MathJax_Hover_Frame {border-radius: .25em; -webkit-border-radius: .25em; -moz-border-radius: .25em; -khtml-border-radius: .25em; box-shadow: 0px 0px 15px #83A; -webkit-box-shadow: 0px 0px 15px #83A; -moz-box-shadow: 0px 0px 15px #83A; -khtml-box-shadow: 0px 0px 15px #83A; border: 1px solid #A6D ! important; display: inline-block; position: absolute}
.MathJax_Menu_Button .MathJax_Hover_Arrow {position: absolute; cursor: pointer; display: inline-block; border: 2px solid #AAA; border-radius: 4px; -webkit-border-radius: 4px; -moz-border-radius: 4px; -khtml-border-radius: 4px; font-family: 'Courier New',Courier; font-size: 9px; color: #F0F0F0}
.MathJax_Menu_Button .MathJax_Hover_Arrow span {display: block; background-color: #AAA; border: 1px solid; border-radius: 3px; line-height: 0; padding: 4px}
.MathJax_Hover_Arrow:hover {color: white!important; border: 2px solid #CCC!important}
.MathJax_Hover_Arrow:hover span {background-color: #CCC!important}
</style><style type="text/css">.MathJax_SVG_Display {text-align: center; margin: 1em 0em; position: relative; display: block!important; text-indent: 0; max-width: none; max-height: none; min-width: 0; min-height: 0; width: 100%}
.MathJax_SVG .MJX-monospace {font-family: monospace}
.MathJax_SVG .MJX-sans-serif {font-family: sans-serif}
#MathJax_SVG_Tooltip {background-color: InfoBackground; color: InfoText; border: 1px solid black; box-shadow: 2px 2px 5px #AAAAAA; -webkit-box-shadow: 2px 2px 5px #AAAAAA; -moz-box-shadow: 2px 2px 5px #AAAAAA; -khtml-box-shadow: 2px 2px 5px #AAAAAA; padding: 3px 4px; z-index: 401; position: absolute; left: 0; top: 0; width: auto; height: auto; display: none}
.MathJax_SVG {display: inline; font-style: normal; font-weight: normal; line-height: normal; font-size: 100%; font-size-adjust: none; text-indent: 0; text-align: left; text-transform: none; letter-spacing: normal; word-spacing: normal; word-wrap: normal; white-space: nowrap; float: none; direction: ltr; max-width: none; max-height: none; min-width: 0; min-height: 0; border: 0; padding: 0; margin: 0}
.MathJax_SVG * {transition: none; -webkit-transition: none; -moz-transition: none; -ms-transition: none; -o-transition: none}
.MathJax_SVG > div {display: inline-block}
.mjx-svg-href {fill: blue; stroke: blue}
.MathJax_SVG_Processing {visibility: hidden; position: absolute; top: 0; left: 0; width: 0; height: 0; overflow: hidden; display: block!important}
.MathJax_SVG_Processed {display: none!important}
.MathJax_SVG_ExBox {display: block!important; overflow: hidden; width: 1px; height: 60ex; min-height: 0; max-height: none; padding: 0; border: 0; margin: 0}
.MathJax_SVG_LineBox {display: table!important}
.MathJax_SVG_LineBox span {display: table-cell!important; width: 10000em!important; min-width: 0; max-width: none; padding: 0; border: 0; margin: 0}
.MathJax_SVG .noError {vertical-align: ; font-size: 90%; text-align: left; color: black; padding: 1px 3px; border: 1px solid}
</style><style type="text/css">.MJXp-script {font-size: .8em}
.MJXp-right {-webkit-transform-origin: right; -moz-transform-origin: right; -ms-transform-origin: right; -o-transform-origin: right; transform-origin: right}
.MJXp-bold {font-weight: bold}
.MJXp-italic {font-style: italic}
.MJXp-scr {font-family: MathJax_Script,'Times New Roman',Times,STIXGeneral,serif}
.MJXp-frak {font-family: MathJax_Fraktur,'Times New Roman',Times,STIXGeneral,serif}
.MJXp-sf {font-family: MathJax_SansSerif,'Times New Roman',Times,STIXGeneral,serif}
.MJXp-cal {font-family: MathJax_Caligraphic,'Times New Roman',Times,STIXGeneral,serif}
.MJXp-mono {font-family: MathJax_Typewriter,'Times New Roman',Times,STIXGeneral,serif}
.MJXp-largeop {font-size: 150%}
.MJXp-largeop.MJXp-int {vertical-align: -.2em}
.MJXp-math {display: inline-block; line-height: 1.2; text-indent: 0; font-family: 'Times New Roman',Times,STIXGeneral,serif; white-space: nowrap; border-collapse: collapse}
.MJXp-display {display: block; text-align: center; margin: 1em 0}
.MJXp-math span {display: inline-block}
.MJXp-box {display: block!important; text-align: center}
.MJXp-box:after {content: " "}
.MJXp-rule {display: block!important; margin-top: .1em}
.MJXp-char {display: block!important}
.MJXp-mo {margin: 0 .15em}
.MJXp-mfrac {margin: 0 .125em; vertical-align: .25em}
.MJXp-denom {display: inline-table!important; width: 100%}
.MJXp-denom > * {display: table-row!important}
.MJXp-surd {vertical-align: top}
.MJXp-surd > * {display: block!important}
.MJXp-script-box > *  {display: table!important; height: 50%}
.MJXp-script-box > * > * {display: table-cell!important; vertical-align: top}
.MJXp-script-box > *:last-child > * {vertical-align: bottom}
.MJXp-script-box > * > * > * {display: block!important}
.MJXp-mphantom {visibility: hidden}
.MJXp-munderover {display: inline-table!important}
.MJXp-over {display: inline-block!important; text-align: center}
.MJXp-over > * {display: block!important}
.MJXp-munderover > * {display: table-row!important}
.MJXp-mtable {vertical-align: .25em; margin: 0 .125em}
.MJXp-mtable > * {display: inline-table!important; vertical-align: middle}
.MJXp-mtr {display: table-row!important}
.MJXp-mtd {display: table-cell!important; text-align: center; padding: .5em 0 0 .5em}
.MJXp-mtr > .MJXp-mtd:first-child {padding-left: 0}
.MJXp-mtr:first-child > .MJXp-mtd {padding-top: 0}
.MJXp-mlabeledtr {display: table-row!important}
.MJXp-mlabeledtr > .MJXp-mtd:first-child {padding-left: 0}
.MJXp-mlabeledtr:first-child > .MJXp-mtd {padding-top: 0}
.MJXp-merror {background-color: #FFFF88; color: #CC0000; border: 1px solid #CC0000; padding: 1px 3px; font-style: normal; font-size: 90%}
.MJXp-scale0 {-webkit-transform: scaleX(.0); -moz-transform: scaleX(.0); -ms-transform: scaleX(.0); -o-transform: scaleX(.0); transform: scaleX(.0)}
.MJXp-scale1 {-webkit-transform: scaleX(.1); -moz-transform: scaleX(.1); -ms-transform: scaleX(.1); -o-transform: scaleX(.1); transform: scaleX(.1)}
.MJXp-scale2 {-webkit-transform: scaleX(.2); -moz-transform: scaleX(.2); -ms-transform: scaleX(.2); -o-transform: scaleX(.2); transform: scaleX(.2)}
.MJXp-scale3 {-webkit-transform: scaleX(.3); -moz-transform: scaleX(.3); -ms-transform: scaleX(.3); -o-transform: scaleX(.3); transform: scaleX(.3)}
.MJXp-scale4 {-webkit-transform: scaleX(.4); -moz-transform: scaleX(.4); -ms-transform: scaleX(.4); -o-transform: scaleX(.4); transform: scaleX(.4)}
.MJXp-scale5 {-webkit-transform: scaleX(.5); -moz-transform: scaleX(.5); -ms-transform: scaleX(.5); -o-transform: scaleX(.5); transform: scaleX(.5)}
.MJXp-scale6 {-webkit-transform: scaleX(.6); -moz-transform: scaleX(.6); -ms-transform: scaleX(.6); -o-transform: scaleX(.6); transform: scaleX(.6)}
.MJXp-scale7 {-webkit-transform: scaleX(.7); -moz-transform: scaleX(.7); -ms-transform: scaleX(.7); -o-transform: scaleX(.7); transform: scaleX(.7)}
.MJXp-scale8 {-webkit-transform: scaleX(.8); -moz-transform: scaleX(.8); -ms-transform: scaleX(.8); -o-transform: scaleX(.8); transform: scaleX(.8)}
.MJXp-scale9 {-webkit-transform: scaleX(.9); -moz-transform: scaleX(.9); -ms-transform: scaleX(.9); -o-transform: scaleX(.9); transform: scaleX(.9)}
.MathJax_PHTML .noError {vertical-align: ; font-size: 90%; text-align: left; color: black; padding: 1px 3px; border: 1px solid}
</style>
</head>
<body>
<div style="visibility: hidden; overflow: hidden; position: absolute; top: 0px; height: 1px; width: auto; padding: 0px; border: 0px; margin: 0px; text-align: left; text-indent: 0px; text-transform: none; line-height: normal; letter-spacing: normal; word-spacing: normal;"><div id="MathJax_SVG_Hidden"><br></br></div><svg><defs id="MathJax_SVG_glyphs"></defs></svg></div><div id="MathJax_Message" style="display: none;"></div>
<article>
  <section>
    <h1>Vihko</h1>
<p>Kirjoita sivun nimi alla olevaan kenttään:</p>
  <form id="frm" action="../">
    <input list="files" type="text" id="txt" />
    <datalist id="files">
""" + options + r"""
    </datalist>
    <input type="submit" id="sub" value="Avaa sivu" />
  </form>
<br>
    <div class="answer rich-text-editor" id="answer1" contenteditable=true= spellcheck="false" data-js="answer">
""" + answer + r"""</div>
  <p>Sivu tallentuu automaattisesti 5 sekunnin välein.</p>
  </section>
</article>
<div class="result"><span class="MathJax_Preview" style="color: inherit; display: none;"></span><span class="MathJax_SVG" id="MathJax-Element-1-Frame" tabindex="0" data-mathml="&lt;math xmlns=&quot;http://www.w3.org/1998/Math/MathML&quot;&gt;&lt;mrow class=&quot;MJX-TeXAtom-ORD&quot;&gt;&lt;/mrow&gt;&lt;/math&gt;" role="presentation" style="font-size: 100%; display: inline-block; position: relative;"><svg xmlns:xlink="http://www.w3.org/1999/xlink" width="0" height="0.246ex" viewBox="0 -53 0 105.9" role="img" focusable="false" aria-hidden="true" style="vertical-align: -0.123ex;"><defs></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)"></g></svg><span class="MJX_Assistive_MathML" role="presentation"><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow class="MJX-TeXAtom-ORD"></mrow></math></span></span><script type="math/tex" id="MathJax-Element-1">{}</script></div>
<script>
  MathJax.Hub.Config({
    jax: ["input/TeX", "output/SVG"],
    extensions: ["toMathML.js", "tex2jax.js", "MathMenu.js", "MathZoom.js", "fast-preview.js", "AssistiveMML.js", "a11y/accessibility-menu.js"],
    TeX: {
      extensions: ["AMSmath.js", "AMSsymbols.js", "noErrors.js", "noUndefined.js", "mhchem.js"]
    },
    SVG: {useFontCache: true, useGlobalCache: false, EqnChunk: 1000000, EqnDelay: 0, font: 'STIX-Web'}
  })

  const answer = document.querySelector('#answer1')
  makeRichText(answer, {
    screenshot: {
      saver: ({data}) =>
        new Promise(resolve => {
          const reader = new FileReader()
          reader.onload = evt => resolve(evt.target.result.replace(/^(data:image)(\/[^;]+)(;.*)/,'$1$3'))
          reader.readAsDataURL(data)
        })
    },
    baseUrl: '',
    updateMathImg: ($img, latex) => {
      updateMath(latex, svg => {
        $img.prop({
          src: svg,
          alt: latex
        })
        $img.closest('[data-js="answer"]').trigger('input')
      })
    }
  })

  let math = null
  MathJax.Hub.queue.Push(() => {
    math = MathJax.Hub.getAllJax('MathOutput')[0]
  })

  function saveAnswer() {
    $.post("/""" + path + r"""/save/""" + fid + r"""", {answer: $(".answer").html()});
    setTimeout(saveAnswer, 5000);
  }

  $(document).ready(function() {
    setTimeout(saveAnswer, 5000);
  });
  
  const encodeMultibyteUnicodeCharactersWithEntities = (str) =>
    str.replace(/[^\x00-\xFF]/g, c => `&#${c.charCodeAt(0).toString(10)};`)

  const updateMath = function (latex, cb) {
    MathJax.Hub.queue.Push(['Text', math, '\\displaystyle{' + latex + '}'])
    MathJax.Hub.Queue(() => {
      if ($('.result svg').length) {
        const $svg = $('.result svg').attr('xmlns', "http://www.w3.org/2000/svg")
        $svg.find('use').each(function () {
          const $use = $(this)
          if ($use[0].outerHTML.indexOf('xmlns:xlink') === -1) {
            $use.attr('xmlns:xlink', 'http://www.w3.org/1999/xlink') //add these for safari
          }
        })
        let svgHtml = $svg.prop('outerHTML')
        //firefox fix
        svgHtml = svgHtml.replace(' xlink=', ' xmlns:xlink=')
        // Safari xlink ns issue fix
        svgHtml = svgHtml.replace(/ ns\d+:href/gi, ' xlink:href')
        cb('data:image/svg+xml;base64,' + window.btoa(encodeMultibyteUnicodeCharactersWithEntities(svgHtml)))
      } else {
        cb('data:image/svg+xml;base64,' + window.btoa(`<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="17px" height="15px" viewBox="0 0 17 15" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <title>Group 2</title>
    <defs></defs>
    <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
        <g transform="translate(-241.000000, -219.000000)">
            <g transform="translate(209.000000, 207.000000)">
                <rect x="-1.58632797e-14" y="0" width="80" height="40"></rect>
                <g transform="translate(32.000000, 12.000000)">
                    <polygon id="Combined-Shape" fill="#9B0000" fill-rule="nonzero" points="0 15 8.04006 0 16.08012 15"></polygon>
                    <polygon id="Combined-Shape-path" fill="#FFFFFF" points="7 11 9 11 9 13 7 13"></polygon>
                    <polygon id="Combined-Shape-path" fill="#FFFFFF" points="7 5 9 5 9 10 7 10"></polygon>
                </g>
            </g>
        </g>
    </g>
</svg>`))
      }
    })
  }

  let studentDisplay = null
  MathJax.Hub.Queue(function () {
    studentDisplay = MathJax.Hub.getAllJax(document.querySelector('.result'))[0];
  })
  const trackError = (e = {}) => {
    const category = 'JavaScript error'
    const action = e.message
    const label = e.filename + ':' + e.lineno
  }

  if (window.addEventListener) {
    window.addEventListener('error', trackError, false)
  } else if (window.attachEvent) {
    window.attachEvent('onerror', trackError)
  } else {
    window.onerror = trackError
  }

  const reader = new FileReader()
  reader.onload = x => $('.answer').html(x.target.result)

</script>
</body>
</html>
"""

webbrowser.open_new('http://localhost:5000/{}/'.format(path))
app.run()
