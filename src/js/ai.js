/* NovoTech AI machine finder — loaded when the "AI machine finder" panel opens.

   The finder engine runs in the browser on ai/catalogue.json, which the site build writes from everything the site says:
   every product family with its models, spec tables, features, options, the words of its PDF brochure and structured
   capacities per model, and every page with its introduction and questions and answers (tools/ai_index.py). The engine
   works out what the visitor wants to do (cut, bend, roll, punch…), the material (pipe, plate, angle…) and the sizes
   ("2-inch pipe", "30-inch diameter", "1/4″ × 10 ft", "25M"), checks every model's capacity, and answers with the best
   match and the similar machines. On the live server ask.php adds a conversational answer written by Claude from the
   same catalogue, when an API key is configured; the engine's picks are shown either way. */
(function (root) {
  "use strict";

  /* ======================================================================================== text, words, stems */
  var FRAC = { "½": " 1/2", "¼": " 1/4", "¾": " 3/4", "⅛": " 1/8", "⅜": " 3/8", "⅝": " 5/8", "⅞": " 7/8", "⅓": " 1/3", "⅔": " 2/3", "⅙": " 1/6" };
  var SPELL = {
    centre: "center", centres: "centers", metre: "meter", metres: "meters", mitre: "miter", mitres: "miters", mitred: "mitered",
    aluminium: "aluminum", colour: "color", bevelling: "beveling", beveller: "beveler", bevelled: "beveled", levelling: "leveling",
    leveller: "leveler", gage: "gauge", gages: "gauges", sheer: "shear", sheers: "shears", sheering: "shearing", lazer: "laser",
    lazers: "lasers", bandsaw: "band saw", bandsaws: "band saws", ironworkers: "ironworker", tonnes: "tons", tonne: "ton",
    tonnage: "tons", pressbrake: "press brake", brakepress: "press brake", pipebender: "pipe bender", tubebender: "tube bender",
    platerolls: "plate rolls", rollers: "rollers", stainles: "stainless", inox: "stainless", alu: "aluminum", galvanized: "galvanized",
    machiene: "machine", machin: "machine", benderr: "bender", brakes: "brakes", guilotine: "guillotine", guillotin: "guillotine",
    notcher: "notcher", positionner: "positioner", ironwroker: "ironworker", ironworkr: "ironworker"
  };
  // a few words in French (Canada) and Persian, mapped to the English the catalogue uses
  var FOREIGN = [
    [/cisaille|guillotine hydraulique/g, " shear "], [/presse[- ]plieuse|plieuse/g, " press brake "], [/rouleuse|cintreuse? de t[oô]le/g, " plate roll "],
    [/cintreuse/g, " bender "], [/tuyaux?/g, " pipe "], [/\bscie\b/g, " saw "], [/ruban/g, " band "], [/poin[cç]onneuse/g, " punch "],
    [/soudage|soudure/g, " welding "], [/barres? d.armature|armature/g, " rebar "], [/t[oô]les?/g, " sheet "], [/plaques?/g, " plate "],
    [/perceuse/g, " drill "], [/fraiseuse/g, " milling "], [/[ée]paisseur/g, " thickness "], [/diam[eè]tre/g, " diameter "], [/pouces?/g, " inch "],
    [/پرس ?برک|پرسبرک/g, " press brake "], [/گیوتین/g, " guillotine shear "], [/قیچی/g, " shear "], [/نورد/g, " roll "], [/رول/g, " roll "],
    [/خم ?کن|خمکاری|خم/g, " bend "], [/لوله/g, " pipe "], [/پروفیل/g, " profile "], [/میلگرد/g, " rebar "], [/اره/g, " saw "], [/برش/g, " cut "],
    [/لیزر/g, " laser "], [/جوش/g, " welding "], [/سوراخ|پانچ/g, " punch "], [/ورق/g, " sheet "], [/تسمه/g, " flat bar "], [/نبشی/g, " angle "],
    [/ناودانی/g, " channel "], [/تیرآهن|تیر آهن/g, " beam "], [/اینچ/g, " inch "], [/میلیمتر|میلی متر/g, " mm "], [/قطر/g, " diameter "],
    [/ضخامت/g, " thickness "], [/طول/g, " length "], [/تراش/g, " lathe "], [/فرز/g, " milling "], [/دریل/g, " drill "], [/پولیش/g, " polish "],
    [/سنگ ?زنی/g, " grinding "], [/آهنگری|آیرون ?ورکر/g, " ironworker "], [/دستگاه/g, " machine "], [/پرس/g, " press "]
  ];
  var FA_DIGITS = /[۰-۹٠-٩]/g;
  function digits(c) { var k = c.charCodeAt(0); return String(k >= 0x6F0 ? k - 0x6F0 : k - 0x660); }

  var KEYWORDS = ("roller rollers rolling bender benders bending shear shears shearing laser lasers brake brakes press presses saw saws punch punching " +
    "notcher notching ironworker plate plates pipe pipes tube tubes tubing rebar welding welder positioner grinder grinding polisher polishing beveler " +
    "drill lathe milling folder folding guillotine angle channel beam cutter cutting forming former machine machines hydraulic electric automatic " +
    "manual mandrel bandsaw section profile stainless aluminum thickness diameter railing deburring sander positioners turning cylinder").split(" ");
  var KW = {}; KEYWORDS.forEach(function (w) { KW[w] = 1; });
  function spell(s) {
    return s.replace(/[a-z]{4,}/g, function (w) {
      if (KW[w] || SPELL[w] || DF[stem(w)] || STOP[w]) return w;     // words the catalogue uses are not typos
      var max = w.length >= 7 ? 2 : 1, best = null, bd = 9;
      for (var i = 0; i < KEYWORDS.length; i++) {
        var k = KEYWORDS[i];
        if (Math.abs(k.length - w.length) > max) continue;
        var dd = editDist(w, k, max);
        if (dd < bd) { bd = dd; best = k; }
      }
      return best && bd <= max && (bd === 1 || w[0] === best[0]) ? best : w;
    });
  }
  function norm(s, index) {
    s = String(s || "");
    if (index) return s.replace(/[″“”]/g, '"').replace(/[–—]/g, "-").replace(/×/g, " x ").replace(/Ø|⌀/g, " dia ").replace(/□/g, " square ").toLowerCase()
      .replace(/\b(centre|centres|metre|metres|mitre|mitres|aluminium|bevelling|beveller|levelling)\b/g, function (w) { return SPELL[w]; });
    s = s.replace(FA_DIGITS, digits).replace(/[½¼¾⅛⅜⅝⅞⅓⅔⅙]/g, function (c) { return FRAC[c]; });
    s = s.replace(/[″“”]/g, '"').replace(/[′‘’`]/g, "'").replace(/[–—]/g, "-").replace(/×/g, " x ").replace(/Ø|⌀/g, " dia ").replace(/□/g, " square ");
    s = s.toLowerCase();
    FOREIGN.forEach(function (p) { s = s.replace(p[0], p[1]); });
    s = s.replace(/\b(iron[- ]worker|iron work)\b/g, "ironworker").replace(/\bre-bar\b/g, "rebar").replace(/\b([a-z]+)\b/g, function (w) { return SPELL[w] || w; });
    return spell(s);
  }
  var WORD;
  try { WORD = new RegExp("[\\p{L}\\p{N}]+(?:[-./][\\p{L}\\p{N}]+)*", "gu"); } catch (e) { WORD = /[a-z0-9]+(?:[-.\/][a-z0-9]+)*/g; }
  var STOP = {};
  ("a an and are as at be by for from has have in is it its of on or that the this to with was were will can not no your you our we " +
   "their they them than then there these those into per each other more most also only such may which when where who how what all any " +
   "both via up out about above below between while i me my want need looking would like please some much do does did make made use " +
   "using get give show find recommend suggest good best right machine machines").split(" ").forEach(function (w) { STOP[w] = 1; });

  var STEMS = Object.create(null);
  function stem(w) {
    var memo = STEMS[w];
    if (memo !== undefined) return memo;
    return (STEMS[w] = stem_(w));
  }
  function stem_(w) {
    if (w.length < 4 || /\d/.test(w)) return w;
    var s = w;
    if (/sses$/.test(s)) s = s.slice(0, -2);
    else if (/ies$/.test(s) && s.length > 4) s = s.slice(0, -3) + "y";
    else if (/(ch|sh|x|zz)es$/.test(s)) s = s.slice(0, -2);
    else if (/[^su]s$/.test(s)) s = s.slice(0, -1);
    if (/ing$/.test(s) && s.length > 5) s = s.slice(0, -3);
    else if (/ed$/.test(s) && s.length > 4) s = s.slice(0, -2);
    if (/ers?$/.test(s) && s.length > 5) s = s.replace(/ers?$/, "");
    if (/(bb|dd|gg|mm|nn|pp|tt)$/.test(s)) s = s.slice(0, -1);
    if (/e$/.test(s) && s.length > 3) s = s.slice(0, -1);
    return s;
  }
  /* words of a text → stems; model codes are also kept joined ('bs-315gf' → bs, 315gf, bs315gf) */
  function terms(text, index) {
    var out = [], m, t = norm(text, index), keepStop = false;
    WORD.lastIndex = 0;
    while ((m = WORD.exec(t))) {
      var w = m[0];
      var parts = w.split(/[-./]/);
      if (parts.length > 1) {
        parts.forEach(function (p) { if (p.length > 1 && (keepStop || !STOP[p])) out.push(stem(p)); });
        if (/\d/.test(w) && /[a-z]/.test(w)) out.push(w.replace(/[-./]/g, ""));
      } else if (w.length > 1 && (keepStop || !STOP[w])) out.push(stem(w));
    }
    return out;
  }
  function compact(s) { return norm(s).replace(/[^a-z0-9]+/g, ""); }

  /* ======================================================================================== numbers and sizes */
  var NUMRX = "(\\d+[- ]\\d+\\/\\d+|\\d+\\/\\d+|\\d+(?:\\.\\d+)?|\\.\\d+)";
  function val(s) {
    s = String(s).trim();
    var m = /^(\d+)[- ](\d+)\/(\d+)$/.exec(s); if (m) return +m[1] + m[2] / m[3];
    m = /^(\d+)\/(\d+)$/.exec(s); if (m) return m[1] / m[2];
    return parseFloat(s);
  }
  var GA = { 3: .2391, 4: .2242, 5: .2092, 6: .1943, 7: .1793, 8: .1644, 9: .1495, 10: .1345, 11: .1196, 12: .1046, 13: .0897, 14: .0747, 15: .0673,
    16: .0598, 17: .0538, 18: .0478, 19: .0418, 20: .0359, 21: .0329, 22: .0299, 23: .0269, 24: .0239, 25: .0209, 26: .0179, 27: .0164, 28: .0149, 29: .0135, 30: .012 };
  var NPS = { "1/8": .405, "1/4": .54, "3/8": .675, "1/2": .84, "3/4": 1.05, "1": 1.315, "1-1/4": 1.66, "1-1/2": 1.9, "2": 2.375, "2-1/2": 2.875,
    "3": 3.5, "3-1/2": 4, "4": 4.5, "5": 5.563, "6": 6.625, "8": 8.625, "10": 10.75, "12": 12.75, "14": 14, "16": 16, "18": 18, "20": 20, "24": 24 };
  function npsOd(x) {
    var key = fracKey(x);
    return NPS[key] || (x >= 14 ? x : null);
  }
  function fracKey(x) {
    var w = Math.floor(x + 1e-9), f = Math.round((x - w) * 8);
    var fr = { 1: "1/8", 2: "1/4", 3: "3/8", 4: "1/2", 5: "5/8", 6: "3/4", 7: "7/8" }[f];
    return w ? (fr ? w + "-" + fr : String(w)) : (fr || "0");
  }
  var CA_BARS = { "10": 11.3, "15": 16, "20": 19.5, "25": 25.2, "30": 29.9, "35": 35.7, "45": 43.7, "55": 56.4 };
  var US_BARS = { "3": 9.5, "4": 12.7, "5": 15.9, "6": 19.1, "7": 22.2, "8": 25.4, "9": 28.7, "10": 32.3, "11": 35.8, "14": 43, "18": 57.3 };

  function gcd(a, b) { return b ? gcd(b, a % b) : a; }
  function fmtIn(x) {
    if (x == null || isNaN(x)) return "";
    if (x < 0.09) return x.toFixed(3).replace(/^0/, "") + "″";
    if (x >= 24) return (Math.round(x * 10) / 10).toString().replace(/\.0$/, "") + "″";
    var w = Math.floor(x + 1e-9), f = Math.round((x - w) * 16);
    if (f === 16) { w += 1; f = 0; }
    var g = f ? gcd(f, 16) : 1, fr = f ? (f / g) + "/" + (16 / g) : "";
    return (w ? w + (fr ? "-" + fr : "") : (fr || "0")) + "″";
  }
  function fmtLen(x) { return x >= 48 ? (Math.round(x / 12 * 10) / 10).toString().replace(/\.0$/, "") + " ft (" + Math.round(x) + "″)" : fmtIn(x); }
  function fmtThk(x) {
    var best = null, bd = 1;
    if (x < 0.18) for (var g in GA) { var dd = Math.abs(GA[g] - x); if (dd < bd) { bd = dd; best = g; } }
    return best && bd < 0.0046 ? best + " ga (" + fmtIn(x) + ")" : fmtIn(x);
  }
  function fmtLb(x) { return Math.round(x).toLocaleString("en-CA") + " lb"; }

  /* ======================================================================================== understanding a request */
  var MATS = [
    ["rebar", /\brebar|reinforc|stirrup|\b(10|15|20|25|30|35|45|55)\s?m\b|#\s?\d{1,2}\b|\bdowel|\bmesh\b/],
    ["sq_tube", /square (tube|tubing|pipe|hollow|hss|section)|\bshs\b|box section|\bsq\.? tube/],
    ["rect_tube", /rect(angular|angle)? (tube|tubing|pipe|hollow|hss|section)|\brhs\b/],
    ["pipe", /\bpipes?\b|\bpiping\b|\bnps\b|\bnpt\b|\bschedule\b|\bsch\.? ?\d/],
    ["tube", /\btubes?\b|\btubing\b|\bhss\b|exhaust|conduit|handrail|\bod\b/],
    ["flat", /flat ?bars?|\bflats\b|\bflat stock|\bstrap/],
    ["angle", /angle iron|\bangles?\b(?!\s*(cut|cuts|cutting|of|grind|head))|l-?section/],
    ["channel", /\bchannels?\b|\bupn\b|c-?section/],
    ["beam", /\bbeams?\b|i-?beam|h-?beam|\bipe\b|\bheb\b|\bhea\b|wide flange|\bw\d+\s?x/],
    ["tee", /\btees?\b|t-?bars?\b|t-?section/],
    ["rd_bar", /(round|solid) (bar|stock|steel)|\brods?\b|\bshafts?\b|round bar/],
    ["sq_bar", /square (bar|stock)/],
    ["coil", /\bcoils?\b/],
    ["plate", /\bplates?\b/],
    ["sheet", /\bsheets?\b|sheet ?metal|\bgauge\b|\bga\b|\bducts?\b|\bductwork/],
    ["profile", /\bprofiles?\b|\bextrusions?\b|\bsections?\b/],
    ["wire", /\bwires?\b/],
    ["wood", /\bwood|timber|lumber|plywood|\bmdf\b/],
    ["pvc", /\bpvc\b|upvc|vinyl/]
  ];
  var LONG = { rebar: 1, sq_tube: 1, rect_tube: 1, pipe: 1, tube: 1, flat: 1, angle: 1, channel: 1, beam: 1, tee: 1, rd_bar: 1, sq_bar: 1, profile: 1, wire: 1 };
  var OPS = [
    ["roll", /\broll(s|ing|ed)?\b|\brollers?\b|\brings?\b|\bcurv(e|ed|ing)\b|\barc(h|hes|hed|s)?\b|\bcylinders?\b|\bcones?\b|\bhoops?\b|\bcircles?\b|\bspirals?\b|\bhelix|\bcoil (a |the )?(tube|pipe)/],
    ["bend", /\bbend|\bbent\b|\bfold|\bbrak(e|es|ing)\b|\bform(ing|ed)?\b|\b90\s?(°|deg)|\belbows?\b/],
    ["shear", /\bshear|\bguillotine/],
    ["laser", /\blasers?\b/],
    ["cut", /\bcut|\bsaw|\bchop|\bslit|\bparting|\bcut-?off/],
    ["punch", /\bpunch|\bholes?\b|\bpierc|\bperforat/],
    ["notch", /\bnotch|\bcop(e|ing)\b|fish ?mouth|\bsaddle/],
    ["weld", /\bweld/],
    ["grind", /\bgrind|\bdeburr|\bpolish|\bsand(ing|er)?\b|\bfinish(ing)?\b|\bbrush|edge round|\bdross/],
    ["bevel", /\bbevel|\bchamfer|weld prep/],
    ["drill", /\bdrill|\btapping\b/],
    ["mill", /\bmill(ing)?\b|machining cent/],
    ["turn", /\blathe|\bturning\b(?!\s*rolls?)/],
    ["press", /\bpress\b(?!\s*brake)|\bpressing\b|straighten|\bstamp/],
    ["endform", /\bflar(e|ing)|\bexpand|\breduc(e|ing|er)\b|\bswag|end form|tube end/]
  ];

  /* machine types: phrase → product pages and how strongly the phrase means them */
  var TYPES = [
    [/press ?brakes?|brake ?press|bending press|\bcnc brake|\bpb\b/, { "hydraulic-press-brake": 10, "electric-press-brake": 8, "compact-hydraulic-press-brakes": 7 }],
    [/electric (press )?brake|servo[- ]electric|\be-?brake|electric bend/, { "electric-press-brake": 14 }],
    [/hybrid press brake|small press brake|compact press brake|mini press brake|bench press brake|table[- ]top press brake/, { "compact-hydraulic-press-brakes": 12, "electric-press-brake": 9 }],
    [/panel bend/, { "panel-bender": 15 }],
    [/\bfolder|folding machine|double folder|up.?and.?down fold/, { "hydraulic-folding-machine": 13, "box-and-pan-brake": 5, "sheet-metal-hand-brake": 4 }],
    [/box (and|&|n) pan|finger brake|\bpan brake|box brake/, { "box-and-pan-brake": 15 }],
    [/hand brake|manual brake|bench brake|sheet ?metal brake|cornice brake|leaf brake|\bhvac brake/, { "sheet-metal-hand-brake": 12, "box-and-pan-brake": 7, "magnetic-sheet-metal-brake": 5 }],
    [/magnetic brake|magna.?bend|electromagnetic/, { "magnetic-sheet-metal-brake": 15 }],
    [/roofing|siding|trim brake|portable brake|slitter/, { "roofing-siding-brake": 15 }],
    [/3.?in.?1|three.?in.?one|shear.?brake.?roll|combination (machine|shear)/, { "shear-brake-roll-3-in-1": 15 }],
    [/horizontal (press )?brake|horizontal bender|bulldozer|horizontal press|flat ?bar bend/, { "horizontal-press-brake": 14 }],
    [/swing ?beam/, { "hydraulic-shearing-machine": 14 }],
    [/guillotine/, { "hydraulic-shearing-machine": 11, "mechanical-guillotine-shear": 10 }],
    [/mechanical shear|foot shear|treadle|manual shear|power shear|throatless|bench shear/, { "mechanical-guillotine-shear": 13 }],
    [/\bshears?\b|\bshearing\b/, { "hydraulic-shearing-machine": 10, "mechanical-guillotine-shear": 8, "shear-brake-roll-3-in-1": 3 }],
    [/ironworker|punch (and|&) shear|multi.?function (punch|machine)/, { "ironworker-machines": 15 }],
    [/punch(ing)? (machine|press)|beam punch|plate punch|\bpunching\b|hole punch/, { "hydraulic-punching-machines": 12, "ironworker-machines": 9 }],
    [/corner notch|\bnotcher\b|notching machine/, { "corner-notcher": 12, "pipe-notcher": 6 }],
    [/(pipe|tube) notch|notch (pipe|tube)|cop(e|ing) (pipe|tube)|fish ?mouth|saddle cut/, { "pipe-notcher": 15 }],
    [/plate roll|slip roll|bending roll|rolling machine|\b3.?roll|\b4.?roll|four.?roll|three.?roll|plate bending (roll|machine)|tank shell|\bcone|\bcylinder/, { "hydraulic-3-roll-plate-rollers": 9, "hydraulic-4-roll-plate-rollers": 9, "motorized-plate-rollers": 8 }],
    [/\b4.?roll|four.?roll/, { "hydraulic-4-roll-plate-rollers": 15 }],
    [/\b3.?roll|three.?roll/, { "hydraulic-3-roll-plate-rollers": 13, "motorized-plate-rollers": 9 }],
    [/slip roll|electric (slip )?roll|motori[sz]ed (plate )?roll|manual roll/, { "motorized-plate-rollers": 13 }],
    [/angle roll|section bend|profile bend|profile roll|ring roll|roll bender|pipe roll|tube roll|roll(ing)? (pipe|tube|bar|angle|beam|channel|profile)|coil(ing)? machine|tube coil/, { "angle-rolls": 15 }],
    [/tube bend|pipe bend|bend(ing)? (a |the )?(tube|pipe|tubing|exhaust|handrail|conduit)|mandrel|rotary draw|\bcnc bender|\bnc bender|draw bend|exhaust/, { "rotary-draw-tube-benders": 10, "nc-tube-benders": 9, "cnc-tube-benders": 8 }],
    [/tube end|end form|flar(e|ing)|tube expand|expander|swag|pipe reduc|tube reduc|beading tube/, { "tube-end-forming-machines": 15 }],
    [/\blasers?\b/, { "fiber-laser-cutting-machine": 10, "tube-laser-cutting-machine": 7, "sheet-and-tube-laser": 6, "large-format-plate-laser": 5, "coil-fed-laser-cutting-line": 4, "3d-laser-cutting-machine": 4 }],
    [/(tube|pipe|profile|beam) laser|laser (for |to cut )?(tube|pipe|profile|beam)/, { "tube-laser-cutting-machine": 15, "sheet-and-tube-laser": 9 }],
    [/sheet (and|&) tube|sheet\/tube|both sheet/, { "sheet-and-tube-laser": 15 }],
    [/laser (weld|clean|cladd)|welding laser|handheld laser/, { "laser-welding-machine": 15 }],
    [/coil[- ]fed|laser.*coil|coil.*laser|blanking line/, { "coil-fed-laser-cutting-line": 15 }],
    [/3d laser|five.?axis|5.?axis|robot laser|trim(ming)? (formed|pressed|hot)/, { "3d-laser-cutting-machine": 15 }],
    [/large (format|plate)|heavy plate laser|bevel(l?ing)? laser|laser.*bevel/, { "large-format-plate-laser": 13 }],
    [/plasma|water ?jet|oxy|flame cut/, { "fiber-laser-cutting-machine": 7, "large-format-plate-laser": 7 }],
    [/band ?saws?/, { "semi-automatic-band-saws": 8, "automatic-band-saws": 7, "affordable-semi-automatic-band-saws": 7, "double-column-band-saws": 6, "manual-band-saws": 5, "automatic-feed-band-saws": 6, "twin-column-band-saws": 5, "vertical-band-saws": 3 }],
    [/double.?column|twin.?column/, { "double-column-band-saws": 13, "twin-column-band-saws": 11 }],
    [/vertical (band ?)?saw|contour saw|plate saw/, { "vertical-band-saws": 14, "vertical-metal-band-saw": 12 }],
    [/cold saw|circular saw|circular cold|chop ?saw|friction saw|abrasive saw|cut.?off saw|\bhss saw|carbide saw|\btct\b/, { "cold-saws": 12, "automatic-cold-saws": 10 }],
    [/up.?cut|alumin(um|ium)? (profile|extrusion|window)s?|alumin(um|ium)? saw|pvc saw|double (head|miter) saw|window saw/, { "aluminum-and-pvc-upcut-saws": 15 }],
    [/\bsaws?\b|\bsawing\b/, { "semi-automatic-band-saws": 6, "automatic-band-saws": 5, "cold-saws": 5, "affordable-semi-automatic-band-saws": 5, "double-column-band-saws": 4, "manual-band-saws": 3 }],
    [/blades?\b.*(band|saw)|(band|saw) blades?|\bwikus/, { "band-saw-blades": 15 }],
    [/rebar|reinforc/, { "rebar-bender": 10, "rebar-cutter": 8, "automatic-rebar-processing-lines": 5 }],
    [/stirrup|rebar (line|processing)|automatic rebar|\bmesh\b|dowel|spiral bend/, { "automatic-rebar-processing-lines": 11, "rebar-bender": 9 }],
    [/hydraulic press|shop press|\bh.?frame|\bc.?frame|gap.?frame|deep.?draw|forging press|stamping press|four.?column press|4.?column press/, { "h-frame-hydraulic-press": 9, "hydraulic-shop-press": 9, "c-frame-hydraulic-press": 7, "hydraulic-straightening-press": 4 }],
    [/shop press|garage press|bearing press|bench press\b/, { "hydraulic-shop-press": 14 }],
    [/\bh.?frame|four.?column|4.?column|deep.?draw/, { "h-frame-hydraulic-press": 14 }],
    [/\bc.?frame|gap.?frame|single.?column press|open.?front/, { "c-frame-hydraulic-press": 14 }],
    [/straighten/, { "hydraulic-straightening-press": 15 }],
    [/rivet/, { "riveting-machine": 15 }],
    [/positioner|turntable|turn ?table|rotary table for weld/, { "welding-positioners": 15 }],
    [/turning roll|rotator|pipe roll(er)?s? for weld|tank (weld|roll)|vessel/, { "welding-turning-rolls": 15 }],
    [/column (and|&) boom|manipulator|welding boom/, { "column-and-boom-welding-manipulators": 15 }],
    [/welding table|fixture table|\bjig table|downdraft/, { "welding-tables": 15 }],
    [/\bweld/, { "welding-positioners": 7, "welding-turning-rolls": 7, "column-and-boom-welding-manipulators": 5, "welding-tables": 5, "laser-welding-machine": 5 }],
    [/(pvc|upvc|vinyl|window) weld/, { "pvc-window-welding-machines": 15 }],
    [/corner weld/, { "corner-welding-machines": 15 }],
    [/deburr|edge round|edge break|\bdross|\bslag|\bgrain(ing)?\b|wide.?belt|timesaver|sheet (sander|grinder)|plate (sander|grinder)/, { "sheet-metal-plate-deburring-edge-rounding-finishing-grinding": 15 }],
    [/belt grind|belt sander|knife|linisher|disc sander|bench grind|pedestal grind|\bgrinders?\b/, { "belt-grinder": 13 }],
    [/polish|pipe sand|tube sand|center.?less|mirror|satin finish|handrail (grind|finish)/, { "pipe-sanding-polishing-machines": 14 }],
    [/corner grind/, { "corner-grinding-machines": 15 }],
    [/tube end deburr|tube deburr|deburr (tube|pipe)|pipe (end )?deburr/, { "tube-end-deburring-machine": 15 }],
    [/surface grind/, { "surface-grinder": 15 }],
    [/bevel|chamfer|weld prep|edge prep/, { "plate-beveler": 14 }],
    [/\blathe|\bturning\b(?!\s*rolls?)|cnc turn/, { "cnc-lathe": 15 }],
    [/vmc|vertical machining|machining cent(er|re)/, { "vertical-machining-center": 15 }],
    [/\bmill(ing)?\b|knee mill|bridgeport|turret mill/, { "milling-machine": 13, "vertical-machining-center": 7 }],
    [/\bdrill|tapping machine|magnetic drill|mag drill/, { "drill-press": 14 }],
    [/window|\bpvc\b|upvc|vinyl|curtain wall|door profile/, { "pvc-window-welding-machines": 8, "window-production-lines": 7, "window-assembly-machines": 7, "profile-machining-centres-copy-routers": 6, "aluminum-and-pvc-upcut-saws": 6 }],
    [/copy rout|\brouter\b|lock slot|end mill(ing)? (machine|profile)|profile machining/, { "profile-machining-centres-copy-routers": 15 }],
    [/window (production )?line|production line for window/, { "window-production-lines": 15 }],
    [/corner clean|crimp|glazing bead|window assembl|mullion/, { "window-assembly-machines": 14 }],
    [/\bwood|planer|jointer|table saw|spindle moulder|thicknesser|panel saw/, { "woodworking-machinery": 15 }],
    [/american (style|tool)|amada|promecam/, { "american-style-press-brake-tooling": 15 }],
    [/\bwila|trumpf|new standard/, { "trumpf-wila-press-brake-tooling": 15 }],
    [/bystronic|\blvd\b/, { "bystronic-lvd-press-brake-tooling": 15 }],
    [/(press brake|brake) (tool|tooling|die|dies|punch|punches)|tooling|\bv.?dies?\b|gooseneck|\bdies?\b|\bpunches\b|euro(pean)? (style )?(tool|punch|die)/, { "european-press-brake-dies": 9, "european-press-brake-punches": 9, "american-style-press-brake-tooling": 7, "press-brake-tool-holders-adapters": 6 }],
    [/tool holder|clamp(ing)? (system|holder)|adapter|intermediate/, { "press-brake-tool-holders-adapters": 14 }],
    [/lock ?former|pittsburgh|button.?lock|snap.?lock|\bseam(er|ing)\b|\bduct/, { "lock-former": 14, "circle-cutters-and-seamers": 5 }],
    [/bead(ing)? roll|\bbeader|roto.?die|rotary machine|swag(e|ing) (machine|roll)/, { "bead-rollers": 15 }],
    [/circle (cut|shear)|disc (cut|blank)|circle cutter|round blank|flanging/, { "circle-cutters-and-seamers": 15 }],
    [/v.?groov/, { "v-grooving-machine": 15 }],
    [/wire bend|wire form|2d wire|3d wire/, { "wire-bending-machines": 15 }],
    [/railings?|handrails?|balustrade|\bgates?\b|fences?|ornamental|wrought iron/, { "angle-rolls": 11, "rotary-draw-tube-benders": 9, "pipe-notcher": 8, "pipe-sanding-polishing-machines": 7, "belt-grinder": 5 }],
    [/structural (steel|shop|fabricat)|steel fabricat|fabrication shop|beam (line|shop)/, { "ironworker-machines": 10, "double-column-band-saws": 8, "semi-automatic-band-saws": 7, "hydraulic-punching-machines": 7, "hydraulic-press-brake": 6 }]
  ];

  /* what the visitor wants, from the words of a question (and the previous question, for follow-ups) */
  function understand(q, prev) {
    var n = norm(q), req = { q: q, n: n, ops: {}, mats: [], qual: {}, pages: {}, nums: {} };
    OPS.forEach(function (o) { if (o[1].test(n)) req.ops[o[0]] = 1; });
    MATS.forEach(function (m) { if (m[1].test(n)) req.mats.push(m[0]); });
    if (req.mats.indexOf("rect_tube") >= 0 || req.mats.indexOf("sq_tube") >= 0) req.mats = req.mats.filter(function (m) { return m !== "tube" && m !== "pipe"; });
    if (req.mats.indexOf("rebar") >= 0) req.mats = req.mats.filter(function (m) { return m === "rebar"; });
    req.mat = req.mats[0] || null;
    // qualifiers
    var Q = [["cnc", /\bcnc\b/], ["nc", /\bnc\b/], ["auto", /\bauto(matic|mated|mation)?\b|production|high.?volume|unattended|bundle/], ["semi", /semi.?auto/],
      ["manual", /\bmanual|\bhand\b|gravity|by hand/], ["hydraulic", /hydraulic/], ["electric", /electric|servo/], ["mechanical", /mechanical/],
      ["premium", /premium|best|heavy.?duty|european|top quality|high.?end|dener|isitan|bekamak|\bgms\b|turkish|made in turkey/],
      ["value", /budget|cheap|affordable|low.?cost|value|econom|inexpensive|starter|hobby|small shop|entry/],
      ["small", /\bsmall|compact|portable|bench|mini|light(weight)?\b|table.?top/], ["heavy", /\bheavy|large|big|industrial|thick/],
      ["stainless", /stainless|\bss\b|\b304\b|\b316\b/], ["aluminum", /alumin/], ["single", /single.?phase|1.?phase|110 ?v|115 ?v|120 ?v|220 ?v|230 ?v/],
      ["miter", /mit(er|re)|\bangle cut|\bangles? of|\b45\s?(°|deg|degree)|\b60\s?(°|deg|degree)|swivel/]];
    Q.forEach(function (x) { if (x[1].test(n)) req.qual[x[0]] = 1; });
    if (req.qual.semi) delete req.qual.auto;
    // machine types named in the question
    TYPES.forEach(function (t) {
      if (t[0].test(n)) for (var p in t[1]) req.pages[p] = Math.max(req.pages[p] || 0, t[1][p]);
    });
    parseNumbers(req);
    inferPages(req);
    // a follow-up ("and 3 inch?", "cheaper one", "automatic?") keeps the subject of the previous question
    var named = Object.keys(req.pages).length > 0;
    if (prev && !named && !req.mat && (Object.keys(req.nums).length || Object.keys(req.qual).length || /^(and|what about|how about|also|same|other|another|cheaper|bigger|smaller|larger)\b|\d/.test(n.trim()))) {
      req.pages = prev.pages; req.mat = prev.mat; req.mats = prev.mats; req.ops = Object.keys(req.ops).length ? req.ops : prev.ops;
      if (!Object.keys(req.nums).length || /\d/.test(n)) { req.nums = {}; parseNumbers(req); }
      for (var k in prev.nums) if (!(k in req.nums)) req.nums[k] = prev.nums[k];
      req.followup = true;
    }
    return req;
  }

  /* sizes in the question → req.nums: size (section or tube OD), nps, thk, len, D (target diameter), clr, ton, kw, load, bar (mm),
     angle, bed [L, W], rect [W, H], hole */
  function parseNumbers(req) {
    var n = " " + req.n.replace(/\b(?:3|three)\s*-?\s*in\s*-?\s*(?:1|one)\b/g, " ").replace(/(\d)\s*(?:inches|inch|in\.|in\b|")/g, '$1" ').replace(/(\d)\s*(?:feet|foot|ft\b|')/g, "$1' ") + " ";
    var N = req.nums, m, re;
    // rebar sizes
    if ((m = /#\s?(\d{1,2})\b/.exec(n)) && US_BARS[m[1]]) N.bar = US_BARS[m[1]];
    if ((m = /\b(10|15|20|25|30|35|45|55)\s?m\b/.exec(n)) && (req.mat === "rebar" || /rebar|bar|bend|cut/.test(n))) N.bar = CA_BARS[m[1]];
    if (!N.bar && req.mat === "rebar" && (m = /(\d+(?:\.\d+)?)\s?mm/.exec(n))) N.bar = +m[1];
    // gauge
    if ((m = /\b(\d{1,2})\s?(?:ga|gauge|gage)\b/.exec(n)) && GA[m[1]]) N.thk = GA[m[1]];
    // tons, kW, lb, kg, degrees
    if ((m = /(\d+(?:\.\d+)?)\s?(?:us\s)?(?:tons?|tonnes?|t)\b(?!\s?(?:roll|pipe))/.exec(n))) N.ton = +m[1];
    if ((m = /(\d+(?:\.\d+)?)\s?kn\b/.exec(n))) N.ton = m[1] * 0.1124;
    if ((m = /(\d+(?:\.\d+)?)\s?kw\b/.exec(n))) N.kw = +m[1];
    if ((m = /(\d[\d,]*(?:\.\d+)?)\s?(?:lbs?|pounds?)\b/.exec(n))) N.load = +m[1].replace(/,/g, "");
    if ((m = /(\d[\d,]*(?:\.\d+)?)\s?kgs?\b/.exec(n))) N.load = m[1].replace(/,/g, "") * 2.2046;
    if (N.ton && (req.ops.weld || /positioner|turning roll|rotator|load|weigh|tank|vessel/.test(n))) { N.load = N.ton * 2000; delete N.ton; }
    if ((m = /\b(\d{2})\s?(?:°|deg\b|degrees?\b)/.exec(n))) N.angle = +m[1];
    // "4x8 sheet", "5 x 10 ft" → bed; "6x4 tube" → rect; "1/4 x 10'" → thickness × length; "2x2x1/4 angle"
    var used = [];
    re = new RegExp(NUMRX + "\\s?(\"|')?\\s?x\\s?" + NUMRX + "\\s?(\"|')?(?:\\s?x\\s?" + NUMRX + "\\s?(\"|')?)?", "g");
    while ((m = re.exec(n))) {
      used.push([m.index, m.index + m[0].length]);
      var a = val(m[1]), ua = m[2], b = val(m[3]), ub = m[4], c = m[5] ? val(m[5]) : null;
      var after = n.slice(m.index + m[0].length, m.index + m[0].length + 24);
      if (c != null && (req.mat === "angle" || req.mat === "channel" || req.mat === "tee" || req.mat === "rect_tube" || req.mat === "sq_tube")) {
        N.size = Math.max(a, b); N.size2 = Math.min(a, b); N.thk = N.thk || c; continue;
      }
      if ((ua === "'" || ub === "'" || /sheet|bed|table|plate size|work area/.test(after)) && a <= 30 && b <= 60 && a >= 2 && b >= 2 && !(a < 1 || b < 1)) {
        var L = Math.max(a, b) * 12, W = Math.min(a, b) * 12;
        if (ua === "'" && ub === "'") { N.bed = [L, W]; N.len = N.len || L; continue; }
        if (/sheet|bed|table|work area|plate size/.test(after) || (req.ops.laser || req.pages["fiber-laser-cutting-machine"])) { N.bed = [L, W]; continue; }
      }
      if (b >= 12 && a < 2 && (ub === "'" || ub === '"' || /ft|long|wide|length/.test(after))) { N.thk = N.thk || a; N.len = ub === "'" ? b * 12 : b; continue; }
      if (ub === "'" && a < 2) { N.thk = N.thk || a; N.len = b * 12; continue; }
      if (req.mat === "flat") { N.size = Math.max(a, b); N.size2 = Math.min(a, b); continue; }
      if (req.mat === "sq_tube" || req.mat === "rect_tube" || /tube|profile|square|rect|bar|beam|channel|angle/.test(after) || req.ops.cut) {
        N.rect = [Math.max(a, b), Math.min(a, b)]; N.size = N.size || Math.max(a, b); N.size2 = Math.min(a, b);
        if (a === b && !req.mat) req.mat = "sq_tube";
        continue;
      }
    }
    // quantities with a unit
    var q = [];
    re = new RegExp(NUMRX + "\\s?(\"|'|mm\\b|cm\\b|m\\b|meters?\\b)", "g");
    while ((m = re.exec(n))) {
      var v = val(m[1]), u = m[2];
      if (u === "'") v *= 12; else if (u === "mm") v /= 25.4; else if (u === "cm") v /= 2.54; else if (u[0] === "m") { if (req.mat === "rebar") continue; v *= 39.37; }
      q.push({ v: v, at: m.index, end: m.index + m[0].length, unit: u });
    }
    // bare numbers before a material word ("2 pipe", "1/4 plate") count as inches
    re = new RegExp("(?:^|\\s)" + NUMRX + "\\s+(?:dia(?:meter)?\\s+)?(pipe|tube|tubing|plate|sheet|bar|rod|angle|channel|flat|round|square|od|thick|nps|sch)", "g");
    while ((m = re.exec(n))) {
      var at = m.index + m[0].indexOf(m[1]);
      if (!q.some(function (x) { return Math.abs(x.at - at) < 3; })) q.push({ v: val(m[1]), at: at, end: at + m[1].length, unit: "", bare: true });
    }
    // bare number after "diameter"/"radius"/"to a" ("into a 30 diameter ring", "radius 15")
    re = new RegExp("(dia(?:meter)?|radius|clr|od|ring|circle|arc|to(?: a| an)?|into(?: a| an)?)\\s+(?:of\\s+)?" + NUMRX + "(?!\\s?(?:\"|'|mm|cm|m\\b|x|ga|ton|kw|lb|kg|deg|°|%))", "g");
    while ((m = re.exec(n))) {
      var at2 = m.index + m[0].lastIndexOf(m[2]);
      if (!q.some(function (x) { return Math.abs(x.at - at2) < 3; }) && /dia|radius|clr|od|ring|circle|arc/.test(m[1] + n.slice(at2, at2 + 25))) q.push({ v: val(m[2]), at: at2, end: at2 + m[2].length, unit: "", bare: true });
    }
    re = new RegExp("(?:^|[\\s,(])(\\d+\\/\\d+|0?\\.\\d+)(?![\\d/\"'.]|\\s?(?:mm|cm|ga|x\\b))", "g");
    while ((m = re.exec(n))) {
      var at3 = m.index + m[0].indexOf(m[1]);
      if (!q.some(function (x) { return Math.abs(x.at - at3) < 3; }) && !/x\s*$/.test(n.slice(Math.max(0, at3 - 4), at3)) && !/^\s*x/.test(n.slice(at3 + m[1].length)))
        q.push({ v: val(m[1]), at: at3, end: at3 + m[1].length, unit: "", bare: true, frac: true });
    }
    q.sort(function (a, b) { return a.at - b.at; });
    q.forEach(function (x) {
      var before = n.slice(Math.max(0, x.at - 26), x.at), after = n.slice(x.end, x.end + 30);
      var aft = after.replace(/^\s*(dia(meter)?\s+)?/, "");
      if (used.some(function (u) { return x.at >= u[0] && x.at < u[1]; })) return;   // part of an A x B group, read above
      if (/radius|\bclr\b|\br\s*$/.test(before + " " + after.slice(0, 8)) && !/dia/.test(after.slice(0, 10))) { N.radius = x.v; return; }
      var dirDia = /^\s*(dia(meter)?|ring|circle|arc|hoop|radius)\b/.test(after) || x.unit !== "'" && /^\s*(cylinders?|tanks?|shells?|cones?)\b/.test(after),
        dirSize = /^\s*(dia(meter)?|od|o\.d\.)\s+(pipe|tube|tubing|bar|rod|round|solid|shaft)/.test(after) || /^\s*(dia(meter)?)\s+(of\s+)?\.?\d/.test(after);
      var rollCtx = req.ops.roll || req.ops.bend || /cylinder|tank|shell|ring|circle|arc/.test(req.n);
      if (dirSize && /^\s*(dia(meter)?)\s+(of\s+)?\.?\d/.test(after)) { N.size = N.size || x.v; if (req.mat === "pipe" && !N.nps) { N.nps = x.v; N.size = npsOd(x.v) || x.v; } return; }
      if (!dirSize && (dirDia && (rollCtx || /\b(to|into|a|an|of|make|min|minimum)\s*$/.test(before + " ") || N.size) ||
          /(dia(meter)?|\bod)\s*(of\s*)?$/.test(before) && (rollCtx || /\b(to|into|ring|circle|roll|bend|curve)\b/.test(before + " ")))) {
        if (/^\s*radius/.test(after)) N.radius = x.v; else N.D = x.v;
        return;
      }
      if (/^\s*(dia(meter)?\s+)?(pipe|nps|sch)/.test(after) || /nps\s*$/.test(before)) { N.nps = x.v; N.size = npsOd(x.v) || x.v; if (!req.mat) req.mat = "pipe"; return; }
      if (/^\s*(dia(meter)?\s+|od\s+|o\.d\.\s+)?(round )?(tube|tubing)/.test(after)) { N.size = x.v; if (!req.mat) req.mat = "tube"; return; }
      if (/^\s*(dia(meter)?\s+)?(round |solid )?(bar|rod|shaft|stock)/.test(after) || /^\s*(dia(meter)?\s+)?round\b/.test(after)) { N.size = x.v; if (!req.mat || req.mat === "profile") req.mat = req.mat || "rd_bar"; return; }
      if (/^\s*(dia(meter)?)\b/.test(after) && !N.size && (req.ops.cut || req.mats.length)) { N.size = x.v; return; }
      if (/^\s*(thick|plate|sheet|wall|ga\b|mild|steel|stainless|alumin|ms\b|carbon)/.test(after) || /thick(ness)?\s*(of\s*)?$/.test(before)) {
        if (/^\s*wall/.test(after) || /wall\s*$/.test(before)) N.wall = x.v; else if (x.v < 6) N.thk = N.thk || x.v;
        return;
      }
      if (/^\s*(long|length|wide|width|bed|table|working)/.test(after) || /(length|width|long|wide|up to)\s*(of\s*)?$/.test(before) || (x.unit === "'" && x.v >= 24)) {
        N.len = Math.max(N.len || 0, x.v); return;
      }
      if (/(hole|punch)/.test(after.slice(0, 12)) || /(hole|punch)\s*(of\s*)?$/.test(before)) { N.hole = x.v; return; }
      if (/^\s*(angle|channel|beam|tee|flat|square|rect)/.test(aft) && !N.size) { N.size = x.v; return; }
      if (/(drill|tap)/.test(before + after)) { N.hole = x.v; return; }
      // still unassigned: a long number is a length, a small one a size
      if (!N.size && x.v <= 24 && (req.mat && LONG[req.mat] || req.ops.cut)) { N.size = x.v; if (req.mat === "pipe" && x.unit === '"') { N.nps = x.v; N.size = npsOd(x.v) || x.v; } return; }
      if (!N.thk && x.v < 2 && (req.mat === "plate" || req.mat === "sheet" || req.ops.shear || sheetCtx(req))) { N.thk = x.v; return; }
      if (x.v >= 24 && !N.len) { N.len = x.v; return; }
      if (!N.D && x.v >= 6 && (req.ops.roll || req.ops.bend) && N.size) { N.D = x.v; return; }
      if (!N.size) N.size = x.v;
    });
    if (N.radius && !N.D && (req.ops.roll || N.radius > 10)) N.D = N.radius * 2;
    // a pipe size typed in inches is the nominal size (NPS): 2″ pipe = 2-3/8″ OD
    if (req.mat === "pipe" && N.size && !N.nps && N.size <= 24 && !/\bod\b|o\.d\./.test(n)) { N.nps = N.size; N.size = npsOd(N.size) || N.size; }
  }

  function sheetCtx(req) {
    var P = req.pages || {};
    return !!(P["hydraulic-press-brake"] || P["hydraulic-shearing-machine"] || P["hydraulic-3-roll-plate-rollers"] || P["electric-press-brake"] || P["mechanical-guillotine-shear"] ||
      P["box-and-pan-brake"] || P["sheet-metal-hand-brake"] || P["hydraulic-folding-machine"] || P["panel-bender"] || P["motorized-plate-rollers"] || P["hydraulic-4-roll-plate-rollers"] ||
      req.ops.bend && !req.mat || req.ops.roll && !req.mat);
  }
  /* every kind of machine that bends sheet: a job given with sizes is answered with all of them (the owner, Nov 7 2026: "a 10 ft
     22 ga bending brake" is a press brake, a hydraulic folder, a box and pan brake, a hand brake…), the smallest first */
  var BEND_SHEET = { "hydraulic-press-brake": 11, "electric-press-brake": 8, "compact-hydraulic-press-brakes": 7, "hydraulic-folding-machine": 8,
    "box-and-pan-brake": 7, "sheet-metal-hand-brake": 6, "magnetic-sheet-metal-brake": 6, "roofing-siding-brake": 5, "shear-brake-roll-3-in-1": 5, "panel-bender": 5 };
  function allBendSheet(P, floor) {
    for (var p in BEND_SHEET) P[p] = Math.max(P[p] || 0, Math.max(BEND_SHEET[p], floor || 0));
  }
  /* machine types from the job (operation + material) when the question names no machine */
  function inferPages(req) {
    var P = req.pages, o = req.ops, mat = req.mat, long = mat && LONG[mat], N = req.nums;
    function add(p, w) { P[p] = Math.max(P[p] || 0, w); }
    if (P["pipe-notcher"] >= 15) delete P["corner-notcher"];
    var named = Object.keys(P).length;
    // a sheet-bending job with sizes, whatever kind of brake was named: every kind that bends sheet joins the list
    var maxW = 0;
    for (var k in P) if (P[k] > maxW) maxW = P[k];
    // (a 3-in-1 or a panel bender named by the visitor is a specific kind — only the brakes and folders open the whole list)
    var bendNamed = Object.keys(P).some(function (p) { return BEND_SHEET[p] && p !== "shear-brake-roll-3-in-1" && p !== "panel-bender" && P[p] >= maxW * 0.7; }) &&
      !(o.shear || o.cut || o.roll || o.punch || o.notch);
    if ((N.thk || N.len) && !long && mat !== "rebar" && (bendNamed || (o.bend && !named && (mat === "sheet" || mat === "plate" || !mat)))) {
      allBendSheet(P, bendNamed ? maxW * 0.45 : 0);
      if (bendNamed) return;
    }
    if (mat === "rebar") {
      if (o.cut && !o.bend) add("rebar-cutter", 14); else if (o.bend && !o.cut) add("rebar-bender", 14);
      else { add("rebar-bender", 10); add("rebar-cutter", 9); }
      if (req.qual.auto || /stirrup/.test(req.n)) add("automatic-rebar-processing-lines", 12);
      return;
    }
    // bending a pipe to a large diameter is roll bending (a section bender), not draw bending
    var D = N.D || (N.radius ? N.radius * 2 : null);
    if ((o.roll || o.bend) && long && (o.roll || (D && D / 2 > Math.max(10, 4 * (N.size || 1))))) {
      add("angle-rolls", 15);
      if (P["rotary-draw-tube-benders"]) P["rotary-draw-tube-benders"] = Math.min(P["rotary-draw-tube-benders"], 6);
      if (P["hydraulic-3-roll-plate-rollers"] && !/plate|sheet/.test(req.n)) { delete P["hydraulic-3-roll-plate-rollers"]; delete P["hydraulic-4-roll-plate-rollers"]; delete P["motorized-plate-rollers"]; }
      return;
    }
    if (named) {
      if (o.cut && long && P["fiber-laser-cutting-machine"] && !P["tube-laser-cutting-machine"]) add("tube-laser-cutting-machine", 12);
      if (o.punch && (o.cut || o.shear) && long) add("ironworker-machines", 15);
      return;
    }
    if (o.roll && (mat === "plate" || mat === "sheet" || N.thk) || /cylinder|cone|tank shell/.test(req.n)) {
      add("hydraulic-3-roll-plate-rollers", 11); add("hydraulic-4-roll-plate-rollers", 10); add("motorized-plate-rollers", 10); add("shear-brake-roll-3-in-1", 4); return;
    }
    if (o.bend && (mat === "pipe" || mat === "tube" || mat === "sq_tube" || mat === "rect_tube")) {
      add("rotary-draw-tube-benders", 11); add("nc-tube-benders", 10); add("cnc-tube-benders", 9); if (req.qual.cnc) add("cnc-tube-benders", 14); if (req.qual.nc) add("nc-tube-benders", 14); return;
    }
    if (o.bend && (mat === "flat" || mat === "angle" || mat === "rd_bar" || mat === "sq_bar")) { add("horizontal-press-brake", 10); add("angle-rolls", 8); add("ironworker-machines", 4); return; }
    if (o.bend && (mat === "sheet" || mat === "plate" || N.thk || !mat)) {
      add("hydraulic-press-brake", 11); add("electric-press-brake", 8); add("compact-hydraulic-press-brakes", 7);
      if (mat === "sheet" || (N.thk && N.thk < 0.08) || N.len) allBendSheet(P);
      return;
    }
    if (o.shear) { add("hydraulic-shearing-machine", 11); add("mechanical-guillotine-shear", 9); if (long) add("ironworker-machines", 9); return; }
    if (o.cut && (mat === "sheet" || mat === "plate" || mat === "coil")) {
      add("hydraulic-shearing-machine", 10); add("fiber-laser-cutting-machine", 9); add("mechanical-guillotine-shear", 7);
      if (/circle|disc|round blank/.test(req.n)) add("circle-cutters-and-seamers", 13);
      return;
    }
    if (o.punch && (o.cut || o.shear || o.notch) && (long || mat === "plate")) { add("ironworker-machines", 15); add("hydraulic-punching-machines", 10); return; }
    if (o.cut && (long || N.rect || N.size)) {
      if (mat === "wood") { add("woodworking-machinery", 14); return; }
      if (mat === "pvc" || req.qual.aluminum && mat === "profile") { add("aluminum-and-pvc-upcut-saws", 14); return; }
      add("semi-automatic-band-saws", 10); add("automatic-band-saws", 9); add("affordable-semi-automatic-band-saws", 8); add("double-column-band-saws", 7);
      add("cold-saws", 8); add("automatic-cold-saws", 6); add("manual-band-saws", 5); add("automatic-feed-band-saws", 6); add("twin-column-band-saws", 5);
      if (mat === "tube" || mat === "pipe" || mat === "sq_tube" || mat === "rect_tube") add("tube-laser-cutting-machine", 5);
      return;
    }
    if (o.punch || N.hole) { add("hydraulic-punching-machines", 11); add("ironworker-machines", 11); if (o.drill) add("drill-press", 10); return; }
    if (o.notch) { if (mat === "pipe" || mat === "tube") add("pipe-notcher", 14); else { add("corner-notcher", 11); add("ironworker-machines", 7); } return; }
    if (o.weld) {
      if (mat === "pipe" || mat === "tube" || /tank|vessel|cylind/.test(req.n)) { add("welding-turning-rolls", 13); add("welding-positioners", 9); add("column-and-boom-welding-manipulators", 8); }
      else { add("welding-positioners", 10); add("welding-tables", 8); add("welding-turning-rolls", 7); add("laser-welding-machine", 6); }
      return;
    }
    if (o.grind) {
      if (mat === "pipe" || mat === "tube" || mat === "rd_bar") { add("pipe-sanding-polishing-machines", 13); add("tube-end-deburring-machine", 7); add("belt-grinder", 6); }
      else if (mat === "sheet" || mat === "plate") add("sheet-metal-plate-deburring-edge-rounding-finishing-grinding", 14);
      else { add("belt-grinder", 10); add("sheet-metal-plate-deburring-edge-rounding-finishing-grinding", 9); add("pipe-sanding-polishing-machines", 7); }
      return;
    }
    if (o.bevel) { add("plate-beveler", 14); return; }
    if (o.drill) { add("drill-press", 14); add("milling-machine", 6); return; }
    if (o.mill) { add("milling-machine", 13); add("vertical-machining-center", 11); return; }
    if (o.turn) { add("cnc-lathe", 14); return; }
    if (o.press) { add("h-frame-hydraulic-press", 10); add("hydraulic-shop-press", 10); add("c-frame-hydraulic-press", 8); return; }
    if (o.endform) { add("tube-end-forming-machines", 14); return; }
    if (o.laser) { add("fiber-laser-cutting-machine", 10); return; }
    if (o.roll) { add("hydraulic-3-roll-plate-rollers", 9); add("motorized-plate-rollers", 8); add("angle-rolls", 8); }
  }

  /* ======================================================================================== the index */
  var DATA = null, FAM = [], FAMBYID = {}, PAGES = [], BYPAGE = {}, DF = {}, NDOC = 0, VOCAB = [], AVG = {}, MODELS = [];
  var FW = { name: 4, cat: 3, head: 2, body: 1.2, spec: 0.8, page: 0.5, pdf: 0.35 };

  function tf(list) { var o = {}; list.forEach(function (t) { o[t] = (o[t] || 0) + 1; }); return o; }
  function specText(f) {
    var s = [];
    (f.specs || []).forEach(function (t) { s.push(t.title); t.rows.forEach(function (r) { s.push(r.join(" ")); }); });
    f.models.forEach(function (m) { for (var k in m) if (k !== "name") s.push(k.replace(/_/g, " ") + " " + m[k]); });
    return s.join(" ");
  }
  function init(data) {
    DATA = data; FAM = data.families || []; PAGES = data.pages || [];
    var pageInfo = {};
    PAGES.forEach(function (p) { pageInfo[p.slug] = p; });
    BYPAGE = {}; DF = {}; MODELS = [];
    var sums = {}, pdfTerms = {};
    FAM.forEach(function (f, i) {
      var p = pageInfo[f.page] || {};
      f._i = i;
      f._p = p;
      if (!p._terms) p._terms = terms([p.nav, p.h1, p.intro].concat(p.points || []).join(" "), true);
      if (f.pdf && data.pdfs && !pdfTerms[f.pdf]) pdfTerms[f.pdf] = terms(data.pdfs[f.pdf] || "", true);
      var fields = {
        name: terms([f.name, f.short, f.models_label].concat(f.models.map(function (m) { return m.name; })).join(" "), true),
        cat: terms([f.category, f.page_title, f.page_nav, f.brand, f.line].join(" "), true),
        head: terms(f.headline || "", true),
        body: terms([f.summary].concat(f.features, f.optional || []).join(" "), true),
        spec: terms(specText(f), true),
        page: p._terms || [],
        pdf: f.pdf ? (pdfTerms[f.pdf] || []) : []
      };
      f._tf = {}; f._len = {};
      var seen = {};
      for (var k in fields) {
        f._tf[k] = tf(fields[k]); f._len[k] = fields[k].length; sums[k] = (sums[k] || 0) + fields[k].length;
        for (var t in f._tf[k]) seen[t] = 1;
      }
      for (var t2 in seen) DF[t2] = (DF[t2] || 0) + 1;
      (BYPAGE[f.page] = BYPAGE[f.page] || []).push(f);
      f.models.forEach(function (m, mi) {
        var c = compact(m.name);
        if (c.length >= 3) MODELS.push({ key: c, f: f, mi: mi });
        var base = c.replace(/(\d)[a-z]{1,3}$/, "$1");     // 'mg20b' also as 'mg20'
        if (base !== c && base.length >= 3) MODELS.push({ key: base, f: f, mi: mi, loose: true });
      });
      f._caps = f.caps || [];
      FAMBYID[f.id] = f;
    });
    NDOC = FAM.length;
    for (var k2 in sums) AVG[k2] = sums[k2] / Math.max(1, NDOC);
    VOCAB = Object.keys(DF);
    PAGES.forEach(function (p) {
      p._q = (p.faq || []).map(function (qa) { return tf(terms(qa[0], true)); });
      p._a = (p.faq || []).map(function (qa) { return tf(terms(qa[0] + " " + qa[1], true)); });
      p._t = tf(terms([p.nav, p.h1, p.desc].join(" "), true));
    });
  }
  function idf(t) { var df = DF[t] || 0; return Math.log(1 + (NDOC - df + 0.5) / (df + 0.5)); }

  /* query terms with weights: the words themselves, a few synonyms, and the closest catalogue word for a typo */
  var SYN = { shear: ["guillotin"], guillotin: ["shear"], pip: ["tub"], tub: ["pip"], notch: ["cop"], bevel: ["chamf"], chamf: ["bevel"],
    deburr: ["edg", "round"], polish: ["sand", "finish"], sand: ["polish"], rebar: ["bar", "reinforc"], positioner: ["turntabl"], turntabl: ["position"],
    fold: ["brak", "folder"], brak: ["fold"], ironwork: ["punch", "shear"], cnc: ["nc"], automat: ["auto"], auto: ["automat"], stainless: ["inox"],
    alumin: ["aluminum"], miter: ["angl", "swivel"], roll: ["roller"], bend: ["bender"], cylind: ["roll"] };
  function editDist(a, b, max) {
    if (Math.abs(a.length - b.length) > max) return max + 1;
    var prev2 = null, prev = [], cur, i, j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur = [i]; var best = i;
      for (j = 1; j <= b.length; j++) {
        var c = a[i - 1] === b[j - 1] ? 0 : 1;
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + c);
        if (prev2 && i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) cur[j] = Math.min(cur[j], prev2[j - 2] + 1);
        if (cur[j] < best) best = cur[j];
      }
      if (best > max) return max + 1;
      prev2 = prev; prev = cur;
    }
    return prev[b.length];
  }
  var LOW = {}, QSTOP = {};
  "pip tub tubing plat sheet bar angl channel beam flat rod steel metal mild carbon round squar rectangular stock profil".split(" ").forEach(function (w) { LOW[w] = 1; });
  "inch in ft feet foot mm cm deg degre dia diamet thick thick long wid length width siz ton kw lb kg od nps sch schedul gaug ga x".split(" ").forEach(function (w) { QSTOP[w] = 1; });
  function queryTerms(n) {
    var out = {}, list = terms(n);
    var raw = n.split(/[^a-z0-9]+/).filter(Boolean);
    for (var i = 0; i + 1 < raw.length; i++) {
      if (/^\d+$/.test(raw[i]) && /^[a-z]{2,}$/.test(raw[i + 1])) { var j = raw[i] + stem(raw[i + 1]), j2 = raw[i] + raw[i + 1]; if (DF[j2]) out[j2] = 1.2; else if (DF[j]) out[j] = 1.2; }
    }
    list.forEach(function (t) {
      if (/^\d+(\.\d+)?$/.test(t) || QSTOP[t]) return;          // plain numbers are sizes, not words
      if (DF[t]) out[t] = Math.max(out[t] || 0, LOW[t] ? 0.35 : 1);
      else if (t.length >= 4 && !/\d/.test(t)) {
        var max = t.length >= 8 ? 2 : 1, best = null, bd = 9;
        for (var i = 0; i < VOCAB.length; i++) {
          var v = VOCAB[i];
          if (Math.abs(v.length - t.length) > max || v[0] !== t[0] && max < 2) continue;
          var dd = editDist(t, v, max);
          if (dd <= max && (dd < bd || (dd === bd && DF[v] > DF[best]))) { best = v; bd = dd; }
        }
        if (best) out[best] = Math.max(out[best] || 0, 0.8);
      } else if (/\d/.test(t) && DF[t]) out[t] = 1;
      (SYN[t] || []).forEach(function (s) { if (DF[s]) out[s] = Math.max(out[s] || 0, 0.5); });
    });
    return out;
  }
  function textScore(f, qt) {
    var s = 0, want = 0, got = 0;
    for (var t in qt) {
      var w = qt[t] * idf(t), best = 0;
      if (qt[t] >= 0.8) want++;
      for (var k in FW) {
        var c = f._tf[k][t];
        if (!c) continue;
        if (qt[t] >= 0.8 && !best) got++;
        var norm_ = 1 - 0.5 + 0.5 * (f._len[k] / (AVG[k] || 1));
        best += FW[k] * (c * 2.2) / (c + 1.2 * norm_);
      }
      s += w * best;
    }
    f._cov = want ? got / want : 0;
    return s * (0.35 + 0.65 * f._cov) + (want >= 2 && got === want ? 3 : 0);   // every word of the question found counts more than many hits on one word
  }

  /* ======================================================================================== capacities */
  var PRESS_BRAKES = { "hydraulic-press-brake": 1, "electric-press-brake": 1, "compact-hydraulic-press-brakes": 1 };
  var SAWS = { "manual-band-saws": 1, "semi-automatic-band-saws": 1, "affordable-semi-automatic-band-saws": 1, "automatic-band-saws": 1, "automatic-feed-band-saws": 1,
    "double-column-band-saws": 1, "twin-column-band-saws": 1, "vertical-band-saws": 1, "vertical-metal-band-saw": 1, "cold-saws": 1, "automatic-cold-saws": 1, "aluminum-and-pvc-upcut-saws": 1 };
  var TUBE_BENDERS = { "rotary-draw-tube-benders": 1, "nc-tube-benders": 1, "cnc-tube-benders": 1 };
  var SHEET_THK = { "hydraulic-shearing-machine": 1, "mechanical-guillotine-shear": 1, "hydraulic-3-roll-plate-rollers": 1, "hydraulic-4-roll-plate-rollers": 1,
    "motorized-plate-rollers": 1, "shear-brake-roll-3-in-1": 1, "panel-bender": 1, "hydraulic-folding-machine": 1, "box-and-pan-brake": 1, "sheet-metal-hand-brake": 1,
    "magnetic-sheet-metal-brake": 1, "roofing-siding-brake": 1, "v-grooving-machine": 1, "plate-beveler": 1, "corner-notcher": 1, "circle-cutters-and-seamers": 1,
    "bead-rollers": 1, "lock-former": 1, "sheet-metal-plate-deburring-edge-rounding-finishing-grinding": 1 };
  var PROF = { pipe: ["pipe", "rd_tube"], tube: ["rd_tube", "pipe"], sq_tube: ["sq_tube"], rect_tube: ["rect_tube"], flat: ["flat_easy", "flat_hard"],
    angle: ["angle_out", "angle_in"], channel: ["channel"], beam: ["beam"], tee: ["tee"], rd_bar: ["rd_bar"], sq_bar: ["sq_bar"] };
  var PROF_NAME = { pipe: "pipe", rd_tube: "round tube", sq_tube: "square tube", rect_tube: "rectangular tube", flat_easy: "flat bar (the easy way)",
    flat_hard: "flat bar (on edge)", angle_out: "angle (leg out)", angle_in: "angle (leg in)", channel: "channel", beam: "beams", tee: "tee", rd_bar: "round bar", sq_bar: "square bar" };

  function sizeOf(p) { return Array.isArray(p[0]) ? p[0][0] : p[0]; }
  /* minimum rolling diameter for a section of size s, interpolated between the chart's points (largest first) */
  function minDiameter(pts, s) {
    if (!pts || !pts.length) return null;
    var big = pts[0];
    if (s > sizeOf(big) * 1.001) return null;
    for (var i = 0; i < pts.length - 1; i++) {
      var a = pts[i], b = pts[i + 1], sa = sizeOf(a), sb = sizeOf(b);
      if (s <= sa && s >= sb) return sa === sb ? Math.min(a[1], b[1]) : b[1] + (a[1] - b[1]) * (s - sb) / (sa - sb);
    }
    return pts[pts.length - 1][1];
  }

  /* how well one model fits the request: {ok: true|false|null, score, notes: ["Rolls NPS 2 pipe to about Ø24″ minimum"], ratio} */
  function fitModel(f, mi, req) {
    var c = (f._caps || [])[mi] || {}, N = req.nums, notes = [], ok = null, ratio = null, checks = 0, fails = 0, warn = [], caution = [];
    var rs = [];
    function pass(cond, note, r) { checks++; if (cond) { if (note) notes.push(note); if (r != null) rs.push(Math.min(1.05, r)); } else { fails++; if (note) warn.push(note); } }
    var page = f.page;
    // section benders
    if (c.sec && (N.size || N.D) && req.mat && PROF[req.mat]) {
      var keys = PROF[req.mat].filter(function (k) { return c.sec[k]; });
      if (req.mat === "pipe" && keys[0] === "rd_tube") keys = [];     // schedule 40 pipe is heavier than the thin-wall tube of a tube-only chart: unknown, not a fit
      if (/hard way|on edge|edgewise/.test(req.n)) keys = keys.filter(function (k) { return k !== "flat_easy"; }).concat(keys.indexOf("flat_easy") >= 0 ? [] : []);
      if (keys.length) {
        var k = keys[0], pts = c.sec[k], s = N.size;
        if (k === "rd_tube" && req.mat === "pipe" && N.size) s = N.size;           // OD either way
        var maxS = sizeOf(pts[0]);
        if (s) {
          var tq = req.mat === "flat" ? N.size2 : N.thk;
          if (Array.isArray(pts[0][0]) && tq && pts[0][0][1] && tq > pts[0][0][1] * 1.03) { pass(false, "thicker than the " + PROF_NAME[k] + " capacity (" + fmtIn(pts[0][0][1]) + ")"); }
          else if (s > maxS * 1.001) pass(false, PROF_NAME[k] + " capacity is " + (k === "pipe" ? "NPS " + npsLabel(maxS) : fmtIn(maxS)) + " — smaller than " + sizeLabel(req));
          else {
            var md = minDiameter(pts, s);
            if (N.D) {
              pass(md != null && md <= N.D * 1.02, md != null ? "rolls " + sizeLabel(req) + " " + PROF_NAME[k] + " down to about Ø" + Math.round(md) + "″, so a Ø" + fmtNum(N.D) + "″ ring is within its range" : null, s / maxS);
            } else pass(true, "rolls " + PROF_NAME[k] + " up to " + (k === "pipe" ? "NPS " + npsLabel(maxS) : fmtIn(maxS)) + (md ? " (about Ø" + Math.round(md) + "″ minimum at your size)" : ""), s / maxS);
          }
        }
      }
    }
    if (page === "angle-rolls" && !c.sec && (c.od || c.nps_od) && N.size && (req.mat === "pipe" || req.mat === "tube")) {
      var capT = req.mat === "pipe" ? c.nps_od : c.od;
      if (capT) pass(N.size <= capT * 1.01, (req.mat === "pipe" ? "rolls pipe up to NPS " + npsLabel(capT) : "rolls tube up to Ø" + fmtIn(capT)), N.size / capT);
    }
    // tube and pipe benders
    if (TUBE_BENDERS[page] || page === "pipe-notcher" || page === "tube-end-forming-machines" || page === "tube-laser-cutting-machine" || page === "sheet-and-tube-laser" ||
        page === "pipe-sanding-polishing-machines" || page === "tube-end-deburring-machine") {
      var od = N.size;
      if (od && (c.od || c.nps_od)) {
        var cap = req.mat === "pipe" ? Math.max(c.nps_od || 0, c.od || 0) : (c.od || c.nps_od);
        pass(od <= cap * 1.01, (page === "tube-laser-cutting-machine" || page === "sheet-and-tube-laser" ? "tube up to Ø" : "tube up to Ø") + fmtIn(cap) + (c.nps_od && req.mat === "pipe" ? " (pipe to NPS " + npsLabel(c.nps_od) + ")" : ""), od / cap);
      }
      var R = N.radius || (N.D ? N.D / 2 : null);
      if (R && c.clr && TUBE_BENDERS[page]) {
        pass((!c.clr[1] || R <= c.clr[1] * 1.02) && (!c.clr[0] || R >= c.clr[0] * 0.98), "bending radius (CLR) " + (c.clr[0] ? fmtIn(c.clr[0]) + " – " : "up to ") + fmtIn(c.clr[1]));
      }
      if (N.wall && c.wall) pass(N.wall <= c.wall * 1.02, "wall up to " + fmtIn(c.wall));
    }
    // sheet and plate machines: thickness and working length
    var thkCap = req.qual.stainless && c.thk_ss ? c.thk_ss : req.qual.aluminum && c.thk_al ? c.thk_al : c.thk;
    if (N.thk && thkCap && (SHEET_THK[page] || PRESS_BRAKES[page] && !c.ton)) pass(N.thk <= thkCap * 1.07, fmtThk(thkCap) + (req.qual.stainless && c.thk_ss ? " stainless" : req.qual.aluminum && c.thk_al ? " aluminum" : " mild steel") + " capacity", N.thk / thkCap);
    if (N.len && c.len && (SHEET_THK[page] || PRESS_BRAKES[page] || page === "horizontal-press-brake")) pass(N.len <= c.len * 1.01, fmtLen(c.len) + (PRESS_BRAKES[page] ? " bending length" : " working length"), N.len / c.len);
    if (N.D && c.min_d && !c.sec) pass(c.min_d <= N.D * 1.02, "rolls down to Ø" + fmtIn(c.min_d));
    // press brakes: the force a bend needs (air bending, die opening 8 × thickness): 575 × t² / V US tons per foot
    if (PRESS_BRAKES[page] && c.ton) {
      if (N.ton) pass(c.ton >= N.ton * 0.98, Math.round(c.ton) + " US tons", N.ton / c.ton);
      else if (N.thk) {
        var t = N.thk, V = Math.max(8 * t, 0.25), perFt = 575 * t * t / V * (req.qual.stainless ? 1.5 : req.qual.aluminum ? 0.5 : 1);
        var need = perFt * Math.max(1, (N.len || c.len || 48) / 12);
        req.need = { tons: need, perFt: perFt, len: N.len };
        pass(c.ton >= need * 0.98, Math.round(c.ton) + " US tons (your bend needs about " + Math.round(need) + ")", need / c.ton);
      }
    } else if (N.ton && c.ton) pass(c.ton >= N.ton * 0.98, Math.round(c.ton) + " US tons", N.ton / c.ton);
    // saws
    if (SAWS[page]) {
      if (N.rect && c.rect) pass(N.rect[0] <= c.rect[0] * 1.01 && N.rect[1] <= c.rect[1] * 1.01, "cuts " + fmtIn(c.rect[0]) + " × " + fmtIn(c.rect[1]) + " at 90°", Math.max(N.rect[0] / c.rect[0], N.rect[1] / c.rect[1]));
      else if (N.size && (c.rnd || c.rect)) {
        var sq = req.mat === "sq_tube" || req.mat === "sq_bar" || /square/.test(req.n);
        var capR = sq && c.rect ? c.rect[1] : (c.rnd || (c.rect ? c.rect[1] : 0));
        pass(N.size <= capR * 1.01, (sq ? "square " : "round ") + fmtIn(capR) + " at 90°", N.size / capR);
      }
      if (N.angle && N.angle !== 90 && c.miter) pass(c.miter.indexOf(N.angle) >= 0 || c.miter.some(function (a) { return a >= N.angle; }), "miter cuts to " + Math.max.apply(null, c.miter) + "°");
      else if ((N.angle && N.angle !== 90 || req.qual.miter) && SAWS[page] && !c.miter && page !== "cold-saws" && page !== "aluminum-and-pvc-upcut-saws" && c.rnd) pass(false, "cuts at 90° only");
    }
    // ironworkers and punching machines
    if (c.punch && (N.hole || N.thk && (req.ops.punch || page === "ironworker-machines"))) {
      // the punching force grows with hole Ø × thickness: the thickest plate this machine punches at the visitor's hole size
      var h = N.hole || 0.75, th = N.thk || 0.25;
      var pmax = Math.max.apply(null, c.punch.map(function (x) { return x[0] * x[1]; })), tTop = Math.max.apply(null, c.punch.map(function (x) { return x[1]; }));
      var bigHole = c.punch.some(function (x) { return x[0] >= h * 0.99; }), tAt = Math.min(tTop, pmax / h);
      pass(bigHole && tAt >= th * 0.99, bigHole ? "punches Ø" + fmtIn(h) + " holes through up to " + fmtIn(Math.floor(tAt * 16 + 1e-6) / 16) : "punches holes up to Ø" + fmtIn(Math.max.apply(null, c.punch.map(function (x) { return x[0]; }))), bigHole ? th / tAt : null);
    }
    if (c.fbs && req.mat === "flat" && N.size) {
      pass(c.fbs.some(function (x) { return (!x[0] || x[0] >= N.size) && (!N.size2 || x[1] >= N.size2 * 0.99); }), "shears flat bar " + fmtIn(c.fbs[0][0]) + " × " + fmtIn(c.fbs[0][1]));
    }
    if (c.ang && req.mat === "angle" && N.size) pass(c.ang[0] >= N.size * 0.99 && (!N.thk || c.ang[1] >= N.thk * 0.99), "shears angle " + fmtIn(c.ang[0]) + " × " + fmtIn(c.ang[1]));
    if (c.bar_rd && req.mat === "rd_bar" && N.size && (req.ops.shear || req.ops.cut) && page === "ironworker-machines") pass(c.bar_rd >= N.size * 0.99, "shears round bar Ø" + fmtIn(c.bar_rd));
    // rebar
    if (N.bar && (c.bar65 || c.bar45)) {
      // the rated size (the maker's "max single bar", as on the product page) decides — the owner: a BT 26 bends 25 mm bar;
      // the smaller Grade 400W size is a caution on the card
      var nom = c.bar45 || c.bar65, g400 = c.bar65 || c.bar45;
      pass(nom >= N.bar * 0.99, (c.op === "cut" ? "cuts" : "bends") + " one bar up to " + barLabel(nom) + (g400 < nom ? " — " + g400 + " mm in Grade 400W" : ""), N.bar / nom);
      if (nom >= N.bar * 0.99 && g400 < N.bar * 0.99) caution.push("in Grade 400W rebar it is rated to " + g400 + " mm — tell us your bar grade and we will confirm");
    }
    // lasers
    if (N.bed && c.bed) pass(c.bed[0] >= N.bed[0] * 0.99 && c.bed[1] >= N.bed[1] * 0.99, "bed " + Math.round(c.bed[0] / 12 * 10) / 10 + " × " + Math.round(c.bed[1] / 12 * 10) / 10 + " ft");
    if (N.kw && c.kw) pass(c.kw[1] >= N.kw, "laser " + c.kw[0] + " – " + c.kw[1] + " kW");
    // weight capacity, work diameter, drilling
    if (N.load && c.load) pass(c.load >= N.load * 0.98, "rated for " + fmtLb(c.load), N.load / c.load);
    if (N.D && c.work_d && c.work_d[1]) pass(N.D <= c.work_d[1] * 1.01 && (!c.work_d[0] || N.D >= c.work_d[0] * 0.99), "work Ø" + fmtIn(c.work_d[0] || 0) + " – " + fmtIn(c.work_d[1]));
    if (N.hole && c.drill && page === "drill-press") pass(c.drill >= N.hole * 0.99, "drills Ø" + fmtIn(c.drill) + " in steel", N.hole / c.drill);
    if (checks) ok = fails === 0;
    if (rs.length) ratio = rs.reduce(function (a, b) { return a + b; }, 0) / rs.length;   // how closely the machine matches the job: 1 = just big enough
    return { ok: ok, notes: notes, warn: warn, ratio: ratio, checks: checks, caution: caution };
  }
  function npsLabel(od) { for (var k in NPS) if (Math.abs(NPS[k] - od) < 0.02) return k; return fmtIn(od).replace("″", ""); }
  function sizeLabel(req) {
    var N = req.nums;
    if (req.mat === "pipe" && N.nps) return "NPS " + fracKey(N.nps) + " (" + fmtIn(N.size) + " OD)";
    if ((req.mat === "flat" || req.mat === "angle") && N.size2) return fmtIn(N.size) + " × " + fmtIn(N.size2);
    return N.size ? fmtIn(N.size) : "";
  }
  function fmtNum(x) { return Math.round(x * 100) / 100; }
  function barLabel(mm) {
    var ca = null, us = null, k;
    for (k in CA_BARS) if (CA_BARS[k] <= mm + 0.3) ca = k;
    for (k in US_BARS) if (US_BARS[k] <= mm + 0.3) us = k;
    return mm + " mm" + (ca ? " (" + ca + "M" + (us ? ", #" + us : "") + ")" : us ? " (#" + us + ")" : "");
  }

  /* ======================================================================================== ranking */
  function rank(req) {
    var qt = queryTerms(req.n), cq = compact(req.q), scored = [];
    // model names typed in the question
    var modelHits = {};
    var toks = norm(req.q).split(/[^a-z0-9]+/).filter(Boolean);
    for (var i = 0; i < toks.length; i++) {
      for (var len = 1; len <= 3 && i + len <= toks.length; len++) {
        var key = toks.slice(i, i + len).join("");
        if (key.length < 3 || !/\d/.test(key)) continue;
        MODELS.forEach(function (m) { if (m.key === key) { var cur = modelHits[m.f.id]; if (!cur || !m.loose) modelHits[m.f.id] = { mi: m.mi, loose: m.loose }; } });
      }
    }
    var anyPages = Object.keys(req.pages).length > 0, hasNums = Object.keys(req.nums).length > 0;
    FAM.forEach(function (f) {
      var s = textScore(f, qt), intent = req.pages[f.page] || 0;
      var hit = modelHits[f.id];
      s = s * (anyPages ? 0.5 : 1) + intent * (anyPages ? 1.4 : 1);
      if (hit) s += hit.loose ? 14 : 22;
      // qualifiers
      var label = (f.name + " " + f.category + " " + (f.automation || "") + " " + f.short).toLowerCase(), Q = req.qual;
      if (Q.cnc && /\bcnc\b/.test(label)) s += 4; if (Q.nc && /\bnc\b/.test(label) && !/\bcnc\b/.test(label)) s += 3;
      if (Q.auto && /automatic|cnc|\bauto|line\b/.test(label) && !/semi/.test(label)) s += 4;
      if (Q.semi && /semi/.test(label)) s += 4;
      if (Q.manual && /manual|gravity|hand/.test(label)) s += 4;
      if (Q.manual && /automatic|cnc/.test(label)) s -= 2;
      if (Q.hydraulic && /hydraulic/.test(label)) s += 2; if (Q.electric && /electric|servo/.test(label)) s += 3; if (Q.mechanical && /mechanical/.test(label)) s += 3;
      if (Q.premium && f.line === "Premium line") s += 3; if (Q.value && f.line === "Value line") s += 3;
      if (Q.small && /compact|bench|mini|light|small|portable|table/.test(label)) s += 2;
      if (Q.heavy && /heavy|double.?column|twin|large/.test(label)) s += 2;
      if (Q.single) {
        if (f._single == null) f._single = /single.?phase|1.?phase|\b(110|115|120|220|230) ?v/i.test(f.summary + " " + f.features.join(" ") + " " + JSON.stringify(f.models));
        if (f._single) s += 6;
      }
      // capacities: the smallest model that does the job, with a margin
      var best = null;
      if (hasNums && f.models.length) {
        f.models.forEach(function (m, mi) {
          var fit = fitModel(f, mi, req);
          if (fit.ok === null) return;
          var key = fit.ok ? 2 + (fit.ratio != null ? Math.min(1, fit.ratio) : 0.5) : (fit.ratio != null ? -fit.ratio : -1);
          if (!best || key > best.key) best = { mi: mi, fit: fit, key: key };
        });
      }
      var fit = best ? best.fit : null, relevant = !anyPages || intent > 0 || hit;
      if (fit && fit.ok && relevant) s += 7 + 3 * Math.min(1, fit.ratio != null ? fit.ratio : 0.5) + 1.5 * Math.min(3, fit.checks - 1);
      else if (fit && fit.ok === false) s -= 9;
      if (s > 0.5) scored.push({ f: f, s: s, mi: hit && !hit.loose ? hit.mi : (best ? best.mi : (hit ? hit.mi : null)), fit: fit, hit: !!hit, intent: intent, cov: f._cov });
    });
    scored.sort(function (a, b) { return b.s - a.s; });
    return { list: scored, qt: qt, modelHit: Object.keys(modelHits).length > 0 };
  }

  /* questions and answers of the pages that match the question */
  function faqMatch(req, qt, pages) {
    var best = null;
    PAGES.forEach(function (p) {
      (p.faq || []).forEach(function (qa, i) {
        var s = 0, sa = 0;
        for (var t in qt) { var w = qt[t] * idf(t); if (p._q[i][t]) s += w * 2; if (p._a[i][t]) sa += w; }
        s = s + sa * 0.35 + (pages[p.slug] ? 2 + pages[p.slug] / 4 : 0);
        if (!best || s > best.s) best = { s: s, p: p, qa: qa };
      });
    });
    return best;
  }

  /* questions about the company: warranty, financing, delivery, location, price, voltage, parts, agents */
  function infoAnswer(n) {
    var C = DATA.contact || {}, A = C.address || {}, contactLine = "Call **" + C.phone + "**, email " + C.email + " or use the quote form.";
    var I = [
      [/warrant|guarantee|money.?back|refund/, "Every new machine comes with a **1-year warranty**, with spare parts and service from Mississauga, ON. In-stock models also carry a **7-day money-back guarantee**: try the machine in your shop, with a full refund within 7 days.", "about-us"],
      [/financ|leas(e|ing)|payment plan|0% down|monthly payment|credit/, "You can finance a machine with **0% down** and competitive rates through NovoTech's financing partners. Ask for financing when you request a quote.", "contact-us"],
      [/deliver|shipping|ship to|freight|install|training|commission|set ?up|setup/, "NovoTech delivers, installs and trains across Canada, and every machine is supported with spare parts and service from our warehouse in Mississauga, ON. " + contactLine, "contact-us"],
      [/where are you|location|located|your address|showroom|warehouse|visit you|directions|opening hours|business hours|office hours|when are you open|what time/, "NovoTech's showroom and warehouse: **" + A.street + ", " + A.city + ", " + A.region + " " + A.postal + "**. Open " + C.hours + " (Eastern). Machines in stock can be seen running in the showroom — call ahead and we will set it up.", "contact-us"],
      [/\bprice|\bcost|how much|\$|pricing|cheapest price|quote/, "Prices depend on the model, the options and delivery, so we quote each machine: use **Request a quote** on the machine's page, or " + contactLine.charAt(0).toLowerCase() + contactLine.slice(1), "contact-us"],
      [/\b(208|240|480|575|600|110|115|120|220|230) ?v(olts?)?\b|voltage|\bcsa\b|three.?phase|single.?phase|\b[13].?phase|power supply|electrical panel/, "Every machine ships with a **CSA-approved electrical panel**. Three-phase machines are supplied for 600 V; 208 V, 240 V or 480 V 3-phase is available on request, and several smaller machines run on single-phase power.", "about-us"],
      [/spare parts?|replacement parts?|parts (and|&) service|\bservice\b|repair|technician|tech support|maintenance/, "Spare parts and technical support are available from Mississauga, ON — for every machine we sell. " + contactLine, "contact-us"],
      [/\bagent|dealer|distribut|represent|resell/, "NovoTech is appointing independent sales agents and dealers across Canada. If you call on fabricators, rebar shops or contractors, contact us at " + C.email + ".", "contact-us"],
      [/brochure|catalog|\bpdf\b|data ?sheet|spec sheet/, "Every product page has its PDF brochure, and the **Brochures** page lists all of them (imperial units).", "brochures"],
      [/contact|phone|email|call you|talk to|speak/, contactLine + " Hours: " + C.hours + " (Eastern).", "contact-us"],
      [/plasma|water ?jet|oxy.?fuel|oxy.?acetylene|flame cut/, "NovoTech does not sell plasma, waterjet or oxy-fuel cutting tables. For cutting sheet and plate we offer fiber laser cutting machines (including large-format plate lasers with bevel heads) and plate shears — they are listed below. Call us to compare them with the job you have in mind.", "laser-cutting-machine"],
      [/\bused (machine|equipment|press|saw|brake|shear|laser|ironworker)|second.?hand|refurbish|pre.?owned/, "The machines on this site are new, with a 1-year warranty and support from Mississauga. Ask us which models are in stock in our warehouse.", "contact-us"]
    ];
    for (var i = 0; i < I.length; i++) if (I[i][0].test(n)) return { text: I[i][1], page: I[i][2], withMachines: /price|cost|plasma/.test(String(I[i][0])) };
    return null;
  }

  /* ======================================================================================== every machine that does the job */
  /* The owner (Nov 7 2026): list every machine on the site that does the job, the smallest that does it first and then
     the bigger ones in order, each as a full card; machines that may also do it (not sure) go below the whole list. */
  var SEC_ORDER = ["pipe", "rd_tube", "sq_tube", "rect_tube", "angle_out", "flat_easy", "flat_hard", "rd_bar", "sq_bar", "channel", "beam", "tee", "angle_in"];
  /* a model's size for "smallest first": its main capacity, then the next one, then its place in the spec table */
  function sizeKey(f, mi) {
    var c = (f._caps || [])[mi] || {}, a = 0, b = 0, i;
    if (c.ton) { a = c.ton; b = c.len || 0; }
    else if (c.thk) { a = c.thk; b = c.len || 0; }
    else if (c.bar45 || c.bar65) { a = c.bar45 || c.bar65; b = c.bar65 || 0; }
    else if (c.sec) { for (i = 0; i < SEC_ORDER.length; i++) if (c.sec[SEC_ORDER[i]]) { a = sizeOf(c.sec[SEC_ORDER[i]][0]); break; } }
    else if (c.od || c.nps_od) { a = c.od || c.nps_od; b = c.wall || 0; }
    else if (c.rnd || c.rect) { a = c.rnd || c.rect[1]; b = c.rect ? c.rect[0] * c.rect[1] : 0; }
    else if (c.punch) a = Math.max.apply(null, c.punch.map(function (x) { return x[0] * x[1]; }));
    else if (c.bed) { a = c.bed[0] * c.bed[1]; b = c.kw ? c.kw[1] : 0; }
    else if (c.kw) a = c.kw[1];
    else if (c.load) a = c.load;
    else if (c.drill) a = c.drill;
    else if (c.work_d) a = c.work_d[1] || 0;
    else if (c.len) a = c.len;
    return [a || 1e9, b, mi];          // a machine without capacities in the index goes after the ones with
  }
  function famSize(f) {
    if (!f.models.length) return [1e9, 0, 0];
    var best = null;
    f.models.forEach(function (m, mi) { var x = sizeKey(f, mi); if (!best || x[0] < best[0] || x[0] === best[0] && x[1] < best[1]) best = x; });
    return [best[0], best[1], 0];
  }
  function cmpSize(a, b) {
    var x = a.size, y = b.size;
    if (x[0] !== y[0]) return x[0] - y[0];
    if (x[1] !== y[1]) return x[1] - y[1];
    if (a.f._i !== b.f._i) return a.f._i - b.f._i;
    return x[2] - y[2];
  }
  /* machines that do the job: the closest fit (just big enough) first */
  function cmpFit(a, b) {
    var ra = a.fit && a.fit.ratio, rb = b.fit && b.fit.ratio;
    if (ra != null && rb != null && Math.abs(ra - rb) > 0.004) return rb - ra;
    if (ra != null && rb == null) return -1;
    if (ra == null && rb != null) return 1;
    return cmpSize(a, b);
  }
  function fam(f, why) { return { f: f, mi: null, fit: null, size: famSize(f), why: why || null }; }
  /* machines made for one special shape: below the list unless the question names it */
  var SPECIAL = ["stirrup", "spiral", "dowel", "mesh", "combined", "bender-cutter", "coiler"];
  function special(f, qn) {
    var t = (f.short + " " + f.name).toLowerCase();
    for (var i = 0; i < SPECIAL.length; i++) if (t.indexOf(SPECIAL[i]) >= 0 && qn.indexOf(SPECIAL[i].slice(0, 5)) < 0) return true;
    return false;
  }
  /* the kind of machine the visitor asked for (automatic, CNC, electric, premium line…) */
  function qualMismatch(f, Q) {
    var label = (f.name + " " + f.category + " " + (f.automation || "") + " " + f.short).toLowerCase();
    if (Q.auto && (/semi/.test(label) || !/automatic|cnc|\bauto|line\b/.test(label))) return "not automatic";
    if (Q.semi && !/semi/.test(label)) return "not semi-automatic";
    if (Q.manual && !/manual|gravity|hand/.test(label)) return "not manual";
    if (Q.cnc && !/\bcnc\b/.test(label)) return "not CNC";
    if (Q.nc && !/\bnc\b|\bcnc\b/.test(label)) return "not NC";
    if (Q.electric && !/electric|servo/.test(label)) return "not electric";
    if (Q.hydraulic && !/hydraulic/.test(label)) return "not hydraulic";
    if (Q.mechanical && !/mechanical/.test(label)) return "not mechanical";
    if (Q.premium && f.line === "Value line") return "not the premium line";
    if (Q.value && f.line !== "Value line") return "not the value line";
    if (Q.single) {
      if (f._single == null) f._single = /single.?phase|1.?phase|\b(110|115|120|220|230) ?v/i.test(f.summary + " " + f.features.join(" ") + " " + JSON.stringify(f.models));
      if (!f._single) return "three-phase";
    }
    return null;
  }
  /* rebar: a bender is not a cutter, and the other way round */
  function opMismatch(f, req) {
    var caps = f._caps || [], ops = req.ops;
    if (!caps.length) return false;
    if (ops.bend && !ops.cut && caps.every(function (c) { return c.op === "cut"; })) return true;
    if (ops.cut && !ops.bend && caps.every(function (c) { return c.op === "bend" && !c.cut65; })) return true;
    return false;
  }
  function machines(req, r) {
    var pages = req.pages, max = 0, k, hasNums = Object.keys(req.nums).length > 0, Q = req.qual, qn = req.n;
    for (k in pages) if (pages[k] > max) max = pages[k];
    var hits = {}, hitList = [];
    r.list.forEach(function (x) { if (x.hit) { hits[x.f.id] = x; hitList.push(x); } });
    var fits = [], maybe = [], fails = [], closest = [], mode = "models";
    // no machine type recognised, only words: the families the words point to, the most relevant first
    if (!max && !hitList.length) {
      var topS = r.list.length ? r.list[0].s : 0;
      r.list.forEach(function (x) { if (x.s >= topS * 0.45) fits.push(fam(x.f)); });
      return { fits: fits, maybe: [], closest: [], mode: "relevance" };
    }
    // a model the visitor named: that model, then the rest of its series and the machines like it
    if (hitList.length && !hasNums) {
      var seenF = {}, pg = {};
      hitList.forEach(function (x) {
        seenF[x.f.id] = 1; pg[x.f.page] = 1;
        if (x.mi != null) fits.push({ f: x.f, mi: x.mi, fit: null, size: sizeKey(x.f, x.mi) }); else fits.push(fam(x.f));
        x.f.models.forEach(function (m, mi) { if (mi !== x.mi) maybe.push({ f: x.f, mi: mi, fit: null, size: sizeKey(x.f, mi), why: "series" }); });
      });
      FAM.forEach(function (f) { if (pg[f.page] && !seenF[f.id]) maybe.push(fam(f, "page")); });
      maybe.sort(function (a, b) { return (a.why === "page") - (b.why === "page") || cmpSize(a, b); });   // its own series first
      return { fits: fits, maybe: maybe, closest: [], mode: "hit" };
    }
    var ACCESSORY = /dispenser|\bstands?\b|\bcarts?\b|accessor|conveyor|\btables?\b(?!.*weld)|dust collector/i;   // not machines that do a job
    FAM.forEach(function (f) {
      var w = pages[f.page] || 0, hit = hits[f.id];
      if (!hit && (!max || w < max * 0.4)) return;
      if (opMismatch(f, req)) return;
      if (hasNums && !hit && w < max * 0.7 && ACCESSORY.test(f.short + " " + f.name)) return;
      // a job with sizes: every kind that was inferred for it is a full answer, not a "similar machine"
      var main = !!hit || w >= max * (hasNums ? 0.4 : 0.7), mis = qualMismatch(f, Q), sp = special(f, qn);
      var why = hit ? null : !main ? "other" : sp ? "special" : mis ? "qual" : null;
      if (hasNums) {
        var ok = [], unknown = !f.models.length;
        f.models.forEach(function (m, mi) {
          var fit = fitModel(f, mi, req), e = { f: f, mi: mi, fit: fit, size: sizeKey(f, mi) };
          if (fit.ok) ok.push(e); else if (fit.ok === null) unknown = true; else if (main && !why) fails.push(e);
        });
        if (ok.length) {
          if (why) { ok.sort(cmpFit); ok[0].why = why; ok[0].mis = mis; maybe.push(ok[0]); }      // the smallest of them that fits, as one card
          else Array.prototype.push.apply(fits, ok);
        } else if (unknown && main && !why) maybe.push(fam(f, "unknown"));
      } else if (why) {
        if (main) { var e2 = fam(f, why); e2.mis = mis; maybe.push(e2); }
      } else if (f.models.length) {
        f.models.forEach(function (m, mi) { fits.push({ f: f, mi: mi, fit: null, size: sizeKey(f, mi) }); });
      } else fits.push(fam(f));
    });
    if (!fits.length && maybe.some(function (e) { return e.why === "qual"; })) {
      maybe = maybe.filter(function (e) {
        if (e.why !== "qual") return true;
        if (hasNums) { if (e.mi != null) { e.why = null; fits.push(e); } }
        else if (e.f.models.length) e.f.models.forEach(function (m, mi) { fits.push({ f: e.f, mi: mi, fit: null, size: sizeKey(e.f, mi) }); });
        else fits.push(fam(e.f));
        return false;
      });
    }
    if (hasNums) {
      fits.sort(cmpFit);
      if (!fits.length && fails.length) { fails.sort(function (a, b) { return cmpSize(b, a); }); closest = fails.slice(0, 3); }
    } else {
      fits.sort(cmpSize);
      if (fits.length > 24) {       // a whole range (press brakes: 100+ models): one card per series, smallest first
        var byF = {}, fl = [];
        fits.forEach(function (e) { if (!byF[e.f.id]) { byF[e.f.id] = 1; fl.push(fam(e.f)); } });
        fits = fl.sort(cmpSize); mode = "families";
      }
    }
    // machines that fit go first in the similar list, the ones without data for this size after them
    maybe.sort(function (a, b) { return (a.why === "unknown") - (b.why === "unknown") || cmpSize(a, b); });
    return { fits: fits, maybe: maybe, closest: closest, mode: mode };
  }
  /* what the visitor asked for, in words: the common end of the product pages' names ("press brakes") */
  function typeLabel(req) {
    var pages = req.pages, max = 0, k, navs = [];
    for (k in pages) if (pages[k] > max) max = pages[k];
    for (k in pages) if (pages[k] >= max * 0.7) {
      var p = pageBySlug(k), nm = p ? (p.nav || (p.h1 || "").split(" — ")[0]) : "";
      if (nm) navs.push(nm.toLowerCase().replace(/[^a-z0-9 &-]+/g, " ").trim());
    }
    if (!navs.length) return "machines";
    if (navs.length === 1) return navs[0];
    var w = navs.map(function (x) { return x.split(/\s+/); }), out = [];
    for (var i = 1; i <= w[0].length; i++) {
      var word = w[0][w[0].length - i];
      if (w.every(function (a) { return a[a.length - i] === word; })) out.unshift(word); else break;
    }
    return out.length ? out.join(" ") : "machines";
  }

  /* the kinds of machine in a list ("roofing brakes, folders, press brakes"), in the order they first appear */
  function kindsOf(list) {
    var seen = {}, out = [];
    list.forEach(function (e) {
      if (seen[e.f.page]) return;
      seen[e.f.page] = 1;
      var p = pageBySlug(e.f.page), nm = p ? (p.nav || (p.h1 || "").split(" — ")[0]) : "";
      if (nm) out.push(nm.toLowerCase().replace(/[^a-z0-9 &-]+/g, " ").replace(/\s+/g, " ").trim());
    });
    return out;
  }
  /* ======================================================================================== the answer */
  function pageBySlug(slug) { for (var i = 0; i < PAGES.length; i++) if (PAGES[i].slug === slug) return PAGES[i]; return null; }
  function firstSentence(t) { var m = /^(.{40,260}?[.!?])\s/.exec((t || "") + " "); return m ? m[1] : (t || "").slice(0, 220); }
  function modelName(r) { return r.mi != null && r.f.models[r.mi] ? r.f.models[r.mi].name : null; }
  function entryName(e) { return modelName(e) || e.f.short || e.f.name; }
  function lineLabel(f) { return f.line === "Premium line" ? "NovoTech premium line" : f.line === "Value line" ? "NovoTech value line" : (f.brand || ""); }

  function answer(q, prev) {
    var req = understand(q, prev), n = req.n;
    var info = infoAnswer(n), greet = /^\s*(hi|hello|hey|good (morning|afternoon|evening)|salam|bonjour|سلام)\b/.test(n) && n.length < 30;
    var r = rank(req), list = r.list;
    var top = list[0], strong = top && (top.s >= 9 || r.modelHit || top.cov >= 0.99 && top.s >= 2.5);
    var anyPages = Object.keys(req.pages).length > 0, N = req.nums, hasNums = Object.keys(N).length > 0;
    var res = { req: req, fits: [], maybe: [], closest: [], best: null, text: [], chips: [], page: null, faq: null, mode: null };
    if (greet && !anyPages) {
      res.text.push("Hello! Tell me what you need to make — the material, its size and what you want to do with it (cut, bend, roll, punch…) — and I will list every machine in NovoTech's catalogue that does it, the smallest first.");
      res.chips = DEFAULT_CHIPS;
      return res;
    }
    var machineAsk = anyPages || r.modelHit || req.mat || hasNums;
    if (info) res.text.push(info.text);
    if (info && (!strong || !machineAsk)) { res.page = pageBySlug(info.page); res.chips = DEFAULT_CHIPS.slice(0, 3); return res; }
    var noMatch = "I could not match that to a machine in our catalogue. Describe the job — the material (plate, sheet, pipe, angle, rebar…), its size, and whether you want to cut, bend, roll, punch or weld it — or call **" + DATA.contact.phone + "** and we will help.";
    if (!list.length || (!strong && !anyPages && !info)) { res.text.push(noMatch); res.chips = DEFAULT_CHIPS; return res; }
    var M = machines(req, r);
    res.fits = M.fits; res.maybe = M.maybe; res.closest = M.closest; res.mode = M.mode;
    var lead = res.fits[0] || res.closest[0] || res.maybe[0];
    if (!lead) { res.text.push(noMatch); res.chips = DEFAULT_CHIPS; return res; }
    res.best = lead;
    res.page = pageBySlug(lead.f.page);
    var what = entryName(lead), nF = res.fits.length, label = typeLabel(req);
    if (M.mode === "hit") {
      res.text.push("**" + what + "** — " + lead.f.name + (lead.f.headline ? ": " + lead.f.headline : "") + ".");
      res.text.push(firstSentence(lead.f.summary));
      if (res.maybe.length) res.text.push("Below it are the other models of the series and the machines like it, from the smallest to the largest.");
    } else {
      var faq = !info && /\?|^(what|which|how|why|can|could|do|does|is|are|should|difference|vs\b)|\bor\b|\bvs\.?\b|difference|better/.test(n.trim()) ? faqMatch(req, r.qt, req.pages) : null;
      if (faq && faq.s >= 8) { res.faq = faq; res.text.push("**" + faq.qa[0] + "** " + faq.qa[1]); }
      if (hasNums) {
        var job = jobLine(req);
        if (nF) {
          var why = lead.fit && lead.fit.notes.length ? " — " + lead.fit.notes.slice(0, 3).join("; ") : "";
          var kinds = kindsOf(res.fits);
          res.text.push((job ? job + " " : "") + (nF === 1 ? "One machine on our site does this job: the **" + what + "** (" + lineLabel(lead.f) + ")" + why + "." :
            "**" + nF + " machines** on our site can do this job" + (kinds.length > 1 ? " — " + kinds.join(", ").replace(/, ([^,]*)$/, " and $1") : "") + ". The smallest that does it is the **" + what + "** (" + lineLabel(lead.f) + ")" + why + (nF === 2 ? ". Both are listed below, the smaller first." : ". All " + nF + " are listed below, from the smallest to the largest" + (kinds.length > 1 ? ", whatever their kind" : "") + ".")));
          if (lead.fit && lead.fit.caution && lead.fit.caution.length) res.text.push("Note: " + lead.fit.caution[0].replace(/^in /, "In ") + ".");
        } else if (res.closest.length) {
          res.text.push((job ? job + " " : "") + "None of our machines of this type is rated for every size you gave. The largest ones are below — call **" + DATA.contact.phone + "** and we will check your part against them.");
        } else {
          res.text.push((job ? job + " " : "") + "I could not find a machine on our site rated for every size you gave. Call **" + DATA.contact.phone + "** and we will check your part.");
        }
        if (req.need && PRESS_BRAKES[lead.f.page]) res.text.push("For air bending " + fmtThk(N.thk) + (req.qual.stainless ? " stainless" : " mild steel") + " on a die about 8 × thickness wide, a press brake needs about **" + Math.round(req.need.perFt) + " US tons per foot**" + (N.len ? " — " + Math.round(req.need.tons) + " US tons over " + fmtLen(N.len) : "") + ".");
      } else if (!res.faq) {
        if (M.mode === "relevance") res.text.push(nF === 1 ? "This machine on our site matches what you wrote:" : "These " + nF + " machines on our site match what you wrote, the closest match first:");
        else if (M.mode === "families") {
          var nm = res.fits.reduce(function (a, e) { return a + e.f.models.length; }, 0);
          res.text.push("We sell **" + nF + " series of " + label + "** (" + nm + " models), listed below from the smallest to the largest. Tell me the material, the size and the length of your parts and I will list the exact models that do the job.");
        } else if (!nF) res.text.push("I found no machine of that exact kind on our site — the closest ones are below. Tell me the material, the size and the length of your parts and I will check which of them does the job.");
        else res.text.push(nF === 1 ? "Here is the one model we sell. Tell me the material and the size of your parts and I will check that it does the job." :
          "Here are all **" + nF + " " + label + "** we sell, from the smallest to the largest. Tell me the material, the size and the length of your parts and I will show only the models that do the job.");
      }
      if (res.maybe.length) res.text.push(res.maybe.length === 1 ? "At the end of the list is one similar machine that may also do it — we confirm it with your drawing." :
        "At the end of the list are " + res.maybe.length + " similar machines that may also do it — we confirm those with your drawing.");
    }
    if (req.mat === "pipe" && N.nps && lead.f.page === "angle-rolls") res.text.push("Pipe and tube need the matching set of pipe rolls; the minimum diameter depends on the wall thickness and the material, so send us your drawing and we will confirm it.");
    res.chips = chipsFor(lead.f.page, lead);
    return res;
  }
  function jobLine(req) {
    var N = req.nums, mat = req.mat, sz = sizeLabel(req), parts = [];
    if (req.ops.roll || (N.D && (req.ops.bend || mat && LONG[mat]))) {
      if (sz && mat && PROF[mat]) parts.push("To roll " + sz + " " + (mat === "pipe" ? "pipe" : (PROF_NAME[PROF[mat][0]] || mat)) + (N.D ? " into a Ø" + fmtNum(N.D) + "″ ring" : "") + ", you need a section bender (angle roll).");
      else if (N.thk) parts.push("To roll " + fmtThk(N.thk) + " plate" + (N.len ? " " + fmtLen(N.len) + " wide" : "") + (N.D ? " to Ø" + fmtNum(N.D) + "″" : "") + ", you need a plate roll.");
    } else if (N.bar) parts.push("For " + barLabel(N.bar).replace(/^[\d.]+ mm /, "").replace(/[()]/g, "") + " rebar (Ø" + Math.round(N.bar) + " mm):");
    else if (N.thk && N.len) parts.push("For " + fmtThk(N.thk) + " × " + fmtLen(N.len) + (req.qual.stainless ? " stainless" : "") + ":");
    return parts.join(" ");
  }
  var DEFAULT_CHIPS = ["Roll 2″ pipe into a 30″ diameter ring", "Shear 1/4″ plate × 10 ft", "Press brake for 3/16″ × 8 ft", "Rebar bender for 25M bars", "Automatic band saw for 6″ tube at 45°"];
  var CHIPS = {
    "angle-rolls": ["Roll L 2 × 2 × 1/4″ angle to Ø60″", "Profile bender for flat bar on edge", "Angle roll with NC control"],
    "hydraulic-shearing-machine": ["CNC guillotine shear 3/8″ × 10 ft", "Shear for 16 ga stainless", "Budget hydraulic shear 1/4″ × 8 ft"],
    "mechanical-guillotine-shear": ["Hydraulic shear 1/4″ × 10 ft", "Foot shear for 18 ga"],
    "hydraulic-press-brake": ["Electric press brake for small parts", "Press brake 1/2″ × 10 ft", "Press brake tooling"],
    "electric-press-brake": ["Hydraulic press brake 1/4″ × 10 ft", "Panel bender"],
    "compact-hydraulic-press-brakes": ["Press brake 3/16″ × 8 ft", "Electric press brake"],
    "hydraulic-3-roll-plate-rollers": ["4-roll plate roll 1/2″ × 10 ft", "Slip roll for 16 ga sheet"],
    "hydraulic-4-roll-plate-rollers": ["3-roll plate roll 1/4″ × 6 ft", "Cone rolling"],
    "motorized-plate-rollers": ["Hydraulic plate roll 3/8″ × 8 ft", "4-roll plate roll"],
    "rotary-draw-tube-benders": ["CNC tube bender 2″ OD", "Roll 2″ pipe into a 40″ ring"],
    "nc-tube-benders": ["CNC tube bender with mandrel", "Tube end flaring machine"],
    "cnc-tube-benders": ["NC tube bender 2″", "Tube laser for 6″ tube"],
    "ironworker-machines": ["Punch 1″ hole in 1/2″ plate", "Hydraulic punching machine"],
    "semi-automatic-band-saws": ["Automatic band saw 10″ round", "Double column saw 20″"],
    "automatic-band-saws": ["Semi-automatic miter saw 10″", "Automatic cold saw"],
    "double-column-band-saws": ["Twin column saw 30″", "Automatic band saw 12″"],
    "rebar-bender": ["Rebar cutter for 35M", "Stirrup bender"],
    "rebar-cutter": ["Rebar bender 25M", "Combined bender-cutter"],
    "fiber-laser-cutting-machine": ["Laser for 5 × 10 ft sheet, 12 kW", "Tube laser 6″", "Laser welding machine"],
    "tube-laser-cutting-machine": ["Sheet and tube laser", "Fiber laser 5 × 10 ft"],
    "welding-positioners": ["Turning rolls for a 10 ton tank", "Welding table"],
    "welding-turning-rolls": ["Welding positioner 2,000 lb", "Column and boom manipulator"]
  };
  function chipsFor(page, best) {
    var c = (CHIPS[page] || DEFAULT_CHIPS.slice(0, 3)).slice(0, 3);
    return c;
  }

  var API = { init: init, answer: answer, understand: understand, rank: rank, fitModel: fitModel, terms: terms, fmtIn: fmtIn, machines: machines, sizeKey: sizeKey };
  root.NTFinder = API;
  if (typeof module !== "undefined" && module.exports) module.exports = API;

  /* ======================================================================================== the chat panel */
  var d = root.document;
  if (!d || !d.getElementById) return;
  var panel = d.getElementById("ai-panel");
  if (!panel || panel.dataset.ready) return;
  panel.dataset.ready = "1";
  var log = d.getElementById("ai-log"), form = d.getElementById("ai-form"), input = d.getElementById("ai-q"), suggest = d.getElementById("ai-suggest");
  var STAGING = !!panel.dataset.staging, history = [], prevReq = null, loading = null, busy = false;

  function el(tag, cls, html) { var e = d.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function md(t) {
    var lines = esc(t).split(/\n/), out = "", inList = false;
    lines.forEach(function (ln) {
      var m = /^\s*(?:[-*•]|\d+[.)])\s+(.*)$/.exec(ln);
      if (m) { if (!inList) { out += "<ul>"; inList = true; } out += "<li>" + m[1] + "</li>"; return; }
      if (inList) { out += "</ul>"; inList = false; }
      if (ln.trim()) out += "<p>" + ln + "</p>";
    });
    if (inList) out += "</ul>";
    return out.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, function (m, t, url) {
      var own = /^(\/|#|[a-z0-9-]+(\.html)?(#[\w-]+)?$)/i.test(url) || /^https?:\/\/(www\.)?novotechmachinetools\.(com|github\.io)\b/i.test(url);
      return own ? '<a href="' + url.replace(/^\/(?!\/)/, "") + '">' + t + "</a>" : t;
    });
  }
  function scrollTo(node) {
    setTimeout(function () { log.scrollTop = Math.max(0, log.scrollTop + node.getBoundingClientRect().top - log.getBoundingClientRect().top - 10); }, 30);
  }
  function load() {
    if (!loading) loading = fetch(panel.dataset.cat || "ai/catalogue.json").then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (j) { init(j); return j; });
    return loading;
  }
  function cap1(t) { return String(t).replace(/^./, function (c) { return c.toUpperCase(); }); }
  /* a short spec summary for a card: the capacity rows of the model's spec table first, at most four */
  var SPEC_HI = /capacit|max(imum|\.)?\b|force|tonnage|length|thickness|width|diameter|Ø|\bbar\b|pipe|tube|laser power|power source|\bbed\b|working (area|range)|table|travel|punch|stroke|swing|centres|centers|load|section|angle|flat|cut/i;
  var SPEC_MID = /motor|power|speed|throat|daylight|axis|control|chuck|spindle|feed|roll/i;
  var SPEC_SKIP = /dimension|oil|tank|colou?r|paint|noise|frame, stroke/i;
  function brief(v) { return String(v).replace(/\s*\([^)]*\)/g, "").split(" · ")[0].replace(/\s+/g, " ").trim(); }
  function shortVal(v) {
    v = String(v).replace(/\s+/g, " ").trim();
    if (v.length > 54) { var first = v.split(" · ")[0]; v = first.length >= 4 && first.length < v.length ? first : v.slice(0, 52).replace(/\s+\S*$/, "") + "…"; }
    return v;
  }
  function specRows(f, mi) {
    var rows = [], name = mi != null && f.models[mi] ? f.models[mi].name : null, i = 0, key;
    if (name) {
      (f.specs || []).some(function (t) {
        var col = (t.models || []).indexOf(name);
        if (col < 0) return false;
        t.rows.forEach(function (r, ri) { var v = r[col + 1]; if (v && !/^[—–-]$/.test(String(v).trim())) rows.push({ k: r[0], v: v, i: ri }); });
        return true;
      });
      if (!rows.length) {
        var m = f.models[mi];
        for (key in m) if (key !== "name" && key !== "img" && m[key] != null) rows.push({ k: cap1(key.replace(/_/g, " ")), v: Array.isArray(m[key]) ? m[key].join(", ") : String(m[key]), i: i++ });
      }
    } else {
      var t = (f.specs || [])[0];          // a whole series: the range from its first model to its last
      if (t && t.models && t.models.length) t.rows.forEach(function (r, ri) {
        var a = r[1], b = r[t.models.length];
        if (!a || /^[—–-]$/.test(String(a).trim())) return;
        var sa = brief(a), sb = b ? brief(b) : sa;
        rows.push({ k: r[0], v: sa === sb ? sa : sa + " – " + sb, i: ri });
      });
    }
    function pr(x) { return SPEC_SKIP.test(x.k) ? 0 : SPEC_HI.test(x.k) ? 3 : SPEC_MID.test(x.k) ? 2 : 1; }
    var top = rows.filter(function (x) { return pr(x) > 0 && String(x.v).length < 160; })
      .sort(function (a, b) { return pr(b) - pr(a) || a.i - b.i; }).slice(0, name ? 4 : 3);
    top.sort(function (a, b) { return a.i - b.i; });
    return top.map(function (x) { return [x.k.replace(/\s*\([^)]*\)\s*$/, "").replace(/,? (mild steel|standard rolls)$/i, ""), shortVal(x.v)]; });
  }
  function cardImg(e) {
    var m = e.mi != null ? e.f.models[e.mi] : null, im = (m && m.img) || e.f.img;
    if (im) return { html: '<img src="' + esc(im.src) + '" srcset="' + esc(im.srcset) + '" sizes="(max-width: 640px) 120px, 230px" alt="" loading="lazy" decoding="async">', cut: !!im.alpha };
    return { html: e.f.image ? '<img src="' + esc(e.f.image) + '" alt="" loading="lazy" decoding="async">' : "", cut: true };
  }
  /* one machine: photo, name, series, why it fits, cautions, a short spec summary and the links — the same for every card */
  function card(e, num, flag) {
    var f = e.f, nm = entryName(e), box = el("article", "ai-card" + (flag ? " is-lead" : ""));
    var series = e.mi != null ? f.name : (f.page_nav || f.category);
    var notes = e.fit && e.fit.ok ? e.fit.notes : (e.fit && e.fit.ok === false ? e.fit.warn : []);
    var cautions = (e.fit && e.fit.caution || []).slice();
    if (e.why === "unknown") cautions.push("our spec tables do not list this size for it — we check it with your drawing");
    if (e.why === "qual" && e.mis) cautions.push(e.mis.replace(/^not /, "not ") + " — listed because it does the job");
    if (e.fit && e.fit.ok === false) cautions.push("below the size you gave");
    var specs = specRows(f, e.mi);
    if (e.mi == null && f.models.length) specs.unshift(["Models", f.models.length > 1 ? f.models[0].name + " … " + f.models[f.models.length - 1].name + " (" + f.models.length + ")" : f.models[0].name]);
    var im = cardImg(e);
    box.innerHTML = '<a class="ai-img' + (im.cut ? "" : " is-photo") + '" href="' + esc(f.href) + '" tabindex="-1" aria-hidden="true">' + im.html + "</a>" +
      '<div class="ai-body">' +
        '<div class="ai-top">' + (num ? '<span class="ai-n">' + num + "</span>" : "") + (flag ? '<span class="ai-flag">' + esc(flag) + "</span>" : "") + '<span class="ai-line">' + esc(lineLabel(f)) + "</span></div>" +
        '<a class="ai-name" href="' + esc(f.href) + '">' + esc(nm) + "</a>" +
        '<span class="ai-fam">' + esc(series) + "</span>" +
        (notes.length ? '<ul class="ai-why' + (e.fit && e.fit.ok === false ? " is-bad" : "") + '">' + notes.map(function (t) { return "<li>" + esc(cap1(t)) + "</li>"; }).join("") + "</ul>" : (!e.fit && f.headline && e.mi == null ? '<p class="ai-cap">' + esc(f.headline) + "</p>" : "")) +
        (cautions.length ? '<ul class="ai-warn">' + cautions.map(function (t) { return "<li>" + esc(cap1(t)) + "</li>"; }).join("") + "</ul>" : "") +
        (specs.length ? '<dl class="ai-specs">' + specs.map(function (r) { return "<div><dt>" + esc(r[0]) + "</dt><dd>" + esc(r[1]) + "</dd></div>"; }).join("") + "</dl>" : "") +
        '<div class="ai-links"><a href="' + esc(f.href) + '">Specifications, photos and video →</a><a href="' + esc(f.page) + '#reques-a-quote">Get a quote</a>' +
          (f.pdf ? '<a href="' + esc(f.pdf) + '" target="_blank" rel="noopener">PDF brochure</a>' : "") + "</div>" +
      "</div>";
    return box;
  }
  function renderResult(res, bubble, text) {
    bubble.className = "ai-msg ai-assistant";
    bubble.innerHTML = '<span class="ai-avatar" aria-hidden="true">AI</span><div class="ai-text">' + md(text || res.text.join("\n")) + "</div>";
    renderLists(res, bubble);
  }
  function renderLists(res, bubble) {
    Array.prototype.forEach.call(bubble.querySelectorAll(".ai-list, .ai-more, .ai-chips"), function (x) { x.parentNode.removeChild(x); });
    var hasNums = res.req && Object.keys(res.req.nums).length > 0;
    function section(title, list, cls, numbered, flag) {
      if (!list.length) return;
      var sec = el("section", "ai-list " + cls);
      sec.appendChild(el("p", "ai-sub", esc(title)));
      list.forEach(function (e, i) { sec.appendChild(card(e, numbered ? i + 1 : 0, i === 0 ? flag : null)); });
      bubble.appendChild(sec);
    }
    var n = res.fits.length, title = res.mode === "hit" ? "The machine you asked about" :
      res.mode === "relevance" ? "Machines that match" :
      hasNums ? (n === 1 ? "The machine that does this job" : "Machines that do this job — smallest first (" + n + ")") :
      res.mode === "families" ? "Every series — smallest first (" + n + ")" : "Every model — smallest first (" + n + ")";
    section(title, res.fits, "is-fits", res.mode !== "hit" && res.mode !== "relevance" && n > 1, hasNums && n ? (n > 1 ? "Smallest that does it" : "Does the job") : null);
    section("Closest machines — below the size you gave", res.closest, "is-closest", false, null);
    section(res.mode === "hit" ? "The rest of the series and the machines like it" : "Similar machines — may also do the job (we confirm with your drawing)", res.maybe, "is-maybe", false, null);
    if (res.page) {
      var more = el("p", "ai-more");
      var label = (res.page.nav || res.page.h1.split(" — ")[0]).replace(/^(premium|value)[- ]line /i, "");
      more.innerHTML = '<a href="' + esc(res.page.slug === "index" ? "./" : res.page.slug) + '">' + (res.fits.length ? "Open the " + esc(label.charAt(0).toLowerCase() + label.slice(1)) + " page →" : "Open the " + esc(label) + " page →") + "</a>";
      bubble.appendChild(more);
    }
    if (res.chips && res.chips.length) {
      var chips = el("div", "ai-chips");
      res.chips.forEach(function (c) { var b = el("button", null, esc(c)); b.type = "button"; chips.appendChild(b); });
      bubble.appendChild(chips);
    }
  }
  /* the machines Claude names (live site), checked against the catalogue */
  function picks(list, req) {
    var out = [], seen = {}, hasNums = Object.keys(req.nums).length > 0;
    (Array.isArray(list) ? list : []).forEach(function (x) {
      var f = x && FAMBYID[x.id];
      if (!f) return;
      var mi = null;
      if (x.model) f.models.forEach(function (m, i) { if (mi == null && m.name === x.model) mi = i; });
      var k = f.id + "|" + mi;
      if (seen[k]) return;
      seen[k] = 1;
      out.push({ f: f, mi: mi, fit: mi != null && hasNums ? fitModel(f, mi, req) : null, size: mi != null ? sizeKey(f, mi) : famSize(f), why: x.note ? "llm" : null });
    });
    return out;
  }
  function visible(t) { var i = t.indexOf("RESULTS:"); return (i >= 0 ? t.slice(0, i) : t).replace(/\s+$/, ""); }
  var SERVER = !!panel.dataset.server && !STAGING;
  function ask(q) {
    q = (q || "").trim();
    if (busy || !q) return;
    busy = true;
    var send = form.querySelector("button[type=submit]");
    send.disabled = true;
    var u = el("div", "ai-msg ai-user", esc(q));
    log.appendChild(u);
    history.push({ role: "user", content: q });
    var bubble = el("div", "ai-msg ai-assistant ai-thinking", '<span class="ai-avatar" aria-hidden="true">AI</span><div class="ai-text"><span class="ai-dots"><i></i><i></i><i></i></span> Looking through every machine, spec table and brochure…</div>');
    log.appendChild(bubble);
    scrollTo(u);
    var t0 = Date.now();
    function done() { busy = false; send.disabled = false; if (!("ontouchstart" in root)) input.focus(); }
    load().then(function () {
      var local = answer(q, prevReq);
      prevReq = local.req;
      return new Promise(function (ok) { setTimeout(ok, Math.max(0, 450 - (Date.now() - t0))); }).then(function () {
        renderResult(local, bubble);
        scrollTo(u);
        var text = local.text.join("\n");
        if (!SERVER) { history.push({ role: "assistant", content: text }); return; }
        // the live site: Claude answers like a chat, from the whole catalogue; the lists stay the engine's unless Claude corrects them
        var tx = bubble.querySelector(".ai-text");
        var note = el("p", "ai-note", '<span class="ai-dots"><i></i><i></i><i></i></span> Writing a fuller answer…');
        tx.parentNode.insertBefore(note, tx.nextSibling);
        var ref = function (e) { return { id: e.f.id, model: modelName(e) || "" }; };
        var body = { messages: history.slice(-12), page: panel.dataset.page, engine: text, stream: true,
          fits: local.fits.slice(0, 90).map(ref), maybe: local.maybe.slice(0, 30).map(ref), closest: local.closest.map(ref) };
        var acc = "", final = null;
        function finish(j) {
          if (note.parentNode) note.parentNode.removeChild(note);
          if (!j || j.error || !j.answer) {
            if (j && (j.error === "not_configured" || j.error === "bad_json")) SERVER = false;
            tx.innerHTML = md(text);
            history.push({ role: "assistant", content: text });
            return;
          }
          tx.innerHTML = md(j.answer);
          var R = j.results || {};
          if (!R.use_engine && (R.fits && R.fits.length || R.maybe && R.maybe.length)) {
            var mine = { req: local.req, fits: picks(R.fits, local.req), maybe: picks(R.maybe, local.req), closest: [], chips: local.chips, page: local.page, mode: local.mode === "hit" ? "hit" : local.mode };
            if (mine.fits.length || mine.maybe.length) {
              if (mine.fits[0]) mine.page = pageBySlug(mine.fits[0].f.page) || local.page;
              renderLists(mine, bubble);
            }
          }
          history.push({ role: "assistant", content: j.answer });
        }
        return fetch("ask.php", { method: "POST", headers: { "Content-Type": "application/json", "Accept": "text/event-stream, application/json" }, body: JSON.stringify(body) })
          .then(function (r) {
            var ct = r.headers.get("Content-Type") || "";
            if (ct.indexOf("event-stream") < 0 || !r.body || !r.body.getReader || !root.TextDecoder) {
              return r.json().then(finish, function () { finish({ error: "bad_json" }); });
            }
            var reader = r.body.getReader(), dec = new root.TextDecoder(), buf = "";
            function pump() {
              return reader.read().then(function (x) {
                if (x.done) return finish(final || (acc ? { answer: visible(acc) } : { error: "empty" }));
                buf += dec.decode(x.value, { stream: true });
                var parts = buf.split("\n\n");
                buf = parts.pop();
                parts.forEach(function (part) {
                  var data = part.split("\n").filter(function (l) { return l.indexOf("data:") === 0; }).map(function (l) { return l.slice(5).trim(); }).join("");
                  if (!data) return;
                  var j;
                  try { j = JSON.parse(data); } catch (e) { return; }
                  if (j.t) { acc += j.t; tx.innerHTML = md(visible(acc)); }
                  else if (j.error) final = j;
                  else if (j.done) final = { answer: j.answer != null ? j.answer : visible(acc), results: j.results, model: j.model };
                });
                return pump();
              });
            }
            return pump();
          })
          .catch(function () { finish({ error: "network" }); });
      });
    }).catch(function () {
      bubble.className = "ai-msg ai-assistant";
      bubble.innerHTML = '<span class="ai-avatar" aria-hidden="true">AI</span><div class="ai-text"><p>The machine finder could not load the catalogue. Please call <a href="tel:+16475265510">+1 647 526 5510</a> or email info@NovoTechMachineTools.com.</p></div>';
    }).then(done, done);
  }

  form.addEventListener("submit", function (e) { e.preventDefault(); var q = input.value; input.value = ""; autosize(); ask(q); });
  input.addEventListener("keydown", function (e) { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event("submit")); } });
  function autosize() { input.style.height = "auto"; input.style.height = Math.min(140, input.scrollHeight + 2) + "px"; }
  input.addEventListener("input", autosize);
  panel.addEventListener("click", function (e) {
    var b = e.target.closest(".ai-chips button, .ai-suggest button");
    if (b) ask(b.textContent);
  });
  load().catch(function () {});
  root.NTFinderAsk = ask;                    // the home page's search boxes ask through the panel
  if (root.NT_AI_PENDING) { var pending = root.NT_AI_PENDING; root.NT_AI_PENDING = null; ask(pending); }
  else if (!("ontouchstart" in root)) input.focus();
})(typeof window !== "undefined" ? window : globalThis);
