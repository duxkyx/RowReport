# Check if input is a 2D list
def is_2d_list(lst):
    return (
        isinstance(lst, list) and
        all(isinstance(i, list) for i in lst) and
        all(not isinstance(j, list) for i in lst for j in i)
    )