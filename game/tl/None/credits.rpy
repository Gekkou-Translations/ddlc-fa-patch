# Copyright (c) yorkyang2333
# The following python classes and functions are borrowed from
# https://github.com/yorkyang2333/ddlc-renpy8

init python:
    import datetime
    import math

    CREDITS_WIPE_WIDTH = 1280.0
    CREDITS_WIPE_FEATHER = 32

    def _credits_music_elapsed(base=0.0, channel="music"):
        try:
            pos = renpy.music.get_pos(channel)
        except Exception:
            pos = None

        if pos is None:
            return None

        # Some backends report the absolute file position for "<from 50.0>",
        # while others report segment-local time. Support both.
        if base and pos >= base - 5.0:
            return max(0.0, pos - base)

        return max(0.0, pos)

    def _credits_wall_elapsed(fallback_start):
        if fallback_start is None:
            return None

        return (datetime.datetime.now() - fallback_start).total_seconds()

    def pause_until_music_relative(relative_target, base=0.0, fallback_start=None, channel="music"):
        if fallback_start is None:
            fallback_start = datetime.datetime.now()

        while True:
            elapsed = _credits_music_elapsed(base=base, channel=channel)

            if elapsed is None:
                elapsed = _credits_wall_elapsed(fallback_start)

            if elapsed is None:
                delay = relative_target
            else:
                delay = relative_target - elapsed

            if delay <= 0:
                return

            renpy.pause(min(delay, 0.25), hard=True)

    class MusicSyncedCreditText(renpy.Displayable):
        def __init__(self, text, start, duration, style="monika_credits_text", base=0.0, channel="music", reverse=False):
            super(MusicSyncedCreditText, self).__init__()
            self.child = Text(text, style=style)
            self.start = float(start)
            self.duration = max(float(duration), 0.001)
            self.base = float(base)
            self.channel = channel
            self.reverse = reverse
            self._cached_size = None

        def visit(self):
            return [self.child]

        def _elapsed(self, st):
            elapsed = _credits_music_elapsed(base=self.base, channel=self.channel)
            if elapsed is None:
                elapsed = st
            return elapsed

        def render(self, width, height, st, at):
            elapsed = self._elapsed(st)
            raw_progress = (elapsed - self.start) / self.duration

            if raw_progress <= 0.0 and self._cached_size is not None:
                rv = renpy.Render(self._cached_size[0], self._cached_size[1])
                renpy.redraw(self, min(max(self.start - elapsed, 0.0), 0.05))
                return rv

            child_render = renpy.render(self.child, width, height, st, at)
            self._cached_size = (child_render.width, child_render.height)
            rv = renpy.Render(child_render.width, child_render.height)

            if raw_progress <= 0.0:
                renpy.redraw(self, min(max(self.start - elapsed, 0.0), 0.05))
                return rv

            progress = max(0.0, min(1.0, raw_progress))

            if progress >= 1.0:
                rv.blit(child_render, (0, 0))
                return rv

            edge = CREDITS_WIPE_WIDTH * progress
            solid_width = int(max(0, min(child_render.width, math.floor(edge))))

            if solid_width:
                if self.reverse:
                    rv.blit(child_render.subsurface((child_render.width - solid_width, 0, solid_width, child_render.height)), (child_render.width - solid_width, 0))
                else:
                    rv.blit(child_render.subsurface((0, 0, solid_width, child_render.height)), (0, 0))

            feather_start = solid_width
            feather_width = int(max(0, min(CREDITS_WIPE_FEATHER, child_render.width - feather_start)))

            if feather_width > 0:
                for x in range(feather_width):
                    alpha = 1.0 - (float(x + 1) / float(CREDITS_WIPE_FEATHER + 1))
                    strip = renpy.Render(1, child_render.height)
                    if self.reverse:
                        strip.blit(child_render.subsurface((child_render.width - (feather_start + x), 0, 1, child_render.height)), (0, 0))
                    else:
                        strip.blit(child_render.subsurface((feather_start + x, 0, 1, child_render.height)), (0, 0))
                    strip.alpha = alpha
                    strip.add_shader("renpy.alpha")
                    strip.add_uniform("u_renpy_alpha", alpha)
                    strip.add_uniform("u_renpy_over", 1.0)
                    if self.reverse:
                        rv.blit(strip, (child_render.width - (feather_start + x), 0))
                    else:
                        rv.blit(strip, (feather_start + x, 0))

            renpy.redraw(self, 0)

            return rv

    class MusicSyncedBlackFade(renpy.Displayable):
        def __init__(self, start, duration, base=0.0, channel="music", size=(1280, 720)):
            super(MusicSyncedBlackFade, self).__init__()
            self.start = float(start)
            self.duration = max(float(duration), 0.001)
            self.base = float(base)
            self.channel = channel
            self.size = size

        def _elapsed(self, st):
            elapsed = _credits_music_elapsed(base=self.base, channel=self.channel)
            if elapsed is None:
                elapsed = st
            return elapsed

        def render(self, width, height, st, at):
            rv = renpy.Render(self.size[0], self.size[1])
            elapsed = self._elapsed(st)
            progress = (elapsed - self.start) / self.duration

            if progress <= 0.0:
                renpy.redraw(self, min(max(self.start - elapsed, 0.0), 0.05))
                return rv

            alpha = max(0.0, min(1.0, progress))
            rv.fill((0, 0, 0, int(255 * alpha)))

            if progress < 1.0:
                renpy.redraw(self, 0)

            return rv

define credits_ypos_tl = 430

style monika_credits_text:
    font "gui/font/m1.ttf"
    color "#fff"
    size 40
    text_align 0.5
    min_width 800

image mcredits_1a:
    ypos credits_ypos
    xoffset -205
    MusicSyncedCreditText("Every day,", 7.5, 11.0)
image mcredits_1b:
    ypos credits_ypos
    xoffset -35
    MusicSyncedCreditText("I imagine a future where", 10.0, 8.5)
image mcredits_1c:
    ypos credits_ypos
    xoffset 170
    MusicSyncedCreditText("I can be with you", 11.52, 9.5)
image mcredits_2a:
    ypos credits_ypos + 50
    xoffset -226
    MusicSyncedCreditText("In my hand", 16.85, 9.2)
image mcredits_2b:
    ypos credits_ypos + 50
    xoffset -10
    MusicSyncedCreditText(" is a pen that will write a poem", 19.7, 6.5)
image mcredits_2c:
    ypos credits_ypos + 50
    xoffset 225
    MusicSyncedCreditText("of me and you", 20.87, 9.1)

image mcredits_3:
    ypos credits_ypos + 100
    MusicSyncedCreditText("The ink flows down into a dark puddle", 26.55, 12.0)

image mcredits_4:
    ypos credits_ypos + 150
    xoffset -5
    MusicSyncedCreditText(" Just move your hand -- write the way into his heart!", 31.9, 8.5)

image mcredits_5:
    ypos credits_ypos + 200
    MusicSyncedCreditText("But in this world of infinite choices", 35.6, 12.5)

image mcredits_6a:
    ypos credits_ypos + 250
    xoffset -145
    MusicSyncedCreditText(" What will it take", 40.2, 7.0)
image mcredits_6b:
    ypos credits_ypos + 250
    xoffset 85
    MusicSyncedCreditText(" just to find that special day?", 42.07, 7.5)

image mcredits_7 = MusicSyncedBlackFade(48.62, 1.5)

image mcredits_1_test:
    ypos credits_ypos + 300
    MusicSyncedCreditText("What will it take just to find that special day?", 0.0, 15.0)

style subtitles is normal:
    xmaximum 1000
    textalign 0.0

image subtitles:
    ypos 680
    xoffset -25
    Null(width=1280, height=720)
    9.3
    Fixed(Text("Can you hear me...?", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    1.8
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    1.9
    Fixed(Text("Hi, it's me.", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    1.8
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    1.7
    Fixed(Text("So you know how I've been like, practicing piano and stuff?", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    4.4
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("And - I'm not really any good at it yet... like, at all.", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    4.3
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("But~ I wrote you a song", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    2.2
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("And I was kinda hoping that I could show it to you!", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    2.5
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("Because I worked really... really hard on it.", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    3.2
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("So... yeah!", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    1.8
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)

image lyrics_original:
    ypos 680
    xoffset -25
    Null(width=1280, height=720)
    9.5
    Fixed(Text("Have I found everybody a fun assignment to do today?{#original}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    5.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    3.5
    Fixed(Text("When you're here, everything that we do is fun for them anyway{#original}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    5.5
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    3.5
    Fixed(Text("When I can't even read my own feelings{#original}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    4.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("What good are words when a smile says it all?{#original}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    4.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("And if this world won't write me an ending{#original}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    4.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("What will it take just for me to have it all?{#original}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    4.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    19.5
    Fixed(Text("Does my pen only write bitter words for those who are dear to me?{#original}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    5.5
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    4.0
    Fixed(Text("Is it love if I take you, or is it love if I set you free?{#original}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    5.5
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    8.0
    Fixed(Text("The ink flows down into a dark puddle{#original}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    4.5
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("How can I write love into reality?{#original}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    3.5
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("If I can't hear the sound of your heartbeat{#original}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    4.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("What do you call love in your reality?{#original}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    3.5
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("And in your reality, if I don't know how to love you...{#original}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    5.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    3.5
    Fixed(Text("I'll leave you be{#original}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    2.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)

image lyrics_translate:
    ypos 710
    xoffset -25
    Null(width=1280, height=720)
    9.5
    Fixed(Text("Have I found everybody a fun assignment to do today?{#translate}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    5.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    3.5
    Fixed(Text("When you're here, everything that we do is fun for them anyway{#translate}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    5.5
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    3.5
    Fixed(Text("When I can't even read my own feelings{#translate}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    4.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("What good are words when a smile says it all?{#translate}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    4.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("And if this world won't write me an ending{#translate}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    4.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("What will it take just for me to have it all?{#translate}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    4.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    19.5
    Fixed(Text("Does my pen only write bitter words for those who are dear to me?{#translate}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    5.5
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    4.0
    Fixed(Text("Is it love if I take you, or is it love if I set you free?{#translate}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    5.5
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    8.0
    Fixed(Text("The ink flows down into a dark puddle{#translate2}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    4.5
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("How can I write love into reality?{#translate}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    3.5
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("If I can't hear the sound of your heartbeat{#translate}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    4.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("What do you call love in your reality?{#translate}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    3.5
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    0.5
    Fixed(Text("And in your reality, if I don't know how to love you...{#translate}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    5.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)
    3.5
    Fixed(Text("I'll leave you be{#translate}", style="subtitles", ypos=680, xoffset=-25)) with Dissolve(0.5, alpha=True)
    2.0
    Null(width=1280, height=720) with Dissolve(0.5, alpha=True)

translate None credits:
    label credits:
        $ persistent.autoload = "credits"
        $ renpy.save_persistent()
        $ config.keymap['game_menu'] = []
        $ config.keymap['hide_windows'] = []
        $ renpy.display.behavior.clear_keymap_cache()
        $ quick_menu = False
        $ config.skipping = False
        $ config.allow_skipping = False
        scene black
        play music "bgm/end-voice.ogg" noloop
        
        show subtitles zorder 100

        show noise zorder 9:
            alpha 0.0
            linear 1.5 alpha 1.0
            time 2.0
            parallel:
                0.05
                choice:
                    alpha 0.5
                choice:
                    alpha 0.75
                choice:
                    alpha 1.0
                repeat
            parallel:
                linear 0.375 alpha 0.7
                linear 0.375 alpha 1.0
            time 2.75
            alpha 0.95
            time 6.45
            alpha 0.3
            time 6.95
            alpha 0.9
            time 8.65
            linear 0.8 alpha 0
            alpha 0.5
            time 22.1
            alpha 0.85
            time 22.35
            alpha 0.5
            time 28.20
            alpha 0.3
            linear 0.45 alpha 0.9
            alpha 0.4
        show vignette zorder 10:
            alpha 0.75
            parallel:
                0.36
                alpha 0.75
                repeat
            parallel:
                0.49
                alpha 0.7
                repeat
        show end_glitch1 zorder 2
        show black as bar zorder 9:
            alpha 0.3
            size (1280,500)
            block:
                ypos 720
                linear 15 ypos -500
                repeat

        pause 41
        scene black
        pause 0.5
        $ consolehistory = []
        call updateconsole ("renpy.music.play(\"ddlc.ogg\")", "Playing audio \"ddlc.ogg\"...") from _call_updateconsole_20
        pause 1.0
        call hideconsole from _call_hideconsole_3
        $ credits_music_fallback_start = datetime.datetime.now()
        play music "<to 50.0>bgm/credits.ogg" noloop

        if _preferences.language != None:
            define credits_ypos=90
            show expression "mcredits_1a_" + str(_preferences.language) zorder 50
            show expression "mcredits_1b_" + str(_preferences.language) zorder 49
            show expression "mcredits_1c_" + str(_preferences.language) zorder 48
            show expression "mcredits_2a_" + str(_preferences.language) zorder 47
            show expression "mcredits_2b_" + str(_preferences.language) zorder 46
            show expression "mcredits_2c_" + str(_preferences.language) zorder 45
            show expression "mcredits_3_" + str(_preferences.language) zorder 44
            show expression "mcredits_4_" + str(_preferences.language) zorder 43
            show expression "mcredits_5_" + str(_preferences.language) zorder 42
            show expression "mcredits_6a_" + str(_preferences.language) zorder 41
            show expression "mcredits_6b_" + str(_preferences.language) zorder 40

        show mcredits_1a zorder 50
        show mcredits_1b zorder 49
        show mcredits_1c zorder 48
        show mcredits_2a zorder 47
        show mcredits_2b zorder 46
        show mcredits_2c zorder 45
        show mcredits_3 zorder 44
        show mcredits_4 zorder 43
        show mcredits_5 zorder 42
        show mcredits_6a zorder 41
        show mcredits_6b zorder 40
        show mcredits_7 zorder 51

        if _preferences.language != None:
            show expression "mcredits_1a_" + str(_preferences.language) zorder 50
            show expression "mcredits_1b_" + str(_preferences.language) zorder 49
            show expression "mcredits_1c_" + str(_preferences.language) zorder 48
            show expression "mcredits_2a_" + str(_preferences.language) zorder 47
            show expression "mcredits_2b_" + str(_preferences.language) zorder 46
            show expression "mcredits_2c_" + str(_preferences.language) zorder 45
            show expression "mcredits_3_" + str(_preferences.language) zorder 44
            show expression "mcredits_4_" + str(_preferences.language) zorder 43
            show expression "mcredits_5_" + str(_preferences.language) zorder 42
            show expression "mcredits_6a_" + str(_preferences.language) zorder 41
            show expression "mcredits_6b_" + str(_preferences.language) zorder 40

        $ pause_until_music_relative(50.0, fallback_start=credits_music_fallback_start)
        jump credits2

    label credits2:
        python:
            sayoriTime = renpy.random.random() * 4 + 4
            natsukiTime = renpy.random.random() * 4 + 4
            yuriTime = renpy.random.random() * 4 + 4
            monikaTime = renpy.random.random() * 4 + 4
            sayoriPos = 0
            natsukiPos = 0
            yuriPos = 0
            monikaPos = 0
            sayoriOffset = 0
            natsukiOffset = 0
            yuriOffset = 0
            monikaOffset = 0
            sayoriZoom = 1
            natsukiZoom = 1
            yuriZoom = 1
            monikaZoom = 1
            imagenum = 0
        scene black
        $ consolehistory = []
        $ credits2_music_fallback_start = datetime.datetime.now()
        play music "<from 50.0>bgm/credits.ogg" noloop
        $ pause_until_music_relative(0.88, base=50.0, fallback_start=credits2_music_fallback_start)
        show credits_logo
        show lyrics_original zorder 100
        if _preferences.language != None:
            show lyrics_translate zorder 101
        $ pause_until_music_relative(10.00, base=50.0, fallback_start=credits2_music_fallback_start)
        $ lockedtext = "" if persistent.clear[imagenum] else "_locked"
        $ if persistent.clearall: lockedtext = "_clearall"
        $ imagenum += 1
        show expression ("credits_cg1" + lockedtext) as credits_image_1 at credits_scroll_right
        show credits_header "Concept & Game Design" as credits_header_1 at credits_text_scroll_left
        show credits_text "Dan Salvato" as credits_text_1 at credits_text_scroll_left
        $ lockedtext = "" if persistent.clear[imagenum] else "_locked"
        $ if persistent.clearall: lockedtext = "_clearall"
        $ imagenum += 1
        $ pause_until_music_relative(16.95, base=50.0, fallback_start=credits2_music_fallback_start)
        if not persistent.clearall:
            call updateconsole ("os.remove(\"images/cg/n_cg1.png\")", "n_cg1.png deleted successfully.") from _call_updateconsole_21
        else:
            call updateconsole_clearall ("os.remove(\"images/cg/n_cg1.png\")", "n_cg1.png deleted successfully.") from _call_updateconsole_clearall_10
        show expression ("credits_cg2" + lockedtext) as credits_image_2 at credits_scroll_left
        show credits_header "Character Art" as credits_header_2 at credits_text_scroll_right
        show credits_text "Satchely" as credits_text_2 at credits_text_scroll_right
        $ lockedtext = "" if persistent.clear[imagenum] else "_locked"
        $ if persistent.clearall: lockedtext = "_clearall"
        $ imagenum += 1
        $ pause_until_music_relative(26.05, base=50.0, fallback_start=credits2_music_fallback_start)
        if not persistent.clearall:
            call updateconsole ("os.remove(\"images/cg/n_cg2.png\")", "n_cg2.png deleted successfully.") from _call_updateconsole_22
        else:
            call updateconsole_clearall ("os.remove(\"images/cg/n_cg2.png\")", "n_cg2.png deleted successfully.") from _call_updateconsole_clearall_11
        show expression ("credits_cg3" + lockedtext) as credits_image_1 at credits_scroll_right
        show credits_header "Background Art" as credits_header_1 at credits_text_scroll_left
        show credits_text "Velinquent" as credits_text_1 at credits_text_scroll_left
        $ lockedtext = "" if persistent.clear[imagenum] else "_locked"
        $ if persistent.clearall: lockedtext = "_clearall"
        $ imagenum += 1
        $ pause_until_music_relative(35.15, base=50.0, fallback_start=credits2_music_fallback_start)
        if not persistent.clearall:
            call updateconsole ("os.remove(\"images/cg/y_cg1.png\")", "y_cg1.png deleted successfully.") from _call_updateconsole_23
        else:
            call updateconsole_clearall ("os.remove(\"images/cg/y_cg1.png\")", "y_cg1.png deleted successfully.") from _call_updateconsole_clearall_12
        show expression ("credits_cg4" + lockedtext) as credits_image_2 at credits_scroll_left
        show credits_header "Writing" as credits_header_2 at credits_text_scroll_right
        show credits_text "Dan Salvato" as credits_text_2 at credits_text_scroll_right
        $ lockedtext = "" if persistent.clear[imagenum] else "_locked"
        $ if persistent.clearall: lockedtext = "_clearall"
        $ imagenum += 1
        $ pause_until_music_relative(44.25, base=50.0, fallback_start=credits2_music_fallback_start)
        if not persistent.clearall:
            call updateconsole ("os.remove(\"images/cg/y_cg2.png\")", "y_cg2.png deleted successfully.") from _call_updateconsole_24
        else:
            call updateconsole_clearall ("os.remove(\"images/cg/y_cg2.png\")", "y_cg2.png deleted successfully.") from _call_updateconsole_clearall_13
        show expression ("credits_cg5" + lockedtext) as credits_image_1 at credits_scroll_right
        show credits_header "Music" as credits_header_1 at credits_text_scroll_left
        show credits_text "Dan Salvato" as credits_text_1 at credits_text_scroll_left
        $ lockedtext = "" if persistent.clear[imagenum] else "_locked"
        $ if persistent.clearall: lockedtext = "_clearall"
        $ imagenum += 1
        $ pause_until_music_relative(53.35, base=50.0, fallback_start=credits2_music_fallback_start)
        if not persistent.clearall:
            call updateconsole ("os.remove(\"images/cg/n_cg3.png\")", "n_cg3.png deleted successfully.") from _call_updateconsole_25
        else:
            call updateconsole_clearall ("os.remove(\"images/cg/n_cg3.png\")", "n_cg3.png deleted successfully.") from _call_updateconsole_clearall_14
        show expression ("credits_cg6" + lockedtext) as credits_image_2 at credits_scroll_left
        show credits_header "Vocals" as credits_header_2 at credits_text_scroll_right
        show credits_text "Jillian Ashcraft" as credits_text_2 at credits_text_scroll_right
        $ lockedtext = "" if persistent.clear[imagenum] else "_locked"
        $ if persistent.clearall: lockedtext = "_clearall"
        $ imagenum += 1
        $ pause_until_music_relative(62.45, base=50.0, fallback_start=credits2_music_fallback_start)
        if not persistent.clearall:
            call updateconsole ("os.remove(\"images/cg/y_cg3.png\")", "y_cg3.png deleted successfully.") from _call_updateconsole_26
        else:
            call updateconsole_clearall ("os.remove(\"images/cg/y_cg3.png\")", "y_cg3.png deleted successfully.") from _call_updateconsole_clearall_15
        show expression ("credits_cg7" + lockedtext) as credits_image_1 at credits_scroll_right
        show credits_header "Special Thanks" as credits_header_1 at credits_text_scroll_left
        show credits_text "Masha Gutin\nKagefumi" as credits_text_1 at credits_text_scroll_left
        $ lockedtext = "" if persistent.clear[imagenum] else "_locked"
        $ if persistent.clearall: lockedtext = "_clearall"
        $ imagenum += 1
        $ pause_until_music_relative(71.55, base=50.0, fallback_start=credits2_music_fallback_start)
        if not persistent.clearall:
            call updateconsole ("os.remove(\"images/cg/s_cg1.png\")", "s_cg1.png deleted successfully.") from _call_updateconsole_27
        else:
            call updateconsole_clearall ("os.remove(\"images/cg/s_cg1.png\")", "s_cg1.png deleted successfully.") from _call_updateconsole_clearall_16
        show expression ("credits_cg8" + lockedtext) as credits_image_2 at credits_scroll_left
        show credits_header "Special Thanks" as credits_header_2 at credits_text_scroll_right
        show credits_text "David Evelyn\nCorey Shin" as credits_text_2 at credits_text_scroll_right
        show s_sticker at credits_sticker_1
        show n_sticker at credits_sticker_2
        show y_sticker at credits_sticker_3
        show m_sticker at credits_sticker_4
        $ pause_until_music_relative(80.60, base=50.0, fallback_start=credits2_music_fallback_start)
        $ lockedtext = "" if persistent.clear[imagenum] else "_locked"
        $ if persistent.clearall: lockedtext = "_clearall"
        $ imagenum += 1
        if not persistent.clearall:
            call updateconsole ("os.remove(\"images/cg/s_cg2.png\")", "s_cg2.png deleted successfully.") from _call_updateconsole_28
        else:
            call updateconsole_clearall ("os.remove(\"images/cg/s_cg2.png\")", "s_cg2.png deleted successfully.") from _call_updateconsole_clearall_17
        $ pause_until_music_relative(88.00, base=50.0, fallback_start=credits2_music_fallback_start)
        show expression ("credits_cg9" + lockedtext) as credits_image_1 at credits_scroll_right
        show credits_header "Special Thanks" as credits_header_1 at credits_text_scroll_left
        show credits_text "Alecia Bardachino\nMatt Naples" as credits_text_1 at credits_text_scroll_left
        $ lockedtext = "" if persistent.clear[imagenum] else "_locked"
        $ if persistent.clearall: lockedtext = "_clearall"
        $ pause_until_music_relative(95.00, base=50.0, fallback_start=credits2_music_fallback_start)
        if not persistent.clearall:
            call updateconsole ("os.remove(\"images/cg/s_cg3.png\")", "s_cg3.png deleted successfully.") from _call_updateconsole_29
        else:
            call updateconsole_clearall ("os.remove(\"images/cg/s_cg3.png\")", "s_cg3.png deleted successfully.") from _call_updateconsole_clearall_18
        show expression ("credits_cg10" + lockedtext) as credits_image_2 at credits_scroll_left
        show credits_header "Special Thanks" as credits_header_2 at credits_text_scroll_right
        show credits_text "Monika\n[player]" as credits_text_2 at credits_text_scroll_right
        $ pause_until_music_relative(104.10, base=50.0, fallback_start=credits2_music_fallback_start)
        if not persistent.clearall:
            call updateconsole ("os.remove(\"images/cg/m_cg1.png\")", "m_cg1.png deleted successfully.") from _call_updateconsole_30
        else:
            call updateconsole_clearall ("os.remove(\"images/cg/m_cg1.png\")", "m_cg1.png deleted successfully.") from _call_updateconsole_clearall_19

        call updateconsole ("os.remove(\"game/screens.rpy\")", "screens.rpy deleted successfully.") from _call_updateconsole_31
        call updateconsole ("os.remove(\"game/gui.rpy\")", "gui.rpy deleted successfully.") from _call_updateconsole_32
        call updateconsole ("os.remove(\"game/menu.rpy\")", "menu.rpy deleted successfully.") from _call_updateconsole_33
        call updateconsole ("os.remove(\"game/script.rpy\")", "script.rpy deleted successfully.") from _call_updateconsole_34
        $ pause_until_music_relative(115.72, base=50.0, fallback_start=credits2_music_fallback_start)
        call hideconsole from _call_hideconsole_4
        show credits_ts
        show credits_text "made with love by":
            zoom 0.75 xalign 0.5 yalign 0.25 alpha 0 subpixel True
            linear 2.0 alpha 1
            4.5
            linear 2.0 alpha 0
        pause 9.3
        play sound page_turn
        show poem_end with Dissolve(1)
        label postcredits_loop:
            $ persistent.autoload = "postcredits_loop"
            $ renpy.save_persistent()
            $ config.keymap['game_menu'] = []
            $ config.keymap['hide_windows'] = []
            $ renpy.display.behavior.clear_keymap_cache()
            $ quick_menu = False
            $ config.skipping = False
            $ config.allow_skipping = False
            scene black
            show poem_end
            $ pause()
            call screen dialog(message="Error: Script file is missing or corrupt.\nPlease reinstall the game.", ok_action=Quit(confirm=False))
            return
