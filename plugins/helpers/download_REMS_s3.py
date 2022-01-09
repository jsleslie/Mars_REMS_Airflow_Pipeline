import logging
import os
import sys
import bs4
import requests
import multiprocessing as mp
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

# -------------------------------------------------------------------------------
# INPUTS

# output directory
outdir = "tmp"

# rename join for creating urls/paths with single backslashes
join = lambda *args: "/".join(args)

# base directory of data archive
baseurl = "https://atmos.nmsu.edu/PDS/data/mslrem_1001/"

# top data directory url
dataurl = join(baseurl, "DATA")

# columns to write to file
env_cols = [
    "TIMESTAMP",
    "LMST",
    "LTST",
    "AMBIENT_TEMP",
    "PRESSURE",
    "HORIZONTAL_WIND_SPEED",
    "VERTICAL_WIND_SPEED",
    "VOLUME_MIXING_RATIO",
    "LOCAL_RELATIVE_HUMIDITY",
]

adr_cols = [
    "TIMESTAMP",
    "LMST",
    "LTST",
    "SOLAR_LONGITUDE_ANGLE",
    "SOLAR_ZENITHAL_ANGLE",
    "ROVER_POSITION_X",
    "ROVER_POSITION_Y",
    "ROVER_POSITION_Z",
    "ROVER_VELOCITY",
    "ROVER_PITCH",
    "ROVER_YAW",
    "ROVER_ROLL",
]

# -------------------------------------------------------------------------------
# FUNCTIONS

# pull file from url and convert it to a string
get_file = lambda url: requests.get(url).content.decode("utf-8")

# get linked files in a single web page, from its url string
def get_links(url):
    # get html text
    html = get_file(url)
    # parse it with beautiful soup
    soup = bs4.BeautifulSoup(html, "html.parser")
    # get path elements for all the links
    links = [link.get("href") for link in soup.find_all("a")]
    return links


def download(url, record_type, sol, colnums, targ_cols, outdir, folder_name):
    # extract data
    table = get_file(url)
    # remove unwanted values
    table = table.replace("UNK", "").replace("NULL", "")
    # write data to new file
    local_file_path = "%s/sol_%06d_%s.csv" % (outdir, sol, record_type)
    with open(local_file_path, "w") as ofile:
        # column headers
        ofile.write("SOL," + ",".join(targ_cols) + "\n")
        # csv body
        for line in table.strip().split("\n"):
            # split the table row on its commas
            s = line.strip().split(",")
            # skip if row is malformed
            if len(s) < len(colnums):
                continue
            # select only the desired column elements
            s = [s[i].strip() for i in colnums]
            # write the elements to file, along with the sol
            ofile.write("%d," % sol)
            ofile.write(",".join(s) + "\n")
    print("sol %s written" % sol)

    bucket_name = "jsleslie-data-engineering-capstone-1.0"
    folder_name = folder_name
    s3_key = f"{folder_name}/{local_file_path.split('/')[-1]}"
    logging.info(
        f"local_file_path: {local_file_path}, bucket_name: {bucket_name}, key: {s3_key}"
    )

    logging.info("Uploading CSV to S3 with S3HOOK")
    s3_hook = S3Hook(aws_conn_id="s3_connection")
    try:
        s3_hook.load_file(
            local_file_path,
            bucket_name=bucket_name,
            key=s3_key,
            acl_policy="bucket-owner-full-control",
        )
    except Exception as e:
        logging.info(e)
        pass
    logging.info("Done uploading CSV to S3 with S3HOOK")


def run_extract(targ_cols, record_type, labelname, folder_name):
    # make sure the output directory is there
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    # label file url
    labelurl = join(baseurl, "LABEL", labelname)

    # read column headers from label file
    name2num = {}
    lines = get_file(labelurl).split("\n")
    for i in range(len(lines)):
        line = lines[i]
        if "COLUMN_NUMBER" in lines[i]:
            # get the column number
            line = lines[i]
            colnum = int(line[line.index("=") + 1 :].strip()) - 1
            # get the column name/description from the following line
            line = lines[i + 1]
            colname = line[line.index("=") + 1 :].strip().replace('"', "")
            # save the column num and name
            name2num[colname] = colnum

    # get desired column indices
    colnums = [name2num[i] for i in targ_cols]
    # loop over all subdirectories in the data directory
    for count, dn1 in enumerate(get_links(dataurl)):
        # loop over all subdirectories in dir1
        if "SOL" in dn1:
            for dn2 in get_links(join(dataurl, dn1)):
                # loop over links in directory for single sol
                if "SOL" in dn2:
                    sol = int(dn2.replace("SOL", "").replace("/", ""))
                    for fn in get_links(join(dataurl, dn1, dn2)):
                        if (record_type in fn) and (".TAB" in fn):
                            url = join(dataurl, dn1, dn2, fn)
                            download(
                                url,
                                record_type,
                                sol,
                                colnums,
                                targ_cols,
                                outdir,
                                folder_name,
                            )


def main():
    run_extract(adr_cols, "ADR", "ADR_GEOM6.FMT", "REMS_ADR")
    run_extract(env_cols, "RMD", "MODRDR6.FMT", "REMS_ENV")


# -------------------------------------------------------------------------------
# MAIN
if __name__ == "__main__":
    main()
