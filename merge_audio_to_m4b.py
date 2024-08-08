import os
import subprocess
import shutil

def process_audio_to_m4b(root_dir):
    # Create the 'finished' and 'delete' directories if they don't exist
    finished_dir = os.path.join(root_dir, 'finished')
    delete_dir = os.path.join(root_dir, 'delete')
    os.makedirs(finished_dir, exist_ok=True)
    os.makedirs(delete_dir, exist_ok=True)

    # Iterate through all subdirectories in the current folder
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)
        
        # Check if it's a directory
        if os.path.isdir(folder_path) and folder_name not in ['finished', 'delete']:
            # Get all MP3 and M4B files in the folder
            audio_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp3', '.m4b'))]
            audio_count = len(audio_files)
            
            if audio_count > 0:
                output_file = f"{folder_name}.m4b"
                output_subfolder = os.path.join(finished_dir, folder_name)
                os.makedirs(output_subfolder, exist_ok=True)
                output_path = os.path.join(f'/mnt/finished/{folder_name}', output_file)
                
                # Construct the base Docker command
                base_command = [
                    'docker', 'run', '-it', '--rm',
                    '-u', f'{os.getuid()}:{os.getgid()}',
                    '-v', f'{root_dir}:/mnt',
                    'sandreas/m4b-tool:latest'
                ]
                
                if audio_count > 1:
                    # Merge multiple files
                    command = base_command + [
                        'merge', '--jobs=4', f'/mnt/{folder_name}',
                        '--output-file', output_path
                    ]
                    if all(f.lower().endswith('.m4b') for f in audio_files):
                        command.insert(-2, '--no-conversion')
                elif audio_count == 1:
                    # Convert single MP3 to M4B or copy single M4B
                    input_file = os.path.join(f'/mnt/{folder_name}', audio_files[0])
                    if audio_files[0].lower().endswith('.mp3'):
                        command = base_command + [
                            'merge', input_file,
                            '--output-file', output_path
                        ]
                    else:  # Single M4B file
                        # Just copy the file to the output folder
                        shutil.copy2(os.path.join(folder_path, audio_files[0]), os.path.join(output_subfolder, output_file))
                        print(f"Copied {audio_files[0]} to {output_file}")
                        command = None  # No need to run m4b-tool
                
                # Execute the command if needed
                if command:
                    try:
                        subprocess.run(command, check=True)
                        print(f"Successfully processed {folder_name} to {output_file}")
                    except subprocess.CalledProcessError as e:
                        print(f"Error processing {folder_name}: {e}")
                        continue  # Skip to next folder if there's an error
                
                # Copy JPG files if they exist
                for file in os.listdir(folder_path):
                    if file.lower().endswith('.jpg'):
                        src_file = os.path.join(folder_path, file)
                        dst_file = os.path.join(output_subfolder, file)
                        shutil.copy2(src_file, dst_file)
                        print(f"Copied {file} to the finished folder")
                
                # Move the original folder to the delete folder
                delete_folder_path = os.path.join(delete_dir, folder_name)
                shutil.move(folder_path, delete_folder_path)
                print(f"Moved {folder_name} to the delete folder")

if __name__ == "__main__":
    current_dir = os.getcwd()
    process_audio_to_m4b(current_dir)