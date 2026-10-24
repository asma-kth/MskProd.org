/* Pictures for the keep-or-remove levels. Every detail a student can remove is
 * a group marked data-d="id", so the engine can fade it out. In a map, .ph
 * parts are the photo look and .mp parts the drawn-map look shown once the
 * map is right. In an icon, .tile is the app background shown once it is right.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};
  CT.pics = CT.pics || {};

  function svg(w, h, label, body) {
    return '<svg viewBox="0 0 ' + w + " " + h + '" class="csel-svg" role="img" aria-label="' + label + '">' + body + "</svg>";
  }
  function g(id, body, extra) { return '<g data-d="' + id + '"' + (extra || "") + ">" + body + "</g>"; }

  CT.pics.football = function () {
    var heads = "", cols = ["#F59E0B", "#EF4444", "#3B82F6", "#10B981", "#8B5CF6", "#EC4899", "#F97316", "#14B8A6"];
    for (var i = 0; i < 30; i++) heads += '<circle cx="' + (6 + i * 12) + '" cy="' + (i % 2 ? 58 : 65) + '" r="5" fill="' + cols[i % cols.length] + '"/>';
    var stripes = "";
    for (var s = 0; s < 6; s++) stripes += '<rect x="' + s * 60 + '" y="72" width="30" height="148" fill="#16A34A" opacity=".35"/>';
    return svg(360, 220, "A football match at Riverside Park: a scoreboard, a clock, a cloud, a crowd, players, a dog and an ice-cream van",
      '<rect width="360" height="220" fill="#BAE6FD"/><rect y="72" width="360" height="148" fill="#22C55E"/>' + stripes +
      '<g fill="none" stroke="#F0FDF4" stroke-width="2"><rect x="8" y="82" width="344" height="132"/><line x1="180" y1="82" x2="180" y2="214"/><circle cx="180" cy="148" r="22"/><rect x="318" y="118" width="34" height="60"/></g>' +
      '<rect x="348" y="130" width="8" height="36" fill="#fff" opacity=".8"/>' +
      g("weather", '<ellipse cx="42" cy="28" rx="24" ry="12" fill="#F8FAFC"/><ellipse cx="60" cy="21" rx="16" ry="12" fill="#F8FAFC"/><ellipse cx="30" cy="21" rx="13" ry="10" fill="#F1F5F9"/>') +
      g("kickoff", '<circle cx="104" cy="24" r="15" fill="#fff" stroke="#0F172A" stroke-width="3"/><path d="M104 24 V13 M104 24 L112 19" stroke="#0F172A" stroke-width="2.5" stroke-linecap="round"/>') +
      g("ground", '<rect x="150" y="32" width="4" height="20" fill="#475569"/><rect x="222" y="32" width="4" height="20" fill="#475569"/><rect x="132" y="6" width="112" height="27" rx="4" fill="#1E3A8A"/><text x="188" y="24" text-anchor="middle" font-size="10" font-weight="800" fill="#fff">RIVERSIDE PARK</text>') +
      '<rect x="258" y="4" width="96" height="44" rx="5" fill="#0F172A"/>' +
      g("teams", '<text x="278" y="21" text-anchor="middle" font-size="11" font-weight="800" fill="#FDE68A">OAK</text><text x="334" y="21" text-anchor="middle" font-size="11" font-weight="800" fill="#FDE68A">RIV</text>') +
      g("score", '<text x="306" y="41" text-anchor="middle" font-size="16" font-weight="800" fill="#F87171">3 - 2</text>') +
      g("crowd", '<rect y="50" width="360" height="22" fill="#64748B"/>' + heads) +
      // a Riverside player, part of the scene whatever the job
      '<circle cx="222" cy="128" r="7" fill="#F1C27D"/><rect x="214" y="136" width="16" height="20" rx="4" fill="#2563EB"/><rect x="215" y="155" width="14" height="8" fill="#1E3A8A"/><path d="M218 163 v13 M226 163 v13" stroke="#F1C27D" stroke-width="4"/><path d="M214 178 h8 M222 178 h8" stroke="#111827" stroke-width="3"/>' +
      // an Oakfield player whose socks are the detail
      '<circle cx="122" cy="118" r="7" fill="#C68642"/><rect x="114" y="126" width="16" height="20" rx="4" fill="#16A34A"/><rect x="115" y="145" width="14" height="8" fill="#F8FAFC"/><path d="M118 153 v16 M126 153 v16" stroke="#C68642" stroke-width="4"/>' +
      g("socks", '<rect x="115" y="161" width="6" height="9" fill="#15803D"/><rect x="123" y="161" width="6" height="9" fill="#15803D"/><rect x="115" y="163" width="6" height="2" fill="#BBF7D0"/><rect x="123" y="163" width="6" height="2" fill="#BBF7D0"/>') +
      '<path d="M114 171 h8 M122 171 h8" stroke="#111827" stroke-width="3"/>' +
      g("scorer", '<text x="292" y="106" text-anchor="middle" font-size="9" font-weight="800" fill="#14532D">MIA</text><circle cx="292" cy="116" r="7" fill="#8D5524"/><rect x="284" y="124" width="16" height="20" rx="4" fill="#16A34A"/><text x="292" y="139" text-anchor="middle" font-size="10" font-weight="800" fill="#fff">9</text><rect x="285" y="143" width="14" height="8" fill="#F8FAFC"/><path d="M289 151 l-4 15 M295 151 l9 11" stroke="#8D5524" stroke-width="4" stroke-linecap="round"/><circle cx="326" cy="158" r="6" fill="#fff" stroke="#111827" stroke-width="1.5"/><path d="M312 156 h-9 M313 162 h-7" stroke="#fff" stroke-width="2" stroke-linecap="round"/>') +
      g("dog", '<path d="M186 190 q-9 -8 -4 -15" stroke="#92400E" stroke-width="3" fill="none"/><path d="M190 196 v9 M196 197 v9 M206 197 v9 M212 196 v9" stroke="#92400E" stroke-width="3"/><ellipse cx="200" cy="191" rx="16" ry="8" fill="#B45309"/><circle cx="216" cy="183" r="7" fill="#B45309"/><path d="M218 177 l6 -4 l0 8 z" fill="#78350F"/><circle cx="219" cy="182" r="1.6" fill="#111"/>') +
      g("icecream", '<rect x="14" y="176" width="70" height="30" rx="5" fill="#F9A8D4"/><rect x="60" y="182" width="20" height="12" rx="2" fill="#E0F2FE"/><rect x="19" y="182" width="36" height="14" rx="2" fill="#fff"/><text x="37" y="192" text-anchor="middle" font-size="7" font-weight="800" fill="#DC2626">SOLD OUT</text><path d="M34 176 l6 -14 l6 14 z" fill="#FBBF24"/><circle cx="40" cy="160" r="6" fill="#FEF3C7"/><circle cx="28" cy="207" r="6" fill="#1F2937"/><circle cx="70" cy="207" r="6" fill="#1F2937"/>')
    );
  };

  CT.pics.town = function () {
    function tree(x, y) { return '<rect x="' + (x - 2) + '" y="' + y + '" width="4" height="9" fill="#92400E"/><circle cx="' + x + '" cy="' + (y - 4) + '" r="8" fill="#16A34A"/>'; }
    function car(x, y, c) { return '<rect x="' + x + '" y="' + y + '" width="20" height="10" rx="3" fill="' + c + '"/><rect x="' + (x + 5) + '" y="' + (y + 2) + '" width="9" height="4" fill="#E0F2FE"/>'; }
    function person(x, y, c) { return '<circle cx="' + x + '" cy="' + y + '" r="3" fill="#F1C27D"/><path d="M' + x + " " + (y + 3) + " v8 m0 -5 h-4 m4 0 h4 m-4 5 l-3 6 m3 -6 l3 6" + '" stroke="' + c + '" stroke-width="2" fill="none"/>'; }
    var trees = [[100, 30], [150, 26], [20, 70], [160, 90], [270, 160], [330, 160], [100, 160], [160, 220], [330, 230], [260, 70]].map(function (t) { return tree(t[0], t[1]); }).join("");
    var road = function (d) { return '<path class="ph" d="' + d + '" stroke="#6B7280" stroke-width="16" fill="none"/><path class="ph" d="' + d + '" stroke="#F8FAFC" stroke-width="1.5" stroke-dasharray="6 6" fill="none"/>'; };
    var mroad = function (d) { return '<path class="mp" d="' + d + '" stroke="#94A3B8" stroke-width="12" fill="none"/><path class="mp" d="' + d + '" stroke="#fff" stroke-width="8" fill="none"/>'; };
    var R = ["M0 120 H360", "M44 120 V182", "M300 120 V46", "M130 0 V240", "M245 200 H360"];
    return svg(360, 240, "A busy picture of a town with a station, a library, a river and a bridge, roads, cars, people, trees, clouds, birds and adverts",
      '<rect class="bg" width="360" height="240" fill="#BBF7D0"/>' +
      g("bridge", '<path class="ph" d="M198 0 C188 60 230 80 210 120 S198 200 212 240 H242 C228 200 240 160 238 120 S222 60 228 0 Z" fill="#3B82F6"/>' +
        '<path class="mp" d="M198 0 C188 60 230 80 210 120 S198 200 212 240 H242 C228 200 240 160 238 120 S222 60 228 0 Z" fill="#BAE6FD"/>') +
      g("roads", R.map(road).join("") + R.map(mroad).join("")) +
      g("bridge", '<rect class="ph" x="196" y="110" width="50" height="20" fill="#A16207"/><path class="ph" d="M196 110 h50 M196 130 h50" stroke="#78350F" stroke-width="3"/>' +
        '<rect class="mp" x="196" y="112" width="50" height="16" fill="#fff" stroke="#334155" stroke-width="2"/>') +
      g("trees", trees) +
      g("station", '<g class="ph"><rect x="14" y="182" width="62" height="44" fill="#B91C1C"/><path d="M10 184 L45 166 L80 184 Z" fill="#7F1D1D"/><rect x="22" y="190" width="46" height="10" fill="#FEF3C7"/><text x="45" y="198" text-anchor="middle" font-size="7" font-weight="800" fill="#7F1D1D">STATION</text><rect x="38" y="206" width="14" height="20" fill="#451A03"/></g>' +
        '<g class="mp"><circle cx="45" cy="200" r="16" fill="#1D4ED8"/><rect x="37" y="190" width="16" height="16" rx="3" fill="#fff"/><rect x="40" y="193" width="10" height="5" fill="#1D4ED8"/><circle cx="41" cy="203" r="1.6" fill="#1D4ED8"/><circle cx="49" cy="203" r="1.6" fill="#1D4ED8"/><text x="45" y="230" text-anchor="middle" font-size="9" font-weight="800" fill="#0F172A">Station</text></g>') +
      g("library", '<g class="ph"><rect x="268" y="14" width="66" height="34" fill="#FDE68A"/><path d="M262 16 L301 2 L340 16 Z" fill="#B45309"/><path d="M276 20 v26 M290 20 v26 M312 20 v26 M326 20 v26" stroke="#B45309" stroke-width="4"/><text x="301" y="36" text-anchor="middle" font-size="7" font-weight="800" fill="#7C2D12">LIBRARY</text></g>' +
        '<g class="mp"><circle cx="300" cy="30" r="16" fill="#7C3AED"/><path d="M290 24 q5 -3 10 0 v13 q-5 -3 -10 0 z M300 24 q5 -3 10 0 v13 q-5 -3 -10 0 z" fill="#fff"/><text x="300" y="60" text-anchor="middle" font-size="9" font-weight="800" fill="#0F172A">Library</text></g>') +
      g("cars", car(80, 112, "#EF4444") + car(150, 124, "#F59E0B") + car(292, 70, "#8B5CF6") + car(310, 192, "#0EA5E9")) +
      g("people", person(60, 136, "#1E293B") + person(176, 100, "#BE185D") + person(258, 100, "#0F766E") + person(318, 140, "#1D4ED8") + person(112, 136, "#B45309")) +
      g("adverts", '<rect x="62" y="56" width="44" height="26" fill="#fff" stroke="#0F172A" stroke-width="2"/><text x="84" y="73" text-anchor="middle" font-size="9" font-weight="800" fill="#DC2626">SALE!</text><rect x="82" y="82" width="3" height="12" fill="#0F172A"/>' +
        '<rect x="256" y="132" width="48" height="24" fill="#FEF3C7" stroke="#0F172A" stroke-width="2"/><text x="280" y="148" text-anchor="middle" font-size="9" font-weight="800" fill="#EA580C">PIZZA</text>') +
      g("clouds", '<ellipse cx="40" cy="22" rx="20" ry="9" fill="#fff"/><ellipse cx="54" cy="16" rx="12" ry="9" fill="#fff"/><ellipse cx="180" cy="40" rx="18" ry="8" fill="#fff"/><ellipse cx="192" cy="34" rx="10" ry="8" fill="#fff"/>') +
      g("birds", '<path d="M150 60 q5 -5 10 0 q5 -5 10 0 M240 24 q4 -4 8 0 q4 -4 8 0 M110 96 q4 -4 8 0 q4 -4 8 0 M330 92 q4 -4 8 0 q4 -4 8 0" stroke="#1E293B" stroke-width="2" fill="none"/>') +
      // the walk itself and the key, drawn only once the map is right
      '<path class="mp" d="M45 182 V120 H300 V48" stroke="#DC2626" stroke-width="3" stroke-dasharray="7 5" fill="none"/>' +
      '<g class="mp"><rect x="262" y="176" width="92" height="58" rx="6" fill="#fff" stroke="#334155" stroke-width="1.5"/><text x="308" y="190" text-anchor="middle" font-size="8" font-weight="800" fill="#0F172A">KEY</text>' +
      '<circle cx="273" cy="201" r="5" fill="#1D4ED8"/><text x="282" y="204" font-size="8" fill="#0F172A">Station</text><circle cx="273" cy="214" r="5" fill="#7C3AED"/><text x="282" y="217" font-size="8" fill="#0F172A">Library</text>' +
      '<path d="M268 227 h10" stroke="#DC2626" stroke-width="2.5" stroke-dasharray="4 3"/><text x="282" y="230" font-size="8" fill="#0F172A">Your walk</text></g>'
    );
  };

  CT.pics.camera = function () {
    return svg(128, 128, "A detailed drawing of a camera",
      '<rect class="tile" x="2" y="2" width="124" height="124" rx="28" fill="#FDBA74"/>' +
      g("shadow", '<ellipse cx="64" cy="110" rx="48" ry="7" fill="#0F172A" opacity=".3"/>') +
      g("strap", '<path d="M16 58 C8 18 120 18 112 58" stroke="#92400E" stroke-width="5" fill="none"/>') +
      g("body", '<rect x="42" y="30" width="30" height="14" rx="3" fill="#334155"/><rect x="12" y="40" width="104" height="64" rx="12" fill="#475569"/>') +
      g("dials", '<rect x="90" y="33" width="16" height="7" rx="2" fill="#94A3B8"/><circle cx="24" cy="50" r="4" fill="#94A3B8"/><circle cx="104" cy="52" r="3" fill="#EF4444"/><circle cx="24" cy="62" r="3" fill="#94A3B8"/>') +
      g("brand", '<text x="64" y="49" text-anchor="middle" font-size="5.5" font-weight="800" fill="#E2E8F0">PIXELCAM 3000 PRO</text>') +
      g("lens", '<circle cx="64" cy="76" r="24" fill="#1E293B"/><circle cx="64" cy="76" r="17" fill="#0EA5E9"/><circle cx="64" cy="76" r="8" fill="#0C4A6E"/>') +
      g("scratches", '<path d="M20 92 l10 -6 M96 92 l9 4 M88 58 l7 3 M30 76 l5 5" stroke="#CBD5E1" stroke-width="1"/>') +
      g("shine", '<ellipse cx="57" cy="69" rx="6" ry="3" fill="#fff" opacity=".7"/><path d="M18 46 q20 -4 34 -2" stroke="#fff" stroke-width="3" opacity=".35" fill="none"/>')
    );
  };

  CT.pics.concert = function () {
    var crowd = "";
    for (var i = 0; i < 9; i++) crowd += '<circle cx="' + (8 + i * 14) + '" cy="' + (i % 2 ? 118 : 121) + '" r="7" fill="#111827" stroke="#475569"/>';
    return svg(128, 128, "A detailed drawing of a concert",
      '<rect class="tile" x="2" y="2" width="124" height="124" rx="28" fill="#DDD6FE"/>' +
      g("lights", '<path d="M6 0 L34 96 H58 Z" fill="#FDE68A" opacity=".5"/><path d="M122 0 L70 96 H94 Z" fill="#FDE68A" opacity=".5"/>') +
      g("stage", '<rect x="0" y="94" width="128" height="34" fill="#1F2937"/><rect x="0" y="94" width="128" height="4" fill="#F59E0B"/>') +
      g("guitarist", '<circle cx="20" cy="52" r="6" fill="#F1C27D"/><path d="M20 58 v20 m0 0 l-5 16 m5 -16 l5 16 m-5 -12 l8 -6" stroke="#1E293B" stroke-width="3" fill="none"/><ellipse cx="26" cy="74" rx="7" ry="5" fill="#B45309" transform="rotate(-30 26 74)"/><path d="M28 70 l12 -12" stroke="#78350F" stroke-width="2.5"/>') +
      g("tickets", '<rect x="86" y="8" width="36" height="18" rx="3" fill="#FDE68A" stroke="#B45309"/><text x="104" y="21" text-anchor="middle" font-size="9" font-weight="800" fill="#7C2D12">£25</text>') +
      g("note", '<ellipse cx="56" cy="84" rx="14" ry="10" fill="#7C3AED" transform="rotate(-20 56 84)"/><rect x="66" y="28" width="6" height="56" fill="#7C3AED"/><path d="M72 28 q18 6 20 26 q-6 -10 -20 -12 z" fill="#7C3AED"/>') +
      g("crowd", crowd)
    );
  };
})(typeof window !== "undefined" ? window : globalThis);
