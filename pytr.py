#!/usr/bin/python

import pysftp #sftp connection manager

import sys, getopt #command line parameter system

import time

import curses

#read configration file
def openConfig ():

    config_dictionary = {}

    config_name = "/etc/pytr.conf"

    try:
        print "\n" + "Reading configuration file" + "\n"
        config_file = open(config_name, "r")

    except:

        print "Cant find config file"
        print "...exiting program..."
        sys.exit(1)

    for line in config_file:

        words = line.split("=")

        if "#" not in words[0]:

            if "user" in words[0]:
                print "Found user: " + words[1]
                config_dict = {words[0].strip(): words[1].strip()}
                config_dictionary.update(config_dict)
                # add here other config code

            if "password" in words[0]:
                print "Found password for user \n"
                config_dict = {words[0].strip(): words[1].strip()}
                config_dictionary.update(config_dict)
                # add here other config code


            if "sftp" in  words[0]:
                print "Testing server: " + words[1]
                config_dict = {words[0].strip() : words[1].strip()}
                config_dictionary.update(config_dict)

            if "directory" in words[0]:
                print "directory to save file: " + words[1]
                config_dict = {words[0].strip() : words[1].strip()}
                config_dictionary.update(config_dict)

    return config_dictionary

def main (argv):

    cnopts = pysftp.CnOpts()
    
    cnopts.hostkeys = None

    config = openConfig()

    ftp_srv = pysftp.Connection(host=config.get("sftp"), username=config.get("user"), password=config.get("password"),cnopts=cnopts)

    ftp_srv.chdir(config.get("directory"))

    print "Remote Dir:" + ftp_srv.pwd

    for arg in argv:
        #ftp_srv.put(arg)
        ftp_srv.put(localpath=arg,remotepath=config.get("directory")+"/"+arg,callback=perc_f,confirm=True,preserve_mtime=True)
        print "\n" #is a return from call back function

    ftp_srv.close()

def perc_f (x,y):
    sys.stdout.write ("\r" + str(x) + " -- " + str(y) + " > " + str(int(100*float(float(x)/float(y)))) + "%")
    sys.stdout.flush()



if __name__ == "__main__":
    main(sys.argv[1:])
