@head: default
@header: default
@footer: default
@body: default
@title: Sound Class Models
@js: basics,jquery,settings,bootstrap,prison/lib/sampa,sound_classes
@css: main,bootstrap

<h3 class="heading">Sound Class Models (<span onclick="toggleInfo()" class="toggle" id="info_toggle">SHOW HELP</span>)</h3>
<div class="help_text" style="display:none" id="info_text">
<p>
Here, you can re-define current sound class models and also define your own models.

</p>
</div>
<div class="form-inline">
<select class="form-control" id="sound_class_models"></select>
<button onclick="reload_sound_class_model()" class="btn">BROWSE</button>
<br>
<br>
<textarea rows="20" cols="80" class="form-control" id="sound_classes">
</textarea>
<br><br>
<input class="form-control" id="sound_class_model_name" type="text" placeholder="insert the name of your new model here" style="width:350px" />
<button onclick="store_sound_class_model();" class="btn">SAVE</button>
</div>
<br>
<div id="error" style="color:red"></div>

