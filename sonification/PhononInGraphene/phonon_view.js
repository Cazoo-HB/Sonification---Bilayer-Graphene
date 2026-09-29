/* Read-only spectrum display plus a draggable angle cursor. */
autowatch = 1;
inlets = 1;
outlets = 1;
include("phonon_data.js");
include("phonon_core.js");
mgraphics.init();
mgraphics.relative_coords = 0;
mgraphics.autofill = 0;
var s = Phonon.defaults();
var colors = [[0.30,0.83,0.80,1],[0.57,0.77,0.97,1],[0.73,0.62,0.98,1],
              [0.96,0.67,0.43,1],[0.96,0.48,0.57,1],[0.83,0.86,0.51,1]];
var labels = ["ZA / ZO'","TA","LA","ZO","TO","LO"];
function state() {
    var a=arrayfromargs(arguments);
    s.angle=a[0];s.mode=a[1];s.mapping=a[2];s.low=a[3];s.high=a[4];
    s.root=a[5];s.octaves=a[6];s.partner=a[7];s.samplerate=a[8];
    s.gains=a.slice(9,15);
    mgraphics.redraw();
}
function label(text,x,y,size,color) {
    mgraphics.set_source_rgba(color||[0.73,0.77,0.82,1]);
    mgraphics.select_font_face("Arial");mgraphics.set_font_size(size||12);
    mgraphics.move_to(x,y);mgraphics.show_text(text);
}
function line(x,y,x2,y2,color,width) {
    mgraphics.set_source_rgba(color);mgraphics.set_line_width(width||1);
    mgraphics.move_to(x,y);mgraphics.line_to(x2,y2);mgraphics.stroke();
}
function paint() {
    var w=box.rect[2]-box.rect[0],h=box.rect[3]-box.rect[1];
    var left=43,right=w-20,top=42,bottom=255;
    var plotw=right-left,ploth=bottom-top;
    mgraphics.set_source_rgba(0.075,0.10,0.135,1);mgraphics.rectangle(0,0,w,h);mgraphics.fill();
    label("PHONON DISPERSION",18,23,12,[0.9,0.93,0.96,1]);
    label("meV",left,top-7,10);
    for(var e=0;e<=200;e+=50){
        var yy=bottom-e/200*ploth;
        line(left,yy,right,yy,[0.2,0.24,0.29,1]);label(String(e),8,yy+4,10);
    }
    for(var t=0;t<=60;t+=10){
        var xx=left+t/60*plotw;
        line(xx,top,xx,bottom,[0.16,0.20,0.25,1]);label(String(t),xx-6,bottom+19,10);
    }
    // These strips identify where the TBG experiment does not resolve phonons.
    mgraphics.set_source_rgba(0.85,0.72,0.42,0.07);
    mgraphics.rectangle(left,top,plotw/10,ploth);mgraphics.fill();
    mgraphics.rectangle(right-plotw/10,top,plotw/10,ploth);mgraphics.fill();
    for(var branch=0;branch<6;branch++){
        for(var bank=1;bank>=0;bank--){
            var c=colors[branch].slice(0);c[3]=bank?(s.partner>0?0.38:0.12):0.95;
            mgraphics.set_source_rgba(c);mgraphics.set_line_width(bank?1:1.6);
            for(var k=0;k<=300;k++){
                var theta=k/5;
                var en=Phonon.energy(bank?60-theta:theta)[branch];
                var x=left+theta/60*plotw,y=bottom-en/200*ploth;
                if(k===0){mgraphics.move_to(x,y);}else{mgraphics.line_to(x,y);}
            }
            mgraphics.stroke();
        }
    }
    var cx=left+s.angle/60*plotw;
    line(cx,top,cx,bottom,[0.95,0.96,0.98,0.9],1);
    label(s.angle.toFixed(1)+" deg",Math.max(left,Math.min(cx-17,right-48)),top-12,11,[1,1,1,1]);
    var r=Phonon.calculate(s);
    for(branch=0;branch<6;branch++){
        mgraphics.set_source_rgba(colors[branch]);
        var cy=bottom-r.voices[branch].energy/200*ploth;
        mgraphics.ellipse(cx-3,cy-3,6,6);mgraphics.fill();
    }
    label("Twist angle (degrees)  /  drag the cursor",left,300,11);
    label("A: q(theta)    B: q(60 - theta), faint curves",left,321,11);
    line(18,342,w-18,342,[0.2,0.25,0.31,1]);
    label("BRANCH",18,370,10);label("A / meV",127,370,10);
    label("A / Hz",228,370,10);label("B / meV",375,370,10);label("B / Hz",482,370,10);
    label("LEVEL*",620,370,10);
    for(branch=0;branch<6;branch++){
        var yrow=402+branch*37;
        line(18,yrow+12,w-18,yrow+12,[0.13,0.18,0.23,1]);
        label(labels[branch],18,yrow,13,colors[branch]);
        for(bank=0;bank<2;bank++){
            var v=r.voices[branch+bank*6],bx=bank?375:127;
            var col=bank&&!s.partner?[0.40,0.45,0.51,1]:[0.90,0.93,0.96,1];
            label(v.energy.toFixed(2),bx,yrow,13,col);
            label(v.hz.toFixed(1)+(v.inBand?"":" x"),bank?482:228,yrow,13,col);
        }
    }
    label("x = outside audible range, muted.   *Level applies to both momentum paths.",18,637,10);
    label("Digitized model curves, Fig. 1f. Graphite proxy; no measured amplitude weighting.",18,658,10);
}
function onclick(x,y) { if(y<290){outlet(0,Phonon.clamp((x-43)/(box.rect[2]-box.rect[0]-63)*60,0,60));} }
function ondrag(x,y) { onclick(x,Math.min(y,289)); }
function onresize(){mgraphics.redraw();}
onresize.local=1;
