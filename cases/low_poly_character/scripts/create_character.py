# Low-poly character v0.1 blockout (2026-11-10)
# Requires: pip install trimesh numpy
# The generated GLB is an approximate blockout, NOT a final recreation.
import trimesh as tm, numpy as np, math, random
from pathlib import Path
random.seed(9)
scene=tm.Scene()
C={'skin':(172,116,96,255),'skinlight':(198,137,110,255),'olive':(72,91,73,255),'olive2':(81,103,81,255),'olive_dark':(48,64,53,255),'brown':(67,47,42,255),'hair':(64,47,40,255),'boot':(31,36,47,255),'white':(202,202,190,255),'gray':(126,125,125,255),'steel':(100,107,115,255),'red':(126,28,36,255),'deepred':(76,20,27,255),'vest':(66,56,43,255),'black':(39,30,29,255)}
def add(mesh,col,name):
 mesh.visual.face_colors=np.tile(np.array(col,dtype=np.uint8),(len(mesh.faces),1));scene.add_geometry(mesh,geom_name=name)
def box(n, pos, ext,col,rot=None):
 m=tm.creation.box(extents=ext);m.apply_translation(pos) if rot is None else None
 if rot is not None:
  m.apply_transform(rot);m.apply_translation(pos)
 add(m,col,n)
def sphere(n,pos,scale,col,sub=1):
 m=tm.creation.icosphere(subdivisions=sub,radius=1);m.apply_scale(scale);m.apply_translation(pos);add(m,col,n)
def segment(n,a,b,r1,r2,col,sections=7):
 a=np.array(a,float);b=np.array(b,float);d=b-a;length=np.linalg.norm(d)
 mesh=tm.creation.cone(radius=r1,height=length,sections=sections) if r2==0 else tm.creation.cylinder(radius=1,height=length,sections=sections)
 if r2!=0:
  ang=np.linspace(0,2*np.pi,sections,endpoint=False);vs=[]
  for z,r in [(-length/2,r1),(length/2,r2)]:
   vs.extend([[r*np.cos(t),r*np.sin(t),z] for t in ang])
  vs.extend([[0,0,-length/2],[0,0,length/2]]);fs=[]
  for k in range(sections):
   j=(k+1)%sections;fs.extend([[k,j,sections+j],[k,sections+j,sections+k],[2*sections,j,k],[2*sections+1,sections+k,sections+j]])
  mesh=tm.Trimesh(vertices=vs,faces=fs,process=False)
 rot=tm.geometry.align_vectors([0,0,1],d/length);mesh.apply_transform(rot);mesh.apply_translation((a+b)/2);add(mesh,col,n)
def poly(n,pts,faces,col):add(tm.Trimesh(vertices=np.array(pts),faces=np.array(faces),process=False),col,n)
def coat_panel(n,xs,z_top,z_bottom,yfront,col):
 x0,x1=xs; dz=.08
 pts=[[x0,yfront,z_top],[x1,yfront,z_top],[x1+.03,yfront,z_bottom+dz],[x0-.05,yfront,z_bottom],
      [x0,yfront+.07,z_top],[x1,yfront+.07,z_top],[x1+.03,yfront+.07,z_bottom+dz],[x0-.05,yfront+.07,z_bottom]]
 fs=[[0,1,2],[0,2,3],[4,6,5],[4,7,6],[0,4,5],[0,5,1],[1,5,6],[1,6,2],[2,6,7],[2,7,3],[3,7,4],[3,4,0]]
 poly(n,pts,fs,col)
sphere('torso_undercoat',[0,0,2.0],[.43,.25,.55],C['olive'],0)
box('vest_body',[0,-.259,2.02],[.43,.055,.72],C['vest'])
coat_panel('left_coat_front',(-.47,-.21),2.45,1.45,-.283,C['olive2'])
coat_panel('right_coat_front',(.21,.47),2.45,1.49,-.283,C['olive'])
box('back_of_coat',[0,.16,1.91],[.8,.17,.86],C['olive'])
coat_panel('back_tail_left',(-.43,-.045),1.68,1.25,.20,C['olive2'])
coat_panel('back_tail_right',(.045,.43),1.68,1.27,.20,C['olive'])
box('shirt_upper',[0,-.304,2.46],[.37,.044,.28],C['white'])
for s in [-1,1]:
 p=[[s*.19,-.343,2.6],[s*.48,-.302,2.46],[s*.31,-.342,2.26],[s*.08,-.344,2.48]]
 poly(f'lapel_{s}',p,[[0,1,2],[0,2,3]],C['brown'])
poly('necktie_top',[[-.09,-.37,2.49],[0,-.372,2.55],[.09,-.37,2.49],[0,-.38,2.41]],[[0,1,2],[0,2,3]],C['red'])
poly('necktie_lower',[[0,-.387,2.42],[-.085,-.387,2.24],[0,-.39,2.1],[.085,-.387,2.24]],[[0,1,2],[0,2,3]],C['red'])
for z in [1.8,1.95,2.10]:sphere('vest_button',[-.015,-.3,z],[.018,.012,.018],C['black'],0)
for s in [-1,1]:
 x=s*.24
 segment(f'thigh_{s}',[x,0,1.65],[x+s*.04,-.045,1.1],.19,.16,C['brown'],6)
 box(f'boot_leg_{s}',[x+s*.06,-.025,.73],[.30,.32,.83],C['boot'])
 box(f'boot_foot_{s}',[x+s*.06,-.19,.245],[.34,.62,.26],C['boot'])
 box(f'boot_sole_{s}',[x+s*.06,-.20,.128],[.35,.66,.075],C['black'])
for s in [-1,1]:
 shoulder=[s*.50,.035,2.40]; elbow=[s*.72,-.02,1.96]; wrist=[s*.65,-.22,1.69]
 segment(f'upper_arm_{s}',shoulder,elbow,.225,.17,C['olive2'],6)
 segment(f'forearm_{s}',elbow,wrist,.176,.126,C['olive'],6)
 sphere(f'hand_{s}',[s*.66,-.24,1.58],[.15,.13,.15],C['skin'],0)
 for j in range(4):
  segment(f'finger_{s}_{j}',[s*(.58+j*.045),-.325,1.56],[s*(.60+j*.055),-.35,1.38+j*.015],.034,.024,C['skinlight'],5)
segment('neck',[0,0,2.49],[0,0,2.68],.14,.14,C['skin'],6)
sphere('head_bulk',[0,-.045,2.99],[.39,.31,.48],C['skin'],0)
sphere('jaw_plate',[0,-.323,2.78],[.32,.16,.18],C['skinlight'],0)
box('deep_eyes',[0,-.351,3.16],[.48,.022,.19],C['deepred'])
for s in [-1,1]:
 box('red_face_wound',[s*.15,-.374,3.04],[.16,.023,.20],C['red'])
segment('forehead_bandage',[-.36,-.25,3.32],[.36,-.25,3.32],.09,.09,C['gray'],6)
box('front_bandage',[0,-.329,3.35],[.71,.09,.16],C['white'])
for s in [-1,1]:
 segment(f'bandage_side_{s}',[s*.35,-.22,3.34],[s*.34,.25,3.30],.065,.067,C['white'],5)
sphere('hair_cap',[0,-.002,3.52],[.42,.355,.25],C['hair'],1)
poly('fringe',[[ -.35,-.30,3.56],[.31,-.35,3.55],[.25,-.376,3.37],[-.36,-.38,3.43],[-.1,-.38,3.60]],[[0,4,1],[0,1,3],[1,2,3]],C['brown'])
for s in [-1,1]:
 poly(f'side_hair_{s}',[[s*.33,0,3.74],[s*.47,.0,3.62],[s*.44,-.13,3.36],[s*.31,-.10,3.46]],[[0,1,2],[0,2,3]],C['hair'])
for s in [-1,1]:
 poly(f'back_bandage_tails_{s}',[[s*.15,.31,3.33],[s*.32,.28,3.25],[s*.17,.32,3.03]],[[0,1,2]],C['white'])
stock=np.array([-.69,-.39,1.62]);far=np.array([-.92,-1.13,.56]);axis=(far-stock)
segment('gun_wood_stock',stock,stock+axis*.30,.100,.075,C['brown'],6)
segment('gun_barrel',stock+axis*.26,far,.07,.045,C['steel'],7)
segment('gun_muzzle',far-axis*.055,far,.064,.067,C['gray'],7)
segment('gun_shroud',stock+axis*.31,stock+axis*.49,.100,.082,C['gray'],6)
for i,(a,b) in enumerate([([-.72,-.47,1.42],[-.80,-.57,1.39]),([-.80,-.57,1.39],[-.84,-.53,1.49])]):segment(f'trigger_guard_{i}',a,b,.017,.017,C['steel'],5)
segment('gun_sight',far-axis*.07+np.array([0,0,.04]),far-axis*.07+np.array([0,0,.11]),.025,.011,C['steel'],5)
segment('hammer',stock+np.array([0,0,.0]),stock+np.array([-.025,.02,.14]),.024,.021,C['gray'],5)
out=Path(__file__).with_name('low_poly_character.glb')
scene.export(out)
print('exported',len(scene.geometry),'meshes to',out)
