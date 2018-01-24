maploc = []

if gc.round()==1:
    start_Node=location.map_location()
    if location.y  < earthMap.height//2:
        if "Bottom" not in  maploc:
            maploc.append("Bottom")
    if location.y > earthMap.height//2:
        if "Top" not in maploc:
            maploc.append("Top")

if gc.round()==2:
    if len(maploc) ==1:
        pos = print(maploc)
    else:
        if location.x < earthMap.width//2:
            pos = "Left"
        else:
            pos = "Right"
