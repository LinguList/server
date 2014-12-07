@head: default
@header: default
@footer: default
@body: default
@title: Settings
@js: basics,jquery,settings,bootstrap,prison/lib/sampa,settings,settings.utils
@css: main,bootstrap

<h3 class="heading">Settings (<span onclick="toggleInfo()" class="toggle" id="info_toggle">SHOW HELP</span>)</h3>
<div class="help_text" style="display:none" id="info_text">
<p>
Basic settings for LingPy sessions. Use this interface to define which kinds of sequences you intend to analyze (plain IPA, ASJP, user-defined), or how you want to analyze your alignments.
</p>
</div>

<br>
<p><b>Select the basic setting for segmentation:</b></p>
<div class="form-inline">
<select class="form-inline form-control" id="segmentations"></select>
<button onclick="redefine_segmentation()" class="btn">SUBMIT</button>
</div>

<br>
<p><b>Select a general schema (IPA or ASJP):</b></p>
<div class="form-inline">
<select class="form-control" id="schema">
<option value="asjp">ASJP</option>
<option value="ipa" selected>IPA</option>
</select>
<button onclick="redefine_schema()" class="btn">SUBMIT</button>
</div>

<br>
<p><b>Select the default sound class model: </b></p>
<div class="form-inline">
<select class="form-control" id="sound_class_models"></select>
<button onclick="redefine_sound_class_model()" class="btn">SUBMIT</button>
</div>

<br>
<p><b>Select your basic settings for alignment analyses (pairwise and multiple):</b></p>
<table id="settings_table" style="display:table" class="table table-condensed table-striped table-bordered">
<thead>
<tbody>
<tr>
<th>Keyword</th>
<th>Values </th>
</tr>
<tr>
<td class="keyword">Scoring Settings (only pairwise)</td>
<td>
<div class="keywords form-group form-inline" id="pw-distance">
<label>distance</label><input type="radio" name="pw-distance" value="True" checked />
<label>similarity</label><input type="radio" name="pw-distance" value="False" />
<label>Hamming</label><input type="radio" name="pw-distance" value="hamming" />
</div>
</td>
</tr>
<tr>
<td class="keyword">Mode (only pairwise)</td>
<td>
<div class="keywords form-group form-inline" id="pw-mode">
<label>global</label><input type="radio" name="pw-mode" value="global" checked />
<label>dialign</label><input type="radio" name="pw-mode" value="dialign" />
<label>semi-global</label><input type="radio" name="pw-mode" value="overlap" />
<label>local</label><input type="radio" name="pw-mode" value="local" />
</div>
</td>
</tr>
<tr>
<td class="keyword">Method (only multiple)</td>
<td>
<div class="keywords form-group form-inline" id="ml-method">
<label>progressive</label><input type="radio" name="ml-method" value="progressive" checked />
<label>library</label><input type="radio" name="ml-method" value="library" />
</div>
</td>
</tr>
<tr>
<td class="keyword">Segmentation</td>
<td>
<div class="keywords form-group form-inline" id="ml-merge_vowels">
<label>merge vowels</label><input type="radio" name="ml-merge_vowels" value="True" checked />
<label>separate vowels</label><input type="radio" name="ml-merge_vowels" value="False" />
</div>
</td>
</tr>
<tr>
<td class="keyword">Sound Class Model</td>
<td>
<div class="keywords form-group form-inline" id="ml-model">
<label>DOLGO</label><input type="radio" name="ml-model" value="dolgo" />
<label>SCA</label><input type="radio" name="ml-model" value="sca" checked />
<label>ASJP</label><input type="radio" name="ml-model" value="asjp" />
</div>
</td>
</tr>
<tr>
<td class="keyword">Gap Opening Penalty (GOP)</td>
<td>
<div class="keywords form-group form-inline">
<input class="form-control" id="ml-gop" type="number" value="-2" min="-10" max="0"/>
</div>
</td>
</tr>
<tr>
<td class="keyword">Gap Extension Scale (GEP-Scale)</td>
<td>
<div class="keywords form-group form-inline">
<label><input class="form-control" id="ml-gep_scale" type="range" min="0" value="0.5" max="1" onchange="outputUpdate(value,'ml-gep_scale-fader')" step="0.05" /></label>
<label for="ml-gep-scale" id="ml-gep_scale-fader">0.5</label>
</div>
</td>
</tr>
<tr>
<td class="keyword">Prosodic Factor</td>
<td>
<div class="keywords form-group form-inline">
<label><input class="form-control" id="ml-factor" type="range" min="0" value="0.3" max="1" onchange="outputUpdate(value,'ml-factor-fader')" step="0.05" /></label>
<label for="ml-factor" id="ml-factor-fader">0.3</label>
</div>
</td>
</tr>
<tr>
<td class="keyword">Gap Weight (only multiple)</td>
<td>
<div class="keywords form-group form-inline">
<input class="form-control" id="ml-gap_weight" type="range" min="0" value="0.5" max="1" onchange="outputUpdate(value,'ml-gap_weight-fader')" step="0.05" />
<label for="ml-gap_weight" id="ml-gap_weight-fader">0.5</label>
</div>
</td>
</tr>
<tr>
<td class="keyword">Guide Tree (only multiple)</td>
<td>
<div class="keywords form-group form-inline" id="ml-tree_calc">
<label>Neighbor-Joining</label><input type="radio" name="ml-tree_calc" value="neighbor" checked />
<label>UGPMA</label><input type="radio" name="ml-tree_calc" value="upgma" />
</div>
</td>
</tr>
<tr>
<td class="keyword">Post-Processing (only multiple)</td>
<td>
<div class="keywords form-group form-inline" id="ml-post_processing">
<label>orphans</label><input type="checkbox" name="ml-post-processing" value="iterate_orphans" />
<label>full iteration</label><input type="checkbox" name="ml-post-processing" value="iterate_all_sequences" />
<label>similar gap sites</label><input type="checkbox" name="ml-post-processing" value="iterate_similar_gap_sites" />
<label>clusters</label><input type="checkbox" name="ml-post-processing" value="iterate_clusters" />
</div>
</td>
</tr>
<tr>
<td class="keyword">Syllable Break Characters</td>
<td>
<div class="keywords form-group form-inline">
<input class="form-control" id="ml-restricted_chars" type="text" value="T_" />
</div>
</td>
</tr>
</tbody>
</table>
<button onclick="redefine_alignment_settings()" class="btn">SUBMIT</button>

<p><b>Select your basic settings for cognate detection analyses:</b></p>
