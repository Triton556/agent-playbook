"""Small reusable grid checks. Missing contracts are unknown, never a pass.

Coordinates refer to the same declared source space. A mask describes ownership,
not just the final palette: overlapping pieces can overwrite each other's colors.
All checks are static and do not establish perception or dynamics.
"""
from collections import deque
from itertools import product

DIRS=((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))

def result(check,status,**evidence):
    return dict(check=check,status=status,evidence=evidence)

def forbidden_overlap(parts,a,b,allowed=()):
    if a not in parts or b not in parts:
        return result('forbidden_overlap','unknown',missing=[p for p in (a,b) if p not in parts])
    overlap=(set(parts[a])&set(parts[b]))-set(allowed)
    return result('forbidden_overlap','fail' if overlap else 'pass',parts=[a,b],
                  overlapCells=len(overlap),examples=[list(p) for p in sorted(overlap)[:8]])

def required_contact(parts,a,b,allowed_overlap=True):
    if a not in parts or b not in parts:
        return result('required_contact','unknown',missing=[p for p in (a,b) if p not in parts])
    aa,bb=set(parts[a]),set(parts[b]);overlap=aa&bb
    faces=sum((x+dx,y+dy,z+dz) in bb for x,y,z in aa for dx,dy,dz in DIRS)
    ok=bool(faces or (overlap and allowed_overlap))
    return result('required_contact','pass' if ok else 'fail',parts=[a,b],
                  sharedCells=len(overlap),faceContacts=faces)

def clearance(parts,a,b,empty_layers=1,allowed=()):
    """Require empty cell layers (26-neighborhood) except an explicit socket.

    For one empty layer, occupied cells cannot touch by face/edge/corner. This is
    conservative for rotation clearance; it is not a continuous collision solver.
    """
    if a not in parts or b not in parts:return result('clearance','unknown')
    aa,bb=set(parts[a]),set(parts[b]);allowed=set(allowed);hits=set()
    for x,y,z in aa:
        for dx,dy,dz in product(range(-empty_layers,empty_layers+1),repeat=3):
            q=(x+dx,y+dy,z+dz)
            if q in bb and q not in allowed and (x,y,z) not in allowed:hits.add(q)
    return result('clearance','fail' if hits else 'pass',emptyLayers=empty_layers,
                  nearOrOverlappingCells=len(hits),examples=[list(p) for p in sorted(hits)[:8]])

def cardinal_visible(cells,region,direction):
    """Exact voxel ray visibility for an axis-aligned orthographic view."""
    if direction not in DIRS:raise ValueError('cardinal direction required')
    cells=set(cells);region=set(region)&cells
    if not region:return set()
    axis=next(i for i,n in enumerate(direction) if n);sign=direction[axis]
    bounds=[min(p[axis] for p in cells),max(p[axis] for p in cells)]
    visible=set()
    for p in region:
        q=list(p);q[axis]+=sign;blocked=False
        while bounds[0]<=q[axis]<=bounds[1]:
            if tuple(q) in cells:blocked=True;break
            q[axis]+=sign
        if not blocked:visible.add(p)
    return visible

def functional_region(cells,region,direction,min_visible=1):
    if region is None:return result('functional_region','unknown',reason='semantic region not supplied')
    visible=cardinal_visible(cells,region,direction)
    return result('functional_region','pass' if len(visible)>=min_visible else 'fail',
                  direction=list(direction),regionCells=len(set(region)),visibleCells=len(visible),
                  caveat='Visibility does not establish pixel size, contrast or recognition.')

def material_depth(cells,selected):
    """Distance in selected occupied cells from any adjacent air, not camera occlusion.

    Solid nonselected load cores are retained and are not used as air seeds.
    """
    occupied=set(cells);selected=set(selected);depth={};queue=deque()
    for x,y,z in selected:
        if any((x+dx,y+dy,z+dz) not in occupied for dx,dy,dz in DIRS):
            p=(x,y,z);depth[p]=1;queue.append(p)
    while queue:
        x,y,z=queue.popleft();d=depth[(x,y,z)]+1
        for dx,dy,dz in DIRS:
            p=(x+dx,y+dy,z+dz)
            if p in selected and p not in depth:depth[p]=d;queue.append(p)
    return depth

def unit_faces(cells):
    occupied=set(cells)
    return sum((x+dx,y+dy,z+dz) not in occupied for x,y,z in occupied for dx,dy,dz in DIRS)

def exterior_faces(cells):
    """Exact faces bordering flood-filled outside air; closed cavities excluded.

    This deliberately excludes sealed interior faces. Use only for an opaque
    exterior render contract, not a destructible/cutaway/inside-view mesh.
    Returns (cell,direction) tuples, preserving color lookup in the input grid.
    """
    occupied=set(cells)
    if not occupied:return set()
    lo=[min(p[a] for p in occupied)-1 for a in range(3)]
    hi=[max(p[a] for p in occupied)+1 for a in range(3)]
    air={tuple(lo)};queue=deque(air);faces=set()
    while queue:
        x,y,z=queue.popleft()
        for dx,dy,dz in DIRS:
            p=(x+dx,y+dy,z+dz)
            if p in occupied:faces.add((p,(-dx,-dy,-dz)))
            elif all(lo[a]<=p[a]<=hi[a] for a in range(3)) and p not in air:
                air.add(p);queue.append(p)
    return faces

def layer_coverage(region_a,region_b,required_fraction=1):
    """Simple explicit XY substrate mask test. Does not infer a biome."""
    if region_a is None or region_b is None:return result('layer_coverage','unknown')
    a={(p[0],p[1]) for p in region_a};b={(p[0],p[1]) for p in region_b}
    if not a:return result('layer_coverage','unknown',reason='empty subject region')
    good=a&b
    return result('layer_coverage','pass' if len(good)/len(a)>=required_fraction else 'fail',
                  subjectColumns=len(a),supportedColumns=len(good),fraction=len(good)/len(a),
                  examplesMissing=[list(p) for p in sorted(a-b)[:8]])
