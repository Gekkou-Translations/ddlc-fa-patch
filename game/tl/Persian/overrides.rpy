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
    "black"
    3.0
    Text("Every day,{#translate}", style="monika_credits_text_Persian") with ImageDissolve("images/menu/wipeleft.png", 10.66, ramplen=4, reverse=True, alpha=False)
image mcredits_1b_Persian:
    ypos credits_ypos_tl
    xoffset 35
    "black"
    5.1
    Text("I imagine a future where{#translate}", style="monika_credits_text_Persian") with ImageDissolve("images/menu/wipeleft.png", 10.5, ramplen=4, reverse=True, alpha=False)
image mcredits_1c_Persian:
    ypos credits_ypos_tl
    xoffset -109
    "black"
    3.7
    Text("I can be with you{#translate}", style="monika_credits_text_Persian") with ImageDissolve("images/menu/wipeleft.png", 15.0, ramplen=4, reverse=True, alpha=False)
image mcredits_2a_Persian:
    ypos credits_ypos_tl + 65
    xoffset 141
    "black"
    10.4
    Text("In my hand{#translate}", style="monika_credits_text_Persian") with ImageDissolve("images/menu/wipeleft.png", 13.0, ramplen=4, reverse=True, alpha=False)
image mcredits_2b_Persian:
    ypos credits_ypos_tl + 65
    xoffset 15
    "black"
    14.8
    Text(" is a pen that will write a poem{#translate}", style="monika_credits_text_Persian") with ImageDissolve("images/menu/wipeleft.png", 9.8, ramplen=4, reverse=True, alpha=False)
image mcredits_2c_Persian:
    ypos credits_ypos_tl + 65
    xoffset -121
    "black"
    13.7
    Text("of me and you{#translate}", style="monika_credits_text_Persian") with ImageDissolve("images/menu/wipeleft.png", 14.0, ramplen=4, reverse=True, alpha=False)
image mcredits_3_Persian:
    ypos credits_ypos_tl + 115
    "black"
    17.5
    Text("The ink flows down into a dark puddle{#translate}", style="monika_credits_text_Persian") with ImageDissolve("images/menu/wipeleft.png", 17.9, ramplen=4, reverse=True, alpha=False)
image mcredits_4_Persian:
    ypos credits_ypos_tl + 175
    "black"
    27.8
    Text(" Just move your hand -- write the way into his heart!{#translate}", style="monika_credits_text_Persian") with ImageDissolve("images/menu/wipeleft.png", 9.7, ramplen=4, reverse=True, alpha=False)
image mcredits_5_Persian:
    ypos credits_ypos_tl + 230
    "black"
    29.5
    Text("But in this world of infinite choices{#translate}", style="monika_credits_text_Persian") with ImageDissolve("images/menu/wipeleft.png", 13.7, ramplen=4, reverse=True, alpha=False)
image mcredits_6a_Persian:
    ypos credits_ypos_tl + 290
    xoffset 94
    "black"
    31.75
    Text(" What will it take{#translate}", style="monika_credits_text_Persian") with ImageDissolve("images/menu/wipeleft.png", 14.8, ramplen=4, reverse=True, alpha=False)
image mcredits_6b_Persian:
    ypos credits_ypos_tl + 290
    xoffset -31
    "black"
    37.82
    Text(" just to find that special day?{#translate}", style="monika_credits_text_Persian") with ImageDissolve("images/menu/wipeleft.png", 9.2, ramplen=4, reverse=True, alpha=False)
