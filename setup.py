import mongoengine

#  Verify mongo exists and is running, set up database schema 

mongoengine.connect('tokenInfo', host='localhost', port=27017)

