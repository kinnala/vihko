import urllib.parse
import random
import secrets
import time
import zipfile
import logging
import os.path
from pathlib import Path
from io import BytesIO
from datetime import datetime
from flask import Flask, request, session, redirect, url_for, send_file


app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.secret_key = secrets.token_bytes(10)
app.config.update(
    PERMANENT_SESSION_LIFETIME=36000  # 10 hours
)


@app.route('/save', methods=['POST'])
def save_answer():
    if 'fid' not in session:
        raise Exception("Session is broken.")
    fid = session['fid']
    app.logger.info("Saving {}".format(fid))
    with open("vihko_{}.html".format(fid), "w") as handle:
        handle.write(urllib.parse.unquote_plus(request.get_data()[7:].decode('utf-8')))
    return {}


@app.route('/clear')
def clear_session():
    session.clear()
    return r"<p>Istuntoon liittyvät tiedot poistettu.</p>"


@app.route('/')
def test():
    return r"""
<!DOCTYPE html>
<html>
<head>
  <script src="//code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
  <script>
  $(document).ready(function(){
    $(frm.txt).keyup(function(){
      $(frm).get(0).setAttribute('action', '/edit/'+$(frm.txt).val());
    });
  });
  </script>
</head>
<body>
  <h1>Vihko</h1>
  <p>Kirjoita tiedoston nimi alla olevaan ruutuun:</p>
  <form id="frm" action="wrong">
    <input type="text" id="txt" />
    <input type="submit" id="sub" value="Avaa tiedosto" />
  </form>
</body>
</html>
"""


@app.route('/edit/<fid>')
def index(fid):
    #question = questions[qid](int.from_bytes(uid.encode("utf-8"), byteorder="big"))
    if 'fid' not in session:
        session['fid'] = fid
    fname = "vihko_{}.html".format(fid)
    if os.path.exists(fname):
        with open(fname, "r") as handle:
            answer = handle.read()
    else:
        answer = ""
        with open(fname, "w") as handle:
            handle.write("")
    return r"""
<!DOCTYPE html>
<html>
<head>
  <meta charset='utf-8'>
  <title>vihko v0.1.0</title>
  <link rel="stylesheet" type="text/css" href="//unpkg.com/@digabi/mathquill/build/mathquill.css">
  <link rel="stylesheet" type="text/css" href="//unpkg.com/rich-text-editor/dist/rich-text-editor.css"/>
  <script src="//code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
  <script src="//cdnjs.cloudflare.com/ajax/libs/bacon.js/1.0.1/Bacon.min.js"></script>
  <script src="//unpkg.com/rich-text-editor/dist/rich-text-editor-bundle.js"></script>
  <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js">
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
<article>
  <section>
    <h1>Vihko</h1>
    <h2>Tiedosto</h2>
""" + fname + r"""
    <h2>Vastaus</h2>
    <div class="answer" id="answer1">
""" + answer + r"""</div>
  </section>
</article>
<div class="result">\({}\)</div>
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
    baseUrl: 'https://math-demo.abitti.fi',
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
    $.post("/save", {answer: $(".answer").html()});
    setTimeout(saveAnswer, 5000);
  }

  $(document).ready(function() {
    setTimeout(saveAnswer, 5000);
  });

  $(".confirm").on("click", function(event){
      $.post("/save", {answer: $(".answer").html()});
      if(confirm("Onko tehtävä varmasti valmis? Aikaisempiin tehtäviin ei voi palata.")){
         return true;
      } else {
          event.preventDefault();
          return false;
      }
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

app.run()
