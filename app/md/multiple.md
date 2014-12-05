@head: default
@header: default
@footer: default
@body: default
@title: Multiple Alignments
@js: basics,jquery,bootstrap,align,prison/lib/highlight,prison/lib/sampa
@css: main,bootstrap,alignments

<h3>Multiple Phonetic Alignment (<span onclick="toggleInfo()" class="toggle" id="info_toggle">SHOW HELP</span>,
<span onclick="toggleSettings()" class="toggle" id="settings_toggle">SHOW SETTINGS</span>)</h3>
<p style="display:none" id="info_text">
Paste or input your phonetic sequences in the text field below and press the "SUBMIT" button to align them.
Use the settings below to modify the basic parameters of the algorithm. As a default, you can input your data both using
IPA or SAMPA. If you input SAMPA values, they will be automatically converted into IPA. If you want to avoid this behaviour,
check "other formats" in the settings below. Your sequences will be automatically segmentized into phonologically meaningful
units by LingPy. If you want to force LingPy to use your predefined segmentation style, just input your sequences with meaningful units separated by a space.
</p>

<table id="settings_table" style="display:none" class="options">
<tr>
<th class="keyword">Input Format</th>
<td>
<div class="keywords" id="ml-input">
<label>IPA or SAMPA</label><input type="radio" name="ml-input" value="sampa" checked />
<label>other formats</label><input type="radio" name="ml-input" value="ipa" />
</div>
</td>
</tr>

<tr>
<th class="keyword">Method</th>
<td>
<div class="keywords" id="ml-method">
<label>progressive</label><input type="radio" name="ml-method" value="progressive" checked />
<label>library</label><input type="radio" name="ml-method" value="library" />
</div>
</td>
</tr>

<tr>
<th class="keyword">Segmentation</th>
<td>
<div class="keywords" id="ml-merge_vowels">
<label>merge vowels</label><input type="radio" name="ml-merge_vowels" value="True" checked />
<label>separate vowels</label><input type="radio" name="ml-merge_vowels" value="False" />
</div>
</td>
</tr>


<tr>
<th class="keyword">Sound Class Model</th>
<td>
<div class="keywords" id="ml-model">
<label>DOLGO</label><input type="radio" name="ml-model" value="dolgo" />
<label>SCA</label><input type="radio" name="ml-model" value="sca" checked />
<label>ASJP</label><input type="radio" name="ml-model" value="asjp" />
</div>
</td>
</tr>

<!--<tr>
<th class="keyword">Mode</th>
<td>
<div class="keywords" id="ml-mode">
<label>global</label><input type="radio" name="ml-mode" value="global" checked />
<label>dialign</label><input type="radio" name="ml-mode" value="dialign" />
</div>
</td>
</tr>-->
<tr>
<th class="keyword">Gap Opening Penalty (GOP)</th>
<td>
<div class="keywords">
<input id="ml-gop" type="number" value="-2" />
</div>
</td>
</tr>
<tr>
<th class="keyword">Gap Extension Scale (GEP-Scale)</th>
<td>
<div class="keywords">
<label for="ml-gep-scale" id="ml-gep_scale-fader">0.5</label>
<label><input id="ml-gep_scale" type="range" min="0" value="0.5" max="1" onchange="outputUpdate(value,'ml-gep_scale-fader')" step="0.05" /></label>
</div>
</td>
</tr>
<tr>
<th class="keyword">Prosodic Factor</th>
<td>
<div class="keywords">
<label for="ml-factor" id="ml-factor-fader">0.3</label>
<label><input id="ml-factor" type="range" min="0" value="0.3" max="1" onchange="outputUpdate(value,'ml-factor-fader')" step="0.05" /></label>
</div>
</td>
</tr>
<tr>
<th class="keyword">Gap Weight</th>
<td>
<div class="keywords">
<label for="ml-gap_weight" id="ml-gap_weight-fader">0.5</label>
<label><input id="ml-gap_weight" type="range" min="0" value="0.5" max="1" onchange="outputUpdate(value,'ml-gap_weight-fader')" step="0.05" /></label>
</div>
</td>
</tr>

<tr>
<th class="keyword">Guide Tree</th>
<td>
<div class="keywords" id="ml-tree_calc">
<label>Neighbor-Joining</label><input type="radio" name="ml-tree_calc" value="neighbor" checked />
<label>UGPMA</label><input type="radio" name="ml-tree_calc" value="upgma" />
</div>
</td>
</tr>

<tr>
<th class="keyword">Post-Processing</th>
<td>
<div class="keywords" id="ml-post_processing">
<label>orphans</label><input type="checkbox" name="ml-post-processing" value="iterate_orphans" />
<label>full iteration</label><input type="checkbox" name="ml-post-processing" value="iterate_all_sequences" />
<label>similar gap sites</label><input type="checkbox" name="ml-post-processing" value="iterate_similar_gap_sites" />
<label>clusters</label><input type="checkbox" name="ml-post-processing" value="iterate_clusters" />
</div>
</td>
</tr>


<tr>
<th class="keyword">Syllable Break Characters</th>
<td>
<div class="keywords">
<input id="ml-restricted_chars" type="text" value="T_" />
</div>
</td>
</tr>


</table>
</form>
<br>

<div style="overflow:hidden"><div style="float:left;display:inline;">
<textarea class="form-control" id="alms" cols="30" rows="10">
w a l d e m a r
w o l d e m o r t
v l a d i m i r
</textarea></div>
<div style="float:left;display:none;margin-left:10px;border:2px solid lightgray;border-radius:5px;padding:10px;" id="alignments"></div></div>
<br>
<div>
<button class="btn btn-submit pull-left" onclick="malign()" value="OK">SUBMIT</button>
</div>

