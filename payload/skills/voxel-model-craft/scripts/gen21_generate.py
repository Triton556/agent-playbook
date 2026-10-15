"""Portable Gen2.1 grid/opaque-mesh generator; standard library only."""
import argparse,hashlib,json,pathlib
import gen21_recipes as G
from voxel_recipes import vox_bytes
from voxel_mesh import export_obj
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=pathlib.Path,required=True);ap.add_argument('--seed',type=int,default=153)
    ap.add_argument('--model',choices=[r[1] for r in G.ROWS]);ap.add_argument('--category',choices=sorted({r[0] for r in G.ROWS}));args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True);rows=[]
    for group,slug,title,_,make in G.ROWS:
        if args.model and slug!=args.model or args.category and group!=args.category:continue
        g=make(args.seed);sz,cells=g.normalized();blob=vox_bytes(g);(args.output/(slug+'.vox')).write_bytes(blob)
        if hasattr(g,'opaque_mesh_source'):
            mins=[min(p[i] for p in g.cells) for i in range(3)];mesh={tuple(p[i]-mins[i] for i in range(3)):c for p,c in g.opaque_mesh_source.items()}
        else:mesh=cells
        quads=export_obj(mesh,args.output/(slug+'.obj'))
        rows.append({'slug':slug,'group':group,'version':'gen2.1','seed':args.seed,'size':sz,'occupied':len(cells),'sha256':hashlib.sha256(blob).hexdigest(),'quads':quads,'contract':g.gen2_meta,'renderAndHumanReview':'not performed by this CLI'})
        print(slug,len(cells),flush=True)
    (args.output/'manifest-gen21.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
