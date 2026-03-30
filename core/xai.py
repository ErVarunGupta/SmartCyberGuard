def explain(cpu, ram, disk):

    total = cpu + ram + disk

    return [
        ("CPU", round(cpu/total*100, 2)),
        ("RAM", round(ram/total*100, 2)),
        ("Disk", round(disk/total*100, 2)),
    ]