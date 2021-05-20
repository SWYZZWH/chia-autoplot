import os
import subprocess
import argparse
import yaml
import logging

neccessary_configs = ["tmp_dir", "final_dir", "k_size", "threads", "buckets", "memory", "queue_size", "queue_num"]
configs_name_map ={"k_size": "k", "threads":"r", "buckets": "u", "memory":"b", "tmp_dir":"t", "final_dir":"d", "queue_size": "n"}
base_command = "chia plots create"


def clean_up_tmp_dir(dir):
    for f in os.listdir(dir):
        if f.endswith(".tmp"):
            os.remove(f)

def auto_plot(config_file: str):
    try:
        with open(config_file, "r") as f:
            y = yaml.load(f)
    except:
        logging.error("No such config file or config file format is invalid!")

    if check_yaml(y) != 0:
        return -1

    tmp_dir = y.get("tmp_dir")


    for i in range(y.get("queue_num")):
        tmp_dir_i = os.path.join(tmp_dir, str(i))
        clean_up_tmp_dir(tmp_dir_i)
        if not os.path.exists(tmp_dir_i):
            os.mkdir(tmp_dir_i)
        y["tmp_dir"] = tmp_dir_i
        cmd_str = get_command(y)
        subprocess.Popen(cmd_str, creationflags=8, close_fds=True) # DETACHED_PROCESS = 8


def check_yaml(y) -> int:
    if y is None:
        logging.error("Invalid config file!")
        return -1

    for config in neccessary_configs:
        if y.get(config) is None:
            logging.error("{} should be provided!".format(config))
            return -1

    for config in ["k_size", "threads", "buckets", "memory"]:
        try:
            val = int(y.get(config))
        except:
            logging.error("value of {} must be valid!".format(config))
            return -1

        if val <= 0 :
            logging.error("value of {} must be valid!".format(config))
            return -1

    return 0


def get_command(y) -> str:

    cmd = base_command
    print(y)
    for k, v in y.items():
        if k in configs_name_map and v != "None":
            cmd += " -{} {} ".format(configs_name_map[k], v)

    return cmd


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest="config_file", help='config yaml file loaction')
    args = parser.parse_args()

    if args.config_file is None:
        logging.error("No config file is provided!")

    auto_plot(args.config_file)
