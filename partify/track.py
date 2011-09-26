from flask import jsonify, request, session, url_for

from partify import app
from partify.decorators import with_mpd

@app.route('/track/search', methods=['GET'])
@with_mpd
def track_search(mpd):
    """Performs a search on the MPD server for tracks matching the specified criteria (as arguments in the URL i.e. HTTP GETs)."""
    mpd_search_terms = []
    for term in ('artist', 'title', 'album'):
        if term in request.args:
            mpd_search_terms.append(term)
            mpd_search_terms.append(request.args[term])
      
    response = {}
          
    if len(mpd_search_terms) > 0:
        results = mpd.search(*mpd_search_terms)
        response['status'] = 'ok'
        response['results'] = _process_results(results, mpd_search_terms)
    else:
        response['status'] = 'error'
        response['message'] = 'No search criteria specified!'
    return jsonify(response)

def _process_results(results, search_terms):
    """Takes a result set in results and returns an organized result set sorted by the following criteria:

    * Sorted first by artist
    * Then by album
    * Then by order in album"""
    
    # Build a dict out of the search_terms list
    search_terms = dict( (k,v) for k,v in zip(search_terms[::2], search_terms[1::2]) )

    return sorted(results, key=lambda k: ( all( [k[term] != searched_term for term, searched_term in search_terms.items()] ), (k['album'], int(k['track']))) )