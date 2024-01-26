---
title: "Portable CPAP 02: Sadness"
date: 2022-07-08T23:30:20-04:00
draft: true
---

I have since tried my hand at a little bit of CAD modelling. I initially started with FreeCAD which seeemed to work ok, although I found it a bit confusing. I then stumbled upon [SolveSpace](https://solvespace.org). It's hard for me to overstate how much I love how the program looks. It feels like a terminal. The same inner hipster that got me using Vim is ecstatic. I feel like it's pretty barebones but I'm willing to put up with it for something that looks so cool. 

I have tried a few iterations at a [volute chamber](https://en.wikipedia.org/wiki/Volute_(pump)) , drawing lots of inspiration from [Matthias Wandel's blower experiments](https://woodgears.ca/dust_collector/blower_build.html). 

### Iteration 1

I think I actually modelled this one in FreeCAD. 

The "volute" chamber doesn't actually increase in radius as air travels along the walls. It wasn't very efficient. 

### Iteration 2

I modelled this one in solvespace. I tried it and it also didn't work very well. It was printed in one piece, so it was _very_ difficult to remove the impeller after installing it. I also realized I didn't have a good way of attaching a top to this, so I gave up on the design. I also didn't realize I needed supports for the nozzle, so that didn't turn out very well lol. 

### Iteration 3

I'm pretty happy with this one as far as designing it goes. The performance is still not very good, though. I designed it in three parts: the bottom (where the motor is mounted), the walls, and the top. I hacked in some sort of lip and groove sort of thing (I don't think that's the right term) and it fits together well enough. I might need to clean up some of the print artifacts to get it to stick together better. I also remembered to add supports in the slicer and the nozzle turned out much better. 

I have a feeling that the motor just isn't spinning the thing fast enough. Based on a comment from [this guy](https://drmrehorst.blogspot.com/2018/04/the-mother-of-all-print-cooling-fans.html) I'm expecting it to draw somewhere around 12 watts -- but it pulls around 5 if I crank the voltage up really high. Short of increasing the diameter of the impeller, not really sure what to do. Since changing the diameter of the impeller means redoing all of the volute chamber, I want to experiment with a few things before then:

1. Longer, curvier vanes: these vanes are basically straight
2. Thicker vanes: I already broke one of them lol. In the final product, I think I'll print the impeller in separate pieces (the vanes, and the base that has cutouts for the vanes) and epoxy them together for better strength.
3. Vanes that do a sort of spiral-y thing. Might make it more efficient at pulling in air. 
4. Shorter vane _height_ . Right now impeller is almost as tall as the casing. I've noticed air being thrown out of the top and maybe it's because the impeller is too high.

That being said, I need to do some more quantitative testing. For that, I think I need:

1. Some sort of test jig for measuring static pressure.
2. Something to measure the RPM of the impeller. I'd probably need to buy something off of the interwebs.

I have some tubing and I'm currently making some brackets and adaptors for the test harness. More to come!
