import tarfile
import sys
import requests
import wget
import os

DDragonVersionsURL = "https://ddragon.leagueoflegends.com/api/versions.json"
DDragonDataURL = "https://ddragon.leagueoflegends.com/cdn/dragontail-"


def main(argv):
    try:
        version = argv[0]
    except IndexError:
        print("You must specify a patch to download.")
        return

    if version == "latest":
        ddVersions_request = requests.get(DDragonVersionsURL)

        if ddVersions_request.status_code != 200:
            print("Error fetching DDragon version. Check URL.")
            return
        
        version = ddVersions_request.json()[0]
    
    cur_dir = os.path.dirname(os.path.realpath(__file__)) 
    download_path = cur_dir + "/temp"
    version_path = cur_dir + "/" + version.replace(".", "_")
    file_path = download_path + version +".tgz"
    
    # Check if file exists. If not, downloads it:
    if not os.path.exists(file_path):
        if not os.path.isfile(file_path):
            if not os.path.exists(download_path):
                os.mkdir(download_path)
            print("Downloading DDragon for patch " + version + " ...")
            wget.download(DDragonDataURL+version+".tgz", file_path)

    # Extracts the content of the tar archive
    print("\n Extracting data...")
    with tarfile.open(file_path) as f:
        if not os.path.exists(version):
            os.mkdir(version_path)
        f.extractall(version_path)

    # Cleanup
    os.remove(file_path)
    if not os.listdir(download_path):
        os.rmdir(download_path)
    print("Done.")

if __name__ == "__main__":
    main(sys.argv[1:])