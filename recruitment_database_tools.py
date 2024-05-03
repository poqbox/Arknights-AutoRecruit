import os
import sqlite3
# import sqlite3tools as sql


# SQLite documentation: https://www.sqlite.org/datatype3.html

# tag dictionaries
tagsQual_dict = {
    "ROB": "Robot",
    "STR": "Starter",
    "SEN": "Senior Operator",
    "TOP": "Top Operator"
}
tagsPos_dict = {
    "MEL": "Melee",
    "RNG": "Ranged"
}
tagsClass_dict = {
    "CAS": "Caster",
    "DEF": "Defender",
    "GUA": "Guard",
    "MED": "Medic",
    "SNI": "Sniper",
    "SPE": "Specialist",
    "SUP": "Supporter",
    "VAN": "Vanguard"
}
tagsSpec_dict = {
    "AOE": "AoE",
    "CDC": "Crowd-Control",
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

# complete code->tag dictionary
tag_dict = tagsQual_dict.copy()
tag_dict.update(tagsPos_dict)
tag_dict.update(tagsClass_dict)
tag_dict.update(tagsSpec_dict)

# lists of codes
tagsQual_keysList = list(tagsQual_dict.keys())
tagsPos_keysList = list(tagsPos_dict.keys())
tagsClass_keysList = list(tagsClass_dict.keys())
tagsSpec_keysList = list(tagsSpec_dict.keys())

# lists of tags
tagsQual_valuesList = list(tagsQual_dict.values())
tagsPos_valuesList = list(tagsPos_dict.values())
tagsClass_valuesList = list(tagsClass_dict.values())
tagsSpec_valuesList = list(tagsSpec_dict.values())

# complete list of tag codes
tag_legend = tagsQual_keysList[:]
tag_legend.extend(tagsPos_keysList)
tag_legend.extend(tagsClass_keysList)
tag_legend.extend(tagsSpec_keysList)


class Database:
    def __init__(self):
        self.con = sqlite3.connect("Recruit.db")
        self.cur = self.con.cursor()
        self.non_dist_combos, self.r4_tag_combos_dist, self.r5_tag_combos_dist, self.r6_tag_combos_dist = self.get_recruit_data_from_text_file()

    def open_db(self):
        self.con = sqlite3.connect("Recruit.db")
        self.cur = self.con.cursor()

    def close_db(self):
        self.con.close()

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
            tags_full.append(tag_dict.get(tag))
        return tags_full

    def get_operator_data(self, get: list, where=None, sort_order=None, limit=None, offset=None, get_full_tags=False, reduce_nested_lists=False):
        """
        get: "id"|"rarity|"name"|"tags"\n
        sort_order: List[List[str]] sorting parameters of the form [sort, order]\n
        sort: "id"|"rarity|"name"\n
        order: "asc"|"desc"\n
        """
        operator_list = []
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
            if tag not in tag_legend:
                print("One of the tags is not a valid tag")
                return
        operator_tags = "".join(tag_list)
        if self.cur.execute("select count(*) from Operators where rarity=?", [str(rarity)]).fetchone()[0] == 0:
            op_id = (rarity * 4) + 1
        else:
            op_id = self.cur.execute("select id from Operators where rarity=? order by id desc limit 1", [str(rarity)]).fetchone()[0] + 1
        self.cur.execute("insert into Operators values (?, ?, ?, ?)", (str(op_id), str(rarity), operator_name, operator_tags))
        self.con.commit()

    def update_operator(self, orig_id=None, orig_name=None, new_name=None, new_tags=[]):
        """
        Provide either orig_id or orig_name, then provide any number of new variables.\n
        If both orig_id or orig_name are provided, then orig_id will be used to identify the operator.\n
        new_tags is a list of tag codes. Refer to the tags legend for the code of each tag.
        """
        # return if identifiers are not provided
        if orig_id is None and orig_name is None:
            print("One of the following was not provided: orig_id, orig_name")
            print("The table will not be updated")
            return
        res = self.cur.execute("select id from Operators")
        ids_list = [row[0] for row in res]
        res = self.cur.execute("select name from Operators")
        names_list = [name[0] for name in res]
        # return if orig_id could not be located
        if orig_id is not None and orig_id not in ids_list:
            print("Could not locate ID", orig_id)
            print("The table will not be updated")
            return
        # return if orig_name could not be located
        if orig_name is not None and orig_name not in names_list:
            print('Could not locate operator name "' + orig_name + '"')
            print("The table will not be updated")
            return
        # return if orig_name is being used, but there are more than one operator with the same name
        if orig_id is None and orig_name is not None:
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
        if new_name is None and new_tags is None:
            print("At least one of the following was not provided: new_name, new_tags")
            print("The table will not be updated")
            return

        # update operator
        provided_entities = [False, False]
        entities = []
        if new_name is not None:
            provided_entities[0] = True
            entities.append(new_name)
        if new_tags:
            for tag in new_tags:
                if tag not in tag_legend:
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
        if orig_id is not None:
            entities.append(orig_id)
            self.cur.execute(query + " where id=?", entities)
            self.con.commit()
            return
        elif orig_name is not None:
            entities.append(orig_name)
            self.cur.execute(query + " where name=?", entities)
            self.con.commit()
            return
        print("Error: the table could not be updated")

    def delete_operator(self, operator_id):
        self.cur.execute("delete from Operators where id=?", (str(operator_id)))
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

    def get_list_of_combinations(self, tags_list, combination_size: int):
        def combination_util(item_list, k):
            if k == 0:
                return [[]]
            coms_list = []
            for i in range(len(item_list)):
                item = item_list[i]
                rem_item_list = item_list[i+1:]
                rem_coms_list = combination_util(rem_item_list, k-1)
                for j in rem_coms_list:
                    coms_list.append([item, *j])
            return coms_list

        combinations_list = combination_util(tags_list, combination_size)
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

        def write_to_text_file(tag_combos):
            for row in tag_combos:
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
            combos = list(r2_tag_combos[i])
            combos.extend(x for x in r3_tag_combos[i] if x not in combos)
            non_dist_combos.append(combos)
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
            combos = []
            for x in r4_tag_combos[i]:
                if x not in non_dist_combos[i]:
                    combos.append(x)
            r4_tag_combos_dist.append(combos)
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
            combos = []
            for x in r5_tag_combos[i]:
                if x not in non_dist_combos[i]:
                    if x not in r4_tag_combos_dist[i]:
                        combos.append(x)
            r5_tag_combos_dist.append(combos)
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
            combos = []
            for x in r6_tag_combos[i]:
                if x not in non_dist_combos[i]:
                    if x not in r4_tag_combos_dist[i]:
                        if x not in r5_tag_combos_dist[i]:
                            combos.append(x)
            r6_tag_combos_dist.append(combos)
        # remove combinations that do not contain TOP OPERATOR
        for i, combos in enumerate(r6_tag_combos_dist):
            row_temp = [x for x in combos if "TOP" in x]
            r6_tag_combos_dist[i] = row_temp
        # save as persistent data
        file.write("r6\n")
        write_to_text_file(r6_tag_combos_dist)
        file.close()
        self.r6_tag_combos_dist = r6_tag_combos_dist

    def test_for_overlap_in_tag_combos(self):
        # test combinations including non_dist_combos
        intersect = [[] for _ in range(3)]
        intersect[0] = [[] for _ in range(3)]
        intersect[1] = [[] for _ in range(2)]
        intersect[2] = [[] for _ in range(1)]
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
                    row = []
                    if i == 0:
                        print("Overlap found between non_dist and r" + str(j+4) + ":")
                        for row in overlapping_combos:
                            for combo in row:
                                print("\t", end="")
                                print(combo)
                    else:
                        print("Overlap found between r" + str(i+4) + " and r" + str(j+4) + ":")
                        for _ in overlapping_combos:
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

        file = open(os.path.join(os.path.dirname(__file__), "recruitment_combinations.txt"), "r")
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

    def find_available_combos(self, available_tags: list, sample_group: list):
        """
        Returns a list of possible tag combinations\n
        If invalid tags are given, they will be removed from the list before searching
        """
        # organize available_tags
        available_tags = [x for x in tag_legend if x in available_tags]
        possible_combos = []
        possible_combos.extend(self.get_list_of_combinations(available_tags, 1))
        possible_combos.extend(self.get_list_of_combinations(available_tags, 2))
        possible_combos.extend(self.get_list_of_combinations(available_tags, 3))
        available_combos = []
        # compare each combo in possible_combos with each combo in all_combos
        # get combos in possible_combos
        for combo in possible_combos:
            # get combos in all_combos
            if combo in sample_group:
                available_combos.append(combo)
        return available_combos

    def find_best_tags(self, available_tags: list, priority_tags: list = None):
        """
        If priority_tags is empty, chooses the least number of tags for the highest available rarity\n
        If invalid tags are given, they will be removed from the list before searching
        Returns a tuple of a string of tags and the recruitment rarity
        """
        # organize available_tags
        available_tags = [x for x in tag_legend if x in available_tags]

        # if priority_tags is None or empty, find in the order [6-star, 5-star, 4-star, None]
        if priority_tags is None or not priority_tags:
            # order available_tags based on self.tag_legend
            possible_r6_combos = self.find_available_combos(available_tags, [combo for sub_list in self.r6_tag_combos_dist for combo in sub_list])
            if possible_r6_combos:
                return possible_r6_combos[0], 6
            possible_r5_combos = self.find_available_combos(available_tags, [combo for sub_list in self.r5_tag_combos_dist for combo in sub_list])
            if possible_r5_combos:
                return possible_r5_combos[0], 5
            possible_r4_combos = self.find_available_combos(available_tags, [combo for sub_list in self.r4_tag_combos_dist for combo in sub_list])
            if possible_r4_combos:
                return possible_r4_combos[0], 4
            return None
        operator_names = []
        res = self.cur.execute("select name from Operators")
        for row in res:
            operator_names.append(row[0])
        for priority in priority_tags:
            possible_combos = []
            rarity = 0
            # if priority in operator_names:
            #     self.decode_tags(self.cur.execute("select tags from Operators where name=?", (priority)).fetchone()[0])
            if priority == "6-star" or priority == "rarity 6":
                possible_combos = self.find_available_combos(available_tags, [combo for sub_list in self.r6_tag_combos_dist for combo in sub_list])
                rarity = 6
            elif priority == "5-star" or priority == "rarity 5":
                possible_combos = self.find_available_combos(available_tags, [combo for sub_list in self.r5_tag_combos_dist for combo in sub_list])
                rarity = 5
            elif priority == "4-star" or priority == "rarity 4":
                possible_combos = self.find_available_combos(available_tags, [combo for sub_list in self.r4_tag_combos_dist for combo in sub_list])
                rarity = 4
            if possible_combos:
                return possible_combos[0], rarity
        return None

    # [Where Vernal Winds Will Never Blow] update
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
    #       CDC - Crowd-Control
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
        available_tags = ["MEL", "STR", "DBF", "SNI", "TOP"]
        possible_r6_combos = db_tools.find_available_combos(available_tags, [combo for sub_list in db_tools.r6_tag_combos_dist for combo in sub_list])
        possible_r5_combos = db_tools.find_available_combos(available_tags, [combo for sub_list in db_tools.r5_tag_combos_dist for combo in sub_list])
        possible_r4_combos = db_tools.find_available_combos(available_tags, [combo for sub_list in db_tools.r4_tag_combos_dist for combo in sub_list])
        possible_non_dist_combos = db_tools.find_available_combos(available_tags, [combo for sub_list in db_tools.non_dist_combos for combo in sub_list])
        possible_combos = [possible_r6_combos, possible_r5_combos, possible_r4_combos, possible_non_dist_combos]
        for i in range(0, 4):
            if i == 3:
                print("non_distinction tags:")
            else:
                print(str(6 - i) + "-star tags:")
            for combo in possible_combos[i]:
                print("\t", end="")
                print(combo)

    db_tools = Database()
    # test code here
    print("--test--")
    # --------------------------------
    # --------------------------------
    tags = db_tools.find_best_tags(["MEL", "STR", "DBF", "SNI", "TOP"], ["6-star", "5-star", "4-star"])
    print(tags)
    # --------------------------------
    # --------------------------------
    print("--test--")
    db_tools.close_db()


if __name__ == "__main__":
    test()
