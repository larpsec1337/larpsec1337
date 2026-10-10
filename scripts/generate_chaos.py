from __future__ import annotations

import json
import math
import os
import random
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

USER = os.getenv("PROFILE_USER", "Larpsec1337")
TOKEN = os.getenv("GITHUB_TOKEN", "")

MONO = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
]
BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf",
]

def font(size, bold=False):
    for p in (BOLD if bold else MONO):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def gh():
    req = urllib.request.Request(
        f"https://api.github.com/users/{USER}",
        headers={
            "User-Agent": "Larpsec1337-profile-generator",
            "Accept": "application/vnd.github+json",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return json.load(r)
    except Exception:
        return {"public_repos":"?","followers":"?","following":"?"}

def txt(d, xy, s, size=12, color=(235,235,235), bold=False, anchor=None):
    d.text(xy, str(s), font=font(size,bold), fill=color, anchor=anchor)

def scanlines(d, w, h, step=4):
    for y in range(0,h,step):
        d.line((0,y,w,y), fill=(10,10,14))

def noise(d,w,h,rng,n=500):
    palette=[(10,0,20),(0,18,22),(28,0,10),(18,18,18),(0,25,10)]
    for _ in range(n):
        d.point((rng.randrange(w),rng.randrange(h)), fill=rng.choice(palette))

def save(frames, name, duration=70, colors=96):
    frames=[f.convert("P", palette=Image.Palette.ADAPTIVE, colors=colors) for f in frames]
    frames[0].save(ASSETS/name,save_all=True,append_images=frames[1:],duration=duration,loop=0,disposal=2,optimize=False)

def glitch(img, seed, bands=8):
    rng=random.Random(seed)
    out=img.copy()
    w,h=out.size
    for _ in range(bands):
        y=rng.randrange(max(1,h-8))
        bh=rng.randrange(2,min(16,h-y))
        dx=rng.randrange(-28,29)
        band=out.crop((0,y,w,y+bh))
        out.paste(band,(dx,y))
    return out

def titlebar(d, box, label, accent):
    x0,y0,x1,y1=box
    d.rectangle(box,fill=(4,4,8),outline=accent,width=2)
    d.rectangle((x0,y0,x1,y0+24),fill=accent)
    txt(d,(x0+7,y0+4),label,12,(0,0,0),True)
    txt(d,(x1-18,y0+3),"×",14,(0,0,0),True)

def main_chaos(stats):
    W,H=960,540
    out=[]
    lines=[
        "mount /dev/reality /mnt/README",
        "grep -R meaning /proc/self -> 0 results",
        "normal presentation layer unavailable",
        "recursive profile mirror mounted",
        "sudo rm -rf /boring/profile",
        "segfault at 0xDEADC0DE: aesthetics overflow",
        "README observing README observing README",
        "semantic checksum mismatch",
        "packet destination: ???",
        "graph causality: NOT FOUND",
    ]
    for f in range(48):
        rng=random.Random(10000+f)
        im=Image.new("RGB",(W,H),(0,0,0))
        d=ImageDraw.Draw(im)
        noise(d,W,H,rng,900); scanlines(d,W,H)
        for x in range(-80,W+80,40):
            c=(255,235,0) if ((x//40+f//2)&1) else (0,0,0)
            d.polygon([(x+f*5%80,0),(x+40+f*5%80,0),(x+24+f*5%80,28),(x-16+f*5%80,28)],fill=c)
        txt(d,(14,36),f"// {USER.upper()} // PROFILE CONTAINMENT FAILURE // FRAME {f:04d}",20,(255,60,160),True)
        txt(d,(14,64),"INFORMATION DENSITY HAS EXCEEDED RECOMMENDED HUMAN LIMITS",13,(0,255,220),True)

        warnings=["DO NOT REFRESH","THE README IS LOOKING BACK","404 REALITY NOT FOUND","TOO MANY LAYERS","NORMALITY DEPRECATED"]
        if f%4:
            txt(d,(W//2,112),warnings[(f//6)%len(warnings)],34,(255,235,0),True,"mm")

        titlebar(d,(18,145,535,300),"root@github:/proc/profile",(0,255,190))
        yy=180
        for i in range(7):
            txt(d,(30,yy),lines[(f+i)%len(lines)],11,(210,235,228))
            yy+=16

        x0,y0,x1,y1=550,145,942,300
        d.rectangle((x0,y0,x1,y1),fill=(235,225,195),outline=(155,20,70),width=3)
        d.rectangle((x0,y0,x1,y0+30),fill=(255,90,150))
        txt(d,(558,151),"LARPSEC1337 // UNVERIFIED ENTITY",13,(15,0,8),True)
        info=[
            ("TYPE","profile / containment breach"),
            ("STATUS","REDACTED" if f%2==0 else "rendering"),
            ("THREAT",f"{(f*37)%100:02d}% aesthetic hazard"),
            ("ORIGIN","github.com/Larpsec1337"),
            ("CANON","disputed by 14 editors"),
            ("NOTES","[citation needed] x 9000"),
        ]
        yy=184
        for k,v in info:
            txt(d,(558,yy),k,11,(100,0,45),True); txt(d,(648,yy),v,11,(25,20,24)); yy+=18

        d.rectangle((18,316,585,517),fill=(14,7,5),outline=(180,80,30),width=2)
        txt(d,(30,325),"EVIDENCE BOARD // ALL ARROWS POINT BACK TO README.md",12,(255,180,40),True)
        cards=[(40,360,"COMMIT\n7f3a??"),(177,395,"BADGE\nSERVICE"),(317,354,"STATIC\nNOISE"),(452,405,"PROFILE\nMIRROR"),(260,458,"YOU ARE\nHERE")]
        centers=[]
        for i,(x,y,label) in enumerate(cards):
            ww,hh=94,48; centers.append((x+ww//2,y+hh//2))
            d.rectangle((x,y,x+ww,y+hh),fill=((255,120,170) if i==4 else (245,235,180)),outline=(0,0,0))
            a,b=label.split("\n"); txt(d,(x+7,y+7),a,10,(20,10,10),True); txt(d,(x+7,y+23),b,10,(20,10,10),True)
        for i,a in enumerate(centers):
            b=centers[(i*2+2+f//7)%len(centers)]
            d.line((a,b),fill=(255,35,35),width=2)

        d.rectangle((603,316,942,517),fill=(3,3,9),outline=(110,0,220),width=2)
        txt(d,(614,326),"CAUSALITY GRAPH (DO NOT INTERPRET)",12,(180,90,255),True)
        nodes=[(650,370),(730,345),(835,375),(690,445),(835,465),(625,465)]
        labels=["README","404","YOU","ROOT","???","ORIGIN"]
        for i,a in enumerate(nodes):
            for j,b in enumerate(nodes):
                if j>i and (i+j+f)%3==0:
                    d.line((a,b),fill=(130,0,255),width=1)
        for i,((x,y),lab) in enumerate(zip(nodes,labels)):
            r=7+((f+i)%4); d.ellipse((x-r,y-r,x+r,y+r),fill=(0,255,220),outline=(255,255,255)); txt(d,(x+10,y-8),lab,10,(255,80,180),True)

        d.rectangle((0,519,W,539),fill=(255,0,120))
        ticker=" // ".join(["NO JAVASCRIPT","GIF HALLUCINATION ENGINE","README IS A CONTAINMENT VESSEL","THERE IS NO FINAL LAYER"])
        tw=d.textbbox((0,0),ticker,font=font(12,True))[2]
        x=-((f*13)%max(1,tw))
        txt(d,(x,521),ticker+" // "+ticker,12,(0,0,0),True)
        out.append(glitch(im,9000+f,10))
    save(out,"chaos.gif",65,128)

def ticker(stats):
    W,H=960,120; out=[]
    line=f"LARPSEC1337 // REPOS={stats.get('public_repos')} // FOLLOWERS={stats.get('followers')} // NORMAL PROFILE MODULE REMOVED // README CONTAINS README CONTAINING README // "
    for f in range(40):
        im=Image.new("RGB",(W,H),(0,0,0)); d=ImageDraw.Draw(im); scanlines(d,W,H)
        d.rectangle((0,0,W,22),fill=(255,235,0)); txt(d,(10,2),"EMERGENCY BROADCAST SYSTEM // PROFILE CORRUPTION EVENT",13,(0,0,0),True)
        tw=d.textbbox((0,0),line,font=font(18,True))[2]
        x=W-((f*30)%(tw+W)); txt(d,(x,42),line+line,18,(0,255,210),True)
        txt(d,(10,82),"██████▒▒▒ DO NOT ATTEMPT TO FORM A COHERENT MODEL OF THIS PAGE ▒▒▒██████",12,(255,0,130),True)
        out.append(im)
    save(out,"ticker.gif",60,64)

def portal():
    W,H=960,260; out=[]
    for f in range(40):
        im=Image.new("RGB",(W,H),(0,0,0)); d=ImageDraw.Draw(im); scanlines(d,W,H)
        cx,cy=W//2,H//2
        for i in range(26):
            phase=(f*9+i*17)%360
            scale=1-((i+f*.45)%26)/29
            ww=int(900*scale); hh=int(220*scale)
            col=((phase*5)%256,(255-phase)%256,(phase*7)%256)
            d.rectangle((cx-ww//2,cy-hh//2,cx+ww//2,cy+hh//2),outline=col,width=2)
        txt(d,(cx,36),"README WITHIN README WITHIN README",23,(255,235,0),True,"mm")
        txt(d,(cx,67),"THE CENTER IS NOT A DESTINATION",13,(0,255,220),True,"mm")
        for n in range(12):
            a=f*.18+n*math.tau/12; r=42+n*5
            x=cx+int(math.cos(a)*r); y=cy+20+int(math.sin(a)*r*.48)
            d.ellipse((x-4,y-4,x+4,y+4),fill=(255,0,130))
        txt(d,(cx,226),f"DEPTH={(f%17)+1:02d} // ESCAPE VECTOR=NULL // LOOP={f:02d}",12,(180,90,255),True,"mm")
        out.append(glitch(im,5000+f,5))
    save(out,"portal.gif",65,96)

def crashswarm():
    W,H=960,300; out=[]
    messages=[
        ("README.EXE","A normal profile was detected.","[ DELETE NORMALITY ]"),
        ("git","fatal: refusing to merge unrelated realities","[ allow-unrelated-histories ]"),
        ("kernel32.dll","Aesthetic overflow at 0xDEADC0DE","[ IGNORE ] [ PANIC ]"),
        ("browser","This tab has become conceptually recursive.","[ OK? ]"),
        ("wiki","Citation loop detected.","[ citation needed ]"),
        ("system","Too many windows. Opening more windows.","[ understandable ]"),
    ]
    for f in range(34):
        rng=random.Random(7000+f)
        im=Image.new("RGB",(W,H),(5,7,12)); d=ImageDraw.Draw(im); noise(d,W,H,rng,250); scanlines(d,W,H)
        for i in range(10):
            title,msg,button=messages[(i+f//4)%len(messages)]
            x=(53*i+f*11)%760; y=(29*i+f*7)%190
            w=180+(i%3)*25; h=86
            d.rectangle((x,y,x+w,y+h),fill=(205,205,205),outline=(255,255,255))
            d.rectangle((x,y,x+w,y+20),fill=((0,45,150) if i%2 else (120,0,120)))
            txt(d,(x+5,y+3),title,10,(255,255,255),True)
            for j,line in enumerate([msg[:29],msg[29:58]]):
                txt(d,(x+8,y+30+j*14),line,9,(0,0,0))
            txt(d,(x+w//2,y+h-16),button,8,(0,0,0),True,"mm")
        txt(d,(W//2,H-18),"ERROR DIALOG SWARM // ALL BUTTONS ARE PLACEBOS",12,(255,235,0),True,"mm")
        out.append(glitch(im,7100+f,7))
    save(out,"crashswarm.gif",75,96)

def surveillance(stats):
    W,H=960,330; out=[]
    for f in range(36):
        rng=random.Random(8000+f)
        im=Image.new("RGB",(W,H),(0,0,0)); d=ImageDraw.Draw(im); scanlines(d,W,H)
        cols,rows=4,2; pad=10; cw=(W-pad*(cols+1))//cols; ch=(H-52-pad*(rows+1))//rows
        for r in range(rows):
            for c in range(cols):
                x=pad+c*(cw+pad); y=pad+r*(ch+pad)
                d.rectangle((x,y,x+cw,y+ch),fill=(2,12,10),outline=(0,255,120))
                for _ in range(60):
                    xx=x+rng.randrange(cw); yy=y+rng.randrange(ch); d.point((xx,yy),fill=(0,rng.randrange(40,160),rng.randrange(20,90)))
                txt(d,(x+5,y+5),f"CAM-{r}{c} // {(f*7+c*13+r*9)%100:02d}:13:37",9,(0,255,120),True)
                cx=x+cw//2+int(math.sin(f*.2+c)*25); cy=y+ch//2+int(math.cos(f*.15+r)*14)
                d.rectangle((cx-20,cy-16,cx+20,cy+16),outline=(255,0,110),width=2)
                txt(d,(cx,cy+23),["README","YOU","404","ROOT"][(c+r)%4],9,(255,0,110),True,"mm")
        txt(d,(W//2,H-31),f"OBSERVATION GRID // followers={stats.get('followers','?')} // every camera points at the same README",11,(255,235,0),True,"mm")
        out.append(im)
    save(out,"surveillance.gif",75,64)

def terminalrain():
    W,H=960,280; out=[]
    glyphs="01ABCDEF<>[]{}#$%&*?LARPSEC1337"
    cols=80
    drops=[(i,random.Random(42+i).randrange(-H,H),random.Random(999+i).randrange(2,9)) for i in range(cols)]
    for f in range(36):
        im=Image.new("RGB",(W,H),(0,0,0)); d=ImageDraw.Draw(im)
        for col,y0,speed in drops:
            x=col*12
            for n in range(13):
                y=(y0+f*speed*5-n*16)%(H+160)-80
                ch=glyphs[(col+n+f)%len(glyphs)]
                bright=max(35,255-n*17)
                txt(d,(x,y),ch,11,(0,bright,min(210,bright//2)),n<2)
        d.rectangle((15,18,945,58),fill=(0,0,0),outline=(255,0,140),width=2)
        txt(d,(W//2,38),">_ STREAMING RAW PROFILE MEMORY // DO NOT PIPE TO /DEV/BRAIN",14,(255,0,140),True,"mm")
        out.append(im)
    save(out,"terminalrain.gif",70,64)

def conspiracy():
    W,H=960,320; out=[]
    base=[(95,90,"PROFILE"),(260,60,"README"),(440,110,"GIF"),(680,70,"ACTION"),(820,145,"YOU"),(540,235,"???"),(210,235,"SOURCE")]
    for f in range(40):
        im=Image.new("RGB",(W,H),(19,10,4)); d=ImageDraw.Draw(im)
        rng=random.Random(900+f)
        for _ in range(420):
            x=rng.randrange(W); y=rng.randrange(H); d.point((x,y),fill=(55+rng.randrange(35),34,10))
        for i,a in enumerate(base):
            for j,b in enumerate(base):
                if j>i and ((i*7+j*11+f//4)%4)!=0:
                    d.line((a[0],a[1],b[0],b[1]),fill=(210,25,25),width=2)
        for i,(x,y,label) in enumerate(base):
            angle=math.sin(f*.2+i)*4
            w,h=110,52
            d.rectangle((x-w//2,y-h//2,x+w//2,y+h//2),fill=(245,235,180),outline=(0,0,0))
            txt(d,(x,y-8),label,12,(10,10,10),True,"mm")
            txt(d,(x,y+10),f"FILE {(i*13+f)%97:02d}",9,(100,0,0),True,"mm")
        txt(d,(W//2,295),"EVERY RED LINE IS EVIDENCE THAT RED LINES EXIST",13,(255,235,0),True,"mm")
        out.append(glitch(im,2222+f,4))
    save(out,"conspiracy.gif",80,96)

def wikimeltdown():
    W,H=960,320; out=[]
    for f in range(36):
        im=Image.new("RGB",(W,H),(238,233,220)); d=ImageDraw.Draw(im)
        accent=(180,20,80)
        d.rectangle((0,0,W,38),fill=(170,170,170)); txt(d,(14,8),"Larpsec Wiki, the unreliable encyclopedia",16,(20,20,20),True)
        txt(d,(18,54),"Larpsec1337",27,(20,20,20),True)
        txt(d,(18,88),"From Larpsec Wiki",10,(80,80,80))
        d.line((18,108,650,108),fill=(80,80,80),width=1)
        paragraphs=[
            "Larpsec1337 is a disputed GitHub entity whose profile allegedly contains",
            "an excessive number of mutually contradictory interface metaphors.",
            "The exact number of layers is unknown because editors keep adding layers.",
            "This article may contain original research, generated GIFs, and bad ideas.",
        ]
        yy=120
        for p in paragraphs:
            txt(d,(20,yy),p,11,(25,25,25)); yy+=18
        x0=670; d.rectangle((x0,56,942,286),fill=(250,245,230),outline=accent,width=2)
        d.rectangle((x0,56,942,82),fill=(255,100,160)); txt(d,(806,69),"Larpsec1337",13,(30,0,10),True,"mm")
        fields=[("Status","REDACTED" if f%2==0 else "citation needed"),("Type","profile entity"),("Canon","disputed"),("Threat",f"{(f*17)%100}%"),("Source","[1][2][1][2]"),("Meaning","merge conflict")]
        yy=96
        for k,v in fields:
            txt(d,(680,yy),k,10,(90,0,40),True); txt(d,(760,yy),v,10,(30,30,30)); yy+=28
        if f%6<3:
            d.rectangle((110,205,620,260),fill=(255,230,120),outline=(160,90,0),width=2)
            txt(d,(365,219),"THIS ARTICLE MAY REQUIRE CLEANUP",13,(90,40,0),True,"mm")
            txt(d,(365,240),"No editor has agreed on what cleanup means.",10,(90,40,0),False,"mm")
        out.append(glitch(im,3333+f,3))
    save(out,"wikimeltdown.gif",85,96)

def oscilloscope():
    W,H=960,260; out=[]
    for f in range(42):
        im=Image.new("RGB",(W,H),(0,5,2)); d=ImageDraw.Draw(im)
        for x in range(0,W,24): d.line((x,0,x,H),fill=(0,30,15))
        for y in range(0,H,24): d.line((0,y,W,y),fill=(0,30,15))
        traces=[((0,255,110),0.0,1.0),((255,0,140),0.8,1.8),((0,180,255),1.5,2.7)]
        for color,phase,mult in traces:
            pts=[]
            for x in range(W):
                t=x/40+f*.18+phase
                y=H//2+int(math.sin(t*mult)*42+math.sin(t*3.3)*10)
                pts.append((x,y))
            d.line(pts,fill=color,width=2)
        txt(d,(14,14),"OSCILLOSCOPE // SEMANTIC NOISE FLOOR",13,(255,235,0),True)
        txt(d,(14,38),f"CH1 README   CH2 PROFILE   CH3 ???   FRAME {f:02d}",11,(0,255,110))
        txt(d,(W-14,H-16),"TRIGGER: EVERYWHERE",11,(255,0,140),True,"rs")
        out.append(im)
    save(out,"oscilloscope.gif",65,64)

def footer():
    W,H=960,170; out=[]
    lines=["END OF DOCUMENT","THIS CLAIM IS FALSE","KEEP SCROLLING","NO MORE LAYERS","ANOTHER LAYER DETECTED","EOF? DENIED"]
    for f in range(36):
        im=Image.new("RGB",(W,H),(0,0,0)); d=ImageDraw.Draw(im); scanlines(d,W,H)
        for i in range(7):
            y=18+i*20
            s=lines[(i+f//3)%len(lines)]
            x=((f*21+i*97)%(W+400))-200
            txt(d,(x,y),s,14,((255 if i%2==0 else 0),(0 if i%3 else 255),(180 if i%2 else 255)),True)
        d.rectangle((0,H-26,W,H),fill=(255,235,0))
        txt(d,(W//2,H-13),"THE PROFILE ENDS HERE EXCEPT FOR THE PART WHERE IT DOES NOT",12,(0,0,0),True,"mm")
        out.append(glitch(im,4444+f,8))
    save(out,"footer.gif",70,64)

def main():
    stats=gh()
    main_chaos(stats)
    ticker(stats)
    portal()
    crashswarm()
    surveillance(stats)
    terminalrain()
    conspiracy()
    wikimeltdown()
    oscilloscope()
    footer()
    print("generated:")
    for p in sorted(ASSETS.glob("*.gif")):
        print(" -", p.name)

if __name__=="__main__":
    main()
