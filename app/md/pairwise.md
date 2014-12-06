@head: default
@header: default
@footer: default
@body: default
@title: Pairwise Alignments
@js: basics,jquery,bootstrap,align,prison/lib/highlight,prison/lib/sampa
@css: main,bootstrap,alignments

<h3 class="heading">Pairwise Phonetic Alignment (<span onclick="toggleInfo()" class="toggle" id="info_toggle">SHOW HELP</span>,<span onclick="toggleSettings()" class="toggle" id="settings_toggle">SHOW SETTINGS</span>)</h3>
<div style="display:none" id="info_text">
<p>Paste or input your phonetic sequence pairs, separated by two slashes ("//"),
each pair in one line, in the text field below and press the "SUBMIT" button to
align them.  Use the settings below to modify the basic parameters of the
algorithm. As a default, you can input your data both using IPA or SAMPA. If
you input SAMPA values, they will be automatically converted into IPA. If you
want to avoid this behaviour, check "other formats" in the settings below. Your
sequences will be automatically segmentized into phonologically meaningful
units by LingPy. If you want to force LingPy to use your predefined
segmentation style, just input your sequences with meaningful units separated
by a space.
 
For the calculation of sequence similarities, LingPy Server currently offers three scores:

<ul>
<li>distance</li>
<li>similarity, and</li>
<li>Hamming</li></ul>

The pairwise alignment module of LingPy Server does not offer a direct way to
calculate the well-known and very popular edit distance between two strings. If you
want to approximate the edit distance with help of this module nevertheless, make sure to set the gap opening penalty to -1, set the gap extension scale to 1.0, choose "Needleman Wunsch" as your alignment method, and set the scoring settings to "Hamming". In most cases, this is equivalent with the normalized edit distance between two strings.
</p></div>

<table id="settings_table" class="table table-condensed table-striped table-bordered" style="display:none" class="options">
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
<div class="keywords form-group form-inline" id="pw-input">
<label>IPA or SAMPA</label><input type="radio" name="pw-input" value="sampa" checked />
<label>other formats</label><input type="radio" name="pw-input" value="ipa" />
</div>
</td>
</tr>

<tr>
<td class="keyword">Method</td>
<td>
<div class="keywords form-group form-inline" id="pw-method">
<label>SCA</label><input type="radio" name="pw-method" value="sca" checked />
<label>Needleman-Wunsch</label><input type="radio" name="pw-method" value="nw" />
</div>
</td>
</tr>

<tr>
<td class="keyword">Segmentation</td>
<td>
<div class="keywords form-group form-inline" id="pw-merge_vowels">
<label>merge vowels</label><input type="radio" name="pw-merge_vowels" value="True" checked />
<label>separate vowels</label><input type="radio" name="pw-merge_vowels" value="False" />
</div>
</td>
</tr>

<tr>
<td class="keyword">Scoring Settings</td>
<td>
<div class="keywords form-group form-inline" id="pw-distance">
<label>distance</label><input type="radio" name="pw-distance" value="True" checked />
<label>similarity</label><input type="radio" name="pw-distance" value="False" />
<label>Hamming</label><input type="radio" name="pw-distance" value="hamming" />
</div>
</td>
</tr>

<tr>
<td class="keyword">Sound Class Model</td>
<td>
<div class="keywords form-group form-inline" id="pw-model">
<label>DOLGO</label><input type="radio" name="pw-model" value="dolgo" />
<label>SCA</label><input type="radio" name="pw-model" value="sca" checked />
<label>ASJP</label><input type="radio" name="pw-model" value="asjp" />
</div>
</td>
</tr>
<tr>
<td class="keyword">Mode</td>
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
<td class="keyword">Gap Opening Penalty (GOP)</td>
<td>
<div class="keywords form-group form-inline">
<input class="form-control" id="pw-gop" type="number" value="-2" min="-10" max="0" />
</div>
</td>
</tr>
<tr>
<td class="keyword">Gap Extension Scale (GEP-Scale)</td>
<td>
<div class="keywords form-group form-inline">
<label><input id="pw-gep_scale" type="range" class="form-control" min="0" value="0.5" max="1" onchange="outputUpdate(value,'pw-gep_scale-fader')" step="0.05" /></label>
<label for="pw-gep-scale" id="pw-gep_scale-fader">0.5</label>
</div>
</td>
</tr>
<tr>
<td class="keyword">Prosodic Factor</td>
<td>
<div class="keywords form-group form-inline">
<label><input id="pw-factor" type="range" class="form-control" min="0" value="0.3" max="1" onchange="outputUpdate(value,'pw-factor-fader')" step="0.05" /></label>
<label for="pw-factor" id="pw-factor-fader">0.3</label>
</div>
</td>
</tr>

<tr>
<td class="keyword">Syllable Break Characters</td>
<td>
<div class="keywords form-group form-inline">
<input class="form-control" id="pw-restricted_chars" type="text" value="T_" />
</div>
</td>
</tr>


</table>
<br>


<table>
<tr>
<td style="vertical-align:top;">
<p><b>Select sequences from PSA files:</b></p>
<div class="form-group form-inline">
<select class="form-control" id="select_psa_files"></select>
<button class="btn btn-submit" onclick="palign('psa')" value="OK">SUBMIT</button>
</div>
<br>
<p><b>Type sequences directly into the text field:</b></p>
<textarea class="form-control" id="alms" cols="30" rows="10">
woldemort // waldemar
wladimir // woldemort
</textarea>
<div style="margin-top:10px;margin-bottom:10px;">
<button class="btn btn-submit" onclick="palign('seqs')" value="OK">SUBMIT</button>
</div>
</td>
<td style="vertical-align:top;">
<div style="float:left;display:none;margin-left:10px;border:2px solid lightgray;border-radius:5px;padding:10px;" id="alignments"></div></div>
</td>
</tr>
</table>



