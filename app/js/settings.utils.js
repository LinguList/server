/* start the application by uploading the current segmentation options */
var available_settings = [];
var selector = document.getElementById('segmentations');
var txt = '';
for (var i=0; i<SETTINGS['segmentations'].length; i++) {
  var segm = SETTINGS['segmentations'][i];
  txt += '<option value="'+segm+'"';
  console.log(SETTINGS['segmentation']);
  if (SETTINGS['segmentation'] == segm) {
    txt += ' selected';
  }
  txt += '>'+segm+'</option>';
  available_settings.push(segm);
}
selector.innerHTML = txt;

