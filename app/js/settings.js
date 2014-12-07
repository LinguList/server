/* Basic Settings of LingPy provided by Ajax call.
 *
 * author   : Johann-Mattis List
 * email    : mattis.list@lingulist.de
 * created  : 2014-12-05 12:22
 * modified : 2014-12-05 12:22
 *
 */

var SETTINGS = {};
$.ajax({
  async: false,
  dataType: "json",
  url: "index.rc",
  success: function(data) {SETTINGS = data;}
});

/* get segmentations, that is, all currently defined and stored segmentations */
$.ajax({
  async: false,
  url: 'index.settings?type=show_segmentations',
  success: function(data) {
    SETTINGS['segmentations'] = data.split('\n');
    SETTINGS['segmentations'].sort();
  }
});

/* get sound classes, that is all sound class models currently available */
$.ajax({
  async: false,
  url: 'index.settings?type=show_sound_classes',
  success: function(data) {
    SETTINGS['sound_class_models'] = data.split('\n');
    SETTINGS['sound_class_models'].sort();
  }
});

/* function gets selected option from a selector */
function _get_option(selector) {
  var slc = document.getElementById(selector);
  for (var i=0,option; option=slc.options[i]; i++) {
    var current_option = option.value;

    if (option.selected) {
      break;
    }
  }

  return current_option;
}

/* modify the schema */
function redefine_schema() {

  var current_schema = _get_option('schema');
  $.ajax({
    url: 'index.settings?type=modify_schema&schema='+current_schema,
    async: false
  });

  if (schema=='asjp') {
    SETTINGS['segmentations_current'] = 'asjp';
  }
  else {
    SETTINGS['segmentations_current'] = 'sca';
  }

}

/* modify the current selector */
function redefine_segmentation() {

  var current_segmentation = _get_option('segmentations');

  /* modify the settings */
  $.ajax({
    url: 'index.settings?type=modify_segmentation&schema='+current_segmentation,
    async: true
  });
  
  SETTINGS['segmentations_current'] = current_segmentation;
}

/* redefine the currently basic sound class model */
function redefine_sound_class_model() {

  var current_sound_class_model = _get_option('sound_class_models');
  
  /* modify it */
  $.ajax({
    url: 'index.settings?type=modify_sound_class_model&model='+current_sound_class_model,
    async: true
    });

  SETTINGS['sound_class_models_current'] = current_sound_class_model;
}

/* function gives values to an identifier by loading them */
function _load_values_to_selector(idf) {
  var out = [];
  var slc = document.getElementById(idf);
  var txt = '';
  for (var i=0; i<SETTINGS[idf].length; i++) {
    var val = SETTINGS[idf][i];
    txt += '<option value="'+val+'"';
    if (SETTINGS[idf+'_current'] == val) {
      txt += ' selected';
    }
    txt += '>'+val+'</option>';
    out.push(val);
  }
  slc.innerHTML = txt;
  return out;
}

