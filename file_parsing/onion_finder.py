import re # Regular expression library
import warc # warc3-wet. To read common crawl files.
from glob import glob # To find all files in specified directory
from multiprocessing import Pool, cpu_count # To utilize multiple processors to speed up the script
from subprocess import Popen, PIPE # Make the script universal
from sys import platform # Determine system
from os.path import splitext # Used in tracking

# Regex for onion pages and domains. Must be able to find with and without www, http://, and https://
onion_regex = r'(?:https?\:\/\/)?[a-zA-Z2-7]{16}\.onion?(?:\/([^/]*))?'

# Determine OS and number of processes to use
def os_processes():
    MAX_PROCESSES = 0
    if platform == "linux" or platform == "linux2":
        # linux
        bashCommand = "nproc"
        process = Popen(bashCommand.split(), stdout=PIPE)
        output, error = process.communicate()
        MAX_PROCESSES = int(output.decode().strip())
    elif platform == "darwin":
        # OS X
        bashCommand = "nproc"
        process = Popen(bashCommand.split(), stdout=PIPE)
        output, error = process.communicate()
        MAX_PROCESSES = int(output.decode().strip())
    elif platform == "win32":
        # Windows
        MAX_PROCESSES = cpu_count()
    return MAX_PROCESSES

# Find onions in data
def find_onions(filename):
    file_onions = {}
    onion = re.compile(onion_regex, re.IGNORECASE)
    with warc.open(filename) as f:
        with open("{}.txt".format(filename.strip(".warc.wet.gz")), 'a+') as output:
            for record in f:
                url = str(record.header.get('WARC-Target-URI', None))
                data = str(record.payload.read())
                onion_match = onion.search(url)
                payload_match = onion.search(data)
                if onion_match:
                    match = onion_match.group(0)
                    file_onions[url] = []
                    file_onions[url].append(match)
                if payload_match:
                    match = payload_match.group(0)
                    file_onions[url] = []
                    file_onions[url].append(match)
            for k,v in  file_onions.items():
                output.write("{} {}\n".format(k,','.join(v)))

if __name__ == "__main__":
    files = glob("*.warc.wet.gz")
    completed = glob("*.txt")
    completed = [splitext(c)[0] for c in completed]
    if completed:
        files = [f for f in files if f.strip(".warc.wet.gz") not in completed]
    processors = os_processes()
    print("Searching for onions.........")
    pool = Pool(processors)
    pool.map(find_onions, files)
    pool.close()