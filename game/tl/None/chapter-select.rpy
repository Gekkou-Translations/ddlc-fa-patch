label chapter_select:
    menu:
        "Act 1":
            menu:
                "Act 1 Day 1":
                    call chapter_select_after(0, 0) from _call_chapter_select_after
                "Act 1 Day 2":
                    call chapter_select_after(0, 1) from _call_chapter_select_after_1
                "Act 1 Day 3":
                    call chapter_select_after(0, 2) from _call_chapter_select_after_2
                "Act 1 Day 4":
                    call chapter_select_after(0, 3) from _call_chapter_select_after_3
                "Act 1 Day 5":
                    call chapter_select_after(0, 4) from _call_chapter_select_after_4
                "Act 1 Day 6":
                    call chapter_select_after(0, 5) from _call_chapter_select_after_5
        "Act 2":
            menu:
                "Act 2 Day 1":
                    call chapter_select_after(1, 0) from _call_chapter_select_after_6
                "Act 2 Day 2":
                    call chapter_select_after(2, 1) from _call_chapter_select_after_7
                "Act 2 Day 3":
                    call chapter_select_after(2, 2) from _call_chapter_select_after_8
                "Act 2 Day 4":
                    call chapter_select_after(2, 3) from _call_chapter_select_after_9
        "Act 3":
            call chapter_select_after(3, 0) from _call_chapter_select_after_10
        "Act 4":
            call chapter_select_after(4, 0) from _call_chapter_select_after_11
        "Ending":
            call chapter_select_after(5, 0) from _call_chapter_select_after_12
    return

label chapter_select_after(playthrough, ch):
    python:
        persistent.playthrough = playthrough
        persistent.autoload = None
        renpy.save_persistent()
        chapter = ch - 1

        s_name = "Sayori"
        m_name = 'Monika'
        n_name = 'Natsuki'
        y_name = 'Yuri'

        quick_menu = True
        style.say_dialogue = style.normal
        in_sayori_kill = None
        allow_skipping = True
        config.allow_skipping = True

        def create_character(name):
            try: renpy.file(config.basedir + "/characters/" + name)
            except: open(config.basedir + "/characters/" + name, "wb").write(renpy.file(name).read())
        def create_file(name):
            try: renpy.file(config.basedir + "/" + name)
            except: open(config.basedir + "/" + name, "wb").write(renpy.file(name).read())
        create_character('sayori.chr')
        create_character('monika.chr')
        create_character('natsuki.chr')
        create_character('yuri.chr')
    call expression "chapter_select_pt" + str(playthrough) +"_day" + str(ch + 1) from _call_expression_26
    return

label chapter_select_pt0_day1:
    jump start
label chapter_select_pt0_day2:
    call poem from _call_poem_7
    call ch1_main from _call_ch1_main_1
    call poemresponse_start from _call_poemresponse_start_6
    call ch1_end from _call_ch1_end_1
label chapter_select_pt0_day3:
    call poem from _call_poem_8
    $ chapter = 2
    call ch2_main from _call_ch2_main_1
    call poemresponse_start from _call_poemresponse_start_7
    call ch2_end from _call_ch2_end_1
label chapter_select_pt0_day4:
    call poem from _call_poem_9
    $ chapter = 3
    call ch3_main from _call_ch3_main_1
    call poemresponse_start from _call_poemresponse_start_8
    call ch3_end from _call_ch3_end_1
label chapter_select_pt0_day5:
    $ chapter = 4
    call ch4_main from _call_ch4_main_1
label chapter_select_pt0_day6:
    $ chapter = 5
    $ create_file('hxppy thxughts.png')
    call ch5_main from _call_ch5_main_1
    call endgame from _call_endgame_1
    return

label chapter_select_pt1_day1:
    $ delete_character("sayori")
    jump start
label chapter_select_pt2_day2:
    jump playthrough2
label chapter_select_pt2_day3:
    call poem (False) from _call_poem_10
    $ create_file('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii.txt')
    $ chapter = 2
    call ch22_main from _call_ch22_main_1
    call poemresponse_start from _call_poemresponse_start_9
    call ch22_end from _call_ch22_end_1
label chapter_select_pt2_day4:
    call poem (False) from _call_poem_11
    $ chapter = 3
    call ch23_main from _call_ch23_main_1
    if y_appeal >= 3:
        call poemresponse_start2 from _call_poemresponse_start2_1
    else:
        call poemresponse_start from _call_poemresponse_start_10
    call ch23_end from _call_ch23_end_1
    return

label chapter_select_pt3_day1:
    $ persistent.autoload = "ch30_main"
    $ renpy.save_persistent()
    $ delete_character("sayori")
    $ delete_character('natsuki')
    $ delete_character('yuri')
    jump ch30_main

label chapter_select_pt4_day1:
    $ delete_character('monika')
    jump start

label chapter_select_pt5_day1:
    $ persistent.autoload = "credits"
    $ renpy.save_persistent()
    jump credits
