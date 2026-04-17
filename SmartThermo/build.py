#!/usr/bin/env python3
"""Build self-contained HTML animation files for SmartThermo (dark + light)."""

svgs = []
for i in range(1, 6):
    with open(f"Smart Thermo - 0{i}.svg", 'r') as f:
        svgs.append(f.read().strip())

with open('gsap.min.js', 'r') as f:
    gsap_js = f.read()

animation_js = r'''
var HOLD = 1.2;
var masterTL;

function dc(n) {
  var svg = document.querySelector('#scene-' + n + ' svg');
  if (!svg) return [];
  return Array.from(svg.children).filter(function(el) { return el.tagName.toLowerCase() !== 'defs'; });
}

// Scene 2 wraps everything in a single <g> — get that group's children
function s2Children() {
  var svg = document.querySelector('#scene-2 svg');
  if (!svg) return [];
  // Find the main <g> child
  var g = Array.from(svg.children).find(function(el) { return el.tagName.toLowerCase() === 'g'; });
  if (!g) return [];
  return Array.from(g.children).filter(function(el) { return el.tagName.toLowerCase() !== 'defs'; });
}

function buildMaster() {
  masterTL = gsap.timeline({ repeat: -1, repeatDelay: 0.6 });
  masterTL
    .add(s1()).add(s2(), '>-0.2').add(s3(), '>-0.2')
    .add(s4(), '>-0.2').add(s5(), '>-0.2');
}

// ═════════════════════════════════════════════════════
// SCENE 1: Title hero — ellipses + data streams + bolt + character
// ═════════════════════════════════════════════════════
function s1() {
  var tl = gsap.timeline(), sc = '#scene-1', ch = dc(1);
  if (ch.length < 3) return tl;
  // [0] bg, [1] inner bg (350x267), [2-4] ellipses, [5-12] data lines, [13] bolt, [14] character
  var ell = ch.slice(2, 5), lines = ch.slice(5, 13), bolt = ch[13], img = ch[14];

  gsap.set(sc, { opacity: 0, visibility: 'hidden' });
  ell.forEach(function(e) { gsap.set(e, { opacity: 0, y: 80 }); });
  lines.forEach(function(e) { gsap.set(e, { opacity: 0, scaleY: 0, transformOrigin: 'center top' }); });
  if (bolt) gsap.set(bolt, { opacity: 0, scale: 0, y: 15, transformOrigin: 'center center' });
  if (img) gsap.set(img, { opacity: 0, scale: 0.8, transformOrigin: 'center center' });

  tl.to(sc, { opacity: 1, visibility: 'visible', duration: 0.3 });
  if (img) tl.to(img, { opacity: 1, scale: 1, duration: 0.7, ease: 'back.out(1.4)' }, 0.15);

  ell.forEach(function(e, i) {
    var op = parseFloat(e.getAttribute('opacity')) || 1;
    tl.to(e, { opacity: op, y: 0, duration: 0.7, ease: 'power2.out' }, 0.3 + i * 0.12);
  });
  lines.forEach(function(e, i) { tl.to(e, { opacity: 1, scaleY: 1, duration: 0.5, ease: 'power2.out' }, 0.4 + i * 0.05); });
  if (bolt) tl.to(bolt, { opacity: 1, scale: 1, y: 0, duration: 0.4, ease: 'back.out(2.5)' }, '>-0.3');

  tl.to({}, { duration: HOLD });

  tl.to(lines, { opacity: 0, scaleY: 0, duration: 0.3, stagger: 0.02, ease: 'power2.in' });
  tl.to(ell, { opacity: 0, y: 40, duration: 0.35, stagger: 0.04, ease: 'power2.in' }, '<');
  if (bolt) tl.to(bolt, { opacity: 0, scale: 0, duration: 0.25, ease: 'power2.in' }, '<');
  if (img) tl.to(img, { opacity: 0, scale: 0.85, duration: 0.35, ease: 'power2.in' }, '<');
  tl.set(sc, { opacity: 0, visibility: 'hidden' });
  return tl;
}

// ═════════════════════════════════════════════════════
// SCENE 2: 3 tilted notification cards + bottom chart area
// ═════════════════════════════════════════════════════
function s2() {
  var tl = gsap.timeline(), sc = '#scene-2';
  var ch = s2Children();
  if (ch.length < 5) return tl;

  // [0] inner bg, [1-2] card1 (fill, stroke), [3] card1 icons group,
  // [4-5] card2 (fill, stroke), [6] card2 icons group,
  // [7-8] card3 (fill, stroke), [9-12] card3 icons,
  // [13] bottom chart group
  // Cards have SVG rotation transforms — do NOT animate rotation
  var card1 = [ch[1], ch[2], ch[3]].filter(Boolean);
  var card2 = [ch[4], ch[5], ch[6]].filter(Boolean);
  var card3 = [ch[7], ch[8]].concat(ch.slice(9, 13)).filter(Boolean);
  var bottom = ch.slice(13).filter(Boolean);

  gsap.set(sc, { opacity: 0, visibility: 'hidden' });
  gsap.set(card1, { opacity: 0, y: -50, x: 40 });
  gsap.set(card2, { opacity: 0, y: -30, x: -50 });
  gsap.set(card3, { opacity: 0, y: 50, x: 30 });
  gsap.set(bottom, { opacity: 0, y: 40 });

  tl.to(sc, { opacity: 1, visibility: 'visible', duration: 0.3 });
  tl.to(card1, { opacity: 1, y: 0, x: 0, duration: 0.6, stagger: 0.04, ease: 'back.out(1.1)' }, 0.15);
  tl.to(card2, { opacity: 1, y: 0, x: 0, duration: 0.6, stagger: 0.04, ease: 'back.out(1.1)' }, 0.25);
  tl.to(card3, { opacity: 1, y: 0, x: 0, duration: 0.6, stagger: 0.04, ease: 'back.out(1.1)' }, 0.35);
  tl.to(bottom, { opacity: 1, y: 0, duration: 0.5, stagger: 0.03, ease: 'power2.out' }, 0.5);

  tl.to({}, { duration: HOLD });

  tl.to(card1.concat(card2, card3), { opacity: 0, y: -30, duration: 0.35, stagger: 0.02, ease: 'power2.in' });
  tl.to(bottom, { opacity: 0, y: 30, duration: 0.3, ease: 'power2.in' }, '<');
  tl.set(sc, { opacity: 0, visibility: 'hidden' });
  return tl;
}

// ═════════════════════════════════════════════════════
// SCENE 3: Horizontal temperature scale with tick marks + indicator circle
// ═════════════════════════════════════════════════════
function s3() {
  var tl = gsap.timeline(), sc = '#scene-3', ch = dc(3);
  if (ch.length < 10) return tl;
  // [0] bg, [1] inner bg, [2] top dark pill, [3-15] tick lines (inc path arrow at 16), [16-29] more ticks
  // [30] blue indicator circle, [31] inner pill, [32-33] white numbers, [34-35] gray numbers
  var topPill = ch[2];
  var ticks = ch.slice(3, 30);    // all tick marks + path markers
  var indicator = ch[30];
  var innerPill = ch[31];
  var labels = ch.slice(32, 36);

  gsap.set(sc, { opacity: 0, visibility: 'hidden' });
  if (topPill) gsap.set(topPill, { opacity: 0, y: -20, scale: 0.9, transformOrigin: 'center center' });
  ticks.forEach(function(e) { gsap.set(e, { opacity: 0, scaleY: 0, transformOrigin: 'center bottom' }); });
  if (indicator) gsap.set(indicator, { opacity: 0, scale: 0, transformOrigin: 'center center' });
  if (innerPill) gsap.set(innerPill, { opacity: 0, scale: 0.8, transformOrigin: 'center center' });
  labels.forEach(function(e) { gsap.set(e, { opacity: 0, y: 8 }); });

  tl.to(sc, { opacity: 1, visibility: 'visible', duration: 0.3 });
  if (topPill) tl.to(topPill, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: 'back.out(1.4)' }, 0.15);
  tl.to(innerPill, { opacity: 1, scale: 1, duration: 0.5, ease: 'back.out(1.4)' }, 0.2);
  tl.to(labels, { opacity: 1, y: 0, duration: 0.4, stagger: 0.04, ease: 'power2.out' }, 0.3);
  tl.to(ticks, { opacity: 1, scaleY: 1, duration: 0.4, stagger: { each: 0.025, from: 'start' }, ease: 'power2.out' }, 0.35);
  if (indicator) tl.to(indicator, { opacity: 1, scale: 1, duration: 0.5, ease: 'back.out(2)' }, '>-0.2');

  tl.to({}, { duration: HOLD });

  // Indicator pulses during hold
  if (indicator) tl.to(indicator, { scale: 1.15, duration: 0.4, yoyo: true, repeat: 2, ease: 'sine.inOut', transformOrigin: 'center center' }, '<-1.0');

  tl.to(labels, { opacity: 0, y: -5, duration: 0.25, stagger: 0.02, ease: 'power2.in' });
  tl.to(ticks, { opacity: 0, scaleY: 0, duration: 0.3, stagger: { each: 0.015, from: 'end' }, ease: 'power2.in' }, '<');
  if (indicator) tl.to(indicator, { opacity: 0, scale: 0, duration: 0.3, ease: 'power2.in' }, '<');
  if (topPill) tl.to(topPill, { opacity: 0, y: -20, duration: 0.3, ease: 'power2.in' }, '<');
  if (innerPill) tl.to(innerPill, { opacity: 0, scale: 0.8, duration: 0.3, ease: 'power2.in' }, '<');
  tl.set(sc, { opacity: 0, visibility: 'hidden' });
  return tl;
}

// ═════════════════════════════════════════════════════
// SCENE 4: Mode toggle with fox mascot speech bubble
// ═════════════════════════════════════════════════════
function s4() {
  var tl = gsap.timeline(), sc = '#scene-4', ch = dc(4);
  if (ch.length < 10) return tl;
  // [0-1] bg, [2] toggle track, [3] left circle, [4-12] snowflake icons, [13] right circle,
  // [14] sparkle group, [15] dashed line, [16] bubble, [17] bubble border, [18-28] fox face parts,
  // [29-30] labels, [31-32] bottom target indicator
  var toggleTrack = ch[2];
  var leftCircle = ch[3];
  var snowflake = ch.slice(4, 13);
  var rightCircle = ch[13];
  var sparkle = ch[14];
  var dashedLine = ch[15];
  var bubble = [ch[16], ch[17]].filter(Boolean);
  var face = ch.slice(18, 29).filter(Boolean);
  var labels = ch.slice(29, 31).filter(Boolean);
  var target = ch.slice(31, 33).filter(Boolean);

  gsap.set(sc, { opacity: 0, visibility: 'hidden' });
  if (toggleTrack) gsap.set(toggleTrack, { opacity: 0, scale: 0.9, transformOrigin: 'center center' });
  if (leftCircle) gsap.set(leftCircle, { opacity: 0, x: -30, transformOrigin: 'center center' });
  snowflake.forEach(function(e) { gsap.set(e, { opacity: 0, scale: 0, transformOrigin: 'center center' }); });
  if (rightCircle) gsap.set(rightCircle, { opacity: 0, x: 30, transformOrigin: 'center center' });
  if (sparkle) gsap.set(sparkle, { opacity: 0, scale: 0, transformOrigin: 'center center' });
  if (dashedLine) gsap.set(dashedLine, { opacity: 0, scaleY: 0, transformOrigin: 'center top' });
  gsap.set(bubble, { opacity: 0, scale: 0.5, transformOrigin: 'center bottom' });
  face.forEach(function(e) { gsap.set(e, { opacity: 0, scale: 0.7, transformOrigin: 'center center' }); });
  labels.forEach(function(e) { gsap.set(e, { opacity: 0, y: 6 }); });
  target.forEach(function(e) { gsap.set(e, { opacity: 0, scale: 0, transformOrigin: 'center center' }); });

  tl.to(sc, { opacity: 1, visibility: 'visible', duration: 0.3 });
  tl.to(bubble, { opacity: 1, scale: 1, duration: 0.6, stagger: 0.03, ease: 'back.out(1.3)' }, 0.15);
  tl.to(face, { opacity: 1, scale: 1, duration: 0.4, stagger: 0.03, ease: 'back.out(1.4)' }, 0.3);
  tl.to(labels, { opacity: 1, y: 0, duration: 0.35, stagger: 0.05, ease: 'power2.out' }, 0.45);

  if (toggleTrack) tl.to(toggleTrack, { opacity: 1, scale: 1, duration: 0.5, ease: 'back.out(1.3)' }, 0.4);
  if (leftCircle) tl.to(leftCircle, { opacity: 1, x: 0, duration: 0.5, ease: 'back.out(1.5)' }, 0.55);
  tl.to(snowflake, { opacity: 1, scale: 1, duration: 0.3, stagger: 0.03, ease: 'back.out(2)' }, 0.7);
  if (rightCircle) tl.to(rightCircle, { opacity: 1, x: 0, duration: 0.5, ease: 'back.out(1.5)' }, 0.65);
  if (sparkle) tl.to(sparkle, { opacity: 1, scale: 1, duration: 0.4, ease: 'back.out(2)' }, 0.8);
  if (dashedLine) tl.to(dashedLine, { opacity: 1, scaleY: 1, duration: 0.4, ease: 'power2.out' }, 0.9);
  tl.to(target, { opacity: 1, scale: 1, duration: 0.4, stagger: 0.08, ease: 'back.out(2)' }, '>-0.2');

  tl.to({}, { duration: HOLD });

  // Target pulse during hold
  if (target[0]) tl.to(target[0], { scale: 1.15, duration: 0.5, yoyo: true, repeat: 1, ease: 'sine.inOut', transformOrigin: 'center center' }, '<-1.0');

  tl.to(target.concat(snowflake), { opacity: 0, scale: 0.5, duration: 0.3, stagger: 0.02, ease: 'power2.in' });
  if (dashedLine) tl.to(dashedLine, { opacity: 0, scaleY: 0, duration: 0.25, ease: 'power2.in' }, '<');
  if (leftCircle) tl.to(leftCircle, { opacity: 0, x: -20, duration: 0.3, ease: 'power2.in' }, '<');
  if (rightCircle) tl.to(rightCircle, { opacity: 0, x: 20, duration: 0.3, ease: 'power2.in' }, '<');
  if (toggleTrack) tl.to(toggleTrack, { opacity: 0, scale: 0.9, duration: 0.3, ease: 'power2.in' }, '<');
  if (sparkle) tl.to(sparkle, { opacity: 0, scale: 0.5, duration: 0.25, ease: 'power2.in' }, '<');
  tl.to(labels, { opacity: 0, y: -5, duration: 0.25, stagger: 0.02, ease: 'power2.in' }, '<');
  tl.to(face, { opacity: 0, duration: 0.25, stagger: 0.02, ease: 'power2.in' }, '<');
  tl.to(bubble, { opacity: 0, scale: 0.6, duration: 0.3, stagger: 0.02, ease: 'power2.in' }, '<');
  tl.set(sc, { opacity: 0, visibility: 'hidden' });
  return tl;
}

// ═════════════════════════════════════════════════════
// SCENE 5: Route/connection map with fox mascot
// ═════════════════════════════════════════════════════
function s5() {
  var tl = gsap.timeline(), sc = '#scene-5', ch = dc(5);
  if (ch.length < 20) return tl;
  // [0-1] bg, [2-7] route lines and circles (bottom route),
  // [8] heart gradient, [9] group (fox bottom),
  // [10-18] fox with teeth (angry/eating fox),
  // [19] group (fox upper),
  // [20-29] main fox face parts,
  // [30-34] more route circles and lines,
  // [35-37] label paths, [38-41] green check badge
  var routeLines = [ch[3], ch[4], ch[7], ch[32], ch[33], ch[34]].filter(Boolean);
  var routeCircles = [ch[5], ch[6], ch[30], ch[31]].filter(Boolean);
  var heartBg = ch[8];
  var foxLower = ch.slice(10, 19).filter(Boolean);
  var foxUpper = ch.slice(20, 30).filter(Boolean);
  var labels = ch.slice(35, 38).filter(Boolean);
  var greenBadge = ch.slice(38, 42).filter(Boolean);
  var bigHeart = ch[2];

  gsap.set(sc, { opacity: 0, visibility: 'hidden' });
  routeLines.forEach(function(e) {
    try {
      var len = e.getTotalLength();
      gsap.set(e, { strokeDasharray: len, strokeDashoffset: len });
    } catch(x) { gsap.set(e, { opacity: 0 }); }
  });
  routeCircles.forEach(function(e) { gsap.set(e, { opacity: 0, scale: 0, transformOrigin: 'center center' }); });
  if (heartBg) gsap.set(heartBg, { opacity: 0, scale: 0.5, transformOrigin: 'center center' });
  if (bigHeart) gsap.set(bigHeart, { opacity: 0, scale: 0, transformOrigin: 'center center' });
  foxLower.forEach(function(e) { gsap.set(e, { opacity: 0, scale: 0.7, transformOrigin: 'center center' }); });
  foxUpper.forEach(function(e) { gsap.set(e, { opacity: 0, scale: 0.7, transformOrigin: 'center center' }); });
  labels.forEach(function(e) { gsap.set(e, { opacity: 0, y: 6 }); });
  greenBadge.forEach(function(e) { gsap.set(e, { opacity: 0, scale: 0, transformOrigin: 'center center' }); });

  tl.to(sc, { opacity: 1, visibility: 'visible', duration: 0.3 });

  // Routes draw on
  routeLines.forEach(function(e, i) {
    try {
      e.getTotalLength();
      tl.to(e, { strokeDashoffset: 0, duration: 0.6, ease: 'power2.inOut' }, 0.15 + i * 0.05);
    } catch(x) { tl.to(e, { opacity: 1, duration: 0.4 }, 0.15 + i * 0.05); }
  });
  tl.to(routeCircles, { opacity: 1, scale: 1, duration: 0.4, stagger: 0.06, ease: 'back.out(2)' }, 0.3);

  // Heart bg behind fox scales up
  if (heartBg) tl.to(heartBg, { opacity: 1, scale: 1, duration: 0.6, ease: 'back.out(1.3)' }, 0.4);
  if (bigHeart) tl.to(bigHeart, { opacity: 1, scale: 1, duration: 0.5, ease: 'back.out(2)' }, 0.5);

  // Fox mascots appear
  tl.to(foxUpper, { opacity: 1, scale: 1, duration: 0.4, stagger: 0.03, ease: 'back.out(1.4)' }, 0.55);
  tl.to(foxLower, { opacity: 1, scale: 1, duration: 0.4, stagger: 0.03, ease: 'back.out(1.4)' }, 0.65);

  // Green badge pops in
  tl.to(greenBadge, { opacity: 1, scale: 1, duration: 0.4, stagger: 0.05, ease: 'back.out(2.5)' }, '>-0.2');

  // Labels fade in
  tl.to(labels, { opacity: 1, y: 0, duration: 0.35, stagger: 0.05, ease: 'power2.out' }, '>-0.2');

  tl.to({}, { duration: HOLD });

  // Green badge pulse during hold
  if (greenBadge[0]) tl.to(greenBadge[0], { scale: 1.15, duration: 0.4, yoyo: true, repeat: 1, ease: 'sine.inOut', transformOrigin: 'center center' }, '<-0.8');

  tl.to(labels, { opacity: 0, y: -5, duration: 0.25, stagger: 0.02, ease: 'power2.in' });
  tl.to(greenBadge, { opacity: 0, scale: 0.5, duration: 0.3, stagger: 0.02, ease: 'power2.in' }, '<');
  tl.to(foxLower.concat(foxUpper), { opacity: 0, scale: 0.7, duration: 0.3, stagger: 0.02, ease: 'power2.in' }, '<');
  if (bigHeart) tl.to(bigHeart, { opacity: 0, scale: 0, duration: 0.25, ease: 'power2.in' }, '<');
  if (heartBg) tl.to(heartBg, { opacity: 0, scale: 0.5, duration: 0.3, ease: 'power2.in' }, '<');
  tl.to(routeCircles, { opacity: 0, scale: 0, duration: 0.25, stagger: 0.02, ease: 'power2.in' }, '<');
  tl.to(routeLines, { opacity: 0, duration: 0.25, ease: 'power2.in' }, '<');
  tl.set(sc, { opacity: 0, visibility: 'hidden' });
  return tl;
}

// Make SVGs fill viewport (cover, not contain)
document.querySelectorAll('#stage svg').forEach(function(svg) {
  svg.setAttribute('preserveAspectRatio', 'xMidYMid slice');
});

buildMaster();
'''

light_fix_js = r'''
function fixLightColors() {
  var safeMap = {
    '#2E3749':'#FFFFFF','#2e3749':'#FFFFFF',
    '#5D6679':'#94A3B8','#5d6679':'#94A3B8',
    '#8B8F96':'#64748B','#8b8f96':'#64748B',
    '#CECECE':'#94A3B8','#cecece':'#94A3B8',
    '#172031':'#1E293B'
  };
  var preserve = ['#FF2C55','#ff2c55','#2FBF94','#2fbf94','#4285F4','#4285f4','#CA2243','#ca2243',
    '#82D2FF','#82d2ff','#BA1F3D','#ba1f3d','#80192D','#80192d','#C3EFD5','#c3efd5'];
  document.querySelectorAll('#stage svg *').forEach(function(el) {
    ['fill','stroke','stop-color'].forEach(function(attr) {
      var v = el.getAttribute(attr);
      if (!v || v.startsWith('url(')) return;
      if (preserve.indexOf(v) !== -1 || preserve.indexOf(v.toLowerCase()) !== -1) return;
      var m = safeMap[v] || safeMap[v.toLowerCase()];
      if (m) el.setAttribute(attr, m);
    });
  });

  // Scene 2: card fills (were #364157) → light cards
  var c2 = s2Children();
  if (c2[1]) c2[1].setAttribute('fill', '#F8FAFC');
  if (c2[4]) c2[4].setAttribute('fill', '#F8FAFC');
  if (c2[7]) c2[7].setAttribute('fill', '#F8FAFC');
  // Card borders
  [2, 5, 8].forEach(function(i) { if (c2[i]) c2[i].setAttribute('stroke', '#CBD5E1'); });
  // White text inside cards → dark
  document.querySelectorAll('#scene-2 g path[fill="white"]').forEach(function(el) {
    el.setAttribute('fill', '#1E293B');
  });

  // Scene 3: dark pill (was #172031) → light
  var c3 = dc(3);
  if (c3[2]) c3[2].setAttribute('fill', '#F0F2F5');
  if (c3[2]) c3[2].setAttribute('stroke', '#CBD5E1');
  if (c3[31]) c3[31].setAttribute('fill', '#1E293B');   // inner pill (dark) stays dark for contrast
  // White number labels → dark
  if (c3[32]) c3[32].setAttribute('fill', '#FFFFFF');   // text inside dark pill stays white
  if (c3[33]) c3[33].setAttribute('fill', '#475569');   // text above (was white) → dark for visibility

  // Scene 4: dark bubble (#364157) → light
  var c4 = dc(4);
  if (c4[16]) c4[16].setAttribute('fill', '#F0F2F5');
  if (c4[17]) c4[17].setAttribute('fill', '#CBD5E1');
  // White text (was #F5F5F5) inside bubble → dark
  [29, 30].forEach(function(i) { if (c4[i]) c4[i].setAttribute('fill', '#1E293B'); });
  // Toggle track gradient stroke - leave as-is
  // White knob circles stay white
  // Dark inner indicator circle
  if (c4[32]) c4[32].setAttribute('fill', '#FFFFFF');

  // Scene 5: heart bg gradient stays, fox colors preserved
  // Label text fills
  var c5 = dc(5);
  for (var i = 35; i < 38; i++) {
    if (c5[i] && c5[i].getAttribute('fill') === '#94A3B8') {
      c5[i].setAttribute('fill', '#475569');
    }
  }
}
fixLightColors();
'''

def build_html(mode):
    is_light = mode == 'light'
    bg = '#FFFFFF' if is_light else '#2E3749'
    fname = 'index-light.html' if is_light else 'index.html'
    scenes_html = ''
    for i, svg in enumerate(svgs):
        scenes_html += f'<div class="scene" id="scene-{i+1}">\n{svg}\n</div>\n'
    extra_js = light_fix_js + '\n' if is_light else ''
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Smart Thermo{" - Light" if is_light else ""}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:100%;height:100%;overflow:hidden;background:{bg}}}
body{{display:flex;justify-content:center;align-items:center}}
#stage{{position:relative;width:100%;height:100%;max-width:698px;max-height:627px}}
.scene{{position:absolute;top:0;left:0;width:100%;height:100%;opacity:0;visibility:hidden}}
.scene svg{{width:100%;height:100%;display:block}}
</style>
</head>
<body>
<div id="stage">
{scenes_html}
</div>
<script>
{gsap_js}
</script>
<script>
{extra_js}
{animation_js}
</script>
</body>
</html>'''
    with open(fname, 'w') as f:
        f.write(html)
    print(f"Built {fname}: {len(html)//1024} KB")

if __name__ == '__main__':
    build_html('dark')
    build_html('light')
    print("Done!")
