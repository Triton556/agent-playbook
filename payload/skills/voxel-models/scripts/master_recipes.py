"""Original higher-detail master construction examples, not upscaled coarse grids."""
import argparse,json,math,pathlib
from voxel_recipes import Grid,vox_bytes
from voxel_mesh import export_obj

def cottage():
    g = Grid()
    w = 48
    d = 38
    h = 28
    g.box(0, 0, 0, w, d, h, 9)
    g.box(2, 2, 2, w - 2, d - 2, h + 1, 0)
    g.box(-1, -1, 0, w + 1, d + 1, 3, 14)
    g.box(21, -1, 2, 28, 3, 19, 0)
    for x in (19, 28):
        g.box(x, -1, 3, x + 2, 1, 21, 1)
    g.box(19, -1, 19, 30, 1, 21, 1)
    g.box(18, -5, 0, 31, 0, 1, 14)
    g.box(20, -3, 1, 29, 0, 2, 14)
    for x in (5, 34):
        g.box(x, -1, 12, x + 8, 1, 24, 1)
        g.box(x + 1, -1, 13, x + 7, 1, 23, 8)
        g.box(x + 3, -2, 13, x + 4, 0, 23, 18)
        g.box(x + 1, -2, 17, x + 7, 0, 18, 18)
        g.box(x - 1, -3, 11, x + 9, 2, 13, 2)
    for y in (7, 25):
        g.box(-1, y, 13, 1, y + 7, 23, 8)
        g.box(-2, y + 3, 13, 0, y + 4, 23, 18)
        g.box(-2, y, 17, 0, y + 7, 18, 18)
    for x in range(-3, w + 3):
        for y in range(-3, d + 3):
            z = h + round((d / 2 - abs(y - (d - 1) / 2)) * 0.72)
            for dz in (0, 1):
                g.put(x, y, z + dz, 10 if y // 3 % 2 else 11)
            if x in (0, 1, w - 2, w - 1) and 0 <= y < d:
                g.box(x, y, h, x + 1, y + 1, z, 9)
    g.box(-3, 18, h + 14, w + 3, 20, h + 16, 10)
    g.box(37, 25, h + 7, 42, 30, h + 23, 14)
    g.box(38, 26, h + 18, 41, 29, h + 23, 0)
    return g

def van():
    g = Grid()
    w = 30
    l = 60
    g.box(3, 3, 8, w - 3, l - 3, 19, 7)
    g.box(4, 5, 6, w - 4, l - 5, 9, 15)
    g.box(5, 20, 18, w - 5, l - 6, 31, 7)
    g.box(7, 23, 20, w - 7, l - 9, 29, 0)
    for z in range(19, 30):
        y = 20 - round((z - 19) * 0.4)
        g.box(5, y, z, w - 5, y + 2, z + 1, 8)
    g.box(4, 15, 30, w - 4, l - 5, 32, 7)
    for x in (4, w - 6):
        g.box(x, 24, 21, x + 2, 34, 29, 8)
        g.box(x, 37, 21, x + 2, l - 10, 29, 8)
        g.box(x, 23, 19, x + 2, 24, 29, 15)
        g.box(x, 35, 19, x + 2, 36, 29, 15)
        g.box(x - 1, 30, 19, x + 3, 34, 20, 14)
    for y in (13, l - 13):
        for yy in range(y - 7, y + 8):
            for z in range(0, 15):
                if (yy - y) ** 2 + (z - 7) ** 2 <= 49:
                    g.box(1, yy, z, 7, yy + 1, z + 1, 0)
                    g.box(w - 7, yy, z, w - 1, yy + 1, z + 1, 0)
        for x in (2, w - 6):
            for yy in range(y - 6, y + 7):
                for z in range(1, 14):
                    if (yy - y) ** 2 + (z - 7) ** 2 <= 40:
                        g.box(x, yy, z, x + 4, yy + 1, z + 1, 12)
            g.ellipsoid(x + 1.5, y, 7, 2.1, 2.8, 2.8, 14)
        g.box(5, y - 1, 6, w - 5, y + 2, 9, 15)
    g.box(3, 1, 9, w - 3, 4, 12, 15)
    g.box(10, 2, 12, 20, 3, 16, 12)
    for x in (5, w - 9):
        g.box(x, 1, 13, x + 4, 3, 17, 18)
        g.box(x, l - 3, 13, x + 4, l - 1, 18, 10)
    g.box(0, 23, 25, 4, 27, 27, 7)
    g.box(w - 4, 23, 25, w, 27, 27, 7)
    return g

def ranger():
    g = Grid()
    g.box(7, 6, 25, 21, 18, 45, 3)
    for x in (7, 15):
        g.box(x, 7, 3, x + 6, 16, 26, 15)
        g.box(x, 3, 0, x + 7, 17, 5, 12)
        g.box(x, 7, 18, x + 6, 8, 22, 2)
    for x in (3, 21):
        g.box(x, 7, 28, x + 4, 16, 44, 3)
        g.box(x, 7, 26, x + 4, 16, 29, 2)
        g.box(x, 7, 23, x + 4, 14, 27, 16)
    g.box(7, 4, 44, 21, 18, 58, 16)
    for x in (9, 16):
        g.box(x, 3, 51, x + 3, 5, 54, 12)
        g.put(x, 3, 53, 18)
    g.box(13, 1, 48, 16, 5, 52, 16)
    g.box(11, 3, 47, 17, 5, 48, 10)
    for x in (5, 21):
        g.box(x, 8, 48, x + 2, 13, 53, 16)
    g.box(4, 1, 57, 24, 21, 59, 2)
    g.box(7, 5, 59, 21, 18, 64, 2)
    g.box(7, 5, 59, 21, 18, 60, 1)
    g.box(6, 5, 29, 22, 19, 32, 1)
    g.box(12, 4, 29, 16, 6, 32, 13)
    for x in (8, 18):
        g.box(x, 5, 32, x + 2, 7, 44, 2)
    g.box(9, 18, 31, 20, 23, 44, 1)
    g.box(10, 19, 43, 19, 24, 46, 2)
    return g

RECIPES={'cottage':cottage,'van':van,'ranger':ranger}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--family',choices=list(RECIPES)+['all'],default='all');ap.add_argument('--output',type=pathlib.Path,required=True);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    rows=[]
    for family in RECIPES if args.family=='all' else [args.family]:
        g=RECIPES[family]();size,cells=g.normalized();(args.output/(family+'-master.vox')).write_bytes(vox_bytes(g));quads=export_obj(cells,args.output/(family+'-master.obj'))
        rows.append({'family':family,'size':size,'occupied':len(cells),'greedyQuads':quads,'coordinateUnit':'object-space design grid; physical meter pitch not specified'})
    (args.output/'master-manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf8');print(json.dumps(rows))
if __name__=='__main__':main()
