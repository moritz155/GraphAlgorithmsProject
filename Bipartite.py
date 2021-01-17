import itertools


def find_other_color_combinations(graph):
    all_combinations = {}
    index = 0
    indexList = []  # gives me index of vertex that can be changed
    colorOptionsList = []  # shows me for all colors the given index it can have, looks like this: ["",""]=>[[],[]]
    for v in graph:
        build_color_options_string = ""
        if len(graph[v]) < 3 or get_amount_of_connected_colors(graph[v]):
            # print(f"{v} and {graph[v]}")
            indexList.append(index)
            if not check_for_element_in_list(graph[v], "B"):
                build_color_options_string += "B"
            if not check_for_element_in_list(graph[v], "Y"):
                build_color_options_string += "Y"
            if not check_for_element_in_list(graph[v], "G"):
                build_color_options_string += "G"
            if not check_for_element_in_list(graph[v], "R"):
                build_color_options_string += "R"
            colorOptionsList.append(build_color_options_string)
        index += 1
    color_codes_vertices = all_color_combinations(colorOptionsList)  # gives back a list of tuples[(),()]
    # tuple indexes are equal to indexes in indexList, so they point to vertex in the graph
    graph_combination = {}
    keys_list = list(graph)
    vertices_to_change = []
    key = 0
    for j in indexList:
        vertices_to_change.append(keys_list[j])
    # print("vertices: ")
    # print(vertices_to_change)
    # print("options: ")
    # print(color_codes_vertices)
    # print(len(color_codes_vertices))
    # print(color_codes_vertices)
    for tuple in color_codes_vertices:
        # print(tuple)
        for i in range(len(tuple)):
            # find vertex in graph at indexList[i] and change to tuple[i]
            tuple_as_list = []
            counter = 0
            for elem in tuple:
                tuple_as_list.append(elem + vertices_to_change[counter][1:])
                counter += 1
            # print(tuple_as_list)
            graph_combination = change_equal_elements(graph, vertices_to_change, tuple_as_list)
        all_combinations[key] = graph_combination
        key += 1
    if all_combinations == {0: {}}:  # in case there is only one coolor option
        all_combinations[0] = graph
    for combination in all_combinations:
        if checkGraph(all_combinations[combination]):
            best_combination_for_least_faces(all_combinations[combination])
    find_best_color_combination()


def get_amount_of_connected_colors(given_list):
    need_to_be_2 = 0
    if not check_for_element_in_list(given_list, "B"):
        need_to_be_2 += 1
    if not check_for_element_in_list(given_list, "G"):
        need_to_be_2 += 1
    if not check_for_element_in_list(given_list, "Y"):
        need_to_be_2 += 1
    if not check_for_element_in_list(given_list, "R"):
        need_to_be_2 += 1
    if need_to_be_2 >= 2:
        # print(given_list)
        return True
    return False


def checkGraph(graph):  # is it necessary?
    for vertex in graph:
        for colored in graph[vertex]:  # get the color
            if vertex[0] == colored[0]:
                # print(f"not: {vertex} to {graph[vertex]}")
                return False
    return True


def init_outsourced_vertices():
    for i in outsourced_vertices:
        outsourced_vertices[i] = 0


def best_combination_for_least_faces(graph):
    # print(graph)
    # dict: key=vertex, value=[adjacent colors]
    init_outsourced_vertices()
    rb, rg, ry, gy, gb, yb = 0, 0, 0, 0, 0, 0
    for key in graph:
        possible_outsourcing = False
        if len(set(graph[key])) == 1:  # true if vertex has degree 1 or vertex is connected with only one color
            possible_outsourcing = True
        for conn_color in graph[key]:
            if key[0] == "R":
                if conn_color[0] == "G":
                    rg += calculate(possible_outsourcing, "rg")
                elif conn_color[0] == "Y":
                    ry += calculate(possible_outsourcing, "ry")
                elif conn_color[0] == "B":
                    rb += calculate(possible_outsourcing, "rb")
            elif key[0] == "Y":
                if conn_color[0] == "G":
                    gy += calculate(possible_outsourcing, "gy")
                elif conn_color[0] == "R":
                    ry += calculate(possible_outsourcing, "ry")
                elif conn_color[0] == "B":
                    yb += calculate(possible_outsourcing, "yb")
            elif key[0] == "G":
                if conn_color[0] == "R":
                    rg += calculate(possible_outsourcing, "rg")
                elif conn_color[0] == "Y":
                    gy += calculate(possible_outsourcing, "gy")
                elif conn_color[0] == "B":
                    gb += calculate(possible_outsourcing, "gb")
            elif key[0] == "B":
                if conn_color[0] == "G":
                    gb += calculate(possible_outsourcing, "gb")
                elif conn_color[0] == "Y":
                    yb += calculate(possible_outsourcing, "yb")
                elif conn_color[0] == "R":
                    rb += calculate(possible_outsourcing, "rb")
    return best_combination(rb, rg, ry, gy, gb, yb, graph)


def calculate(boolean, key):
    if boolean:
        outsourced_vertices[key] += 1
    return 1


def best_combination(rb, rg, ry, gy, gb, yb, graph):
    rb_gy_ignored_edges = (rb + gy) / 2
    rg_yb_ignored_edges = (rg + yb) / 2
    ry_gb_ignored_edges = (ry + gb) / 2
    rb_gy = int(2 + (get_number_edges(graph) - rb_gy_ignored_edges) - (len(graph) - (
            outsourced_vertices['rb'] + outsourced_vertices['gy'])))
    rg_yb = int(2 + (get_number_edges(graph) - rg_yb_ignored_edges) - (len(graph) - (
            outsourced_vertices['rg'] + outsourced_vertices['yb'])))
    ry_gb = int(2 + (get_number_edges(graph) - ry_gb_ignored_edges) - (len(graph) - (
            outsourced_vertices['ry'] + outsourced_vertices['gb'])))
    least_faces = min([ry_gb, rg_yb, rb_gy])
    # example for most faces:  max([ry_gb, rg_yb, rb_gy])
    result = ""
    if least_faces == ry_gb:
        result = f"combination: ry_gb ,edges removed: {ry_gb_ignored_edges} vertices outsourced: {outsourced_vertices['ry'] + outsourced_vertices['gb']} , number of faces: {least_faces}"
    if least_faces == rg_yb:
        result = f"combination: rg_yb ,edges removed: {rg_yb_ignored_edges} vertices outsourced: {outsourced_vertices['rg'] + outsourced_vertices['yb']}, number of faces: {least_faces}"
    if least_faces == rb_gy:
        result = f"combination: rb_gy ,edges removed: {rb_gy_ignored_edges} vertices outsourced: {outsourced_vertices['rb'] + outsourced_vertices['gy']}, number of faces: {least_faces}"
    global key_for_result_dict
    gather_all_results[key_for_result_dict] = [least_faces, result, graph]
    key_for_result_dict += 1
    return 0


def get_number_edges(graph):
    edges = 0
    for key in graph:
        edges += len(graph[key])
    return edges / 2


def change_equal_elements(dict_to_change, change_us, to_these):
    new_dict = {}
    for vertex in dict_to_change:
        value_list = []
        for adjacent in dict_to_change[vertex]:
            added = False
            for i in range(len(change_us)):
                if adjacent == change_us[i]:
                    value_list.append(to_these[i])
                    added = True
            if not added:
                value_list.append(adjacent)
        added = False
        for i in range(len(change_us)):
            if vertex == change_us[i]:
                new_dict[to_these[i]] = value_list
                added = True
        if not added:
            new_dict[vertex] = value_list
    return new_dict


def all_color_combinations(many_lists):
    color_codes_vertices = []
    for element in itertools.product(*many_lists):
        color_codes_vertices.append(element)
    return color_codes_vertices


def check_for_element_in_list(given_list, search_for):
    for element in given_list:
        if search_for in element[0]:  # Color code is at index 0
            return True
    return False


def find_best_color_combination():
    amount_faces_list = []
    for result in gather_all_results:
        amount_faces_list.append(gather_all_results[result][0])
    least_faces_of_all = min(amount_faces_list)
    counter = 0
    # print(len(gather_all_results))
    for result in gather_all_results:
        if gather_all_results[result][0] == least_faces_of_all:
            counter += 1
            print(gather_all_results[result][1])
            print(gather_all_results[result][2])
    # print(counter)


samplegraph = {"R0": ["B", "Y", "G", "B"],  # 1
               "R1": ["Y", "G", "G", "B"],  # 1
               "G2": ["Y", "B", "R", "B"],  # 2
               "Y3": ["R", "R", "G", "B"],  # 2
               "G4": ["B", "R", "B"],  # 2
               "B5": ["R", "Y", "G", "G"],  # 2
               "B6": ["G", "G", "R", "Y", "R", "G"],  # 3
               "G7": ["B", "R"],  # 1
               "Y8": ["B"]}  # 0

outsourced_vertices = {"rg": 0,
                       "rb": 0,
                       "ry": 0,
                       "gb": 0,
                       "yb": 0,
                       "gy": 0}
gather_all_results = {}
key_for_result_dict = 0
