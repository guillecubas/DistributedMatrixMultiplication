def remote_multiply_partition(context):
    """
    context = {
        "matrix_a": [...],
        "matrix_b": [...],
        "start_row": 0,
        "end_row": 127
    }
    """
    a = context["matrix_a"]
    b = context["matrix_b"]
    start = context["start_row"]
    end = context["end_row"]

    # Transponer matriz B para acceso por columnas
    b_t = list(zip(*b))

    result = []
    for i in range(start, end):
        row_result = [sum(a[i][k] * b_t[j][k] for k in range(len(b_t[j]))) for j in range(len(b_t))]
        result.append(row_result)

    return result
