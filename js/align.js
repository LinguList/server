var STORE = '';
function malign() {
  
  var msa = {};

  /* get the basic settings for the alignment procedure */
  /* get the method for the object */
  var tmp = document.getElementById('ml-method');
  for (var i=0,child; child=tmp.childNodes[i]; i++) {
    if (child.checked) {
      msa['method'] = child.value;
      break;
    }
  }

  /* get merge vowel parameter for the object */
  var tmp = document.getElementById('ml-merge_vowels');
  for (var i=0,child; child=tmp.childNodes[i]; i++) {
    if (child.checked) {
      msa['merge_vowels'] = child.value;
      break;
    }
  }

  /* get merge vowel parameter for the object */
  var tmp = document.getElementById('ml-post_processing');
  for (var i=0,child; child=tmp.childNodes[i]; i++) {
    if (child.checked) {
      msa[child.value] = 'True';
      break;
    }
  }


  /* get the tree-calc for the object */
  var tmp = document.getElementById('ml-tree_calc');
  for (var i=0,child; child=tmp.childNodes[i]; i++) {
    if (child.checked) {
      msa['tree_calc'] = child.value;
      break;
    }
  }

  /* get the mode for the object */
  /*var tmp = document.getElementById('ml-mode');
  for (var i=0,child; child=tmp.childNodes[i]; i++) {
    if (child.checked) {
      msa['mode'] = child.value;
      break;
    }
  }*/

  /* get the model for the object */
  var tmp = document.getElementById('ml-model');
  for (var i=0,child; child=tmp.childNodes[i]; i++) {
    if (child.checked) {
      msa['model'] = child.value;
      break;
    }
  }

  /* get the sampa-ipa settings for the object */
  var tmp = document.getElementById('ml-input');
  for (var i=0,child; child=tmp.childNodes[i]; i++) {
    if (child.checked) {
      msa['input'] = child.value;
      break;
    }
  }

  /* get the gop for the object */
  var tmp = document.getElementById('ml-gop');
  msa['gop'] = parseInt(tmp.value);

  var tmp = document.getElementById('ml-gep_scale');
  msa['gep_scale'] = parseFloat(tmp.value);

  var tmp = document.getElementById('ml-factor');
  msa['factor'] = parseFloat(tmp.value);

  var tmp = document.getElementById('ml-gap_weight');
  msa['gap_weight'] = parseFloat(tmp.value);

  var tmp = document.getElementById('ml-restricted_chars');
  msa['restricted_chars'] = tmp.value;

  /* get the data from the textarea */
  var alm = document.getElementById('alms');
  /* get the sequences from the data */
  var seqs = alm.value.split(/\n/);
  msa.seqs = [];
  for (var i=0; i < seqs.length; i++) {
    var seq = seqs[i];
    if (seq.replace(/\s*/,'') != '') {
      if (msa['input'] == 'sampa') {
        var this_seq = sampa2ipa(seq);
      }
      else {
        var this_seq = seq
      }
      msa['seqs'].push(this_seq);
    }
  }
  
  /* set the type of the object */
  msa['type'] = 'msa';

  console.log("MSA",msa);

  /* create the url to be passed to ajax */
  var msa_url = 'basic.msa?'+serialize_object(msa)
  $.ajax({
        async: false,
        type: "GET",
        contentType: "application/text; charset=utf-8",
        url: msa_url,
        dataType: "text",
        success: function(data) {
          STORE = data;
        },
        error: function() {
          console.log('erreur');
        }    
  });
  console.log(STORE);
  var alms = STORE.split('\n');
  var txt = '';
  for (var i=0,alm; alm=alms[i]; i++) {
    if (alm.slice(0,1) != '@') {
      txt += '<tr>'+plotWord(alm, 'td') + '</tr>';
    }
    else {
      var pid = alm.split(' ')[1];
    }
  }
  txt = '<table>'+txt+'</table>'+'Percentage Identity: '+pid;
  document.getElementById('alignments').innerHTML = txt;
  document.getElementById('alignments').style.display = 'inline';
}

function outputUpdate(vol,what) {
  document.querySelector('#'+what).innerHTML = vol;
}

function toggleSettings() {
  var settings = document.querySelector('#settings_table');
  if (settings.style.display == 'none') {
    settings.style.display = 'block';
    document.querySelector('#settings_toggle').innerHTML = 'HIDE SETTINGS';
  }
  else {
    settings.style.display = 'none';
    document.querySelector('#settings_toggle').innerHTML = 'SHOW SETTINGS';
  }
}

function toggleInfo() {
  var settings = document.querySelector('#info_text');
  if (settings.style.display == 'none') {
    settings.style.display = 'block';
    document.querySelector('#info_toggle').innerHTML = 'HIDE HELP';
  }
  else {
    settings.style.display = 'none';
    document.querySelector('#info_toggle').innerHTML = 'SHOW HELP';
  }

}


function palign() {
  
  var psa = {};

  /* get merge vowel parameter for the object */
  var tmp = document.getElementById('pw-merge_vowels');
  for (var i=0,child; child=tmp.childNodes[i]; i++) {
    if (child.checked) {
      psa['merge_vowels'] = child.value;
      break;
    }
  }

  /* get the mode for the object */
  var tmp = document.getElementById('pw-mode');
  for (var i=0,child; child=tmp.childNodes[i]; i++) {
    if (child.checked) {
      psa['mode'] = child.value;
      break;
    }
  }

  /* get the model for the object */
  var tmp = document.getElementById('pw-model');
  for (var i=0,child; child=tmp.childNodes[i]; i++) {
    if (child.checked) {
      psa['model'] = child.value;
      break;
    }
  }

  /* get the sampa-ipa settings for the object */
  var tmp = document.getElementById('pw-input');
  for (var i=0,child; child=tmp.childNodes[i]; i++) {
    if (child.checked) {
      psa['input'] = child.value;
      break;
    }
  }

  /* get the sampa-ipa settings for the object */
  var tmp = document.getElementById('pw-distance');
  for (var i=0,child; child=tmp.childNodes[i]; i++) {
    if (child.checked) {
      psa['distance'] = child.value;
      break;
    }
  }

  /* get the sampa-ipa settings for the object */
  var tmp = document.getElementById('pw-method');
  for (var i=0,child; child=tmp.childNodes[i]; i++) {
    if (child.checked) {
      psa['method'] = child.value;
      break;
    }
  }



  /* get the gop for the object */
  var tmp = document.getElementById('pw-gop');
  psa['gop'] = parseInt(tmp.value);

  var tmp = document.getElementById('pw-gep_scale');
  psa['gep_scale'] = parseFloat(tmp.value);

  var tmp = document.getElementById('pw-factor');
  psa['factor'] = parseFloat(tmp.value);

  var tmp = document.getElementById('pw-restricted_chars');
  psa['restricted_chars'] = tmp.value;

  /* get the data from the textarea */
  var alm = document.getElementById('alms');
  /* get the sequences from the data */
  var seqs = alm.value.split(/\n/);
  psa.seqs = [];
  for (var i=0; i < seqs.length; i++) {
    var seq = seqs[i];
    if (seq.replace(/\s*/,'') != '') {
      if (seq.indexOf('//') != -1) {
        if (psa['input'] == 'sampa') {
          var this_seq = sampa2ipa(seq);
        }
        else {
          var this_seq = seq
        }
        psa['seqs'].push(this_seq);
      }
    }
  }
  
  /* set the type of the object */
  psa['type'] = 'psa';

  console.log("PSA",psa);

  /* create the url to be passed to ajax */
  var psa_url = 'basic.psa?'+serialize_object(psa)
  $.ajax({
        async: false,
        type: "GET",
        contentType: "application/text; charset=utf-8",
        url: psa_url,
        dataType: "text",
        success: function(data) {
          STORE = data;
        },
        error: function() {
          console.log('erreur');
        }    
  });
  console.log(STORE);
  var alms = STORE.split('\n');
  var txt = '';
  for (var i=0,alm; alm=alms[i]; i++) {
    var almABC = alm.split('//');
    txt += '<table><tr>'+plotWord(almABC[0],'td')+'</tr>';
    txt += '<tr>'+plotWord(almABC[1],'td')+'</tr>';
    txt += '</table>';
    txt += 'Score: '+almABC[2];
  }
  //  if (alm.slice(0,1) != '@') {
  //    txt += '<tr>'+plotWord(alm, 'td') + '</tr>';
  //  }
  //  else {
  //    var pid = alm.split(' ')[1];
  //  }
  //}
  //txt = '<table>'+txt+'</table>'+'Percentage Identity: '+pid;
  document.getElementById('alignments').innerHTML = txt;
  document.getElementById('alignments').style.display = 'inline';
}

