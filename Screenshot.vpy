import vapoursynth as vs
from awsmfunc import ScreenGen
import debandshit
core = vs.core

#define the source video file
src = core.lsmas.LWLibavSource("C:\Video\Going Clear\Going Clear_t00.mkv")

#resize to 16 bit
src = core.resize.Point(src, format=vs.YUV420P16)

#the frames to make a screenshot of
frames=[3098,8000] 

#full set of parameters for f3kdb
f3kdb_ranges = [15,20,25]
f3kdb_ys = [64,128,192]
f3kdb_grainys = [64]
f3kdb_graincs = [64]
f3kdb_dynamic_grain=True
f3kdb_sample_mode=4

#full set of parameters for f3kpf
f3kpf_radiuses = [5,10,15]
f3kpf_thresholds = [30, 40, 50]

clip = None;

for frame in frames:
    #trim the video to only have a single frame
    trim = core.std.Trim(src, frame, frame) 
    for f3kdb_range in f3kdb_ranges:
        for f3kdb_y in f3kdb_ys:
            for f3kdb_grainy in f3kdb_grainys:
                for f3kdb_grainc in f3kdb_graincs:
                    #apply f3kdb to the screen
                    neo_f3kdb = core.neo_f3kdb.Deband(trim, range=f3kdb_range, y=f3kdb_y, grainy=f3kdb_grainy, grainc=f3kdb_grainc, dynamic_grain=f3kdb_dynamic_grain, sample_mode=f3kdb_sample_mode)
                    overlay = core.text.Text(neo_f3kdb, "Range:"+str(f3kdb_range)+" y:"+str(f3kdb_y)+" grainy:"+str(f3kdb_grainy)+" grainc:"+str(f3kdb_grainc))
                    overlay = core.text.Text(overlay, "f3kdb", 9)
                    overlay = core.text.Text(overlay, frame, 8)
                    if (clip is None):
                        clip=overlay
                    else:
                        clip=clip+overlay;
    #trim the video to only have a single frame
    trim = core.std.Trim(src, frame, frame) 
    for f3kpf_radius in f3kpf_radiuses:
        for f3kpf_threshold in f3kpf_thresholds:
            #apply f3kpf to the screen
            fk3pf = debandshit.f3kpf(trim, f3kpf_radius, f3kpf_threshold) 
            overlay = core.text.Text(fk3pf, "Radius:"+str(f3kpf_radius)+" Threshold:"+str(f3kpf_threshold))
            overlay = core.text.Text(overlay, "f3kpf", 9)
            overlay = core.text.Text(overlay, frame, 8)
            clip=clip+overlay

clip.set_output();