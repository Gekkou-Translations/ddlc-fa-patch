# Right to left override
define config.rtl = True
define config.default_language = "Persian"

# Font overrides
translate Persian python:
    gui.default_font = "gui/font/Sahel.ttf"
    gui.name_font = "gui/font/Estedad-Black.ttf"
    gui.interface_font = "gui/font/Sahel.ttf"
    gui.choice_button_borders = Borders(10, 5, 10, 5)

translate Persian style default:
    font "gui/font/Sahel.ttf"
    shaper "harfbuzz"
    line_spacing -4

translate Persian style normal:
    outlines [(2, "#444", 0, 0), (1, "#444", 2, 2)]
    shaper "harfbuzz"
    reading_order "rtl"
    ypos 55
    xpos 1012
    xminimum 744
    language "western"
    textalign 1.0
    xalign 1.0

translate Persian style say_dialogue:
    ypos 55
    xpos 1012
    xminimum 744
    textalign 1.0
    xalign 1.0

translate Persian style button_text:
    font "gui/font/Sahel.ttf"
    shaper "harfbuzz"

translate Persian style check_button_text:
    font "gui/font/Mikhak-DS2-Regular.ttf"
    shaper "harfbuzz"

translate Persian style choice_button_text:
    font "gui/font/Sahel.ttf"
    shaper "harfbuzz"

translate Persian style edited:
    font "gui/font/ScheherazadeNew-Bold.ttf"
    shaper "harfbuzz"
    ypos 55
    xpos 1012
    xminimum 744
    textalign 1.0
    xalign 1.0

translate Persian style splash_text:
    shaper "harfbuzz"
    reading_order "rtl"

translate Persian style game_menu_label_text:
    font "gui/font/Estedad-Black.ttf"
    shaper "harfbuzz"

translate Persian style navigation_button_text:
    font "gui/font/Estedad-Black.ttf"
    shaper "harfbuzz"

translate Persian style poemgame_text:
    font "gui/font/Mikhak-DS2-Regular.ttf"
    shaper "harfbuzz"

translate Persian style pref_label_text:
    font "gui/font/Estedad-Black.ttf"
    shaper "harfbuzz"

translate Persian style radio_button_text:
    font "gui/font/Mikhak-DS2-Regular.ttf"
    shaper "harfbuzz"

# Poems
translate Persian style yuri_text:
    font "gui/font/AShekari.ttf"
    shaper "harfbuzz"
    xpos 50
    size 32
    min_width 660
    xsize 660
    line_spacing 20
    textalign 1.0

translate Persian style yuri_text_2:
    font "gui/font/Mj_Ghalam-2.ttf"
    shaper "harfbuzz"
    xpos 50
    size 36
    min_width 660
    xsize 660
    line_spacing 20
    textalign 1.0

translate Persian style yuri_text_3:
    font "gui/font/AFSANEH.ttf"
    shaper "harfbuzz"
    xpos 50
    size 27
    kerning -6
    min_width 660
    xsize 660
    language "western"
    line_spacing 20
    textalign 1.0

translate Persian style natsuki_text:
    font "gui/font/DigiNozhaRegular.ttf"
    shaper "harfbuzz"
    xpos 50
    size 30
    min_width 660
    xsize 660
    line_spacing 20
    textalign 1.0

translate Persian style sayori_text:
    font "gui/font/DigiEin-GhafRegular.ttf"
    shaper "harfbuzz"
    xpos 50
    size 30
    min_width 660
    xsize 660
    line_spacing 20
    textalign 1.0

translate Persian style monika_text:
    font "gui/font/Farid.ttf"
    shaper "harfbuzz"
    xpos 50
    size 28
    min_width 660
    xsize 660
    line_spacing -10
    textalign 1.0

translate Persian style poem_vbar:
    xpos 260

# Credits
translate Persian style credits_header:
    font "gui/font/Sahel.ttf"
    shaper "harfbuzz"

translate Persian style credits_text:
    font "gui/font/Mikhak-DS2-Regular.ttf"
    shaper "harfbuzz"

style monika_credits_text_Persian is monika_credits_text:
    font "gui/font/Farid.ttf"
    size 28
    line_spacing 20
    min_width 800

translate Persian style subtitles:
    font "gui/font/Sahel.ttf"
    shaper "harfbuzz"
    reading_order None
    xalign 0.5

translate Persian python:
    # Dialog suffixes and prefixes
    for char in [mc, s, m, n, y, ny]:
        char.what_prefix = '«'
        char.what_suffix = '»'

    # Replace .chr files
    recreate_character('sayori')
    recreate_character('monika')
    recreate_character('natsuki')
    recreate_character('yuri')

    # README file
    readme_file = "README_fa.html"

# Ending
image mcredits_1a_Persian:
    ypos credits_ypos_tl
    xoffset 144
    MusicSyncedCreditText("Every day,{#translate}", 6.03, 15.0, style="monika_credits_text_Persian", reverse=True)
image mcredits_1b_Persian:
    ypos credits_ypos_tl
    xoffset 35
    MusicSyncedCreditText("I imagine a future where{#translate}", 9.0, 12.0, style="monika_credits_text_Persian", reverse=True)
image mcredits_1c_Persian:
    ypos credits_ypos_tl
    xoffset -109
    MusicSyncedCreditText("I can be with you{#translate}", 10.0, 14.5, style="monika_credits_text_Persian", reverse=True)
image mcredits_2a_Persian:
    ypos credits_ypos_tl + 65
    xoffset 141
    MusicSyncedCreditText("In my hand{#translate}", 15.7, 13.0, style="monika_credits_text_Persian", reverse=True)
image mcredits_2b_Persian:
    ypos credits_ypos_tl + 65
    xoffset 15
    MusicSyncedCreditText(" is a pen that will write a poem{#translate}", 18.4, 10.9, style="monika_credits_text_Persian", reverse=True)
image mcredits_2c_Persian:
    ypos credits_ypos_tl + 65
    xoffset -121
    MusicSyncedCreditText("of me and you{#translate}", 19.0, 15.5, style="monika_credits_text_Persian", reverse=True)
image mcredits_3_Persian:
    ypos credits_ypos_tl + 115
    MusicSyncedCreditText("The ink flows down into a dark puddle{#translate}", 24.4, 19.2, style="monika_credits_text_Persian", reverse=True)
image mcredits_4_Persian:
    ypos credits_ypos_tl + 175
    MusicSyncedCreditText(" Just move your hand -- write the way into his heart!{#translate}", 30.9, 11.9, style="monika_credits_text_Persian", reverse=True)
image mcredits_5_Persian:
    ypos credits_ypos_tl + 230
    MusicSyncedCreditText("But in this world of infinite choices{#translate}", 34.5, 16.0, style="monika_credits_text_Persian", reverse=True)
image mcredits_6a_Persian:
    ypos credits_ypos_tl + 290
    xoffset 94
    MusicSyncedCreditText(" What will it take{#translate}", 37.9, 15.0, style="monika_credits_text_Persian", reverse=True)
image mcredits_6b_Persian:
    ypos credits_ypos_tl + 290
    xoffset -31
    MusicSyncedCreditText(" just to find that special day?{#translate}", 40.92, 11.6, style="monika_credits_text_Persian", reverse=True)
