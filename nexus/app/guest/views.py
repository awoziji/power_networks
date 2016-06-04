from app.guest import guest
from flask import render_template, flash, redirect, session, g, request, url_for, abort
from app.solr.SolrIndex import *

@guest.route('/')
def show():
    import hashlib
    text = hashlib.md5("yoyo").hexdigest()
    return render_template("temp.html", homeclass="active", temptext=text)

@guest.route('/temp2/')
def temp2():
    from app.models.dbmodels.index_entities import Entity
    print 'should work fine'
    #Entity.del_all_entities()
    #en = Entity(4, 'Kapil', 'person,politician', 'Kapil, Thakkar', 'gujrat iit mumbai')
    #rows = en.insertEntity()
    #en.name = 'Amartya'
    #en.updateEntity()
    en2= Entity()
    en2.getEntity(4)
    print 'will be here if all fine'
    return render_template("temp.html", homeclass="active", temptext ='You are here '+en2.name+' '+en2.labels)

@guest.route('/meta/')
def meta():
    from app.models.dbmodels.user import User
    print 'should work fine'
    usr = User('amartya', 'yummytummy', 5)
    usr.insert()
    usr2 = User('abhishek', 'zzzzzz')
    usr2.insert()
    usr2.password = 'wewrerw'
    usr2.update('password')
    print usr2.validateUser('yummytummy')
    usr2.role = 3
    usr2.keyEnabled = 1
    usr2.update('all')

    print 'will be here if all fine'
    return render_template("temp.html", homeclass="active", temptext='You are here ' + usr.userid + ' ' + usr2.userid)


@guest.route('/temp3/')
def temp3():
    from app.utils.locprocess import getCityState
    (city,state) = getCityState('pondicherry')
    return render_template("temp.html", homeclass="active", temptext=city+' '+state)

@guest.route('/viz/', methods=['GET', 'POST'])
def viz():
    ##get cypher from request.args['cypher']

    ## use constant variables

    ##cypher variable is the one having query
    ##task 1 validate if query is read query - at start assume the query is valid

    ##### any validation function can be moved to graphdb.py later to see if the query is read or not.
    ##### use cypher card  : http://neo4j.com/docs/cypher-refcard/current/
    #####  CREATE, MERGE, DELETE, REMOVE, SET, INDEX, LOAD, LOAD CSV, CONSTRAINT, any case
    ##### nodes return, mandatory

    ##task 2 fecth the results of the query
    ##task 3 show on viz.html or something

    ##to decide: post or not?
    from app.utils.validate_cypher import isValidCypher

    cypher = request.form.get('query')
    print cypher

    from app.constants import CORE_GRAPH_HOST, CORE_GRAPH_PASSWORD, CORE_GRAPH_PORT, CORE_GRAPH_USER

    ## TODO: constants
    if isValidCypher(cypher):
        return render_template("viz2.html", homeclass="active", temptext=cypher, 
            CORE_GRAPH_HOST =CORE_GRAPH_HOST, CORE_GRAPH_PASSWORD = CORE_GRAPH_PASSWORD, 
            CORE_GRAPH_PORT = CORE_GRAPH_PORT, CORE_GRAPH_USER = CORE_GRAPH_USER)
    else:
        flash('Invalid query')
        return render_template("viz2.html", homeclass="active", temptext='', 
            CORE_GRAPH_HOST =CORE_GRAPH_HOST, CORE_GRAPH_PASSWORD = CORE_GRAPH_PASSWORD, 
            CORE_GRAPH_PORT = CORE_GRAPH_PORT, CORE_GRAPH_USER = CORE_GRAPH_USER)

@guest.route('/temp4/')
def solr():
    delete_index()
    full_import()
    print 'will be here if all fine'
    return render_template("temp.html", homeclass="active", temptext = 'You are here')
