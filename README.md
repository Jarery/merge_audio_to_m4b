# merge_audio_to_m4b
python script to convert audio files to a single M4B file using M4B-tool
Created after auot-m4b from seanap stopped working for me.
Follows similar structure, in a merge folder place folders with your multi mp3 or mp4 files.
Run python3 merge_audio_to_m4b.py
will create subfolders under finished with merged single m4b file, copy over any jpg cover, and then move the original multi audio file foder to a delete folder.
Currently set to work with 4 cores
Must have newest Docker of M4B-Tool installed as follows :
  - docker pull sandreas/m4b-tool:latest
  - alias m4b-tool='docker run -it --rm -u $(id -u):$(id -g) -v "$(pwd)":/mnt sandreas/m4b-tool:latest'
  - m4b-tool --version
  - python3 merge_audio_to_m4b.py
Once finsihed, use beets-audiobooks to tag and put M4B files to library

