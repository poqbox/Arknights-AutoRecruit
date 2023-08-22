import sqlite3
# import sqlite3tools as sql


# SQLite documentation: https://www.sqlite.org/datatype3.html


class tools:
    def __init__(self):
        self.con = sqlite3.connect("Recruit.db")
        self.cur = self.con.cursor()
        self.non_dist_combos, self.r4_tag_combos_dist, self.r5_tag_combos_dist, self.r6_tag_combos_dist = self.get_recruit_data_from_text_file()
        self.tag_legend = (
            "ROB", "STR", "SEN", "TOP",
            "MEL", "RNG",
            "CAS", "DEF", "GUA", "MED",
            "SNI", "SPE", "SUP", "VAN",
            "AOE", "CDC", "DBF", "DFS", "DPR", "DPS", "FRD", "HEA", "NUK", "SFT", "SLW", "SMN", "SPT", "SRV"
        )
        self.tag_dict = {
            "ROB": "Robot",
            "STR": "Starter",
            "SEN": "Senior Operator",
            "TOP": "Top Operator",
            "MEL": "Melee",
            "RNG": "Ranged",
            "CAS": "Caster",
            "DEF": "Defender",
            "GUA": "Guard",
            "MED": "Medic",
            "SNI": "Sniper",
            "SPE": "Specialist",
            "SUP": "Supporter",
            "VAN": "Vanguard",
            "AOE": "AoE",
            "CDC": "Crowd Control",
            "DBF": "Debuff",
            "DFS": "Defense",
            "DPR": "DP-Recovery",
            "DPS": "DPS",
            "FRD": "Fast-Redeploy",
            "HEA": "Healing",
            "NUK": "Nuker",
            "SFT": "Shift",
            "SLW": "Slow",
            "SMN": "Summon",
            "SPT": "Support",
            "SRV": "Survival"
        }
        # retrieve recruitment data


    def open_db(self):
        self.con = sqlite3.connect("Recruit.db")
        self.cur = self.con.cursor()


    def create_table_Operators(self):
        self.cur.execute("create table Operators(id INTEGER, rarity INTEGER, name TEXT, tags TEXT, PRIMARY KEY (id))")


    def create_table_Tags(self):
        self.cur.execute("create table Tags(code TEXT, tag TEXT, type TEXT, PRIMARY KEY (code))")


    def initial_Operators_inserts(self):
        data6 = [
            (6001, 6, "Exusiai", ""),
            (6002, 6, "Hoshiguma", ""),
            (6003, 6, "Ifrit", ""),
            (6004, 6, "Nightingale", ""),
            (6005, 6, "Saria", ""),
            (6006, 6, "Shining", ""),
            (6007, 6, "Siege", ""),
            (6008, 6, "SilverAsh", ""),
            (6009, 6, "Ch'en", ""),  # [1st-anni] update
            (6010, 6, "Skadi", ""),
            (6011, 6, "Hellagur", ""),
            (6012, 6, "Schwarz", ""),
            (6013, 6, "Magallan", ""),
            (6014, 6, "Mostima", ""),
            (6015, 6, "Blaze", ""),
            (6016, 6, "Aak", ""),
            (6017, 6, "Ceobe", ""),
            (6018, 6, "Bagpipe", ""),
            (6019, 6, "Phantom", ""),
            (6020, 6, "Weedy", "")
        ]
        data5 = [
            (5001, 5, "Blue Poison", ""),
            (5002, 5, "Cliffheart", ""),
            (5003, 5, "Croissant", ""),
            (5004, 5, "FEater", ""),
            (5005, 5, "Firewatch", ""),
            (5006, 5, "Indra", ""),
            (5007, 5, "Istina", ""),
            (5008, 5, "Liskarm", ""),
            (5009, 5, "Manticore", ""),
            (5010, 5, "Mayer", ""),
            (5011, 5, "Meteorite", ""),
            (5012, 5, "Nearl", ""),
            (5013, 5, "Platinum", ""),
            (5014, 5, "Pramanix", ""),
            (5015, 5, "Projekt Red", ""),
            (5016, 5, "Provence", ""),
            (5017, 5, "Ptilopsis", ""),
            (5018, 5, "Specter", ""),
            (5019, 5, "Silence", ""),
            (5020, 5, "Texas", ""),
            (5021, 5, "Vulcan", ""),
            (5022, 5, "Warfarin", ""),
            (5023, 5, "Zima", ""),
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
            ("AOE", "AoE", "Spec"),
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


    def view_all_tables(self):
        """
        Prints the name of all tables in the database
        """
        # The table containing the names of all tables is: sqlite_master
        self.cur.execute("select name from sqlite_master where type='table'")
        table_list = self.cur.fetchall()
        for row in table_list:
            print(row[0])


    def split_tags(self, tags_keys: str):
        """
        Splits a string of coded tags into their individual codes\n
        Returns them in a list
        """
        if len(tags_keys) % 3 != 0:
            print("Error: tags string is formatted incorrectly")
            return
        tags_list = []
        while tags_keys:
            tag = tags_keys[0:3]
            tags_keys = tags_keys[3:]
            tags_list.append(tag)
        return tags_list


    def decode_tags(self, tags_keys: str):
        """
        Splits a string of coded tags into their full-named tags\n
        Returns them in a list
        """
        if len(tags_keys) % 3 != 0:
            print("Error: tags string is formatted incorrectly")
            return
        tags_full = []
        while tags_keys:
            tag = tags_keys[0:3]
            tags_keys = tags_keys[3:]
            tags_full.append(self.tag_dict.get(tag))
        return tags_full


    def get_operator_data(self, get: list, where=None, sort_order=None, limit=None, offset=None, get_full_tags=False, reduce_nested_lists=False):
        """
        get: "id"|"rarity|"name"|"tags"\n
        sort_order: List[List[str]] sorting parameters of the form [sort, order]\n
        sort: "id"|"rarity|"name"\n
        order: "asc"|"desc"\n
        """
        operator_list = []
        query = ""
        # SELECT statement
        columns = []
        col_list = ["id", "rarity", "name", "tags"]
        if get[0] == "all" or get[0] == "ALL" or get[0] == "*":
            columns = col_list
            query = "select * from Operators"
        else:
            for col_name in col_list:
                if col_name.lower() in get or col_name.upper() in get:
                    columns.append(col_name)
            query = "select " + ", ".join(columns) + " from Operators"
        # WHERE clause
        if where:
            query += " where " + " or ".join(where)
        # ORDER BY clause
        if sort_order:
            query += " order by " + ", ".join([" ".join(group) for group in sort_order])
        # LIMIT clause
        if limit:
            query += " limit " + str(limit)
            # OFFSET clause
            if offset:
                query += " offset " + str(offset)
        res = self.cur.execute(query)
        if reduce_nested_lists and len(columns) == 1:
            for col in res:
                operator_list.append(col[0])
        else:
            for col in res:
                operator_list.append(list(col))
        if get_full_tags:
            tag_col = columns.index("tags")
            for i in range(len(operator_list)):
                operator_list[i][tag_col] = self.decode_tags(operator_list[i][tag_col])
        return operator_list


    def insert_new_operator(self, operator_name: str, rarity: int, tag_list):
        """
        tags is a list of tag codes. Refer to the tags legend for the code of each tag.
        """
        if not tag_list:
            print("Please select some tags")
            return
        for tag in tag_list:
            if tag not in self.tag_legend:
                print("One of the tags is not a valid tag")
                return
        operator_tags = "".join(tag_list)
        if self.cur.execute("select count(*) from Operators where rarity=?", [str(rarity)]).fetchone()[0] == 0:
            id = (rarity * 4) + 1
        else:
            id = self.cur.execute("select id from Operators where rarity=? order by id desc limit 1", [str(rarity)]).fetchone()[0] + 1
        self.cur.execute("insert into Operators values (?, ?, ?, ?)", (str(id), str(rarity), operator_name, operator_tags))
        self.con.commit()


    def update_operator(self, orig_id=None, orig_name=None, new_name=None, new_tags=[]):
        """
        Provide either orig_id or orig_name, then provide any number of new variables.\n
        If both orig_id or orig_name are provided, then orig_id will be used to identify the operator.\n
        new_tags is a list of tag codes. Refer to the tags legend for the code of each tag.
        """
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

        # UPDATE statement
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
        self.cur.execute("delete from Operators where id=?", (str(id)))
        self.con.commit()


    def get_unique_tags(self, rarity: int):
        """
        Returns a list of tag codes
        """
        tags_list = []
        result = self.cur.execute("select tags from Operators where rarity=?", (str(rarity)))
        for row in result:
            for tags in row:
                if tags not in tags_list:
                    tags_list.append(tags)
        return tags_list


    def get_non_distinctions_tags(self):
        """
        Returns a list of tag codes
        """
        rarity_2_3_tags_list = []
        all_tags = self.get_unique_tags(2) + self.get_unique_tags(3)
        for tags in all_tags:
            if tags not in rarity_2_3_tags_list:
                rarity_2_3_tags_list.append(tags)
        return rarity_2_3_tags_list


    def close_db(self):
        self.con.close()


    def get_list_of_combinations(self, item_list, combination_size: int):
        def combination_util(item_list, k):
            if k == 0:
                return[[]]
            coms_list = []
            for i in range(len(item_list)):
                item = item_list[i]
                rem_item_list = item_list[i+1:]
                rem_coms_list = combination_util(rem_item_list, k-1)
                for j in rem_coms_list:
                    coms_list.append([item, *j])
            return coms_list

        combinations_list = combination_util(item_list, combination_size)
        return combinations_list


    def calculate(self):
        """
        Calculate tag combinations for recruitment
        """

        def get_recruitment_combinations(tags_list, max_combo=3):
            """
            1st-order indices represents number of selected tags\n
            2nd-order indices hold the tag combination
            """
            recruitment_tags = []
            for num_tags in range(1, max_combo+1):
                tag_combos = []
                for tag_str in tags_list:
                    op_tag_list = []
                    tag_idx = 0
                    while tag_idx < len(tag_str):
                        tag = tag_str[tag_idx:tag_idx+3]
                        op_tag_list.append(tag)
                        tag_idx += 3
                    more_tag_combos = self.get_list_of_combinations(op_tag_list, num_tags)
                    for combo in more_tag_combos:
                        if combo not in tag_combos:
                            tag_combos.append(combo)
                recruitment_tags.append(tag_combos)
            return recruitment_tags

        def write_to_text_file(list):
            for row in list:
                line = ""
                for combo in row:
                    line = line + ",".join(combo) + "|"
                file.write(line + "\n")

        file = open("recruitment_combinations.txt", "w")
        # get tag combinations for non-distinction operators
        r2_list = self.get_unique_tags(2)
        r3_list = self.get_unique_tags(3)
        r2_tag_combos = get_recruitment_combinations(r2_list)
        r3_tag_combos = get_recruitment_combinations(r3_list)
        non_dist_combos = []
        # merge r2 and r3 without duplicates
        for i in range(len(r2_tag_combos)):
            row = list(r2_tag_combos[i])
            row.extend(x for x in r3_tag_combos[i] if x not in row)
            non_dist_combos.append(row)
        # save as persistent data
        file.write("non_dist\n")
        write_to_text_file(non_dist_combos)
        self.non_dist_combos = non_dist_combos

        # get tag combinations for rarity 4 operators
        r4_list = self.get_unique_tags(4)
        r4_tag_combos = get_recruitment_combinations(r4_list)
        r4_tag_combos_dist = []
        # remove r2 and r3 combos from r4
        for i in range(len(r4_tag_combos)):
            row = []
            for x in r4_tag_combos[i]:
                if x not in non_dist_combos[i]:
                    row.append(x)
            r4_tag_combos_dist.append(row)
        # save as persistent data
        file.write("r4\n")
        write_to_text_file(r4_tag_combos_dist)
        self.r4_tag_combos_dist = r4_tag_combos_dist

        # get tag combinations for rarity 5 operators
        r5_list = self.get_unique_tags(5)
        r5_tag_combos = get_recruitment_combinations(r5_list)
        r5_tag_combos_dist = []
        # remove r2, r3, and r4 combos from r5
        for i in range(len(r5_tag_combos)):
            row = []
            for x in r5_tag_combos[i]:
                if x not in non_dist_combos[i]:
                    if x not in r4_tag_combos_dist[i]:
                        row.append(x)
            r5_tag_combos_dist.append(row)
        # save as persistent data
        file.write("r5\n")
        write_to_text_file(r5_tag_combos_dist)
        self.r5_tag_combos_dist = r5_tag_combos_dist

        # get tag combinations for rarity 6 operators
        r6_list = self.get_unique_tags(6)
        r6_tag_combos = get_recruitment_combinations(r6_list)
        # remove r2, r3, r4, and r5 combos from r6
        r6_tag_combos_dist = []
        for i in range(len(r6_tag_combos)):
            row = []
            for x in r6_tag_combos[i]:
                if x not in non_dist_combos[i]:
                    if x not in r4_tag_combos_dist[i]:
                        if x not in r5_tag_combos_dist[i]:
                            row.append(x)
            r6_tag_combos_dist.append(row)
        # remove combinations that do not contain TOP OPERATOR
        for i, row in enumerate(r6_tag_combos_dist):
            row_temp = [x for x in row if "TOP" in x]
            r6_tag_combos_dist[i] = row_temp
        # save as persistent data
        file.write("r6\n")
        write_to_text_file(r6_tag_combos_dist)
        file.close()
        self.r6_tag_combos_dist = r6_tag_combos_dist


    def test_for_overlap_in_tag_combos(self):
        # test combinations including non_dist_combos
        intersect = [ [] for _ in range(3)]
        intersect[0] = [ [] for _ in range(3)]
        intersect[1] = [ [] for _ in range(2)]
        intersect[2] = [ [] for _ in range(1)]
        for i, row in enumerate(self.non_dist_combos):
            # non_dist[i] and r4[i]
            intersect[0][0].append([x for x in row if x in self.r4_tag_combos_dist[i]])
            # non_dist[i] and r5[i]
            intersect[0][1].append([x for x in row if x in self.r5_tag_combos_dist[i]])
            # non_dist[i] and r6[i]
            intersect[0][2].append([x for x in row if x in self.r6_tag_combos_dist[i]])
        for i, row in enumerate(self.non_dist_combos):
            # r4[i] and r5[i]
            intersect[1][0].append([x for x in row if x in self.r5_tag_combos_dist[i]])
            # r4[i] and r6[i]
            intersect[1][1].append([x for x in row if x in self.r6_tag_combos_dist[i]])
        for i, row in enumerate(self.non_dist_combos):
            # r4[i] and r6[i]
            intersect[2][0].append([x for x in row if x in self.r6_tag_combos_dist[i]])
        overlap = False
        for i, list1 in enumerate(intersect):
            for j, list2 in enumerate(list1):
                overlapping_combos = []
                for k, combo in enumerate(list2):
                    if combo:
                        overlapping_combos.append(intersect[i][j][k])
                if overlapping_combos:
                    overlap = True
                    if i == 0:
                        print("Overlap found between non_dist and r" + str(j+4) + ":")
                        for row in overlapping_combos:
                            for combo in row:
                                print("\t", end="")
                                print(combo)
                    else:
                        print("Overlap found between r" + str(i+4) + " and r" + str(j+4) + ":")
                        for combo in overlapping_combos:
                            for combo in row:
                                print("\t", end="")
                                print(combo)
        if not overlap:
            print("No overlapping tag combinations found")


    def get_recruit_data_from_text_file(self):
        """
        Chooses based on highest distinction return
        """
        def read_util(max_combo=3):
            list = []
            for r in range(max_combo):
                line = file.readline()
                combo = []
                idx = 0
                while idx < len(line)-1:
                    tags = []
                    while line[idx] != "|":
                        if line[idx] == ",":
                            idx += 1
                        tags.append(line[idx:idx+3])
                        idx += 3
                    idx += 1
                    combo.append(tags)
                list.append(combo)
            return list

        file = open("recruitment_combinations.txt", "r")
        # read non-distinction tags
        non_dist_combos = []
        if file.readline() == "non_dist\n":
            non_dist_combos = read_util()
        # read r4 tags
        r4_tag_combos_dist = []
        if file.readline() == "r4\n":
            r4_tag_combos_dist = read_util()
        # read r5 tags
        r5_tag_combos_dist = []
        if file.readline() == "r5\n":
            r5_tag_combos_dist = read_util()
        # read r6 tags
        r6_tag_combos_dist = []
        if file.readline() == "r6\n":
            r6_tag_combos_dist = read_util()
        return non_dist_combos, r4_tag_combos_dist, r5_tag_combos_dist, r6_tag_combos_dist


    def find_best_tags(self, available_tags: list):
        """
        Chooses based on highest distinction return
        """
        def find_possible_combos(all_combos):
            # compares each combo in possible_combos with each combo in all_combos
            possible_combos = []
            possible_combos.append(self.get_list_of_combinations(available_tags, 1))
            possible_combos.append(self.get_list_of_combinations(available_tags, 2))
            possible_combos.append(self.get_list_of_combinations(available_tags, 3))
            available_combos = []
            # get combos in possible_combos
            for possible_combos_row in possible_combos:
                available_combos_row = []
                for combo in possible_combos_row:
                    # get combos in all_combos
                    for combos_list in all_combos:
                        if combo in combos_list:
                            available_combos_row.append(combo)
                available_combos.append(available_combos_row)
            return available_combos

        # order available_tags based on self.tag_legend
        available_tags = [x for x in self.tag_legend if x in available_tags]
        possible_non_dist_combos = find_possible_combos(self.non_dist_combos)
        possible_r4_combos = find_possible_combos(self.r4_tag_combos_dist)
        possible_r5_combos = find_possible_combos(self.r5_tag_combos_dist)
        possible_r6_combos = find_possible_combos(self.r6_tag_combos_dist)
        return possible_non_dist_combos, possible_r4_combos, possible_r5_combos, possible_r6_combos


    # [Il Siracusano] update
    # Recruitment updates typically happen during events with limited-time operators
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
    #       AOE - AoE
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


def test():
    def print_operators_table():
        operator_id = "5001"
        operator_table = db_tools.get_operator_data(get=["all"])
        for row in operator_table:
            print(row)

    def get_tables():
        db_tools.view_all_tables()

    def test_tag_calculator():
        available_combos = db_tools.find_best_tags(["MEL", "STR", "DEF", "SNI", "TOP"])
        for i in range(0, 4):
            if i == 0:
                print("non_distinction tags:")
            else:
                print(str(i + 3) + "-star tags:")
            for row in reversed(available_combos[i]):
                for combo in row:
                    print("\t", end="")
                    print(combo)

    db_tools = tools()
    # test code here
    print("--test--")
    print()
    print("--test--")
    db_tools.close_db()


if __name__ == "__main__":
    test()
