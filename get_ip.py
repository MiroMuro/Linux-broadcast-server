import subprocess

def get_wsl_ip():
    # Call the shell script and capture the output
    result = subprocess.run(['./get_wsl_ip.sh'], stdout=subprocess.PIPE)
    # Decode the result from bytes to string and remove any trailing newlines
    ip_address = result.stdout.decode('utf-8').strip()
    return ip_address

if __name__ == "__main__":
    wsl_ip = get_wsl_ip()
    print(f"WSL2 IP Address: {wsl_ip}")

