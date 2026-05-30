# Apply filter (skip if filter doesn't match)
if actions["filter"]:
    expected_ext = ".{}".format(actions["filter"])
    if not filename.lower().endswith(expected_ext):
        return filename