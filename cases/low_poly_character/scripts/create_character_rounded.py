#!/usr/bin/env python3
"""Rounded, unified low-poly character v0.2.

Input: low_poly_character.glb produced by create_character.py.
Output: one connected watertight BODY + separate CAP and WEAPON objects.
Requires: numpy scipy scikit-image trimesh vtk.
Run: python create_character.py; python create_character_rounded.py.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import numpy as np
import trimesh as tm
from scipy.ndimage import gaussian_filter, binary_closing, generate_binary_structure, label
from scipy.spatial import cKDTree
from skimage.measure import marching_cubes

PALETTE = {"skin":(172,116,96,255),"skinlight":(198,137,110,255),"olive":(72,91,73,255),
"olive2":(81,103,81,255),"brown":(67,47,42,255),"hair":(64,47,40,255),"boot":(31,36,47,255),
"white":(202,202,190,255),"gray":(126,125,125,255),"steel":(100,107,115,255),
"red":(126,28,36,255),"deepred":(76,20,27,255),"vest":(66,56,43,255),"black":(39,30,29,255)}

def classify(name):
    if name.startswith(('gun_', 'trigger_guard_', 'hammer')): return 'Weapon'
    if name in ('hair_cap','fringe') or name.startswith('side_hair_'): return 'Cap'
    return 'Body'

def make_thick_triangle(triangle, thickness=.048):
    tri=np.asarray(triangle,float)
    if np.linalg.norm(np.cross(tri[1]-tri[0],tri[2]-tri[0]))<1e-7: return None
    a=tri+np.array([0,-thickness/2,0])
    b=tri+np.array([0, thickness/2,0])
    vertices=np.vstack((a,b))
    faces=[[0,1,2],[5,4,3]]
    for j in range(3):
        k=(j+1)%3
        faces.extend([[j,k,k+3],[j,k+3,j+3]])
    m=tm.Trimesh(vertices=vertices,faces=faces,process=True)
    m.fix_normals()
    return m

def expand_flat(mesh):
    if mesh.is_watertight:return mesh.copy()
    chunks=[]
    for tri in mesh.faces:
        part=make_thick_triangle(mesh.vertices[tri])
        if part is not None:chunks.append(part)
    return tm.util.concatenate(chunks) if chunks else mesh.copy()

def source_to_pieces(scene,kind):
    out=[]
    for name,original in scene.geometry.items():
        if classify(name)!=kind:continue
        mesh=expand_flat(original)
        color=np.array(original.visual.face_colors[0],np.uint8)
        mesh.visual.face_colors=np.tile(color,(len(mesh.faces),1))
        out.append((name,mesh,color))
    return out

def add_bridges(pieces):
    def cylinder(name,a,b,r,c):
        a,b=np.array(a,float),np.array(b,float)
        m=tm.creation.cylinder(radius=r,height=np.linalg.norm(b-a),sections=12)
        m.apply_transform(tm.geometry.align_vectors([0,0,1],b-a))
        m.apply_translation((a+b)/2)
        pieces.append((name,m,np.array(c,np.uint8)))
    cylinder('neck_join',[0,0,2.40],[0,0,2.71],.143,PALETTE['skin'])
    cylinder('core_join',[0,0,1.55],[0,0,2.38],.195,PALETTE['vest'])

def voxel_union(parts,pitch=.018,sigma=1.55,closing=2):
    bounds=np.array([m.bounds for _,m,_ in parts])
    origin=bounds[:,0,:].min(axis=0)-pitch*6
    high=bounds[:,1,:].max(axis=0)+pitch*6
    size=np.ceil((high-origin)/pitch).astype(int)+1
    solid=np.zeros(size,dtype=bool)
    for name,m,col in parts:
        if not m.is_watertight:
            print('WARNING: cannot voxelize unclosed part',name)
            continue
        v=m.voxelized(pitch).fill()
        idx=np.rint((v.points-origin)/pitch).astype(int)
        good=np.all((idx>=0)&(idx<size),axis=1)
        idx=idx[good]
        solid[idx[:,0],idx[:,1],idx[:,2]]=True
    if closing:
        solid=binary_closing(solid,structure=generate_binary_structure(3,1),iterations=closing)
    _,components=label(solid)
    print('occupancy components:',components)
    field=gaussian_filter(solid.astype(np.float32),sigma=sigma,mode='constant')
    vertices,faces,_,_=marching_cubes(field,level=.39,spacing=(pitch,)*3)
    m=tm.Trimesh(vertices=vertices+origin,faces=faces,process=False)
    m.fix_normals()
    return m

def decimate(mesh,target=11000,smoothing_iterations=8):
    import vtk
    from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy
    points=vtk.vtkPoints()
    points.SetData(numpy_to_vtk(np.ascontiguousarray(mesh.vertices,dtype=np.float64),deep=True))
    faces=vtk.vtkCellArray()
    for tri in mesh.faces:
        faces.InsertNextCell(3)
        for k in tri:faces.InsertCellPoint(int(k))
    surface=vtk.vtkPolyData();surface.SetPoints(points);surface.SetPolys(faces)
    smooth=vtk.vtkWindowedSincPolyDataFilter();smooth.SetInputData(surface)
    smooth.SetNumberOfIterations(smoothing_iterations);smooth.SetPassBand(.28)
    smooth.BoundarySmoothingOff();smooth.FeatureEdgeSmoothingOff();smooth.NormalizeCoordinatesOn();smooth.Update()
    dec=vtk.vtkDecimatePro();dec.SetInputConnection(smooth.GetOutputPort())
    dec.SetTargetReduction(max(0.,min(.98,1-target/len(mesh.faces))))
    dec.PreserveTopologyOn();dec.SplittingOff();dec.BoundaryVertexDeletionOff();dec.Update()
    out=dec.GetOutput()
    p=vtk_to_numpy(out.GetPoints().GetData())
    # VTK exports triangle faces with 3 vertex indices per polygon.
    raw=vtk_to_numpy(out.GetPolys().GetData()).reshape(-1,4)[:,1:]
    m=tm.Trimesh(vertices=np.array(p),faces=np.array(raw),process=True)
    m.fix_normals()
    return m

def transfer_face_colors(mesh,parts):
    points=[];colors=[]
    for name,source,color in parts:
        if source.area<1e-8:continue
        n=max(60,min(15000,int(source.area*2400)))
        sample,_=tm.sample.sample_surface(source,n,seed=42)
        points.append(sample)
        colors.extend([color]*len(sample))
    tree=cKDTree(np.vstack(points))
    _,idx=tree.query(mesh.triangles_center,workers=-1)
    mesh.visual.face_colors=np.asarray(colors,dtype=np.uint8)[idx]

def build(source,target,pitch=.018):
    scn=tm.load(source,force='scene')
    grouped={k:source_to_pieces(scn,k) for k in ('Body','Cap','Weapon')}
    add_bridges(grouped['Body'])

    body=voxel_union(grouped['Body'],pitch=pitch,sigma=1.55,closing=2)
    body=decimate(body,target=11000,smoothing_iterations=8)
    # Ignore tiny floating triangle artifacts and retain the genuine connected solid.
    islands=body.split(only_watertight=False)
    if len(islands)>1:
        body=max(islands,key=lambda x:x.volume if x.is_watertight else x.area)
    transfer_face_colors(body,grouped['Body'])

    cap=voxel_union(grouped['Cap'],pitch=pitch,sigma=1.3,closing=1)
    cap=decimate(cap,target=1650,smoothing_iterations=3)
    transfer_face_colors(cap,grouped['Cap'])

    weapon=tm.util.concatenate([m for _,m,_ in grouped['Weapon']])
    weapon.visual.face_colors=np.vstack([np.tile(c,(len(m.faces),1)) for _,m,c in grouped['Weapon']])

    out=tm.Scene()
    out.add_geometry(body,geom_name='01_Body_Unified_Rounded',node_name='01_Body_Unified_Rounded')
    out.add_geometry(cap,geom_name='02_Cap_Separate',node_name='02_Cap_Separate')
    out.add_geometry(weapon,geom_name='03_Weapon_Separate',node_name='03_Weapon_Separate')
    out.export(target)
    print('saved',target)
    for name,m in out.geometry.items():
        print(name,len(m.faces),'triangles','watertight',m.is_watertight,'islands',len(m.split(only_watertight=False)))
    return out

if __name__=='__main__':
    directory=Path(__file__).parent
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',default=str(directory/'low_poly_character.glb'))
    ap.add_argument('--output',default=str(directory/'low_poly_character_rounded_v02.glb'))
    ap.add_argument('--pitch',type=float,default=.018)
    args=ap.parse_args()
    build(args.input,args.output,args.pitch)
