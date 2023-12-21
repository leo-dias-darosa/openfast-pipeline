import os.path


def remove_extension(file):
    return file[0:len(file) - 4]


def get_file_name(file_full_path: str):
    return file_full_path.split("/")[-1]


def delete_files(file):
    if os.path.exists(file):
        os.remove(file)


def define_simulation_file_name(simulation_time_stamp, file_path, extension):
    """

    :return: The unique ID for the simulation
    """
    model_file = os.path.basename(file_path)
    model_file_no_extension = remove_extension(model_file)
    return f"{model_file_no_extension}-{simulation_time_stamp}.{extension}"
