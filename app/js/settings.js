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


