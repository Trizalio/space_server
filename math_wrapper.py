import numpy

#
# a = numpy.array([[1,2,3], [-3,-2,-1], [0, 0, 0]])
# b = numpy.array([0, 0, 0])
# x = numpy.linalg.solve(a, b)
# print x
#
# exit(0)

dimensions = 3


#
# transition_matrix = numpy.matrix([[2.,-1.], [2.,1.]])
# input_vector = numpy.array([0., -3.])
# result = transition_matrix.dot(input_vector)
# print result
# input_vector = numpy.array([1./2., -1])
# result = transition_matrix.dot(input_vector)
# print result
#
# inverted_transition_matrix = numpy.linalg.inv(transition_matrix)
# input_vector = numpy.array([3., -3.])
# result = inverted_transition_matrix.dot(input_vector)
# print result
# input_vector = numpy.array([2., 0.])
# result = inverted_transition_matrix.dot(input_vector)
# print result


def find_result(v1, v2, t):
    transition_matrix = numpy.matrix([[v1[0], v2[0]], [v1[1], v2[1]]])
    inverted_transition_matrix = numpy.linalg.inv(transition_matrix)
    result = inverted_transition_matrix.dot(numpy.array([t[0], t[1]]))
    return result


def calculate_fractions(v1, v2, v3, t):
    print 'calc', v1, v2, v3, t
    transition_matrix = numpy.matrix([[v1[0], v2[0], v3[0]], [v1[1], v2[1], v3[1]], [v1[2], v2[2], v3[2]]])
    inverted_transition_matrix = numpy.linalg.inv(transition_matrix)
    result = inverted_transition_matrix.dot(numpy.array([t[0], t[1], t[2]]))
    return result


# print find_result((1.,0.),(1.,1.), (1., 0.5))

# >>> a = np.array([[ 5, 1 ,3],
#                   [ 1, 1 ,1],
#                   [ 1, 2 ,1]])
# >>> b = np.array([1, 2, 3])
# >>> print a.dot(b)
# array([16, 6, 8])

# control_map = {(11.562264865483717, 11.562264865483717, -33.03504247281061): 1, (61.562264865483726, 61.562264865483726, 45.03504247281061): 26, (73.12452973096744, 73.12452973096744, 12.0): 27, (23.12452973096744, 23.12452973096744, -12.0): 13, (73.12452973096744, 73.12452973096744, -12.0): 15, (-9.797174393178826e-16, -9.797174393178826e-16, -12.0): 4, (11.562264865483725, 11.562264865483725, 33.03504247281061): 8, (-1.959434878635765e-15, -1.959434878635765e-15, 0.0): 20, (61.562264865483726, 61.562264865483726, 33.03504247281061): 30, (73.12452973096744, 73.12452973096744, 0.0): 31, (61.562264865483726, 61.562264865483726, 21.03504247281061): 14, (61.56226486548372, 61.56226486548372, -45.03504247281061): 7, (11.562264865483721, 11.562264865483721, 33.03504247281061): 28, (23.124529730967442, 23.124529730967442, 0.0): 9, (61.56226486548372, 61.56226486548372, -33.03504247281061): 23, (11.562264865483714, 11.562264865483714, -33.03504247281061): 21, (11.562264865483716, 11.562264865483716, -45.03504247281061): 5, (50.0, 50.0, 12.0): 18, (-9.797174393178826e-16, -9.797174393178826e-16, 12.0): 16, (50.0, 50.0, -12.0): 6, (23.124529730967442, 23.124529730967442, 12.0): 25, (11.562264865483723, 11.562264865483723, 45.03504247281061): 24, (50.0, 50.0, 0.0): 22, (0, 0, 0): 0, (23.12452973096744, 23.12452973096744, 0.0): 29, (11.562264865483716, 11.562264865483716, -21.03504247281061): 17, (61.56226486548372, 61.56226486548372, -21.03504247281061): 19, (11.562264865483723, 11.562264865483723, 21.03504247281061): 12}


control_map = {(10., 20, 30): 1,
               (10., 0, 30): 2,
               (10., 20, 0): 3,
               (10., 0, 0): 4,
               (0., 20, 30): 5,
               (0., 0, 30): 6,
               (0., 20, 0): 7,
               (0., 0, 0): 8,
               (0., -10, 10): 8,
               }


# control_map = {(5., 10, 0): 1,
#                (5., 0, 0): 2,
#                (5., -10, 0): 3,
#                }

def pick_first_point(control_map, task):
    result = None
    result_mode = None
    result_range = 0
    for key in control_map:
        delta_range = vector_quadric_range(vector_minus(key, task))
        if not result or result_range > delta_range:
            result = key
            result_mode = control_map[key]
            result_range = delta_range
            print 'nearest updated', result, result_range
    return result, result_mode


def check_dot(plane, dot, hard=False):
    result = 0
    for i in range(0, dimensions):
        delta = plane['root'][i] - dot[i]
        result += delta * plane['normal'][i]
        print 'p', dot, result
    print 'plane', dot, result, result <= 0., result < 0., result == 0., result > 0., result >= 0.
    if hard:
        return result > 0.
    return result >= 0.


def create_plane_from_two_dots(root, normal):
    return {'root': (root[0] - normal[0], root[1] - normal[1], root[2] - normal[2]),
            'normal': (root[0] - normal[0], root[1] - normal[1], root[2] - normal[2])}


def create_plane_from_root_and_normal(root, normal):
    print 'create plane', root, normal
    return {'root': root,
            'normal': normal}


def create_line_from_root_and_normal(root, normal):
    return {'root': root,
            'normal': normal}


def vector_minus(first, second):
    arr = []
    for i in range(0, dimensions):
        arr += [first[i] - second[i]]
    return tuple(arr)


def vector_quadric_range(vector):
    quadric_range = 0
    for i in range(0, dimensions):
        quadric_range += vector[i] ** 2
    return quadric_range


def pick_second_point(control_map, planes, task, first_point):
    result = None
    result_mode = None
    result_range = 0
    for key in control_map:
        # print key
        if key == first_point:
            continue
        for plane in planes:
            if not check_dot(plane, key):
                print 'skipped by plane'
                continue
        delta_range = vector_quadric_range(vector_minus(key, task))
        # print key, delta_range
        if not result or result_range > delta_range:
            result = key
            result_mode = control_map[key]
            result_range = delta_range
            print 'nearest updated', result, result_range
    return result, result_mode


def find_intersection(plane, line):
    pr = plane['root']
    pn = plane['normal']
    lr = line['root']
    ln = line['normal']
    numerator = 0
    denominator = 0
    for i in range(0, dimensions):
        numerator += pn[i] * (pr[i] - lr[i])
        denominator += pn[i] * ln[i]
    t = numerator / float(denominator)
    print 't', t
    arr = []
    for i in range(0, dimensions):
        arr += [t * ln[i] + lr[i]]
    return tuple(arr)


def create_plane_from_two_dots_and_normal(line_point_1, line_point_2, normal_point):
    pre_plane = create_plane_from_root_and_normal(normal_point, vector_minus(line_point_1, line_point_2))
    line = create_line_from_root_and_normal(line_point_1, vector_minus(line_point_1, line_point_2))
    target_point = find_intersection(pre_plane, line)
    print 'target_point', target_point

    return create_plane_from_root_and_normal(target_point, vector_minus(target_point, normal_point))
    # return create_plane_from_two_dots(target_point, normal_point)


#
# def pick_third_point(control_map, first_point, second_point, task):
#     result = None
#     result_range = 0
#     plane = create_plane_from_two_dots_and_normal(first_point, second_point, task)
#     for key in control_map:
#         if not check_dot(plane, key, hard=True):
#             print 'skipped by plane'
#             continue
#         delta_range = vector_quadric_range(vector_minus(key, task))
#         if not result or result_range > delta_range:
#             result = key
#             result_range = delta_range
#             print 'nearest updated', result, result_range
#     return result


def create_plane_from_tree_dots(d1, d2, d3):
    print 'create_plane_from_tree_dots', d1, d2, d3
    x1, y1, z1 = d1
    x2, y2, z2 = d2
    x3, y3, z3 = d3
    a = y1 * (z2 - z3) + y2 * (z3 - z1) + y3 * (z1 - z2)
    b = z1 * (x2 - x3) + z2 * (x3 - x1) + z3 * (x1 - x2)
    c = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
    d = x1 * (y2 * z3 - y3 * z2) + x2 * (y3 * z1 - y1 * z3) + x3 * (y1 * z2 - y2 * z1)

    root = (d * a, d * b, d * c)
    normal = (-a, -b, -c)
    print 'create plane', root, normal
    return {'root': root,
            'normal': normal}

    # print a, b, c, d
    # exit(0)
    # print 'target_point', target_point

    # return create_plane_from_root_and_normal(target_point, vector_minus(target_point, normal_point))
    # return create_plane_from_two_dots(target_point, normal_point)


#
# def pick_forth_point(control_map, first_point, second_point, third_point, task):
#     result = None
#     result_range = 0
#     plane1 = create_plane_from_root_and_normal(first_point, vector_minus(first_point, task))
#     plane2 = create_plane_from_two_dots_and_normal(first_point, second_point, task)
#     plane3 = create_plane_from_tree_dots(first_point, second_point, third_point)
#     for key in control_map:
#         if not check_dot(plane1, key, hard=True):
#             print 'skipped by plane1'
#             continue
#         if not check_dot(plane2, key, hard=True):
#             print 'skipped by plane2'
#             continue
#         if not check_dot(plane3, key, hard=True):
#             print 'skipped by plane3'
#             continue
#         delta_range = vector_quadric_range(vector_minus(key, task))
#         if not result or result_range > delta_range:
#             result = key
#             result_range = delta_range
#             print 'nearest updated', result, result_range
#     return result

def pick_next_point(control_map, planes, task):
    result = None
    result_mode = None
    result_range = 0
    for key in control_map:
        skip = False
        for plane in planes:
            if not check_dot(plane, key, hard=True):
                print 'skipped by plane'
                skip = True
        if skip:
            continue
        delta_range = vector_quadric_range(vector_minus(key, task))
        print key, delta_range
        if not result or result_range > delta_range:
            result = key
            result_mode = control_map[key]
            result_range = delta_range
            print 'nearest updated', result, result_range
    return result, result_mode


task = (5, 5, 5)
def get_best_mode(control_map, task):
    first_point, first_mode = pick_first_point(control_map, task)
    print first_point
    print "-----"
    planes = [create_plane_from_root_and_normal(first_point, vector_minus(first_point, task))]

    second_point, second_mode = pick_second_point(control_map, planes, task, first_point)
    if not second_point:
        return {'base': first_mode,'shifts': {}}
    print second_point
    print "-----"
    planes += [create_plane_from_two_dots_and_normal(first_point, second_point, task)]

    third_point, third_mode = pick_next_point(control_map, planes, task)
    if not third_point:
        return {'base': first_mode,'shifts': {}}
    print third_point
    print "-----"
    planes += [create_plane_from_tree_dots(first_point, second_point, third_point)]

    forth_point, forth_mode = pick_next_point(control_map, planes, task)
    if not forth_point:
        return {'base': first_mode,'shifts': {}}
    print forth_point

    fractions = calculate_fractions(vector_minus(first_point, second_point), vector_minus(first_point, third_point),
                                    vector_minus(first_point, forth_point), task)

    print fractions
    return {'base':first_mode, 'shifts':{second_mode:fractions[0], third_mode:fractions[1], forth_mode:fractions[2]}}


