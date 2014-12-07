
/* load the current default model and add it to the app */
function reload_sound_class_model() {
  current_model = _get_option('sound_class_models');
  $.ajax({
    url: 'index.settings?type=load_sound_classes&model='+current_model,
    async: false,
    success: function(data) {
      document.getElementById('sound_classes').value = data;
    }
  });
}

/* function stores a given sound class model */
function store_sound_class_model() {
  
  /* get error node */
  error = document.getElementById('error');

  /* get error message and clean it */
  error.innerHTML = '';

  /* get sound class model name */
  scmn = document.getElementById('sound_class_model_name').value;

  /* check value */
  if (scmn == '') {
    error.innerHTML = "Your model name is not defined.";
    return;
  }
  else if (scmn.replace(/[a-zA-Z0-9_]*/,'') != '') {
    error.innerHTML = "Your model name should only contain alphanumeric characters and understrokes";
    return;
  }
  else if (available_sound_class_models.indexOf(scmn) != -1) {
    error.innerHTML = "Your model is already defined.";
    return;
  }

  var model = {};
  model['name'] = scmn;
  model['data'] = document.getElementById('sound_classes').value;
  model['type'] = 'store_sound_classes';

  var url = serialize_object(model);

  /* now send store signal via ajax to python */
  $.ajax({
    async: true,
    url: 'index.settings?'+url,
    success: function(data) {
      error.innerHTML = "Successfully stored your sound class model.";
      SETTINGS['sound_class_models'].push(scmn);
      SETTINGS['sound_class_models'].sort();
      available_sound_class_models = _load_values_to_selector('sound_class_models');
    }
  });
  
}

/* get available sound class models and load them to the app */
available_sound_class_models = _load_values_to_selector('sound_class_models');

reload_sound_class_model();
