---
title: "Portable CPAP machine: The prequel"
date: 2022-05-17T16:23:24-05:00
---

Alternative title: The math guy tries to do things in the real world. It's jank.

I have been using a CPAP machine for a few years now. I sleep better, and so do the people around me. Ideally I wouldn't have to use one, but for now, it is a net positive.

A huge problem is that I basically bring it everywhere. I would like a portable CPAP machine that I can bring with me for travel, especially travel that involves little to no power availablity (camping, bikepacking, etc). 

Now that USB-C is a thing and can provide a decent amount of power, I figure I might as well give it a shot. The problem: I know basically nothing about electronics, I can't solder for shit, and I don't really have very much equipment. I also need to make components, so a 3D printer is also in order.

Things I already had:

- A USB-C power supply
- A soldering iron
- hope

Things I needed:

- A 3D printer
- A way to test different voltages, etc, i.e., a bench power supply.
- _Knowledge_ [tai lopez voice]

So I bought a Monoprice Select Mini V2 off a guy on Kijiji that works pretty well so far, although I have yet to figure out how to level the bed and get prints to stick reliably (or: get prints to unstick reliably).

The first thing I built was a bench power supply. Since I'm all in on that usb-c life, I figured, why not create a [USB-C bench power supply?](https://www.instructables.com/USB-C-Powered-Bench-Power-Supply/) . The overall components are fairly cheap, just requires a usb-c negotiator (usb-c power supplies and usb-c devices both have to negotiate on how much power they can provide / accept), a "buck boost converter", some wires and banana jacks and stuff. 

The case they provided was a bit too big for my lowly printer, but I did find a [different model](https://www.thingiverse.com/thing:5252156) that fit the print bed. Unfortunately, it wasn't a perfect fit volume wise. Luckily, I had tried to print it before and ran out of the little bit of filament the printer came with. So I just taped the two together. Is it jank? Very.

![It's ugly, but it works](/img/portable_cpap_prequel/jank_psu_front.jpg)
![Don't look.](/img/portable_cpap_prequel/jank_psu_back.jpg)



Now, I just need to learn how to model things!

