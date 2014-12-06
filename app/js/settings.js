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

function redefine_segmentation() {
  var segmentations = document.getElementById('segmentations');
  for (var i=0,option; option=segmentations.options[i]; i++) {
    var current_segmentation = option.value;

    if (option.selected) {
      break;
    }
  }
  console.log('current_segmentation',current_segmentation);

  /* modify the settings */
  $.ajax({
    url: 'index.settings?type=modify_segmentation&schema='+current_segmentation,
    async: false
  });
  SETTINGS['segmentation'] = current_segmentation;
}
