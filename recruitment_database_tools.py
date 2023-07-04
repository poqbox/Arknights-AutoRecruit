import sqlite3
# import sqlite3tools as sql


# SQLite documentation: https://www.sqlite.org/datatype3.html


class tools:
    def __init__(self):
        self.con = sqlite3.connect("Recruit.db")
        self.cur = self.con.cursor()
        self.tag_legend = (
            "ROB", "STR", "SEN", "TOP",
            "MEL", "RNG",
            "CAS", "DEF", "GUA", "MED", "SNI", "SPE", "SUP", "VAN",
            "AOE", "CDC", "DBF", "DFS", "DPR", "DPS", "FRD", "HEA", "NUK", "SFT", "SLW", "SMN", "SPT", "SRV"
        )

    def create_table_Operators(self):
        self.cur.execute("create table Operators(id INTEGER, rarity INTEGER, name TEXT, tags TEXT, PRIMARY KEY (id))")


    def create_table_Tags(self):
        self.cur.execute("create table Tags(code TEXT, tag TEXT, type TEXT, PRIMARY KEY (code))")


    def create_table_OperatorTags(self):
        self.cur.execute("create table OperatorTags(id INTEGER, rarity INTEGER, tags TEXT, FOREIGN KEY (id) REFERENCES Operators(id))")


    def initial_Operators_inserts(self):
        data6 = [
            (6001, 6, "Angelina", ""),
            (6002, 6, "Exusiai", ""),
            (6003, 6, "Eyjafjalla", ""),
            (6004, 6, "Hoshiguma", ""),
            (6005, 6, "Ifrit", ""),
            (6006, 6, "Nightingale", ""),
            (6007, 6, "Saria", ""),
            (6008, 6, "Shining", ""),
            (6009, 6, "Siege", ""),
            (6010, 6, "SilverAsh", ""),
            (6011, 6, "Ch'en", ""),  # [1st-anni] update
            (6012, 6, "Skadi", ""),
            (6013, 6, "Hellagur", ""),
            (6014, 6, "Schwarz", ""),
            (6015, 6, "Magallan", ""),
            (6016, 6, "Mostima", ""),
            (6017, 6, "Blaze", ""),
            (6018, 6, "Aak", ""),
            (6019, 6, "Ceobe", ""),
            (6020, 6, "Bagpipe", ""),
            (6021, 6, "Phantom", ""),
            (6022, 6, "Weedy", "")
        ]
        data5 = [
            (5001, 5, "Texas", ""),
            (5002, 5, "Zima", ""),
            (5003, 5, "Ptilopsis", ""),
            (5004, 5, "Silence", ""),
            (5005, 5, "Warfarin", ""),
            (5006, 5, "Projekt Red", ""),
            (5007, 5, "Manticore", ""),
            (5008, 5, "Cliffheart", ""),
            (5009, 5, "FEater", ""),
            (5010, 5, "Provence", ""),
            (5011, 5, "Blue Poison", ""),
            (5012, 5, "Firewatch", ""),
            (5013, 5, "Meteorite", ""),
            (5014, 5, "Platinum", ""),
            (5015, 5, "Pramanix", ""),
            (5016, 5, "Istina", ""),
            (5017, 5, "Mayer", ""),
            (5018, 5, "Specter", ""),
            (5019, 5, "Indra", ""),
            (5020, 5, "Nearl", ""),
            (5021, 5, "Liskarm", ""),
            (5022, 5, "Vulcan", ""),
            (5023, 5, "Croissant", ""),
            (5024, 5, "Nightmare", ""),  # [1st-anni] update
            (5025, 5, "Swire", ""),
            (5026, 5, "Astesia", ""),
            (5027, 5, "Glaucus", ""),
            (5028, 5, "Executor", ""),
            (5029, 5, "Waai Fu", ""),
            (5030, 5, "Broca", ""),
            (5031, 5, "GreyThroat", ""),
            (5032, 5, "Reed", ""),
            (5033, 5, "Hung", ""),
            (5034, 5, "Leizi", ""),
            (5035, 5, "Sesa", ""),
            (5036, 5, "Shamare", ""),
            (5037, 5, "Asbestos", ""),
            (5038, 5, "Elysium", ""),
            (5039, 5, "Tsukinogi", "")
        ]
        data4 = [
            (4001, 4, "Cuora", ""),
            (4002, 4, "Dobermann", ""),
            (4003, 4, "Earthspirit", ""),
            (4004, 4, "Estelle", ""),
            (4005, 4, "Frostleaf", ""),
            (4006, 4, "Gitano", ""),
            (4007, 4, "Gravel", ""),
            (4008, 4, "Gummy", ""),
            (4009, 4, "Haze", ""),
            (4010, 4, "Jessica", ""),
            (4011, 4, "Matoimaru", ""),
            (4012, 4, "Matterhorn", ""),
            (4013, 4, "Meteor", ""),
            (4014, 4, "Mousse", ""),
            (4015, 4, "Myrrh", ""),
            (4016, 4, "Perfumer", ""),
            (4017, 4, "Rope", ""),
            (4018, 4, "Scavenger", ""),
            (4019, 4, "Shaw", ""),
            (4020, 4, "Shirayuki", ""),
            (4021, 4, "Vigna", ""),
            (4022, 4, "Beehunter", ""),  # [1st-anni] update
            (4023, 4, "Greyy", ""),
            (4024, 4, "Myrtle", ""),
            (4025, 4, "Sussuro", ""),
            (4026, 4, "Vermeil", ""),
            (4027, 4, "May", ""),
            (4028, 4, "Ambriel", ""),
            (4029, 4, "Purestream", ""),
            (4030, 4, "Utage", ""),
            (4031, 4, "Cutter", "")
        ]
        data3 = [
            (3001, 3, "Adnachiel", ""),
            (3002, 3, "Ansel", ""),
            (3003, 3, "Beagle", ""),
            (3004, 3, "Fang", ""),
            (3005, 3, "Hibiscus", ""),
            (3006, 3, "Kroos", ""),
            (3007, 3, "Lava", ""),
            (3008, 3, "Melantha", ""),
            (3009, 3, "Orchid", ""),
            (3010, 3, "Plume", ""),
            (3011, 3, "Steward", ""),
            (3012, 3, "Vanilla", ""),
            (3013, 3, "Catapult", ""),  # [1st-anni] update
            (3014, 3, "Midnight", ""),
            (3015, 3, "Popukar", ""),
            (3016, 3, "Spot", "")
        ]
        data2 = [
            (2001, 2, "12F", ""),
            (2002, 2, "Durin", ""),
            (2003, 2, "Noir Corne", ""),
            (2004, 2, "Rangers", ""),
            (2005, 2, "Yato", "")
        ]
        data1 = [
            (1001, 1, "Castle-3", ""),
            (1002, 1, "Lancet-2", ""),
            (1003, 1, "THRM-EX", ""),  # [1st-anni] update
            (1004, 1, "'Justice Knight'", "")
        ]
        self.cur.executemany("insert into Operators values(?, ?, ?, ?)", data1)
        self.cur.executemany("insert into Operators values(?, ?, ?, ?)", data2)
        self.cur.executemany("insert into Operators values(?, ?, ?, ?)", data3)
        self.cur.executemany("insert into Operators values(?, ?, ?, ?)", data4)
        self.cur.executemany("insert into Operators values(?, ?, ?, ?)", data5)
        self.cur.executemany("insert into Operators values(?, ?, ?, ?)", data6)
        self.con.commit()


    def initial_Tags_inserts(self):
        data1 = [
            ("ROB", "Robot", "Qual"),
            ("STR", "Starter", "Qual"),
            ("SEN", "Senior Operator", "Qual"),
            ("TOP", "Top Operator", "Qual")
        ]
        data2 = [
            ("MEL", "Melee", "Pos"),
            ("RNG", "Ranged", "Pos")
        ]
        data3 = [
            ("CAS", "Caster", "Class"),
            ("DEF", "Defender", "Class"),
            ("GUA", "Guard", "Class"),
            ("MED", "Medic", "Class"),
            ("SNI", "Sniper", "Class"),
            ("SPE", "Specialist", "Class"),
            ("SUP", "Supporter", "Class"),
            ("VAN", "Vanguard", "Class")
        ]
        data4 = [
            ("AOE", "AOE", "Spec"),
            ("CDC", "Crowd Control", "Spec"),
            ("DBF", "Debuff", "Spec"),
            ("DFS", "Defense", "Spec"),
            ("DPR", "DP-Recovery", "Spec"),
            ("DPS", "DPS", "Spec"),
            ("FRD", "Fast-Redeploy", "Spec"),
            ("HEA", "Healing", "Spec"),
            ("NUK", "Nuker", "Spec"),
            ("SFT", "Shift", "Spec"),
            ("SLW", "Slow", "Spec"),
            ("SMN", "Summon", "Spec"),
            ("SPT", "Support", "Spec"),
            ("SRV", "Survival", "Spec")
        ]
        cur.executemany("insert into Tags values(?, ?, ?)", data1)
        cur.executemany("insert into Tags values(?, ?, ?)", data2)
        cur.executemany("insert into Tags values(?, ?, ?)", data3)
        cur.executemany("insert into Tags values(?, ?, ?)", data4)
        con.commit()


    def initial_OperatorTags_inserts(self):
        self.con.commit()


    # def initial_guaranteed_tag_combination_inserts():
    #     data1 = [
    #         (1, 1, "ROBGUA"),
    #         (1, 1, "ROBGUAMEL"),
    #         (1, 1, "ROBSPTMEL"),
    #         (1, 1, "ROBSPTGUA"),
    #         (2, 1, "ROBHEA"),
    #         (2, 1, "ROBMED"),
    #         (2, 1, "ROBHEARNG"),
    #         (2, 1, "ROBHEAMED"),
    #         (2, 1, "ROBMEDRNG"),
    #         (3, 1, "NUKSPE"),
    #         (3, 1, "ROBSPE"),
    #         (3, 1, "ROBNUK"),
    #         (3, 1, "NUKSPEMEL"),
    #         (3, 1, "ROBSPEMEL"),
    #         (3, 1, "ROBNUKMEL"),
    #         (3, 1, "ROBNUKSPE"),
    #         (4, 1, "SPTSNI"),
    #         (4, 1, "ROBSNI"),
    #         (4, 1, "ROBSPTSNI"),
    #         (4, 1, "ROBSNIRNG"),
    #         (4, 1, "ROBSPTSNI"),
    #         (4, 1, "SPTSNIRNG")
    #     ]
    #     data2 = [
    #         (3, 2, "STRDEF"),
    #         (3, 2, "STRDEFMEL"),
    #         (4, 2, "STRSNI"),
    #         (4, 2, "STRSNIRNG"),
    #         (5, 2, "STRVAN"),
    #         (5, 2, "STRVANMEL")
    #     ]
    #     data3 = [
    #         # N/A
    #     ]


    def view_all_tables(self):
        """The table containing the names of all tables is: sqlite_master"""

        self.cur.execute("select name from sqlite_master where type = 'table'")
        table_list = self.cur.fetchall()
        for row in table_list:
            print(row[0])


    def drop_table(self):
        self.cur.execute("drop table Operators")


    def delete_all_rows(self):
        self.cur.execute("delete from Operators")
        self.con.commit()


    def delete_TagCombinations_row(self, tags):
        """Tags should be a string.

        Refer to the tags legend for the code of each tag."""
        self.cur.execute("delete from TagCombinations where tags = ?", [tags])
        self.con.commit()


    def update_OperatorTags_row(self, orig_id, orig_rarity, orig_tags, new_id, new_rarity, new_tags):
        entities = (new_id, new_rarity, new_tags, orig_id, orig_rarity, orig_tags)
        self.cur.execute("update OperatorTags set id=?, rarity=?, tags=? where id=?, rarity=?, tags=?", entities)
        self.con.commit()


    def insert_new_operator(self, operator_name: str, rarity: int, tag_list):
        """tags is a list of tag codes. Refer to the tags legend for the code of each tag."""
        if not tag_list:
            print("Please select some tags")
            return
        for tag in tag_list:
            if tag not in self.tag_legend:
                print("One of the tags is not a valid tag")
                return
        operator_tags = "".join(tag_list)
        if self.cur.execute("select count(*) from Operators where rarity=?", [rarity]).fetchone()[0] == 0:
            id = (rarity * 4) + 1
        else:
            id = self.cur.execute("select id from Operators where rarity = ? order by id desc limit 1", [rarity]).fetchone()[0] + 1
        self.cur.execute("insert into Operators values (?, ?, ?, ?)", (id, rarity, operator_name, operator_tags))
        self.con.commit()


    def update_operator(self, orig_id=None, orig_name=None, new_name=None, new_tags=[]):
        """Provide either orig_id or orig_name, then provide any number of new variables.

        If both orig_id or orig_name are provided, then orig_id will be used to identify the operator.

        new_tags is a list of tag codes. Refer to the tags legend for the code of each tag."""

        # return if identifiers are not provided
        if orig_id == None and orig_name == None:
            print("One of the following was not provided: orig_id, orig_name")
            print("The table will not be updated")
            return

        res = self.cur.execute("select id from Operators")
        ids_list = [row[0] for row in res]
        res = self.cur.execute("select name from Operators")
        names_list = [name[0] for name in res]
        # return if orig_id could not be located
        if orig_id != None and orig_id not in ids_list:
            print("Could not locate ID", orig_id)
            print("The table will not be updated")
            return
        # return if orig_name could not be located
        if orig_name != None and orig_name not in names_list:
            print('Could not locate operator name "' + orig_name + '"')
            print("The table will not be updated")
            return
        # return if orig_name is being used, but there are more than one operators with the same name
        if orig_id == None and orig_name != None:
            op_id = []
            res = self.cur.execute("select id, name from Operators")
            for row in res:
                if row[1] == orig_name:
                    op_id.append(row[0])
            num_ops = len(op_id)
            if num_ops > 1:
                print('There exists', num_ops, 'with the name "' + orig_name + '"')
                print("The table will not be updated")
                print("Please provide the operator's ID instead")
                print("Their IDs are: ", end="")
                print(*op_id)
                return

        # return if new entities are not provided
        if new_name == None and new_tags == None:
            print("At least one of the following was not provided: new_name, new_tags")
            print("The table will not be updated")
            return

        # update operator
        provided_entities = [False, False]
        entities = []
        if new_name != None:
            provided_entities[0] = True
            entities.append(new_name)
        if new_tags:
            for tag in new_tags:
                if tag not in self.tag_legend:
                    print("At least one of the tags is not a valid tag")
                    print("The table will not be updated")
                    return
            provided_entities[1] = True
            operator_tags = "".join(new_tags)
            entities.append(operator_tags)

        # prepare update query
        query = "update Operators set "
        for i in range(len(provided_entities)):
            if provided_entities[i]:
                if i == 0:
                    query += "name=?, "
                if i == 1:
                    query += "tags=?, "
        query = query[:-2]
        if orig_id != None:
            entities.append(orig_id)
            self.cur.execute(query + " where id=?", entities)
            self.con.commit()
            return
        elif orig_name != None:
            entities.append(orig_name)
            self.cur.execute(query + " where name=?", entities)
            self.con.commit()
            return
        print("Error: the table could not be updated")


    def delete_operator(self, id):
        self.cur.execute("delete from Operators where id=?", [id])
        self.con.commit()


    def select_all_from_Operators(self):
        operator_list = []
        res = self.cur.execute("select * from Operators")
        for row in res:
            operator_list.append(row)
        return operator_list


    # [Il Siracusano] update
    # SETUP: create a table of operators and the individual tags that could lead to them [formula?]
    # AUTO-RECRUITING:
    #   when calculating, create a list from the table above using the give tags
    #   in the TagCombinations table, search only for operators in the list

    # tags legend:
    #   a tag is represented by a string of three letters
    #   Qualification:
    #       ROB - Robot
    #       STR - Starter
    #       SEN - Senior Operator
    #       TOP - Top Operator
    #   Position:
    #       MEL - Melee
    #       RNG - Ranged
    #   Class:
    #       CAS - Caster
    #       DEF - Defender
    #       GUA - Guard
    #       MED - Medic
    #       SNI - Sniper
    #       SPE - Specialist
    #       SUP - Supporter
    #       VAN - Vanguard
    #   Specification:
    #       AOE - AOE
    #       CDC - Crowd Control
    #       DBF - Debuff
    #       DFS - Defense
    #       DPR - DP-Recovery
    #       DPS - DPS
    #       FRD - Fast-Redeploy
    #       HEA - Healing
    #       NUK - Nuker
    #       SFT - Shift
    #       SLW - Slow
    #       SMN - Summon
    #       SPT - Support
    #       SRV - Survival

    # for row in cur.execute("select * from Tags order by type"):
    #     print(row)

    def close_db(self):
        self.con.close()


def test():
    db_tools = tools()
    # db_tools.insert_new_operator("Cat", 1, ["ROB", "SPE", "CDC"])
    # db_tools.update_operator(orig_name="Cat", new_tags=["ROB", "SPE"])
    # db_tools.delete_operator(1005)
    operator_table = db_tools.select_all_from_Operators()
    for row in operator_table:
        print(row)
    db_tools.close_db()


if __name__ == "__main__":
    test()
