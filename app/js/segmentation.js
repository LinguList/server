/* Segmentation basics for LingPy-Server
 *
 * author   : Johann-Mattis List
 * email    : mattis.list@lingulist.de
 * created  : 2014-12-05 12:15
 * modified : 2014-12-05 12:15
 *
 */

/* define a currently local default settings value */
_SETTINGS = {};
_SETTINGS['segmentations_current'] = SETTINGS['segmentations_current'];

/* modify the default settings with ajax call */
function reloadSettings(schema) {
  $.ajax({
    async: false,
    dataType: "json",
    url: "index.settings?type=load_segmentation&schema="+schema,
    success: function(data) {
      _SETTINGS = data;
      _SETTINGS['segmentations_current'] = schema;
    }
  });
}

/* load default settings for a given item */
function presentDefaults(what) {

  var node = document.getElementById(what);
  var data = _SETTINGS[what];

  if (what == 'diacritics' || what == 'combiners') {
    data = '◌' + data.split('').join(' ◌');
  }
  else {
    data = data.split('').join(' ');
  }
  node.value = data;
}

/* function gets the value of a given setting and converts it according
 * to specific rules so that it is easier for the user to view the data */
function retrieveSettings(what) {
  var data = document.getElementById(what).value;
  if (what == 'diacritics' || what == 'combiners') {
    data = data.replace(/[◌\s]/g,'');
  }
  else {
    data = data.replace(/\s/g,'');
  }
  return data;
}

/* function iterates over input fields, reads in all modifications and stores
 * the given segmentation under the name specified by the user */
function storeSettings() {
  
  document.getElementById('error').innerHTML = '';

  var settings = {};
  settings['vowels'] = retrieveSettings('vowels');
  settings['diacritics'] = retrieveSettings('diacritics');
  settings['tones'] = retrieveSettings('tones');
  settings['combiners'] = retrieveSettings('combiners');
  settings['breaks'] = retrieveSettings('breaks');
  
  var name = document.getElementById('settings_name').value;
  
  var error_node = document.getElementById('error');

  if (name.replace(/[a-zA-Z_0-9]*/,'') != '') { 
    error_node.innerHTML = "Your setting name should only contain letters, numbers, and the understroke.";
    return;
  }
  else if (name == '') {
    error_node.innerHTML = "Your setting name is not defined.";
    return;
  }
  else if (available_settings.indexOf(name) != -1) {
    error_node.innerHTML = "Your setting name is already taken.";
    return;
  }
  else {
    settings['name'] = name;
  }

  settings['type'] = 'store_segmentation';
  
  var url = serialize_object(settings);
  
  $.ajax({
    async: false,
    url: 'index.settings?' + url,
    success: function(data) {
      document.getElementById('error').innerHTML = "Successfully stored your data.";
      }
  });
  location.reload();
}

/* now use the function to load the defaults */
function init_page() {

  reloadSettings(_SETTINGS['segmentations_current']);

  presentDefaults('vowels');
  presentDefaults('diacritics');
  presentDefaults('tones');
  presentDefaults('combiners');
  presentDefaults('breaks');
}


/* get segmentations, that is, all currently defined and stored segmentations */
$.ajax({
  async: false,
  url: 'index.settings?type=show_segmentations',
  success: function(data) {
    SETTINGS['segmentations'] = data.split('\n');
    SETTINGS['segmentations'].sort();
  }
});

/* start the application by uploading the current segmentation options */
var available_settings = [];
var selector = document.getElementById('segmentations');
var txt = '';
for (var i=0; i<SETTINGS['segmentations'].length; i++) {
  var segm = SETTINGS['segmentations'][i];
  txt += '<option value="'+segm+'"';
  console.log(SETTINGS['segmentations_current']);
  if (SETTINGS['segmentations_current'] == segm) {
    txt += ' selected';
  }
  txt += '>'+segm+'</option>';
  available_settings.push(segm);
}
selector.innerHTML = txt;

/* modifies current segmentation schema in order to make it easier for the 
 * user to set up a new schema */
function modify_segmentation() {
  var segmentations = document.getElementById('segmentations');
  for (var i=0,option; option=segmentations.options[i]; i++) {
    var current_segmentation = option.value;
    /* reload the settings */
  
    if (option.selected) {
      reloadSettings(option.value);
      break;
    }
  }
  init_page();
}

init_page();
