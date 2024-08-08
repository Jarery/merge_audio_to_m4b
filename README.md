# merge_audio_to_m4b
python script (made via Claude 3.5) to convert audio files to a single M4B file using M4B-tool
Created after auto-m4b from seanap stopped working for myself.

In a folder place media subfolders (only 1 level deep) with the merge_audio_to_m4b.py script.
Run python3 merge_audio_to_m4b.py

Script will create subfolders called "delete" & "finished" with merged single m4b files being copied to subfolders in "finished", copy over any jpg covers, and then move the original multi audio file folder to the delete folder.

Currently set to work with 4 cores, adjust as necassary with --jobs:4
Must have newest Docker of M4B-Tool installed as follows :
  - docker pull sandreas/m4b-tool:latest
  - alias m4b-tool='docker run -it --rm -u $(id -u):$(id -g) -v "$(pwd)":/mnt sandreas/m4b-tool:latest'
  - m4b-tool --version
  - python3 merge_audio_to_m4b.py
Once finsihed, use beets-audiobooks to tag and put M4B files to library

