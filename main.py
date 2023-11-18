# import libraries
from Code import gui, database_manager
import pymongo

"""
    Run main progran
"""
if __name__ == '__main__':
    # make connection to MongoDB
    dbm = database_manager.Database_Manager()
    client = dbm.get_client()
    #dbm.search_data(id="2")
    query, result = dbm.search_reviews(id="2")
    dbm.sort_data("AmazonDB", query, [("Id", pymongo.ASCENDING)])
    # open gui
    gui = gui.GUI(dbm)
    gui.Create_Page()
    gui.Run()

    # close connection
    client.close()
