/* Basic functions for LingPy integration with a Web-GUI
 *
 * author   : Johann-Mattis List
 * email    : mattis.list@lingulist.de
 * created  : 2014-11-28 20:38
 * modified : 2014-11-28 20:38
 *
 */

/* two main functions serve to communicate between python and javascript
 * we use urlencodings and get statements here in order to keep everything as simple
 * as possible, once function converts an object to an url, another function
 * codes back from the url to the object.
 * in this way, we guarantee that both results from python can be displayed
 * in the guy and that data can be passed to python
 */

function serialize_object(obj) {
  var str = [];
  for(var p in obj) {
    console.log(p);
    if (obj.hasOwnProperty(p)) {
      if(typeof obj[p] == 'string' || typeof obj[p] == 'number') {
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
      }
      else if (typeof obj[p] == 'object') {
        for (key in obj[p]) {
          str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p][key]));
        }
      }
      else {
        console.log(p,obj[p]);
      }
    }
  }
  
  return str.join('&');
}

function deserialize_object(url) {
  var ab = url.split('?');
  var query = ab[1].split('#')[0];
  var objects = query.split('&');
  var out = {};
  for (var i=0,q; q = objects[i]; i++) {
    var kv = q.split('=');
    if (kv[0] in out) {
      out[decodeURIComponent(kv[0])].push(decodeURIComponent(kv[1]));
    }
    else {
      out[decodeURIComponent(kv[0])] = [decodeURIComponent(kv[1])];
    }
  }
  return out;
}

/* testing the functions for node js */
//var url = 'http://schokolade.de?arsch=wurst&arsch=scheiben&schweine=backe';
//
//var bla = deserialize_object(url);
//var blu = serialize_object(bla)
//console.log(deserialize_object(url));
//console.log(blu);


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


