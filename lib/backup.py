#!/usr/bin/env python3
#
# megatron.thx 2024 Margate
#

import os
import json

#
# Note: so far only 2 level of dirs on home
# 
directories_bk = (
    ("~/.cache/chromium/", "vault/cache/chromium/"),
    ("~/.config/chromium/", "vault/config/chromium/"),
    ("~/.config/dconf/", "vault/config/dconf/"),
)

class Backup():
    def __init__(self):
        self.json_config_path = "vault/config.json"

        # initial values to write if json does not exist
        self.config = {
            "backup_number": 2,
            "backup_max": 2,
        }

    def run(self):
        self.config_load()
        self.create_dirs()
        self.backup_previous()
        self.config_dump()

    def config_load(self):
        if os.path.exists(self.json_config_path):
            print("reading " + self.json_config_path)
            with open(self.json_config_path, "r") as file:
                self.config = json.load(file)
        else:
            print("writing initial values vault/config.json")
            self.config_dump()

    def create_dirs(self):
        print("creating dirs")
        for (d1,d2) in directories_bk:
            for directory in (d1,d2):
                if not os.path.exists(directory):
                    command = "mkdir -p " + directory
                    print(command)
                    os.system(command)            

    def config_dump(self):
        print("writing " + self.json_config_path)
        with open(self.json_config_path, "w") as file:
            json.dump(self.config, file)

    def backup_previous(self):
        print("backup previous")
        if self.config["backup_number"] >= (self.config["backup_max"] - 1):
            self.config["backup_number"] = 0
        else:
            self.config["backup_number"] = self.config["backup_number"] + 1

        for(_, origin) in directories_bk:
            tokens = origin.split("/")
            dir_bk = tokens[1] + "_" + tokens[2] + "_bk_"
            destiny = "vault/" + dir_bk + str(self.config["backup_number"])+".tar.gz"

            if os.path.exists(destiny):
                command = "rm " + destiny
                print(command)
                os.system(command)

            command = "tar -czvf " + destiny + " " + origin
            print(command)
            os.system(command)

    def pre_chromium(self):
        print("restore from Persistent")
        for destiny, origin in directories_bk:
            command = "rsync -avz --delete " + origin + " " + destiny        
            print(command)
            os.system(command)

    def post_chromium(self):
        print("saving to Persistent")
        for origin, destiny in directories_bk:
            command = "rsync -avz --delete " + origin + " " + destiny
            print(command)
            os.system(command)

