/* Pure ES5 calculations, shared by Max, the display and verification scripts. */
var Phonon = (function () {
    var THZ_PER_MEV = 0.2417989242084918; // E = h f; h in eV s
    function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
    function energy(theta) {
        var t = clamp(theta, 0, 60) / PHONON_DATA.step_degrees;
        var i = Math.min(Math.floor(t), PHONON_DATA.rows.length - 1);
        var j = Math.min(i + 1, PHONON_DATA.rows.length - 1);
        var w = t - i, result = [];
        for (var b = 1; b <= 6; b++) {
            result.push(PHONON_DATA.rows[i][b] * (1-w) + PHONON_DATA.rows[j][b] * w);
        }
        return result;
    }
    function defaults() {
        return {angle: 15, mode: 0, mapping: 0, low: 30, high: 4000,
                root: 110, octaves: 1, partner: 0, glide: 60,
                samplerate: 44100, gains: [1,1,1,1,1,1]};
    }
    function zaPosition(theta) {
        var e0 = energy(0)[0], e60 = energy(60)[0];
        return Math.log(energy(theta)[0] / e0) / Math.log(e60 / e0);
    }
    function carrier(theta, mode, root, octaves) {
        var u = mode === 2 ? tuningPosition(theta) : theta / 60;
        return root * Math.pow(2, octaves * u);
    }
    function tuningPosition(theta) {
        // The digitized ZA curve is flat near Gamma. A stated 10% equal-step
        // component separates those reference pitches; the energy table is unchanged.
        return 0.9 * zaPosition(theta) + 0.1 * theta / 60;
    }
    function mapped(e, s) {
        if (e <= 0) { return 0; }
        var u = e / PHONON_DATA.energy_ceiling_meV;
        if (s.mapping === 1) { return s.low + (s.high-s.low) * u; }
        if (s.mapping === 2) { return s.low * Math.pow(s.high/s.low, u); }
        return s.high * u;
    }
    function calculate(s) {
        var theta = s.mode ? Math.round(clamp(s.angle,0,60)) : clamp(s.angle,0,60);
        var a = energy(theta), b = energy(60-theta), energies = a.concat(b);
        var ref = s.mode ? carrier(theta,s.mode,s.root,s.octaves) : mapped(a[0],s);
        var maxHz = Math.min(s.high, 0.45*s.samplerate, 20000);
        var voices = [], active = 0, outOfBand = 0;
        for (var i=0; i<12; i++) {
            var e = energies[i];
            var hz = s.mode ? (e > 0 ? ref * e / a[0] : 0) : mapped(e,s);
            var weight = s.gains[i%6] * (i>=6 ? s.partner : 1);
            var inBand = hz>=s.low && hz<=maxHz && e>0;
            if (inBand && weight>0) { active++; }
            if (!inBand && weight>0) { outOfBand++; }
            voices.push({energy:e, thz:e*THZ_PER_MEV, hz:hz,
                         oscillatorHz:inBand ? hz : 0,
                         amplitude:inBand ? weight : 0, inBand:inBand});
        }
        return {angle:theta, voices:voices, reference:ref, active:active,
                outOfBand:outOfBand, maxHz:maxHz};
    }
    function scale(mode, octaves) {
        var cents=[];
        for (var i=0;i<=60;i++) {
            cents.push(1200 * octaves * (mode===2 ? tuningPosition(i) : i/60));
        }
        return cents;
    }
    return {clamp:clamp, energy:energy, defaults:defaults, calculate:calculate,
            carrier:carrier, zaPosition:zaPosition, tuningPosition:tuningPosition, scale:scale,
            THZ_PER_MEV:THZ_PER_MEV};
}());
