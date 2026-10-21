// MODE packaging renders. Units are millimetres; textures are the real print artwork (build/tex).
// Scene is chosen by the URL hash: #sachets, #frontback, #carton, #range, #mailer-open, #mailer-closed, #tumbler
import * as THREE from './three.module.js';
import { RoomEnvironment } from './RoomEnvironment.js';
import { EffectComposer } from './jsm/postprocessing/EffectComposer.js';
import { RenderPass } from './jsm/postprocessing/RenderPass.js';
import { BokehPass } from './jsm/postprocessing/BokehPass.js';
import { OutputPass } from './jsm/postprocessing/OutputPass.js';

const W = window.innerWidth, H = window.innerHeight;
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.VSMShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
const TM = new URLSearchParams(location.search).get('tm') || 'linear';
renderer.toneMapping = TM === 'linear' ? THREE.LinearToneMapping : THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = TM === 'linear' ? 1.0 : 0.92;
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentRotation && scene.environmentRotation.set(0, 0.6, 0);

const loader = new THREE.TextureLoader();
const tex = (name) => new Promise((res) => loader.load(`../build/tex/${name}.png`, (t) => {
  t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; res(t);
}));

const C = { paper: '#F4F2ED', oat: '#E6DCCB', roast: '#4B3D2F', carbon: '#151515', kraft: '#C9A57C', stone: '#D9D4CA' };

function ground(color, size = 3000) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(size, size), new THREE.MeshStandardMaterial({ color, roughness: 0.95, envMapIntensity: 0.6 }));
  m.rotation.x = -Math.PI / 2; m.receiveShadow = true; scene.add(m);
  scene.background = new THREE.Color(color);
  scene.fog = new THREE.Fog(color, 700, 1500);        // melt the far table into the backdrop: no horizon line
}

function lights({ x = -160, y = 420, z = 260, intensity = 1.75, span = 260, radius = 10 } = {}) {
  const d = new THREE.DirectionalLight('#fffaf2', intensity);
  d.position.set(x, y, z); d.castShadow = true;
  d.shadow.mapSize.set(2048, 2048);
  Object.assign(d.shadow.camera, { left: -span, right: span, top: span, bottom: -span, near: 10, far: 1600 });
  d.shadow.radius = radius; d.shadow.blurSamples = 24; d.shadow.bias = -0.0004;
  scene.add(d);
  const fill = new THREE.DirectionalLight('#eef2ff', 0.25); fill.position.set(220, 160, 120); scene.add(fill);
  scene.add(new THREE.HemisphereLight('#ffffff', '#d8cfc2', 0.2));
}

// ------------------------------------------------------------------ sachet: pillowed film, crimped seal, snap crease
const S = { w: 60, h: 88, seal: 3.5, puff: 2.5 };
const smooth = (a, b, v) => { const t = Math.min(1, Math.max(0, (v - a) / (b - a))); return t * t * (3 - 2 * t); };

function crimpMap() {
  const k = 10, cv = document.createElement('canvas');
  cv.width = S.w * k; cv.height = S.h * k;
  const g = cv.getContext('2d');
  g.fillStyle = '#808080'; g.fillRect(0, 0, cv.width, cv.height);
  g.save();
  g.beginPath(); g.rect(0, 0, cv.width, cv.height);
  g.rect(S.seal * k, S.seal * k, (S.w - 2 * S.seal) * k, (S.h - 2 * S.seal) * k);
  g.clip('evenodd');
  g.strokeStyle = '#d0d0d0'; g.lineWidth = 3.2;
  for (let i = -cv.height; i < cv.width + cv.height; i += 7.5) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i + cv.height, cv.height); g.stroke(); }
  g.restore();
  const t = new THREE.CanvasTexture(cv); return t;
}
const CRIMP = crimpMap();

function pillow() {
  const geo = new THREE.PlaneGeometry(S.w, S.h, 120, 176);
  const p = geo.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i), y = p.getY(i);
    const dx = S.w / 2 - Math.abs(x), dy = S.h / 2 - Math.abs(y);
    let z = S.puff * Math.pow(smooth(S.seal, S.seal + 11, dx) * smooth(S.seal, S.seal + 15, dy), 0.7);
    z *= 1 - 0.2 * Math.exp(-Math.pow(y / 1.8, 2));                    // the snap crease across the middle
    z += 0.05 * Math.sin(x * 0.9 + y * 0.4) * smooth(S.seal + 4, S.seal + 14, Math.min(dx, dy));   // a little film life
    p.setZ(i, z + 0.08);                                               // keep the two films apart at the seal
  }
  geo.computeVertexNormals();
  return geo;
}
const PILLOW = pillow();

function film(map) {
  return new THREE.MeshPhysicalMaterial({ map, bumpMap: CRIMP, bumpScale: 0.7, roughness: 0.6, metalness: 0,
    clearcoat: 0.18, clearcoatRoughness: 0.5, envMapIntensity: 0.55 });
}

async function sachet(key) {
  const [f, b] = await Promise.all([tex(`sachet-${key}-front`), tex(`sachet-${key}-back`)]);
  const grp = new THREE.Group();
  const front = new THREE.Mesh(PILLOW, film(f));
  const back = new THREE.Mesh(PILLOW, film(b)); back.rotation.y = Math.PI;
  for (const m of [front, back]) { m.castShadow = true; m.receiveShadow = true; grp.add(m); }
  return grp;
}

// lying flat on the table, face up (or face down to show the back)
function lay(obj, x, z, rotDeg = 0, faceDown = false, lift = 0) {
  const wrap = new THREE.Group();
  if (faceDown) obj.rotation.y = Math.PI;          // turned over, so the back reads the right way up
  wrap.add(obj);
  wrap.rotation.set(-Math.PI / 2, 0, THREE.MathUtils.degToRad(rotDeg));
  wrap.position.set(x, S.puff + lift, z);
  scene.add(wrap);
  return wrap;
}

// ------------------------------------------------------------------ carton
const K = { w: 64, h: 92, d: 34 };
async function carton(key) {
  const faces = await Promise.all(['sidea', 'sideb', 'top', 'bottom', 'front', 'back'].map((n) => tex(`carton-${key}-${n}`)));
  const mats = faces.map((map) => new THREE.MeshStandardMaterial({ map, roughness: 0.62, envMapIntensity: 0.8 }));
  const box = new THREE.Mesh(new THREE.BoxGeometry(K.w, K.h, K.d), mats);
  box.castShadow = true; box.receiveShadow = true;
  return box;
}

// ------------------------------------------------------------------ mailer (kraft)
const M = { w: 220, h: 70, d: 160, t: 2.2 };
function kraftMat(extra = {}) {
  const cv = document.createElement('canvas'); cv.width = cv.height = 512;
  const g = cv.getContext('2d');
  g.fillStyle = C.kraft; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 9000; i++) {
    const v = Math.random();
    g.fillStyle = v > 0.5 ? 'rgba(255,240,210,0.07)' : 'rgba(90,60,30,0.08)';
    g.fillRect(Math.random() * 512, Math.random() * 512, 1 + Math.random() * 3, 1);
  }
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(2, 2);
  return new THREE.MeshStandardMaterial({ map: t, roughness: 0.9, envMapIntensity: 0.7, ...extra });
}

async function mailer(open) {
  const grp = new THREE.Group();
  const k = kraftMat();
  const inside = kraftMat({ color: '#e9dccb' });
  const wall = (w, h, d, x, y, z) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), [k, k, k, inside, k, k]); m.position.set(x, y, z); m.castShadow = m.receiveShadow = true; grp.add(m); };
  wall(M.w, M.t, M.d, 0, M.t / 2, 0);                                  // floor
  wall(M.w, M.h, M.t, 0, M.h / 2, M.d / 2 - M.t / 2);                  // front wall
  wall(M.w, M.h, M.t, 0, M.h / 2, -M.d / 2 + M.t / 2);                 // back wall
  wall(M.t, M.h, M.d, M.w / 2 - M.t / 2, M.h / 2, 0);
  wall(M.t, M.h, M.d, -M.w / 2 + M.t / 2, M.h / 2, 0);
  const [top, ins] = await Promise.all([tex('mode-mailer-lid'), tex('mode-mailer-inside-lid')]);
  const lidMats = [k, k, new THREE.MeshStandardMaterial({ map: top, roughness: 0.88, envMapIntensity: 0.7 }),
    new THREE.MeshStandardMaterial({ map: ins, roughness: 0.7, envMapIntensity: 0.8 }), k, k];
  const lid = new THREE.Mesh(new THREE.BoxGeometry(M.w + 4, M.t, M.d + 2), lidMats);
  lid.castShadow = lid.receiveShadow = true;
  const hinge = new THREE.Group();
  hinge.position.set(0, M.h + M.t / 2, -M.d / 2 - 1);
  lid.position.set(0, 0, M.d / 2 + 1);
  hinge.add(lid);
  if (open) hinge.rotation.x = -THREE.MathUtils.degToRad(104);
  grp.add(hinge);
  scene.add(grp);
  return grp;
}

// ------------------------------------------------------------------ tumbler
async function tumbler() {
  const wrap = await tex('mode-tumbler-wrap');
  const grp = new THREE.Group();
  const body = new THREE.Mesh(new THREE.CylinderGeometry(37.5, 34.5, 150, 160, 1, true, Math.PI, Math.PI * 2),
    new THREE.MeshPhysicalMaterial({ map: wrap, roughness: 0.55, metalness: 0.15, clearcoat: 0.2, envMapIntensity: 0.9, side: THREE.DoubleSide }));
  body.position.y = 75;
  const dark = new THREE.MeshPhysicalMaterial({ color: C.carbon, roughness: 0.42, metalness: 0.2, clearcoat: 0.4, envMapIntensity: 1 });
  const base = new THREE.Mesh(new THREE.CircleGeometry(34.5, 96), dark); base.rotation.x = Math.PI / 2; base.position.y = 0.1;
  const lid = new THREE.Mesh(new THREE.CylinderGeometry(38.6, 38.6, 13, 160), dark); lid.position.y = 150 + 6.5;
  const top = new THREE.Mesh(new THREE.CylinderGeometry(33, 36, 4, 160), dark); top.position.y = 150 + 15;
  const sip = new THREE.Mesh(new THREE.BoxGeometry(14, 2, 6), new THREE.MeshStandardMaterial({ color: '#2a2a2a', roughness: 0.6 }));
  sip.position.set(0, 150 + 17.2, 24);
  for (const m of [body, base, lid, top, sip]) { m.castShadow = true; m.receiveShadow = true; grp.add(m); }
  scene.add(grp);
  return grp;
}

function camera(fov, pos, look) {
  const cam = new THREE.PerspectiveCamera(fov, W / H, 5, 5000);
  cam.position.set(...pos); cam.lookAt(new THREE.Vector3(...look));
  return cam;
}

const MODES = ['wake', 'active', 'zen', 'vital', 'calm'];
const scenes = {
  async sachets() {
    ground('#DCD5C9'); lights({ span: 170 });
    // an overlapping fan, the way they'd fall out of the carton
    const P = [['wake', -96, 8, 12, 0], ['active', -48, -6, -5, 2.6], ['zen', 0, 10, 8, 5.2], ['vital', 48, -4, -9, 7.8], ['calm', 96, 8, 6, 10.4]];
    for (const [k, x, z, r, lift] of P) lay(await sachet(k), x, z, r, false, lift);
    return camera(25, [0, 440, 240], [2, 0, 2]);
  },
  async frontback() {
    ground('#D6CEC0'); lights({ span: 160 });
    lay(await sachet('wake'), -38, 0, 3);
    lay(await sachet('wake'), 38, 2, -4, true);
    return camera(26, [0, 360, 150], [0, 0, 0]);
  },
  async carton() {
    ground('#DED8CE'); lights({ x: -220, y: 360, z: 300, span: 180 });
    const box = await carton('wake'); box.position.set(-30, K.h / 2, -20); box.rotation.y = THREE.MathUtils.degToRad(18); scene.add(box);
    const e = await carton('calm'); e.position.set(44, K.d / 2, 6); e.rotation.set(-Math.PI / 2, 0, THREE.MathUtils.degToRad(-14)); scene.add(e);
    lay(await sachet('wake'), 28, 62, 16, false, 0.2);
    lay(await sachet('calm'), -54, 58, -10);
    return camera(30, [40, 210, 330], [0, 34, 10]);
  },
  async range() {
    ground('#DCD5C9'); lights({ x: -260, y: 380, z: 320, span: 220 });
    for (let i = 0; i < 5; i++) {
      const b = await carton(MODES[i]);
      b.position.set(-152 + i * 76, K.h / 2, (i % 2) * 12); b.rotation.y = THREE.MathUtils.degToRad(-10);
      scene.add(b);
    }
    return camera(29, [10, 200, 600], [-4, 38, 0]);
  },
  async 'mailer-open'() {
    ground('#D9D2C6'); lights({ x: -260, y: 520, z: 360, span: 300 });
    await mailer(true);
    for (let i = 0; i < 3; i++) {
      const b = await carton(MODES[i]);
      b.rotation.set(-Math.PI / 2, 0, 0); b.position.set(-70 + i * 70, M.t + K.d / 2, 18); scene.add(b);
    }
    const s = await sachet('vital'); lay(s, 150, 110, 24);
    const s2 = await sachet('calm'); lay(s2, 205, 40, -12);
    return camera(32, [170, 470, 560], [40, 60, -10]);
  },
  async 'mailer-closed'() {
    ground('#DCD5C9'); lights({ x: -240, y: 520, z: 320, span: 300 });
    await mailer(false);
    const b = await carton('zen'); b.position.set(178, K.h / 2, 70); b.rotation.y = THREE.MathUtils.degToRad(-24); scene.add(b);
    lay(await sachet('zen'), 150, 150, 30);
    return camera(28, [140, 520, 470], [40, 20, 30]);
  },
  async tumbler() {
    ground('#D6CEC0'); lights({ x: -260, y: 420, z: 300, span: 220 });
    const t = await tumbler(); t.position.set(-30, 0, 0); t.rotation.y = THREE.MathUtils.degToRad(-6);
    lay(await sachet('zen'), 70, 40, -18);
    const b = await carton('zen'); b.position.set(78, K.d / 2, -50); b.rotation.set(-Math.PI / 2, 0, THREE.MathUtils.degToRad(12)); scene.add(b);
    return camera(28, [60, 230, 420], [10, 70, 0]);
  },
};

// ------------------------------------------------------------------ film shots: a camera path + depth of field
// Each returns { fov, at(u) -> {pos, look, focus} } for u in 0..1 (eased by the caller).
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const mixV = (a, b, u) => a.clone().lerp(b, u);
const ease = (u) => u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
const films = {
  async 'film-fan'() {
    ground('#D3CBBE'); lights({ x: -260, y: 300, z: 140, intensity: 1.75, span: 220, radius: 8 });
    const P = [['wake', -150, 6, 10, 0], ['active', -75, -8, -6, 0.3], ['zen', 0, 8, 7, 0.6], ['vital', 75, -6, -8, 0.9], ['calm', 150, 6, 6, 1.2]];
    for (const [k, x, z, r, lift] of P) lay(await sachet(k), x, z, r, false, lift);
    return { fov: 24, at: (u) => ({ pos: mixV(V(-230, 92, 150), V(150, 112, 175), u), look: mixV(V(-150, 0, 0), V(150, 0, 0), u),
      focus: null }) };
  },
  async 'film-range'() {
    ground('#D6CEC1'); lights({ x: -280, y: 360, z: 300, span: 260, radius: 9 });
    const keys = ['wake', 'active', 'zen', 'vital', 'calm'];
    for (let i = 0; i < 5; i++) {
      const b = await carton(keys[i]); b.position.set(-152 + i * 76, K.h / 2, (i % 2) * 12); b.rotation.y = THREE.MathUtils.degToRad(-10); scene.add(b);
    }
    return { fov: 26, at: (u) => ({ pos: mixV(V(330, 70, 300), V(-60, 150, 470), ease(u)), look: mixV(V(60, 46, 0), V(-10, 42, 0), ease(u)), focus: null }) };
  },
  async 'film-hero'() {
    ground('#DCD5C9'); lights({ x: -240, y: 380, z: 300, intensity: 1.45, span: 220, radius: 10 });
    const b = await carton('wake'); b.position.set(40, K.h / 2, -10); b.rotation.y = THREE.MathUtils.degToRad(-16); scene.add(b);
    const c = await carton('calm'); c.position.set(132, K.h / 2, -112); c.rotation.y = THREE.MathUtils.degToRad(8); scene.add(c);
    lay(await sachet('zen'), 112, 58, 20, false, 0.2);
    lay(await sachet('active'), 12, 74, -12);
    return { fov: 26, at: (u) => ({ pos: mixV(V(-96, 146, 430), V(-84, 122, 372), ease(u)), look: mixV(V(-34, 44, 0), V(-30, 44, 4), ease(u)), focus: null }) };
  },
};

const name = decodeURIComponent(location.hash.slice(1)) || 'sachets';
if (name.startsWith('film-')) {
  films[name]().then((shot) => {
    const cam = new THREE.PerspectiveCamera(shot.fov, W / H, 5, 5000);
    const composer = new EffectComposer(renderer);
    composer.addPass(new RenderPass(scene, cam));
    const bokeh = new BokehPass(scene, cam, { focus: 400, aperture: 0.00006, maxblur: 0.008 });
    composer.addPass(bokeh);
    composer.addPass(new OutputPass());
    window.frameAt = (u) => {
      const k = shot.at(u);
      cam.position.copy(k.pos); cam.lookAt(k.look);
      bokeh.uniforms.focus.value = k.focus ?? cam.position.distanceTo(k.look);
      composer.render();
      return true;
    };
    window.frameAt(0);
    renderer.shadowMap.autoUpdate = false;          // the scene is static: shadows are computed once
    window.__done = true;
  }).catch((e) => { window.__error = String(e && e.stack || e); });
} else {
scenes[name]().then((cam) => {
  renderer.render(scene, cam);
  requestAnimationFrame(() => { renderer.render(scene, cam); window.__done = true; });
}).catch((e) => { window.__error = String(e && e.stack || e); });
}
