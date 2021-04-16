

if __name__ == "__main__":
    content = None
    with open('utils/input') as f:
        content = f.readlines()
    data = [x.replace("\n", "").split("") for x in content]
    # - japanese: [こうこう]
    #   english: [high school]
    for e in data:
        print(f"- japanese: [\"{e[0]}\"]")
        english = ", ".join([f"\"{x}\"" for x in e[1].split("; ")])
        print(f"  english: [{english}]")
