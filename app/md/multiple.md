@head: default
@header: default
@footer: default
@body: default
@title: Multiple Alignments
@js: basics,jquery,bootstrap,align,prison/lib/highlight,prison/lib/sampa
@css: main,bootstrap,alignments

<h3 class="heading">Multiple Phonetic Alignment (<span onclick="toggleInfo()" class="toggle" id="info_toggle">SHOW HELP</span>,
<span onclick="toggleSettings()" class="toggle" id="settings_toggle">SHOW SETTINGS</span>)</h3>
<div class="help_text" style="display:none" id="info_text">
<p>
Paste or input your phonetic sequences in the text field below and press the "SUBMIT" button to align them.
Use the settings below to modify the basic parameters of the algorithm. As a default, you can input your data both using
IPA or SAMPA. If you input SAMPA values, they will be automatically converted into IPA. If you want to avoid this behaviour,
check "other formats" in the settings below. Your sequences will be automatically segmentized into phonologically meaningful
units by LingPy. If you want to force LingPy to use your predefined segmentation style, just input your sequences with meaningful units separated by a space.
</p>
</div>

<table id="settings_table" style="display:none" class="table table-condensed table-striped table-bordered">
<thead>
<tr>
<th>Keyword</th>
<th>Values </th>
</tr>
</thead>
<tbody>
<tr>
<td class="keyword">Input Format</td>
<td>
<div class="keywords form-group form-inline" id="ml-input">
<label>IPA or SAMPA</label><input type="radio" name="ml-input" value="sampa" checked />
<label>other formats</label><input type="radio" name="ml-input" value="ipa" />
</div>
</td>
</tr>
<tr>
<td class="keyword">Method</td>
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
<td class="keyword">Gap Weight</td>
<td>
<div class="keywords form-group form-inline">
<input class="form-control" id="ml-gap_weight" type="range" min="0" value="0.5" max="1" onchange="outputUpdate(value,'ml-gap_weight-fader')" step="0.05" />
<label for="ml-gap_weight" id="ml-gap_weight-fader">0.5</label>
</div>
</td>
</tr>
<tr>
<td class="keyword">Guide Tree</td>
<td>
<div class="keywords form-group form-inline" id="ml-tree_calc">
<label>Neighbor-Joining</label><input type="radio" name="ml-tree_calc" value="neighbor" checked />
<label>UGPMA</label><input type="radio" name="ml-tree_calc" value="upgma" />
</div>
</td>
</tr>
<tr>
<td class="keyword">Post-Processing</td>
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

<br>
<table>
<tr>
<td style="vertical-align:top">
<p><b>Select sequences from MSA files:</b></p>
<div class="form-group form-inline">
<select class="form-control" id="select_msa_files"></select>
<button class="btn btn-submit" onclick="malign('msa')" value="OK">SUBMIT</button>
</div>
<br>
<p><b>Type sequences directly into the text field:</b></p>
<textarea class="form-control" id="alms" cols="30" rows="10">
w a l d e m a r
w o l d e m o r t
v l a d i m i r
</textarea>
<div style="margin-top:10px;margin-bottom:10px;">
<button class="btn btn-submit" onclick="malign('seqs')" value="OK">SUBMIT</button>
</div>

</td>
<td style="vertical-align:top;">
<div style="float:left;display:none;margin-left:10px;border:2px solid lightgray;border-radius:5px;padding:10px;" id="alignments"></div></td></tr></table>



