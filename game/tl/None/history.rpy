init python:
    def replace_dialogue_to_identifier(h):
        if h.kind != "adv": return

        identifier = renpy.game.context().translate_identifier
        if identifier is None: return
        h.what = "{#" + identifier + "}"

        if len(_history_list) and _history_list[-1].what == h.what: _history_list.pop(-1)

    config.history_callbacks.append(replace_dialogue_to_identifier)

translate None strings:
    old "سایوری"
    new "Sayori"

    old "مونیکا"
    new "Monika"

    old "ناتسوکی"
    new "Natsuki"

    old "یوری"
    new "Yuri"

    old "ناتسوکی و یوری"
    new "Nat & Yuri"

    old "؟؟؟"
    new "???"

    old "دختر ۱"
    new "Girl 1"

    old "دختر ۲"
    new "Girl 2"

    old "دختر ۳"
    new "Girl 3"
