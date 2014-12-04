A LingPy GUI based on a webserver
=================================

The basic idea of this LingPy plugin is to provide GUI-like functionality
by setting up a local webserver which is used to communicate with LingPy.
The communication is managed in a very simple way: The web-interface uses
HTML and JavaScript to offer basic functions available in LingPy.
With help of JavaScript ajax-requests, queries are passed to LingPy and answered right away. The answer is then retrieved and presented with help of JavaScript.

The local server itself is structured in such a way that it allows to display HTML/JavaScript in full. Small modifications have been made in order to guarantee that the server can receive commands from GET requests and pass them over to LingPy. 

In this system, the Edictor can also be fully integrated, since it is easy to manage an sqlite3 backend that behaves similar to the current PHP version. Furthermore, remote access can in theory also be managed in the future:

* Instead of sending ajax requests which are not allowed in normal servers in order to pass and get the data from remote, the local server can be structured in such a way that it catches outgoing commands and retrieves the results via Python's urllib.
* This guarantees ideally that a user then has full access to both external sources which are managed with the PHP-based simple remote server, and the full functionality of LingPy.

Things that can be done with these settings are:

* loading a TSV file, having it preprocessed using tokenization procedures and the like
* having LingPy search for cognate sets and displaying the results in the Edictor
* having LingPy conduct alignment analyses while editing cognate sets with the Edictor
* displaying results of phylogenetic reconstruction (using Neighbor-Joining or other algorithms) directly in the browser
* etc., etc.

There are surely many, many possibilities here. We just have to find a way how to structure everything nicely.

## Next Steps

* manage remote file access in ajax statements by catching specific statements and having Python handle downloading and sending them (this should be easily doable by defining a specific "outgoing portal" which is catched by the server and then served accordingly) **already done, at least basically**
* manage the whole interactive interface and define the wanted functionalities
* manage a cache directory in which data will be stored temporarily (especially when downloading things with urllib, but this could be the basic Python cache) 
* arrange the server in such a way that once it is being given Markdown files it serves them with a given header and converts them to HTML **done**
* arrange some quit-button that stops the server process (basic should be some interface website) **done, added a quit button that stops the server, but the user has to close the website**

## Current experience with Remote access

Using the remote capabilities of Python and catching them witht he server is working excellent. It is possible now to use the Edictor as in the web-version, that is:

* opening a remote database (server catches this and provides the relevant data)
* modifying local database and sending modifications back to remote server (using specific authentication routines in python's urllib)

What we need as a next point for this kind of functionality is a real prompt for the user where the user can then login. This is probably best done with HTML/JS again, we just create a new page for login, in case the user has not yet been logged in, and then we offer the typical prompt. Once this has been submitted, we close the window again using window.close() function in JS:

* http://stackoverflow.com/questions/2076299/how-to-close-current-tab-in-a-browser-window

This would give the user the "look and feel" of some application with regular login.

## User access to home directory files

We provide general user access to home directory files in a very simply way by which the user's home directory is also searched for files which cannot be served by the server internally. This is useful for later on when the user may want to load external files quickly.

## Modularizing the application

In the current version, all code is in the server.py file. This should be changed: Modules need to be provided for each access to specific lingpy functions. The current HTML structure has:

* HOME: basic homepage that introduces the server
* Models (allowing the user to define his or her own models)
  - Segmentation (dealing with segmentation issues, like tokenization, syllable segmentation, and the like
  - sound classes (dealing with soudn class conversion)
  - prosodic strings (dealing with the representation of prostrings)
  - scoring functions (dealing with the way segments are scored in sequence alignment)
* Sequences (allowing the user to test segmentation with specific models, but also to align sequences, basically provided for illustration of algorithms and testing)
  - segmentize (dealing with segmentation)
  - sound classes (dealing with sound class conversion)
  - pairwise (dealing with pairwise alignments **already more or less implemented**)
  - multiple (dealing with multiple alignments **already more or less implemented**)
* Lanugages (dealing with whole applications, allows quick access without creating a project to main LingPy functionalities)
  - cognate detection (dealing with basic cognate detection)
  - multiple alignment (dealing with alignment representation of detected cognates)
  - borrowing detection (dealing with incongruencies in the cognate sets, using MLN method)
  - cluster (dealing with basic cluster applications, using LingPy's cluster module to compute phylogenetic trees and the like
* projects (core part of the server that allows users to create their projects and use LingPy to help where it can help while users will be able to interfere with the workflow by applying manual corrections)
  - create (create a new project, using input files, templates, and the like)
  - browse (allow user to browse ongoing projects at different stages)
* edit (link to the edictor, should later be merged with "browse" and allow the user to manually edit projects with the edictor)
* close (closes the application **already implemented**)

This strucutre is not complete and perfect at the moment, and it needs refinement, but having both the direct access to lingpy functions and providing the possibility to work on whole projects should be one general goal here.
  



