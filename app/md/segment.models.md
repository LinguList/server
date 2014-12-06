@head: default
@header: default
@footer: default
@body: default
@title: Segmentation
@js: basics,jquery,settings,bootstrap,prison/lib/sampa,segmentation
@css: main,bootstrap

<h3>Segmentation Settings (<span onclick="toggleInfo()" class="toggle" id="info_toggle">SHOW HELP</span>)</h3>
<div class="help_text" style="display:none" id="info_text">
<p>
Basic segmentation in LingPy is based on the assignment of characters to specific classes. Consonants are negatively defined by not being assigned 
to any class. The remaining characters need to be explicitly defined. Among these are <ul>
<ul>
 <li>vowels</li>
 <li>diacritics</li>
 <li>tones</li>
 <li>combiners, and</li>
 <li>breaks</li>
</ul></p>
<p>
Once these characters are sufficiently defined (such that no vowels not defined as belonging to the class of vowels occur in your data), automatic segmentation of sound sequences into sound segments should work accurately. It will fail in those cases where ambiguous characters are used in the data, such as, for example the use of &quot;h&quot; both as a diacritic indicating aspiration and as a full segment. In these cases, manual adjustment of automatic segmentation by the user is required.</p>
<p>
LingPy Server allows you to create your own segmentation models. In order to do so, just adjust the standard settings of LingPy presented below (or select another model as your basic model to be modified). Then select a name for your segmentation model, and press the &quot;SAVE&quot; button.
</p>
</div>
<br>
<div class="form-inline">
<select class="form-inline form-control" id="segmentations"></select>
<button onclick="modify_segmentation()" class="btn">BROWSE</button>
</div>
<br>

<label style="width:200px">Vowels</label>     <br><textarea class="form-control" rows="3" style="width:70%" type="text" id="vowels"></textarea><br>
<label style="width:200px">Diacritics</label> <br><textarea class="form-control" rows="3" style="width:70%" type="text" id="diacritics"></textarea><br>
<label style="width:200px">Tones</label>      <br><textarea class="form-control" rows="1" style="width:70%" type="text" id="tones"></textarea><br>
<label style="width:200px">Combiners</label>  <br><textarea class="form-control" rows="1" style="width:70%" type="text" id="combiners"></textarea><br>
<label style="width:200px">Breaks</label>     <br><textarea class="form-control" rows="1" style="width:70%" type="text" id="breaks"></textarea><br>

<input id="settings_name" type="text" placeholder="name your settings" style="width:250px" />
<button onclick="storeSettings();" class="btn">SAVE</button>
<div id="error" style="color:red;font-weight:bold;"></div>
