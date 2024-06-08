import subprocess

def update():
    """
    Update Micro Agent to the latest version.
    """
    print('')
    command = 'npm update -g @builder.io/micro-agent'
    print(f'Running: {command}')
    print('')
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        # No need to handle, will go to stderr
        pass
    print('')

if __name__ == "__main__":
    update()
