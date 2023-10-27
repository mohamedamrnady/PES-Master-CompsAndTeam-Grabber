import shutil
from datetime import date


shutil.make_archive(
    "eFootball CSVs for PES21 " + str(date.today()),
    "zip",
    "Output",
)
