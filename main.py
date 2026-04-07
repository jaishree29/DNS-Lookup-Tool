import subprocess

q = ".\\q.exe"

def get_ns_ip(domain):
    result = subprocess.run([q, "@1.1.1.1", "--type=NS", domain], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if " NS " in line:
            ns_hostname = line.split()[-1].rstrip(".")
            ip_result = subprocess.run([q, "@1.1.1.1", "--type=A", ns_hostname], capture_output=True, text=True)
            for ip_line in ip_result.stdout.splitlines():
                if " A " in ip_line:
                    return ip_line.split()[-1]
    return None


with open("domains.txt", "r") as f:

    for line in f:
        domain = line.strip()
        if not domain:
            continue
        
        ns_ip = get_ns_ip(domain)

        if ns_ip is None:
            print(f"{domain} could not resolve NS")
            continue

        result = subprocess.run([q, f"@tls://{ns_ip}", "--type=A", domain], capture_output=True, text=True)

        if result.returncode == 0:
            print(result)
            print(f"{domain} - Supports DoT: True")
        else:
            print(result)
            print(f"{domain} - Supports DoT: False")
