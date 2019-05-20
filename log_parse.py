def parse_log():
    dones = set()
    with open('log.txt', 'r') as log:
        for line in log.readlines():
            items = line.strip().split(' ')
            if 'done' in items or 'nothing' in items:
                dones.add(items[-2])
    return dones

if __name__ == "__main__":
    print(parse_log())