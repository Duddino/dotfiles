from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.lazy import lazy
from libqtile import layout, bar, widget

from typing import List  # noqa: F401
import os
import subprocess
from libqtile import hook

current_project_path = "/home/duddino/SocialDeductionGame"
mod = "mod4"

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "h", lazy.layout.left()),
    # Move windows up or down in current stack
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),

    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),
    # Grow and shrink
    Key([mod], "b", lazy.layout.grow()),
    Key([mod], "n", lazy.layout.shrink()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("alacritty")),
    Key([mod], "q", lazy.spawn("qutebrowser")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"],  "q", lazy.window.kill()),

    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "e", lazy.shutdown()),
    Key([mod], "d", lazy.spawn("rofi -show run")),
    # Toggle fullscreen
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    # Toggle floating mode
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
    # Audio commands
    Key([], "XF86AudioMute", lazy.spawn("amixer -c 1 set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 1 sset Master 10%- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 1 sset Master 10%+ unmute")),
    # Open vim in my current project
    Key([mod], "p", lazy.spawn("alacritty --working-directory " + current_project_path + " -e vim")),
]


terminal_icon = ''
games_icon = ''
firefox_icon = ''
code_icon = ''
code2_icon = ''
music_icon = ''

groups = [
    Group(terminal_icon),
    Group(firefox_icon, matches=[Match(wm_class=["firefox"])]),
    Group(code_icon),
    Group(code2_icon),
    Group(music_icon),
] + [Group(i) for i in "6789"] + [Group(games_icon, matches=[Match(wm_class=["Steam"])])]
group_key_bindings = [i for i in "1234567890"]

for group, key_binding in zip(groups, group_key_bindings):
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], key_binding, lazy.group[group.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], key_binding, lazy.window.togroup(group.name, switch_group=True)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

gaps_width = 8
layouts = [
    # layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    layout.MonadTall(margin=gaps_width, border_focus="#203C2B", single_margin=0),
    layout.MonadWide(margin=gaps_width, border_focus="#203C2B", single_margin=0),
    # layout.Max(),
    layout.RatioTile(margin=int(gaps_width/2), border_focus="#203C2B", single_margin=0),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Hasklig',
    fontsize=15,
    padding=3,
)
extension_defaults = widget_defaults.copy()

background_color = "#000000" #111D13
foreground_color = "#203C2B"
time_bg_color = "#006400"
volume_bg_color = "#013220"

screens = [
    Screen(
        top = bar.Bar(
            [
                widget.Image(
                    filename = '/usr/share/backgrounds/arch.png',
                    margin = 3,
                ),
                widget.Image(
                    filename = '/usr/share/backgrounds/vim.png',
                    margin = 3,
                ),
                widget.CurrentLayout(background = background_color),
                widget.GroupBox(
                    background = background_color,
                    block_highlight_text_color = "#00FF00",
                    this_current_screen_border = foreground_color,
                    use_mouse_wheel = False,
                    disable_drag = True,
                    rounded = True,
                    highlight_method = "line",
                ),
                # Hack: Not used to display the window name, but to separate the bar
                widget.WindowName(fmt=''),
                widget.Cmus(fmt = ''),
                widget.TextBox(
                    text = "",
                    padding = 0,
                    fontsize = 45,
                    foreground = volume_bg_color,
                ),
                widget.PulseVolume(background = volume_bg_color, fmt = " {}"),
                widget.TextBox(
                    text = "",
                    padding = 0,
                    fontsize = 45,
                    foreground = time_bg_color,
                    background = volume_bg_color,
                ),
                widget.Clock(background = time_bg_color, format='%Y/%m/%d %a %I:%M %p'),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call(home)
