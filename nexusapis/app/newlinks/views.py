from app.newlinks import newlinks
from flask import render_template, flash, redirect, session, g, request, url_for, abort, jsonify
from utils_crawler import *

##Usage: http://localhost:5000/newlinks/randomrandom/?_token=NexusToken
## http://localhost:5000/newlinks/randomrandom?_token=NexusToken
@newlinks.route('/randomrandom/')
def show():
    return jsonify({'message':'randomrandom success'}), 200
    # resp = Response(response=jsonify({'message':'randomrandom'}), 
    #     status=200, 
    #     mimetype="application/json")
    # return(resp)

@newlinks.route('/')
def home():
    return jsonify({'message':'Token works!'}), 200

##TODO: can be handled by session for now, then persistence can be brought in picture
##Usage: http://localhost:5000/newlinks/startwork/?_token=NexusToken2&workname=wow5

##TODO: GET or PUSH??? 
@newlinks.route('/startwork/', methods=['GET'])
def startWork():
    ##against the token number in session dict
    ##save a dict with workname given
    ##no startwork can begin till this token dict in session
    ##endwork will remove the token dict!
    ##TODO: remove this work from session after an hour

    ##two args needed here thus!
    if session.get(request.args.get('_token'),None) is not None:
        return jsonify({'message': 'startwork: Already in progress, use endwork first'}), 400
    
    timenow = getTimeNow()
    
    workname = request.args.get('workname',None)
    tokenid = request.args.get('_token')

    if workname is None:
        return jsonify({'message': 'startwork: Cannot start, no workname given to start'}), 400    

    to_save_dict = {}
    to_save_dict['_token'] = tokenid ## no sense, butfor better http response
    to_save_dict['workname'] = workname
    to_save_dict['starttime'] = timenow
    to_save_dict['status'] = 'Active'

    session[tokenid] = to_save_dict
    print session[tokenid]
    return jsonify(to_save_dict), 200

##Usage: http://localhost:5000/newlinks/endwork/?_token=NexusToken2
@newlinks.route('/endwork/', methods=['GET'])
def endWork():

    ##only one arg needed here!

    if session.get(request.args.get('_token'),None) is None:
        return jsonify({'message': 'endwork: No work against your token in progress, use startwork first'}), 400

    timenow = getTimeNow()

    tokenid = request.args.get('_token')
    popped_obj = session.pop(tokenid)
    popped_obj['endtime'] = timenow
    popped_obj['status'] = 'Ended' 
    
    return jsonify(popped_obj), 200

@newlinks.route('/pushlinked/', methods=['POST'])
def pushLinked():
    return jsonify({'message': 'pushlinked: Success'}), 200