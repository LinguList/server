/* Segmentation basics for LingPy-Server
 *
 * author   : Johann-Mattis List
 * email    : mattis.list@lingulist.de
 * created  : 2014-12-05 12:15
 * modified : 2014-12-05 12:15
 *
 */


/* load default settings for a given item */
function presentDefaults(what) {

  var node = document.getElementById(what);
  var data = SETTINGS[what];

  if (what == 'diacritics' || what == 'combiners') {
    data = '◌' + data.split('').join(' ◌');
  }
  else {
    data = data.split('').join(' ');
  }
  node.value = data;
}

function retrieveDefaults(what) {
  var data = document.getElementById(what).value;
  if (what == 'diacritics' || what == 'combiners') {
    data = data.replace('◌','').split(' ').join('');
  }
  else {
    data = data.split(' ').join('');
  }
  return data;
}


/* now use the function to load the defaults */
presentDefaults('vowels');
presentDefaults('diacritics');
presentDefaults('tones');
presentDefaults('combiners');
presentDefaults('breaks');




function storeSettings() {
  
  document.getElementById('error').innerHTML = '';

  var settings = {};
  settings['vowels'] = retrieveDefaults('vowels');
  settings['diacritics'] = retrieveDefaults('diacritics');
  settings['tones'] = retrieveDefaults('tones');
  settings['combiners'] = retrieveDefaults('combiners');
  settings['breaks'] = retrieveDefaults('breaks');
  
  var name = document.getElementById('settings_name').value;
  
  if (name.replace(/[a-zA-Z_0-9]/g,'') == '' && name != '') {
    settings['name'] = name;
  }
  else {
    document.getElementById('error').innerHTML = "Your settings name should only contain letters and numbers. It cannot be empty.";
    return;
  }


  settings['type'] = 'segmentation';
  
  var url = serialize_object(settings);

  $.ajax({
    async: false,
    url: 'index.settings?' + url,
    success: function(data) {
      document.getElementById('error').innerHTML = "Successfully stored your data.";
      }
  });

  if (success) {
  }
  
}
