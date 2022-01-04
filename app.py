import urllib.parse
import random
import glob
import logging
import os.path
import webbrowser
from pathlib import Path
from flask import Flask, request, send_from_directory, redirect, url_for
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
    with open("sivut/vihko_{}.html".format(fid), "w", encoding='utf-8') as handle:
        handle.write(urllib.parse.unquote_plus(request.get_data()[7:].decode('utf-8')))
    return {}


@app.route('/{}/'.format(path))
def index():
    return redirect(url_for('edit', fid='testi'))


@app.route('/{}/edit/<fid>'.format(path))
def edit(fid):
    fname = "sivut/vihko_{}.html".format(fid)
    if os.path.exists(fname):
        with open(fname, "r", encoding='utf-8') as handle:
            answer = handle.read()
    else:
        answer = ""
        with open(fname, "w", encoding='utf-8') as handle:
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
  <title>vihko</title>
  <link rel="stylesheet" type="text/css" href="../static/mathquill.css">
  <link rel="stylesheet" type="text/css" href="../static/rich-text-editor.css">
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
  <link rel="stylesheet" type="text/css" href="../static/extra.css">
</head>
<body>
<div style="visibility: hidden; overflow: hidden; position: absolute; top: 0px; height: 1px; width: auto; padding: 0px; border: 0px; margin: 0px; text-align: left; text-indent: 0px; text-transform: none; line-height: normal; letter-spacing: normal; word-spacing: normal;"><div id="MathJax_SVG_Hidden"><br></br></div><svg><defs id="MathJax_SVG_glyphs"></defs></svg></div><div id="MathJax_Message" style="display: none;"></div>
<article>
<section>
<div class="wrapper">
<form id="frm" action="../">
  <input list="files" type="text" id="txt" />
  <datalist id="files">
""" + options + r"""
  </datalist>
  <input type="submit" id="sub" value="Avaa" />
  <span class="savetext">★</span>
</form>
<div class="answer rich-text-editor" id="answer1" contenteditable=true= spellcheck="false" data-js="answer" oninput="$('.savetext').css('color', 'red')">
""" + answer + r"""</div>
</div>
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
    $(".savetext").css('color', 'green');
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
